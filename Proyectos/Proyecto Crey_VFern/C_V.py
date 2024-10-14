import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as  px

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
Cat = P_Urbanos[P_Urbanos['cod_dep'] == 'V']

# Eliminar los apartamentos duplicados y quedarte solo con un registro por padrón
Cat = Cat.drop_duplicates(subset='pad').reset_index(drop=True)

# Reemplazar cadenas vacías o '/  /' por NaN
Cat['Fecha_UDJ'] = Cat['Fecha_UDJ'].replace(['', '/  /'], pd.NA)

# Separar la columna 'Fecha' en tres nuevas columnas, manejando valores NaN
Cat[['dia', 'mes', 'anio']] = Cat['Fecha_UDJ'].str.split('/', expand=True)

# Convertir las nuevas columnas a tipo entero, usando fillna para evitar errores
Cat['dia'] = Cat['dia'].astype('Int64')  # 'Int64' permite valores NA
Cat['mes'] = Cat['mes'].astype('Int64')
Cat['anio'] = Cat['anio'].astype('Int64')

# Mostrar el DataFrame resultante
Cat.head()



Dic_Cat = pd.read_csv('C:/Users/vfernand/Desktop/archivos proyecto PYTHON/Diccionario variables catastro.csv', sep=';', encoding='latin1')

# Contar la cantidad de registros por año
resultado_cat_per = Cat.groupby('anio').size().reset_index(name='cantidad_registros')

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
p_conteo_por_anio = p_sin_duplicados.groupby('anio').size().reset_index(name='cantidad_registros')

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
resultado_per_cat = per_cat.groupby(['anio', 'mes']).size().reset_index(name ='conteo_año')

# %%
# Colocar la imagen en el encabezado
st.image("C:/Users/vfernand/Desktop/archivos proyecto PYTHON/Imagen carátula.jpg", width=700)

st.subheader('Análisis descriptivo y comparativo')

#Creo una barra lateral para el filtro
st.sidebar.header('Descripción de las bases:')
st.sidebar.subheader('Catastro: Padrones Urbanos a nivel nacional, con la fecha de la última declaración y registra todas las superficies afectadas. https://catalogodatos.gub.uy/dataset/direccion-nacional-de-catastro-padrones-urbanos-y-rurales/resource/14a3e2e5-a7c4-4795-8baf-f56691765d8e ')   
st.sidebar.subheader('Permisos: Permisos solicitados y aprobados por padrón y superficie afectada por el mismo. https://catalogodatos.gub.uy/dataset/permisos-de-construccion-aprobados')   

# Creo las tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([':skin-tone-6: Bases de datos', ':bar_chart: Gráfico' , '📈 Región', 'otro', 'otro2'])

with tab1:
    st.header('Base de Datos')
    st.subheader('Pueden descargarse las base de datos y diccionarios de ambas bases.')
    
    # Crear un selectbox en la primera pestaña
    opcion1 = st.selectbox('Selecciona una opción:', ['Catastro', 'Permisos'])
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
    
   
# Pestaña 2: Gráfico 
with tab2:
    st.subheader(':bar_chart: Gráfico')
         
    # Crear columnas para mostrar dos cuadros uno al lado del otro
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Catastro")
        st.dataframe(resultado_cat_per)  # Mostrar el DataFrame de Catastro en la primera columna

    with col2:
        st.subheader("Permisos")
        st.dataframe(resultado_per_cat)  # Mostrar el DataFrame de Permisos en la segunda columna
 
    

# Pestaña 3: Gráfico por región
with tab3:
    st.header('git add Región')
      

#Pestaña 4: Gráfico por región
with tab3:
    st.header('📈 Región')
    
    
    
#Pestaña 5: Gráfico por región
with tab3:
    st.header('📈 Región')
    
