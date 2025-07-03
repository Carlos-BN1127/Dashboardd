import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Encabezado
st.title("Dashboard Académico")
st.write("Visualización de datos escolares")

# Cargar datos de ejemplo
try:
    calificaciones = pd.read_csv("calificaciones.csv")
    st.success("Archivo de calificaciones cargado correctamente.")
except Exception as e:
    st.error(f"No se pudo cargar calificaciones.csv: {e}")
    calificaciones = pd.DataFrame()

# Si hay datos, mostrar gráfica
if not calificaciones.empty:
    st.write("Vista previa de los datos:")
    st.dataframe(calificaciones.head())

    st.subheader("Promedios por materia")
    fig, ax = plt.subplots()
    sns.barplot(data=calificaciones, x="materia", y="calificacion", ax=ax, palette="viridis")
    st.pyplot(fig)
else:
    st.warning("No hay datos para mostrar.")
