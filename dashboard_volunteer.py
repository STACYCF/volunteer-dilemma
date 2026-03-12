import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# -----------------------------
# Cargar datos
# -----------------------------

df = pd.read_excel("RESULTADOS-VD.xlsx")

# -----------------------------
# Seleccionar columnas importantes
# -----------------------------

df_clean = df[[
    "session.config.treatment",
    "volunteer_dilemma.1.player.volunteer",
    "volunteer_dilemma.1.group.id_in_subsession",
    "volunteer_dilemma.1.group.num_volunteers"
]]

# Renombrar columnas
df_clean.columns = ["treatment","volunteer","group","group_volunteers"]

# Eliminar filas sin decisión
df_clean = df_clean.dropna(subset=["volunteer"])

# Convertir decisión a número
df_clean["volunteer"] = df_clean["volunteer"].astype(int)

# -----------------------------
# MÉTRICAS DEL EXPERIMENTO
# -----------------------------

# Probabilidad de voluntariar
volunteer_rate = df_clean.groupby("treatment")["volunteer"].mean()

# Tasa de no voluntariado (free-riding)
free_riding = 1 - volunteer_rate

# Datos a nivel grupo
group_data = df_clean.dropna(subset=["group_volunteers"])

# Promedio de voluntarios por grupo
avg_volunteers = group_data.groupby("treatment")["group_volunteers"].mean()

# Probabilidad de que exista al menos un voluntario (bien público provisto)
public_good = group_data.groupby("treatment")["group_volunteers"].apply(lambda x: (x > 0).mean())

# -----------------------------
# DASHBOARD
# -----------------------------

st.title("Resultados del Experimento: Dilema del Voluntario")

# KPIs principales
st.subheader("Indicadores principales")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Tasa de voluntariado",
    f"{volunteer_rate.mean()*100:.1f}%"
)

col2.metric(
    "Tasa de no voluntariado",
    f"{free_riding.mean()*100:.1f}%"
)

col3.metric(
    "Provisión del bien público",
    f"{public_good.mean()*100:.1f}%"
)

# -----------------------------
# Datos
# -----------------------------

st.subheader("Datos del experimento (limpios)")
st.dataframe(df_clean)

# -----------------------------
# Tasa de voluntariado
# -----------------------------

st.subheader("Tasa de voluntariado por tratamiento")
st.write(volunteer_rate)

# -----------------------------
# Gráfico 1
# Probabilidad de voluntariar
# -----------------------------

fig, ax = plt.subplots()

sns.barplot(
    data=df_clean,
    x="treatment",
    y="volunteer",
    errorbar="ci"
)

ax.set_title("Probabilidad de voluntariar por tratamiento")
ax.set_xlabel("Tratamiento")
ax.set_ylabel("Probabilidad de voluntariado")

st.pyplot(fig)

# -----------------------------
# Gráfico 2
# Voluntarios por grupo
# -----------------------------

st.subheader("Promedio de voluntarios por grupo")

fig2, ax2 = plt.subplots()

sns.barplot(
    data=group_data,
    x="treatment",
    y="group_volunteers",
    errorbar="ci"
)

ax2.set_title("Promedio de voluntarios por grupo")
ax2.set_xlabel("Tratamiento")
ax2.set_ylabel("Número de voluntarios")

st.pyplot(fig2)

# -----------------------------
# Gráfico 3
# Distribución de decisiones
# -----------------------------

st.subheader("Distribución de decisiones")

fig3, ax3 = plt.subplots()

sns.countplot(
    data=df_clean,
    x="volunteer",
    hue="treatment"
)

ax3.set_title("Decisiones: voluntariar vs no voluntariar")
ax3.set_xlabel("Decisión (1 = voluntariar)")
ax3.set_ylabel("Cantidad")

st.pyplot(fig3)