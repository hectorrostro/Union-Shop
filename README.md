# Union-Shop 🏬

Centro comercial virtual desarrollado en Python como proyecto de fin de ciclo (TFG) del ciclo formativo de Sistemas Microinformáticos y Redes (SMR).

## Descripción

Union-Shop es una aplicación de consola que simula un centro comercial virtual con tres plantas y varias tiendas. Permite navegar por las tiendas, añadir productos al carrito, confirmar compras y gestionar el inventario desde un modo administrador. Los datos se almacenan en MongoDB y se sincronizan con archivos JSON como copia de seguridad.

## Requisitos

- Python 3.10 o superior
- MongoDB instalado y en ejecución
- Las siguientes librerías de Python: fastapi, uvicorn, pymongo

## Instalación

1. Clona el repositorio:
git clone https://github.com/hectorrostro/Union-Shop.git

2. Entra en la carpeta del proyecto:
cd Union-Shop

3. Instala las librerías necesarias:
pip install fastapi uvicorn pymongo

4. Instala MongoDB:
winget install MongoDB.Server

5. Arranca MongoDB como administrador:
net start MongoDB

6. Importa los datos a MongoDB ejecutando una sola vez:
python Backup/importar.py

## Cómo ejecutar

### Programa principal
Abre una terminal en la carpeta del proyecto y ejecuta:
python Centro.py

### API REST
Abre una terminal en la carpeta del proyecto y ejecuta:
uvicorn api:app --reload

### Ver la API en el navegador
Con la API corriendo, abre el navegador y ve a:
http://127.0.0.1:8000/docs

Desde ahí podrás probar todos los endpoints del proyecto directamente desde el navegador usando Swagger.

## Uso del programa

1. Al ejecutar Centro.py aparece el menú principal con las tres plantas del centro comercial.
2. Elige una planta para ver sus tiendas.
3. Elige una tienda para ver sus productos y añadirlos al carrito indicando la cantidad.
4. Desde el menú puedes ver el carrito, confirmar la compra o vaciarlo.
5. Para acceder al modo administrador introduce la contraseña cuando se solicite.
6. Desde el modo administrador puedes añadir, eliminar y cambiar precios de productos.

## Estructura del proyecto

- Centro.py — Programa principal de consola
- api.py — API REST con FastAPI
- productos.json — Copia de seguridad de los productos
- carrito.json — Copia de seguridad del carrito
- Backup/ — Archivos de respaldo y script de importación
- Documentacion/ — Manuales y documentación del proyecto
- Observaciones/ — Notas y observaciones del equipo

## Autores

- Héctor José Rostro Almaraz
- Jesús Tarifa Pozuelo
- Ismael Sánchez Amores