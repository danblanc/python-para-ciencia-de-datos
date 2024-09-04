# Capítulo 2: Qué es un repositorio de código y un entorno virtual

En este capítulo, exploraremos los conceptos fundamentales de un repositorio de código y el uso de entornos virtuales en Python. Entender cómo gestionar el código y mantener un entorno controlado es esencial para cualquier proyecto de desarrollo, y también en ciencia de datos.

## GIT

### 1. Qué es un repositorio de código

Un repositorio de código es un lugar donde se almacena el código fuente de un proyecto. Los repositorios permiten a los desarrolladores organizar, gestionar, y compartir su código de manera efectiva. Son fundamentales para el desarrollo colaborativo, ya que facilitan la coordinación entre múltiples desarrolladores trabajando en el mismo proyecto. Un repositorio de código puede estar alojado localmente en tu computadora o en una plataforma en la nube, como GitHub.

Los repositorios no solo almacenan el código, sino también el historial de cambios, lo que permite rastrear quién hizo qué cambio y cuándo. Esto es crucial para mantener la integridad del proyecto y para la resolución de conflictos cuando múltiples desarrolladores contribuyen simultáneamente.

### 2. Qué es Git

Git es un sistema de control de versiones distribuido que permite a los desarrolladores rastrear los cambios en el código a lo largo del tiempo. Creado por Linus Torvalds en 2005, Git es una herramienta esencial para el desarrollo de software moderno. Con Git, es posible crear múltiples versiones de un proyecto, trabajar en diferentes ramas de desarrollo, y fusionar cambios de manera segura.

Git permite un flujo de trabajo no lineal, lo que significa que varios desarrolladores pueden trabajar en diferentes partes del código simultáneamente, sin interferir entre sí. Además, Git permite revertir cambios, restaurar versiones anteriores, y crear ramas para probar nuevas características sin afectar el código principal.

![alt text](img/01%20How%20it%20works.svg)

### 3. Por qué usar Git para desarrollo

El uso de Git para el desarrollo tiene numerosos beneficios:

- **Colaboración:** Git facilita el trabajo en equipo, permitiendo que múltiples desarrolladores trabajen en el mismo proyecto sin sobrescribir el trabajo de otros.
- **Control de versiones:** Con Git, puedes rastrear cada cambio hecho en el código, quién lo hizo, y cuándo se hizo, lo que facilita la identificación de errores y la reversión a versiones anteriores si es necesario.
- **Seguridad:** Al mantener un historial completo de cambios, Git permite revertir errores fácilmente, lo que reduce el riesgo de pérdida de datos.
- **Flexibilidad:** Git soporta múltiples flujos de trabajo y permite a los desarrolladores experimentar con nuevas ideas mediante la creación de ramas sin afectar el código de producción.

![alt text](img/02%20Feature%20branches.svg)

### 4. Estructura y lógica de Git

Git organiza los cambios en el código mediante el uso de commits, ramas, y repositorios:

- **Commits:** Un commit en Git es como una "foto" del estado del código en un momento específico. Cada commit tiene un identificador único y registra todos los cambios realizados desde el último commit.
- **Ramas:** Las ramas permiten a los desarrolladores trabajar en diferentes partes de un proyecto al mismo tiempo. La rama principal (o "main") generalmente contiene el código estable, mientras que otras ramas pueden ser utilizadas para desarrollo de nuevas características o corrección de errores.
- **Repositorios:** Un repositorio es el lugar donde se almacena todo el historial del proyecto, incluyendo todas las ramas y commits. Puedes clonar un repositorio para obtener una copia local y trabajar en él desde tu computadora.

![alt text](img/04%20Hotfix%20branches%20(1).svg)

### 5. Qué es GitHub

GitHub es una plataforma de desarrollo colaborativo basada en la web que utiliza Git para el control de versiones. Ofrece a los desarrolladores un lugar para alojar sus repositorios, colaborar con otros, y gestionar proyectos. GitHub no solo permite almacenar y compartir código, sino que también proporciona herramientas para gestionar proyectos, hacer revisiones de código, y documentar el progreso.

Además de ser una plataforma para proyectos de código abierto, GitHub es ampliamente utilizado en la industria para el desarrollo de software privado. Empresas de todo el mundo confían en GitHub para gestionar su código y colaborar en equipo.

### 6. Workshop: Crear una cuenta en GitHub, crear un repositorio y utilizarlo localmente

#### Paso 0: Instalar Git en tu computadora
1. **Windows:**
   - Descarga el instalador de Git desde [git-scm.com](https://git-scm.com/downloads).
   - Sigue las instrucciones del instalador para completar la instalación.
2. **macOS:**
   - Abre la Terminal y escribe el siguiente comando:
     ```bash
     xcode-select --install
     ```
   - Sigue las instrucciones para instalar las herramientas de línea de comandos, que incluyen Git.
3. **Linux:**
   - Abre una terminal y utiliza el gestor de paquetes de tu distribución para instalar Git. Por ejemplo, en Ubuntu:
     ```bash
     sudo apt-get update
     sudo apt-get install git
     ```

#### Paso 1: Crear una cuenta en GitHub
1. Visita [GitHub](https://github.com) y regístrate con un correo electrónico y una contraseña.
2. Sigue las instrucciones para completar tu perfil.

#### Paso 2: Crear un nuevo repositorio
1. Inicia sesión en tu cuenta de GitHub.
2. Haz clic en el botón "New" en la página principal de GitHub.
3. Asigna un nombre a tu nuevo repositorio, agrega una descripción (opcional) y selecciona si quieres que sea público o privado.
4. Haz clic en "Create repository".

#### Paso 3: Utilizar el repositorio localmente
1. Clona el repositorio en tu máquina local utilizando Git:
   ```bash
   git clone https://github.com/tu-usuario/nombre-del-repositorio.git
   ```
2.	Navega al directorio del repositorio clonado y comienza a trabajar en él.

### 7. Ejercicio: Crear una rama, agregar un README.md y hacer un pull request a main

#### Paso 1: Crear una nueva rama

1.	Navega al directorio de tu repositorio local.
2.	Crea una nueva rama:

```bash
git checkout -b nueva-rama
```

#### Paso 2: Agregar un archivo README.md

1.	Crea un archivo README.md en la nueva rama:

```bash
echo "# Mi Proyecto" > README.md
```

2.	Guarda los cambios y haz un commit:

```bash
git add README.md
git commit -m "Agregar README.md"
```

#### Paso 3: Hacer un pull request

1.	Sube la nueva rama a GitHub:
```bash
git push origin nueva-rama
```
2.	Ve a GitHub, navega a tu repositorio, y verás un botón para comparar y hacer un “Pull Request” desde la nueva rama.
3.	Haz clic en “Create Pull Request” y sigue las instrucciones para fusionar los cambios en la rama main.

## Entornos virtuales

### 1. Qué es un entorno virtual

Un entorno virtual en Python es un entorno aislado donde puedes instalar paquetes y librerías sin afectar el sistema global o los otros proyectos en los que estés trabajando. Cada entorno virtual tiene su propia copia del intérprete de Python y una estructura independiente de carpetas donde se almacenan los paquetes instalados. Esto te permite mantener las dependencias separadas entre proyectos, evitando conflictos y problemas de compatibilidad.

Los entornos virtuales son particularmente útiles cuando se trabaja en múltiples proyectos que requieren diferentes versiones de las mismas librerías o incluso de Python mismo.

### 2. Por qué deben usarse entornos virtuales

El uso de entornos virtuales ofrece varios beneficios clave:

- **Aislamiento de dependencias:** Evita que los paquetes de un proyecto interfieran con otros proyectos o con el sistema global de Python.
- **Compatibilidad:** Permite trabajar con diferentes versiones de librerías y de Python, asegurando que cada proyecto tenga el entorno que necesita.
- **Facilidad de despliegue:** Facilita la reproducción de entornos en diferentes máquinas, asegurando que los proyectos funcionen de manera consistente independientemente del entorno de desarrollo.
- **Gestión de proyectos:** Mantiene los proyectos organizados y su entorno de desarrollo limpio y controlado, lo que es crucial para la colaboración en equipo y el despliegue de aplicaciones en producción.

### 3. Workshop: Cómo crear un entorno virtual en Python con `virtualenv`

#### Paso 1: Instalar `virtualenv`
1. Abre una terminal.
2. Instala `virtualenv` usando pip:
   ```bash
   pip install virtualenv
   ```

#### Paso 2: Crear un entorno virtual

1.	Navega al directorio de tu proyecto:

```bash
cd /ruta/a/tu/proyecto
```

2.	Crea un entorno virtual:
```bash
virtualenv nombre_del_entorno
```

#### Paso 3: Activar el entorno virtual

1.	Windows:
```bash 
nombre_del_entorno\Scripts\activate
```

2.	macOS y Linux:
```bash
source nombre_del_entorno/bin/activate
```
#### Paso 4: Instalar dependencias dentro del entorno virtual

1.	Ahora puedes instalar las librerías necesarias utilizando pip, y estas se instalarán solo dentro del entorno virtual:

```bash
pip install nombre_del_paquete
```

#### Paso 5: Desactivar el entorno virtual

1.	Cuando termines de trabajar, puedes desactivar el entorno virtual con el siguiente comando:

```bash
deactivate
```

### 4. VSCode: Qué es, cuál es su estructura, y cómo utilizarlo

#### Qué es VSCode

Visual Studio Code (VSCode) es un editor de código fuente gratuito desarrollado por Microsoft. Es altamente configurable, soporta una amplia variedad de lenguajes de programación, y tiene una gran cantidad de extensiones que mejoran su funcionalidad.

#### Estructura de VSCode

VSCode tiene una interfaz intuitiva que se compone de varias secciones clave:

- Explorador de archivos: Muestra la estructura de tu proyecto, permitiendo navegar fácilmente entre archivos y carpetas.
- Editor de código: La sección principal donde puedes escribir y editar tu código.
- Terminal integrada: Permite ejecutar comandos sin salir del editor.
- Panel de extensiones: Aquí puedes buscar, instalar y gestionar extensiones que amplían la funcionalidad de VSCode.

#### Cómo utilizar VSCode

1.	Abrir un proyecto: Puedes abrir cualquier carpeta como proyecto, lo que permitirá a VSCode indexar todos los archivos y carpetas para una fácil navegación.
2.	Instalar extensiones: Busca extensiones específicas como el soporte para Python, Git, o Jupyter Notebooks para mejorar tu flujo de trabajo.
3.	Configuración: VSCode permite personalizar casi todos los aspectos, desde temas y atajos de teclado hasta configuraciones específicas para diferentes lenguajes.

### 5. Jupyter Notebooks: Qué es, por qué es utilizado en Python, y cómo usarlo a través de VSCode

#### Qué es Jupyter Notebooks

Jupyter Notebooks es una aplicación web que permite crear y compartir documentos que contienen código en vivo, ecuaciones, visualizaciones y texto explicativo. Es ampliamente utilizado en ciencia de datos por su capacidad de combinar código ejecutable con narrativas explicativas, gráficos, y visualizaciones en un solo documento.

#### Por qué es utilizado en Python

- Interactividad: Permite ejecutar bloques de código y ver los resultados inmediatamente, lo que es ideal para exploración de datos, pruebas rápidas, y desarrollo iterativo.
- Documentación: Facilita la creación de documentos explicativos que pueden incluir gráficos y resultados junto con el código que los genera.
- Compartibilidad: Los notebooks pueden ser compartidos fácilmente y ejecutados en diferentes entornos, lo que los hace perfectos para la colaboración.

#### Cómo usar Jupyter Notebooks a través de VSCode

1. Instalar la extensión de Jupyter en VSCode: Abre el panel de extensiones, busca “Jupyter” e instálalo.
2. Abrir un notebook: Puedes abrir el ejemplo `jupyter_example.ipynb` o crear un nuevo notebook .ipynb directamente en VSCode.
3. Configurar el entorno: Asegúrate de que el entorno virtual adecuado esté seleccionado como el kernel de Python en VSCode.

### 6. Workshop: Instalación del plugin de Jupyter en VSCode y configuración de entorno virtual como kernel

#### Paso 1: Instalar la extensión de Jupyter en VSCode

1. Abre VSCode y dirígete al panel de extensiones.
2. Busca “Jupyter” y haz clic en “Instalar”.

#### Paso 2: Crear un nuevo notebook o abrir uno existente

1. Puedes crear un nuevo archivo con extensión .ipynb o abrir un notebook existente desde el explorador de archivos en VSCode.

#### Paso 3: Seleccionar el entorno virtual como kernel

1. Abre el notebook en VSCode.
2. Haz clic en la esquina superior derecha donde se selecciona el kernel.
3. Elige el entorno virtual que has creado previamente como el kernel para ejecutar el código.

### 7. Ejercicio: Crear un entorno virtual y usarlo como kernel en tu Jupyter Notebook

1. Crear un entorno virtual:
- Crea un entorno virtual usando virtualenv, siguiendo los pasos anteriores.
2. Activar el entorno virtual:
- Activa el entorno virtual en tu terminal.
3. Descarga un paquete:
- Descarga el paquete `matplotlib` utilizando 
```bash
pip install matplotlib
```
4. Ejecuta el script:
- Corre el script de ejemplo `statistical_example.py` utilizando
```bash
python tu-carpeta/statistical_example.py
```
- Debería aparecer un pop-up con una gráfica tridimensional
5. Configurar el kernel:
- Abre VSCode, abre un Jupyter Notebook y selecciona tu entorno virtual como kernel.
6. Escribir y ejecutar código:
- Escribe el mismo código que está en `statistical_example.py` y corre el bloque, deberías obtener el mismo resultado que ejecutándolo en consola.
7. Agregar tu entorno virtual al repositorio
- Agrega la carpeta de tu entorno virtual a tu repositorio, además de tus archivos modificados, luego de crear una rama llamada `feature/entorno-virtual`.
8. Pushea la rama al repositorio github en la nube y haz un pull request
- Mergea la nueva rama con `main`.