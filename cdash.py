import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def cargar_datos():
    df = pd.read_csv('todos_los_codigos.csv', sep='\t')  # tu CSV tiene tabulación como separador
    return df

def preparar_datos(df):
    # No necesitas calcular porcentaje_asistencia porque ya existe
    return df

def promedio_por_materia(df):
    # Convertimos columnas de calificaciones a formato largo para agrupar por materia
    df_melt = df.melt(
        id_vars=["semestre", "grupo", "id_alumno", "nombre", "promedio_final", "porcentaje_asistencias"],
        value_vars=[
            "calificaciones_matematicas",
            "calificaciones_ciencias",
            "calificaciones_historia",
            "calificaciones_espanol",
            "calificaciones_ingles"
        ],
        var_name="materia",
        value_name="calificacion"
    )
    # Limpiamos nombres de materia para que se vean bien
    df_melt["materia"] = df_melt["materia"].str.replace("calificaciones_", "").str.capitalize()
    
    promedio = df_melt.groupby("materia")["calificacion"].mean().reset_index()
    return promedio, df_melt

def alumnos_en_riesgo(df_melt):
    # Filtrar alumnos con asistencia < 70% y calificación < 6 (60 si la escala es 0-100)
    # Ajustamos calificación menor a 60 para riesgo
    df_riesgo = df_melt[(df_melt["porcentaje_asistencias"] < 70) & (df_melt["calificacion"] < 60)]
    return df_riesgo

st.set_page_config(page_title="Dashboard Académico", layout="wide")
st.title("📊 Dashboard Académico Adaptado a tu CSV")

df_original = cargar_datos()
df = preparar_datos(df_original)

# Filtros
grupo = st.selectbox("Selecciona un grupo:", sorted(df["grupo"].unique()))
semestre = st.selectbox("Selecciona un semestre:", sorted(df["semestre"].unique()))
filtrado = df[(df["grupo"] == grupo) & (df["semestre"] == semestre)]

promedios, df_melt = promedio_por_materia(filtrado)

# Gráfico promedio por materia
st.subheader("📚 Promedio General por Materia")
fig1, ax1 = plt.subplots()
sns.barplot(data=promedios, x="materia", y="calificacion", ax=ax1, palette="viridis")
ax1.set_ylabel("Calificación promedio")
ax1.set_xlabel("Materia")
st.pyplot(fig1)

# Gráfico dispersión asistencia vs promedio_final
st.subheader("📈 Relación entre Asistencia y Promedio Final")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=filtrado, x="porcentaje_asistencias", y="promedio_final", hue="grupo", ax=ax2)
ax2.set_xlabel("Porcentaje de Asistencia")
ax2.set_ylabel("Promedio Final")
st.pyplot(fig2)

# Alumnos en riesgo
st.subheader("🚨 Alumnos en Riesgo de Reprobación")
riesgo = alumnos_en_riesgo(df_melt)
st.dataframe(riesgo[["id_alumno", "nombre", "materia", "calificacion", "porcentaje_asistencias"]])

st.markdown("<hr><center><i>Desarrollado por el equipo Scrum ✨</i></center>", unsafe_allow_html=True)


