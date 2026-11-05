from tabulate import tabulate


class BusinessRuleError(Exception):
    pass


def add_product(inventory: dict, code: str, name: str, category: str, price: float, stock: int, min_stock: int, supplier: str) -> dict:
    if code in inventory:
        raise BusinessRuleError(f"El producto con código '{code}' ya existe.")
    if price <= 0:
        raise BusinessRuleError("El precio debe ser estrictamente mayor a 0.")
    if stock < 0 or min_stock < 0:
        raise BusinessRuleError("El stock no puede ser negativo.")

    product = {
        "code": code,
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
        "min_stock": min_stock,
        "supplier": supplier
    }
    inventory[code] = product
    return product


def find_by_code(inventory: dict, code: str) -> dict | None:
    return inventory.get(code)


def find_by_category(inventory: dict, category: str) -> list:
    return [item for item in inventory.values() if item["category"].lower() == category.lower()]


def update_product(inventory: dict, code: str, price: float | None = None, stock: int | None = None) -> dict:
    if code not in inventory:
        raise BusinessRuleError(f"El producto con código '{code}' no existe.")
    if price is not None:
        if price <= 0:
            raise BusinessRuleError("El precio debe ser estrictamente mayor a 0.")
        inventory[code]["price"] = price
    if stock is not None:
        if stock < 0:
            raise BusinessRuleError("El stock no puede ser negativo.")
        inventory[code]["stock"] = stock
    return inventory[code]


def delete_product(inventory: dict, code: str) -> dict:
    if code not in inventory:
        raise BusinessRuleError(f"El producto con código '{code}' no existe.")
    return inventory.pop(code)


def get_products_table(products: list) -> str:
    if not products:
        return "No hay productos para mostrar."
    
    headers = ["Código", "Nombre", "Categoría", "Precio (COP)", "Stock", "Stock Mín.", "Proveedor"]
    rows = [
        [
            p["code"],
            p["name"],
            p["category"],
            f"${p['price']:,.2f}",
            p["stock"],
            p["min_stock"],
            p["supplier"]
        ]
        for p in products
    ]
    return tabulate(rows, headers=headers, tablefmt="grid")