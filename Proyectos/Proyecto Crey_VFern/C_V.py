import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
import geopandas as gpd
import contextily as ctx


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
resultado_Cat_Per=filtro_dep.groupby(['anio']).size().reset_index(name ='Cantidad')


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
resultado_Per_Cat = p_sin_duplicados.groupby('anio').size().reset_index(name='Cantidad')

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


# Ver los tipos de datos de cada columna
tipos_datos = Cat_Permisos.dtypes
print(tipos_datos)

## Contar la cantidad de registros por año
resultado_Cat_Permisos = Cat_Permisos.groupby('anio').size().reset_index(name='Cantidad')

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


Cat_Permisos_agrupado = Cat_Permisos.groupby(['anio','DSC_REGIME']).size().reset_index(name='Cantidad')

conteo_destino = Cat_Permisos['Nuevo_Destino'].value_counts().reset_index()
conteo_destino.columns = ['Destino', 'Cantidad']

casos_por_año_destino = Cat_Permisos.groupby(['anio', 'Nuevo_Destino']).size().reset_index(name='Cantidad')


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

Tipo_de_obra = Cat_Permisos.groupby(['anio','MES_APRO','DSC_TIPO_O']).size().reset_index(name='Cantidad_TI_O')

print(Cat_Permisos['DSC_TIPO_O'].unique())




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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([':skin-tone-6: Bases de datos', 'Análisis por año' , 'Mapa', ':bar_chart: Régimen', 'Tipo de obra', ':bar_chart: Destino', ':bar_chart: Destino por Año', ':chart_with_downwards_trend: Promedio de Tiempos de Demora por Año'])

with tab1:
    st.header('Base de Datos')
    st.subheader('Pueden descargarse las base de datos y diccionarios de ambas bases.')
    
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
         
    # Crear columnas para mostrar dos cuadros uno al lado del otro
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Catastro")
        st.dataframe(resultado_Cat_Per)  # Mostrar el DataFrame de Catastro en la primera columna

    with col2:
        st.subheader("Permisos")
        st.dataframe(resultado_Per_Cat)  # Mostrar el DataFrame de Permisos en la segunda columna
 
    with col3:
        st.subheader("Cat_Permisos")
        st.dataframe(resultado_Cat_Permisos)  # Mostrar el DataFrame de Permisos en la segunda columna
        
    st.markdown("###### Por los análisis realizados anteriormente y este, llegamos a la conclución que faltan variables en DGC e IM como para realizar un correcto join, por lo tanto la presentación a partir de aquí será dela última base de datos") 
    

# Pestaña 3: Mapa
    with tab3:
        st.subheader('Mapa')

    
     

#Pestaña 4: Gráfico por región
with tab4:
    st.header(':bar_chart: Régimen')
    
 
    # Crear gráfico de barras con Plotly
    fig = px.bar(Cat_Permisos_agrupado, 
                 x='anio', 
                 y='Cantidad', 
                 color='DSC_REGIME', 
                 title='Cantidad de Registros por Año',
                 labels={'Cantidad': 'Cantidad', 'anio': 'Año'},
                 barmode='group')  # Agrupar las barras por año

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)
       
  
    
    
#Pestaña 5: Gráfico por región
with tab5:
    fig, Tipo_de_obra = plt.subplots()
    Tipo_de_obra.scatter(['Tipo_Obra'], ['Destino'])
    plt.show()
    
    
    
#Pestaña 6: Gráfico de cantidad de casos por Destino   (se puede dejar esto y o la tabla 7)
with tab6:
    st.header(':bar_chart: Destino')

    # Crear gráfico de barras con Plotly
    fig_destino = px.bar(conteo_destino, 
                     x='Destino', 
                     y='Cantidad', 
                     title='Cantidad por Destino',
                     labels={'Cantidad': 'Cantidad', 'Destino': 'Destino'})

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_destino)

#Pestaña 7: Gráfico de cantidad de casos por Destino por Año  
with tab7:
    st.header(':bar_chart: Destino por Año')

    # Crear gráfico de barras con Plotly
      
    fig_año_destino = px.bar(casos_por_año_destino, 
                          x='anio', 
                          y='Cantidad', 
                          color='Nuevo_Destino', 
                          title='Cantidad por Año y Destino',
                          labels={'Cantidad': 'Cantidad', 'anio': 'Año' , 'Nuevo_Destino':'Destino'},
                          barmode='stack', # Apilar las barras
                        color_discrete_sequence=['#008080', '#40E0D0', '#17becf', '#48D1CC', '#F5FFFA']) 
    

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_año_destino)
    
#Ver el promedio de demora en días entre que se incia el expediente y se otorga el permiso
with tab8:
    st.header(':chart_with_downwards_trend: Promedio de Tiempos de Demora por Año')

    # Crear gráfico de líneas
    fig_promedio_demora = px.line(PROM_DEMORA_por_año, 
                            x='año_ini', 
                            y='Promedio_T_Demora', 
                            title='Promedio de Tiempos de Demora por Año',
                            labels={'Promedio_T_Demora': 'Promedio de Demora', 'año_ini': 'Año', 'Nuevo_Destino':'Destino'},
                            markers=True,  # Agregar marcadores a las líneas
                            color_discrete_sequence=['#FF5733'])  # Cambia el color de la línea (Ejemplo: rojo-naranja)
    
    


    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_promedio_demora)
    
