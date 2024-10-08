* Encoding: windows-1252.

****************CALCULOS EN LA BASE DE GASTOS******************.
*******************************************************mach base de nutrientes con base de gastos********************************.
*****levanto la base de gastos y macheo la tabla de composición de alimentos que creamos, las variables deciles y quintiles y hogares con niños****.
****alimentos con registros en la base de gastos son 237180***:
****6853 hogares****BASE HOGAR 6889***.
***VER CON CUAL BASE TRABAJAR... HAY QUE MACHEAR A LA DE PEROSONA****.
****actualización 5/8****. 
****actualización 23/8****. 
****actualización 29/8****. 
****actualización 13/9****. 
***se dejan los destino codigos 1, 5****
***para alimentación solo van los destinos 1 y 5***.
***se corre una nueva clasificación de azucar libre 25 - 3 al 27 - 3***

GET 
  FILE='C:\Users\Cecilia\Desktop\Base Engih 2016 marzo 2022\ENGIH 2016 Base de Datos Gastos.sav'.

WEIGHT
  OFF.

IF (DESTINOCODIGO = 1 or DESTINOCODIGO = 5) gasto_hogar = 1.

freq gasto_hogar.

FILTER OFF.
USE ALL.
SELECT IF(gasto_hogar = 1).
EXECUTE .

freq gasto_hogar DESTINOCODIGO.

SAVE OUTFILE='C:\Users\Cecilia\Desktop\Base Engih 2016 marzo 2022\Base de Gastos Engih 2016 con Nutrientes.sav'
 /COMPRESSED.

sort cases by ARTICULOCODIGO (a) .

##C:\Users\ctoledo\Desktop\SONU 2024\Proyecto Tablas de composición quimica 2024\Base Engih 2016 para R\azucar libre nueva clasificación\Tabla COMPOSICIÓN QUIMICA
ésta es la tabla que levanto y uso de composición quimica##

MATCH FILES /FILE=*
 /TABLE='C:\Users\Cecilia\Desktop\Base Engih 2016 marzo 2022\Tabla COMPOSICIÓN QUIMICA\Tabla composición para mach 01 - 6 - 2021.sav'
 /BY ARTICULOCODIGO.
EXECUTE.

sort cases by NUMERO (a) .

MATCH FILES /FILE=*
 /TABLE='C:\Users\Cecilia\Desktop\Base Engih 2016 marzo 2022\variables intermedias\Niños hogar.sav'
 /BY NUMERO.
EXECUTE.

sort cases by CCIF_2016 (a) .

MATCH FILES /FILE=*
 /TABLE='C:\Users\Cecilia\Desktop\Base Engih 2016 marzo 2022\variables intermedias\Grupos 2006 y ultra msp.sav'
 /BY CCIF_2016.
EXECUTE.

sort cases by CCIF_2016 (a) .

MATCH FILES /FILE=*
 /TABLE='C:\Users\Cecilia\Desktop\Base Engih 2016 marzo 2022\variables intermedias\clasificaciones grupos 20 - 9 - 2021.sav'
 /BY CCIF_2016.
EXECUTE.

sort cases by CCIF_2016 (a) .

MATCH FILES /FILE=*
 /TABLE='C:\Users\Cecilia\Desktop\Base Engih 2016 marzo 2022\azucar libre nueva clasificación\azucar libre new.sav'
 /BY CCIF_2016.
EXECUTE.

value labels grupos_2006 
1 Panes, galletas, Alfajores y productos de pastelería
2 Arroz, fideos, harinas y otros cereales
3 Carne de vaca, pollo, cerdo y cordero
4 Fiambres y Embutidos
5 Pescados
6 Leches y derivados
7 Huevo
8 Frutas
9 Verduras
10 Papa y Boniatos
11 Lentejas, porotos, garbanzo y arvejas
12 Dulces y dulces
13 Sal, caldos y sopas concentradas
14 Aceites, grasas y oleaginosas
15 Yerba, café, té y cocoa en polvo
16 Otros alimentos
17 Agua, Refrescos y jugos
18 Bebidas alcohólicas
19 Comidas y Bebidas fuera del hogar
20 Programas Sociales.

value labels Ultra_mps
1 "Si"
2 "No".

freq grupos_2006 Ultra_mps Azúc_libres_new prop_azucarlibre_new.

*******************recodificación descripción en la variable alimentos*****************.

IF (Descripción_CCIF_2016_msp = "Bebidas no alcohólicas, otras (Terma, malta, energizantes)") Alimentos = 2.                      

****mach de los requerimientos calculados****.

USE ALL.
COMPUTE filter_$=(Alimentos  >= 1).
VARIABLE LABEL filter_$ 'Alimentos  >= 1 (FILTER)'.
VALUE LABELS filter_$  0 'No seleccionado' 1 'Seleccionado'.
FORMAT filter_$ (f1.0).
FILTER BY filter_$.
EXECUTE .

FILTER OFF.
USE ALL.
SELECT IF(Alimentos  >= 1).
EXECUTE .

IF (CCIF_2016 = 1121110) Na_2016 = 61.15.
IF (CCIF_2016 = 1121120)  Na_2016  = 61.15 .
IF (CCIF_2016 = 1122010 )  Na_2016  = 61.15 .
IF (CCIF_2016 = 1122020 )  Na_2016  = 61.15 .
IF (CCIF_2016 = 1124050 )  Na_2016  = 82 .
IF (CCIF_2016 = 1125041 )  Na_2016  = 970 .
IF (CCIF_2016 = 1125042 )  Na_2016  = 970 .
IF (CCIF_2016 = 1125051 )  Na_2016  = 970 .
IF (CCIF_2016 = 1125052 )  Na_2016  = 970 .
IF (CCIF_2016 = 1125210 )  Na_2016  = 668 .
IF (CCIF_2016 = 1132010 )  Na_2016  = 41.15 .
IF (CCIF_2016 = 1133023 )  Na_2016  = 414 .
IF (CCIF_2016 = 11112350 )  Na_2016  = 290 .
IF (CCIF_2016 = 11112360 )  Na_2016  = 271 .
IF (CCIF_2016 = 11112392 )  Na_2016  = 53.5 .
IF (CCIF_2016 = 11112393 )  Na_2016  = 53.5 .
IF (CCIF_2016 = 11112500 )  Na_2016  = 1357 .
IF (CCIF_2016 = 11112700 )  Na_2016  = 462 .
exe. 

COMPUTE sal_2= Na_2016 / 400.
EXECUTE .

COMPUTE DIF_sal = sal_2016  -  sal_2 .
EXECUTE .

delete variable sal_2016. 

rename variable sal_2 = sal_2016.

freq sal_2016. 

* Identificar casos duplicados.
SORT CASES BY NUMERO(A) .
MATCH FILES /FILE = * /BY NUMERO
 /FIRST = PrimarioPrimero /LAST = hogar.
DO IF (PrimarioPrimero).
COMPUTE SecuenciaCoincidencia = 1 - hogar.
ELSE.
COMPUTE SecuenciaCoincidencia = SecuenciaCoincidencia + 1.
END IF.
LEAVE SecuenciaCoincidencia.
FORMAT SecuenciaCoincidencia (f7).
COMPUTE InDupGrp = SecuenciaCoincidencia > 0.
SORT CASES InDupGrp(D).
MATCH FILES /FILE = * /DROP = PrimarioPrimero InDupGrp SecuenciaCoincidencia.
VARIABLE LABELS hogar 'Indicador de cada último caso coincidente como Primario' .
VALUE LABELS hogar 0 'Caso duplicado' 1 'Caso primario'.
VARIABLE LEVEL hogar (ORDINAL).
FREQUENCIES VARIABLES = hogar .
EXECUTE.

SAVE OUTFILE='C:\Users\Cecilia\Desktop\Base Engih 2016 marzo 2022\Base de Gastos Engih 2016 con Nutrientes 26 - 03.sav'
 /COMPRESSED.

freq grupos_2006 Ultra_mps Azúc_libres_new prop_azucarlibre_new ref_cb  agua_cb galletas_cb alfajores_cb.

**************************************************.

rename variable CANTIDADCONVERTIDA = CANTIDADCONVERTIDA_0.

COMPUTE CANTIDADCONVERTIDA =  CANTIDADCONVERTIDA_0 / FC.
EXECUTE .

COMPUTE Calorias_final = CANTIDADCONVERTIDA * Calorias_2016 / 100 .
EXECUTE .

**************************************************.

if (Niños_hogar_sum >= 1)  Niños_hogar = 1.

RECODE
  Niños_hogar  (SYSMIS=0)  .
EXECUTE .

value labels Niños_hogar  
0 "Hogar sin niños"
1 "Hogar con niños".

COMPUTE gr_mes = CANTIDADCONVERTIDA * 4.3.
EXECUTE .
exe.

**************me manejo con gramos en días***************.

COMPUTE gr_dia = CANTIDADCONVERTIDA * 52.179 / 366.
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /gr_hogar = SUM(gr_dia).

COMPUTE gr_percapita = gr_hogar / nper_hogar.
EXECUTE .

COMPUTE Cal_articulo_dia = gr_dia * Calorias_2016 / 100 .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /Calorias_hogar = SUM(Cal_articulo_dia).

COMPUTE Cal_percapita = Calorias_hogar / nper_hogar.
EXECUTE .

COMPUTE adec_kcal = Cal_percapita * 100 / reqk_mean.
EXECUTE .
exe.

**********************************Distribución de macronutrientes**********************************.
***************expresados en el hogar no lo hice per capita*****************.

WEIGHT
  OFF.

COMPUTE gr_proteinas = gr_dia * Proteinas_2016 /100.
EXECUTE .

RECODE
  gr_proteinas (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /prot_hogar = SUM(gr_proteinas).

COMPUTE cal_proteinas = prot_hogar * 4.
EXECUTE .
exe.

*************************calculo de grasas********************.

WEIGHT
  OFF.

COMPUTE gr_grasas = gr_dia * Grasas_2016 / 100.
EXECUTE .

RECODE
  gr_grasas (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /grasas_hogar = SUM(gr_grasas).

COMPUTE cal_grasas = grasas_hogar * 9.
EXECUTE .
exe.

*************************calculo de hidratos********************.

WEIGHT
  OFF.

COMPUTE gr_hidratos = gr_dia * Hidratos_2016 / 100.
EXECUTE .

RECODE
  gr_hidratos (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /hidratos_hogar = SUM(gr_hidratos).

COMPUTE cal_hidratos = hidratos_hogar * 4.
EXECUTE .

COMPUTE calorias_macro = cal_proteinas + cal_hidratos + cal_grasas.
EXECUTE .
exe.

*******************adecuación calorica********************.

COMPUTE adec_proteinas = cal_proteinas * 100 / calorias_macro.
EXECUTE .

COMPUTE adec_grasas = cal_grasas * 100 / calorias_macro.
EXECUTE .
exe.

COMPUTE adec_hidratos = cal_hidratos * 100 / calorias_macro.
EXECUTE .

WEIGHT
  OFF.

*************************calculo de AG Saturados********************.

WEIGHT
  OFF.

COMPUTE gr_AGS = gr_dia * AGS_2016 / 100.
EXECUTE .

RECODE
 gr_AGS (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /AGS_hogar = SUM(gr_AGS).

COMPUTE cal_AGS = AGS_hogar * 9.
EXECUTE .

COMPUTE cal_AGS_percapita = cal_AGS / nper_hogar.
EXECUTE .

COMPUTE adec_AGS = cal_AGS_percapita * 100 / Cal_percapita.
EXECUTE .
exe.

*************************calculo de azucares libres********************.

COMPUTE gr_azucar_libre = gr_hidratos * prop_azucarlibre_2016/100.
EXECUTE .

RECODE
  gr_azucar_libre (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /azu_hogar = SUM(gr_azucar_libre).

COMPUTE cal_azucar_libre = azu_hogar * 4.
EXECUTE .

COMPUTE azu_libre_per_capita = cal_azucar_libre / nper_hogar.
EXECUTE .

COMPUTE prop_azucar_libre = azu_libre_per_capita * 100 / Cal_percapita.
EXECUTE .
exe.

*************************calculo de azucares libres new********************.

COMPUTE gr_azucar_new = gr_hidratos * prop_azucarlibre_new/100.
EXECUTE .

RECODE
  gr_azucar_new (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /azu_hogar_new = SUM(gr_azucar_new).

COMPUTE cal_azucar_libre_new = azu_hogar_new * 4.
EXECUTE .

COMPUTE azu_libre_new_per_capita = cal_azucar_libre_new / nper_hogar.
EXECUTE .

COMPUTE prop_azucar_libre_new = azu_libre_new_per_capita * 100 / Cal_percapita.
EXECUTE .


*************************calculo de sal********************.

WEIGHT
  OFF.

COMPUTE sal_dia = gr_dia * sal_2016 / 100.
EXECUTE .

RECODE
  sal_dia (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /sal_gr0= SUM(sal_dia).

COMPUTE sal_gr = sal_gr0 / nper_hogar.
EXECUTE .
exe.

*************************sodio********************.

WEIGHT
  OFF.

COMPUTE sodio_dia = gr_dia * Na_2016 / 100.
EXECUTE .

RECODE
  sodio_dia (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /sodio_mg0= SUM(sodio_dia).

COMPUTE sodio_mg = sodio_mg0 / nper_hogar.
EXECUTE .
exe.

*************************FIBRA********************.

WEIGHT
  OFF.

COMPUTE fibra_dia = gr_dia * Fibra_2016 / 100.
EXECUTE .

RECODE
  fibra_dia (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /fibra_gr0= SUM(fibra_dia).

COMPUTE fibra_gr = fibra_gr0 / nper_hogar.
EXECUTE .
exe.

*************************HIERRO********************.

WEIGHT
  OFF.

COMPUTE hierro_dia = gr_dia * FE_2016 / 100.
EXECUTE .

RECODE
  hierro_dia (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /hierro_mg0= SUM(hierro_dia).

COMPUTE hierro_percapita = hierro_mg0 / nper_hogar.
EXECUTE .
exe.

*************************potacio********************.

WEIGHT
  OFF.

COMPUTE K_dia = gr_dia * K_2016 / 100.
EXECUTE .

RECODE
  K_dia (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /K_mg0= SUM(K_dia).

COMPUTE K_percapita = K_mg0 / nper_hogar.
EXECUTE .
exe.

*************************Acido Folico********************.

WEIGHT
  OFF.

COMPUTE AF_dia = gr_dia * A_Folico_2016 / 100.
EXECUTE .

RECODE
  AF_dia (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /AF_mg0= SUM(AF_dia).

COMPUTE AF_percapita = AF_mg0 / nper_hogar.
EXECUTE .
exe.

*************************calcio********************.

WEIGHT
  OFF.

COMPUTE calcio_dia = gr_dia * Ca_2016 / 100.
EXECUTE .

RECODE
  calcio_dia (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO
  /CA_mg0= SUM(calcio_dia).

COMPUTE CA_percapita = CA_mg0 / nper_hogar.
EXECUTE .
exe.

*************************grupo_vegyfrutas_2016********************.

IF (CCIF_2016 = 1111360) grupo_vegyfrutas_2016 = 0.
IF (CCIF_2016 = 1171390) grupo_vegyfrutas_2016 = 0.
IF (CCIF_2016 = 1171400) grupo_vegyfrutas_2016 = 0.
IF (CCIF_2016 = 1171460) grupo_vegyfrutas_2016 = 0.
IF (CCIF_2016 = 1261010) grupo_vegyfrutas_2016 = 0.
IF (CCIF_2016 = 11112442) grupo_vegyfrutas_2016 = 0.
IF (CCIF_2016 = 11112450) grupo_vegyfrutas_2016 = 0.
IF (CCIF_2016 = 11112490) grupo_vegyfrutas_2016 = 0.
IF (CCIF_2016 = 11112850) grupo_vegyfrutas_2016 = 0.
IF (CCIF_2016 = 11113010) grupo_vegyfrutas_2016 = 0.
IF (CCIF_2016 = 11112430) grupo_vegyfrutas_2016 = 1.
IF (CCIF_2016 = 11112443) grupo_vegyfrutas_2016 = 1.
exe.

IF (grupo_vegyfrutas_2016 = 1) vegyfrutagr = gr_dia. 

RECODE
  vegyfrutagr (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_vegyfrutasSUM= SUM(vegyfrutagr).

COMPUTE gr_vegyfruta_percapita = gr_vegyfrutasSUM / nper_hogar.
EXECUTE .
exe.

*************************ALIMENTOS Y BEBIDAS********************.

IF (Alimentos = 1) alimentosgr = gr_dia. 
IF (Alimentos = 1) alimentoscal = Cal_articulo_dia. 

RECODE
  alimentosgr (SYSMIS=0)  .
EXECUTE .

RECODE
 alimentoscal (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_Alimentos_sum = SUM(alimentosgr).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_Alimentos_sum = SUM(alimentoscal).

COMPUTE gr_Alimentos_percapita = gr_Alimentos_sum / nper_hogar.
EXECUTE .

COMPUTE cal_Alimentos_percapita = cal_Alimentos_sum / nper_hogar.
EXECUTE .
exe.

IF (Alimentos = 2) bebidasgr = gr_dia. 
IF (Alimentos = 2) bebidascal = Cal_articulo_dia. 

RECODE
  bebidasgr  (SYSMIS=0)  .
EXECUTE .

RECODE
 bebidascal  (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_bebidas_sum = SUM(bebidasgr).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_bebidas_sum = SUM(bebidascal).

COMPUTE gr_bebidas_percapita = gr_bebidas_sum / nper_hogar.
EXECUTE .

COMPUTE cal_bebidas_percapita = cal_bebidas_sum / nper_hogar.
EXECUTE .

delete variable gr_bebidas_sum bebidasgr cal_bebidas_sum bebidascal.
delete variable gr_Alimentos_sum alimentosgr cal_Alimentos_sum alimentoscal.

***********************************grupos 2006***************************************.
***1 Panes, galletas, Alfajores y productos de pastelería***.

IF (grupos_2006 = 1) gr_panes  = gr_dia. 
IF (grupos_2006 = 1) cal_panes = Cal_articulo_dia. 

RECODE
  gr_panes (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_panes (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_panesSUM= SUM(gr_panes).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_panesSUM = SUM(cal_panes).

COMPUTE gr_panes_percapita = gr_panesSUM / nper_hogar.
EXECUTE .

COMPUTE cal_panes_percapita = cal_panesSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_panes cal_panes gr_panesSUM cal_panesSUM.

freq gr_panes_percapita cal_panes_percapita.

***2 Arroz, fideos, harinas y otros cereales***.

IF (grupos_2006 = 2) gr_Cereales  = gr_dia. 
IF (grupos_2006 = 2) cal_Cereales = Cal_articulo_dia. 

RECODE
  gr_Cereales (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Cereales (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_CerealesSUM= SUM(gr_Cereales).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_CerealesSUM = SUM(cal_Cereales).

COMPUTE gr_Cereales_percapita = gr_CerealesSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Cereales_percapita = cal_CerealesSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Cereales cal_Cereales gr_CerealesSUM cal_CerealesSUM.

freq gr_Cereales_percapita cal_Cereales_percapita.

***3 carnes***.

IF (grupos_2006 = 3) gr_Carnes  = gr_dia. 
IF (grupos_2006 = 3) cal_Carnes = Cal_articulo_dia. 

RECODE
  gr_Carnes (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Carnes (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_CarnesSUM= SUM(gr_Carnes).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_CarnesSUM = SUM(cal_Carnes).

COMPUTE gr_Carnes_percapita = gr_CarnesSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Carnes_percapita = cal_CarnesSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Carnes cal_Carnes gr_CarnesSUM cal_CarnesSUM.

freq gr_Carnes_percapita cal_Carnes_percapita.

***4 Fiambres y Embutidos***.

IF (grupos_2006 = 4) gr_Fiambres  = gr_dia. 
IF (grupos_2006 = 4) cal_Fiambres = Cal_articulo_dia. 

RECODE
  gr_Fiambres (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Fiambres (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_FiambresSUM= SUM(gr_Fiambres).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_FiambresSUM = SUM(cal_Fiambres).

COMPUTE gr_Fiambres_percapita = gr_FiambresSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Fiambres_percapita = cal_FiambresSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Fiambres cal_Fiambres gr_FiambresSUM cal_FiambresSUM.

freq gr_Fiambres_percapita cal_Fiambres_percapita.

***5 Pescados***.

IF (grupos_2006 = 5) gr_Pescado  = gr_dia. 
IF (grupos_2006 = 5) cal_Pescado = Cal_articulo_dia. 

RECODE
  gr_Pescado (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Pescado (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_PescadoSUM= SUM(gr_Pescado).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_PescadoSUM = SUM(cal_Pescado).

COMPUTE gr_Pescado_percapita = gr_PescadoSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Pescado_percapita = cal_PescadoSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Pescado cal_Pescado gr_PescadoSUM cal_PescadoSUM.

freq gr_Pescado_percapita cal_Pescado_percapita.

***6 Leches y derivados***.

IF (grupos_2006 = 6) gr_Leche  = gr_dia. 
IF (grupos_2006 = 6) cal_Leche = Cal_articulo_dia. 

RECODE
  gr_Leche (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Leche (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_LecheSUM= SUM(gr_Leche).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_LecheSUM = SUM(cal_Leche).

COMPUTE gr_Leche_percapita = gr_LecheSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Leche_percapita = cal_LecheSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Leche cal_Leche gr_LecheSUM cal_LecheSUM.

freq gr_Leche_percapita cal_Leche_percapita.

***7 Huevo***.

IF (grupos_2006 = 7) gr_Huevo  = gr_dia. 
IF (grupos_2006 = 7) cal_Huevo = Cal_articulo_dia. 

RECODE
  gr_Huevo (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Huevo (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_HuevoSUM= SUM(gr_Huevo).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_HuevoSUM = SUM(cal_Huevo).

COMPUTE gr_Huevo_percapita = gr_HuevoSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Huevo_percapita = cal_HuevoSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Huevo cal_Huevo gr_HuevoSUM cal_HuevoSUM.

freq gr_Huevo_percapita cal_Huevo_percapita.

***8 Frutas***.

IF (grupos_2006 = 8) gr_Frutas  = gr_dia. 
IF (grupos_2006 = 8) cal_Frutas = Cal_articulo_dia. 

RECODE
  gr_Frutas (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Frutas (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_FrutasSUM= SUM(gr_Frutas).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_FrutasSUM = SUM(cal_Frutas).

COMPUTE gr_Frutas_percapita = gr_FrutasSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Frutas_percapita = cal_FrutasSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Frutas cal_Frutas gr_FrutasSUM cal_FrutasSUM.

freq gr_Frutas_percapita cal_Frutas_percapita.

***9 Verduras***.

IF (grupos_2006 = 9) gr_Vegetales  = gr_dia. 
IF (grupos_2006 = 9) cal_Vegetales = Cal_articulo_dia. 

RECODE
  gr_Vegetales (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Vegetales (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_VegetalesSUM= SUM(gr_Vegetales).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_VegetalesSUM = SUM(cal_Vegetales).

COMPUTE gr_Vegetales_percapita = gr_VegetalesSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Vegetales_percapita = cal_VegetalesSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Vegetales cal_Vegetales gr_VegetalesSUM cal_VegetalesSUM.

freq gr_Vegetales_percapita cal_Vegetales_percapita.

***10 Papa y Boniatos***.

IF (grupos_2006 = 10) gr_Papa  = gr_dia. 
IF (grupos_2006 = 10) cal_Papa = Cal_articulo_dia. 

RECODE
  gr_Papa (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Papa (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_PapaSUM= SUM(gr_Papa).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_PapaSUM = SUM(cal_Papa).

COMPUTE gr_Papa_percapita = gr_PapaSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Papa_percapita = cal_PapaSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Papa cal_Papa gr_PapaSUM cal_PapaSUM.

freq gr_Papa_percapita cal_Papa_percapita.

***11 Lentejas, porotos, garbanzo y arvejas***.

IF (grupos_2006 = 11) gr_Leguminosa  = gr_dia. 
IF (grupos_2006 = 11) cal_Leguminosa = Cal_articulo_dia. 

RECODE
  gr_Leguminosa (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Leguminosa (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_LeguminosaSUM= SUM(gr_Leguminosa).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_LeguminosaSUM = SUM(cal_Leguminosa).

COMPUTE gr_Leguminosa_percapita = gr_LeguminosaSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Leguminosa_percapita = cal_LeguminosaSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Leguminosa cal_Leguminosa gr_LeguminosaSUM cal_LeguminosaSUM.

freq gr_Leguminosa_percapita cal_Leguminosa_percapita.

***12 Dulces y dulces***.

IF (grupos_2006 = 12) gr_Dulces  = gr_dia. 
IF (grupos_2006 = 12) cal_Dulces = Cal_articulo_dia. 

RECODE
  gr_Dulces (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Dulces (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_DulcesSUM= SUM(gr_Dulces).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_DulcesSUM = SUM(cal_Dulces).

COMPUTE gr_Dulces_percapita = gr_DulcesSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Dulces_percapita = cal_DulcesSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Dulces cal_Dulces gr_DulcesSUM cal_DulcesSUM.

freq gr_Dulces_percapita cal_Dulces_percapita.

***13 Sal, caldos y sopas concentradas***.

IF (grupos_2006 = 13) gr_Caldos  = gr_dia. 
IF (grupos_2006 = 13) cal_Caldos = Cal_articulo_dia. 

RECODE
  gr_Caldos (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Caldos (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_CaldosSUM= SUM(gr_Caldos).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_CaldosSUM = SUM(cal_Caldos).

COMPUTE gr_Caldos_percapita = gr_CaldosSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Caldos_percapita = cal_CaldosSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Caldos cal_Caldos gr_CaldosSUM cal_CaldosSUM.

freq gr_Caldos_percapita cal_Caldos_percapita.

***14 Aceites, grasas y oleaginosas***.

IF (grupos_2006 = 14) gr_Aceite  = gr_dia. 
IF (grupos_2006 = 14) cal_Aceite = Cal_articulo_dia. 

RECODE
  gr_Aceite (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Aceite (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_AceiteSUM= SUM(gr_Aceite).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_AceiteSUM = SUM(cal_Aceite).

COMPUTE gr_Aceite_percapita = gr_AceiteSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Aceite_percapita = cal_AceiteSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Aceite cal_Aceite gr_AceiteSUM cal_AceiteSUM.

freq gr_Aceite_percapita cal_Aceite_percapita.

***15 Yerba, café, té y cocoa en polvo***.

IF (grupos_2006 = 15) gr_Yerba  = gr_dia. 
IF (grupos_2006 = 15) cal_Yerba = Cal_articulo_dia. 

RECODE
  gr_Yerba (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Yerba (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_YerbaSUM= SUM(gr_Yerba).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_YerbaSUM = SUM(cal_Yerba).

COMPUTE gr_Yerba_percapita = gr_YerbaSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Yerba_percapita = cal_YerbaSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Yerba cal_Yerba gr_YerbaSUM cal_YerbaSUM.

freq gr_Yerba_percapita cal_Yerba_percapita.

***16 Otros alimentos***.

IF (grupos_2006 = 16) gr_Otro  = gr_dia. 
IF (grupos_2006 = 16) cal_Otro = Cal_articulo_dia. 

RECODE
  gr_Otro (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Otro (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_OtroSUM= SUM(gr_Otro).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_OtroSUM = SUM(cal_Otro).

COMPUTE gr_Otro_percapita = gr_OtroSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Otro_percapita = cal_OtroSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Otro cal_Otro gr_OtroSUM cal_OtroSUM.

freq gr_Otro_percapita cal_Otro_percapita.

***17 Agua, Refrescos y jugos***.

IF (grupos_2006 = 17) gr_Bebida  = gr_dia. 
IF (grupos_2006 = 17) cal_Bebida = Cal_articulo_dia. 

RECODE
  gr_Bebida (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Bebida (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_BebidaSUM= SUM(gr_Bebida).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_BebidaSUM = SUM(cal_Bebida).

COMPUTE gr_Bebida_percapita = gr_BebidaSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Bebida_percapita = cal_BebidaSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Bebida cal_Bebida gr_BebidaSUM cal_BebidaSUM.

freq gr_Bebida_percapita cal_Bebida_percapita.

***18 Bebidas alcohólicas***.

IF (grupos_2006 = 18) gr_Alcohol  = gr_dia. 
IF (grupos_2006 = 18) cal_Alcohol = Cal_articulo_dia. 

RECODE
  gr_Alcohol (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Alcohol (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_AlcoholSUM= SUM(gr_Alcohol).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_AlcoholSUM = SUM(cal_Alcohol).

COMPUTE gr_Alcohol_percapita = gr_AlcoholSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Alcohol_percapita = cal_AlcoholSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Alcohol cal_Alcohol gr_AlcoholSUM cal_AlcoholSUM.

freq gr_Alcohol_percapita cal_Alcohol_percapita.

***19 Comidas y Bebidas fuera del hogar***.

IF (grupos_2006 = 19) gr_RH  = gr_dia. 
IF (grupos_2006 = 19) cal_RH = Cal_articulo_dia. 

RECODE
  gr_RH (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_RH (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_RHSUM= SUM(gr_RH).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_RHSUM = SUM(cal_RH).

COMPUTE gr_RH_percapita = gr_RHSUM / nper_hogar.
EXECUTE .

COMPUTE cal_RH_percapita = cal_RHSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_RH cal_RH gr_RHSUM cal_RHSUM.

freq gr_RH_percapita cal_RH_percapita.

***20 Programas Sociales.***.

IF (grupos_2006 = 20) gr_Progsociales  = gr_dia. 
IF (grupos_2006 = 20) cal_Progsociales = Cal_articulo_dia. 

RECODE
  gr_Progsociales (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_Progsociales (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_ProgsocialesSUM= SUM(gr_Progsociales).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_ProgsocialesSUM = SUM(cal_Progsociales).

COMPUTE gr_Progsociales_percapita = gr_ProgsocialesSUM / nper_hogar.
EXECUTE .

COMPUTE cal_Progsociales_percapita = cal_ProgsocialesSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_Progsociales cal_Progsociales gr_ProgsocialesSUM cal_ProgsocialesSUM.

freq gr_Progsociales_percapita cal_Progsociales_percapita.

****Refrescos y jugos*****.

IF (grupos_2006 = 17 & GABA_2016 = 8) refrescos = 1. 

RECODE
  refrescos (SYSMIS=0)  .
EXECUTE .

temporary.
select if refrescos = 1. 

SUMMARIZE
  /TABLES=Descripción_CCIF_2016
  /FORMAT=VALIDLIST NOCASENUM TOTAL
  /TITLE='Resúmenes de casos'
  /MISSING=VARIABLE
  /CELLS=COUNT .

**********************************ultraprocesados**********************************************.
***ULTRAPROCESADOS***.

IF (Ultra_mps = 1) gr_ULT  = gr_dia. 
IF (Ultra_mps = 1) cal_ULT = Cal_articulo_dia. 

RECODE
  gr_ULT (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_ULT (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_ULTSUM= SUM(gr_ULT).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_ULTSUM = SUM(cal_ULT).

COMPUTE gr_ultra_percapita = gr_ULTSUM / nper_hogar.
EXECUTE .

COMPUTE cal_ultra_percapita = cal_ULTSUM / nper_hogar.
EXECUTE .
exe.

freq gr_ultra_percapita cal_ultra_percapita.

delete variable gr_ULT  cal_ULT gr_ULTSUM cal_ULTSUM.

COMPUTE prop_ultra_percapita =  cal_ultra_percapita * 100/ Cal_percapita.
EXECUTE .

RECODE
  prop_ultra_percapita (SYSMIS=0)  .
EXECUTE .

* Tablas personalizadas.
CTABLES
  /VLABELS VARIABLES=prop_ultra_percapita DISPLAY=DEFAULT
  /TABLE prop_ultra_percapita [MEAN].

***refrescos y jugos***.

IF (ref_cb = 1) gr_ref_cb  = gr_dia. 
IF (ref_cb= 1) cal_ref_cb = Cal_articulo_dia. 

RECODE
  gr_ref_cb (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_ref_cb (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_ref_cbSUM= SUM(gr_ref_cb).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_ref_cbSUM = SUM(cal_ref_cb).

COMPUTE gr_ref_cb_percapita = gr_ref_cbSUM/ nper_hogar.
EXECUTE .

COMPUTE cal_ref_cb_percapita = cal_ref_cbSUM / nper_hogar.
EXECUTE .
exe.

COMPUTE prop_cal_ref_cb_percapita = cal_ref_cb_percapita * 100 / Cal_percapita.
EXECUTE .
exe.

freq prop_cal_ref_cb_percapita.

delete variable gr_ref_cb  cal_ref_cb cal_ref_cb cal_ref_cbSUM.

freq gr_ref_cb_percapita cal_ref_cb_percapita.

freq gr_refrescos_percapita cal_refrescos_percapita.

***agua_cb***.

IF (agua_cb= 1) gr_agua_cb= gr_dia. 
IF (agua_cb= 1) cal_agua_cb= Cal_articulo_dia. 

RECODE
  gr_agua_cb (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_agua_cb (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_agua_cbSUM= SUM(gr_agua_cb).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_agua_cbSUM = SUM(cal_agua_cb).

COMPUTE gr_agua_cb_percapita = gr_agua_cbSUM/ nper_hogar.
EXECUTE .

COMPUTE cal_agua_cb_percapita = cal_agua_cbSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_agua_cb  cal_agua_cb cal_agua_cb  cal_agua_cbSUM.

freq gr_agua_cb_percapita cal_agua_cb_percapita.

***galletas_cb***.

IF (galletas_cb= 1) gr_galletas_cb= gr_dia. 
IF (galletas_cb= 1) cal_galletas_cb= Cal_articulo_dia. 

RECODE
  gr_galletas_cb (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_galletas_cb (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_galletas_cbSUM= SUM(gr_galletas_cb).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_galletas_cbSUM = SUM(cal_galletas_cb).

COMPUTE gr_galletas_cb_percapita = gr_galletas_cbSUM/ nper_hogar.
EXECUTE .

COMPUTE cal_galletas_cb_percapita = cal_galletas_cbSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_galletas_cb  cal_galletas_cb cal_galletas_cb  cal_galletas_cbSUM.

freq gr_galletas_cb_percapita cal_galletas_cb_percapita.

***alfajores_cb***.

IF (alfajores_cb= 1) gr_alfajores_cb= gr_dia. 
IF (alfajores_cb= 1) cal_alfajores_cb= Cal_articulo_dia. 

RECODE
  gr_alfajores_cb (SYSMIS=0)  .
EXECUTE .

RECODE
  cal_alfajores_cb (SYSMIS=0)  .
EXECUTE .

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /gr_alfajores_cbSUM= SUM(gr_alfajores_cb).

AGGREGATE
  /OUTFILE=*
  MODE=ADDVARIABLES
  /BREAK=NUMERO 
  /cal_alfajores_cbSUM = SUM(cal_alfajores_cb).

COMPUTE gr_alfajores_cb_percapita = gr_alfajores_cbSUM/ nper_hogar.
EXECUTE .

COMPUTE cal_alfajores_cb_percapita = cal_alfajores_cbSUM / nper_hogar.
EXECUTE .
exe.

delete variable gr_alfajores_cb  cal_alfajores_cb cal_alfajores_cb  cal_alfajores_cbSUM.

freq gr_alfajores_cb_percapita cal_alfajores_cb_percapita.


***************************************************generar base final hogar***************************************.

*****BASE DE GASTOS CON NUTRIENTES***.

SAVE OUTFILE='C:\Users\Cecilia\Desktop\Base Engih 2016 marzo 2022\Base de Gastos Engih 2016 con Nutrientes 27 - 03.sav'
 /COMPRESSED.

FILTER OFF.
USE ALL.
SELECT IF(hogar = 1).
EXECUTE .

delete variable DOMMES semana ARTICULOCODIGO DONDECODIGO COMOCODIGO DESTINOCODIGO GASTOTIPO DIVISION VALORCONT VALORCONTM.
delete variable CANTIDADCONVERTIDA_0 VL_IMPUTADO VALORCONT_IMPUTADO CALORIAS FC Calorias_2016 Proteinas_2016.
delete variable Grasas_2016 Hidratos_2016 AGS_2016 AGM_2016 AGP_2016 Na_2016 Fibra_2016 Ca_2016 FE_2016 A_Folico_2016 K_2016 RH_fuerahogar_2016 grupo_vegyfrutas_2016.
exe.
delete variable Azúc_libres_2016 prop_azucarlibre_2016 Azúc_libres_rev GABA_2016 recomendados Descripción_CCIF_2016_msp GABA_msp HT11 Niños_hogar_sum.
exe.
delete variable grupos_2006 Ultra_mps filter_$ sal_2016 DIF_sal hogar CANTIDADCONVERTIDA Calorias_final vegyfrutagr gr_vegyfrutasSUM gr_harinas_percapita cal_harinas_percapita.
exe.
delete variable gr_vegleg_percapita cal_vegleg_percapita gr_fruta_percapita cal_fruta_percapita gr_dulce_percapita cal_dulce_percapita gr_aceite_percapita0 cal_aceite_percapita0 gr_carne_percapita.
delete variable cal_carne_percapita gr_leche_percapita0 cal_leche_percapita0 gr_agua_percapita cal_agua_percapita gr_otro_alim_percapita.  
delete variable cal_otro_alim_percapita gr_alcohol_percapita0 cal_alcohol_percapita0 gr_susedaños_percapita cal_susedaños_percapita.
exe.

delete variable Alimentos Ultra_msp gr_mes gr_dia gr_hogar Cal_articulo_dia gr_proteinas prot_hogar gr_grasas grasas_hogar gr_hidratos hidratos_hogar gr_AGS AGS_hogar cal_AGS gr_azucar_libre azu_hogar.
delete variable cal_azucar_libre azu_libre_per_capita sal_dia sal_gr0 sodio_dia sodio_mg0 fibra_dia fibra_gr0 hierro_dia hierro_mg0 K_dia K_mg0 AF_dia AF_mg0 calcio_dia CA_mg0.
exe.

delete variable Calorias_hogar.

***BASE DE NUTRIENTES A NIVEL HOGAR, SOLO LOS AGREGATE***.

SAVE OUTFILE='C:\Users\Cecilia\Desktop\Base Engih 2016 marzo 2022\Base Consumo Aparente Hogar Engih 2016 new.sav'
 /COMPRESSED.

WEIGHT
  OFF.

freq Niños_hogar.

WEIGHT
  BY peso .

* Tablas personalizadas.
CTABLES
  /VLABELS VARIABLES=REGION Cal_percapita adec_proteinas adec_hidratos adec_grasas adec_AGS sal_gr sodio_mg
  fibra_gr hierro_percapita AF_percapita prop_azucar_libre K_percapita gr_vegyfruta_percapita gr_Pescado_percapita
    DISPLAY=DEFAULT
  /TABLE Cal_percapita [MEAN, MEDIAN] + adec_proteinas [MEAN, MEDIAN] + adec_hidratos [MEAN, MEDIAN] + adec_grasas [MEAN, MEDIAN] +
  adec_AGS [MEAN, MEDIAN] + sal_gr [MEAN, MEDIAN] + sodio_mg [MEAN, MEDIAN] + fibra_gr [MEAN, MEDIAN] + hierro_percapita [MEAN, MEDIAN] + AF_percapita [MEAN, MEDIAN] +
  prop_azucar_libre [MEAN, MEDIAN] + K_percapita [MEAN, MEDIAN] + gr_vegyfruta_percapita [MEAN, MEDIAN] + gr_Pescado_percapita [MEAN, MEDIAN] BY REGION
  /CATEGORIES VARIABLES=REGION ORDER=A KEY=VALUE EMPTY=EXCLUDE TOTAL=YES POSITION=BEFORE.

WEIGHT
  OFF.

*************************************************FIN***************************************************************.
