from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime
import json
import os

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["unionshop"]

ruta_productos = "productos.json"
ruta_carrito = "carrito.json"


def cargar_centro():
    centro = {}
    for doc in db["productos"].find():
        planta = doc["planta"]
        tienda = doc["tienda"]
        if planta not in centro:
            centro[planta] = {}
        centro[planta][tienda] = {"productos": doc["productos"]}
    return centro


def guardar_tienda(planta, tienda, productos):
    db["productos"].update_one(
        {"planta": planta, "tienda": tienda},
        {"$set": {"productos": productos}}
    )
    centro_actual = cargar_centro()
    with open(ruta_productos, "w", encoding="utf-8") as f:
        json.dump(centro_actual, f, ensure_ascii=False, indent=4)


def cargar_carrito():
    doc = db["carrito"].find_one({"_id": "carrito"})
    if doc:
        return doc["productos"]
    return []


def guardar_carrito(carrito):
    db["carrito"].update_one(
        {"_id": "carrito"},
        {"$set": {"productos": carrito}},
        upsert=True
    )
    with open(ruta_carrito, "w", encoding="utf-8") as f:
        json.dump(carrito, f, ensure_ascii=False, indent=4)


centro = cargar_centro()
carrito = cargar_carrito()


@app.get("/")
def inicio():
    return {"mensaje": "UnionShop Centro Comercial"}


@app.get("/plantas")
def obtener_plantas():
    return list(centro.keys())


@app.get("/plantas/{planta}/tiendas")
def obtener_tiendas(planta: str):
    if planta not in centro:
        raise HTTPException(status_code=404, detail="Planta no encontrada")
    return list(centro[planta].keys())


@app.get("/plantas/{planta}/tiendas/{tienda}/productos")
def obtener_productos(planta: str, tienda: str):
    try:
        return centro[planta][tienda]["productos"]
    except KeyError:
        raise HTTPException(status_code=404, detail="Tienda o productos no encontrados")


@app.post("/carrito")
def añadir_carrito(planta: str, tienda: str, indice: int, cantidad: int = 1):
    try:
        producto = centro[planta][tienda]["productos"][indice]
        stock_disponible = producto["stock"]
        if cantidad < 1:
            raise HTTPException(status_code=400, detail="Cantidad no valida")
        if cantidad > stock_disponible:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente, disponible: {stock_disponible}")
        carrito.append([producto["nombre"], producto["precio"], cantidad])
        producto["stock"] -= cantidad
        guardar_tienda(planta, tienda, centro[planta][tienda]["productos"])
        guardar_carrito(carrito)
        return {"mensaje": "Producto añadido", "producto": producto["nombre"], "cantidad": cantidad}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Error al añadir producto")


@app.get("/carrito")
def ver_carrito():
    total = sum(p[1] * p[2] for p in carrito)
    productos = [{"nombre": p[0], "precio": p[1], "cantidad": p[2], "subtotal": p[1] * p[2]} for p in carrito]
    return {"productos": productos, "total": total}


@app.delete("/carrito")
def vaciar_carrito():
    carrito.clear()
    guardar_carrito(carrito)
    return {"mensaje": "Carrito vaciado"}


@app.post("/confirmar_compra")
def confirmar_compra():
    if len(carrito) == 0:
        raise HTTPException(status_code=400, detail="El carrito esta vacio")

    total = sum(p[1] * p[2] for p in carrito)

    pedido = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "productos": carrito.copy(),
        "total": total
    }

    db["pedidos"].insert_one(pedido)
    carrito.clear()
    guardar_carrito(carrito)

    return {"mensaje": "Compra confirmada", "total": total}


@app.get("/pedidos")
def ver_pedidos():
    pedidos = []
    for doc in db["pedidos"].find():
        doc.pop("_id")
        pedidos.append(doc)
    return pedidos


@app.post("/admin/producto")
def añadir_producto(planta: str, tienda: str, nombre: str, precio: float, stock: int = 10):
    if planta not in centro or tienda not in centro[planta]:
        raise HTTPException(status_code=404, detail="Planta o tienda no encontrada")
    nuevo = {"nombre": nombre, "precio": precio, "stock": stock}
    centro[planta][tienda]["productos"].append(nuevo)
    guardar_tienda(planta, tienda, centro[planta][tienda]["productos"])
    return {"mensaje": "Producto añadido", "producto": nuevo}


@app.delete("/admin/producto")
def eliminar_producto(planta: str, tienda: str, indice: int):
    try:
        productos = centro[planta][tienda]["productos"]
        eliminado = productos.pop(indice)
        guardar_tienda(planta, tienda, productos)
        return {"mensaje": "Producto eliminado", "producto": eliminado}
    except Exception:
        raise HTTPException(status_code=400, detail="Error al eliminar producto")


@app.put("/admin/precio")
def cambiar_precio(planta: str, tienda: str, indice: int, nuevo_precio: float):
    try:
        centro[planta][tienda]["productos"][indice]["precio"] = nuevo_precio
        guardar_tienda(planta, tienda, centro[planta][tienda]["productos"])
        return {"mensaje": "Precio actualizado"}
    except Exception:
        raise HTTPException(status_code=400, detail="Error al actualizar precio")


@app.put("/admin/stock")
def cambiar_stock(planta: str, tienda: str, indice: int, nuevo_stock: int):
    try:
        centro[planta][tienda]["productos"][indice]["stock"] = nuevo_stock
        guardar_tienda(planta, tienda, centro[planta][tienda]["productos"])
        return {"mensaje": "Stock actualizado"}
    except Exception:
        raise HTTPException(status_code=400, detail="Error al actualizar stock")