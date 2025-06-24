import requests
import pymongo

# Conectar a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["clima"]
collection = db["historico"]

# Lista de ciudades
ciudades = [
    {"nombre": "CDMX", "lat": 19.43, "lon": -99.13},
    {"nombre": "Monterrey", "lat": 25.67, "lon": -100.31},
    {"nombre": "Guadalajara", "lat": 20.67, "lon": -103.35},
    {"nombre": "Cancún", "lat": 21.16, "lon": -86.85},
]

# comunes
start_date = "2024-06-01"
end_date = "2024-06-10"
variables = "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,uv_index_max"

for ciudad in ciudades:
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={ciudad['lat']}&longitude={ciudad['lon']}&start_date={start_date}&end_date={end_date}&daily={variables}&timezone=America%2FMexico_City"
    res = requests.get(url)
    data = res.json()

    for i in range(len(data["daily"]["time"])):
        doc = {
            "ciudad": ciudad["nombre"],
            "fecha": data["daily"]["time"][i],
            "temp_max": data["daily"]["temperature_2m_max"][i],
            "temp_min": data["daily"]["temperature_2m_min"][i],
            "lluvia_mm": data["daily"]["precipitation_sum"][i],
            "viento_max_kmh": data["daily"]["windspeed_10m_max"][i],
            "uv_index": data["daily"]["uv_index_max"][i],
        }
        collection.insert_one(doc)

print("Datos insertados correctamente para todas las ciudades.")
