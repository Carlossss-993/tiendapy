import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from persistence import load_inventory, save_inventory, load_sales
from inventory import (
    BusinessRuleError,
    add_product,
    find_by_code,
    find_by_category,
    update_product,
    delete_product,
    get_products_table,
)
from sales import new_sale
from reports import (
    get_stock_alerts,
    format_stock_alerts,
    get_daily_closing,
    format_daily_closing,
)
from validation import (
    get_string,
    get_int,
    get_float,
    get_category,
    get_bool,
)


def inventory_menu(inventory: dict) -> None:
    while True:
        print("\n--- GESTIÓN DE INVENTARIO ---")
        print("1. Registrar nuevo producto")
        print("2. Consultar producto por código")
        print("3. Consultar productos por categoría")
        print("4. Modificar precio o stock de producto")
        print("5. Eliminar producto")
        print("6. Ver inventario completo")
        print("0. Volver al menú principal")

        option = get_int("Seleccione una opción: ")

        try:
            if option == 1:
                code = get_string("Código del producto (ej. LAC001): ").upper()
                name = get_string("Nombre del producto: ")
                category = get_category()
                price = get_float("Precio de venta (COP): ")
                stock = get_int("Stock inicial: ")
                min_stock = get_int("Stock mínimo de alerta: ")
                supplier = get_string("Nombre del proveedor: ")

                add_product(inventory, code, name, category, price, stock, min_stock, supplier)
                print(f" Producto '{name}' ({code}) registrado con éxito.")

            elif option == 2:
                code = get_string("Ingrese el código a buscar: ").upper()
                product = find_by_code(inventory, code)
                if product:
                    print(get_products_table([product]))
                else:
                    print(f" No se encontró ningún producto con el código '{code}'.")

            elif option == 3:
                category = get_category()
                products = find_by_category(inventory, category)
                if products:
                    print(get_products_table(products))
                else:
                    print(f" No hay productos registrados en la categoría '{category}'.")

            elif option == 4:
                code = get_string("Ingrese el código del producto a modificar: ").upper()
                product = find_by_code(inventory, code)
                if not product:
                    print(f" El producto '{code}' no existe.")
                    continue

                print(f"Modificando: {product['name']} (Precio actual: ${product['price']:,.2f}, Stock actual: {product['stock']})")
                change_price = get_bool("¿Desea cambiar el precio?")
                new_price = get_float("Nuevo precio: ") if change_price else None

                change_stock = get_bool("¿Desea cambiar el stock?")
                new_stock = get_int("Nuevo stock: ") if change_stock else None

                if new_price is not None or new_stock is not None:
                    update_product(inventory, code, price=new_price, stock=new_stock)
                    print("Producto actualizado correctamente.")
                else:
                    print("No se realizaron cambios.")

            elif option == 5:
                code = get_string("Ingrese el código del producto a eliminar: ").upper()
                product = find_by_code(inventory, code)
                if not product:
                    print(f"El producto '{code}' no existe.")
                    continue

                if get_bool(f"¿Está seguro de eliminar '{product['name']}' ({code})?"):
                    delete_product(inventory, code)
                    print("Producto eliminado.")
                else:
                    print("Operación cancelada.")

            elif option == 6:
                print(get_products_table(list(inventory.values())))

            elif option == 0:
                break
            else:
                print("Error: Opción no válida. Seleccione una opción del menú.")

        except BusinessRuleError as e:
            print(f"Error de negocio: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")


def main():
    inventory = load_inventory()
    print(f"Inventario cargado exitosamente ({len(inventory)} productos).")

    try:
        while True:
            print("\n=================================")
            print("   TIENDAPY - MENÚ PRINCIPAL    ")
            print("=================================")
            print("1. Gestión de inventario")
            print("2. Registrar nueva venta")
            print("3. Ver alertas de stock")
            print("4. Generar cierre del día")
            print("5. Guardar inventario")
            print("6. Salir")

            option = get_int("Seleccione una opción: ")

            try:
                if option == 1:
                    inventory_menu(inventory)
                elif option == 2:
                    new_sale(inventory)
                elif option == 3:
                    alerts = get_stock_alerts(inventory)
                    print(format_stock_alerts(alerts))
                elif option == 4:
                    sales = load_sales()
                    report = get_daily_closing(inventory, sales)
                    print(format_daily_closing(report))
                elif option == 5:
                    save_inventory(inventory)
                    print(" Inventario guardado en el disco de manera exitosa.")
                elif option == 6:
                    print("Saliendo de la aplicación...")
                    break
                else:
                    print("Error: Opción no válida. Seleccione un número entre 1 y 6.")
            except BusinessRuleError as e:
                print(f"Error de negocio: {e}")
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")

    finally:
        save_inventory(inventory)
        print("Guardado automático finalizado. !Hasta luego!")


if __name__ == "__main__":
    main()