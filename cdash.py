import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# DataFrame de ejemplo
def crear_dataframe_ejemplo():
    data = {
        "grupo": ["A", "A", "B", "B"],
        "semestre": [1, 1, 2, 2],
        "materia": ["Matemáticas", "Historia", "Matemáticas", "Historia"],
        "calificacion": [7.5, 8.0, 5.0, 9.0],
        "asistencias": [15, 14, 10, 16],
        "totales": [20, 20, 20, 20]
    }
    return pd.DataFrame(data)

def transformar_datos(df):
    df["porcentaje_asistencia"] = (df["asistencias"] / df["totales"]) * 100
    return df

# Resto de funciones iguales...

st.title("Dashboard Académico - Ejemplo sin CSV")

usar_ejemplo = st.checkbox("Usar datos de ejemplo")

if usar_ejemplo:
    df_original = crear_dataframe_ejemplo()
else:
    uploaded_file = st.file_uploader("Sube el archivo CSV", type="csv")
    if uploaded_file is not None:
        df_original = pd.read_csv(uploaded_file)
    else:
        st.warning("Por favor sube un archivo CSV o usa datos de ejemplo.")
        st.stop()

df = transformar_datos(df_original)

# Aquí continúa el resto de tu dashboard igual...


