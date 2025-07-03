import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Título del dashboard
st.title("📊 Dashboard Académico")

# Cargar archivo CSV
try:
    df = pd.read_csv("calificaciones.csv")
    st.success("✅ Archivo calificaciones.csv cargado correctamente.")
except Exception as e:
    st.error(f"❌ Error al cargar el archivo: {e}")
    df = pd.DataFrame()

# Mostrar tabla de datos
if not df.empty:
    st.subheader("Vista previa de los datos:")
    st.dataframe(df.head())

    st.subheader("Gráfico de promedio por materia:")
    try:
        # Agrupar y calcular promedio
        promedio = df.groupby("materia")["calificacion"].mean().reset_index()

        # Crear gráfico
        fig, ax = plt.subplots()
        sns.barplot(data=promedio, x="materia", y="calificacion", ax=ax, palette="viridis")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error al graficar: {e}")
else:
    st.warning("⚠️ No hay datos disponibles para graficar.")
