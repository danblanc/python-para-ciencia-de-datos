import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
import geopandas as gpd
import contextily as ctx


# Definir los nombres de las columnas
Variables= ['cod_reg', 'cod_dep', 'cod_loc', 'pad', 'block', 'EP', 'uni', 'sup_predio','sup_edificada', 'V_cat_terreno',
            'V_cat_mejoras',  'V_cat_total', 'V_impuestos', 'Fecha_UDJ', 'Vigencia_UDJ']  

# Especificar los tipos de datos para las columnas
dtypes = {
    'cod_reg': str,
    'cod_dep': str,
    'cod_loc': str,  # O str, dependiendo de tus datos
    'pad': int,
    'block': str,
    'EP': str,
    'uni': int,
    'sup_predio': int,
    'sup_edificada': int,
    'V_cat_terreno': int,
    'V_cat_mejoras': int,
    'V_cat_total': int,
    'V_impuestos': int,
    'Fecha_UDJ': bool,
    'Vigencia_UDJ': bool
}

# Leer el archivo CSV y asignar los nombres a las columnas
P_Urbanos = pd.read_csv('C:/Users/vfernand/Desktop/archivos proyecto PYTHON/DatosAbiertosDNC(2024-09)/Padrones Urbanos.csv',
sep=',', encoding='cp1252', header=None, names=Variables, dtype={4: str, 5: str}  )

# Mostrar las primeras filas del archivo
P_Urbanos.head(8)

# Filtrar filas donde 'cod_dep' es igual a 'V' que es Montevideo
filtro_dep = P_Urbanos[P_Urbanos['cod_dep'] == 'V']

# Mostrar el DataFrame filtrado
filtro_dep.head()

# Eliminar los apartamentos duplicados y quedarte solo con un registro por padrón
filtro_dep = filtro_dep.drop_duplicates(subset='pad').reset_index(drop=True)

# Mostrar el DataFrame filtrado
filtro_dep.head()

# Reemplazar cadenas vacías o '/  /' por NaN
filtro_dep['Fecha_UDJ'] = filtro_dep['Fecha_UDJ'].replace(['', '/  /'], pd.NA)

# Separar la columna 'Fecha' en tres nuevas columnas, manejando valores NaN
filtro_dep[['dia', 'mes', 'anio']] = filtro_dep['Fecha_UDJ'].str.split('/', expand=True)

# Convertir las nuevas columnas a tipo entero, usando fillna para evitar errores
filtro_dep['dia'] = filtro_dep['dia'].astype('Int64')  # 'Int64' permite valores NA
filtro_dep['mes'] = filtro_dep['mes'].astype('Int64')
filtro_dep['anio'] = filtro_dep['anio'].astype('Int64')

# Mostrar el DataFrame resultante
filtro_dep.head()

Cat = filtro_dep[filtro_dep['anio'] >= 1997]

Dic_Cat = pd.read_csv('C:/Users/vfernand/Desktop/archivos proyecto PYTHON/Diccionario variables catastro.csv', sep=';', encoding='latin1')

# %%
#Permisos Intendencia Montevideo
# Leer el archivo CSV y asignar los nombres a las columnas
Permisos = pd.read_csv('C:/Users/vfernand/Desktop/archivos proyecto PYTHON/permisos_construccion.csv', sep=';')

Permisos.rename(columns={'padron': 'pad'}, inplace=True)
# Mostrar las primeras filas del archivo
Permisos.head()

# Ver los tipos de datos de cada columna
tipos_datos = Permisos.dtypes

Dic_Per = pd.read_csv('C:/Users/vfernand/Desktop/archivos proyecto PYTHON/Diccionario variables permisos.csv', sep=';', encoding='latin1')

# Mostrar los tipos de datos
print(tipos_datos)

#Crear en permisos la variable cod_dep
Permisos['cod_dep'] = 'V'

# Ordenar el DataFrame por Padron (ascendente), anio, mes, area en orden descendente me quedo con el ùltimo permiso aprobado para ese padron y el area màs grande de esa fecha.
Permisos_ordenado = Permisos.sort_values(by=['pad','anio', 'mes', 'area'], ascending=[True,False, False, False])

# Mostrar el DataFrame ordenado
Permisos_ordenado.head(15)

# Primero, eliminamos duplicados por padròn para quedarnos con el ùtimo registro en año para ese padròn.

p_sin_duplicados = Permisos_ordenado.drop_duplicates(subset=['pad','anio','mes'])

p_sin_duplicados.head(15)

# Contar cuántos registros hay por 'anio' y 'mes'
resultado = p_sin_duplicados.groupby(['anio', 'mes']).size().reset_index(name ='conteo_destino')

# Mostrar el resultado
print(resultado)

# Contar la cantidad de registros por año
p_conteo_por_anio = p_sin_duplicados.groupby('anio').size().reset_index(name='Cantidad')
p_conteo_por_anio = p_conteo_por_anio[p_conteo_por_anio['anio'] >= 1997]

print(p_conteo_por_anio)

# Supongamos que 'resultado' es tu DataFrame que contiene los conteos
# Calcular la suma total de 'conteo_destino'
suma_conteo_destino = resultado['conteo_destino'].sum()

# Mostrar la suma total
print(f"Suma total de conteo_destino: {suma_conteo_destino}")

# %%
# Machear los DataFrames usando un left join
cat_per = pd.merge(Cat, Permisos, on=['anio','mes','pad'], how='left')

# Machear los DataFrames usando un left join
per_cat = pd.merge(p_sin_duplicados,Cat, on=['anio','mes','pad'], how='left')

# Contar cuántos registros hay por 'anio' y 'mes'
resultado_per_cat = per_cat.groupby(['anio']).size().reset_index(name ='Cantidad')


# %%
#Luego de un análisis profundo de las tablas y resultando que Catastro tiene apto y Permisos no.
#decidimos incorporar un nuevo archivo de la Intendencia de Montevideo que posee ambas bases macheadas por ellos.

#################  Catastro  e Intendencia Montevideo

# Leer el archivo CSV 
Cat_Permisos = pd.read_csv('C:/Users/vfernand/Desktop/archivos proyecto PYTHON/v_ce_permisos_construccion_geom.csv', sep=';' , encoding='cp1252')

Cat_Permisos.head()

# Reemplazar las comas por puntos o eliminar las comas si los números son enteros
Cat_Permisos['AREA_EDIF'] = Cat_Permisos['AREA_EDIF'].str.replace(',', '').astype(float)

# Convertir la columna a enteros
Cat_Permisos['AREA_EDIF'] = Cat_Permisos['AREA_EDIF'].astype('Int64')

# Ver los tipos de datos de cada columna
tipos_datos = Cat_Permisos.dtypes
print(tipos_datos)

Dic_Cat_Per = pd.read_csv('C:/Users/vfernand/Desktop/archivos proyecto PYTHON/Diccionario_v_ce_permisos_construccion_geom.csv', sep=';', encoding='latin1')

Cat_Permisos = Cat_Permisos.rename(columns={'ANIO_APRO': 'anio'})

# Contar la cantidad de registros por año
resultado_Cat_Permisos = Cat_Permisos.groupby('anio').size().reset_index(name='Cantidad')
resultado_Cat_Permisos = resultado_Cat_Permisos[resultado_Cat_Permisos['anio'] >= 1997]

#Recodificar destinos
mapeo_DSC_DESTIN = {
    'Comercio': 'Comercio',
    'Comercio, Industria, Otros': 'Varios destinos',
    'Comercio,Industria': 'Varios destinos',
    'Comercio,Otros': 'Varios destinos',
    'Industria': 'Industria',
    'Industria,Otros': 'Varios destinos',
    'Vivienda': 'Vivienda',
    'Vivienda, Industria, Otros': 'Varios destinos',
    'Vivienda,Comercio': 'Varios destinos',
    'Vivienda,Comercio,Industria': 'Varios destinos',
    'Vivienda,Comercio,Otros': 'Varios destinos',
    'Vivienda,Industria': 'Varios destinos',
    'Vivienda,Otros': 'Varios destinos',
    'Desconocido' : 'Sin destino definido',
    'Otros': 'Sin destino definido'         
}

Cat_Permisos['Nuevo_Destino'] = Cat_Permisos['DSC_DESTIN'].map(mapeo_DSC_DESTIN)

print(Cat_Permisos['Nuevo_Destino'].unique())



print(resultado_Cat_Permisos)

# %%
# Colocar la imagen en el encabezado
st.image("C:/Users/vfernand/Desktop/archivos proyecto PYTHON/Imagen carátula.jpg", width=700)

st.subheader('Análisis descriptivo y comparativo')

#Creo una barra lateral para el filtro
st.sidebar.header('Descripción de las bases:')
st.sidebar.subheader('Catastro: Padrones Urbanos a nivel nacional, con la fecha de la última declaración y registra todas las superficies afectadas. https://catalogodatos.gub.uy/dataset/direccion-nacional-de-catastro-padrones-urbanos-y-rurales/resource/14a3e2e5-a7c4-4795-8baf-f56691765d8e ')   
st.sidebar.subheader('Permisos: Permisos solicitados y aprobados por padrón y superficie afectada por el mismo. https://catalogodatos.gub.uy/dataset/permisos-de-construccion-aprobados')   
st.sidebar.subheader('Cat_Per: Permisos solicitados y aprobados con información de catastro. https://intgis.montevideo.gub.uy/sit/php/common/datos/generar_zip2.php?nom_tab=v_mdg_parcelas_geom&tipo=gis')

# Creo las tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([':skin-tone-6: Bases de datos', 'Análisis por año' , 'Mapa', 'otro', 'otro2'])

with tab1:
    st.header('Base de Datos')
    st.subheader('Pueden descargarse las base de datos y diccionarios de ambas bases.')
    
    # Crear un selectbox en la primera pestaña
    opcion1 = st.selectbox('Selecciona una opción:', ['Catastro', 'Permisos', 'Cat_Per'])
    st.write(f'Has seleccionado: {opcion1}')
    
        # Mostrar la base de datos correspondiente
    if opcion1 == "Catastro":
        st.dataframe(P_Urbanos)  # Mostrar la base de datos de Catastro
        st.subheader("Diccionario de Variables - Catastro")
        st.write(Dic_Cat)  # Mostrar el diccionario de variables de Catastro

    elif opcion1 == "Permisos":
        st.dataframe(Permisos)  # Mostrar la base de datos de Permisos
        st.subheader("Diccionario de Variables - Permisos")
        st.write(Dic_Per)  # Mostrar el diccionario de variables de Catastro
        
    elif opcion1 == "Cat_Per":
        st.dataframe(Cat_Permisos)  # Mostrar la base de datos de Cat_Permisos
        st.subheader("Diccionario de Variables - Cat_Permisos")
        st.write(Dic_Cat_Per)  # Mostrar el diccionario de variables de Cat_Permisos
   
# Pestaña 2: Conteo por año 
with tab2:
    st.subheader('Bases agrupadas por año')
         
    # Crear columnas para mostrar dos cuadros uno al lado del otro
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Catastro")
        st.dataframe(resultado_cat_per)  # Mostrar el DataFrame de Catastro en la primera columna

    with col2:
        st.subheader("Permisos")
        st.dataframe(resultado_per_cat)  # Mostrar el DataFrame de Permisos en la segunda columna
 
    with col3:
        st.subheader("Cat_Permisos")
        st.dataframe(resultado_Cat_Permisos)  # Mostrar el DataFrame de Permisos en la segunda columna
        
    st.markdown("###### Por los análisis realizados anteriormente y este, llegamos a la conclución que faltan variables en DGC e IM como para realizar un correcto join, por lo tanto la presentación a partir de aquí será dela última base de datos") 
    

# Pestaña 3: Mapa
    with tab3:
        st.subheader('Mapa')

    # Ruta al archivo .zip que contiene los shapefiles
    zip_path = 'C:/Users/vfernand/Desktop/archivos proyecto PYTHON/paisurbano_shp.zip'

    # Cargar el shapefile desde el archivo .zip
    gdf = gpd.read_file(f'zip://{zip_path}')

    # Mostrar las primeras filas para verificar la carga de los datos
    print(gdf)

    # Crear un mapa simple de los polígonos
    gdf.plot(edgecolor='black', facecolor='lightblue')

    # Agregar título y etiquetas
    plt.title('Mapa de Polígonos desde un Shapefile comprimido en ZIP')
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')

    # Mostrar el mapa
    plt.show()
       
 
 
      

#Pestaña 4: Gráfico por región
with tab4:
    st.header('📈 Destinos')
    
    df = resultado_Cat_Permisos.groupby('anio').size().reset_index(name='Cantidad')   
    
    # Crear gráfico de líneas por destino y años
    fig = px.line(df, x='ANIO_APRO', y='Cantidad', color='DSC_DESTIN', title="Evolución de valores por destino según años")

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)
    
    
    
    
#Pestaña 5: Gráfico por región
with tab5:
    st.header('📈 Región')
    
