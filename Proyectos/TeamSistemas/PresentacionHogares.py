import streamlit as st
import seaborn as sns
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
    promedio_edad = ECH_Seg_12024.groupby('nom_dpto')['e27'].mean().reset_index()

    data = pd.DataFrame({
        'Departamentos': promedio_edad['nom_dpto'],
        'Edad': promedio_edad['e27']
    })   

    # Gráfico de promedio de edad
    fig_avg_price = px.line(data, x='Departamentos', y='Edad', title='Promedio de Edad por departamento')
    st.plotly_chart(fig_avg_price)
   
   
with tabs[3]:
    if option_depto == 'Todos':
        st.subheader("Seleccione un Departamento para ver su mapa...")
    else:   

        if option_depto =='Artigas':    
            st.subheader("Departamento de Artigas")

             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-30.4, -56.46667],  # Simular diferentes posiciones
                popup='Artigas, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)
                 
    
        elif option_depto == 'Canelones':  
            st.subheader("Departamento de Canelones:")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-34.52278, -56.27778],  # Simular diferentes posiciones
                popup='Canelones, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)
        
        elif option_depto == 'Cerro Largo':   
            st.subheader("Departamento de Cerro Largo")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-33.02940, -55.35351],  # Simular diferentes posiciones
                popup='Cerro Largo, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)

        elif option_depto == 'Colonia':   
            st.subheader("Departamento de Colonia")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-34.4626200, -57.8397600],  # Simular diferentes posiciones
                popup='Colonia, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500) 

        elif option_depto == 'Durazno':   
            st.subheader("Departamento de Durazno")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-33.38056, -56.52361],  # Simular diferentes posiciones
                popup='Durazno, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500) 

        elif option_depto == 'Flores':   
            st.subheader("Departamento de Flores")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-33.583333, -56.833333],  # Simular diferentes posiciones
                popup='Flores, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)   

        elif option_depto == 'Florida':   
            st.subheader("Departamento de Florida")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-34.09556, -56.21417],  # Simular diferentes posiciones
                popup='Florida, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)    

        elif option_depto == 'Lavalleja':   
            st.subheader("Departamento de Lavalleja")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-33.997196, -54.999224],  # Simular diferentes posiciones
                popup='Lavalleja, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)   

        elif option_depto == 'Maldonado':   
            st.subheader("Departamento de Maldonado")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-34.908716, -54.958272],  # Simular diferentes posiciones
                popup='Maldonado, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)  

        elif option_depto == 'Montevideo':   
            st.subheader("Departamento de Montevideo")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-34.90328, -56.18816],  # Simular diferentes posiciones
                popup='Montevideo, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)  

        elif option_depto == 'Paysandú':   
            st.subheader("Departamento de Paysandú")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-32.3171, -58.08072],  # Simular diferentes posiciones
                popup='Paysandú, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)   

        elif option_depto == 'Río Negro':   
            st.subheader("Departamento de Río Negro")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-32.725742, -57.387578],  # Simular diferentes posiciones
                popup='Río Negro, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)

        elif option_depto == 'Rivera':   
            st.subheader("Departamento de Rivera")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-30.90534, -55.55076],  # Simular diferentes posiciones
                popup='Rivera, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500) 

        elif option_depto == 'Rocha':   
            st.subheader("Departamento de Rocha")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-34, -54],  # Simular diferentes posiciones
                popup='Rocha, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)

        elif option_depto == 'Salto':   
            st.subheader("Departamento de Salto")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-31.38333, -57.96667],  # Simular diferentes posiciones
                popup='Salto, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)   

        elif option_depto == 'San José':   
            st.subheader("Departamento de San José")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-34.455, -56.616944],  # Simular diferentes posiciones
                popup='San José, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)

        elif option_depto == 'Soriano':   
            st.subheader("Departamento de Soriano")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-33.492127, -57.78931],  # Simular diferentes posiciones
                popup='Soriano, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)

        elif option_depto == 'Tacuarembó':   
            st.subheader("Departamento de Tacuarembó")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-31.71694, -55.98111],  # Simular diferentes posiciones
                popup='Tacuarembó, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)                                     

        else:   
            st.subheader("Departamento de Treinta y Tres")
             # Crear el mapa base  
            m = folium.Map(location=[-32.522779, -55.765835], zoom_start=6)  # Ubicación genérica

            # cargo los mapas
            folium.Marker(
                location=[-33, -54.25],  # Simular diferentes posiciones
                popup='Treinta y Tres, Uruguay',
                icon=folium.Icon(color='blue')
        
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium (m, width=700, height=500)  
   
