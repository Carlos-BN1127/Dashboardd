import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 🧩 HU-01: Cargar datos desde un solo CSV con manejo de error
@st.cache_data
def cargar_datos():
    archivo = 'todos_los_codigos.csv'
    st.write(f"Ruta actual: {os.getcwd()}")
    try:
        df = pd.read_csv(archivo)
        st.success(f"Archivo '{archivo}' cargado correctamente.")
        return df
    except FileNotFoundError:
        st.error(f"Archivo '{archivo}' no encontrado. Asegúrate de que el archivo exista y esté en la ruta correcta.")
        return None

# 🧩 HU-02: Procesar datos
def transformar_datos(df):
    df["porcentaje_asistencia"] = (df["asistencias"] / df["totales"]) * 100
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
df_original = cargar_datos()

if df_original is not None:
    df = transformar_datos(df_original)

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
else:
    st.stop()  # Detiene la ejecución si no hay datos

