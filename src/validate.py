VALID_CATEGORIES = {"Lácteos", "Bebidas", "Aseo", "Abarrotes", "Snacks"}


def get_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: El texto no puede estar vacío. Intente de nuevo.")


def get_int(prompt: str, positive_only: bool = True, allow_zero: bool = False) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if positive_only:
                if allow_zero and value < 0:
                    print("Error: El valor no puede ser negativo.")
                    continue
                if not allow_zero and value <= 0:
                    print("Error: El valor debe ser mayor a 0.")
                    continue
            return value
        except ValueError:
            print("Error: Entrada inválida. Debe ingresar un número entero válido.")


def get_float(prompt: str, positive_only: bool = True, allow_zero: bool = False) -> float:
    while True:
        try:
            value = float(input(prompt).strip())
            if positive_only:
                if allow_zero and value < 0:
                    print("Error: El valor no puede ser negativo.")
                    continue
                if not allow_zero and value <= 0:
                    print("Error: El valor debe ser mayor a 0.")
                    continue
            return value
        except ValueError:
            print("Error: Entrada inválida. Debe ingresar un número decimal válido.")


def get_category() -> str:
    categories_list = sorted(list(VALID_CATEGORIES))
    print("\nCategorías disponibles:")
    for idx, cat in enumerate(categories_list, 1):
        print(f"  {idx}. {cat}")

    while True:
        user_input = input("Seleccione el número o escriba la categoría: ").strip()
        if user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index < len(categories_list):
                return categories_list[index]

        for cat in categories_list:
            if user_input.lower() == cat.lower():
                return cat

        options_str = ", ".join(categories_list)
        print(f"Error: Categoría no válida. Opciones permitidas: {options_str}")


def get_bool(prompt: str) -> bool:
    while True:
        response = input(f"{prompt} (s/n): ").strip().lower()
        if response in {"s", "si", "y", "yes"}:
            return True
        if response in {"n", "no"}:
            return False
        print("Error: Entrada no reconocida. Responda con 's' (Si) o 'n' (No).")