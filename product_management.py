import pandas as pd
import openpyxl
from openpyxl import Workbook
from functools import reduce
from utils import log_action
import os

DATABASE_PATH = "database/products.xlsx"


def validate_product_data(func):
    """
    Dekorator sprawdzający poprawność danych produktu.
    """

    def wrapper(*args, **kwargs):
        try:
            product_data = args[1] if len(args) > 1 else kwargs
            if not all(key in product_data for key in ["id", "name", "price", "stock"]):
                raise ValueError("Brak wymaganych danych produktu (id, name, price, stock)")
            if not isinstance(product_data["price"], (int, float)) or product_data["price"] < 0:
                raise ValueError("Cena musi być liczbą nieujemną")
            if not isinstance(product_data["stock"], int) or product_data["stock"] < 0:
                raise ValueError("Stan magazynowy musi być liczbą nieujemną")
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Błąd walidacji danych produktu: {e}")
            return None

    return wrapper


def initialize_excel_file(db_path: str):
    """
    Inicjalizuje nowy plik Excel z odpowiednimi kolumnami, jeśli nie istnieje.

    Args:
        db_path (str): Ścieżka do pliku Excel.
    """
    try:
        if not os.path.exists(db_path):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            wb = Workbook()
            ws = wb.active
            ws.append(["id", "name", "price", "stock"])
            wb.save(db_path)
    except PermissionError as e:
        print(f"Błąd uprawnień podczas inicjalizacji pliku {db_path}: {e}")
        print("Sprawdź uprawnienia do folderu 'database/'.")
    except Exception as e:
        print(f"Błąd podczas inicjalizacji pliku Excel: {e}")


@validate_product_data
@log_action("Dodano produkt")
def add_product(db_path: str, product_data: dict) -> bool:
    """
    Dodaje nowy produkt do bazy produktów (products.xlsx).

    Args:
        db_path (str): Ścieżka do pliku bazy danych.
        product_data (dict): Dane produktu (id, name, price, stock).

    Returns:
        bool: True, jeśli dodano pomyślnie, False w przeciwnym razie.
    """
    try:
        initialize_excel_file(db_path)
        df = pd.read_excel(db_path, engine="openpyxl")
        if str(product_data["id"]) in df["id"].astype(str).values:
            raise ValueError(f"Produkt o ID {product_data['id']} już istnieje")
        new_row = pd.DataFrame([product_data])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(db_path, engine="openpyxl", index=False)
        return True
    except PermissionError as e:
        print(f"Błąd uprawnień podczas dodawania produktu: {e}")
        print("Sprawdź uprawnienia do pliku 'products.xlsx'.")
        return False
    except Exception as e:
        print(f"Błąd podczas dodawania produktu: {e}")
        return False


@log_action("Usunięto produkt")
def remove_product(db_path: str, identifier: str, by: str = "id") -> bool:
    """
    Usuwa produkt z bazy produktów na podstawie ID lub nazwy.

    Args:
        db_path (str): Ścieżka do pliku bazy danych.
        identifier (str): ID lub nazwa produktu.
        by (str): Kryterium usuwania ("id" lub "name").

    Returns:
        bool: True, jeśli usunięto pomyślnie, False w przeciwnym razie.
    """
    try:
        initialize_excel_file(db_path)
        df = pd.read_excel(db_path, engine="openpyxl")
        if by == "id":
            df = df[df["id"].astype(str) != str(identifier)]
        elif by == "name":
            df = df[df["name"] != identifier]
        else:
            raise ValueError("Nieprawidłowe kryterium usuwania")
        df.to_excel(db_path, engine="openpyxl", index=False)
        return True
    except PermissionError as e:
        print(f"Błąd uprawnień podczas usuwania produktu: {e}")
        print("Sprawdź uprawnienia do pliku 'products.xlsx'.")
        return False
    except Exception as e:
        print(f"Błąd podczas usuwania produktu: {e}")
        return False


def get_product_stats(db_path: str) -> dict:
    """
    Zwraca statystyki produktów (min, max, średnia cena i stan magazynowy).

    Args:
        db_path (str): Ścieżka do pliku bazy danych.

    Returns:
        dict: Statystyki produktów.
    """
    try:
        initialize_excel_file(db_path)
        df = pd.read_excel(db_path, engine="openpyxl")
        stats = {
            "min_price": df["price"].min(),
            "max_price": df["price"].max(),
            "avg_price": df["price"].mean(),
            "min_stock": df["stock"].min(),
            "max_stock": df["stock"].max(),
            "avg_stock": df["stock"].mean()
        }
        return stats
    except PermissionError as e:
        print(f"Błąd uprawnień podczas obliczania statystyk: {e}")
        print("Sprawdź uprawnienia do pliku 'products.xlsx'.")
        return {}
    except Exception as e:
        print(f"Błąd podczas obliczania statystyk: {e}")
        return {}


def check_product_availability(db_path: str, product_id: str) -> bool:
    """
    Sprawdza, czy produkt o podanym ID istnieje i jest dostępny (stock > 0).

    Args:
        db_path (str): Ścieżka do pliku bazy danych.
        product_id (str): ID produktu.

    Returns:
        bool: True, jeśli produkt jest dostępny, False w przeciwnym razie.
    """
    try:
        initialize_excel_file(db_path)
        df = pd.read_excel(db_path, engine="openpyxl")
        product_id = str(product_id)
        product_row = df[df["id"].astype(str) == product_id]
        if product_row.empty:
            print(f"Produkt o ID {product_id} nie istnieje w bazie")
            return False
        stock = product_row["stock"].iloc[0]
        if stock <= 0:
            print(f"Produkt o ID {product_id} ma zerowy stan magazynowy")
            return False
        return True
    except PermissionError as e:
        print(f"Błąd uprawnień podczas sprawdzania dostępności: {e}")
        print("Sprawdź uprawnienia do pliku 'products.xlsx'.")
        return False
    except Exception as e:
        print(f"Błąd podczas sprawdzania dostępności produktu {product_id}: {e}")
        return False