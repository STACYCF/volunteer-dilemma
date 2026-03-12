import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# -----------------------------
# CONFIGURACIÓN VISUAL
# -----------------------------

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (7,5)

# -----------------------------
# CARGAR DATOS
# -----------------------------

df = pd.read_excel("RESULTADOS-VD.xlsx")

# -----------------------------
# LIMPIEZA DE DATOS
# -----------------------------

df_clean = df[[
    "session.config.treatment",
    "volunteer_dilemma.1.player.volunteer",
    "volunteer_dilemma.1.group.id_in_subsession",
    "volunteer_dilemma.1.group.num_volunteers"
]]

df_clean.columns = [
    "treatment",
    "volunteer",
    "group",
    "group_volunteers"
]

# eliminar filas sin decisión
df_clean = df_clean.dropna(subset=["volunteer"])

# convertir a entero
df_clean["volunteer"] = df_clean["volunteer"].astype(int)

# -----------------------------
# MÉTRICAS EXPERIMENTALES
# -----------------------------

# Probabilidad individual de voluntariar
volunteer_rate = df_clean.groupby("treatment")["volunteer"].mean()

# Tasa de no voluntariado (free riding)
free_riding_rate = 1 - volunteer_rate

# Datos a nivel grupo
group_data = df_clean.dropna(subset=["group_volunteers"])

# Promedio de voluntarios por grupo
avg_volunteers = group_data.groupby("treatment")["group_volunteers"].mean()

# Probabilidad de provisión del bien público
public_good_rate = group_data.groupby("treatment")["group_volunteers"].apply(lambda x: (x > 0).mean())

# -----------------------------
# DASHBOARD STREAMLIT
# -----------------------------

st.title("Resultados del Experimento: Dilema del Voluntario")

# -----------------------------
# INDICADORES PRINCIPALES
# -----------------------------

st.subheader("Indicadores principales del experimento")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Tasa de voluntariado (costo bajo)",
    f"{volunteer_rate.get('low_cost',0)*100:.1f}%"
)

col2.metric(
    "Tasa de voluntariado (costo alto)",
    f"{volunteer_rate.get('high_cost',0)*100:.1f}%"
)

col3.metric(
    "Tasa de no voluntariado (free-riding)",
    f"{free_riding_rate.mean()*100:.1f}%"
)

# -----------------------------
# DATOS
# -----------------------------

st.subheader("Vista previa de datos limpios")
st.dataframe(df_clean.head())

# -----------------------------
# RESULTADOS NUMÉRICOS
# -----------------------------

st.subheader("Tasa de voluntariado por tratamiento")
st.write(volunteer_rate)

st.subheader("Promedio de voluntarios por grupo")
st.write(avg_volunteers)

st.subheader("Probabilidad de provisión del bien público")
st.write(public_good_rate)

# -----------------------------
# GRÁFICO 1
# Probabilidad de voluntariado
# -----------------------------

st.subheader("Probabilidad de voluntariar")

fig1, ax1 = plt.subplots()

sns.barplot(
    data=df_clean,
    x="treatment",
    y="volunteer",
    errorbar="ci",
    palette="Set2",
    ax=ax1
)

ax1.set_title("Probabilidad de voluntariado por tratamiento")
ax1.set_xlabel("Tratamiento")
ax1.set_ylabel("Probabilidad de voluntariado")

st.pyplot(fig1)

# -----------------------------
# GRÁFICO 2
# Voluntarios por grupo
# -----------------------------

st.subheader("Promedio de voluntarios por grupo")

fig2, ax2 = plt.subplots()

sns.barplot(
    data=group_data,
    x="treatment",
    y="group_volunteers",
    errorbar="ci",
    palette="Set1",
    ax=ax2
)

ax2.set_title("Promedio de voluntarios por grupo")
ax2.set_xlabel("Tratamiento")
ax2.set_ylabel("Número de voluntarios")

st.pyplot(fig2)

# -----------------------------
# GRÁFICO 3
# Distribución de decisiones
# -----------------------------

st.subheader("Distribución de decisiones de voluntariado")

fig3, ax3 = plt.subplots()

sns.countplot(
    data=df_clean,
    x="volunteer",
    hue="treatment",
    palette="pastel",
    ax=ax3
)

ax3.set_title("Distribución de decisiones (voluntariar vs no voluntariar)")
ax3.set_xlabel("Decisión (1 = voluntariar)")
ax3.set_ylabel("Cantidad")

st.pyplot(fig3)

# -----------------------------
# GRÁFICO 4
# Distribución de voluntarios por grupo
# -----------------------------

st.subheader("Distribución de voluntarios por grupo")

fig4, ax4 = plt.subplots()

sns.histplot(
    data=group_data,
    x="group_volunteers",
    hue="treatment",
    bins=4,
    multiple="stack",
    ax=ax4
)

ax4.set_title("Distribución del número de voluntarios por grupo")
ax4.set_xlabel("Número de voluntarios")
ax4.set_ylabel("Frecuencia")

st.pyplot(fig4)
