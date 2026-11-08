from datetime import datetime
from inventory import BusinessRuleError
from persistence import save_sale
from validation import get_float, get_int, get_string, get_bool


def calculate_subtotal(cart: dict, inventory: dict) -> float:
    subtotal = 0.0
    for code, qty in cart.items():
        if code not in inventory:
            raise BusinessRuleError(f"El producto con código '{code}' no existe en el inventario.")
        subtotal += inventory[code]["price"] * qty
    return subtotal


def calculate_discount(subtotal: float) -> tuple[float, float]:
    if subtotal >= 100000.0:
        rate = 0.10
    elif subtotal >= 50000.0:
        rate = 0.05
    else:
        rate = 0.0

    discount_amount = subtotal * rate
    return rate, discount_amount


def add_to_cart(cart: dict, inventory: dict, code: str, quantity: int) -> dict:
    if code not in inventory:
        raise BusinessRuleError(f"El producto '{code}' no existe en el inventario.")
    if quantity <= 0:
        raise BusinessRuleError("La cantidad a vender debe ser mayor a 0.")

    current_in_cart = cart.get(code, 0)
    total_requested = current_in_cart + quantity
    available_stock = inventory[code]["stock"]

    if total_requested > available_stock:
        raise BusinessRuleError(
            f"Stock insuficiente para '{inventory[code]['name']}'. "
            f"Disponible: {available_stock}, Solicitado total en carrito: {total_requested}."
        )

    cart[code] = total_requested
    return cart


def process_payment(total: float) -> float:
    while True:
        payment = get_float(f"Ingrese el monto con el que paga el cliente (Total a pagar: ${total:,.2f}): ")
        if payment < total:
            print(f"Error: El pago (${payment:,.2f}) es inferior al total a pagar (${total:,.2f}). Reintente.")
            continue
        change = payment - total
        return change


def confirm_sale(cart: dict, inventory: dict) -> float:
    subtotal = calculate_subtotal(cart, inventory)
    _, discount_amount = calculate_discount(subtotal)
    total = subtotal - discount_amount

    change = process_payment(total)

    for code, qty in cart.items():
        inventory[code]["stock"] -= qty

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_sale(date_str, total, cart)

    return change


def new_sale(inventory: dict) -> None:
    cart = {}

    while True:
        code = get_string("Ingrese el código del producto a vender (o 'FIN' para terminar): ").upper()
        if code == "FIN":
            if not cart:
                print("Venta cancelada: El carrito está vacío.")
                return
            break

        if code not in inventory:
            print(f"Error: El producto '{code}' no existe en el inventario.")
            continue

        qty = get_int(f"Ingrese la cantidad para '{inventory[code]['name']}': ")

        try:
            add_to_cart(cart, inventory, code, qty)
            print(f"-> Añadido: {inventory[code]['name']} x{qty}")
        except BusinessRuleError as e:
            print(f"Error: {e}")

    subtotal = calculate_subtotal(cart, inventory)
    rate, discount_amount = calculate_discount(subtotal)
    total = subtotal - discount_amount

    print("\n--- RESUMEN DE LA VENTA ---")
    for code, qty in cart.items():
        item = inventory[code]
        item_total = item["price"] * qty
        print(f"- {item['name']} (x{qty}) @ ${item['price']:,.2f} = ${item_total:,.2f}")

    print(f"Subtotal:   ${subtotal:,.2f}")
    print(f"Descuento:  ${discount_amount:,.2f} ({int(rate * 100)}%)")
    print(f"Total:      ${total:,.2f}")

    if not get_bool("¿Desea confirmar y procesar la venta?"):
        print("Venta cancelada. El inventario no sufrió cambios.")
        return

    change = confirm_sale(cart, inventory)
    print(f"¡Venta registrada exitosamente! Cambio a devolver: ${change:,.2f}")