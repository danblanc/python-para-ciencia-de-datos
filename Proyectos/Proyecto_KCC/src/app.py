
import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar el dataset
dd = pd.read_excel('../data/Hogar_Nutrientes_Final.xlsx')

# Crear el título principal del dashboard
st.title('Visualizador de Consumo de Alimentos')

# Agregar estilo CSS para el fondo
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("C:/Users/ctoledo/Desktop/Proyecto_KCC/data/Captura.PNG");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;  /* Asegura que el fondo cubra toda la pantalla */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F0F8FF;  /* Cambia este código de color por el que desees */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Crear las pestañas
tab1, tab2, tab3 = st.tabs(["Calorias", "Macronutrientes", "Ultraprocesados"])

# Contenido para la Pestaña 1 - Calorias
with tab1:
    st.header('Capítulo 1: Consumo calorico')
    st.write('En este visualizador vamos a mostrar el consumo aparente de las personas en calorías')
    
    # Calcular la media de Cal_percapita
    dd_media = dd.groupby('Cal_percapita')['Cal_percapita'].mean().reset_index(name='Media_Cal_percapita')
    
    # Crear un gráfico de barras para mostrar la media
    fig = px.bar(dd_media, x='Cal_percapita', y='Media_Cal_percapita', title='Media de Cal_percapita')
    
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)
    
    # Mostrar el dataframe agrupado
    st.dataframe(dd_media)

# Contenido para la Pestaña 2 - Filtros
with tab2:
    st.sidebar.header('Puedes hacer los filtros a través de:')
    
    # Definir las etiquetas de las regiones
    categorias = {
        '1': 'Montevideo',
        '2': 'Localidades mayor a 5000 hab',
        '3': 'Localidades Pequeñas'
    }

    # Crear el selectbox en la barra lateral
    region_seleccionada = st.sidebar.selectbox('Región:', list(categorias.keys()), format_func=lambda x: categorias[x])

    # Mostrar la región seleccionada
    st.write(f'Región: {categorias[region_seleccionada]}')

    categorias_quintil = {
        '1': 'Primer quintil',
        '2': 'Segundo quintil',
        '3': 'Tercer quintil',
        '4': 'Cuarto quintil',
        '5': 'Quinto quintil',
    }

    # Crear el selectbox en la barra lateral
    quintil_seleccionada = st.sidebar.selectbox('Quintiles:', list(categorias_quintil.keys()), format_func=lambda x: categorias_quintil[x])

    # Mostrar la región seleccionada
    st.write(f'Quintiles: {categorias_quintil[quintil_seleccionada]}')

    categorias_pobre_20 = {
        '1': '20% más pobre',
        '0': 'Por encima del 20%',
    }

    # Crear el selectbox en la barra lateral
    pobre_20_seleccionada = st.sidebar.selectbox('Pobre 20%:', list(categorias_pobre_20.keys()), format_func=lambda x: categorias_pobre_20[x])

    # Mostrar la región seleccionada
    st.write(f'Pobre 20%: {categorias_pobre_20[pobre_20_seleccionada]}')

    categorias_rico_20 = {
        '1': '20% más rico',
        '0': 'Por debajo del 20%',
    }

    # Crear el selectbox en la barra lateral
    rico_20_seleccionada = st.sidebar.selectbox('Rico 20%:', list(categorias_rico_20.keys()), format_func=lambda x: categorias_rico_20[x])

    # Mostrar la región seleccionada
    st.write(f'Rico 20%: {categorias_rico_20[rico_20_seleccionada]}')

    # Aplicar los filtros al dataset
    dd_filtrado = dd[(dd['REGION'] == region_seleccionada) & 
                     (dd['Quintiles'] == quintil_seleccionada) & 
                     (dd['pobre_20'] == pobre_20_seleccionada) & 
                     (dd['rico_20'] == rico_20_seleccionada)]
                     
    st.subheader(f'Filtrado por: {region_seleccionada}, {quintil_seleccionada}, {pobre_20_seleccionada}, {rico_20_seleccionada}')
    st.dataframe(dd_filtrado)

# Contenido para la Pestaña 3 - Gráficos
with tab3:
    st.header('Gráfico de calorías según región')
    st.write('A continuación se muestra un gráfico de calorías por hogares con Niños:')
    
    # Crear un gráfico simple, suponiendo que tienes una columna 'Caloria' y 'region'
    if not dd_filtrado.empty:
        st.bar_chart(dd_filtrado.set_index('Cal_percapita')['REGION'])  
    else:
        st.write('No hay datos para mostrar con los filtros seleccionados.')

# Ejecutar el dashboard
# Este bloque no es necesario en Streamlit, simplemente guarda el archivo y ejecuta con streamlit run
