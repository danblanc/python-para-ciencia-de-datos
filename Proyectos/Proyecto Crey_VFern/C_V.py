import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

cat_per = pd.read_csv('C:/Users/macar/Desktop/python-para-ciencia-de-datos/cat_per.csv', sep=';')
per_cat = pd.read_csv('C:/Users/macar/Desktop/python-para-ciencia-de-datos/per_cat.csv', sep=';')


st.title('ANÁLISIS DE CATASTRO Y PERMISOS DE OBRA DE LA IMM')

tab1, tab2, tab3 = st.tabs(["CATASTRO", "PERMISOS", "CATASTRO_PERMISOS"])

with tab1:
    st.header("DESCRIPCIÓN DE CATASTRO")
    st.write("...")

with tab2:
    st.header("DESCRIPCIÓN DE PERMISOS")
    st.write("...")

with tab3:
    st.header("CATASTRO_PERMISOS")
    st.write("...")
