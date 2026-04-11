from pymongo import MongoClient
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta = os.path.join(BASE_DIR, "..", "productos.json")

client = MongoClient("mongodb://localhost:27017/")
db = client["unionshop"]

with open(ruta, "r", encoding="utf-8") as f:
    centro = json.load(f)

for planta, tiendas in centro.items():
    for tienda, datos in tiendas.items():
        db["productos"].insert_one({
            "planta": planta,
            "tienda": tienda,
            "productos": datos["productos"]
        })

print("Datos importados correctamente")
