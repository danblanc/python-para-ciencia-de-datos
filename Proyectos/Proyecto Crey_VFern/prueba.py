import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
import geopandas as gpd
import contextily as ctx
import folium 
from streamlit_folium import st_folium

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

Dic_Cat = pd.read_csv('C:/Users/vfernand/Desktop/archivos proyecto PYTHON/Diccionario variables catastro.csv', sep=';', encoding='latin1')

# Mostrar las primeras filas del archivo
P_Urbanos.head(8)

# Filtrar filas donde 'cod_dep' es igual a 'V' que es Montevideo
filtro_dep = P_Urbanos[P_Urbanos['cod_dep'] == 'V']

# Mostrar el DataFrame filtrado
filtro_dep.head()

# Eliminar los apartamentos duplicados y quedarte solo con un registro por padrón
filtro_dep = filtro_dep.drop_duplicates(subset='pad').reset_index(drop=True)

# Reemplazar cadenas vacías o '/  /' por NaN
filtro_dep['Fecha_UDJ'] = filtro_dep['Fecha_UDJ'].replace(['', '/  /'], pd.NA)

# Separar la columna 'Fecha' en tres nuevas columnas, manejando valores NaN
filtro_dep[['dia', 'mes', 'anio']] = filtro_dep['Fecha_UDJ'].str.split('/', expand=True)

# Convertir las nuevas columnas a tipo entero, usando fillna para evitar errores
filtro_dep['dia'] = filtro_dep['dia'].astype('Int64')  # 'Int64' permite valores NA
filtro_dep['mes'] = filtro_dep['mes'].astype('Int64')
filtro_dep['anio'] = filtro_dep['anio'].astype('Int64')

#filtro registros anteriores a 1997
filtro_dep = filtro_dep[filtro_dep['anio'] >= 1997]

#Agrupo por anio
resultado_Cat_Per=filtro_dep.groupby(['anio','mes']).size().reset_index(name ='Cantidad')


# %%
#Permisos Intendencia Montevideo
# Leer el archivo CSV y asignar los nombres a las columnas
Permisos = pd.read_csv('C:/Users/vfernand/Desktop/archivos proyecto PYTHON/permisos_construccion.csv', sep=';')
Dic_Per = pd.read_csv('C:/Users/vfernand/Desktop/archivos proyecto PYTHON/Diccionario variables permisos.csv', sep=';', encoding='latin1')

Permisos.rename(columns={'padron': 'pad'}, inplace=True)
# Mostrar las primeras filas del archivo
Permisos.head()

# Ver los tipos de datos de cada columna
tipos_datos = Permisos.dtypes

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

# Contar la cantidad de registros por año
resultado_Per_Cat = p_sin_duplicados.groupby(['anio','mes']).size().reset_index(name='Cantidad')

# %%
# Machear los DataFrames usando un left join
cat_per = pd.merge(filtro_dep, Permisos, on=['anio','mes','pad'], how='left')

# Machear los DataFrames usando un left join
per_cat = pd.merge(p_sin_duplicados,filtro_dep, on=['anio','mes','pad'], how='left')


# %%
#Luego de un análisis profundo de las tablas y resultando que Catastro tiene apto y Permisos no.
#decidimos incorporar un nuevo archivo de la Intendencia de Montevideo que posee ambas bases macheadas por ellos.

#################  Catastro  e Intendencia Montevideo

# Leer el archivo CSV 
Cat_Permisos = pd.read_csv('C:/Users/vfernand/Desktop/archivos proyecto PYTHON/v_ce_permisos_construccion_geom.csv', sep=';' , encoding='cp1252')
Dic_Cat_Per = pd.read_csv('C:/Users/vfernand/Desktop/archivos proyecto PYTHON/Diccionario_v_ce_permisos_construccion_geom.csv', sep=';', encoding='latin1')

Cat_Permisos.head()

# Reemplazar las comas por puntos o eliminar las comas si los números son enteros
Cat_Permisos['AREA_EDIF'] = Cat_Permisos['AREA_EDIF'].str.replace(',', '').astype(float)

# Convertir la columna a enteros
Cat_Permisos['AREA_EDIF'] = Cat_Permisos['AREA_EDIF'].astype('Int64')

Cat_Permisos = Cat_Permisos[Cat_Permisos['ANIO_APRO'] >= 1997]

Cat_Permisos = Cat_Permisos.rename(columns={'ANIO_APRO': 'anio'})

Cat_Permisos = Cat_Permisos.rename(columns={'MES_APRO': 'mes'})


# Ver los tipos de datos de cada columna
tipos_datos = Cat_Permisos.dtypes
print(tipos_datos)

## Contar la cantidad de registros por año
resultado_Cat_Permisos = Cat_Permisos.groupby(['anio','mes']).size().reset_index(name='Cantidad')

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

#Recodificar destinos
mapeo_DSC_REGIME = {
    'Común': 'Común',
    'Incorporaci??n': 'Propiedad Horizontal',
    'Propiedad Horizontal' : 'Propiedad Horizontal',
    'Desconocido': 'Sin codigo de régimen'         
}

Cat_Permisos['DSC_REGIME'] = Cat_Permisos['DSC_REGIME'].map(mapeo_DSC_REGIME)

Cat_Permisos['Cantidad'] = 1


Cat_Permisos_agrupado = Cat_Permisos.groupby(['anio','mes','DSC_REGIME']).size().reset_index(name='Cantidad')

conteo_destino = Cat_Permisos['Nuevo_Destino'].value_counts().reset_index()
conteo_destino.columns = ['Destino', 'Cantidad']

casos_por_año_destino = Cat_Permisos.groupby(['anio','mes','Nuevo_Destino']).size().reset_index(name='Cantidad')


Cat_Permisos['FECHA_INI'] = pd.to_datetime(Cat_Permisos['FECHA_INI'], format='%d/%m/%Y', errors='coerce')
Cat_Permisos['FECHA_APRO'] = pd.to_datetime(Cat_Permisos['FECHA_APRO'], format='%d/%m/%Y', errors='coerce')

Cat_Permisos['T_Demora'] = (Cat_Permisos['FECHA_APRO'] - Cat_Permisos['FECHA_INI']).dt.days
Cat_Permisos['año_ini'] = Cat_Permisos['FECHA_INI'].dt.year

PROM_DEMORA_por_año = Cat_Permisos.groupby('año_ini')['T_Demora'].mean().reset_index()

PROM_DEMORA_por_año.rename(columns={'T_Demora': 'Promedio_T_Demora'}, inplace=True)

PROM_DEMORA_por_año['Promedio_T_Demora'] = PROM_DEMORA_por_año['Promedio_T_Demora'].astype(int)

#Recodificar Tipo de obra
mapeo_DSC_TIPO_O = {
    'Obra Nueva': 'Obra Nueva',
    'Regularizacion - Año' : 'Regularización',
    'Reforma': 'Reforma',
    'Reforma a Regularizar': 'Regularización',
    'Incorporacion A.P.H.': 'Incorporacion P.H.',
    'Pilotaje': 'Otros',
    'Estacionamiento': 'Otros',
    'Obra nueva / ampliaci??n': 'Obra Nueva',
    'Demolicion': 'Demolición',
    'A regularizar': 'Regularización',
    'Autorizada': 'Otros',
    'Reciclaje': 'Otros',
    'Regularizaci??n de reforma': 'Regularización',
    'Desconocido' : 'Sin tipo de obra definido',
    'Galpon' : 'Otros',
    'Marquesina':'Otros',
    'Toldo':'Otros',
    'A ocupar':'Otros',
    'Cielo A. Autorizada':'Otros',
    'Cielo A. A regularizar':'Otros',
    '  ':'Sin tipo de obra definido',
    'Incorporaci??n a PH': 'Incorporacion P.H.'         
}

Cat_Permisos['Tipo_Obra'] = Cat_Permisos['DSC_TIPO_O'].map(mapeo_DSC_TIPO_O)

# Agrupamos por 'anio', 'mes', 'Nuevo_Destino', 'Tipo_Obra' y sumamos 'AREA_EDIF' y 'Cantidad'
Tipo_de_obra = Cat_Permisos.groupby(['anio', 'mes', 'Nuevo_Destino', 'Tipo_Obra'])[['AREA_EDIF', 'Cantidad']].sum().reset_index()

# Renombramos las columnas directamente al hacer el reset_index
Tipo_de_obra.columns = ['anio', 'mes', 'Nuevo_Destino', 'Tipo_Obra', 'Suma_Area_Edificada', 'Suma_Cantidad']

# Mostramos el DataFrame con los nuevos nombres
print(Tipo_de_obra)


# %%
# Colocar la imagen en el encabezado
st.image("C:/Users/vfernand/Desktop/archivos proyecto PYTHON/Imagen carátula.jpg", width=700)

st.subheader('Análisis descriptivo y comparativo')

#Creo una barra lateral 
st.sidebar.header('Descripción de las bases:')
st.sidebar.subheader('Catastro: Padrones Urbanos a nivel nacional, con la fecha de la última declaración y registra todas las superficies afectadas. https://catalogodatos.gub.uy/dataset/direccion-nacional-de-catastro-padrones-urbanos-y-rurales/resource/14a3e2e5-a7c4-4795-8baf-f56691765d8e ')   
st.sidebar.subheader('Permisos: Permisos solicitados y aprobados por padrón y superficie afectada por el mismo. https://catalogodatos.gub.uy/dataset/permisos-de-construccion-aprobados')   
st.sidebar.subheader('Cat_Per: Permisos solicitados y aprobados con información de catastro. https://intgis.montevideo.gub.uy/sit/php/common/datos/generar_zip2.php?nom_tab=v_mdg_parcelas_geom&tipo=gis')

#Creo una barra lateral para el filtro
st.sidebar.header('Filtros')


# Creo las tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([':skin-tone-6: Bases', 'Análisis/año' , ':bar_chart: Régimen', 'Tipo de obra', ':bar_chart: Destino', ':bar_chart: Destino/Año', ':chart_with_downwards_trend: Tiempos/Demora', 'Mapa'])

with tab1:
    st.header('Base de Datos')
    st.markdown('###### Pueden descargarse las base de datos y diccionarios.')
    
    
    # Crear un selectbox en la primera pestaña
    opcion1 = st.selectbox('Selecciona una opción:', ['Catastro', 'Permisos', 'Cat_Per_IM'])
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
        
    elif opcion1 == "Cat_Per_IM":
        st.dataframe(Cat_Permisos)  # Mostrar la base de datos de Cat_Permisos
        st.subheader("Diccionario de Variables - Cat_Permisos")
        st.write(Dic_Cat_Per)  # Mostrar el diccionario de variables de Cat_Permisos
   
# Pestaña 2: Conteo por año 
with tab2:
    st.subheader('Bases agrupadas por año')
    
   # Opción para seleccionar el año, incluyendo "Ver Todos"
    year_filter = st.sidebar.selectbox('Selecciona un año:', ['Ver Todos'] + sorted(filtro_dep['anio'].unique()))

    # Si el año no es "Ver Todos", obtener los meses correspondientes
    if year_filter != 'Ver Todos':
        meses_disponibles = ['Ver Todos'] + sorted(filtro_dep[filtro_dep['anio'] == year_filter]['mes'].unique())
        month_filter = st.sidebar.selectbox('Selecciona un mes:', meses_disponibles)
    else:
        month_filter = 'Ver Todos'  # Opción para mostrar todos los meses

    # Filtrar las bases de datos dependiendo de los filtros seleccionados
    if year_filter != 'Ver Todos' and month_filter != 'Ver Todos':
        filtered_cat = resultado_Cat_Per[(resultado_Cat_Per['anio'] == year_filter) & (resultado_Cat_Per['mes'] == month_filter)]
        filtered_per = resultado_Per_Cat[(resultado_Per_Cat['anio'] == year_filter) & (resultado_Per_Cat['mes'] == month_filter)]
        filtered_cat_perm = resultado_Cat_Permisos[(resultado_Cat_Permisos['anio'] == year_filter) & (resultado_Cat_Permisos['mes'] == month_filter)]
    elif year_filter != 'Ver Todos' and month_filter == 'Ver Todos':
        filtered_cat = resultado_Cat_Per[resultado_Cat_Per['anio'] == year_filter]
        filtered_per = resultado_Per_Cat[resultado_Per_Cat['anio'] == year_filter]
        filtered_cat_perm = resultado_Cat_Permisos[resultado_Cat_Permisos['anio'] == year_filter]
    elif year_filter == 'Ver Todos' and month_filter != 'Ver Todos':
        filtered_cat = resultado_Cat_Per[resultado_Cat_Per['mes'] == month_filter]
        filtered_per = resultado_Per_Cat[resultado_Per_Cat['mes'] == month_filter]
        filtered_cat_perm = resultado_Cat_Permisos[resultado_Cat_Permisos['mes'] == month_filter]
    else:
        # Si se selecciona "Ver Todos" en ambos casos, no se filtra nada
        filtered_cat = resultado_Cat_Per
        filtered_per = resultado_Per_Cat
        filtered_cat_perm = resultado_Cat_Permisos
       
    # Crear columnas para mostrar dos cuadros uno al lado del otro
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Catastro")
        st.dataframe(filtered_cat)  # Mostrar el DataFrame de Catastro filtrado

    with col2:
        st.subheader("Permisos")
        st.dataframe(filtered_per)  # Mostrar el DataFrame de Permisos filtrado
 
    with col3:
        st.subheader("Cat_Permisos")
        st.dataframe(filtered_cat_perm)  # Mostrar el DataFrame de Cat_Permisos filtrado
          
    st.markdown("###### Por los análisis realizados anteriormente y este, llegamos a la conclución que faltan variables en DGC e IM como para realizar un correcto join, por lo tanto la presentación a partir de aquí será dela última base de datos") 
    
# Pestaña 3: Régimen
with tab3:
    st.header(':bar_chart: Régimen')

    # Filtrar los datos según el año y el mes seleccionados previamente
    if year_filter != 'Ver Todos' and month_filter != 'Ver Todos':
        datos_filtrados_tab4 = Cat_Permisos_agrupado[
            (Cat_Permisos_agrupado['anio'] == year_filter) & 
            (Cat_Permisos_agrupado['mes'] == month_filter)
        ]
    elif year_filter != 'Ver Todos' and month_filter == 'Ver Todos':
        datos_filtrados_tab4 = Cat_Permisos_agrupado[Cat_Permisos_agrupado['anio'] == year_filter]
    elif year_filter == 'Ver Todos' and month_filter != 'Ver Todos':
        datos_filtrados_tab4 = Cat_Permisos_agrupado[Cat_Permisos_agrupado['mes'] == month_filter]
    else:
        datos_filtrados_tab4 = Cat_Permisos_agrupado  # Si selecciona "Ver Todos", no se filtran los datos

    # Crear gráfico de barras con Plotly
    fig = px.bar(datos_filtrados_tab4, 
                x='anio', 
                y='Cantidad', 
                color='DSC_REGIME', 
                title='Cantidad de Registros por Año y Régimen',
                labels={'Cantidad': 'Cantidad', 'anio': 'Año'},
                barmode='group',
                color_discrete_sequence=['#008080', '#00FFFF', '#98FB98'])   # Agrupar las barras por año

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

# Pestaña 4: Gráfico por Tipo de Obra
with tab4:
    st.header(':bar_chart: Tipo de Obra')

    # Filtrar los datos de Tipo_de_obra según el año y el mes seleccionados
    if year_filter != 'Ver Todos' and month_filter != 'Ver Todos':
        datos_filtrados_tab5 = Tipo_de_obra[
            (Tipo_de_obra['anio'] == year_filter) & 
            (Tipo_de_obra['mes'] == month_filter)
        ]
    elif year_filter != 'Ver Todos' and month_filter == 'Ver Todos':
        datos_filtrados_tab5 = Tipo_de_obra[Tipo_de_obra['anio'] == year_filter]
    elif year_filter == 'Ver Todos' and month_filter != 'Ver Todos':
        datos_filtrados_tab5 = Tipo_de_obra[Tipo_de_obra['mes'] == month_filter]
    else:
        datos_filtrados_tab5 = Tipo_de_obra  # Si se selecciona "Ver Todos", no filtrar

    # Crear gráfico de dispersión con Plotly
    fig = px.scatter(datos_filtrados_tab5, 
                    x='Tipo_Obra', 
                    y='Suma_Area_Edificada', 
                    color='Nuevo_Destino', 
                    title='Área de Edificación por Tipo de Construcción',
                    labels={'Suma_Area_Edificada': 'Área Edificada', 'Tipo_Obra': 'Tipo de Construcción'},
                    color_discrete_sequence=['#008080', '#66CDAA', '#7FFFD4', '#00FFFF', '#98FB98']) 
                    

    # Rotar etiquetas del eje X
    fig.update_layout(xaxis_tickangle=-45)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

        
        
# Pestaña 5: Gráfico de cantidad de casos por Destino
with tab5:
    st.header(':bar_chart: Destino')
    
    # Filtrar los datos de conteo_destino según el año y el mes seleccionados
    if year_filter != 'Ver Todos' and month_filter != 'Ver Todos':
        datos_filtrados_destino = casos_por_año_destino[
            (casos_por_año_destino['anio'] == year_filter) & 
            (casos_por_año_destino['mes'] == month_filter)
        ]
    elif year_filter != 'Ver Todos' and month_filter == 'Ver Todos':
        datos_filtrados_destino = casos_por_año_destino[casos_por_año_destino['anio'] == year_filter]
    elif year_filter == 'Ver Todos' and month_filter != 'Ver Todos':
        datos_filtrados_destino = casos_por_año_destino[casos_por_año_destino['mes'] == month_filter]
    else:
        datos_filtrados_destino = casos_por_año_destino  # Si se selecciona "Ver Todos", no filtrar

    # Crear gráfico de barras con Plotly
    fig_destino = px.bar(datos_filtrados_destino, 
                         x='Nuevo_Destino',  # Asegúrate de que la columna se llame así en el DataFrame
                         y='Cantidad', 
                         color='Nuevo_Destino',  # Colorear cada destino diferente
                         title='Cantidad por Destino',
                         labels={'Cantidad': 'Cantidad', 'Nuevo_Destino': 'Destino'},
                         color_discrete_sequence=['#008080', '#40E0D0', '#17becf', '#48D1CC', '#B2E2E2']) 
                        

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_destino)


# Pestaña 6: Gráfico de cantidad de casos por Destino por Año  
with tab6:
    st.header(':bar_chart: Destino por Año')

    # Filtrar los datos de casos_por_año_destino según el año y el mes seleccionados
    if year_filter != 'Ver Todos' and month_filter != 'Ver Todos':
        datos_filtrados_año_destino = casos_por_año_destino[
            (casos_por_año_destino['anio'] == year_filter) & 
            (casos_por_año_destino['mes'] == month_filter)
        ]
    elif year_filter != 'Ver Todos':
        datos_filtrados_año_destino = casos_por_año_destino[
            casos_por_año_destino['anio'] == year_filter
        ]
    elif month_filter != 'Ver Todos':
        datos_filtrados_año_destino = casos_por_año_destino[
            casos_por_año_destino['mes'] == month_filter
        ]
    else:
        datos_filtrados_año_destino = casos_por_año_destino  # Si se selecciona "Ver Todos", no filtrar

    # Crear gráfico de barras con Plotly
    fig_año_destino = px.bar(datos_filtrados_año_destino, 
                            x='anio', 
                            y='Cantidad', 
                            color='Nuevo_Destino', 
                            title='Cantidad por Año y Destino',
                            labels={'Cantidad': 'Cantidad', 'anio': 'Año', 'Nuevo_Destino': 'Destino'},
                            barmode='stack',  # Apilar las barras
                            color_discrete_sequence=['#008080', '#40E0D0', '#17becf', '#48D1CC', '#B2E2E2']) 

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_año_destino)

#Pestaña 7: Gráfico de cantidad de casos por Destino por Año  
with tab7:
    st.header(':chart_with_downwards_trend: Promedio de Tiempos de Demora por Año')
    
        # Filtrar los datos de Cat_Permisos solo según el año seleccionado
    if year_filter != 'Ver Todos':
        PROM_DEMORA_por_año = PROM_DEMORA_por_año[
            PROM_DEMORA_por_año['año_ini'] == year_filter
        ]
    else:
        PROM_DEMORA_por_año = PROM_DEMORA_por_año  # Si se selecciona "Ver Todos", no filtrar

    # Crear gráfico de líneas
    fig_promedio_demora = px.line(PROM_DEMORA_por_año, 
                            x='año_ini', 
                            y='Promedio_T_Demora', 
                            title='Promedio de Tiempos de Demora por Año',
                            labels={'Promedio_T_Demora': 'Promedio de Demora', 'año_ini': 'Año', 'Nuevo_Destino':'Destino'},
                            markers=True,  # Agregar marcadores a las líneas
                            color_discrete_sequence=['#00CED1'])  # Cambia el color de la línea (Ejemplo: rojo-naranja)
    
    
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_promedio_demora)


# Pestaña 8: Mapa
with tab8:  
    st.header('Mapa desde Shapefile')
    
    # Cargar el shapefile (cambia la ruta al archivo .shp que descargaste)
    shapefile_path = 'C:/Users/vfernand/Desktop/archivos proyecto PYTHON/v_ce_permisos_construccion_geom/v_ce_permisos_construccion_geom.shp'
    gdf = gpd.read_file(shapefile_path)

    # Crear un mapa base centrado en Montevideo
    mapa = folium.Map(location=[-34.9011, -56.1645], zoom_start=12)

    # Añadir el shapefile al mapa
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row['geometry'],
            popup=f"PADRON: {row.get('PADRON', 'Sin información')}"  # Asegúrate de usar el nombre correcto de la columna
        ).add_to(mapa)

    # Mostrar el mapa en Streamlit
    st_folium(mapa, width=700)


