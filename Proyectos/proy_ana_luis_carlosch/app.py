import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium #Widget de Streamlit para mostrar los mapas

st.set_page_config(
    page_title="Dashboard Proyecto",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded")

# Crea dataframe de farmacias por departamento
df_farmacias_depto = pd.read_csv('data/farmacias_departamento.csv')

# Crea dataframe de todas las farmacias de Uruguay
df_farmacias = pd.read_csv('data/farmacias_loc_depto.csv')

# Crea dataframe loc grandes sin farmacias
df_loc_grandes_sin_farm = pd.read_csv('data/loc_grandes_sin_farm.csv')

# Crea dataframe loc chicas con farmacias
df_loc_chicas_con_farm = pd.read_csv('data/loc_chicas_con_farm.csv')

# Título del Dashboard
st.title('INE - Dashboard Famacias')
st.logo('data/logoINE_Transparente.png',size="large", link=None, icon_image=None)

#tabs = st.tabs(["Total de Farmacias por Departamento", "Ubicación de Farmacias", "Grafica 3"])
tab1,tab2,tab3=st.tabs(["Total de Farmacias por Departamento",
                        "Ubicación de Farmacias",
                        "Localidades con cantidad de farmacias atípicas"])

# Filtro en la Barra Lateral
st.sidebar.header('Filtros')
filtro_departamento = st.sidebar.multiselect('Seleccione Departamento:', df_farmacias_depto['NOMBDEPTO'].unique())

with tab1: 

    # Filtrar datos según selección
    df_filtrado = df_farmacias_depto.copy()

    # Filtrado por departamento
    if filtro_departamento:
        df_filtrado = df_filtrado[df_filtrado['NOMBDEPTO'].isin(filtro_departamento)]

    # Visualización 1: Gráfico de Farmacias por Departamento
    st.subheader('Farmacias por Departamento')
    fig1 = px.bar(df_filtrado, x='NOMBDEPTO', y='CANT_FARMACIAS', title='Total de Farmacias por Departamento')
    st.plotly_chart(fig1)

with tab2:

    # Filtrado por nombre de farmacia
    filtro_nombre_farmacia = st.text_input('Nombre de Farmacia: ')

    if filtro_nombre_farmacia:
        # El nombre de la farmacia puede ser ingresado en mayúsculas o minúsculas y no ser completo
        df_farmacias = df_farmacias[df_farmacias['NOMBRE'].str.contains(filtro_nombre_farmacia, case=False)]

    # Filtrado por departamento
    if filtro_departamento:
        df_farmacias = df_farmacias[df_farmacias['NOMDEPTO'].isin(filtro_departamento)]

    # Despliega farmacias georreferenciadas sobre mapa del Uruguay
    fig = px.scatter_mapbox(df_farmacias,lat='LATITUD',lon='LONGITUD', 
                                hover_name='NOMBRE',hover_data=['DIRECCION','NOMBLOC', 'NOMDEPTO'],
                                zoom=5, height=600)
    fig.update_layout(mapbox_style='open-street-map')
    st.plotly_chart(fig,use_container_width=True)


with tab3:

    # Cuadros de localidades con 2 casos atípicos:
    # localidades < 3.000 habitantes con farmacias y localidades > 3.000 habitantes sin farmacias
    st.subheader('Localidades con cantidad de farmacias atípicas')
    cuadro = st.radio('Cuadro:',options=['Localidades de mas de 3.000 habitantes sin farmacias en un radio de 1 km',
                                         'Localidades de menos de 3.000 habitantes con farmacias en un radio de 1 km'],horizontal=False)
    if cuadro == 'Localidades de mas de 3.000 habitantes sin farmacias en un radio de 1 km':
        # Filtrado por departamento
        if filtro_departamento:
            df_loc_grandes_sin_farm = df_loc_grandes_sin_farm[df_loc_grandes_sin_farm['NOMBDEPTO'].isin(filtro_departamento)]

        st.dataframe(df_loc_grandes_sin_farm, use_container_width=True)

    else:
        # Filtrado por departamento
        if filtro_departamento:
            df_loc_chicas_con_farm = df_loc_chicas_con_farm[df_loc_chicas_con_farm['NOMBDEPTO'].isin(filtro_departamento)]

        st.dataframe(df_loc_chicas_con_farm, use_container_width=True)