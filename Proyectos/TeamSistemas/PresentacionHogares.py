import streamlit as st
#import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium



st.image("data/ine.jpg", caption="", use_column_width=True)

st.title('PRESENTACION DE DATOS DE LA ENCUESTA CONTINUA DE HOGARES (ECH)')
st.header('CORRESPODIENTE A ENERO DEL 2024')

#leo el csv
ECH_Seg_12024 = pd.read_csv('data/ECH_Seguimiento_Mes_1_2024.csv')

#cargo las opciones de taps
tabs = st.tabs(["Inicio", "Tabla", "Graficos", "Mapas"])

st.sidebar.title('Filtros')

###FILTROS

# Selectbox para elegir el departamento
option_depto = st.sidebar.selectbox("Seleccione el Departamento:", ['Todos'] + ECH_Seg_12024["nom_dpto"].unique().tolist())

# Selectbox para elegir el localidad segun el departamento
if option_depto == 'Todos':
    option_localidad= st.sidebar.selectbox("Seleccione la Localidad:", ['Todos'] + ECH_Seg_12024["NOM_LOC_AGR_13"].unique().tolist())
else:    
    option_localidad= st.sidebar.selectbox("Seleccione la Localidad:", ['Todos'] + ECH_Seg_12024[ECH_Seg_12024['nom_dpto'] == option_depto]["NOM_LOC_AGR_13"].unique().tolist())

#seleccion de sexo
sexo = ['Todos','Hombre', 'Mujer']
option_sexo = st.sidebar.selectbox("Seleccione el sexo:", sexo)

# Selectbox rango de edad
rango = ['Todos','0-18', '19-30', '31-40', '41-50', '51-60', '61-100', '>100']
option_rango = st.sidebar.selectbox("Seleccione rango de edad:", rango)

##Aplico los filtros###########################################
if ((option_depto != 'Todos') and (option_localidad != 'Todos')):

        if option_rango == 'Todos':
            if option_sexo == 'Hombre':                    
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 1)]
                 
            elif option_sexo == 'Mujer':    
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 2)]
                
            else:   
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad)]
                
    
        elif option_rango == '0-18':
            if option_sexo == 'Hombre':                    
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] < 19)]
                
            elif option_sexo == 'Mujer':   
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] < 19)]
                
            else:   
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e27'] < 19)]
                  
        
        elif option_rango == '19-30': 
            if option_sexo == 'Hombre':                    
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 18) & (ECH_Seg_12024['e27'] < 31)]
                
            elif option_sexo == 'Mujer':   
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 18) & (ECH_Seg_12024['e27'] < 31)]
                
            else:
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e27'] > 18) & (ECH_Seg_12024['e27'] < 31)]
                

        elif option_rango == '31-40': 
            if option_sexo == 'Hombre': 
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 30) & (ECH_Seg_12024['e27'] < 41)]
                  
            elif option_sexo == 'Mujer':    
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 30) & (ECH_Seg_12024['e27'] < 41)]
                
            else: 
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e27'] > 30) & (ECH_Seg_12024['e27'] < 41)]
                 

        elif option_rango == '41-50':
            if option_sexo == 'Hombre': 
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 40) & (ECH_Seg_12024['e27'] < 51)]
                 
            elif option_sexo == 'Mujer':    
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 40) & (ECH_Seg_12024['e27'] < 51)]
                
            else:  
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e27'] > 40) & (ECH_Seg_12024['e27'] < 51)]
                  

        elif option_rango == '51-60': 
            if option_sexo == 'Hombre': 
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 50) & (ECH_Seg_12024['e27'] < 61)]
                 
            elif option_sexo == 'Mujer':    
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 50) & (ECH_Seg_12024['e27'] < 61)]
                
            else:   
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e27'] > 50) & (ECH_Seg_12024['e27'] < 61)]
                 

        elif option_rango == '61-100': 
            if option_sexo == 'Hombre': 
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 60) & (ECH_Seg_12024['e27'] < 101)]
                 
            elif option_sexo == 'Mujer':   
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 60) & (ECH_Seg_12024['e27'] < 101)]
                
            else:  
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e27'] > 60) & (ECH_Seg_12024['e27'] < 101)]
                  

        else:                    
            if option_sexo == 'Hombre': 
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 100)]
                 
            elif option_sexo == 'Mujer':    
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 100)]
                
            else: 
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['NOM_LOC_AGR_13'] == option_localidad) & 
                                            (ECH_Seg_12024['e27'] > 100)]
                 
##localidad todos################################################################################################33
elif ((option_depto != 'Todos') and (option_localidad == 'Todos')):
            if option_rango == 'Todos':
                if option_sexo == 'Hombre':                    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 1)]
                     
                elif option_sexo == 'Mujer':    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 2)]
                    
                else:   
                    df_filtrado = (ECH_Seg_12024[ECH_Seg_12024['nom_dpto'] == option_depto]) 
                    
    
            elif option_rango == '0-18':
                if option_sexo == 'Hombre':                    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] < 19)]
                    
                elif option_sexo == 'Mujer':   
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] < 19)]
                    
                else:   
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e27'] < 19)]
                       
            
            elif option_rango == '19-30': 
                if option_sexo == 'Hombre':                    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 18) & (ECH_Seg_12024['e27'] < 31)]
                     
                elif option_sexo == 'Mujer':   
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 18) & (ECH_Seg_12024['e27'] < 31)]
                    
                else:
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e27'] > 18) & (ECH_Seg_12024['e27'] < 31)]
                    

            elif option_rango == '31-40': 
                if option_sexo == 'Hombre': 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 30) & (ECH_Seg_12024['e27'] < 41)]
                     
                elif option_sexo == 'Mujer':    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 30) & (ECH_Seg_12024['e27'] < 41)]
                    
                else: 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e27'] > 30) & (ECH_Seg_12024['e27'] < 41)]
                       

            elif option_rango == '41-50':
                if option_sexo == 'Hombre': 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 40) & (ECH_Seg_12024['e27'] < 51)]
                      
                elif option_sexo == 'Mujer':    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 40) & (ECH_Seg_12024['e27'] < 51)]
                    
                else:  
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e27'] > 40) & (ECH_Seg_12024['e27'] < 51)]
                     

            elif option_rango == '51-60': 
                if option_sexo == 'Hombre': 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 50) & (ECH_Seg_12024['e27'] < 61)]
                     
                elif option_sexo == 'Mujer':    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 50) & (ECH_Seg_12024['e27'] < 61)]
                    
                else:   
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e27'] > 50) & (ECH_Seg_12024['e27'] < 61)]
                     

            elif option_rango == '61-100': 
                if option_sexo == 'Hombre': 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 60) & (ECH_Seg_12024['e27'] < 101)]
                      
                elif option_sexo == 'Mujer':   
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 60) & (ECH_Seg_12024['e27'] < 101)]
                    
                else:  
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e27'] > 60) & (ECH_Seg_12024['e27'] < 101)]
                     

            else:                    
                if option_sexo == 'Hombre': 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 100)]
                     
                elif option_sexo == 'Mujer':    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 100)]
                    
                else: 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['nom_dpto'] == option_depto) & (ECH_Seg_12024['e27'] > 100)]
                     
##################################################################################################################            
else:            
            if option_rango == 'Todos':
                if option_sexo == 'Hombre':                    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 1)]
                      
                elif option_sexo == 'Mujer':    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 2)]
                    
                else: 
                    df_filtrado = ECH_Seg_12024
                    
        
            elif option_rango == '0-18':
                if option_sexo == 'Hombre':                    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] < 19)]
                     
                elif option_sexo == 'Mujer':   
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] < 19)]
                    
                else:   
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e27'] < 19)]
                       
            
            elif option_rango == '19-30': 
                if option_sexo == 'Hombre':                    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 18) & (ECH_Seg_12024['e27'] < 31)]
                      
                elif option_sexo == 'Mujer':   
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 18) & (ECH_Seg_12024['e27'] < 31)]
                    
                else:
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e27'] > 18) & (ECH_Seg_12024['e27'] < 31)]
                     

            elif option_rango == '31-40': 
                if option_sexo == 'Hombre': 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 30) & (ECH_Seg_12024['e27'] < 41)]
                      
                elif option_sexo == 'Mujer':    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 30) & (ECH_Seg_12024['e27'] < 41)]
                    
                else: 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e27'] > 30) & (ECH_Seg_12024['e27'] < 41)]
                       

            elif option_rango == '41-50':
                if option_sexo == 'Hombre': 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 40) & (ECH_Seg_12024['e27'] < 51)]
                     
                elif option_sexo == 'Mujer':    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 40) & (ECH_Seg_12024['e27'] < 51)]
                    
                else:  
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e27'] > 40) & (ECH_Seg_12024['e27'] < 51)]
                      

            elif option_rango == '51-60': 
                if option_sexo == 'Hombre': 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 50) & (ECH_Seg_12024['e27'] < 61)]
                     
                elif option_sexo == 'Mujer':    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 50) & (ECH_Seg_12024['e27'] < 61)]
                    st.write(df_filtrado)
                else:   
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e27'] > 50) & (ECH_Seg_12024['e27'] < 61)]
                    

            elif option_rango == '61-100': 
                if option_sexo == 'Hombre': 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 60) & (ECH_Seg_12024['e27'] < 101)]
                     
                elif option_sexo == 'Mujer':   
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 60) & (ECH_Seg_12024['e27'] < 101)]
                    
                else:  
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e27'] > 60) & (ECH_Seg_12024['e27'] < 101)]
                     

            else:                    
                if option_sexo == 'Hombre': 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 1) & (ECH_Seg_12024['e27'] > 100)]
                     
                elif option_sexo == 'Mujer':    
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e26'] == 2) & (ECH_Seg_12024['e27'] > 100)]
                   
                else: 
                    df_filtrado = ECH_Seg_12024[(ECH_Seg_12024['e27'] > 100)]

# Contenido de la pestaña "Inicio"
with tabs[0]: 
    st.subheader('Información de las series')
    st.write('La Encuesta Continua de Hogares (ECH) es una encuesta multipropósito que el Instituto Nacional de Estadisitica realiza, sin interrupciones y durante todo el año, desde el año 1968.')
    st.write('Su origen, al igual que muchas encuestas a hogares de los países americanos, lo constituye el " Modelo Atlántida" diseñado por el Bureau of Census de Estados Unidos de América.')
    st.write('Hasta 1979 su alcance geográfico permantente fue el departamento de Montevideo. En 1980, a través de un convenio con el Programa de las Naciones Unidas para el Desarrollo y el Fondo de las Naciones Unidad para Actividades de Población se extendió la muestra a todo el país y se introdujeron pequeñas modificaciones estructurales en el cuestionario que se siguió aplicando hasta 1989.')
    st.write('En 1981 la encuesta, por primera y única vez y en el marco de un proyecto del Fondo de las Naciones Unidas para Actividades de Población, se investigó el área rural, situación que recién se volvió a repetir con la Encuesta Nacional de Hogares Ampliada de 2006.')

    st.subheader('Resumen')
    st.write('La Encuesta Continua de Hogares 2024 tiene como objetivos:')
    st.write('  - Estimar las tasas de actividad, de empleo y desempleo de la población')
    st.write('  - Estimar el ingreso de los hogares y de las personas')

    st.subheader('Unidad de análisis')
    st.write('La encuesta va dirigida a la población que reside en viviendas particulares y que integra hogares particulares, por lo que quedan excluidos tanto las viviendas como los hogares colectivos (hoteles, conventos, cuarteles, hospitales). No obstante lo establecido anteriormente, se incluyen los hogares, que formando un grupo independiente, residen en estos establecimientos, como puede ser el caso de los encargados, caseros, porteros,etc.')
# Contenido de la pestaña "Datos"
with tabs[1]:    
    st.subheader(f'Información filtrada para {option_depto} y {option_localidad}')    
    st.write(df_filtrado)   

with tabs[2]:
    
    # Generar datos aleatorios
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Crear un gráfico de Matplotlib
    plt.plot(x, y)
    plt.title("Gráfico de Seno")

    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)     
   
with tabs[3]:
    if option_depto == 'Todos':
        st.subheader("Seleccione un Departamento para ver su mapa...")
    else:   

        if option_depto =='Artigas':    
            st.subheader("Departamento de Artigas")

             # Crear el mapa base
    #m = folium.Map(location=[-33.45, -70.65], zoom_start=4)  # Ubicación genérica

    # cargo los mapas
    #region_sales_data = ECH_Seg_12024[(ECH_Seg_12024["nom_dpto"].unique())]
    
    #for idx, option_depto in region_sales_data.iterrows():
     #   folium.Marker(
      #      location=[-33.45 + idx * 0.1, -70.65 + idx * 0.1],  # Simular diferentes posiciones
       #     popup= option_depto,
       
        #).add_to(m)

    # Renderizar el mapa en Streamlit
    #st_folium (m, width=700, height=500)



            #st.image("data/artigas.jpg",use_column_width=True)        
    
        elif option_depto == 'Canelones':  
            st.subheader("Departamento de Canelones:")
            st.image("data/canelones.jfif",use_column_width=True)
        
        elif option_depto == 'Cerro Largo':   
            st.subheader("Departamento de Cerro Largo")
            st.image("data/cerroLargo.jfif",use_column_width=True)

        elif option_depto == 'Colonia':   
            st.subheader("Departamento de Colonia")
            st.image("data/colonia.jfif",use_column_width=True)   

        elif option_depto == 'Durazno':   
            st.subheader("Departamento de Durazno")
            st.image("data/durazno.jfif",use_column_width=True) 

        elif option_depto == 'Flores':   
            st.subheader("Departamento de Flores")
            st.image("data/flores.jfif",use_column_width=True)   

        elif option_depto == 'Florida':   
            st.subheader("Departamento de Florida")
            st.image("data/florida.jfif",use_column_width=True)    

        elif option_depto == 'Lavalleja':   
            st.subheader("Departamento de Lavalleja")
            st.image("data/lavalleja.jfif",use_column_width=True)   

        elif option_depto == 'Maldonado':   
            st.subheader("Departamento de Maldonado")
            st.image("data/maldonado.jfif",use_column_width=True)   

        elif option_depto == 'Montevideo':   
            st.subheader("Departamento de Montevideo")
            st.image("data/montevideo.jfif",use_column_width=True)  

        elif option_depto == 'Paysandú':   
            st.subheader("Departamento de Paysandú")
            st.image("data/paysandu.jfif",use_column_width=True)    

        elif option_depto == 'Río Negro':   
            st.subheader("Departamento de Río Negro")
            st.image("data/rioNegro.jfif",use_column_width=True)   

        elif option_depto == 'Rivera':   
            st.subheader("Departamento de Rivera")
            st.image("data/rivera.jfif",use_column_width=True)   

        elif option_depto == 'Rocha':   
            st.subheader("Departamento de Rocha")
            st.image("data/rocha.jfif",use_column_width=True) 

        elif option_depto == 'Salto':   
            st.subheader("Departamento de Salto")
            st.image("data/salto.jfif",use_column_width=True)    

        elif option_depto == 'San José':   
            st.subheader("Departamento de San José")
            st.image("data/sanJose.jfif",use_column_width=True) 

        elif option_depto == 'Soriano':   
            st.subheader("Departamento de Soriano")
            st.image("data/soriano.jfif",use_column_width=True)  

        elif option_depto == 'Tacuarembó':   
            st.subheader("Departamento de Tacuarembó")
            st.image("data/tacuarembo.jfif",use_column_width=True)                                     

        else:   
            st.subheader("Departamento de Treinta y Tres")
            st.image("data/treintaytres.jfif",use_column_width=True)   


   
 # Crear pestaña única
tab = st.tab("Visualización")

# Barra lateral de filtros
st.sidebar.title('Filtros')

# Selectbox para elegir el departamento
option_depto = st.sidebar.selectbox("Seleccione el Departamento:", ['Todos'] + ECH_Seg_12024["nom_dpto"].unique().tolist())

# Selectbox para elegir la localidad según el departamento
if option_depto == 'Todos':
    option_localidad = st.sidebar.selectbox("Seleccione la Localidad:", ['Todos'] + ECH_Seg_12024["NOM_LOC_AGR_13"].unique().tolist())
else:
    option_localidad = st.sidebar.selectbox("Seleccione la Localidad:", ['Todos'] + ECH_Seg_12024[ECH_Seg_12024['nom_dpto'] == option_depto]["NOM_LOC_AGR_13"].unique().tolist())

# Filtramos los datos por departamento y localidad
if option_depto == 'Todos':
    region_sales_data = ECH_Seg_12024
else:
    region_sales_data = ECH_Seg_12024[ECH_Seg_12024['nom_dpto'] == option_depto]

if option_localidad != 'Todos':
    region_sales_data = region_sales_data[region_sales_data['NOM_LOC_AGR_13'] == option_localidad]

# Contenido del tab único
with tab[4]:
    st.subheader(f'Información filtrada para {option_depto} y {option_localidad}')

    # Mostrar la tabla con los datos filtrados
    st.write(region_sales_data)

    # Gráfico de barras: Distribución por sexo
    st.subheader('Gráfico de barras - Distribución por Sexo')
    
    sex_counts = region_sales_data['e26'].value_counts()
    plt.figure(figsize=(6, 4))
    plt.bar(['Hombres', 'Mujeres'], sex_counts)
    plt.title('Distribución por Sexo')
    plt.ylabel('Cantidad de personas')

    # Mostrar el gráfico de barras en Streamlit
    st.pyplot(plt)

    # Mapa interactivo usando folium
    st.subheader(f'Mapa del departamento: {option_depto}')
    
    if 'latitud' in region_sales_data.columns and 'longitud' in region_sales_data.columns:
        # Crear el mapa base centrado en Uruguay
        m = folium.Map(location=[-33.0, -56.0], zoom_start=6)

        # Agregar marcadores para cada fila en el dataset filtrado
        for idx, row in region_sales_data.iterrows():
            folium.Marker(
                location=[row['latitud'], row['longitud']],
                popup=f"{row['NOM_LOC_AGR_13']}, {row['nom_dpto']}",
                tooltip=f"{row['NOM_LOC_AGR_13']}, {row['nom_dpto']}"
            ).add_to(m)

        # Mostrar el mapa en Streamlit
        st_folium(m, width=700, height=500)
    else:
        st.write("No hay datos de coordenadas disponibles para mostrar el mapa.")