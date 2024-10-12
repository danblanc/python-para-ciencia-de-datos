# %%
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

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
P_Urbanos = pd.read_csv('C:/Users/macar/Desktop/python-para-ciencia-de-datos/DatosAbiertosDNC(2024-09)/Padrones Urbanos.csv', sep=',', encoding='cp1252', header=None, names=Variables, dtype={4: str, 5: str}  )

# Mostrar las primeras filas del archivo
P_Urbanos.head(8)

# %%
# Filtrar filas donde 'cod_dep' es igual a 'V' que es Montevideo
filtro_dep = P_Urbanos[P_Urbanos['cod_dep'] == 'V']


# Mostrar el DataFrame filtrado
filtro_dep.head()

# %%

# Eliminar los apartamentos duplicados y quedarte solo con un registro por padrón
filtro_dep = filtro_dep.drop_duplicates(subset='pad').reset_index(drop=True)

# Mostrar el DataFrame filtrado
filtro_dep.head()

# %%
#cantidad de filas y columnas del archivo
filtro_dep.shape   

# %%
#CUantas filas tiene el archivo
num_filas = filtro_dep.shape[0]

print(num_filas)

# %%
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

# %%
# Ver los tipos de datos de cada columna
tipos_datos = filtro_dep.dtypes

# Mostrar los tipos de datos
print(tipos_datos)

# %%
# Contar la cantidad de registros por año
conteo_por_anio = filtro_dep.groupby('anio').size().reset_index(name='cantidad_registros')

print(conteo_por_anio)

# %%
#Permisos Intendencia Montevideo
# Leer el archivo CSV y asignar los nombres a las columnas
Permisos = pd.read_csv('C:/Users/macar/Desktop/python-para-ciencia-de-datos/permisos_construccion.csv', sep=';')

Permisos.rename(columns={'padron': 'pad'}, inplace=True)
# Mostrar las primeras filas del archivo
Permisos.head()

# %%
# Ver los tipos de datos de cada columna
tipos_datos = Permisos.dtypes

# Mostrar los tipos de datos
print(tipos_datos)

# %%
#Crear en permisos la variable cod_dep
Permisos['cod_dep'] = 'V'
Permisos.head()

# %%
# Supongamos que 'resultado' es tu DataFrame que contiene los conteos        ### ESto lo eliminaría, no aporta nada
# Calcular la suma total de 'conteo_destino'
conteo_pad = Permisos['pad'].count()

# Mostrar la suma total
print(f"Suma total de conteo_pad: {conteo_pad}")

# %%
#CUantas filas tiene el archivo                                             ### también lo eliminaría
num_filas = Permisos.shape[0]

print(Permisos)

# %%
### VEr el shape directamente para saber cantidad de filas y columnas
Permisos.shape

# %%
# Ordenar el DataFrame por Padron (ascendente), anio, mes, area en orden descendente me quedo con el ùltimo permiso aprobado para ese padron y el area màs grande de esa fecha.
Permisos_ordenado = Permisos.sort_values(by=['pad','anio', 'mes', 'area'], ascending=[True,False, False, False])

# Mostrar el DataFrame ordenado
Permisos_ordenado.head(15)


# %%
# Primero, eliminamos duplicados por padròn para quedarnos con el ùtimo registro en año para ese padròn.

p_sin_duplicados = Permisos_ordenado.drop_duplicates(subset=['pad','anio','mes'])

p_sin_duplicados.head(15)

# %%
# Contar cuántos registros hay por 'anio' y 'mes'
resultado = p_sin_duplicados.groupby(['anio', 'mes']).size().reset_index(name ='conteo_destino')


# Mostrar el resultado
print(resultado)

# %%
# Contar la cantidad de registros por año
p_conteo_por_anio = p_sin_duplicados.groupby('anio').size().reset_index(name='cantidad_registros')

print(p_conteo_por_anio)

# %%
# Supongamos que 'resultado' es tu DataFrame que contiene los conteos
# Calcular la suma total de 'conteo_destino'
suma_conteo_destino = resultado['conteo_destino'].sum()

# Mostrar la suma total
print(f"Suma total de conteo_destino: {suma_conteo_destino}")

# %%
# Machear los DataFrames usando un left join
cat_per = pd.merge(filtro_dep, Permisos, on=['anio','mes','pad'], how='left')

# Machear los DataFrames usando un left join
per_cat = pd.merge(p_sin_duplicados,filtro_dep, on=['anio','mes','pad'], how='left')





# %%
#Mostrar el primer Dataframe resultante
cat_per.head()

# %%
#Mostrar cantidad de filas y columnas del primer Dataframe resultante
cat_per.shape

# %%
#Mosstrar el segundo Dataframe resultante
per_cat.head()

# %%
per_cat.shape

# %%
# Guardar el DataFrame macheado como CSV de catastro
cat_per.to_csv('C:/Users/macar/Desktop/python-para-ciencia-de-datos/DatosAbiertosDNC(2024-09)/cat_per.csv', index=False)

# %%
# Guardar el DataFrame macheado como CSV de permisos
per_cat.to_csv('C:/Users/macar/Desktop/python-para-ciencia-de-datos/DatosAbiertosDNC(2024-09)/per_cat.csv', index=False)

# %%
conteo_codreg = per_cat.groupby('cod_reg').size().reset_index(name='cantidad_expedientes')

conteo_codreg

st.title('ANÁLISIS DE CATASTRO Y PERMISOS DE OBRA DE LA IMM')

