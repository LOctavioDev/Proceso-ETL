# Proceso ETL con Diferentes Orígenes o Fuentes de Datos (Data Source)

---

### Autor del Proyecto

- **Nombre:** Luis Octavio López Martínez  
- **Matrícula:** 220096  
- **Carrera:** Ingeniería en Desarrollo y Gestión de Software  
- **Materia:** Extracción de Conocimiento en Bases de Datos  

---

## Descripción General

El estudiante aplicará los conceptos del proceso **ETL** (**Extracción, Transformación y Carga de Datos**), utilizando fuentes de datos variadas como APIs públicas, bases de datos relacionales (PostgreSQL) y no relacionales (MongoDB), para demostrar un flujo completo de análisis de datos.

Además, se emplearán herramientas de visualización interactivas como **Dash** y **Bokeh** para representar gráficamente los resultados.

---

## Uso de Docker y PowerShell

- Se utilizaron **contenedores Docker** para levantar las bases de datos PostgreSQL y MongoDB, garantizando entornos reproducibles y portables.
- Los comandos para manejar los contenedores y ejecutar los scripts se automatizaron mediante **PowerShell** con `Invoke-Command` y scripts `.ps1`, facilitando la ejecución desde Windows.
- Esto permite levantar, detener y monitorear fácilmente los servicios de base de datos sin configuraciones complejas en la máquina local.

---

## Visualización de Contenedores Docker

![Contenedores Docker levantados](assets/docker.png)

---

## Tecnologías Utilizadas

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white"/>
  <img src="https://img.shields.io/badge/Dash-000000?style=for-the-badge&logo=plotly&logoColor=white"/>
  <img src="https://img.shields.io/badge/Bokeh-1A1A1A?style=for-the-badge&logo=bokeh&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/PowerShell-012456?style=for-the-badge&logo=powershell&logoColor=white"/>
</p>

---

## Contenido

Este proyecto se divide en tres partes:

1. **Base de Datos Relacional**: Extracción desde PostgreSQL y visualización con Dash.  
2. **API Pública (COVID-19)**: Consumo de datos en tiempo real y visualización con Flask + Bokeh.  
3. **Base de Datos No Relacional (MongoDB)**: Extracción desde Open-Meteo, almacenamiento y visualización con Dash.

Cada módulo incluye su propio script, documentación y visualización.

---
"""

## Actividades

## 1. Base de Datos Relacional (PostgreSQL)

### Archivo principal: `scripts/p1.py`

### Descripción del Script

Este script se conecta a una base de datos relacional **PostgreSQL** utilizando la librería `SQLAlchemy`. Su propósito es extraer, transformar y visualizar artículos de Wikipedia almacenados en la tabla `public.articles`.

---

### Flujo de Trabajo:

1. **Conexión a la base de datos:**
   ```python
   from sqlalchemy import create_engine
   engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5434/wikipedia")
   ```

2. **Extracción de datos:**
   ```python
   import pandas as pd
   query = "SELECT id, url, title, content FROM public.articles"
   df = pd.read_sql(query, engine)
   ```

3. **Transformación de datos:**
   - Eliminación de valores nulos.
   - Filtrado por longitud del contenido.
   - Ordenamiento para mostrar los artículos más extensos.

4. **Visualización con Dash y Plotly:**
   - Histograma de longitud de artículos.
   - Tabla y gráfica de los 10 artículos más largos.

---

### Resultados Visuales

| Histograma de longitud de artículos | Top 10 artículos más largos |
|:-----------------------------------:|:---------------------------:|
| ![Histograma](assets/p1.png)         | ![Top 10](assets/p11.png)   |


## 2. API Pública (COVID-19)

### Archivo principal: `scripts/p2.py`

### Descripción del Script

Este script consume una **API pública de COVID-19** y visualiza los casos confirmados por país en un mapa interactivo. Utiliza **Flask** como servidor web y **Bokeh** para renderizar visualizaciones geográficas dinámicas.

---

### Flujo de Trabajo:

1. **Consumo de la API**:
   - Se obtienen los datos actualizados desde `https://disease.sh/v3/covid-19/countries`.
   - Se transforma la respuesta en un `DataFrame` con `pandas`.

2. **Integración con GeoJSON mundial**:
   - Se descarga un archivo GeoJSON desde GitHub.
   - Se integran los datos de COVID por país mediante el código ISO3.

3. **Visualización con Bokeh**:
   - Se genera un mapa mundial donde el color representa la cantidad de casos.
   - Se personaliza con `HoverTool` para mostrar información por país.

4. **Renderizado con Flask**:
   - El resultado se incrusta dinámicamente en HTML usando `components()` de Bokeh.
   - La visualización se muestra al acceder a la ruta principal `/`.

---

### Visualización

![Visualización API COVID](assets/p3.png)

---

### Librerías Utilizadas

- `requests`: para consumir la API REST
- `pandas`: para manejar y transformar los datos
- `bokeh`: para crear visualizaciones interactivas
- `flask`: servidor web para renderizar el HTML
- `json`: manejo de estructuras GeoJSON

---


---

### Notas

- El script obtiene **datos en vivo**, así que los números cambian con el tiempo.
- El código ISO3 es clave para integrar correctamente los datos en el mapa.
- El mapa está centrado automáticamente y se puede hacer zoom.

---
  

## 3. Extra: Base de Datos No Relacional (MongoDB)

### Extracción, transformación y carga (ETL)

#### Archivo: `scripts/pe.py`

Este script obtiene datos históricos de clima para varias ciudades mexicanas desde la **API pública de Open-Meteo**, los transforma y los carga en una colección de **MongoDB** (`clima.historico`).

---

### Proceso de ETL:

1. **Extracción**:
   - Se hace una petición HTTP a la API de Open-Meteo por ciudad y por fechas.
   - Se obtienen variables como temperatura máxima/mínima, lluvia, viento y UV.

2. **Transformación**:
   - Se formatea cada entrada como documento JSON por día y por ciudad.
   - Se normalizan los nombres y estructuras de los datos.

3. **Carga**:
   - Cada documento se inserta en la colección `historico` dentro de la base de datos `clima`.

---

### Visualización y análisis

#### Archivo: `scripts/pm.py`

Una vez cargados los datos en MongoDB, este segundo script se conecta a la base, limpia los datos y genera visualizaciones con **Dash** y **Plotly**.

---

### Visualización:

- Se muestra un dropdown interactivo para seleccionar ciudad.
- Se grafican las temperaturas máximas y mínimas diarias.
- Se usa `plotly_dark` para un tema oscuro moderno.

---

### Resultados Visuales

| Temperaturas por ciudad (línea) |
|---------------------------------|
| ![Visualización MongoDB](assets/p2.png) |
| ![Visualización MongoDB](assets/p22.png) |

---

### Notas

- La API de Open-Meteo no requiere autenticación y soporta fechas pasadas con precisión diaria.
- MongoDB permite almacenar documentos por ciudad y fecha sin estructura rígida.
- Ideal para practicar un flujo completo de **API → procesamiento → base de datos → visualización**.

---

### Librerías Utilizadas

- `requests`: consumir API de clima
- `pymongo`: conexión y carga de datos a MongoDB
- `dash`, `plotly.express`: visualización web interactiva
- `pandas`: procesamiento de datos
- `json`: conversión estructurada de la API

---

## Herramientas Utilizadas
- **Jupyter Notebook**
- **Python**
- **Librerías:** pandas, sqlalchemy, requests, pymongo, dash, plotly, flask, bokeh, entre otras.

## Objetivo
Desarrollar habilidades prácticas en la manipulación de datos provenientes de diferentes fuentes, aplicando el proceso ETL completo y utilizando herramientas modernas de análisis de datos.


