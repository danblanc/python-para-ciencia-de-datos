import pandas as pd
import streamlit as st
import plotly.express as px

# Cargar el DataFrame desde el ipcdata.csv
df_IPC = pd.read_csv('./data/IPCDATA.csv', encoding='utf-8')
df_IPCGraAnual = pd.read_csv('./data/IPCDATA.csv', encoding='utf-8')
df_IPCGraMensual = pd.read_csv('./data/IPCDATA.csv', encoding='utf-8')

# Configurar página
st.set_page_config(
    page_title="INE - IPC",
    page_icon="logoINEGra.png",
    layout="wide",
    initial_sidebar_state="expanded")

# Título del Dashboard
st.title("Indice de Precios del Consumo")
st.subheader("Análisis de cálculo")

# Mostrar Filtros 
st.sidebar.header('Filtros')
anios_ordenados = sorted(df_IPC['ANIO'].unique())
meses_ordenados = sorted(df_IPC['MES'].unique())
niveles_ordenados = sorted(df_IPC['NIVEL'].unique())
regiones_ordenadas = sorted(df_IPC['REGION'].unique())
filtro_anio = st.sidebar.selectbox('Selecciona Año:', anios_ordenados)
filtro_mes = st.sidebar.selectbox('Selecciona Mes:', meses_ordenados)
filtro_nivel = st.sidebar.selectbox('Selecciona Nivel:', niveles_ordenados)
filtro_region = st.sidebar.selectbox('Selecciona Región:', regiones_ordenadas)

filtro_variacion = st.sidebar.number_input("Variación Mensual")
st.sidebar.write("Se mostraran aquellos items del nivel que superen la variación mensual indicada (+/-). Si indica valor 0 (cero) se mostraron los items que no variaron en el año y mes seleccionados.")

# Aplicar filtros según selección
if filtro_anio:
    df_IPC = df_IPC[df_IPC['ANIO'] == filtro_anio]
if filtro_mes:
    df_IPC = df_IPC[df_IPC['MES'] == filtro_mes]
if filtro_nivel:
    df_IPC = df_IPC[df_IPC['NIVEL'] == filtro_nivel]
if filtro_region:
    df_IPC = df_IPC[df_IPC['REGION'] == filtro_region]
if filtro_variacion == 0:
    df_IPC = df_IPC[df_IPC['VAR_MENSUAL'] == filtro_variacion]
if filtro_variacion > 0:
   df_IPC = df_IPC[df_IPC['VAR_MENSUAL'] >= filtro_variacion]
if filtro_variacion < 0:
    df_IPC = df_IPC[df_IPC['VAR_MENSUAL'] <= filtro_variacion]

# Definir filtro para gráficos    
filtro_itemsseleccionados = sorted(df_IPC['DESCRIPCION'].unique())

df_IPCGraMensual = df_IPCGraMensual[df_IPCGraMensual['DESCRIPCION'].isin(filtro_itemsseleccionados)]
df_IPCGraMensual = df_IPCGraMensual.sort_values(by=['DESCRIPCION', 'ANIO', 'MES'], ascending=True)
 
df_IPCGraAnual = df_IPCGraAnual[df_IPCGraAnual['DESCRIPCION'].isin(filtro_itemsseleccionados)]
df_IPCGraAnual = df_IPCGraAnual.sort_values(by=['DESCRIPCION', 'ANIO', 'MES'], ascending=True)


# Crear tabs para mostrar datos y graficos
tabDatos, tabMensual, tabAnual = st.tabs(["Datos", "Mensual","Anual"])
with tabDatos:
    # Mostrar tabla de datos filtrada
    st.header("Tabla de datos filtrada")
    st.write(df_IPC)

with tabMensual:
    st.subheader('Variación Mensual')
    st.write('Valores de variación mensual en el año de referencia')

    # Gráfico de Líneas de variación mensual
    if filtro_anio:
        df_IPCGraMensual = df_IPCGraMensual[df_IPCGraMensual['ANIO'] == filtro_anio]
    if filtro_nivel:
        df_IPCGraMensual = df_IPCGraMensual[df_IPCGraMensual['NIVEL'] == filtro_nivel]
    if filtro_region:
        df_IPCGraMensual = df_IPCGraMensual[df_IPCGraMensual['REGION'] == filtro_region]


    GrafMensual = px.line(df_IPCGraMensual, x='MES', y='VAR_MENSUAL', color='DESCRIPCION', title='Variación')
    st.plotly_chart(GrafMensual)

with tabAnual:
    # Gráfico de Líneas de variación anual
    # Solo las divisiones tienen información de variación anual
    if filtro_nivel == 'DIVISION':
        if filtro_mes:
            df_IPCGraAnual = df_IPCGraAnual[df_IPCGraAnual['MES'] == filtro_mes]
        if filtro_nivel:
            df_IPCGraAnual = df_IPCGraAnual[df_IPCGraAnual['NIVEL'] == filtro_nivel]
        if filtro_region:
            df_IPCGraAnual = df_IPCGraAnual[df_IPCGraAnual['REGION'] == filtro_region]


        st.subheader('Variación Anual')
        st.write('Valores de variación anual en el mes de referencia')
        GrafAnual = px.line(df_IPCGraAnual, x='ANIO', y='VAR_ANUAL', color='DESCRIPCION', title='Variación')
        st.plotly_chart(GrafAnual)
    else:
        st.write('No hay información disponible de variaición anual para el nivel seleccionado.')
