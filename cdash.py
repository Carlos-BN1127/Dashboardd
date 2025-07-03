import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple

# Configuración inicial
st.set_page_config(page_title="Dashboard Académico", layout="wide")
st.title("📊 Dashboard Académico - Proyecto Final Scrum")

# 🧩 HU-01: Cargar datos desde CSV con manejo de errores
@st.cache_data
def cargar_datos() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Carga los datos desde archivos CSV con verificación de existencia."""
    try:
        calificaciones = pd.read_csv('calificaciones.csv')
        asistencias = pd.read_csv('asistencias.csv')
        alumnos = pd.read_csv('datos_alumnos.csv')
        
        # Verificar columnas mínimas requeridas
        for df, name, required_cols in zip(
            [calificaciones, asistencias, alumnos],
            ['calificaciones', 'asistencias', 'alumnos'],
            [['id_alumno', 'nombre', 'materia', 'calificacion', 'grupo', 'semestre'],
             ['id_alumno', 'nombre', 'asistencias', 'totales'],
             ['id_alumno', 'nombre']]
        ):
            if not all(col in df.columns for col in required_cols):
                raise ValueError(f"Faltan columnas requeridas en {name}.csv")
        
        return calificaciones, asistencias, alumnos
        
    except FileNotFoundError as e:
        st.error(f"Error al cargar archivos: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
        st.stop()

# 🧩 HU-02: Limpiar y unir datos con validación
def transformar_datos(
    calificaciones: pd.DataFrame, 
    asistencias: pd.DataFrame, 
    alumnos: pd.DataFrame
) -> pd.DataFrame:
    """Transforma y une los DataFrames con verificación de datos."""
    try:
        # Calcular porcentaje de asistencia
        if (asistencias["totales"] == 0).any():
            st.warning("Algunos alumnos tienen 0 clases totales. Revisar datos.")
            asistencias = asistencias[asistencias["totales"] > 0].copy()
        
        asistencias["porcentaje_asistencia"] = (asistencias["asistencias"] / asistencias["totales"]) * 100
        
        # Unir datos con validación de merges
        df = pd.merge(
            calificaciones, 
            asistencias[['id_alumno', 'nombre', 'porcentaje_asistencia']], 
            on=["id_alumno", "nombre"],
            how='left',
            validate='many_to_one'
        )
        
        df = pd.merge(
            df, 
            alumnos, 
            on=["id_alumno", "nombre"],
            how='left',
            validate='many_to_one'
        )
        
        # Verificar valores nulos después del merge
        if df.isnull().any().any():
            st.warning("Advertencia: Hay valores nulos después de unir los datos.")
        
        return df
        
    except pd.errors.MergeError as e:
        st.error(f"Error al unir datos: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"Error inesperado al transformar datos: {str(e)}")
        st.stop()

# 🧩 HU-03: Promedio por materia con redondeo
def promedio_por_materia(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula el promedio por materia con formato adecuado."""
    return (
        df.groupby('materia', observed=True)['calificacion']
        .mean()
        .round(2)
        .reset_index()
        .sort_values('calificacion', ascending=False)
    )

# 🧩 HU-07: Alumnos en riesgo con criterios claros
def alumnos_en_riesgo(df: pd.DataFrame) -> pd.DataFrame:
    """Identifica alumnos en riesgo con umbrales configurables."""
    UMBRAL_CALIFICACION = 6.0
    UMBRAL_ASISTENCIA = 70.0
    
    riesgo = df[
        (df['porcentaje_asistencia'] < UMBRAL_ASISTENCIA) & 
        (df['calificacion'] < UMBRAL_CALIFICACION)
    ].copy()
    
    # Ordenar por mayor riesgo (peores calificaciones primero)
    riesgo = riesgo.sort_values(
        by=['calificacion', 'porcentaje_asistencia'], 
        ascending=[True, True]
    )
    
    return riesgo

# Cargar y transformar datos
calificaciones, asistencias, alumnos = cargar_datos()
df = transformar_datos(calificaciones, asistencias, alumnos)

# Sidebar para filtros
with st.sidebar:
    st.header("Filtros")
    
    # 🧩 HU-05: Filtros por grupo y semestre con opción "Todos"
    grupo = st.selectbox(
        "Selecciona un grupo:",
        options=["Todos"] + sorted(df["grupo"].unique().tolist())
    ) # <--- ¡Aquí faltaba un paréntesis!
    
    semestre = st.selectbox(
        "Selecciona un semestre:",
        options=["Todos"] + sorted(df["semestre"].unique().tolist())
    ) # <--- ¡Y aquí también!
    
    # Aplicar filtros
    filtrado = df.copy()
    if grupo != "Todos":
        filtrado = filtrado[filtrado["grupo"] == grupo]
    if semestre != "Todos":
        filtrado = filtrado[filtrado["semestre"] == semestre]

# Mostrar métricas clave
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Alumnos", len(filtrado["id_alumno"].unique()))
with col2:
    st.metric("Promedio General", f"{filtrado['calificacion'].mean():.1f}")
with col3:
    st.metric("Asistencia Promedio", f"{filtrado['porcentaje_asistencia'].mean():.1f}%")

# 🧩 HU-03: Gráfico de barras - Promedio por materia
st.subheader("📚 Promedio General por Materia")
promedios = promedio_por_materia(filtrado)

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=promedios, 
    x="materia", 
    y="calificacion", 
    ax=ax1, 
    palette="viridis"
)
ax1.set_title("Promedio por materia", fontsize=14)
ax1.set_ylabel("Calificación promedio", fontsize=12)
ax1.set_xlabel("Materia", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig1)

# 🧩 HU-04: Gráfico de dispersión mejorado
st.subheader("📈 Relación entre Asistencia y Calificación")

fig2, ax2 = plt.subplots(figsize=(10, 6))
scatter = sns.scatterplot(
    data=filtrado, 
    x="porcentaje_asistencia", 
    y="calificacion", 
    hue="materia",
    palette="tab10",
    s=100,
    alpha=0.7,
    ax=ax2
)
ax2.set_title("Dispersión Asistencia vs Calificación", fontsize=14)
ax2.set_xlabel("Porcentaje de Asistencia", fontsize=12)
ax2.set_ylabel("Calificación", fontsize=12)
ax2.axhline(y=6, color='r', linestyle='--', label='Umbral aprobación')
ax2.axvline(x=70, color='r', linestyle='--', label='Umbral asistencia')
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(fig2)

# 🧩 HU-07: Alumnos en riesgo con más detalles
st.subheader("🚨 Alumnos en Riesgo de Reprobación")
riesgo = alumnos_en_riesgo(filtrado)

if not riesgo.empty:
    st.dataframe(
        riesgo[
            ['id_alumno', 'nombre', 'grupo', 'semestre', 
             'materia', 'calificacion', 'porcentaje_asistencia']
        ].style.format({
            'calificacion': '{:.1f}',
            'porcentaje_asistencia': '{:.1f}%'
        }),
        height=min(400, 50 + 35 * len(riesgo)),
        use_container_width=True
    )
    
    # Opción para descargar
    csv = riesgo.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar lista de riesgo",
        data=csv,
        file_name='alumnos_en_riesgo.csv',
        mime='text/csv'
    )
else:
    st.success("🎉 No hay alumnos en riesgo con los filtros actuales")

# 🧩 HU-06: Mejorar estética y pie de página
st.markdown("""
<hr>
<center>
    <i>Desarrollado por el equipo Scrum ✨ | 
    <a href="#" target="_blank">Documentación</a> | 
    <a href="#" target="_blank">Código Fuente</a></i>
</center>
""", unsafe_allow_html=True)
