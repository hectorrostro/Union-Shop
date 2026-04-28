import json
from pymongo import MongoClient

# Cambia esto por tu connection string
MONGO_URI = "mongodb+srv://hector2871_db_user:union1234@test.v6fh5uo.mongodb.net/unionshop?appName=Test"

client = MongoClient(MONGO_URI)
db = client["unionshop"]

# Limpiar colección antes de importar
db["productos"].drop()
print("Colección 'productos' limpiada.")

# Cargar productos.json
with open("productos.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Insertar cada tienda como un documento
documentos = []
for planta, tiendas in data.items():
    for tienda, contenido in tiendas.items():
        doc = {
            "planta": planta,
            "tienda": tienda,
            "productos": contenido["productos"]
        }
        documentos.append(doc)

db["productos"].insert_many(documentos)
print(f"Importados {len(documentos)} documentos a Atlas.")

# Verificar
for doc in db["productos"].find({}, {"_id": 0, "planta": 1, "tienda": 1}):
    print(f"  ✓ {doc['planta']} - {doc['tienda']}")

print("\n¡Importación completada!")
