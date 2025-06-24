import pandas as pd
from io import StringIO

archivo_original = "data/salaries.csv" 

nuevos_datos = """
work_year,experience_level,employment_type,job_title,salary,salary_currency,salary_in_usd,employee_residence,remote_ratio,company_location,company_size
2021,MI,FT,Data Scientist,,SGD,119059,SG,100,IL,M
2021,MI,FT,Applied Machine Learning Scientist,,USD,423000,US,50,US,L
2021,MI,FT,Data Engineer,,EUR,28369,MT,50,MT,L
2021,SE,FT,Data Specialist,,USD,165000,US,100,US,L
2020,SE,FT,Data Scientist,,USD,412000,US,100,US,L
2021,MI,FT,Principal Data Scientist,,USD,151000,US,100,US,L
2020,EN,FT,Data Scientist,,USD,105000,US,100,US,S
2020,EN,CT,Business Data Analyst,,USD,100000,US,100,US,L
2021,SE,FT,Data Scientist,,INR,94665,IN,50,IN,L
2021,SE,FT,Data Engineer,,USD,130000,US,100,US,M
"""

df_original = pd.read_csv(archivo_original)

df_nuevos = pd.read_csv(StringIO(nuevos_datos))

df_completo = pd.concat([df_original, df_nuevos], ignore_index=True)

df_completo.to_csv("datos_actualizados.csv", index=False)

print("Listo. Se agregaron 10 entidades con salario vacío.")
