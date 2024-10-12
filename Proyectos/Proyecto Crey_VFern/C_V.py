import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

cat_per = pd.read_csv('C:/Users/macar/Desktop/python-para-ciencia-de-datos/cat_per.csv', sep=';')
per_cat = pd.read_csv('C:/Users/macar/Desktop/python-para-ciencia-de-datos/per_cat.csv', sep=';')


st.title('ANÁLISIS DE CATASTRO Y PERMISOS DE OBRA DE LA IMM')
