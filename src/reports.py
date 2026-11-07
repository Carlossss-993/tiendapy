from datetime import datetime
from tabulate import tabulate


def get_stock_alerts(inventory: dict) -> dict:
    alerts_by_supplier = {}
    for item in inventory.values():
        if item["stock"] <= item["min_stock"]:
            supplier = item["supplier"]
            if supplier not in alerts_by_supplier:
                alerts_by_supplier[supplier] = []
            alerts_by_supplier[supplier].append({
                "code": item["code"],
                "name": item["name"],
                "stock": item["stock"],
                "min_stock": item["min_stock"],
                "is_out_of_stock": item["stock"] == 0
            })
    return alerts_by_supplier


def format_stock_alerts(alerts_by_supplier: dict) -> str:
    if not alerts_by_supplier:
        return "No hay alertas de stock. Todos los productos tienen existencias suficientes."

    output = []
    for supplier, products in alerts_by_supplier.items():
        output.append(f"\nProveedor: {supplier}")
        headers = ["Código", "Nombre", "Stock Actual", "Stock Mínimo", "Estado"]
        rows = [
            [
                p["code"],
                p["name"],
                p["stock"],
                p["min_stock"],
                "AGOTADO" if p["is_out_of_stock"] else "STOCK BAJO"
            ]
            for p in products
        ]
        output.append(tabulate(rows, headers=headers, tablefmt="grid"))

    return "\n".join(output)


def get_daily_closing(inventory: dict, sales: list, date_str: str | None = None) -> dict:
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    today_sales = [s for s in sales if s["date"].startswith(date_str)]

    total_sales_amount = sum(s["total"] for s in today_sales)
    sales_count = len(today_sales)
    average_ticket = (total_sales_amount / sales_count) if sales_count > 0 else 0.0

    product_quantities = {}
    for s in today_sales:
        for code, qty in s["items"].items():
            product_quantities[code] = product_quantities.get(code, 0) + qty

    if product_quantities:
        max_qty = max(product_quantities.values())
        most_sold_codes = [code for code, qty in product_quantities.items() if qty == max_qty]
        most_sold_products = [
            {
                "code": code,
                "name": inventory[code]["name"] if code in inventory else code,
                "quantity": max_qty
            }
            for code in most_sold_codes
        ]
    else:
        most_sold_products = []

    sold_product_codes = set(product_quantities.keys())
    products_without_sales = [
        item for code, item in inventory.items() if code not in sold_product_codes
    ]

    active_categories = {
        inventory[code]["category"]
        for code in sold_product_codes
        if code in inventory
    }

    return {
        "date": date_str,
        "total_sales_amount": total_sales_amount,
        "sales_count": sales_count,
        "average_ticket": average_ticket,
        "most_sold_products": most_sold_products,
        "products_without_sales": products_without_sales,
        "active_categories": active_categories
    }


def format_daily_closing(report: dict) -> str:
    lines = [
        f"\n=== CIERRE DE CAJA DEL DÍA ({report['date']}) ===",
        f"Total Vendido:         ${report['total_sales_amount']:,.2f}",
        f"Número de Ventas:      {report['sales_count']}",
        f"Ticket Promedio:       ${report['average_ticket']:,.2f}\n"
    ]

    lines.append("--- Producto(s) Más Vendido(s) ---")
    if report["most_sold_products"]:
        for p in report["most_sold_products"]:
            lines.append(f"- {p['name']} ({p['code']}): {p['quantity']} unidad(es)")
    else:
        lines.append("No se registraron ventas hoy.")

    lines.append("\n--- Categorías con Movimiento ---")
    if report["active_categories"]:
        lines.append(", ".join(sorted(list(report["active_categories"]))))
    else:
        lines.append("Ninguna categoría registró movimiento.")

    lines.append("\n--- Productos Sin Ventas Hoy ---")
    if report["products_without_sales"]:
        headers = ["Código", "Nombre", "Categoría", "Stock Actual"]
        rows = [
            [p["code"], p["name"], p["category"], p["stock"]]
            for p in report["products_without_sales"]
        ]
        lines.append(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        lines.append("Todos los productos del inventario registraron ventas hoy.")

    return "\n".join(lines)