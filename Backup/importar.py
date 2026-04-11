from pymongo import MongoClient
import json

ruta = r"C:\Users\Hector\Desktop\Clase\Lenguaje Phyton\Trabajos\TFG\Centro Comercial\productos.json"

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