  
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# Ruta al archivo .zip que contiene los shapefiles
zip_path = 'C:/Users/vfernand/Desktop/archivos proyecto PYTHON/Otros/barrios ine.zip'

# Crear pestañas en Streamlit
tab1, tab2 = st.tabs(["Mapa de Polígonos", "Información del GeoDataFrame"])

with tab1:
    st.header("Mapa de Polígonos")

    # Cargar el shapefile desde el archivo .zip
    gdf = gpd.read_file(f'zip://{zip_path}')
    
    # Convertir CRS a EPSG:3857 para usar el mapa base
    gdf = gdf.to_crs(epsg=3857)

    # Crear el mapa de polígonos
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, edgecolor='black', facecolor='lightblue', alpha=0.5)
    
    # Agregar un mapa base (OpenStreetMap)
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    
    # Mostrar el mapa en Streamlit
    st.pyplot(fig)

with tab2:
    st.header("Información del GeoDataFrame")
    
    # Mostrar las primeras filas del GeoDataFrame
    st.write(gdf.head())

       