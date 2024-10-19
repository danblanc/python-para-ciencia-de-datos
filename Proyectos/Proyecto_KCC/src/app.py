import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import base64
from io import BytesIO

# Configuración inicial de la página
st.set_page_config(
    page_title="Visualizador de Consumo de Alimentos",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Función para cargar datos con caché
@st.cache_data
def cargar_datos(ruta):
    return pd.read_excel(ruta)

# Cargar el dataset
df = cargar_datos('../data/Hogar_Nutrientes_Final.xlsx')

# Función para aplicar filtros
def aplicar_filtros(data, region, quintil, con_ninos):
    df_filtrado = data.copy()
    if region:
        df_filtrado = df_filtrado[df_filtrado['REGION'].isin(region)]
    if quintil:
        df_filtrado = df_filtrado[df_filtrado['quintiles'].isin(quintil)]
    # if pobre_20 != 'Todos':
    #     df_filtrado = df_filtrado[df_filtrado['pobre_20'] == pobre_20]
    # if rico_20 != 'Todos':
    #     df_filtrado = df_filtrado[df_filtrado['rico_20'] == rico_20]
    if con_ninos and con_ninos != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Niños_hogar'] == categorias_con_ninos[con_ninos]]
    return df_filtrado

# Función para convertir imagen a base64
def image_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return encoded

# Cargar y aplicar imagen de fondo con traslucidez
def agregar_fondo():
    try:
        # Asegúrate de que la ruta de la imagen sea accesible por Streamlit
        image = Image.open("../data/Captura.PNG")
        encoded_image = image_to_base64(image)
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.2)), url("data:image/png;base64,{encoded_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .stApp * {{
                color: #000000 !important;  /* Cambiar el color del texto a negro */
            }}

            .stSidebar .css-1d391kg a {{
                color: #FFFFFF !important;
            }}
            .stSidebar .css-1d391kg .stButton>button {{
                color: #000000 !important;
            }}
            .stSidebar label, .stSidebar [data-baseweb="select"] {{
                color: #FFFFFF !important;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.write("No se pudo cargar la imagen de fondo.")
        st.write(e)

agregar_fondo()

# Crear el título principal del dashboard
st.title('Visualizador de Consumo de Alimentos')

# Crear las pestañas
tab_calorias, tab_macronutrientes, tab_ultraprocesados, tab_metodologia = st.tabs(
    ["Calorías", "Macronutrientes", "Ultraprocesados", "Aclaraciones Metodológicas"]
)

# Definir las categorías para los filtros en español
categorias_region = {
    1: 'Montevideo',
    2: 'Localidades mayor a 5000 hab',
    3: 'Localidades Pequeñas'
}

categorias_quintil = {
    1: 'Primer quintil',
    2: 'Segundo quintil',
    3: 'Tercer quintil',
    4: 'Cuarto quintil',
    5: 'Quinto quintil',
}

# categorias_pobre_20 = {
#     'Todos': 'Todos',
#     1: '20% más pobre',
#     0: 'Por encima del 20%',
# }

# categorias_rico_20 = {
#     'Todos': 'Todos',
#     1: '20% más rico',
#     0: 'Por debajo del 20%',
# }

categorias_con_ninos = {
    '1': 'Hogar con niños',
    '0': 'Hogar sin niños',
}

# Sidebar para los filtros
st.sidebar.header('Filtros')

# Filtros múltiples con opciones de selección
selected_region = st.sidebar.multiselect(
    'Región:',
    options=list(categorias_region.keys()),
    format_func=lambda x: categorias_region[x]
)

selected_quintil = st.sidebar.multiselect(
    'Quintiles:',
    options=list(categorias_quintil.keys()),
    format_func=lambda x: categorias_quintil[x]
)

# selected_pobre_20 = st.sidebar.selectbox(
#     'Pobre 20%',
#     options=list(categorias_pobre_20.keys()),
#     format_func=lambda x: categorias_pobre_20[x]
# )

# selected_rico_20 = st.sidebar.selectbox(
#     'Rico 20%',
#     options=list(categorias_rico_20.keys()),
#     format_func=lambda x: categorias_rico_20[x]
# )

selected_con_ninos = st.sidebar.selectbox(
    'Hogar con niños:',
    options=['Todos'] + list(categorias_con_ninos.keys()),
    format_func=lambda x: categorias_con_ninos[x] if x in categorias_con_ninos else 'Todos'
)

# Aplicar los filtros al dataset
df_filtrado = aplicar_filtros(
    df,
    region=selected_region if selected_region else None,
    quintil=selected_quintil if selected_quintil else None,
    # pobre_20=selected_pobre_20 if selected_pobre_20 else 'Todos',
    # rico_20=selected_rico_20 if selected_rico_20 else 'Todos',
    con_ninos=selected_con_ninos if selected_con_ninos in categorias_con_ninos else 'Todos',
)

# Mostrar los filtros aplicados en la barra lateral (opcional)
st.sidebar.markdown("### Filtros Aplicados")
if selected_region:
    st.sidebar.write(f"**Región:** {', '.join([categorias_region[r] for r in selected_region])}")
if selected_quintil:
    st.sidebar.write(f"**Quintiles:** {', '.join([categorias_quintil[q] for q in selected_quintil])}")
# if selected_pobre_20 != 'Todos':
#     st.sidebar.write(f"**Pobre 20%:** {categorias_pobre_20[selected_pobre_20]}")
# if selected_rico_20 != 'Todos':
#     st.sidebar.write(f"**Rico 20%:** {categorias_rico_20[selected_rico_20]}")
if selected_con_ninos != 'Todos':
    st.sidebar.write(f"**Hogar con niños:** {categorias_con_ninos[selected_con_ninos]}")

# Verificar si 'cal_ultra_percapita' existe en el DataFrame filtrado
if 'cal_ultra_percapita' not in df_filtrado.columns:
    st.error("La columna 'cal_ultra_percapita' no está presente en los datos filtrados. Por favor, verifica el procesamiento de datos.")
else:
    # Contenido para la Pestaña 1 - Calorías
    with tab_calorias:
        st.header('Capítulo 1: Consumo Calórico')
        st.write('En este visualizador vamos a mostrar el consumo aparente de las personas en calorías.')

        # Calcular estadísticas
        calorias_media = df_filtrado['Cal_percapita'].mean()
        calorias_mediana = df_filtrado['Cal_percapita'].median()

        st.write(f"**Media de Calorías per cápita:** {calorias_media:.2f}")
        st.write(f"**Mediana de Calorías per cápita:** {calorias_mediana:.2f}")

        # Filtrar filas con calorías menores o iguales a 4000 solo para el histograma
        df_filtrado_calorias = df_filtrado[df_filtrado['Cal_percapita'] <= 10000]

        # Crear un histograma de calorías per cápita con el filtro aplicado
        fig_cal_hist = px.histogram(
            df_filtrado_calorias,
            x='Cal_percapita',
            nbins=30,
            title='Distribución de Calorías per cápita',
            labels={'Cal_percapita': 'Calorías per cápita'},
            template='plotly_white'
        )
        st.plotly_chart(fig_cal_hist, use_container_width=True)

        # Gráfico de barras por región
        fig_cal_region = px.bar(
            df_filtrado.groupby('REGION')['Cal_percapita'].mean().reset_index(),
            x='REGION',
            y='Cal_percapita',
            title='Media de Calorías per cápita por Región',
            labels={'Cal_percapita': 'Calorías per cápita', 'REGION': 'Región'},
            template='plotly_white'
        )
        st.plotly_chart(fig_cal_region, use_container_width=True)

        # Mostrar la tabla filtrada
        st.subheader('Datos Filtrados')
        st.dataframe(df_filtrado[['NUMERO', 'REGION', 'Cal_percapita', 'gr_percapita', 'Calorias_hogar']])

    # Contenido para la Pestaña 2 - Macronutrientes
    with tab_macronutrientes:
        st.header('Capítulo 2: Distribución de Macronutrientes')
        st.write('Análisis de la distribución porcentual de proteínas, grasas e hidratos de carbono.')

        # Gráfico de pastel para la distribución promedio de macronutrientes
        distribucion_macro = df_filtrado[['adec_proteinas', 'adec_grasas', 'adec_hidratos']].mean().reset_index()
        distribucion_macro.columns = ['Macronutriente', 'Porcentaje']
        distribucion_macro['Macronutriente'] = distribucion_macro['Macronutriente'].map({
            'adec_proteinas': 'Proteínas',
            'adec_grasas': 'Grasas',
            'adec_hidratos': 'Hidratos de Carbono'
        })
        fig_pie = px.pie(
            distribucion_macro,
            names='Macronutriente',
            values='Porcentaje',
            title='Distribución Promedio de Macronutrientes',
            hole=0.3,
            template='plotly_white'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Gráfico de barras apiladas por región
        distribucion_region = df_filtrado.groupby('REGION')[['adec_proteinas', 'adec_grasas', 'adec_hidratos']].mean().reset_index()
        distribucion_region_melted = distribucion_region.melt(id_vars='REGION', value_vars=['adec_proteinas', 'adec_grasas', 'adec_hidratos'],
                                                               var_name='Macronutriente', value_name='Porcentaje')
        distribucion_region_melted['Macronutriente'] = distribucion_region_melted['Macronutriente'].map({
            'adec_proteinas': 'Proteínas',
            'adec_grasas': 'Grasas',
            'adec_hidratos': 'Hidratos de Carbono'
        })
        fig_bar_stacked = px.bar(
            distribucion_region_melted,
            x='REGION',
            y='Porcentaje',
            color='Macronutriente',
            title='Distribución de Macronutrientes por Región',
            labels={'Porcentaje': 'Porcentaje (%)', 'REGION': 'Región'},
            barmode='stack',
            template='plotly_white'
        )
        st.plotly_chart(fig_bar_stacked, use_container_width=True)

        # Mostrar la tabla filtrada
        st.subheader('Datos Filtrados')
        st.dataframe(df_filtrado[['NUMERO', 'REGION', 'adec_proteinas', 'adec_grasas', 'adec_hidratos']])

    # Contenido para la Pestaña 3 - Ultraprocesados
    with tab_ultraprocesados:
        st.header('Capítulo 3: Consumo de Ultraprocesados')
        st.write('Análisis del consumo de alimentos ultraprocesados en calorías.')

        # Calcular estadísticas
        ultra_media = df_filtrado['cal_ultra_percapita'].mean()
        ultra_mediana = df_filtrado['cal_ultra_percapita'].median()

        st.write(f"**Media de Calorías de Ultraprocesados per cápita:** {ultra_media:.2f}")
        st.write(f"**Mediana de Calorías de Ultraprocesados per cápita:** {ultra_mediana:.2f}")

        # Gráfico de barras de proporción de calorías de ultraprocesados por región
        calories_region = df_filtrado.groupby('REGION')[['Cal_percapita', 'cal_ultra_percapita']].mean().reset_index()
        calories_region['Proporcion'] = (calories_region['cal_ultra_percapita'] / calories_region['Cal_percapita']) * 100

        fig_ultra_proportion = px.bar(
            calories_region,
            x='REGION',
            y='Proporcion',
            title='Proporción de Calorías de Ultraprocesados por Región',
            labels={'Proporcion': 'Proporción (%)', 'REGION': 'Región'},
            template='plotly_white'
        )
        st.plotly_chart(fig_ultra_proportion, use_container_width=True)

        # Mostrar la tabla filtrada
        st.subheader('Datos Filtrados')
        st.dataframe(df_filtrado[['NUMERO', 'REGION', 'cal_ultra_percapita', 'Cal_percapita']])

    # Contenido para la Pestaña 4 - Aclaraciones Metodológicas
    with tab_metodologia:
        st.header('Aclaraciones Metodológicas')
        st.markdown("""
        ## Encuesta de Gasto e Ingresos de los Hogares - ENGIH 2016 - 2017
        La Encuesta de Gasto e Ingresos de los Hogares (ENGIH) 2016-2017 en Uruguay es un estudio fundamental realizado por el Instituto Nacional de Estadística (INE), cuyo propósito principal es obtener información detallada sobre el gasto, ingreso y condiciones de vida de los hogares uruguayos. A continuación te detallo sus principales características y objetivos:

        ### Características de la ENGIH 2016-2017:

        - **Periodicidad**: Es una encuesta de carácter periódico, que generalmente se realiza cada 10 años aproximadamente, con el fin de actualizar la canasta de consumo que se utiliza para el cálculo del Índice de Precios al Consumo (IPC).
        
        - **Cobertura**: La ENGIH abarca todo el territorio nacional, incluyendo tanto zonas urbanas como rurales. Se encuesta una muestra representativa de hogares, permitiendo la inferencia de resultados a nivel nacional, por regiones y por distintos niveles socioeconómicos.
        
        - **Método de recolección**: La encuesta se realiza mediante entrevistas directas en los hogares, con el uso de un diario de gastos en el cual las familias registran todos sus gastos cotidianos por un período determinado.
        
        - **Contenido**: La encuesta recopila información sobre:
        
            - **Ingresos del hogar**: Ingresos laborales y no laborales, pensiones, transferencias, entre otros.
            - **Gastos del hogar**: En bienes y servicios de consumo, gastos en salud, educación, transporte, alimentos, vivienda, etc.
            - **Condiciones de vida**: Características del hogar, tenencia de bienes durables, acceso a servicios básicos, entre otros.
        
        - **Duración del relevamiento**: Se realizó a lo largo de un año, desde diciembre de 2016 hasta diciembre de 2017, con el fin de captar variaciones estacionales en los patrones de gasto e ingreso.
        
        ### Objetivos de la ENGIH 2016-2017:

        - **Actualización de la canasta de consumo**: Uno de los principales objetivos es actualizar la canasta de bienes y servicios que se utiliza para calcular el Índice de Precios al Consumo (IPC), el cual mide la evolución de los precios de bienes y servicios consumidos por los hogares uruguayos.
        
        - **Medición de la distribución del ingreso**: La ENGIH permite estimar la distribución del ingreso en los hogares, lo que contribuye al análisis de la pobreza, la desigualdad y la equidad en Uruguay.
        
        - **Conocer patrones de consumo**: Ayuda a entender los patrones de gasto de los hogares uruguayos, identificando en qué productos y servicios destinan sus recursos, lo que es esencial para la formulación de políticas públicas y decisiones de mercado.
        
        - **Análisis de condiciones de vida**: La encuesta permite estudiar las condiciones de vida de los hogares, como la calidad de la vivienda, el acceso a servicios básicos, la tenencia de bienes, etc., información clave para el diseño de políticas sociales y económicas.
        
        - **Evaluación de políticas públicas**: Provee una base de datos robusta para evaluar el impacto de diversas políticas públicas en la economía de los hogares, especialmente en relación con la pobreza, el empleo, y las transferencias de ingresos.
        
        - **Estimación de la demanda de bienes y servicios**: Aporta insumos cruciales para la planificación y el diseño de políticas económicas y sociales, proporcionando datos sobre la estructura de la demanda interna de bienes y servicios.
        
        La ENGIH 2016-2017 es una herramienta vital para entender las dinámicas económicas y sociales de los hogares en Uruguay, y sus resultados son utilizados para la toma de decisiones en múltiples áreas, desde el cálculo de indicadores macroeconómicos hasta la formulación de políticas sociales.
        """)

    # Opciones adicionales en la barra lateral
    st.sidebar.markdown("### Opciones Adicionales")
    if st.sidebar.button('Descargar Datos Filtrados'):
        towrite = BytesIO()
        df_filtrado.to_excel(towrite, index=False)
        towrite.seek(0)
        st.sidebar.download_button(
            label="📥 Descargar Excel",
            data=towrite,
            file_name='Hogar_Nutrientes_Filtrado.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
