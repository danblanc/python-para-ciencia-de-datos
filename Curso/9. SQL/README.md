### **Módulo: Introducción a SQL**

**SQL** (Structured Query Language) es el lenguaje estándar para interactuar con bases de datos relacionales. Permite realizar operaciones como consultar, insertar, actualizar y eliminar datos, así como definir la estructura de la base de datos.

En este módulo, exploraremos los conceptos fundamentales de SQL, sus diferentes tipos y la estructura básica de las consultas, y nos enfocaremos en el uso del comando `SELECT` y otras operaciones esenciales.

---

### **1. ¿Qué es SQL?**

SQL es un lenguaje de programación diseñado para gestionar y manipular bases de datos relacionales. Permite a los usuarios ejecutar consultas para obtener información de una base de datos, modificar datos y definir la estructura de la base.

#### **Principales Usos de SQL:**
- **Consulta de Datos**: Obtener información almacenada en la base de datos.
- **Modificación de Datos**: Insertar, actualizar o eliminar registros.
- **Definición de Datos**: Crear y modificar la estructura de las tablas y las relaciones entre ellas.
- **Control de Acceso**: Gestionar permisos y roles de usuarios en la base de datos.

---

### **2. Tipos de SQL**

SQL se divide en varias categorías según el tipo de operación que se realiza. Estas son las más importantes:

#### **a. DDL (Data Definition Language):**
DDL se utiliza para definir la estructura de la base de datos, incluyendo tablas, columnas, índices y relaciones.

- **Comandos Principales:**
  - `CREATE`: Crea una nueva tabla o base de datos.
  - `ALTER`: Modifica la estructura de una tabla existente.
  - `DROP`: Elimina una tabla o base de datos.

**Ejemplo:**
```sql
CREATE TABLE empleados (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    salario DECIMAL(10, 2)
);
```

#### **b. DML (Data Manipulation Language):**
DML se utiliza para manipular los datos dentro de las tablas.

- **Comandos Principales:**
  - `INSERT`: Inserta nuevos registros en una tabla.
  - `UPDATE`: Actualiza registros existentes.
  - `DELETE`: Elimina registros de una tabla.

**Ejemplo:**
```sql
INSERT INTO empleados (id, nombre, salario)
VALUES (1, 'Juan Pérez', 3500.50);
```

#### **c. DQL (Data Query Language):**
DQL se utiliza para consultar datos de las tablas. El comando principal es `SELECT`.

**Ejemplo:**
```sql
SELECT nombre, salario
FROM empleados;
```

#### **d. DCL (Data Control Language):**
DCL se utiliza para controlar el acceso a los datos en la base de datos.

- **Comandos Principales:**
  - `GRANT`: Otorga permisos a los usuarios.
  - `REVOKE`: Revoca permisos de los usuarios.

**Ejemplo:**
```sql
GRANT SELECT ON empleados TO usuario1;
```

#### **e. TCL (Transaction Control Language):**
TCL gestiona las transacciones dentro de la base de datos.

- **Comandos Principales:**
  - `COMMIT`: Confirma una transacción.
  - `ROLLBACK`: Revierte una transacción.

**Ejemplo:**
```sql
BEGIN;
UPDATE empleados SET salario = salario * 1.10 WHERE id = 1;
COMMIT;
```

---

### **3. Estructura de una Consulta SQL**

Una consulta SQL sigue una estructura básica que consta de varias cláusulas opcionales. La estructura más común es:

```sql
SELECT columnas
FROM tabla
WHERE condición
GROUP BY columnas
HAVING condición
ORDER BY columnas
LIMIT número;
```

- **SELECT**: Especifica las columnas que se desean mostrar.
- **FROM**: Indica la tabla de donde provienen los datos.
- **WHERE**: Filtra los registros según una condición.
- **GROUP BY**: Agrupa registros que tienen valores idénticos en columnas especificadas.
- **HAVING**: Filtra grupos de registros según una condición.
- **ORDER BY**: Ordena los resultados de la consulta.
- **LIMIT**: Limita el número de filas devueltas.

---

### **4. El Comando `SELECT`**

El comando `SELECT` es la base de cualquier consulta SQL. Permite especificar qué columnas y datos se desean extraer de las tablas.

#### **Sintaxis Básica:**
```sql
SELECT columna1, columna2
FROM tabla
WHERE condición;
```

#### **Ejemplo:**
```sql
SELECT nombre, salario
FROM empleados
WHERE salario > 3000;
```

#### **Alias en SQL:**
Los alias se utilizan para renombrar columnas o tablas temporalmente dentro de una consulta.

**Ejemplo con Alias:**
```sql
SELECT nombre AS empleado, salario AS sueldo
FROM empleados;
```

---

### **5. Filtros en SQL (Cláusula `WHERE`)**

La cláusula `WHERE` se utiliza para filtrar los registros que cumplen con ciertas condiciones.

#### **Operadores Comunes:**
- **`=`**: Igual a.
- **`<>` o `!=`**: Distinto de.
- **`>` o `<`**: Mayor o menor que.
- **`BETWEEN`**: Dentro de un rango.
- **`LIKE`**: Coincidencia de patrones.
- **`IN`**: Coincidencia con una lista de valores.

#### **Ejemplo:**
```sql
SELECT nombre, salario
FROM empleados
WHERE salario BETWEEN 3000 AND 5000;
```

---

### **6. Agrupación de Datos (`GROUP BY`)**

La cláusula `GROUP BY` se utiliza para agrupar filas que tienen valores idénticos en una o más columnas. A menudo se usa junto con funciones agregadas como `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`.

#### **Ejemplo:**
```sql
SELECT departamento, AVG(salario) AS salario_promedio
FROM empleados
GROUP BY departamento;
```

---

### **7. Transformación y Creación de Columnas**

Se pueden crear nuevas columnas en una consulta usando expresiones y funciones. Esto permite transformar los datos en tiempo real.

#### **Ejemplo:**
```sql
SELECT nombre,
       salario,
       salario * 1.10 AS nuevo_salario
FROM empleados;
```

---

### **8. `CASE` Statement en SQL**

La sentencia `CASE` se utiliza para realizar operaciones condicionales dentro de una consulta SQL.

#### **Sintaxis:**
```sql
SELECT columna,
       CASE
           WHEN condición1 THEN resultado1
           WHEN condición2 THEN resultado2
           ELSE resultado_default
       END AS nombre_columna
FROM tabla;
```

#### **Ejemplo:**
```sql
SELECT nombre,
       salario,
       CASE
           WHEN salario > 4000 THEN 'Alto'
           WHEN salario BETWEEN 2000 AND 4000 THEN 'Medio'
           ELSE 'Bajo'
       END AS rango_salarial
FROM empleados;
```

---

### **Conclusión**

SQL es un lenguaje esencial para trabajar con bases de datos, permitiendo a los usuarios consultar, manipular y estructurar datos de manera eficiente. Con este módulo, hemos cubierto las bases del lenguaje SQL, explorando sus distintos tipos, la estructura de las consultas y cómo utilizar el comando `SELECT` junto con cláusulas y transformaciones para extraer y manipular datos de manera efectiva.