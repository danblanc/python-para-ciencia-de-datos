import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import plotly.express as px


ECH2023 = pd.read_csv('Data/ECH_implantacion_2023.csv')
uruguay_map = gpd.read_file('Data/ine_depto.shp') 

# armado de tablas

tabla_porcentaje = ECH2023['e557'].value_counts(normalize=True).reset_index(name='Porcentaje') * 100
tabla_porcentaje = pd.DataFrame(tabla_porcentaje)

#agrego columna con los valores de la variable
tabla_porcentaje['e557'] = [2,1,3]
# creo columnas categoría y filtro
tabla_porcentaje['Categoría'] = 'Total'
tabla_porcentaje['Filtro'] = 'Total'
# ahora hago frecuencia de esta variable pero por sexo
tabla_sexo = ECH2023.groupby('e26')['e557'].value_counts(normalize=True).reset_index(name='Porcentaje')
tabla_sexo['Porcentaje'] *= 100
# modifico las categorías de la variable sexo (e26)
tabla_sexo['e26'] = tabla_sexo['e26'].map({1: 'Hombre', 2: 'Mujer'})
tabla_sexo.rename(columns={'e26': 'Categoría'}, inplace=True)
# agrego una variable filtro
tabla_sexo['Filtro'] = 'Sexo'
#concateno las tablas
tabla_junta_e557 = pd.concat([tabla_porcentaje, tabla_sexo], axis=0)
#Creo una variable de tramos de edad
bins = [0, 13, 17, 40 ,64, 110]
labels = ['[0 a 13]', '[14 a 17]', '[18 a 40]','[41 a 64]' ,'[65 o más]']

ECH2023['tramo_edad'] = pd.cut(ECH2023['e27'], bins=bins, labels=labels, right=True)

# ahora hago frecuencia de esta variable pero por tramos de edad
tabla_edad = ECH2023.groupby('tramo_edad')['e557'].value_counts(normalize=True).reset_index(name='Porcentaje')
tabla_edad['Porcentaje'] *= 100
tabla_edad.rename(columns={'tramo_edad': 'Categoría'}, inplace=True)
tabla_edad['Filtro'] = 'Tramo etario'

#concateno a la tabla principal
tabla_junta_e557 = pd.concat([tabla_junta_e557, tabla_edad], axis=0)
#creo variable mdeo_int a partir de la variable dpto
ECH2023['mdeo_int'] = np.where(ECH2023['dpto'] == 1, 'Montevideo', 'Interior')

# calculo frecuencia de la variable pero por region
tabla_region = ECH2023.groupby('mdeo_int')['e557'].value_counts(normalize=True).reset_index(name='Porcentaje')
tabla_region['Porcentaje'] *= 100
tabla_region.rename(columns={'mdeo_int': 'Categoría'}, inplace=True)
tabla_region['Filtro'] = 'Región'

#concateno a la tabla principal
tabla_junta_e557 = pd.concat([tabla_junta_e557, tabla_region], axis=0)

# creo la variable descripción a partir de la e557
tabla_junta_e557['Descripción'] = tabla_junta_e557['e557'].apply(lambda x: 'Sí, es la misma persona' if x == 1 else ('No, responde un miembro de este hogar' if x == 2 else ('No, responde un miembro calificado de otro hogar' if x == 3 else 99)))

#redondeo la variable porcentaje
tabla_junta_e557['Porcentaje'] = tabla_junta_e557['Porcentaje'].round(1)

# Finalmente restablezco el índice del DataFrame concatenado
tabla_junta_e557 = tabla_junta_e557.reset_index(drop=True)

##########################################################################
# PESTAÑA 2
df_selected = ECH2023[['nom_dpto', 'ESTRED13', 'c6_1', 'e38', 'e46_cv', 'e582', 'f75', 'f285', 'f288', 'f99', 'f101', 'f102', 'f299', 'f110', 'f116', 'g132', 'g140', 'h161', 'e557']]

# juntamos las categorias 2 y 3 de la variable e557, para diferenciar entre los que responden por si mismos y los que no
df_selected['Informante'] = df_selected['e557'].apply(lambda x: 1 if x == 1 else 2)
# 1 si informa por si mismo
# 2 si informa otra persona

#########################################################################
#PESTAÑA 3
codigos_interes = [9700, 8610, 4100, 141, 4711]

# Filtrar las filas donde f72_2 coincide con los códigos de interés
df_ocupacion_filtrada = ECH2023[ECH2023['f72_2'].isin(codigos_interes)]
df_ocupacion_filtrada['Informante'] = df_ocupacion_filtrada['e557'].apply(lambda x: 1 if x == 1 else 2)

df_ocupacion_filtrada['NIVEDURR'] = df_ocupacion_filtrada.apply(lambda x: (
    "9. TERCIARIA COMP" if x['e215_1'] == 1 or x['e218_1'] == 1 or x['e221_1'] == 1 or x['e224_1'] == 1 else
    "8. TERCIARIA INCOMP" if (x['e51_8'] + x['e51_9'] + x['e51_10']) > 0 else
    "7. EMS COMP" if x['e201_1c'] == 1 or x['e201_1d'] == 1 else
    "6. EMS INCOMP" if (x['e51_5'] + x['e51_6']) > 0 else
    "5. EM CICLO BASICO COMP" if x['e201_1a'] == 1 or x['e201_1b'] == 1 else
    "4. EM CICLO BASICO INCOMP" if (x['e51_4_a'] + x['e51_4_b']) > 0 else
    "3. PRIMARIA COMP" if x['e197_1'] == 1 else
    "2. PRIMARIA INCOMP" if (x['e51_2'] + x['e51_3']) > 0 else
    "0. SIN INSTRUCCION" if x['e49'] == 2 else None
), axis=1)

# Crear la variable 'NIVEDU2021'
df_ocupacion_filtrada['NIVEDU2021'] = df_ocupacion_filtrada['NIVEDURR'].apply(lambda x: (
    "0. S/INSTRUCCIÓN Y PRIM. INC" if x in ["0. SIN INSTRUCCION", "1. PRESCOLAR", "2. PRIMARIA INCOMP"] else
    "1. PRIMARIA COMPLETA O CB INCOMPLETO" if x in ["3. PRIMARIA COMP", "4. EM CICLO BASICO INCOMP"] else
    "2. CB COMPLETO O EMS INCOMP" if x in ["5. EM CICLO BASICO COMP", "6. EMS INCOMP"] else
    "3. SEC. COMPLETA O TERCIARIA INCOMP" if x in ["7. EMS COMP", "8. TERCIARIA INCOMP"] else
    "4. TERCIARIO COMPLETO O POSGRADO" if x == "9. TERCIARIA COMP" else None
))

# Crear la variable 'NIVEDU2021_2'
df_ocupacion_filtrada['NIVEDU2021_2'] = df_ocupacion_filtrada['NIVEDU2021'].apply(lambda x: (
    "1. CB INCOMPLETO O MENOS" if x in ["0. S/INSTRUCCIÓN Y PRIM. INC", "1. PRIMARIA COMPLETA O CB INCOMPLETO"] else
    "2. CB COMPLETO O EMS INCOMP" if x == "2. CB COMPLETO O EMS INCOMP" else
    "3. SEC. COMPLETA O TERCIARIA INCOMP" if x == "3. SEC. COMPLETA O TERCIARIA INCOMP" else
    "4. TERCIARIO COMPLETO O POSGRADO" if x == "4. TERCIARIO COMPLETO O POSGRADO" else None
))

#creo variable horas efectivas
df_ocupacion_filtrada['Horas_efectivas'] = df_ocupacion_filtrada['f284_1']+df_ocupacion_filtrada['f284_2']+df_ocupacion_filtrada['f284_3']+df_ocupacion_filtrada['f284_4']+df_ocupacion_filtrada['f284_5']+df_ocupacion_filtrada['f284_6']+df_ocupacion_filtrada['f284_7']

tabla_estadisticas_h = (
    df_ocupacion_filtrada.groupby(['Informante','f72_2', 'NIVEDU2021_2', 'e26'])
    .agg(
        media_horas=('Horas_efectivas', 'mean'),
        media_ingreso=('PT2', 'mean')
    )
    .reset_index()
)

# Redondear las estadísticas a 1 decimal
tabla_estadisticas_h[['media_horas', 'media_ingreso']] = tabla_estadisticas_h[['media_horas', 'media_ingreso']].round(1)

# Ordenar por la columna 'Frecuencia' en orden descendente
tabla_estadisticas_h = tabla_estadisticas_h.sort_values(by='f72_2', ascending=False).reset_index(drop=True)

tabla_estadisticas_h['e26'] = tabla_estadisticas_h['e26'].apply(lambda x: '1- Hombre' if x == 1 else '2- Mujer')

# Modificar los valores de la variable rama
mapeo_ciu = { 8610: 'Act. Hospitales', 141: 'Cría de ganado vacuno', 4711: 'Comercio minorista', 9700: 'Act. Hogares', 4100: 'Construcción' } 
# Aplicar el mapeo a la columna 
tabla_estadisticas_h['f72_2'] = tabla_estadisticas_h['f72_2'].map(mapeo_ciu) 
##########################################################################

tab1, tab2, tab3 = st.tabs(["Caracterización del informante", "Camino mínimo", "Ingresos y horas efectivas"])

tabla_grafico1 = tabla_junta_e557.copy()

tabla_grafico2 = df_selected.copy()

tabla_grafico3 = tabla_estadisticas_h.copy()

#creo el filtro para el grafico 1 en la primera pestaña
with tab1:
    filtro_grafico1 = st.selectbox('Selecciona variable de corte:', tabla_junta_e557['Filtro'].unique())

    # Verificar si 'filtro_grafico1' es un string y convertirlo en lista si es necesario
    if isinstance(filtro_grafico1, str):
        filtro_grafico1 = [filtro_grafico1]

    if filtro_grafico1:
        tabla_grafico1 = tabla_grafico1[tabla_grafico1['Filtro'].isin(filtro_grafico1)]

    st.header("Caracterización del informante de la ECH 2023")
    fig1 = px.bar(tabla_grafico1, x='e557', y='Porcentaje', color='Categoría', title='Distribucón de la variable e557', barmode='group')
    st.plotly_chart(fig1)
    st.write("Categorías de e557: 1- Responde la misma persona; 2- Responde otro miembro del hogar; 3- Responde un informante calificado de otro hogar")

#creo el filtro para el grafico 2 en la segunda pestaña
with tab2:
    filtro_grafico2 = st.selectbox('Selecciona informante:', df_selected['Informante'].unique())
    st.write("Categorías de informante: 1- Responde la misma persona; 2- Responde otro miembro del hogar o un informante calificado de otro hogar")
    st.header("Puntaje de recorrido mínimo por departamento y estrato")
    # Verificar si 'filtro_grafico2' es un string y convertirlo en lista si es necesario
    if isinstance(filtro_grafico2, str):
        filtro_grafico2 = [filtro_grafico2]

    if filtro_grafico2:
        tabla_grafico2 = tabla_grafico2[tabla_grafico2['Informante'] == filtro_grafico2]
        tabla_grafico2['low_score'] = ((tabla_grafico2['c6_1'] == 1) & (tabla_grafico2['e38'] == 1)).astype(int)

        # Puntuación media: Observaciones que cumplen con más condiciones
        tabla_grafico2['medium_score'] = ((tabla_grafico2['e46_cv'] == 2) | (tabla_grafico2['e582'] == 2) | (tabla_grafico2['f75'] == 1)).astype(int)

        # Puntuación alta: Observaciones que cumplen con la mayoría de las condiciones
        tabla_grafico2['high_score'] = (
        (tabla_grafico2['f285'] == 2) | (tabla_grafico2['f288'].isin([2, 3])) | (tabla_grafico2['f99'] == 2) |
        (tabla_grafico2['f101'].isin([2, 3, 4])) | (tabla_grafico2['f102'] == 2) | (tabla_grafico2['f299'] == 2) |
        (tabla_grafico2['f110'] == 7) | (tabla_grafico2['f116'] == 2) | (tabla_grafico2['g132'] == 3) |
        (tabla_grafico2['g140'] == 3) | (tabla_grafico2['h161'] == 2)
        ).astype(int)

        # combino puntajes en un indicador gradual
        tabla_grafico2['gradual_indicator'] = tabla_grafico2['low_score'] + tabla_grafico2['medium_score'] + tabla_grafico2['high_score']

        # Agrego puntajes por departamento y estrato
        df_grouped = tabla_grafico2.groupby(['nom_dpto', 'ESTRED13']).agg(
        total_score=('gradual_indicator', 'sum'),  
        count=('gradual_indicator', 'size')  
        ).reset_index()

        # Normalizar la Puntuación a un Rango de 0 a 1
        max_score = df_grouped['total_score'].max()
        df_grouped['normalized_score'] = df_grouped['total_score'] / max_score  

        # Merge de datos y visualización de mapa
        df_grouped['nom_dpto'] = df_grouped['nom_dpto'].str.upper()
        uruguay_map['NOMBRE'] = uruguay_map['NOMBRE'].str.upper()

        merged_map = uruguay_map.merge(df_grouped, left_on='NOMBRE', right_on='nom_dpto', how='left')
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        merged_map.boundary.plot(ax=ax)  
        merged_map.plot(column='normalized_score', ax=ax, legend=True, cmap='Reds', missing_kwds={"color": "white"})
        plt.title('Puntaje de mínimo recorrido por departamento')
        st.pyplot(fig)
        # Gráfico Sunburst
        fig3 = px.sunburst(
                df_grouped,
                path=['nom_dpto', 'ESTRED13'],  
                values='normalized_score',  
                color='normalized_score',  
                color_continuous_scale='Reds',  
                title="Distribución por estrato y departamento del puntaje de riesgo por menor recorrido en la encuesta"
            )

            # Mejoro la visualización
        fig3.update_layout(
                margin=dict(t=50, l=25, r=25, b=25),  
                coloraxis_colorbar=dict(title="Score Normalizado")  
            )

            # Mostrar el gráfico Sunburst
        st.plotly_chart(fig3) 
         
        st.write("Se puntúan las encuestas según una selección de variables y valores que permiten acortar la realización de la ECH. Esta puntuación se clasifica en tres niveles: bajo, medio o alto. Posteriormente, se agrupa la información por departamento y se suman los puntajes, normalizándolos entre 0 y 1.")
with tab3:
    filtro_grafico3 = st.selectbox('Selecciona rama de ocupación:', tabla_estadisticas_h['f72_2'].unique())
    filtro_grafico4 = st.selectbox('Selecciona sexo:', tabla_estadisticas_h['e26'].unique())

    
    # 
    if not isinstance(filtro_grafico3, list):
        filtro_grafico3 = [filtro_grafico3]
    
    if not isinstance(filtro_grafico4, list):
        filtro_grafico4 = [filtro_grafico4]

    # Filtrar la tabla según los filtros seleccionados
    if filtro_grafico3:
        tabla_grafico3 = tabla_grafico3[tabla_grafico3['f72_2'].isin(filtro_grafico3)]

    if filtro_grafico4:
        tabla_grafico3 = tabla_grafico3[tabla_grafico3['e26'].isin(filtro_grafico4)]

    
    st.header("Media de ingresos y horas efectivas trabajadas por informante según rama de ocupación y sexo")
    fig4 = px.scatter(
        tabla_grafico3, 
        x='media_horas', 
        y='media_ingreso', 
        symbol='Informante', 
        color='NIVEDU2021_2', 
        title='Distribución de la variable e557'
    )
    
    # Modificar el tamaño de los puntos
    fig4.update_traces(marker=dict(sizemode='diameter', size=10, opacity=0.8, line=dict(width=2)))  
    st.plotly_chart(fig4)
    
    st.write("Categorías de informante: 1- Responde la misma persona; 2- Responde otro miembro del hogar o un informante calificado de otro hogar")