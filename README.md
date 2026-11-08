# Proyecto Final - Python 0 a 100 - TiendaPy

## Carlos Sneider Fandiño Hernández - 20211020148

Este proyecto es una aplicacion de consola desarrollada en Python para la gestion de inventario, procesamiento de ventas y generacion de reportes de la tienda de barrio "Don Aurelio". La solucion permite almacenar la información de manera permanente en archivos de texto plano (.txt) sin dependerr de bases de datos externas ni librerias complejas.

## Requisitos e Instalacion

Para ejecutar este proyecto es necesario contar con Python 3.10 o superior y la libreria `tabulate` para el formateo de tablas en consola.

1. Clonar el repositorio y entrar a la carpeta del proyecto:
```bash
git clone <URL_DE_TU_REPOSITORIO>
cd tiendapy
```

2. Crear y activar el entorno virtual:
```bash
python -m venv venv
source venv/Scripts/activate
```

3. Instalar las dependencias listadas en el archivo de requerimientos:
```bash
pip install -r requirements.txt
```

## Como Ejecutar

Uan vez activado el entorno virtual, se debe ejecutar el archivo principal desde la raiz del proyecto con el siguiente comando:

```bash
python src/main.py
```

## Estructura del Proyecto

```text
tiendapy/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── inventario.txt
│   └── ventas.txt
└── src/
    ├── __init__.py
    ├── main.py
    ├── inventario.py
    ├── ventas.py
    ├── reportes.py
    ├── persistencia.py
    └── validaciones.py
```

* `src/main.py`: Punto de entrada del programa. Contiene el menu principal e integra los demas modulos con un flujo continuo mediante ciclos
* `src/inventario.py`: Logica para la gestion de productos (agregar, consultar por codigo/categoria, modificar precio/stock y eliminar)
* `src/ventas.py`: Manejo del carrito de compras, calculo de subtotales, aplicacion de descuentos por umbral y procesamiento del pago.
* `src/reportes.py`: Generacion del reporte de alertas de stock bajo y el reporte del cierre de caja diario.
* `src/persistencia.py`: Carga y guardado de datos desde y hacia los archivos de texto `.txt`
* `src/validaciones.py`: Funciones para solicitar datos al usuario de forma segura y evitar que el programa se detenga por errores de digitacion
* `data/inventario.txt`: Archivo de texto plano con la lista de productos del inventario.
* `data/ventas.txt`: Archivo donde se registra el historial de ventas realizadas.

## Decisiones de Diseño

En este proyecto tome variias decisiones de arquitectura y estructura para cumplir con todos los requerimientos y mantener el código dentro del alcance del curso:

1. Modelado sin clases (Programacion Estructurada y Modular):
   Decidi no utilizar clases ni Programacion Orientada a Objetos (POO) ya que el enunciado no lo exige. Modelé los productos como diccionarios nativos de Python y el inventario como un diccionario general donde la clave es el codigo del producto. Esto simplifica la busqueda directa por codigo en tiempo constante y facilita la conversion a texto plano.

2. Separacion de Logica y Presentacion:
   Las funciones en `inventario.py`, `ventas.py` y `reportes.py` no mezclan `input()` e `print()` directamente con los calculos. Reciben las estructuras de datos, procesan la información y devuelven valoores o tablas formateadas con `tabulate`. La interaccion con el usuario la concentre en `validaciones.py` y `main.py`.

3. Garantía de Persistencia:
   El guardado automatico del inventario al finalizar la ejecucion lo envolvi en un bloque `try ... finally` en `main.py`. Esto garantiza que, incluso si ocurre una interrupcion o error inesperado durante el uso del menu, la información modificada se guarde correctamente en `data/inventory.txt`.

## Formato de los Archivos de Datos

- `data/inventory.txt`: Guarda un producto por linea con los campos separados por la barra vertical (`|`):
  `codigo|nombre|categoria|precio|stock|stock_minimo|proveedor`
  *Ejemplo:* `LAC001|Leche entera 1L|Lacteos|4200.0|35|10|Alqueria`

- `data/sales.txt`: Guarda una venta por linea con la fecha y hora, el total cobrado y la lsita de items comprados:
  `fecha|total|codigo:cantidad;codigo:cantidad`
  *Ejemplo:* `2026-11-07 19:47:42|8400.0|LAC001:2`