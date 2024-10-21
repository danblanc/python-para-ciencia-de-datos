# Python para Ciencia de Datos - Proyecto Final


## Problema a resolver
Búsqueda e identificación de inconsistencias en variaciones y/o incidencias de precios luego de procesado el cálculo mensual y/o semanal

## El origen y razón de los datos que maneja
Sistema de recolección y cálculo del Indice de Precios al Consumo.
Tablas con información desagregada de números Indice, Variaciones e Incidencias.
Información Disponible de Octubre/2022 a Noviembre/2024

## La solución planteada
La solución consiste en un dashboard que incluye una serie de filtros temporales y categorizados. Estos filtros permiten generar dos tipos de visualización: una salida en forma de tabla y otras dos en formato gráfico.
Al aplicar los filtros se podrán ver en la tabla aquellos items que cumplan con las condiciones establecidas y en las gráficas la variación Anual(solo Divisiones) y/o Mensual para cada uno de los items.
En el gráfico es posible activar o desactivar los items según el análisis requerido.
Al realizar diferentes combinaciones de filtros, es posible comparar información y detectar inconsistencias en variaciones.

#### Ejemplo
Filtros: Año=2023, Mes=10, Nivel=DIVISION, Región=TOTAL_PAIS , Variación mensual=1
Resultado: 
    1. Tabla de datos con dos registros de las divisiones Ropa y Calzado y Transporte. Son las divisiones que tienen una variación positiva >= 1
    2. Grafica de variación Anual de cada división entre los meses 10(filtro) de los años 2022 2023 y 2024.
    2. Grafica de variación Mensual de cada división entre todos los meses del año 2023(filtro).


### Equipo de Proyecto
Carlos Rodriguez, Edinson Alvite
