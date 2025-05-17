import csv
import os
import datetime

CUSTOMER_FILE = "customer.csv"
DATABASE_DIR = "DATABASE"
LOGGED_USER = None


def load_customers():
    """Wczytuje klientów z pliku CSV jako listę słowników."""
    with open(CUSTOMER_FILE, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def save_customers(customers):
    """Zapisuje listę słowników klientów do pliku CSV."""
    with open(CUSTOMER_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "NAME", "E-MAIL", "PHONE", "CREATED", "UPDATED"])
        writer.writeheader()
        writer.writerows(customers)


def generate_new_id(customers):
    """Generuje nowe unikalne ID."""
    existing_ids = [int(c["ID"]) for c in customers if c["ID"].isdigit()]
    return str(max(existing_ids, default=200) + 1)


def register_customer(name, email, phone=None):
    """
    Rejestruje nowego klienta i zapisuje do bazy danych.

    :param name: Imię i nazwisko
    :param email: Adres e-mail
    :param phone: Numer telefonu (opcjonalnie)
    """
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


def remove_customer(identifier):
    """
    Usuwa klienta na podstawie ID lub nazwy.

    :param identifier: ID (str lub int) lub nazwa (str)
    """
    customers = load_customers()
    original_count = len(customers)

    customers = [c for c in customers if c["ID"] != str(identifier) and c["NAME"].lower() != str(identifier).lower()]
    save_customers(customers)

    if len(customers) < original_count:
        print(f"Usunięto klienta o identyfikatorze: {identifier}.")
    else:
        print(f"Nie znaleziono klienta o identyfikatorze: {identifier}.")


def login(email):
    """
    Loguje użytkownika po e-mailu.

    :param email: E-mail klienta
    :return: True jeśli znaleziono, False w przeciwnym razie
    """
    global LOGGED_USER
    customers = load_customers()
    for c in customers:
        if c["E-MAIL"].lower() == email.lower():
            LOGGED_USER = c
            print(f"Zalogowano jako {c['NAME']} (ID: {c['ID']})")
            return True
    print("Nie znaleziono użytkownika.")
    return False


def purchase_products(products):
    """
    Zapisuje zakupione produkty do pliku historii.

    :param products: Lista zakupionych produktów (str)
    """
    if not LOGGED_USER:
        print("Brak zalogowanego użytkownika.")
        return

    os.makedirs(DATABASE_DIR, exist_ok=True)
    history_file = os.path.join(DATABASE_DIR, f"{LOGGED_USER['ID']}_history.csv")
    now = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')

    with open(history_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if os.path.getsize(history_file) == 0:
            writer.writerow(["DATE", "PRODUCTS"])
        writer.writerow([now, ", ".join(products)])

    print(f"Zakup zapisany dla {LOGGED_USER['NAME']}.")


def get_customer_history(customer_id):
    """
    Wyświetla historię zakupów klienta.

    :param customer_id: ID klienta
    """
    history_file = os.path.join(DATABASE_DIR, f"{customer_id}_history.csv")
    if not os.path.exists(history_file):
        print("Brak historii zakupów dla tego klienta.")
        return

    print(f"Historia zakupów klienta {customer_id}:")
    with open(history_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(" | ".join(row))


# Przykład użycia
if __name__ == "__main__":
    register_customer("Anna Kowalska", "anna.k@example.com", "600700800")
    login("anna.k@example.com")
    purchase_products(["Milk", "Bread", "Butter"])
    get_customer_history(LOGGED_USER['ID'])
    remove_customer("Anna Kowalska")
