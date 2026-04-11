import json
import os
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["unionshop"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_carrito = os.path.join(BASE_DIR, "carrito.json")


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


def cargar_carrito():
    doc = db["carrito"].find_one({"_id": "carrito"})
    if doc:
        return doc["productos"]
    return []


def guardar_carrito():
    db["carrito"].update_one(
        {"_id": "carrito"},
        {"$set": {"productos": carrito}},
        upsert=True
    )
    with open(ruta_carrito, "w", encoding="utf-8") as f:
        json.dump(carrito, f, ensure_ascii=False, indent=4)


def confirmar_compra():
    if len(carrito) == 0:
        print("\nEl carrito esta vacio")
        return

    total = sum(p[1] * p[2] for p in carrito)

    pedido = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "productos": carrito.copy(),
        "total": total
    }

    db["pedidos"].insert_one(pedido)
    carrito.clear()
    guardar_carrito()
    print("\nCompra confirmada! Total:", total, "€")


centro = cargar_centro()
carrito = cargar_carrito()


def menu():
    print("\nMENU")
    print("1. Planta Baja")
    print("2. Planta 1")
    print("3. Planta 2")
    print("4. Ver carrito")
    print("5. Confirmar compra")
    print("6. Vaciar carrito")
    print("7. Modo administrador")
    print("8. Salir")


def elegir_tienda(planta):
    tiendas = list(centro[planta].keys())

    print("\nTIENDAS EN", planta)

    for i in range(len(tiendas)):
        print(i + 1, ".", tiendas[i])

    try:
        opcion = int(input("Elige tienda (0 para salir): "))
    except ValueError:
        print("Por favor introduce un numero")
        return

    if opcion >= 1 and opcion <= len(tiendas):
        tienda = tiendas[opcion - 1]
        entrar_tienda(planta, tienda)
    elif opcion != 0:
        print("Opcion no valida")


def entrar_tienda(planta, tienda):
    datos = centro[planta][tienda]
    productos = datos["productos"]

    while True:
        print("\nTienda:", tienda)

        for i in range(len(productos)):
            print(i + 1, ".", productos[i]["nombre"], "-", productos[i]["precio"], "€", "- Stock:", productos[i]["stock"])

        try:
            opcion = int(input("Elige producto (0 para salir): "))
        except ValueError:
            print("Por favor introduce un numero")
            continue

        if opcion == 0:
            break
        elif opcion >= 1 and opcion <= len(productos):
            nombre = productos[opcion - 1]["nombre"]
            precio = productos[opcion - 1]["precio"]
            stock_disponible = productos[opcion - 1]["stock"]
            try:
                cantidad = int(input("Cuantas unidades quieres añadir? "))
            except ValueError:
                print("Por favor introduce un numero")
                continue
            if cantidad < 1:
                print("Cantidad no valida")
            elif cantidad > stock_disponible:
                print("No hay suficiente stock, disponible:", stock_disponible)
            else:
                carrito.append([nombre, precio, cantidad])
                productos[opcion - 1]["stock"] -= cantidad
                guardar_tienda(planta, tienda, productos)
                guardar_carrito()
                print("Has añadido", cantidad, "unidades de:", nombre)
        else:
            print("Opcion no valida")


def ver_carrito():
    if len(carrito) == 0:
        print("\nEl carrito esta vacio")
        return

    total = 0

    print("\nCARRITO:")

    for producto in carrito:
        print(producto[0], "-", producto[1], "€ x", producto[2], "=", producto[1] * producto[2], "€")
        total = total + producto[1] * producto[2]

    print("Total:", total, "€")


def añadir_producto():
    plantas = list(centro.keys())

    print("\nPLANTAS:")
    for i in range(len(plantas)):
        print(i + 1, ".", plantas[i])

    try:
        opcion = int(input("Elige planta: "))
    except ValueError:
        print("Por favor introduce un numero")
        return

    if opcion < 1 or opcion > len(plantas):
        print("Opcion no valida")
        return

    planta = plantas[opcion - 1]
    tiendas = list(centro[planta].keys())

    print("\nTIENDAS:")
    for i in range(len(tiendas)):
        print(i + 1, ".", tiendas[i])

    try:
        opcion = int(input("Elige tienda: "))
    except ValueError:
        print("Por favor introduce un numero")
        return

    if opcion < 1 or opcion > len(tiendas):
        print("Opcion no valida")
        return

    tienda = tiendas[opcion - 1]
    nombre = input("Nombre del producto: ")

    try:
        precio = float(input("Precio: "))
    except ValueError:
        print("Precio no valido")
        return

    try:
        stock = int(input("Stock inicial: "))
    except ValueError:
        print("Stock no valido")
        return

    centro[planta][tienda]["productos"].append({"nombre": nombre, "precio": precio, "stock": stock})
    guardar_tienda(planta, tienda, centro[planta][tienda]["productos"])
    print("Producto añadido correctamente")


def eliminar_producto():
    plantas = list(centro.keys())

    print("\nPLANTAS:")
    for i in range(len(plantas)):
        print(i + 1, ".", plantas[i])

    try:
        opcion = int(input("Elige planta: "))
    except ValueError:
        print("Por favor introduce un numero")
        return

    if opcion < 1 or opcion > len(plantas):
        print("Opcion no valida")
        return

    planta = plantas[opcion - 1]
    tiendas = list(centro[planta].keys())

    print("\nTIENDAS:")
    for i in range(len(tiendas)):
        print(i + 1, ".", tiendas[i])

    try:
        opcion = int(input("Elige tienda: "))
    except ValueError:
        print("Por favor introduce un numero")
        return

    if opcion < 1 or opcion > len(tiendas):
        print("Opcion no valida")
        return

    tienda = tiendas[opcion - 1]
    productos = centro[planta][tienda]["productos"]

    print("\nPRODUCTOS:")
    for i in range(len(productos)):
        print(i + 1, ".", productos[i]["nombre"], "-", productos[i]["precio"], "€", "- Stock:", productos[i]["stock"])

    try:
        opcion = int(input("Elige producto a eliminar (0 para salir): "))
    except ValueError:
        print("Por favor introduce un numero")
        return

    if opcion == 0:
        return
    elif opcion >= 1 and opcion <= len(productos):
        nombre = productos[opcion - 1]["nombre"]
        productos.pop(opcion - 1)
        guardar_tienda(planta, tienda, productos)
        print("Producto", nombre, "eliminado")
    else:
        print("Opcion no valida")


def cambiar_precio():
    plantas = list(centro.keys())

    print("\nPLANTAS:")
    for i in range(len(plantas)):
        print(i + 1, ".", plantas[i])

    try:
        opcion = int(input("Elige planta: "))
    except ValueError:
        print("Por favor introduce un numero")
        return

    if opcion < 1 or opcion > len(plantas):
        print("Opcion no valida")
        return

    planta = plantas[opcion - 1]
    tiendas = list(centro[planta].keys())

    print("\nTIENDAS:")
    for i in range(len(tiendas)):
        print(i + 1, ".", tiendas[i])

    try:
        opcion = int(input("Elige tienda: "))
    except ValueError:
        print("Por favor introduce un numero")
        return

    if opcion < 1 or opcion > len(tiendas):
        print("Opcion no valida")
        return

    tienda = tiendas[opcion - 1]
    productos = centro[planta][tienda]["productos"]

    print("\nPRODUCTOS:")
    for i in range(len(productos)):
        print(i + 1, ".", productos[i]["nombre"], "-", productos[i]["precio"], "€", "- Stock:", productos[i]["stock"])

    try:
        opcion = int(input("Elige producto (0 para salir): "))
    except ValueError:
        print("Por favor introduce un numero")
        return

    if opcion == 0:
        return
    elif opcion >= 1 and opcion <= len(productos):
        try:
            nuevo_precio = float(input("Nuevo precio: "))
        except ValueError:
            print("Precio no valido")
            return
        productos[opcion - 1]["precio"] = nuevo_precio
        guardar_tienda(planta, tienda, productos)
        print("Precio actualizado correctamente")
    else:
        print("Opcion no valida")


def menu_admin():
    while True:
        print("\nMODO ADMINISTRADOR")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Cambiar precio")
        print("0. Salir")

        opcion = input("Opcion: ")

        if opcion == "1":
            añadir_producto()
        elif opcion == "2":
            eliminar_producto()
        elif opcion == "3":
            cambiar_precio()
        elif opcion == "0":
            break
        else:
            print("Opcion no valida")


# PROGRAMA PRINCIPAL
while True:
    menu()
    opcion = input("Opcion: ")

    match opcion:
        case "1":
            elegir_tienda("Planta Baja")
        case "2":
            elegir_tienda("Planta 1")
        case "3":
            elegir_tienda("Planta 2")
        case "4":
            ver_carrito()
        case "5":
            confirmar_compra()
        case "6":
            carrito.clear()
            guardar_carrito()
            print("Carrito vaciado")
        case "7":
            contrasena = input("Introduce la contrasena: ")
            if contrasena == "123456":
                menu_admin()
            else:
                print("Contrasena incorrecta")
        case "8":
            print("Saliendo...")
            break
        case _:
            print("Opcion no valida")