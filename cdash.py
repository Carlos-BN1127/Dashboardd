import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(page_title='Dashboard Académico Avanzado', layout='wide', page_icon='📊')
st.title('📊 Dashboard de Rendimiento Académico Completo')

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv('resumen_alumnos.csv')

df = cargar_datos()

# Limpieza de datos
df['asistencia_promedio'] = df['asistencia_promedio'].round(2)
df['calificacion_promedio'] = df['calificacion_promedio'].round(2)

# Sidebar con filtros
st.sidebar.header('Filtros')
grupos = st.sidebar.multiselect(
    'Grupos:',
    options=sorted(df['grupo'].unique()),
    default=sorted(df['grupo'].unique())
)

semestres = st.sidebar.multiselect(
    'Semestres:',
    options=sorted(df['semestre'].unique()),
    default=sorted(df['semestre'].unique())
)

sexos = st.sidebar.multiselect(
    'Sexo:',
    options=df['sexo'].unique(),
    default=df['sexo'].unique()
)

edades = st.sidebar.slider(
    'Rango de edad:',
    min_value=int(df['edad'].min()),
    max_value=int(df['edad'].max()),
    value=(int(df['edad'].min()), int(df['edad'].max()))
)

# Aplicar filtros
df_filtrado = df[
    (df['grupo'].isin(grupos)) &
    (df['semestre'].isin(semestres)) &
    (df['sexo'].isin(sexos)) &
    (df['edad'] >= edades[0]) &
    (df['edad'] <= edades[1])
]

# Métricas clave
st.subheader('📌 Métricas Clave')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Alumnos", len(df_filtrado))
col2.metric("Calificación Promedio", f"{df_filtrado['calificacion_promedio'].mean():.2f}")
col3.metric("Asistencia Promedio", f"{df_filtrado['asistencia_promedio'].mean():.2f}%")

# Calcular tasa de aprobación (solo alumnos con promedio >= 7)
aprobados = df_filtrado[df_filtrado['calificacion_promedio'] >= 7]
tasa_aprobacion = (len(aprobados) / len(df_filtrado)) * 100 if len(df_filtrado) > 0 else 0
col4.metric("Tasa de Aprobación (≥7)", f"{tasa_aprobacion:.1f}%")

# Gráficos en pestañas
tab1, tab2, tab3, tab4 = st.tabs(["📈 Distribuciones", "📊 Comparativas", "🔍 Relaciones", "📅 Evolución"])

with tab1:
    # Gráficos de distribución mejorados
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.histogram(
            df_filtrado, 
            x="calificacion_promedio", 
            nbins=15,
            title="Distribución de Calificaciones",
            color='sexo',
            color_discrete_map={'M': '#636EFA', 'F': '#EF553B'},
            labels={'calificacion_promedio': 'Calificación Promedio', 'count': 'Número de Alumnos'}
        )
        fig1.update_layout(bargap=0.1)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.histogram(
            df_filtrado, 
            x="asistencia_promedio", 
            nbins=15,
            title="Distribución de Asistencia",
            color='sexo',
            color_discrete_map={'M': '#636EFA', 'F': '#EF553B'},
            labels={'asistencia_promedio': 'Asistencia Promedio (%)', 'count': 'Número de Alumnos'}
        )
        fig2.update_layout(bargap=0.1)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Gráfico de rendimiento mejorado
    fig3 = px.sunburst(
        df_filtrado, 
        path=['grupo', 'rendimiento'], 
        title='Rendimiento por Grupo',
        color='rendimiento',
        color_discrete_map={
            'Excelente': '#2CA02C',
            'Bueno': '#1F77B4',
            'Aprobado': '#FF7F0E'
        }
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    # Gráficos comparativos
    st.subheader("Comparativa por Grupos y Semestres")
    
    fig4 = px.box(
        df_filtrado,
        x='grupo',
        y='calificacion_promedio',
        color='sexo',
        title='Distribución de Calificaciones por Grupo',
        labels={'calificacion_promedio': 'Calificación Promedio', 'grupo': 'Grupo'},
        color_discrete_map={'M': '#636EFA', 'F': '#EF553B'}
    )
    st.plotly_chart(fig4, use_container_width=True)
    
    fig5 = px.box(
        df_filtrado,
        x='semestre',
        y='asistencia_promedio',
        color='sexo',
        title='Distribución de Asistencia por Semestre',
        labels={'asistencia_promedio': 'Asistencia Promedio (%)', 'semestre': 'Semestre'},
        color_discrete_map={'M': '#636EFA', 'F': '#EF553B'}
    )
    st.plotly_chart(fig5, use_container_width=True)

with tab3:
    # Relación entre variables
    st.subheader("Relación entre Variables")
    
    fig6 = px.scatter(
        df_filtrado,
        x='asistencia_promedio',
        y='calificacion_promedio',
        color='rendimiento',
        size='edad',
        hover_name='nombre',
        title='Relación Asistencia vs Calificación',
        labels={
            'asistencia_promedio': 'Asistencia Promedio (%)',
            'calificacion_promedio': 'Calificación Promedio',
            'rendimiento': 'Rendimiento',
            'edad': 'Edad'
        },
        color_discrete_map={
            'Excelente': '#2CA02C',
            'Bueno': '#1F77B4',
            'Aprobado': '#FF7F0E'
        }
    )
    st.plotly_chart(fig6, use_container_width=True)
    
    # Heatmap de correlación
    numeric_df = df_filtrado[['asistencia_promedio', 'calificacion_promedio', 'edad', 'semestre']].corr()
    fig7 = px.imshow(
        numeric_df,
        text_auto=True,
        title='Mapa de Calor: Correlación entre Variables',
        labels=dict(x="Variable", y="Variable", color="Correlación"),
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig7, use_container_width=True)

with tab4:
    # Evolución temporal (simulada basada en semestre)
    st.subheader("Evolución por Semestre")
    
    # Agregar datos por semestre
    evolucion = df_filtrado.groupby('semestre').agg({
        'calificacion_promedio': 'mean',
        'asistencia_promedio': 'mean',
        'id_alumno': 'count'
    }).reset_index()
    
    fig8 = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig8.add_trace(
        go.Scatter(
            x=evolucion['semestre'],
            y=evolucion['calificacion_promedio'],
            name='Calificación Promedio',
            line=dict(color='#1F77B4')
        ),
        secondary_y=False
    )
    
    fig8.add_trace(
        go.Scatter(
            x=evolucion['semestre'],
            y=evolucion['asistencia_promedio'],
            name='Asistencia Promedio (%)',
            line=dict(color='#FF7F0E')
        ),
        secondary_y=True
    )
    
    fig8.update_layout(
        title_text='Evolución de Calificaciones y Asistencia por Semestre',
        xaxis_title='Semestre',
        hovermode='x unified'
    )
    
    fig8.update_yaxes(title_text="Calificación Promedio", secondary_y=False)
    fig8.update_yaxes(title_text="Asistencia Promedio (%)", secondary_y=True)
    
    st.plotly_chart(fig8, use_container_width=True)

# Mostrar datos filtrados
st.subheader("📋 Datos Filtrados")
st.dataframe(df_filtrado, use_container_width=True)
