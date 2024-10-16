import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
import altair as alt
import plotly.graph_objects as go
import matplotlib.cm as cm
import matplotlib.ticker as mtick
import matplotlib.colorbar as cbar
import matplotlib.colors as mcolors


# Cargar la imagen
st.image("data/ine.jpg", caption="", width=400)

st.title('PRESENTACION DE DATOS DE LA ENCUESTA CONTINUA DE HOGARES (ECH)')
st.header('CORRESPONDIENTE A ENERO DEL 2024')

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
    option_localidad = st.sidebar.selectbox("Seleccione la Localidad:", ['Todos'] + ECH_Seg_12024["NOM_LOC_AGR_13"].unique().tolist())
else:    
    option_localidad = st.sidebar.selectbox("Seleccione la Localidad:", ['Todos'] + ECH_Seg_12024[ECH_Seg_12024['nom_dpto'] == option_depto]["NOM_LOC_AGR_13"].unique().tolist())

#seleccion de sexo
sexo = ['Todos','Hombre', 'Mujer']
option_sexo = st.sidebar.selectbox("Seleccione el sexo:", ['Todos', 'Hombre', 'Mujer'])



# Selectbox rango de edad
rango = ['Todos','0-18', '19-30', '31-40', '41-50', '51-60', '61-100', '>100']
option_rango = st.sidebar.selectbox("Seleccione rango de edad:", rango)
# Control deslizante para seleccionar un rango de edad

if 'e27' in ECH_Seg_12024.columns:
    edad_min, edad_max = int(ECH_Seg_12024['e27'].min()), int(ECH_Seg_12024['e27'].max())
    rango_edad = st.sidebar.slider("Seleccione el rango de edad:", min_value=edad_min, max_value=edad_max, value=(edad_min, edad_max))
else:
    st.sidebar.write("No se encontró la columna de edades ('e27') en los datos.")




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


# Contenido de la pestaña "Tabla"
with tabs[1]:
    st.subheader(f'Información filtrada para {option_depto} y {option_localidad}')
    st.write(df_filtrado)

# Contenido de la pestaña "Graficos"
with tabs[2]:

      # Crear subtabs dentro de Tab 1
    st.subheader("GRÁFICOS Y ANÁLISIS DE LOS DATOS")
    subtab = st.radio("", 
                      ["2.1 - Promedio de Edad para todos los departamentos", 
                       "2.2 - Promedio de Edad por departamentos",
                       "2.3 - Nivel Educativo", 
                       "2.4 - Distribución de ascendencia", 
                       "2.5 - Composición de los hogares", 
                       "2.6 - Todos los gráficos"])

    if subtab == "2.1 - Promedio de Edad para todos los departamentos":
        # Gráfico de promedio de edad
        promedio_edad = ECH_Seg_12024.groupby('nom_dpto')['e27'].mean().reset_index()

        data = pd.DataFrame({
            'Departamentos': promedio_edad['nom_dpto'],
            'Edad': promedio_edad['e27']
        })

        fig_avg_price = px.line(data, x='Departamentos', y='Edad', title='Promedio de Edad para todos los departamento')
        st.plotly_chart(fig_avg_price)

    elif subtab == "2.2 - Promedio de Edad por departamentos":

            # Calcular el promedio de edad por departamento
        # Calcular el promedio de edad por departamento
        promedio_edad = ECH_Seg_12024.groupby('nom_dpto')['e27'].mean().reset_index()

    ###############
        if option_depto == 'Todos':
            promedio_edad = ECH_Seg_12024.groupby('nom_dpto')['e27'].mean().reset_index()

        else:
            df_filtrado = ECH_Seg_12024[(ECH_Seg_12024["nom_dpto"] == option_depto)] 
            promedio_edad = df_filtrado.groupby('nom_dpto')['e27'].mean().reset_index()

    ###############

        # Calcular el promedio general de edad y la desviación estándar
        promedio_general = ECH_Seg_12024['e27'].mean()
        desviacion_estandar = ECH_Seg_12024['e27'].std()

        # Preparar los datos para el gráfico
        data = pd.DataFrame({
            'Departamentos': promedio_edad['nom_dpto'],
            'Edad': promedio_edad['e27']
        })

        dataTodos = pd.DataFrame({
            'Departamentos': ECH_Seg_12024['nom_dpto'],
            'Edad': ECH_Seg_12024['e27']
        })

        # Crear el gráfico de línea con Plotly Express
        fig_avg_price = px.line(
            data, 
            x='Departamentos', 
            y='Edad', 
            title='Promedio de Edad por Departamento',
            labels={'Edad': 'Edad Promedio', 'Departamentos': 'Departamentos'}
        )

        # Añadir una línea de referencia para el promedio general
        fig_avg_price.add_hline(
            y=promedio_general, 
            line_dash="dash", 
            line_color="red", 
            annotation_text="Promedio General", 
            annotation_position="bottom right"
        )

        # Añadir un área de sombreado para la desviación estándar
        fig_avg_price.add_shape(
            type="rect",
            x0=0, 
            x1=1, 
            y0=promedio_general - desviacion_estandar, 
            y1=promedio_general + desviacion_estandar,
            line=dict(color="LightSeaGreen", width=0),
            fillcolor="LightSeaGreen",
            opacity=0.2,
            layer="below",
            xref="paper",
            yref="y"
        )
        fig_avg_price.add_annotation(
            text="Desviación Estándar", 
            xref="paper", yref="y",
            x=0.99, y=promedio_general + desviacion_estandar, showarrow=False,
            font=dict(size=12, color="LightSeaGreen")
        )

        # Añadir etiquetas en los puntos que muestran el valor exacto de la edad promedio
        fig_avg_price.update_traces(
            mode='lines+markers+text', 
            text=data['Edad'].round(2),  # Mostrar el valor de la edad
            textposition='top center'
        )

        # Personalizar colores de la línea y los puntos
        fig_avg_price.update_traces(
            line=dict(color='blue'),  # Color de la línea
            marker=dict(size=8, color='blue', line=dict(width=2, color='DarkSlateGrey'))  # Personalización de los puntos
        )

        # Ajustar los ejes y mejorar la presentación del gráfico
        fig_avg_price.update_layout(
            xaxis_title='Departamento',
            yaxis_title='Edad Promedio',
            plot_bgcolor='rgba(0,0,0,0)',  # Fondo transparente
            paper_bgcolor='rgba(0,0,0,0)',  # Fondo transparente del papel
            font=dict(family="Arial", size=14, color="Black")  # Estilo de fuente
        )

        # Añadir interactividad avanzada con zoom y desplazamiento
        fig_avg_price.update_layout(
            xaxis=dict(fixedrange=False),  # Habilitar zoom en eje X
            yaxis=dict(fixedrange=False),  # Habilitar zoom en eje Y
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig_avg_price)

        # Añadir resumen estadístico de desviación estándar
        st.subheader("Estadísticas adicionales:")
        st.write(f"**Promedio General de Edad:** {round(promedio_general, 2)} años")
        st.write(f"**Desviación Estándar de Edad:** {round(desviacion_estandar, 2)} años")
        st.write(f"**Edad Promedio más alta:** {dataTodos['Edad'].max()} años ({dataTodos.loc[data['Edad'].idxmax(), 'Departamentos']})")
        st.write(f"**Edad Promedio más baja:** {dataTodos['Edad'].min()} años ({dataTodos.loc[data['Edad'].idxmin(), 'Departamentos']})")

    
         

    elif subtab == "2.3 - Nivel Educativo":
            if option_depto == 'Todos':                
                df_filtrado = ECH_Seg_12024
            else:    
                # Filtra el DataFrame por el departamento seleccionado
                df_filtrado = ECH_Seg_12024[(ECH_Seg_12024["nom_dpto"] == option_depto)] 

            # Agrupa los datos por nivel educativo y edad
            grouped = df_filtrado.groupby('NIV_EDU').size()
        
            # Configura el gráfico
            # Mostrar título
            st.markdown("<h1 style='text-align: center; font-size: 32px;'>Gráfico de barras por nivel educativo</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; font-size: 24px;'>Departamento: {option_depto}</h2>", unsafe_allow_html=True)

            # Agrupar datos por nivel educativo
            grouped = df_filtrado.groupby('NIV_EDU').size().reset_index(name='count')

            # Verificar si hay datos
            if grouped.empty:
                st.write("No hay datos disponibles para este nivel educativo.")
            else:
                # Verificar si los valores son válidos
                if grouped['count'].isnull().all() or grouped['count'].sum() == 0:
                    st.write("No hay suficientes datos para mostrar el gráfico.")
                else:
                    # Colores por rango
                    num_barras = len(grouped)
                    norm = mcolors.Normalize(vmin=grouped['count'].min(), vmax=grouped['count'].max())
                    cmap = cm.get_cmap('coolwarm')

                    # Crear la figura
                    fig, ax = plt.subplots(figsize=(12, 6))

                    # Generar gráfico de barras con colores personalizados
                    bars = ax.bar(grouped['NIV_EDU'], grouped['count'], color=cmap(norm(grouped['count'])), edgecolor='black')

                    # Títulos y etiquetas
                    ax.set_title('Número de personas por Nivel Educativo', fontsize=20, fontweight='bold')
                    ax.set_ylabel('Cantidad de Personas', fontsize=14)
                    ax.set_xlabel('Nivel Educativo', fontsize=14)

                    # Rotar etiquetas del eje X
                    plt.xticks(rotation=45, ha='right')

                    # Añadir valores encima de las barras con porcentaje
                    total_personas = grouped['count'].sum()
                    for bar in bars:
                        height = bar.get_height()
                        porcentaje = (height / total_personas) * 100
                        ax.annotate(f'{int(height)} ({porcentaje:.1f}%)',
                                    xy=(bar.get_x() + bar.get_width() / 2, height),
                                    xytext=(0, 5),
                                    textcoords="offset points",
                                    ha='center', va='bottom', fontsize=10, fontweight='bold')

                    # Media
                    media = grouped['count'].mean()
                    ax.axhline(media, color='red', linestyle='--', linewidth=1, label=f'Media: {int(media)}')

                    # Mínimo y Máximo
                    minimo = grouped['count'].min()
                    maximo = grouped['count'].max()
                    ax.text(len(grouped) - 1, maximo, f'Máximo: {maximo}', color='green', fontsize=12, fontweight='bold', ha='center')
                    ax.text(0, minimo, f'Mínimo: {minimo}', color='red', fontsize=12, fontweight='bold', ha='center')

                    # Añadir leyenda
                    ax.legend(loc='upper right')

                    # Ajustar fondo del gráfico
                    ax.set_facecolor('#f7f7f7')

                    # Crear barra de colores como referencia
                    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
                    sm.set_array([])
                    cbar = fig.colorbar(sm, ax=ax)
                    cbar.set_label('Cantidad de Personas', fontsize=12)

                    # Mostrar el gráfico
                    st.pyplot(fig)

                    # Mostrar resumen de estadísticas
                    st.subheader("Estadísticas clave:")
                    st.write(f"**Total de personas:** {grouped['count'].sum()}")
                    st.write(f"**Promedio de personas por nivel educativo:** {round(media, 2)}")
                    st.write(f"**Nivel educativo con mayor cantidad de personas:** {grouped.loc[grouped['count'].idxmax(), 'NIV_EDU']} ({maximo})")
                    st.write(f"**Nivel educativo con menor cantidad de personas:** {grouped.loc[grouped['count'].idxmin(), 'NIV_EDU']} ({minimo})")

    elif subtab == "2.4 - Distribución de ascendencia":
         ######grafico de torta
        st.subheader(f"Distribución de ascendencia por el conjunto de filtros aplicados")

        # Gráfico de la distribución de ascendencia
        if not df_filtrado.empty:
            columnas_ascendencia = ['e29_1', 'e29_2', 'e29_3', 'e29_4', 'e29_5']
            columnas_existentes = [col for col in columnas_ascendencia if col in df_filtrado.columns]

            if columnas_existentes:
                ascendencia_totals = [df_filtrado[col].sum() for col in columnas_existentes]
                ascendencia_labels = ['Afro o negra', 'Asiática o amarilla', 'Blanca', 'Indígena', 'Otra']

                fig_ascendencia, ax = plt.subplots()
                ax.pie(ascendencia_totals, labels=ascendencia_labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')

                st.pyplot(fig_ascendencia)
            else:
                st.write("No se encontraron las columnas de ascendencia en los datos.")
        else:
            st.write("No hay datos disponibles para los filtros seleccionados.")
       
    elif subtab == "2.5 - Composición de los hogares":
         #################
        st.subheader(f"Composición de los hogares por departamento")

        # Gráfico de barras apiladas para la composición de hogares
        df_hogares = df_filtrado[['nom_dpto', 'd23', 'd24', 'd25']].dropna()

        # Agrupar los hogares por departamento y sumar las personas mayores y menores de 14 años
        df_hogares_grouped = df_hogares.groupby('nom_dpto').sum().reset_index()

        # Crear un gráfico de barras apiladas
        fig_hogares, ax = plt.subplots(figsize=(10, 6))

        # Crear el gráfico apilado con personas mayores de 14 (D23) y menores de 14 (D24)
        ax.bar(df_hogares_grouped['nom_dpto'], df_hogares_grouped['d23'], label='Mayores de 14 años', color='blue')
        ax.bar(df_hogares_grouped['nom_dpto'], df_hogares_grouped['d24'], label='Menores de 14 años', color='orange', bottom=df_hogares_grouped['d23'])

        # Título y etiquetas
        ax.set_title('Composición de los hogares por departamento')
        ax.set_xlabel('Departamento')
        ax.set_ylabel('Número de personas')
        ax.legend()

        # Rotar las etiquetas de los departamentos en el eje x
        plt.xticks(rotation=45)

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig_hogares) 
        #################
    
    elif subtab == "2.6 - Todos los gráficos":
        
    ####################################################################
    ####################################################################

        # Calcular el promedio de edad por departamento

         # Gráfico de promedio de edad para todos los departamentos
        promedio_edad = ECH_Seg_12024.groupby('nom_dpto')['e27'].mean().reset_index()

        data = pd.DataFrame({
            'Departamentos': promedio_edad['nom_dpto'],
            'Edad': promedio_edad['e27']
        })

        fig_avg_price = px.line(data, x='Departamentos', y='Edad', title='Promedio de Edad para todos los departamento')
        st.plotly_chart(fig_avg_price)        
        ##########################################

        
        promedio_edad = ECH_Seg_12024.groupby('nom_dpto')['e27'].mean().reset_index()

    ###############
        if option_depto == 'Todos':
            promedio_edad = ECH_Seg_12024.groupby('nom_dpto')['e27'].mean().reset_index()

        else:
            df_filtrado = ECH_Seg_12024[(ECH_Seg_12024["nom_dpto"] == option_depto)] 
            promedio_edad = df_filtrado.groupby('nom_dpto')['e27'].mean().reset_index()

    ###############



        # Calcular el promedio general de edad y la desviación estándar
        promedio_general = ECH_Seg_12024['e27'].mean()
        desviacion_estandar = ECH_Seg_12024['e27'].std()

        # Preparar los datos para el gráfico
        data = pd.DataFrame({
            'Departamentos': promedio_edad['nom_dpto'],
            'Edad': promedio_edad['e27']
        })

        dataTodos = pd.DataFrame({
            'Departamentos': ECH_Seg_12024['nom_dpto'],
            'Edad': ECH_Seg_12024['e27']
        })

        # Crear el gráfico de línea con Plotly Express
        fig_avg_price = px.line(
            data, 
            x='Departamentos', 
            y='Edad', 
            title='Promedio de Edad por Departamento',
            labels={'Edad': 'Edad Promedio', 'Departamentos': 'Departamentos'}
        )

        # Añadir una línea de referencia para el promedio general
        fig_avg_price.add_hline(
            y=promedio_general, 
            line_dash="dash", 
            line_color="red", 
            annotation_text="Promedio General", 
            annotation_position="bottom right"
        )

        # Añadir un área de sombreado para la desviación estándar
        fig_avg_price.add_shape(
            type="rect",
            x0=0, 
            x1=1, 
            y0=promedio_general - desviacion_estandar, 
            y1=promedio_general + desviacion_estandar,
            line=dict(color="LightSeaGreen", width=0),
            fillcolor="LightSeaGreen",
            opacity=0.2,
            layer="below",
            xref="paper",
            yref="y"
        )
        fig_avg_price.add_annotation(
            text="Desviación Estándar", 
            xref="paper", yref="y",
            x=0.99, y=promedio_general + desviacion_estandar, showarrow=False,
            font=dict(size=12, color="LightSeaGreen")
        )

        # Añadir etiquetas en los puntos que muestran el valor exacto de la edad promedio
        fig_avg_price.update_traces(
            mode='lines+markers+text', 
            text=data['Edad'].round(2),  # Mostrar el valor de la edad
            textposition='top center'
        )

        # Personalizar colores de la línea y los puntos
        fig_avg_price.update_traces(
            line=dict(color='blue'),  # Color de la línea
            marker=dict(size=8, color='blue', line=dict(width=2, color='DarkSlateGrey'))  # Personalización de los puntos
        )

        # Ajustar los ejes y mejorar la presentación del gráfico
        fig_avg_price.update_layout(
            xaxis_title='Departamento',
            yaxis_title='Edad Promedio',
            plot_bgcolor='rgba(0,0,0,0)',  # Fondo transparente
            paper_bgcolor='rgba(0,0,0,0)',  # Fondo transparente del papel
            font=dict(family="Arial", size=14, color="Black")  # Estilo de fuente
        )

        # Añadir interactividad avanzada con zoom y desplazamiento
        fig_avg_price.update_layout(
            xaxis=dict(fixedrange=False),  # Habilitar zoom en eje X
            yaxis=dict(fixedrange=False),  # Habilitar zoom en eje Y
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig_avg_price)

        # Añadir resumen estadístico de desviación estándar
        st.subheader("Estadísticas adicionales:")
        st.write(f"**Promedio General de Edad:** {round(promedio_general, 2)} años")
        st.write(f"**Desviación Estándar de Edad:** {round(desviacion_estandar, 2)} años")
        st.write(f"**Edad Promedio más alta:** {dataTodos['Edad'].max()} años ({dataTodos.loc[data['Edad'].idxmax(), 'Departamentos']})")
        st.write(f"**Edad Promedio más baja:** {dataTodos['Edad'].min()} años ({dataTodos.loc[data['Edad'].idxmin(), 'Departamentos']})")

        if option_depto == 'Todos':
             df_filtrado = ECH_Seg_12024
        else:    
        # Filtra el DataFrame por el departamento seleccionado
            df_filtrado = ECH_Seg_12024[(ECH_Seg_12024["nom_dpto"] == option_depto)] 

          # Agrupa los datos por nivel educativo y edad
        grouped = df_filtrado.groupby('NIV_EDU').size()
                
            # Configura el gráfico
            # Mostrar título
        st.markdown("<h1 style='text-align: center; font-size: 32px;'>Gráfico de barras por nivel educativo</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; font-size: 24px;'>Departamento: {option_depto}</h2>", unsafe_allow_html=True)

            # Agrupar datos por nivel educativo
        grouped = df_filtrado.groupby('NIV_EDU').size().reset_index(name='count')

            # Verificar si hay datos
        if grouped.empty:
            st.write("No hay datos disponibles para este nivel educativo.")
        else:
                        # Verificar si los valores son válidos
            if grouped['count'].isnull().all() or grouped['count'].sum() == 0:
                   st.write("No hay suficientes datos para mostrar el gráfico.")
            else:
                    # Colores por rango
                    num_barras = len(grouped)
                    norm = mcolors.Normalize(vmin=grouped['count'].min(), vmax=grouped['count'].max())
                    cmap = cm.get_cmap('coolwarm')
                    # Crear la figura
                    fig, ax = plt.subplots(figsize=(12, 6))

                    # Generar gráfico de barras con colores personalizados
                    bars = ax.bar(grouped['NIV_EDU'], grouped['count'], color=cmap(norm(grouped['count'])), edgecolor='black')

                    # Títulos y etiquetas
                    ax.set_title('Número de personas por Nivel Educativo', fontsize=20, fontweight='bold')
                    ax.set_ylabel('Cantidad de Personas', fontsize=14)
                    ax.set_xlabel('Nivel Educativo', fontsize=14)

                    # Rotar etiquetas del eje X
                    plt.xticks(rotation=45, ha='right')

                            # Añadir valores encima de las barras con porcentaje
                    total_personas = grouped['count'].sum()
                    for bar in bars:
                        height = bar.get_height()
                        porcentaje = (height / total_personas) * 100
                        ax.annotate(f'{int(height)} ({porcentaje:.1f}%)',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, fontweight='bold')

                    # Media
                    media = grouped['count'].mean()
                    ax.axhline(media, color='red', linestyle='--', linewidth=1, label=f'Media: {int(media)}')

                            # Mínimo y Máximo
                    minimo = grouped['count'].min()
                    maximo = grouped['count'].max()
                    ax.text(len(grouped) - 1, maximo, f'Máximo: {maximo}', color='green', fontsize=12, fontweight='bold', ha='center')
                    ax.text(0, minimo, f'Mínimo: {minimo}', color='red', fontsize=12, fontweight='bold', ha='center')

                            # Añadir leyenda
                    ax.legend(loc='upper right')

                            # Ajustar fondo del gráfico
                    ax.set_facecolor('#f7f7f7')

                            # Crear barra de colores como referencia
                    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
                    sm.set_array([])
                    cbar = fig.colorbar(sm, ax=ax)
                    cbar.set_label('Cantidad de Personas', fontsize=12)

                            # Mostrar el gráfico
                    st.pyplot(fig)

                            # Mostrar resumen de estadísticas
                    st.subheader("Estadísticas clave:")
                    st.write(f"**Total de personas:** {grouped['count'].sum()}")
                    st.write(f"**Promedio de personas por nivel educativo:** {round(media, 2)}")
                    st.write(f"**Nivel educativo con mayor cantidad de personas:** {grouped.loc[grouped['count'].idxmax(), 'NIV_EDU']} ({maximo})")
                    st.write(f"**Nivel educativo con menor cantidad de personas:** {grouped.loc[grouped['count'].idxmin(), 'NIV_EDU']} ({minimo})")


                ######grafico de torta
        st.subheader(f"Distribución de ascendencia por el conjunto de filtros aplicados")

                # Gráfico de la distribución de ascendencia
        if not df_filtrado.empty:
                    columnas_ascendencia = ['e29_1', 'e29_2', 'e29_3', 'e29_4', 'e29_5']
                    columnas_existentes = [col for col in columnas_ascendencia if col in df_filtrado.columns]

                    if columnas_existentes:
                        ascendencia_totals = [df_filtrado[col].sum() for col in columnas_existentes]
                        ascendencia_labels = ['Afro o negra', 'Asiática o amarilla', 'Blanca', 'Indígena', 'Otra']

                        fig_ascendencia, ax = plt.subplots()
                        ax.pie(ascendencia_totals, labels=ascendencia_labels, autopct='%1.1f%%', startangle=90)
                        ax.axis('equal')

                        st.pyplot(fig_ascendencia)
                    else:
                        st.write("No se encontraron las columnas de ascendencia en los datos.")
        else:
                    st.write("No hay datos disponibles para los filtros seleccionados.")

                #################
        st.subheader(f"Composición de los hogares por departamento")

                # Gráfico de barras apiladas para la composición de hogares
        df_hogares = df_filtrado[['nom_dpto', 'd23', 'd24', 'd25']].dropna()

                # Agrupar los hogares por departamento y sumar las personas mayores y menores de 14 años
        df_hogares_grouped = df_hogares.groupby('nom_dpto').sum().reset_index()

                # Crear un gráfico de barras apiladas
        fig_hogares, ax = plt.subplots(figsize=(10, 6))

                # Crear el gráfico apilado con personas mayores de 14 (D23) y menores de 14 (D24)
        ax.bar(df_hogares_grouped['nom_dpto'], df_hogares_grouped['d23'], label='Mayores de 14 años', color='blue')
        ax.bar(df_hogares_grouped['nom_dpto'], df_hogares_grouped['d24'], label='Menores de 14 años', color='orange', bottom=df_hogares_grouped['d23'])

                # Título y etiquetas
        ax.set_title('Composición de los hogares por departamento')
        ax.set_xlabel('Departamento')
        ax.set_ylabel('Número de personas')
        ax.legend()

                # Rotar las etiquetas de los departamentos en el eje x
        plt.xticks(rotation=45)

                # Mostrar el gráfico en Streamlit
        st.pyplot(fig_hogares) 
                #################
      
with tabs[3]:  
    # Función para crear y renderizar el mapa
    def crear_mapa(latitud, longitud, zoom=6):
        # Crear el mapa base centrado en la ubicación proporcionada
        return folium.Map(location=[latitud, longitud], zoom_start=zoom)

    # Función para agregar marcadores al mapa
    def agregar_marcadores(m, departamentos):
        for dep, info in departamentos.items():
            folium.Marker(
                location=[info['lat'], info['lon']],
                popup=info['popup'],
                icon=folium.Icon(color='blue', icon='info-sign')  # Icono personalizado
            ).add_to(m)

    departamentos = {
        'Artigas': {'lat': -30.4, 'lon': -56.46667, 'popup': 'Artigas, Uruguay'},
        'Canelones': {'lat': -34.52278, 'lon': -56.27778, 'popup': 'Canelones, Uruguay'},
        'Cerro Largo': {'lat': -33.02940, 'lon': -55.35351, 'popup': 'Cerro Largo, Uruguay'},
        'Colonia': {'lat': -34.4626200, 'lon': -57.8397600, 'popup': 'Colonia, Uruguay'},
        'Durazno': {'lat': -33.38056, 'lon': -56.52361, 'popup': 'Durazno, Uruguay'},
        'Flores': {'lat': -33.583333, 'lon': -56.833333, 'popup': 'Flores, Uruguay'},
        'Florida': {'lat': -34.09556, 'lon': -56.21417, 'popup': 'Florida, Uruguay'},
        'Lavalleja': {'lat': -33.997196, 'lon': -54.999224, 'popup': 'Lavalleja, Uruguay'},
        'Maldonado': {'lat': -34.908716, 'lon': -54.958272, 'popup': 'Maldonado, Uruguay'},
        'Montevideo': {'lat': -34.90328, 'lon': -56.18816, 'popup': 'Montevideo, Uruguay'},
        'Paysandú': {'lat': -32.3171, 'lon': -58.08072, 'popup': 'Paysandú, Uruguay'},
        'Río Negro': {'lat': -32.725742, 'lon': -57.387578, 'popup': 'Río Negro, Uruguay'},
        'Rivera': {'lat': -30.90534, 'lon': -55.55076, 'popup': 'Rivera, Uruguay'},
        'Rocha': {'lat': -34.0, 'lon': -54.0, 'popup': 'Rocha, Uruguay'},
        'Salto': {'lat': -31.38333, 'lon': -57.96667, 'popup': 'Salto, Uruguay'},
        'San José': {'lat': -34.455, 'lon': -56.616944, 'popup': 'San José, Uruguay'},
        'Soriano': {'lat': -33.492127, 'lon': -57.78931, 'popup': 'Soriano, Uruguay'},
        'Tacuarembó': {'lat': -31.71694, 'lon': -55.98111, 'popup': 'Tacuarembó, Uruguay'},
        'Treinta y Tres': {'lat': -33.23333, 'lon': -54.38333, 'popup': 'Treinta y Tres, Uruguay'}
    }

    if option_depto == 'Todos':
        st.subheader("Mapa de Uruguay con todos los departamentos")

        # Crear un mapa centrado en Uruguay
        m = crear_mapa(-32.522779, -55.765835, zoom=6)

        # Agregar todos los departamentos al mapa
        agregar_marcadores(m, departamentos)

        # Añadir control de capas
        folium.LayerControl().add_to(m)

        # Renderizar el mapa en Streamlit
        st_folium(m, width=800, height=500)
    
    else:
        # Verificar si el departamento existe en el diccionario
        if option_depto in departamentos:
            dep_info = departamentos[option_depto]
            st.subheader(f"Departamento de {option_depto}")

            # Crear el mapa centrado en el departamento
            m = crear_mapa(dep_info['lat'], dep_info['lon'], zoom=10)

            # Agregar solo el marcador del departamento seleccionado
            folium.Marker(
                location=[dep_info['lat'], dep_info['lon']],
                popup=dep_info['popup'],
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)

            # Renderizar el mapa en Streamlit
            st_folium(m, width=800, height=500)

        else:
            st.write("Departamento no encontrado.")


   
