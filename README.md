# Union-Shop

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

2. Instala las librerías necesarias:
pip install fastapi uvicorn pymongo

3. Instala MongoDB:
winget install MongoDB.Server

4. Importa los datos a MongoDB ejecutando una sola vez:
python Backup/importar.py

## Cómo ejecutar

Para ejecutar el programa principal:
python Centro.py

Para arrancar la API:
uvicorn api:app --reload

Para ver la API en el navegador abre:
http://127.0.0.1:8000/docs

## Autores

- Héctor José Rostro Almaraz
- Jesús Tarifa Pozuelo
- Ismael Sánchez Amores