import csv
import os
import datetime
import pandas as pd
from product_management import  update_product_stock
CUSTOMER_FILE = "database/customer.csv"
DATABASE_DIR = "database/DATABASE"

def load_customers():
    """Wczytuje klientów z pliku CSV jako listę słowników."""
    try:
        with open(CUSTOMER_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            expected_headers = {"ID", "NAME", "E-MAIL", "PHONE", "CREATED", "UPDATED"}
            if not expected_headers.issubset(reader.fieldnames):
                raise ValueError(f"Nieprawidłowe nagłówki w pliku {CUSTOMER_FILE}. Oczekiwano: {expected_headers}")
            return list(reader)
    except FileNotFoundError:
        return []
    except PermissionError as e:
        print(f"Błąd uprawnień podczas odczytu pliku {CUSTOMER_FILE}: {e}")
        return []
    except ValueError as e:
        print(f"Błąd formatu pliku {CUSTOMER_FILE}: {e}")
        return []
    except Exception as e:
        print(f"Błąd podczas wczytywania klientów: {e}")
        return []

def save_customers(customers):
    """Zapisuje listę słowników klientów do pliku CSV."""
    try:
        os.makedirs(os.path.dirname(CUSTOMER_FILE), exist_ok=True)
        with open(CUSTOMER_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["ID", "NAME", "E-MAIL", "PHONE", "CREATED", "UPDATED"])
            writer.writeheader()
            writer.writerows(customers)
    except PermissionError as e:
        print(f"Błąd uprawnień podczas zapisu do pliku {CUSTOMER_FILE}: {e}")
        raise
    except Exception as e:
        print(f"Błąd podczas zapisu klientów: {e}")
        raise

def generate_new_id(customers):
    """Generuje nowe unikalne ID."""
    try:
        existing_ids = []
        for c in customers:
            id_value = c.get("ID", "")
            if id_value and id_value.isdigit():
                existing_ids.append(int(id_value))
            else:
                print(f"Pominięto nieprawidłowe ID: {id_value}")
        return str(max(existing_ids, default=200) + 1)
    except Exception as e:
        print(f"Błąd podczas generowania nowego ID: {e}")
        raise

def register_customer(name, email, phone=None):
    """
    Rejestruje nowego klienta i zapisuje do bazy danych.
    """
    try:
        customers = load_customers()
        new_id = generate_new_id(customers)
        now = datetime.date.today().isoformat()

        new_customer = {
            "ID": new_id,
            "NAME": name,
            "E-MAIL": email,
            "PHONE": phone or "",
            "CREATED": now,
            "UPDATED": now
        }

        customers.append(new_customer)
        save_customers(customers)
        print(f"Zarejestrowano klienta {name} z ID {new_id}.")
        return new_id
    except PermissionError as e:
        print(f"Błąd uprawnień podczas rejestracji klienta: {e}")
        return None
    except Exception as e:
        print(f"Błąd podczas rejestracji klienta: {e}")
        return None

def remove_customer(identifier):
    """
    Usuwa klienta na podstawie ID lub nazwy.
    """
    try:
        customers = load_customers()
        original_count = len(customers)

        customers = [c for c in customers if c["ID"] != str(identifier) and c["NAME"].lower() != str(identifier).lower()]
        save_customers(customers)

        if len(customers) < original_count:
            print(f"Usunięto klienta o identyfikatorze: {identifier}.")
            return True
        else:
            print(f"Nie znaleziono klienta o identyfikatorze: {identifier}.")
            return False
    except PermissionError as e:
        print(f"Błąd uprawnień podczas usuwania klienta: {e}")
        return False
    except Exception as e:
        print(f"Błąd podczas usuwania klienta: {e}")
        return False

def login(email):
    """
    Loguje użytkownika po e-mailu.
    """
    customers = load_customers()
    for c in customers:
        if c["E-MAIL"].lower() == email.lower():
            print(f"Zalogowano jako {c['NAME']} (ID: {c['ID']})")
            return c
    print("Nie znaleziono użytkownika.")
    return None


def purchase_products(cart, user):
    """
    Zapisuje zakupione produkty do pliku historii i aktualizuje stan magazynowy.
    """
    if not user:
        print("Brak zalogowanego użytkownika.")
        return None

    try:
        products_df = pd.read_excel("database/products.xlsx", engine="openpyxl")
        total_price = 0.0
        purchase_details = []

        for product_id, quantity in cart:
            product = products_df[products_df['id'] == product_id]
            if product.empty:
                print(f"Produkt o ID {product_id} nie istnieje.")
                return None
            stock = int(product['stock'].iloc[0])
            if quantity > stock:
                print(f"Brak wystarczającej ilości produktu {product['name'].iloc[0]} (dostępne: {stock}).")
                return None

        for product_id, quantity in cart:
            product = products_df[products_df['id'] == product_id]
            product_name = product['name'].iloc[0]
            price = float(product['price'].iloc[0])
            total_price += price * quantity
            purchase_details.append(f"{product_name} (ID: {product_id}, Ilość: {quantity}, Cena: {price:.2f})")

            if not update_product_stock("database/products.xlsx", product_id, -quantity):
                print(f"Nie udało się zaktualizować stanu dla produktu {product_name}")
                return None

        os.makedirs(DATABASE_DIR, exist_ok=True)
        history_file = os.path.join(DATABASE_DIR, f"{user['ID']}_history.csv")
        now = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')

        with open(history_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if os.path.getsize(history_file) == 0:
                writer.writerow(["DATE", "PRODUCTS", "TOTAL_PRICE"])
            writer.writerow([now, "; ".join(purchase_details), f"{total_price:.2f}"])

        print(f"Zakup zapisany dla {user['NAME']} (Całkowita cena: {total_price:.2f}).")
        return total_price
    except PermissionError as e:
        print(f"Błąd uprawnień podczas zapisu historii zakupów: {e}")
        return None
    except Exception as e:
        print(f"Błąd podczas zapisu historii zakupów: {e}")
        return None
