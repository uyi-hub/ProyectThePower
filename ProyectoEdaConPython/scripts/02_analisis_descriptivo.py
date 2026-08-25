"""
02_analisis_descriptivo.py
----------------------------
Análisis estadístico descriptivo sobre el dataset final (fusión de campañas
+ datos demográficos). Genera por consola los principales estadísticos y
guarda dos tablas de apoyo en data/processed/ que se usan luego en el README
(informe) y en las visualizaciones.
"""

import pandas as pd

RUTA_PROCESSED = "../data/processed"

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)

df = pd.read_csv(f"{RUTA_PROCESSED}/dataset_final.csv")

# Columnas 'ruido' que no aportan valor analítico real (ver justificación
# en el script de limpieza), las dejamos fuera del análisis descriptivo
COLUMNAS_EXCLUIDAS = ["latitude", "longitude", "id", "date", "Dt_Customer", "hoja_origen"]
df_analisis = df.drop(columns=COLUMNAS_EXCLUIDAS)


# ============================================================
# 1. VISIÓN GENERAL
# ============================================================
print("=" * 70)
print("1. VISIÓN GENERAL DEL DATASET")
print("=" * 70)
print(f"Filas: {df.shape[0]:,} | Columnas: {df.shape[1]}")
print("\nDistribución de la variable objetivo (y):")
print(df["y"].value_counts())
print(df["y"].value_counts(normalize=True).round(3) * 100, "%")
print("\n(El dataset está desbalanceado: solo ~11% de los clientes suscribe "
      "el depósito. Esto es importante para no sacar conclusiones erróneas "
      "de comparaciones de medias sin tener en cuenta el tamaño de cada grupo.)")


# ============================================================
# 2. ESTADÍSTICOS DESCRIPTIVOS - VARIABLES NUMÉRICAS
# ============================================================
print("\n" + "=" * 70)
print("2. ESTADÍSTICOS DESCRIPTIVOS (variables numéricas)")
print("=" * 70)
columnas_numericas = [
    "age", "duration", "campaign", "pdays", "previous",
    "emp_var_rate", "cons_price_idx", "cons_conf_idx", "euribor3m", "nr_employed",
    "Income", "Kidhome", "Teenhome", "NumWebVisitsMonth",
]
resumen_numerico = df_analisis[columnas_numericas].describe().T
resumen_numerico["mediana"] = df_analisis[columnas_numericas].median()
print(resumen_numerico.round(2))
resumen_numerico.round(2).to_csv(f"{RUTA_PROCESSED}/resumen_estadistico.csv")


# ============================================================
# 3. MATRIZ DE CORRELACIÓN
# ============================================================
print("\n" + "=" * 70)
print("3. MATRIZ DE CORRELACIÓN (variables numéricas)")
print("=" * 70)
correlacion = df_analisis[columnas_numericas].corr()
print(correlacion.round(2))
correlacion.round(3).to_csv(f"{RUTA_PROCESSED}/matriz_correlacion.csv")

print("\nCorrelaciones más fuertes (excluyendo la diagonal):")
# Extraemos manualmente los pares (i, j) con i < j para no repetir cada
# correlación dos veces (la matriz es simétrica) ni contar la diagonal (1.0)
pares = []
cols = correlacion.columns
for i in range(len(cols)):
    for j in range(i + 1, len(cols)):
        pares.append((cols[i], cols[j], correlacion.iloc[i, j]))
pares_ordenados = sorted(pares, key=lambda x: abs(x[2]), reverse=True)
for var1, var2, valor in pares_ordenados[:8]:
    print(f"  {var1:>16} vs {var2:<16} -> {valor:+.2f}")


# ============================================================
# 4. TASA DE SUSCRIPCIÓN POR VARIABLE CATEGÓRICA
# ============================================================
print("\n" + "=" * 70)
print("4. TASA DE SUSCRIPCIÓN (% de 'yes') POR CATEGORÍA")
print("=" * 70)

variables_categoricas = ["job", "education", "marital", "contact", "poutcome",
                          "default", "housing", "loan"]

tasas = {}
for col in variables_categoricas:
    tasa = (
        df_analisis.groupby(col)["y"]
        .apply(lambda s: (s == "yes").mean() * 100)
        .sort_values(ascending=False)
    )
    tasas[col] = tasa
    print(f"\n--- {col} ---")
    print(tasa.round(1).astype(str) + " %")

tabla_tasas = pd.concat(tasas, names=["variable", "categoria"]).reset_index()
tabla_tasas.columns = ["variable", "categoria", "tasa_suscripcion_%"]
tabla_tasas.to_csv(f"{RUTA_PROCESSED}/tasa_suscripcion_categorias.csv", index=False)


# ============================================================
# 5. COMPARATIVA DE VARIABLES NUMÉRICAS ENTRE SUSCRIPTORES Y NO SUSCRIPTORES
# ============================================================
print("\n" + "=" * 70)
print("5. COMPARATIVA yes vs no (medias) EN VARIABLES NUMÉRICAS")
print("=" * 70)
comparativa = df_analisis.groupby("y")[columnas_numericas].mean().T
comparativa["diferencia_%"] = (
    (comparativa["yes"] - comparativa["no"]) / comparativa["no"] * 100
)
print(comparativa.round(2))
comparativa.round(2).to_csv(f"{RUTA_PROCESSED}/comparativa_yes_no.csv")


# ============================================================
# 6. EVOLUCIÓN TEMPORAL: TASA DE SUSCRIPCIÓN POR MES/AÑO
# ============================================================
print("\n" + "=" * 70)
print("6. TASA DE SUSCRIPCIÓN POR AÑO Y MES DE CONTACTO")
print("=" * 70)
df_fecha = df_analisis.dropna(subset=["contact_year", "contact_month"]).copy()
df_fecha["contact_year"] = df_fecha["contact_year"].astype(int)
df_fecha["contact_month"] = df_fecha["contact_month"].astype(int)

tasa_temporal = (
    df_fecha.groupby(["contact_year", "contact_month"])["y"]
    .apply(lambda s: (s == "yes").mean() * 100)
)
print(tasa_temporal.round(1))
tasa_temporal.round(2).to_csv(f"{RUTA_PROCESSED}/tasa_suscripcion_temporal.csv")


# ============================================================
# 7. RESULTADO DE CAMPAÑA ANTERIOR (poutcome) vs SUSCRIPCIÓN ACTUAL
# ============================================================
print("\n" + "=" * 70)
print("7. TABLA CRUZADA: resultado de campaña anterior vs suscripción actual")
print("=" * 70)
tabla_cruzada = pd.crosstab(df_analisis["poutcome"], df_analisis["y"], normalize="index") * 100
print(tabla_cruzada.round(1))

print("\nAnálisis completado. Tablas de apoyo guardadas en data/processed/.")
