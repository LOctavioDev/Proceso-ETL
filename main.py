# # Análisis de salarios en Estados Unidos (2023+)
# Este script realiza un análisis de los salarios de empleos de tiempo completo en Estados Unidos desde el año 2023, utilizando datos de un archivo CSV.

# ## Importación de librerías
# Se importan las librerías necesarias para el análisis y visualización de datos.
# Realizado por: **Luis Octavio Lopez Martinez** - 220096

print("\n--- 1. Importación de librerías y paquetes ---\n")
## 1. Importacion de las librerias y Paquetes a utilizar para el analisis de datos.
import numpy as np
import pandas as pd
import time

##Graficadores
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

print("\n--- 2. Carga de datos y consulta del DataFrame ---\n")
# ## Carga de datos
# Se carga el archivo `salaries.csv` y se muestra información básica del DataFrame.
## 2. Ubicacion de los datos

## 3. Construccion y consulta del Dataframe
df = pd.read_csv("datos_actualizados.csv")

print("\nInformación del DataFrame:")
print(df.info())
print("\nTamaño total de celdas:", df.size)
print("Cantidad de filas:", len(df))
print("\nPrimeras 5 filas:")
print(df.head())
print("\nÚltimas 5 filas:")
print(df.tail())


print("\n--- 3. Limpieza de datos previo al análisis ---\n")
# 4. Limpieza de datos previo al análisis
# Eliminación de datos duplicados

df_noDuplicated = df.drop_duplicates()
print("Tamaño del DataFrame original:", len(df))
print("Tamaño del DataFrame sin duplicados:", len(df_noDuplicated))
print("Registros/Tuplas eliminados:", len(df) - len(df_noDuplicated))

print("\nEliminando filas con valores NaN...")
# Eliminar datos de las filas con un salario vacio
df_clean = df.dropna()
print("Tamaño del DataFrame original:", len(df))
print("Tamaño del DataFrame sin NaN:", len(df_clean))
print("Registros/Tuplas eliminados:", len(df) - len(df_clean))
print("\nDescripción estadística tras limpieza:")
print(df.describe())


df.isnull()  # mapping de la matriz de datos, True si es NaN, False si no es NaN

print("\nEliminando filas con salario vacío...")
# eliminar campos con salario vacio
df_clean = df_clean[df_clean["salary"] != ""]
print("Tamaño del DataFrame original:", len(df))
print("Tamaño del DataFrame con salarios vacíos eliminados:", len(df_clean))
print("Registros/Tuplas eliminados:", len(df) - len(df_clean))

df.notnull()  # Realiza el mapeo con la matriz original colocando valores boleanos de acuerdo a la condicion es nulo

print("\n--- 4. Análisis básico del DataFrame (Datos estadísticos generales) ---\n")
print(df.describe())

## 5. Definir criterios de analisis (Categories)


analysis_cryteria = [
    "work_year",
    "experience_level",
    "employment_type",
    "job_title",
    "employee_residence",
    "company_location",
    "company_size",
]


df_clean = df.dropna()

print(f"\n========{df_clean['experience_level'].unique()}========")
print(f"\n========{df_clean.info()}========")
df_clean.hist(column="work_year")
plt.xlabel("Año de trabajo")
plt.ylabel("Frecuencia")
plt.title("Histograma de work_year")

# Mostrar los valores arriba de las barras
n, bins, patches = plt.hist(df_clean["work_year"], alpha=0)  # alpha=0 para no dibujar barras extra
for i in range(len(patches)):
    plt.text(
        patches[i].get_x() + patches[i].get_width() / 2,
        n[i],
        int(n[i]),
        ha='center', va='bottom', fontsize=10, color='black'
    )
plt.show()

def_color = "darkblue"
print("\n--- 5. Gráficas básicas por categoría ---\n")
for f in analysis_cryteria:
    print(f"\nGráfica de la categoría: {f}")
    plt.figure(figsize=(12, 3))
    df[f].value_counts().plot(kind="bar", color=def_color)
    plt.title(f)
    plt.grid()
    plt.show()

print("\n--- 6. Filtrado de datos: empleados FT en US desde 2023 y en México ---\n")
# ## 6. Limpiamos los datos para enfocarnos en los datos recolectados desde 2023, empleados de tiempo completo(Full time) en EU/US


# Creamos un subconjunto de la muetsra original

df_after2023 = df[
    (df.work_year >= 2023)
    & (df.employment_type == "FT")
    & (df.company_location == "US")
]
df_mex = df[(df.company_location == "MX")]

# Revisamos los metadatos de la nueva entrada

print("\nInfo de empleados FT en US desde 2023:")
print(df_after2023.info())
print("\nInfo de empleados en México:")
print(df_mex.info())
print("\nTamaño del subconjunto US:", df_after2023.size)
print("Cantidad de empleados US:", len(df_after2023))
print("Cantidad de empleados MX:", len(df_mex))
print("Tamaño de empleados fuera de US:", len(df) - len(df_after2023))
print(df_after2023.employee_residence.value_counts())

# Mostrar la distribucion del trabajo remoto
plt.figure(figsize=(7,3))
df_after2023.remote_ratio.value_counts().sort_index().plot(kind='bar', color=def_color)
plt.title('Distribucion de modalidad de trabajo para las empresas Estadounidenses')
plt.grid()
plt.show()



analysis_salary = ["salary_in_usd"]
def_color = "darkblue"
print("\n--- 7. Gráfica de grupos salariales (US FT 2023+) ---\n")
for f in analysis_salary:
    print(f"\nGráfica de grupo salarial para: {f}")
    plt.figure(figsize=(12, 3))
    bins = [0, 100000, 250000, df_after2023[f].max()]
    labels = ["Bajo (<60k)", "Medio (60k-100k)", "Alto (>100k)"]
    df_after2023["salary_group"] = pd.cut(
        df_after2023[f], bins=bins, labels=labels, include_lowest=True
    )
    df_after2023["salary_group"].value_counts().sort_index().plot(
        kind="bar", color=def_color
    )
    plt.title(f)
    plt.xlabel("Grupo de salario")
    plt.ylabel("Cantidad de empleados")
    plt.grid()
    plt.show()

print("\n--- 8. Reemplazo de valores nulos por 'N/A' ---\n")
df_valoresNulosSustituidos = df.fillna(
    value="N/A"
)  # javascript es nan y python es none
print(df_valoresNulosSustituidos.head())

print("\n--- 9. Descripción tras reemplazo de nulos ---\n")
print(df_valoresNulosSustituidos.describe())

print("\n--- 10. Sustitución de nulos por 0 en salario ---\n")
df_clean = df.fillna({"salary": 0.0, "salary_in_usd": 0.0})
print(df_clean.describe())

print("\n--- 11. Limpieza de datos con valores erróneos en 'experience_level' ---\n")
print(df["experience_level"].unique())

print("\nTotales por categoría 'experience_level':")
print(df["experience_level"].value_counts(dropna=False))

print("\n--- 12. Gráfica de total de ganancias por grupo salarial ---\n")
plt.figure(figsize=(10, 4))
df["salary_in_usd"] = pd.to_numeric(df["salary_in_usd"], errors="coerce")
bins = [0, 100000, 250000, df["salary_in_usd"].max()]
labels = ["0-100k", "101k-250k", "250k+"]
df["salary_group"] = pd.cut(
    df["salary_in_usd"], bins=bins, labels=labels, include_lowest=True
)
df["salary_group"].value_counts().sort_index().plot(kind="bar", color=def_color)
plt.title("Total de ganancias por grupo salarial")
plt.xlabel("Grupo salarial (USD)")
plt.ylabel("Cantidad de empleados")
plt.grid()
plt.show()
