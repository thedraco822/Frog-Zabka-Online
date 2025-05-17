import pandas as pd
import random
import os
from utils import log_action, apply_discount
from product_management import check_product_availability, DATABASE_PATH

CUSTOMER_DB_PATH = "database/customer.csv"
DATABASE_FOLDER = "database/DATABASE/"


def initialize_customer_csv(db_path: str):
    """
    Inicjalizuje plik customer.csv z nagłówkami, jeśli nie istnieje.

    Args:
        db_path (str): Ścieżka do pliku CSV.
    """
    try:
        if not os.path.exists(db_path):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            df = pd.DataFrame(columns=["id", "name", "surname"])
            df.to_csv(db_path, index=False)
    except PermissionError as e:
        print(f"Błąd uprawnień podczas inicjalizacji pliku {db_path}: {e}")
        print("Sprawdź uprawnienia do folderu 'database/' lub uruchom program jako administrator.")
    except Exception as e:
        print(f"Błąd podczas inicjalizacji pliku CSV: {e}")


def generate_customer_id():
    """Funkcja zagnieżdżona generująca losowy 4-cyfrowy ID klienta."""

    def format_id(num: int) -> str:
        return f"{num:04d}"

    return format_id(random.randint(0, 9999))


@log_action("Zarejestrowano klienta")
def register_customer(db_path: str, customer_data: dict) -> str:
    """
    Rejestruje nowego klienta i tworzy plik historii zakupów.

    Args:
        db_path (str): Ścieżka do pliku bazy klientów.
        customer_data (dict): Dane klienta (name, surname).

    Returns:
        str: ID klienta lub None w przypadku błędu.
    """
    try:
        initialize_customer_csv(db_path)
        df = pd.read_csv(db_path)

        if not all(col in df.columns for col in ["id", "name", "surname"]):
            raise ValueError("Plik CSV nie zawiera wymaganych kolumn: id, name, surname")

        customer_id = generate_customer_id()
        while customer_id in df["id"].astype(str).values:
            customer_id = generate_customer_id()
        customer_data["id"] = customer_id
        new_row = pd.DataFrame([customer_data])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(db_path, index=False)

        os.makedirs(DATABASE_FOLDER, exist_ok=True)
        history_path = os.path.join(DATABASE_FOLDER, f"{customer_id}.txt")
        with open(history_path, "w") as f:
            f.write("Historia zakupów:\n")
        return customer_id
    except PermissionError as e:
        print(f"Błąd uprawnień podczas rejestracji klienta: {e}")
        print("Sprawdź uprawnienia do pliku 'customer.csv' lub folderu 'database/'.")
        return None
    except Exception as e:
        print(f"Błąd podczas rejestracji klienta: {e}")
        return None


@log_action("Usunięto klienta")
def remove_customer(db_path: str, identifier: str, by: str = "id") -> bool:
    try:
        initialize_customer_csv(db_path)
        df = pd.read_csv(db_path)
        if by == "id":
            customer_id = identifier
            df = df[df["id"].astype(str) != identifier]
        elif by == "name":
            df = df[df["name"] != identifier]
        else:
            raise ValueError("Nieprawidłowe kryterium usuwania")
        df.to_csv(db_path, index=False)

        history_path = os.path.join(DATABASE_FOLDER, f"{customer_id}.txt")
        if os.path.exists(history_path):
            os.remove(history_path)
        return True
    except PermissionError as e:
        print(f"Błąd uprawnień podczas usuwania klienta: {e}")
        print("Sprawdź uprawnienia do pliku 'customer.csv' lub folderu 'database/'.")
        return False
    except Exception as e:
        print(f"Błąd podczas usuwania klienta: {e}")
        return False


def purchase_products(customer_id: str, *products, discount_rate: float = 0.0) -> bool:
    """
    Funkcja wyższego rzędu obsługująca zakup wielu produktów z możliwością rabatu.

    Args:
        customer_id (str): ID klienta.
        *products: Lista krotek (product_id, quantity).
        discount_rate (float): Procent rabatu.

    Returns:
        bool: True, jeśli zakup zakończony sukcesem, False w przeciwnym razie.
    """

    def process_purchase(product_id: str, quantity: int) -> bool:
        try:
            product_id = str(product_id)  # Konwersja ID na string
            if not check_product_availability(DATABASE_PATH, product_id):
                print(f"Produkt {product_id} niedostępny")
                return False
            df = pd.read_excel(DATABASE_PATH, engine="openpyxl")
            product_row = df[df["id"].astype(str) == product_id]
            if product_row.empty:
                print(f"Produkt o ID {product_id} nie znaleziony w bazie")
                return False
            product = product_row.iloc[0]
            if product["stock"] < quantity:
                print(
                    f"Niewystarczający stan magazynowy dla {product_id}: dostępne {product['stock']}, żądane {quantity}")
                return False

            # Aktualizacja stanu magazynowego
            df.loc[df["id"].astype(str) == product_id, "stock"] -= quantity
            df.to_excel(DATABASE_PATH, engine="openpyxl", index=False)

            # Zapis do historii
            history_path = os.path.join(DATABASE_FOLDER, f"{customer_id}.txt")
            total_price = apply_discount(product["price"] * quantity, discount_rate)
            with open(history_path, "a") as f:
                f.write(f"Produkt: {product['name']}, Ilość: {quantity}, Cena: {total_price}\n")
            return True
        except PermissionError as e:
            print(f"Błąd uprawnień podczas zapisu zakupu: {e}")
            print("Sprawdź uprawnienia do folderu 'database/DATABASE/' lub pliku 'products.xlsx'.")
            return False
        except Exception as e:
            print(f"Błąd podczas przetwarzania zakupu produktu {product_id}: {e}")
            return False

    return all(process_purchase(pid, qty) for pid, qty in products)


def get_customer_history(customer_id: str) -> list:
    try:
        history_path = os.path.join(DATABASE_FOLDER, f"{customer_id}.txt")
        with open(history_path, "r") as f:
            return f.readlines()[1:]  # Pomijamy nagłówek
    except PermissionError as e:
        print(f"Błąd uprawnień podczas odczytu historii: {e}")
        print(f"Sprawdź uprawnienia do pliku '{history_path}'.")
        return []
    except Exception as e:
        print(f"Błąd podczas odczytu historii: {e}")
        return []