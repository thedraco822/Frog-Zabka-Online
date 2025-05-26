import pandas as pd
import os

def add_product(file_path, product_data):
    """
    Dodaje produkt do pliku Excel.
    """
    try:
        if os.path.exists(file_path):
            df = pd.read_excel(file_path, engine='openpyxl')
        else:
            df = pd.DataFrame(columns=['id', 'name', 'price', 'stock'])

        if product_data['id'] in df['id'].values:
            print(f"Produkt o ID {product_data['id']} już istnieje.")
            return False

        new_row = pd.DataFrame([product_data])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(file_path, index=False, engine='openpyxl')
        print(f"Dodano produkt: {product_data['name']}")
        return True
    except PermissionError as e:
        print(f"Błąd uprawnień podczas zapisu do pliku {file_path}: {e}")
        return False
    except Exception as e:
        print(f"Błąd podczas dodawania produktu: {e}")
        return False

def remove_product(file_path, identifier, by='id'):
    """
    Usuwa produkt na podstawie ID lub nazwy.
    """
    try:
        if not os.path.exists(file_path):
            print(f"Plik {file_path} nie istnieje.")
            return False

        df = pd.read_excel(file_path, engine='openpyxl')
        if df.empty:
            print("Brak produktów do usunięcia.")
            return False

        if by == 'id':
            try:
                identifier = int(identifier)
            except ValueError:
                print(f"Nieprawidłowy format ID: {identifier}")
                return False
            original_len = len(df)
            df = df[df['id'] != identifier]
            if len(df) < original_len:
                df.to_excel(file_path, index=False, engine='openpyxl')
                print(f"Usunięto produkt o ID {identifier}.")
                return True
            else:
                print(f"Nie znaleziono produktu o ID {identifier}.")
                return False
        elif by == 'name':
            original_len = len(df)
            df = df[df['name'].str.lower() != identifier.lower()]
            if len(df) < original_len:
                df.to_excel(file_path, index=False, engine='openpyxl')
                print(f"Usunięto produkt o nazwie {identifier}.")
                return True
            else:
                print(f"Nie znaleziono produktu o nazwie {identifier}.")
                return False
        else:
            print(f"Nieprawidłowy typ identyfikatora: {by}")
            return False
    except PermissionError as e:
        print(f"Błąd uprawnień podczas zapisu do pliku {file_path}: {e}")
        return False
    except Exception as e:
        print(f"Błąd podczas usuwania produktu: {e}")
        return False

def get_product_stats(file_path):
    """
    Zwraca statystyki produktów.
    """
    try:
        if not os.path.exists(file_path):
            print(f"Plik {file_path} nie istnieje.")
            return {}

        df = pd.read_excel(file_path, engine='openpyxl')
        if df.empty:
            print("Brak produktów do analizy.")
            return {}

        stats = {
            'min_price': df['price'].min(),
            'max_price': df['price'].max(),
            'avg_price': df['price'].mean(),
            'min_stock': df['stock'].min(),
            'max_stock': df['stock'].max(),
            'avg_stock': df['stock'].mean()
        }
        return stats
    except PermissionError as e:
        print(f"Błąd uprawnień podczas odczytu pliku {file_path}: {e}")
        return {}
    except Exception as e:
        print(f"Błąd podczas obliczania statystyk: {e}")
        return {}

def check_product_availability(file_path, product_id, quantity=1):
    """
    Sprawdza dostępność produktu na podstawie ID.
    """
    try:
        if not os.path.exists(file_path):
            print(f"Plik {file_path} nie istnieje.")
            return False

        df = pd.read_excel(file_path, engine='openpyxl')
        product = df[df['id'] == product_id]
        if product.empty:
            print(f"Produkt o ID {product_id} nie istnieje.")
            return False

        stock = product['stock'].iloc[0]
        return stock >= quantity
    except PermissionError as e:
        print(f"Błąd uprawnień podczas odczytu pliku {file_path}: {e}")
        return False
    except Exception as e:
        print(f"Błąd podczas sprawdzania dostępności: {e}")
        return False

def get_all_products(file_path):
    """
    Zwraca listę wszystkich produktów jako słowniki.
    """
    try:
        if not os.path.exists(file_path):
            print(f"Plik {file_path} nie istnieje.")
            return []

        df = pd.read_excel(file_path, engine='openpyxl')
        if df.empty:
            print("Brak produktów.")
            return []

        products = df.to_dict('records')
        return products
    except PermissionError as e:
        print(f"Błąd uprawnień podczas odczytu pliku {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Błąd podczas wczytywania produktów: {e}")
        return []


def update_product_stock(file_path, product_id, quantity_change):
    """
    Aktualizuje stan magazynowy produktu.

    Args:
        file_path (str): Ścieżka do pliku z produktami.
        product_id (int): ID produktu.
        quantity_change (int): Zmiana stanu (ujemna dla zmniejszenia).

    Returns:
        bool: True jeśli aktualizacja się powiodła, False w przeciwnym razie.
    """
    try:
        if not os.path.exists(file_path):
            print(f"Plik {file_path} nie istnieje.")
            return False

        df = pd.read_excel(file_path, engine='openpyxl')
        product_index = df[df['id'] == product_id].index
        if len(product_index) == 0:
            print(f"Produkt o ID {product_id} nie istnieje.")
            return False

        current_stock = df.at[product_index[0], 'stock']
        new_stock = current_stock + quantity_change
        if new_stock < 0:
            print("Nie można zaktualizować stanu - wynikowy stan byłby ujemny.")
            return False

        df.at[product_index[0], 'stock'] = new_stock
        df.to_excel(file_path, index=False, engine='openpyxl')
        return True
    except PermissionError as e:
        print(f"Błąd uprawnień podczas aktualizacji stanu: {e}")
        return False
    except Exception as e:
        print(f"Błąd podczas aktualizacji stanu: {e}")
        return False
