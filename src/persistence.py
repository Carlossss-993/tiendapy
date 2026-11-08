import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY_FILE = os.path.join(BASE, "data", "inventario.txt")
SALES_FILE = os.path.join(BASE, "data", "ventas.txt")


def load_inventory(filepath: str = INVENTORY_FILE) -> dict:
    inventory = {}
    if not os.path.exists(filepath):
        print(f"Advertencia: El archivo '{filepath}' no existe. Se creará uno nuevo al guardar.")
        return inventory

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 7:
                    print(f"Advertencia (Linea {line_num}): Estructura de linea inválida. Omitiendo.")
                    continue
                try:
                    code, name, category, price_str, stock_str, min_stock_str, supplier = parts
                    inventory[code] = {
                        "code": code,
                        "name": name,
                        "category": category,
                        "price": float(price_str),
                        "stock": int(stock_str),
                        "min_stock": int(min_stock_str),
                        "supplier": supplier
                    }
                except (ValueError, IndexError):
                    print(f"Advertencia (Linea {line_num}): Error de conversión en datos de producto. Omitiendo.")
    except Exception as e:
        print(f"Error al leer '{filepath}': {e}")

    return inventory


def save_inventory(inventory: dict, filepath: str = INVENTORY_FILE) -> None:
    dir_name = os.path.dirname(filepath)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        for item in inventory.values():
            line = f"{item['code']}|{item['name']}|{item['category']}|{item['price']}|{item['stock']}|{item['min_stock']}|{item['supplier']}\n"
            file.write(line)


def save_sale(date_str: str, total: float, cart: dict, filepath: str = SALES_FILE) -> None:
    dir_name = os.path.dirname(filepath)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    items_str = ";".join([f"{code}:{qty}" for code, qty in cart.items()])
    line = f"{date_str}|{total}|{items_str}\n"
    with open(filepath, "a", encoding="utf-8") as file:
        file.write(line)


def load_sales(filepath: str = SALES_FILE) -> list:
    sales = []
    if not os.path.exists(filepath):
        return sales

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) < 3:
                    parts = line.split(" ", 2)
                    if len(parts) < 3:
                        print(f"Advertencia (Ventas Linea {line_num}): Estructura corrupta. Omitiendo.")
                        continue

                try:
                    date_str = parts[0].strip()
                    total = float(parts[1].strip())
                    raw_items = parts[2].strip()
                    items = {}
                    if raw_items:
                        for entry in raw_items.split(";"):
                            entry = entry.strip()
                            if not entry:
                                continue
                            code, qty_str = entry.split(":")
                            items[code.strip()] = int(qty_str.strip())
                    sales.append({
                        "date": date_str,
                        "total": total,
                        "items": items
                    })
                except (ValueError, IndexError):
                    print(f"Advertencia (Ventas Linea {line_num}): Error de parseo de venta. Omitiendo.")
    except Exception as e:
        print(f"Error al leer ventas en '{filepath}': {e}")

    return sales