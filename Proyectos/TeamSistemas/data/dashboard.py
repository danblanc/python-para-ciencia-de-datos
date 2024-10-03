import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos del ejercicio simple
data_simple = pd.read_csv("dashboard_simple_data.csv")

# Título y subtítulo
st.title("Dashboard Interactivo Simple")
st.subheader("Exploración de datos por categoría")

# Filtro de categoría
categoria = st.sidebar.selectbox("Selecciona una categoría:", data_simple["Categoria"].unique())

# Filtrar datos según la categoría seleccionada
filtered_data_simple = data_simple[data_simple["Categoria"] == categoria]

# Agrupar los datos por Fecha y sumar los valores
grouped_data_simple = filtered_data_simple.groupby("Fecha").agg({"Valor":"sum"}).reset_index()

# Visualización: Gráfico de barras con totales por fecha
fig_simple = px.bar(grouped_data_simple, x="Fecha", y="Valor", title=f"Total de valores por fecha para la categoría {categoria}")

# Mostrar gráfico en la aplicación
st.plotly_chart(fig_simple)




#Ejercicio 2: Dashboard Interactivo Complejo
#Utilizando el dataset demo_data.csv, crea un dashboard más complejo con las siguientes características:

#Pestañas (Tabs): Incluye dos o tres pestañas diferentes para mostrar distintas vistas o análisis.
#Filtros Múltiples: Incluye varios filtros para que el usuario pueda seleccionar diferentes criterios, como categorías, rangos de fechas, y otros.
#Varias Visualizaciones: Incorpora al menos tres tipos diferentes de visualizaciones (gráfico de líneas, gráfico de dispersión, gráfico de barras, etc.) que permitan explorar los datos desde diferentes perspectivas.
#Interactividad Avanzada: Asegúrate de que todas las visualizaciones respondan a los filtros seleccionados por el usuario.

import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium

# Cargar el dataset
@st.cache_data
def load_data():
    data = pd.read_csv('demo_data.csv')
    return data

# Cargar datos
data = load_data()

# Mostrar las columnas disponibles
st.write("Columnas disponibles en el DataFrame:", data.columns.tolist())

# Función para convertir nombres de meses en fechas
def convert_month_to_date(month_name):
    month_dict = {
        "Enero": "2023-01-01",
        "Febrero": "2023-02-01",
        "Marzo": "2023-03-01",
        "Abril": "2023-04-01",
        "Mayo": "2023-05-01",
        "Junio": "2023-06-01",
        "Julio": "2023-07-01",
        "Agosto": "2023-08-01",
        "Septiembre": "2023-09-01",
        "Octubre": "2023-10-01",
        "Noviembre": "2023-11-01",
        "Diciembre": "2023-12-01",
    }
    return month_dict.get(month_name)

# Convertir la columna 'Mes'
data['Mes'] = data['Mes'].apply(convert_month_to_date)
data['Mes'] = pd.to_datetime(data['Mes'])  # Convertir a datetime

# Definir función para categorizar precios
def categorize_price(price):
    if price < 20:
        return "Bajo"
    elif 20 <= price < 50:
        return "Medio"
    else:
        return "Alto"

# Aplicar categorización a los precios
data['Categoría_Precio'] = data['Precio'].apply(categorize_price)

# Agrupamiento de datos por Mes, Producto y Categoría de Precio
grouped_data = data.groupby(['Mes', 'Producto', 'Categoría_Precio']).agg(
    Total_Ventas=('Precio', 'sum'),
    Total_Cantidad=('Cantidad', 'sum'),
    Precio_Promedio=('Precio', 'mean')).reset_index()

# Títulos
st.title("Dashboard Interactivo Complejo")  
st.subheader("Explora los datos con diferentes vistas y filtros")

# Pestañas
tab1, tab2, tab3, tab4 = st.tabs(["Análisis por Producto", "Análisis por Región", "Resumen General", "Mapa"])

# Pestaña 1: Análisis por Producto
with tab1:
    st.header("Análisis por Producto")
    
    # Filtros
    product_filter = st.sidebar.multiselect("Selecciona Productos", options=grouped_data['Producto'].unique())
    filtered_data_product = grouped_data[grouped_data['Producto'].isin(product_filter)] if product_filter else grouped_data

    # Gráfico de líneas
    fig_line_product = px.line(filtered_data_product, x='Mes', y='Total_Ventas', color='Producto', title='Ventas Totales por Producto a lo Largo del Tiempo')
    st.plotly_chart(fig_line_product)

    # Gráfico de barras
    fig_bar_product = px.bar(filtered_data_product, x='Producto', y='Total_Ventas', title='Ventas Totales por Producto', color='Producto')
    st.plotly_chart(fig_bar_product)

    # Gráfico de Precio Promedio
    fig_avg_price = px.line(filtered_data_product, x='Mes', y='Precio_Promedio', color='Producto', title='Precio Promedio por Producto a lo Largo del Tiempo')
    st.plotly_chart(fig_avg_price)

# Pestaña 2: Análisis por Región
with tab2:
    st.header("Análisis por Región")
    
    # Filtros
    region_filter = st.sidebar.multiselect("Selecciona Regiones", options=data['Region'].unique())
    filtered_data_region = data[data['Region'].isin(region_filter)] if region_filter else data

    # Agrupamiento de datos por Región
    grouped_region_data = filtered_data_region.groupby(['Mes', 'Region']).agg(Total_Ventas=('Precio', 'sum'),
                                                                               Total_Cantidad=('Cantidad', 'sum')).reset_index()

    # Gráfico de dispersión
    fig_scatter_region = px.scatter(grouped_region_data, x='Total_Ventas', y='Total_Cantidad', color='Region', title='Cantidad vs Ventas por Región')
    st.plotly_chart(fig_scatter_region)

    # Gráfico de líneas
    fig_line_region = px.line(grouped_region_data, x='Mes', y='Total_Ventas', color='Region', title='Tendencia de Ventas por Región')
    st.plotly_chart(fig_line_region)

# Pestaña 3: Resumen General
with tab3:
    st.header("Resumen General")
    
    # Filtros
    date_range = st.sidebar.date_input("Selecciona el rango de fechas", 
                                         [data['Mes'].min().date(), data['Mes'].max().date()])
    
    # Verificar que el rango tiene al menos dos fechas
    if len(date_range) == 2:
        # Asegurarse de que se comparen tipos de datetime
        filtered_summary = grouped_data[(grouped_data['Mes'] >= pd.to_datetime(date_range[0])) & 
                                        (grouped_data['Mes'] <= pd.to_datetime(date_range[1]))]
    
        # Gráfico de barras de resumen total de ventas
        fig_bar_summary = px.bar(filtered_summary, x='Mes', y='Total_Ventas', title='Ventas Totales por Mes')
        st.plotly_chart(fig_bar_summary)

        # Gráfico de líneas para cantidad total
        fig_line_quantity = px.line(filtered_summary, x='Mes', y='Total_Cantidad', title='Cantidad Total de Ventas por Mes')
        st.plotly_chart(fig_line_quantity)


# Pestaña 4: Mapa

#with tab4:
 #   st.header("Mapa Interactivo por Región")

    # Agrupamiento de datos por Región para Total de Ventas
    #region_sales_data = data.groupby('Region').agg(Total_Ventas=('Precio', 'sum')).reset_index()

    # Crear el mapa base
    #m = folium.Map(location=[-33.45, -70.65], zoom_start=4)  # Ubicación genérica

    # Añadir marcadores por región con ventas
    #for idx, row in region_sales_data.iterrows():
     #   folium.Marker(
      #      location=[-33.45 + idx * 0.1, -70.65 + idx * 0.1],  # Simular diferentes posiciones
       #     popup=f"{row['Region']}: Ventas totales: {row['Total_Ventas']}",
        #    tooltip=row['Region']
        #).add_to(m)

    # Renderizar el mapa en Streamlit
    #st_folium (m, width=700, height=500)


# Mensaje final
st.markdown("### Explora los datos utilizando los filtros disponibles para obtener diferentes perspectivas.")
