import tkinter as tk
from tkinter import messagebox, ttk
import csv
from projekt_customers import login, purchase_products
from product_management import get_all_products, check_product_availability

def create_user_gui(root):
    """
    Tworzy GUI dla użytkownika z ekranem logowania i panelem głównym.
    """
    root.title("Żabka Online - Panel Użytkownika")
    root.geometry("500x400")
    logged_in_user = None
    cart = []

    def clear_window():
        """Czyści wszystkie widżety w oknie."""
        for widget in root.winfo_children():
            widget.destroy()

    def show_login_screen():
        """Wyświetla ekran logowania."""
        nonlocal logged_in_user, cart
        logged_in_user = None
        cart = []
        clear_window()
        tk.Label(root, text="Logowanie użytkownika", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Label(root, text="E-mail:", font=("Arial", 12)).pack()
        email_entry = tk.Entry(root, width=30)
        email_entry.pack(pady=5)

        def try_login():
            nonlocal logged_in_user
            email = email_entry.get().strip()
            if not email:
                messagebox.showerror("Błąd", "Proszę podać adres e-mail.")
                return
            user = login(email)
            if user:
                logged_in_user = user
                show_main_panel()
            else:
                messagebox.showerror("Błąd", "Nie znaleziono użytkownika o podanym e-mailu.")

        tk.Button(root, text="Zaloguj", command=try_login, font=("Arial", 12), width=15).pack(pady=10)

    def show_main_panel():
        """Wyświetla główny panel użytkownika po zalogowaniu."""
        clear_window()
        tk.Label(root, text=f"Witaj, {logged_in_user['NAME']}!", font=("Arial", 14, "bold")).pack(pady=20)

        # Sekcja zakupów
        tk.Label(root, text="Zakupy", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(root, text="Wybierz produkt:", font=("Arial", 10)).pack()
        products = get_all_products("database/products.xlsx")
        product_names = [f"{p['name']} (ID: {p['id']}, Cena: {p['price']:.2f}, Dostępne: {p['stock']})" for p in products]
        product_combobox = ttk.Combobox(root, values=product_names, width=50, state="readonly")
        product_combobox.pack(pady=5)
        if products:
            product_combobox.current(0)

        tk.Label(root, text="Ilość:", font=("Arial", 10)).pack()
        quantity_combobox = ttk.Combobox(root, values=[str(i) for i in range(1, 11)], width=10, state="readonly")
        quantity_combobox.pack(pady=5)
        if quantity_combobox['values']:
            quantity_combobox.current(0)

        def update_quantity_options(_):
            """Aktualizuje opcje ilości na podstawie wybranego produktu."""
            if not products or not product_combobox.get():
                quantity_combobox['values'] = [str(i) for i in range(1, 11)]
                if quantity_combobox['values']:
                    quantity_combobox.current(0)
                return
            selected_index = product_combobox.current()
            stock = products[selected_index]['stock']
            max_quantity = min(stock, 10)  # Maksymalnie 10 sztuk
            quantity_combobox['values'] = [str(i) for i in range(1, max_quantity + 1)]
            if quantity_combobox['values']:
                quantity_combobox.current(0)

        product_combobox.bind("<<ComboboxSelected>>", update_quantity_options)

        def add_to_cart():
            """Dodaje wybrany produkt i ilość do koszyka."""
            nonlocal cart
            if not products or not product_combobox.get():
                messagebox.showerror("Błąd", "Proszę wybrać produkt.")
                return
            selected_index = product_combobox.current()
            product = products[selected_index]
            quantity = int(quantity_combobox.get())
            if not check_product_availability("database/products.xlsx", product['id'], quantity):
                messagebox.showerror("Błąd", f"Brak wystarczającej ilości produktu {product['name']} (dostępne: {product['stock']}).")
                return
            cart.append((product['id'], quantity))
            messagebox.showinfo("Sukces", f"Dodano {quantity} x {product['name']} do koszyka.")

        tk.Button(root, text="Dodaj do koszyka", command=add_to_cart, font=("Arial", 10), width=15).pack(pady=5)

        tk.Label(root, text="Koszyk i historia", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(root, text="Pokaż koszyk", command=show_cart, font=("Arial", 10), width=15).pack(pady=5)
        tk.Button(root, text="Pokaż historię", command=show_history, font=("Arial", 10), width=15).pack(pady=5)

        tk.Button(root, text="Wyloguj", command=show_login_screen, font=("Arial", 10), width=15).pack(pady=20)

    def show_cart():
        """Wyświetla koszyk z wybranymi produktami i całkowitą ceną."""
        cart_window = tk.Toplevel(root)
        cart_window.title("Koszyk")
        cart_window.geometry("700x500")

        tree = ttk.Treeview(cart_window, columns=("ID", "Name", "Quantity", "Price", "Total"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Nazwa")
        tree.heading("Quantity", text="Ilość")
        tree.heading("Price", text="Cena jednostkowa")
        tree.heading("Total", text="Cena całkowita")
        tree.column("ID", width=50)
        tree.column("Name", width=200)
        tree.column("Quantity", width=80)
        tree.column("Price", width=120)
        tree.column("Total", width=120)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar_y = ttk.Scrollbar(cart_window, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar_y.set)

        products = get_all_products("database/products.xlsx")
        total_cart_price = 0.0
        for product_id, quantity in cart:
            product = next((p for p in products if p['id'] == product_id), None)
            if product:
                price = float(product['price'])
                total_price = price * quantity
                total_cart_price += total_price
                tree.insert("", "end", values=(
                    product['id'],
                    product['name'],
                    quantity,
                    f"{price:.2f}",
                    f"{total_price:.2f}"
                ))

        tk.Label(cart_window, text=f"Całkowita cena: {total_cart_price:.2f} PLN", font=("Arial", 12, "bold")).pack(pady=10)

        def save_purchase():
            nonlocal cart
            if not cart:
                messagebox.showerror("Błąd", "Koszyk jest pusty.")
                return
            total_price = purchase_products(cart, logged_in_user)
            if total_price is not None:
                messagebox.showinfo("Sukces", f"Zakup zapisany! Całkowita cena: {total_price:.2f} PLN")
                cart = []  # Wyczyść koszyk
                cart_window.destroy()
            else:
                messagebox.showerror("Błąd", "Nie udało się zapisać zakupu. Sprawdź dostępność produktów lub uprawnienia.")

        tk.Button(cart_window, text="Zapisz zakup", command=save_purchase, font=("Arial", 10), width=15).pack(pady=10)

    def show_history():
        """Wyświetla historię zakupów w osobnym oknie."""
        history_window = tk.Toplevel(root)
        history_window.title("Historia zakupów")
        history_window.geometry("600x400")

        tree = ttk.Treeview(history_window, columns=("Date", "Products", "TotalPrice"), show="headings")
        tree.heading("Date", text="Data")
        tree.heading("Products", text="Produkty")
        tree.heading("TotalPrice", text="Całkowita cena")
        tree.column("Date", width=200)
        tree.column("Products", width=300)
        tree.column("TotalPrice", width=100)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar_y = ttk.Scrollbar(history_window, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar_y.set)

        history_file = f"database/DATABASE/{logged_in_user['ID']}_history.csv"
        try:
            with open(history_file, newline='', encoding='utf-8') as f:
                next(f, None)  # Pomija nagłówek
                for row in f:
                    values = row.strip().split(',')
                    tree.insert("", "end", values=(values[0], values[1], values[2]))
        except FileNotFoundError:
            messagebox.showinfo("Informacja", "Brak historii zakupów.")
            history_window.destroy()
        except PermissionError as e:
            messagebox.showerror("Błąd", f"Brak uprawnień do pliku historii: {e}")
            history_window.destroy()
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas wczytywania historii: {e}")
            history_window.destroy()

    # Uruchom ekran logowania przy starcie
    show_login_screen()
