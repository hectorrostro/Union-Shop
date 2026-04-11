from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()

ruta = "productos.json"
ruta_carrito = "carrito.json"

def cargar_datos():
    if not os.path.exists(ruta):
        return {}
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(data):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def cargar_carrito():
    if not os.path.exists(ruta_carrito):
        return []
    with open(ruta_carrito, "r", encoding="utf-8") as f:
        contenido = f.read().strip()
        if not contenido:
            return []
        return json.loads(contenido)

def guardar_carrito(carrito):
    with open(ruta_carrito, "w", encoding="utf-8") as f:
        json.dump(carrito, f, ensure_ascii=False, indent=4)

centro = cargar_datos()
carrito = cargar_carrito()

@app.get("/")
def inicio():
    return {"mensaje": "UnionShop Centro Comercial U$"}

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
        guardar_datos(centro)
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

@app.post("/admin/producto")
def añadir_producto(planta: str, tienda: str, nombre: str, precio: float, stock: int = 10):
    if planta not in centro or tienda not in centro[planta]:
        raise HTTPException(status_code=404, detail="Planta o tienda no encontrada")

    nuevo = {"nombre": nombre, "precio": precio, "stock": stock}
    centro[planta][tienda]["productos"].append(nuevo)
    guardar_datos(centro)

    return {"mensaje": "Producto añadido", "producto": nuevo}

@app.delete("/admin/producto")
def eliminar_producto(planta: str, tienda: str, indice: int):
    try:
        eliminado = centro[planta][tienda]["productos"].pop(indice)
        guardar_datos(centro)
        return {"mensaje": "Producto eliminado", "producto": eliminado}
    except Exception:
        raise HTTPException(status_code=400, detail="Error al eliminar producto")

@app.put("/admin/precio")
def cambiar_precio(planta: str, tienda: str, indice: int, nuevo_precio: float):
    try:
        centro[planta][tienda]["productos"][indice]["precio"] = nuevo_precio
        guardar_datos(centro)
        return {"mensaje": "Precio actualizado"}
    except Exception:
        raise HTTPException(status_code=400, detail="Error al actualizar precio")

@app.put("/admin/stock")
def cambiar_stock(planta: str, tienda: str, indice: int, nuevo_stock: int):
    try:
        centro[planta][tienda]["productos"][indice]["stock"] = nuevo_stock
        guardar_datos(centro)
        return {"mensaje": "Stock actualizado"}
    except Exception:
        raise HTTPException(status_code=400, detail="Error al actualizar stock")