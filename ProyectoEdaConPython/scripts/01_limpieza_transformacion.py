"""
01_limpieza_transformacion.py
------------------------------
Carga los dos datasets en bruto (bank-additional.csv y customer-details.xlsx),
detecta y corrige los problemas de calidad encontrados durante la exploración
inicial, y guarda:
    - data/processed/bank_clean.csv        -> campañas de marketing, limpio
    - data/processed/customer_clean.csv    -> datos demográficos, limpio (3 hojas unidas)
    - data/processed/dataset_final.csv     -> unión de ambos por el ID de cliente

Todas las decisiones de limpieza están documentadas en el README del proyecto,
en la sección "Transformación y limpieza de datos".
"""

import pandas as pd
import numpy as np

RUTA_RAW = "../data/raw"
RUTA_PROCESSED = "../data/processed"

# Diccionario de meses en español -> número de mes.
# La columna 'date' llega en formato "2-agosto-2019", que no es directamente
# parseable por pandas (no reconoce nombres de mes en español), así que
# construimos el mapeo manualmente.
MESES_ES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10,
    "noviembre": 11, "diciembre": 12,
}


# ============================================================
# 1. LIMPIEZA DE 'bank-additional.csv'
# ============================================================
def cargar_y_limpiar_bank(ruta_csv):
    df = pd.read_csv(ruta_csv)

    # --- Columnas sobrantes ---
    # 'Unnamed: 0' es un índice residual guardado por error al exportar el CSV
    df = df.drop(columns=["Unnamed: 0"])

    # --- Normalizar nombres de columnas ---
    # Sustituimos los puntos por guiones bajos para poder acceder a las
    # columnas como atributos y evitar errores en operaciones futuras
    # (ej. df.emp_var_rate en vez de df['emp.var.rate'])
    df.columns = [c.replace(".", "_") for c in df.columns]
    df = df.rename(columns={"id_": "id"})

    # --- Estandarizar texto en columnas categóricas ---
    # 'marital' y 'poutcome' venían en MAYÚSCULAS mientras que 'job',
    # 'education', 'contact' y 'y' venían en minúsculas. Unificamos todo
    # a minúsculas para que no se traten como categorías distintas.
    columnas_categoricas = ["job", "marital", "education", "contact", "poutcome", "y"]
    for col in columnas_categoricas:
        df[col] = df[col].str.strip().str.lower()

    # --- Valores faltantes en categóricas ---
    # El dataset original de UCI (bank-marketing) usa la categoría "unknown"
    # para estos mismos casos, así que seguimos esa misma convención en vez
    # de eliminar filas (perderíamos ~4% de los registros).
    for col in ["job", "marital", "education"]:
        df[col] = df[col].fillna("unknown")

    # --- default / housing / loan ---
    # Vienen como float 0.0/1.0/NaN. Los convertimos a texto "yes"/"no"/"unknown"
    # porque es más legible en el análisis y evita interpretar el NaN como un 0.
    mapa_binario = {1.0: "yes", 0.0: "no"}
    for col in ["default", "housing", "loan"]:
        df[col] = df[col].map(mapa_binario).fillna("unknown")

    # --- age ---
    # ~12% de valores nulos. Imputamos con la mediana de edad DEL MISMO
    # trabajo (job), ya que la edad varía sistemáticamente según la
    # ocupación (ej. 'student' vs 'retired'); es más preciso que usar
    # una única mediana global.
    df["age"] = df.groupby("job")["age"].transform(lambda s: s.fillna(s.median()))

    # --- columnas numéricas con coma decimal (formato europeo) ---
    # cons.price.idx, cons.conf.idx, euribor3m y nr.employed llegan como
    # texto tipo "93,994" en vez de 93.994, porque el CSV se exportó con
    # configuración regional europea. Sustituimos la coma por un punto y
    # convertimos a float.
    columnas_coma = ["cons_price_idx", "cons_conf_idx", "euribor3m", "nr_employed"]
    for col in columnas_coma:
        df[col] = df[col].astype(str).str.replace(",", ".", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- Indicadores económicos con nulos ---
    # Estos 4 indicadores (emp_var_rate, cons_price_idx, cons_conf_idx,
    # euribor3m, nr_employed) reflejan la situación económica de un
    # periodo concreto, no del cliente individual: todos los registros
    # contactados en el mismo mes/año comparten (casi) el mismo valor.
    # Por eso, en vez de imputar con la media global, rellenamos con la
    # mediana del propio mes/año una vez tengamos esas columnas creadas
    # (ver más abajo, después de parsear la fecha).

    # --- date: parsear fecha en español y extraer mes/año ---
    def parsear_fecha(valor):
        if pd.isna(valor):
            return pd.NaT
        try:
            dia, mes_texto, anio = valor.split("-")
            mes_num = MESES_ES[mes_texto.lower()]
            return pd.Timestamp(year=int(anio), month=mes_num, day=int(dia))
        except (KeyError, ValueError):
            return pd.NaT

    df["date"] = df["date"].apply(parsear_fecha)
    # El enunciado menciona las columnas 'contact_month' y 'contact_year',
    # que no existían como tal en el CSV recibido: las derivamos de 'date'.
    df["contact_month"] = df["date"].dt.month
    df["contact_year"] = df["date"].dt.year

    # Ahora que tenemos mes/año, imputamos los indicadores económicos
    # faltantes con la mediana de su propio periodo (mes+año)
    for col in ["cons_price_idx", "euribor3m"]:
        df[col] = df.groupby(["contact_year", "contact_month"])[col].transform(
            lambda s: s.fillna(s.median())
        )

    # --- pdays ---
    # El valor 999 es un código especial que significa "nunca contactado
    # antes", no un número real de días. Lo dejamos tal cual (es la
    # convención estándar de este dataset), pero añadimos una columna
    # booleana explícita para que el análisis no lo confunda con un dato
    # numérico real.
    df["contactado_previamente"] = df["pdays"] != 999

    # --- latitude / longitude ---
    # Estas dos columnas no aparecen descritas en el enunciado y sus valores
    # corresponden a coordenadas de EE. UU., no de Portugal (donde opera el
    # banco). Todo apunta a que son datos sintéticos/ruido sin relación real
    # con el negocio, así que se conservan en el csv limpio por transparencia,
    # pero se excluyen del análisis y del informe.

    # --- duplicados ---
    duplicados = df.duplicated().sum()
    if duplicados > 0:
        df = df.drop_duplicates()
    print(f"[bank] Duplicados eliminados: {duplicados}")

    return df


# ============================================================
# 2. LIMPIEZA DE 'customer-details.xlsx'
# ============================================================
def cargar_y_limpiar_customer(ruta_xlsx):
    hojas = pd.read_excel(ruta_xlsx, sheet_name=None)  # dict {nombre_hoja: df}

    dataframes = []
    for nombre_hoja, df_hoja in hojas.items():
        df_hoja = df_hoja.drop(columns=["Unnamed: 0"])
        # Guardamos de qué hoja viene cada cliente como columna de control,
        # útil para comprobar que coincide con el año real de Dt_Customer
        df_hoja["hoja_origen"] = nombre_hoja
        dataframes.append(df_hoja)

    df = pd.concat(dataframes, ignore_index=True)
    df = df.rename(columns={"ID": "id"})

    # Comprobación de consistencia: ¿el año de Dt_Customer coincide con
    # el nombre de la hoja de la que viene? (lo mostramos por consola,
    # no detiene el proceso si hay discrepancias, solo informa)
    discrepancias = (df["Dt_Customer"].dt.year.astype(str) != df["hoja_origen"]).sum()
    print(f"[customer] Registros cuyo año de alta no coincide con su hoja: {discrepancias}")

    # --- duplicados ---
    duplicados_id = df["id"].duplicated().sum()
    print(f"[customer] IDs duplicados: {duplicados_id}")

    return df


# ============================================================
# 3. UNIÓN DE AMBOS DATASETS
# ============================================================
def unir_datasets(df_bank, df_customer):
    # Unión por el identificador de cliente. Usamos 'inner' porque el
    # análisis de campañas (bank) solo tiene sentido cruzado con las
    # características demográficas de esos mismos clientes.
    df_final = df_bank.merge(df_customer, on="id", how="inner")

    solo_en_customer = set(df_customer["id"]) - set(df_bank["id"])
    print(f"[merge] Clientes en customer-details sin campañas asociadas: {len(solo_en_customer)}")
    print(f"[merge] Registros en el dataset final: {len(df_final)}")

    return df_final


# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    df_bank = cargar_y_limpiar_bank(f"{RUTA_RAW}/bank-additional.csv")
    df_customer = cargar_y_limpiar_customer(f"{RUTA_RAW}/customer-details.xlsx")
    df_final = unir_datasets(df_bank, df_customer)

    df_bank.to_csv(f"{RUTA_PROCESSED}/bank_clean.csv", index=False)
    df_customer.to_csv(f"{RUTA_PROCESSED}/customer_clean.csv", index=False)
    df_final.to_csv(f"{RUTA_PROCESSED}/dataset_final.csv", index=False)

    print("\nArchivos generados en data/processed/:")
    print(" - bank_clean.csv")
    print(" - customer_clean.csv")
    print(" - dataset_final.csv")

    print("\nResumen de nulos restantes en dataset_final:")
    print(df_final.isnull().sum()[df_final.isnull().sum() > 0])
