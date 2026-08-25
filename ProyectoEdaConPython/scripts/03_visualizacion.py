"""
03_visualizacion.py
---------------------
Genera los gráficos que ilustran los hallazgos del análisis descriptivo
(02_analisis_descriptivo.py) y los guarda como imágenes .png en la carpeta
visualizaciones/, para poder incrustarlos en el README (informe).
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RUTA_PROCESSED = "../data/processed"
RUTA_VIS = "../visualizaciones"

sns.set_theme(style="whitegrid")
PALETA = {"no": "#94a3b8", "yes": "#2563eb"}  # gris para 'no', azul para 'yes'

df = pd.read_csv(f"{RUTA_PROCESSED}/dataset_final.csv")


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(f"{RUTA_VIS}/{nombre}.png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"Guardado: {nombre}.png")


# ============================================================
# 1. Balance de la variable objetivo
# ============================================================
fig, ax = plt.subplots(figsize=(5, 4))
conteo = df["y"].value_counts()
ax.bar(conteo.index, conteo.values, color=[PALETA[c] for c in conteo.index])
for i, v in enumerate(conteo.values):
    ax.text(i, v + 500, f"{v:,}\n({v/len(df)*100:.1f}%)", ha="center")
ax.set_title("Distribución de la variable objetivo (¿suscribió el depósito?)")
ax.set_xlabel("")
ax.set_ylabel("Número de clientes")
guardar(fig, "01_balance_clases")


# ============================================================
# 2. Distribución de la edad
# ============================================================
fig, ax = plt.subplots(figsize=(7, 4))
sns.histplot(df["age"], bins=40, kde=True, color="#2563eb", ax=ax)
ax.set_title("Distribución de la edad de los clientes")
ax.set_xlabel("Edad")
ax.set_ylabel("Frecuencia")
guardar(fig, "02_distribucion_edad")


# ============================================================
# 3. Tasa de suscripción por ocupación (job)
# ============================================================
tasa_job = (
    df.groupby("job")["y"].apply(lambda s: (s == "yes").mean() * 100).sort_values()
)
fig, ax = plt.subplots(figsize=(7, 6))
ax.barh(tasa_job.index, tasa_job.values, color="#2563eb")
ax.set_title("Tasa de suscripción por ocupación")
ax.set_xlabel("% de clientes que suscriben")
guardar(fig, "03_tasa_suscripcion_por_job")


# ============================================================
# 4. Tasa de suscripción por nivel educativo
# ============================================================
tasa_edu = (
    df.groupby("education")["y"].apply(lambda s: (s == "yes").mean() * 100).sort_values()
)
fig, ax = plt.subplots(figsize=(7, 5))
ax.barh(tasa_edu.index, tasa_edu.values, color="#0ea5e9")
ax.set_title("Tasa de suscripción por nivel educativo")
ax.set_xlabel("% de clientes que suscriben")
guardar(fig, "04_tasa_suscripcion_por_educacion")


# ============================================================
# 5. Duración de la llamada según suscripción (boxplot)
# ============================================================
fig, ax = plt.subplots(figsize=(6, 4.5))
sns.boxplot(data=df, x="y", y="duration", hue="y", palette=PALETA, ax=ax, legend=False)
ax.set_title("Duración de la llamada según si el cliente suscribió")
ax.set_xlabel("¿Suscribió?")
ax.set_ylabel("Duración de la llamada (segundos)")
ax.set_ylim(0, 1500)  # recortamos outliers extremos para que el gráfico sea legible
guardar(fig, "05_duracion_llamada_vs_suscripcion")


# ============================================================
# 6. Mapa de calor de correlaciones
# ============================================================
columnas_numericas = [
    "age", "duration", "campaign", "pdays", "previous",
    "emp_var_rate", "cons_price_idx", "cons_conf_idx", "euribor3m", "nr_employed",
]
correlacion = df[columnas_numericas].corr()
fig, ax = plt.subplots(figsize=(8, 6.5))
sns.heatmap(correlacion, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
ax.set_title("Correlación entre indicadores económicos y variables de campaña")
guardar(fig, "06_mapa_correlacion")


# ============================================================
# 7. Evolución de la tasa de suscripción en el tiempo
# ============================================================
df_fecha = df.dropna(subset=["contact_year", "contact_month"]).copy()
df_fecha["periodo"] = (
    df_fecha["contact_year"].astype(int).astype(str)
    + "-"
    + df_fecha["contact_month"].astype(int).astype(str).str.zfill(2)
)
tasa_temporal = (
    df_fecha.groupby("periodo")["y"].apply(lambda s: (s == "yes").mean() * 100).sort_index()
)
fig, ax = plt.subplots(figsize=(12, 4.5))
ax.plot(tasa_temporal.index, tasa_temporal.values, marker="o", color="#2563eb", linewidth=1)
ax.set_title("Evolución mensual de la tasa de suscripción (2015-2019)")
ax.set_xlabel("Periodo (año-mes)")
ax.set_ylabel("% de suscripción")
ax.tick_params(axis="x", rotation=90, labelsize=6)
# Mostramos solo 1 de cada 3 etiquetas para que no se amontonen
for i, label in enumerate(ax.xaxis.get_ticklabels()):
    if i % 3 != 0:
        label.set_visible(False)
guardar(fig, "07_evolucion_temporal_suscripcion")


# ============================================================
# 8. Tasa de suscripción por canal de contacto
# ============================================================
tasa_contacto = df.groupby("contact")["y"].apply(lambda s: (s == "yes").mean() * 100)
fig, ax = plt.subplots(figsize=(5, 4))
ax.bar(tasa_contacto.index, tasa_contacto.values, color="#2563eb")
for i, v in enumerate(tasa_contacto.values):
    ax.text(i, v + 0.3, f"{v:.1f}%", ha="center")
ax.set_title("Tasa de suscripción por canal de contacto")
ax.set_ylabel("% de suscripción")
guardar(fig, "08_tasa_suscripcion_por_canal")


# ============================================================
# 9. Resultado de campaña anterior (poutcome) vs suscripción actual
# ============================================================
tasa_poutcome = df.groupby("poutcome")["y"].apply(lambda s: (s == "yes").mean() * 100)
tasa_poutcome = tasa_poutcome.sort_values()
fig, ax = plt.subplots(figsize=(6, 4))
ax.barh(tasa_poutcome.index, tasa_poutcome.values, color="#2563eb")
for i, v in enumerate(tasa_poutcome.values):
    ax.text(v + 1, i, f"{v:.1f}%", va="center")
ax.set_title("Tasa de suscripción según resultado de la campaña anterior")
ax.set_xlabel("% de suscripción")
guardar(fig, "09_tasa_suscripcion_por_poutcome")


# ============================================================
# 10. Ingresos (Income) según suscripción -- variable demográfica
# ============================================================
fig, ax = plt.subplots(figsize=(6, 4.5))
sns.boxplot(data=df, x="y", y="Income", hue="y", palette=PALETA, ax=ax, legend=False)
ax.set_title("Ingresos anuales del cliente según si suscribió")
ax.set_xlabel("¿Suscribió?")
ax.set_ylabel("Ingresos anuales")
guardar(fig, "10_income_vs_suscripcion")

print("\nTodas las visualizaciones se han generado correctamente.")
