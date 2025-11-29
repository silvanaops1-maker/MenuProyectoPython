import sys
import os
print("Directorio actual:", os.getcwd())   # te dice desde qué carpeta se está ejecutando Python

import sqlite3
from colorama import Fore, Style, init
init(autoreset=True)

# Ruta completa a la base de datos - recomendacion chatGPT
DB_PATH = r"C:\Users\Silvana\Desktop\Inicio python\.vscode\Nuevoproyecto.py\Menuproyecto.py\inventario.db"
# Nombre de la tabla
TABLE_NAME = "productos"

# Función para mostrar títulos con estilo
def titulo(texto):
    print(Fore.CYAN + Style.BRIGHT + texto.upper())

# Conectar a la base de datos
def conectar_base_datos():
    return sqlite3.connect(DB_PATH)

def inicializar_base_datos():
    try:
        with conectar_base_datos() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    precio INTEGER NOT NULL
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
        # # Conectar a la base de datos (se crea si no existe)

def mostrar_menu():
    while True:
        print("\n" + "="*40) # ======================================
        print("1 - agregar producto")
        print("2 - mostrar productos")
        print("3 - buscar productos")
        print("4 - eliminar producto")
        print("5 - salir")
        print("="*40) # ==========================================

        opcion = input("\nSeleccione una opcion (1-5): ").strip()
        if opcion == "":
            print("Debe ingresar una opción válida.")
            continue  # vuelve a preguntar

        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            mostrar_productos_guardados()
        elif opcion == "3":
            buscar_productos()
        elif opcion == "4":
            eliminar_productos()
        elif opcion == "5":
            print("Gracias por usar el sistema. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
        """
        La funcion mostrar_menu despliega las opciones que pueden ser elegidas 
        por el usuario
        """


def agregar_producto():
    while True:
        nombre = input("Favor ingresar el nombre del producto: ").strip().capitalize()
        if nombre != "":
            break
        print("Error: El nombre no puede estar vacío.")
    while True:
        categoria = input("Favor ingresar la categoria del producto: ").strip().capitalize()
        if categoria != "":
            break
        print("Error: El campo no puede estar vacío.")
    while True:
        try:
            precio_input = input("Valor del producto (número entero positivo): ").strip()
            precio = int(precio_input)
            if precio > 0:
                break  # ✅ datos válidos
            else:
                print("Error: debe ser un número positivo.")
        except ValueError:
            print("Error: ingrese un número entero válido.")
        """
        La funcion solicita los argumentos nombre, categoria y precio.
        El argumento nombre puede ser utilizado fuera de la funcion 
        Luego los ordena alfabeticamente y los muestra en diccionario
        """
    try:
        with conectar_base_datos() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO {TABLE_NAME} (nombre, categoria, precio) VALUES (?, ?, ?)",
                (nombre, categoria, precio)
            )
            conn.commit()
        print(f"Producto '{nombre}' agregado con éxito a la base de datos.")  # ✅ ahora está dentro del with
    except sqlite3.Error as e:
        print(f"Error al agregar producto: {e}")


def mostrar_productos_guardados ():
    try:
        with conectar_base_datos() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME}")
            productos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al leer productos: {e}")
        return

    if not productos:
        print("No hay productos registrados en nuestra tienda.")
        return
    
    print(f"\nTotal de productos: {len(productos)}\n")
    for i, producto in enumerate (productos, start=1):
         # Suponiendo que la tupla es (id, nombre, categoria, precio)
        print(f"{i}. ID: {producto[0]} | Nombre: {producto[1]} | Categoria: {producto[2]} | Precio: {producto[3]}")

        """"
        La funcion motrar_productos_guardados, verifica si el cliente ha ingresado informacion.
        En el caso que asi sea muestra los mismos de manera ordenada, incluyendo los datos 
        que se han solicitados anteriormente. 
        """

def buscar_productos():
    #se debe ingresar el nombre o categoria con 1ra letra mayuscula
    termino = input("Ingrese nombre o categoría a buscar: ").strip()
    if termino == "":
        print("Debe ingresar un término.")
        return

    try:
        with conectar_base_datos() as conn:
            cursor = conn.cursor()
            cursor.execute(
                 f"""
                SELECT * FROM {TABLE_NAME} WHERE nombre LIKE ? OR categoria LIKE ?
              """,
                (f"%{termino}%", f"%{termino}%")
            )
            resultados = cursor.fetchall()
    except sqlite3.Error as e:
        print("Error en la búsqueda:", e)
        return

    if not resultados:
        print("No se encontraron productos.")
        return
    print("\nResultados encontrados:\n")
    for prod in resultados:
        print(f"ID: {prod[0]} | Nombre: {prod[1]} | Categoria: {prod[2]} | Precio: {prod[3]}")
        """
        La funcion buscar_productos permite al usuario buscar productos por nombre o categoria exacta.
        Muestra los resultados encontrados o un mensaje si no hay coincidencias.
        """
def eliminar_productos():
    mostrar_productos_guardados()
    id_input = input("Ingrese el ID del producto a eliminar: ").strip()
    if not id_input.isdigit():
        print("Debe ingresar un ID numérico válido.")
        return
    id_producto = int(id_input)

    try:
        with conectar_base_datos() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?", (id_producto,))
            producto = cursor.fetchone()
            if not producto:
                print("No se encontró un producto con ese ID.")
                return
        # Mostrar el producto y pedir confirmación
        print(f"\nProducto encontrado:")
        print(f"ID: {producto[0]} | Nombre: {producto[1]} | Categoria: {producto[2]} | Precio: {producto[3]}")
            
        # Confirmación
        confirmar = input("\n¿Está seguro que desea eliminar el producto? (S/N): ").strip().lower()
        if confirmar != "s":
            print("Operación cancelada.")
            return

            # Si confirma, eliminar
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (id_producto,))
        conn.commit()

        print(f"Producto con ID {id_producto} eliminado exitosamente.")

    except sqlite3.Error as e:
        print("Error al eliminar el producto:", e)
        """
        La funcion eliminar_productos permite al usuario eliminar un producto especificando su ID.
        Verifica si el ID existe y elimina el producto de la base de datos.
        """
