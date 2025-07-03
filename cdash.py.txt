import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# 🧩 HU-01: Cargar datos desde CSV
@st.cache_data
def cargar_datos():
    calificaciones = pd.read_csv('calificaciones.csv')
    asistencias = pd.read_csv('asistencias.csv')
    alumnos = pd.read_csv('datos_alumnos.csv')
    return calificaciones, asistencias, alumnos

# 🧩 HU-02: Limpiar y unir datos
def transformar_datos(calificaciones, asistencias, alumnos):
    asistencias["porcentaje_asistencia"] = (asistencias["asistencias"] / asistencias["totales"]) * 100
    df = pd.merge(calificaciones, asistencias, on=["id_alumno", "nombre"])
    df = pd.merge(df, alumnos, on=["id_alumno", "nombre"])
    return df

# 🧩 HU-03: Promedio por materia
def promedio_por_materia(df):
    return df.groupby('materia')['calificacion'].mean().reset_index()

# 🧩 HU-07: Alumnos en riesgo
def alumnos_en_riesgo(df):
    return df[(df['porcentaje_asistencia'] < 70) & (df['calificacion'] < 6)]

# 🚀 INICIO DEL DASHBOARD STREAMLIT
st.set_page_config(page_title="Dashboard Académico", layout="wide")
st.title("📊 Dashboard Académico - Proyecto Final Scrum")

# Cargar y transformar datos
calificaciones, asistencias, alumnos = cargar_datos()
df = transformar_datos(calificaciones, asistencias, alumnos)

# 🧩 HU-05: Filtros por grupo y semestre
grupo = st.selectbox("Selecciona un grupo:", sorted(df["grupo"].unique()))
semestre = st.selectbox("Selecciona un semestre:", sorted(df["semestre"].unique()))
filtrado = df[(df["grupo"] == grupo) & (df["semestre"] == semestre)]

# 🧩 HU-03: Gráfico de barras - Promedio por materia
st.subheader("📚 Promedio General por Materia")
promedios = promedio_por_materia(filtrado)
fig1, ax1 = plt.subplots()
sns.barplot(data=promedios, x="materia", y="calificacion", ax=ax1, palette="viridis")
ax1.set_title("Promedio por materia")
ax1.set_ylabel("Calificación promedio")
ax1.set_xlabel("Materia")
st.pyplot(fig1)

# 🧩 HU-04: Gráfico de dispersión
st.subheader("📈 Relación entre Asistencia y Calificación")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=filtrado, x="porcentaje_asistencia", y="calificacion", hue="materia", ax=ax2)
ax2.set_title("Dispersión Asistencia vs Calificación")
st.pyplot(fig2)

# 🧩 HU-07: Alumnos en riesgo
st.subheader("🚨 Alumnos en Riesgo de Reprobación")
riesgo = alumnos_en_riesgo(filtrado)
st.dataframe(riesgo)

# 🧩 HU-06: Estética y pie de página
st.markdown("<hr><center><i>Desarrollado por el equipo Scrum ✨</i></center>", unsafe_allow_html=True)