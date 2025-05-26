import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

def create_gui(root: tk.Tk, add_product, remove_product, register_customer, remove_customer, get_product_stats, check_product_availability):
    """
    Tworzy interfejs graficzny dla aplikacji.

    Args:
        root (tk.Tk): Główne okno Tkinter.
        add_product, remove_product, register_customer, remove_customer: Funkcje do obsługi produktów i klientów.
        get_product_stats, check_product_availability: Funkcje do zarządzania produktami.
    """
    root.title("Żabka Online - Pakiet Frog")

    def add_product_gui():
        try:
            product_data = {
                "id": entry_product_id.get().strip(),
                "name": entry_product_name.get().strip(),
                "price": float(entry_product_price.get().strip()),
                "stock": int(entry_product_stock.get().strip())
            }
            if not product_data["id"] or not product_data["name"]:
                messagebox.showerror("Błąd", "ID i nazwa produktu nie mogą być puste.")
                return
            success = add_product("database/products.xlsx", product_data)
            if success:
                messagebox.showinfo("Sukces", "Produkt dodany!")
            else:
                messagebox.showerror("Błąd", "Nie udało się dodać produktu. Sprawdź uprawnienia do pliku products.xlsx.")
        except ValueError as e:
            messagebox.showerror("Błąd", f"Nieprawidłowe dane: {str(e)}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas dodawania produktu: {str(e)}")

    def remove_product_gui():
        try:
            product_id = entry_remove_product_id.get().strip()
            product_name = entry_remove_product_name.get().strip()
            if product_id and product_name:
                messagebox.showerror("Błąd", "Proszę podać tylko ID lub nazwę, nie oba.")
                return
            if not product_id and not product_name:
                messagebox.showerror("Błąd", "Proszę podać ID lub nazwę produktu.")
                return
            if product_id:
                success = remove_product("database/products.xlsx", product_id, by="id")
                criterion = f"ID {product_id}"
            else:
                success = remove_product("database/products.xlsx", product_name, by="name")
                criterion = f"nazwie {product_name}"
            if success:
                messagebox.showinfo("Sukces", f"Produkt usunięty na podstawie {criterion}!")
            else:
                messagebox.showerror("Błąd", f"Nie udało się usunąć produktu o {criterion}.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas usuwania produktu: {str(e)}")

    def register_customer_gui():
        try:
            name = entry_customer_name.get().strip()
            email = entry_customer_email.get().strip()
            phone = entry_customer_phone.get().strip() or None
            if not name or not email:
                messagebox.showerror("Błąd", "Imię i e-mail klienta nie mogą być puste.")
                return
            customer_id = register_customer(name, email, phone)
            if customer_id:
                messagebox.showinfo("Sukces", f"Zarejestrowano klienta z ID: {customer_id}")
            else:
                messagebox.showerror("Błąd", "Nie udało się zarejestrować klienta. Sprawdź uprawnienia do pliku customer.csv.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas rejestracji klienta: {str(e)}")

    def remove_customer_gui():
        try:
            customer_id = entry_remove_customer_id.get().strip()
            customer_name = entry_remove_customer_name.get().strip()
            if customer_id and customer_name:
                messagebox.showerror("Błąd", "Proszę podać tylko ID lub imię, nie oba.")
                return
            if not customer_id and not customer_name:
                messagebox.showerror("Błąd", "Proszę podać ID lub imię klienta.")
                return
            identifier = customer_id or customer_name
            success = remove_customer(identifier)
            criterion = f"ID {customer_id}" if customer_id else f"nazwie {customer_name}"
            if success:
                messagebox.showinfo("Sukces", f"Klient usunięty na podstawie {criterion}!")
            else:
                messagebox.showerror("Błąd", f"Nie udało się usunąć klienta o {criterion}.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas usuwania klienta: {str(e)}")

    def show_product_stats():
        try:
            stats = get_product_stats("database/products.xlsx")
            if not stats:
                messagebox.showerror("Błąd", "Nie udało się pobrać statystyk produktów. Plik products.xlsx może być pusty lub niedostępny.")
                return
            stats = {k: (v if pd.notna(v) else 0) for k, v in stats.items()}
            stats_message = (
                f"Statystyki produktów:\n"
                f"Minimalna cena: {stats['min_price']:.2f}\n"
                f"Maksymalna cena: {stats['max_price']:.2f}\n"
                f"Średnia cena: {stats['avg_price']:.2f}\n"
                f"Minimalny stan: {stats['min_stock']}\n"
                f"Maksymalny stan: {stats['max_stock']}\n"
                f"Średni stan: {stats['avg_stock']:.2f}"
            )
            messagebox.showinfo("Statystyki produktów", stats_message)
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas pobierania statystyk: {str(e)}")


    def preview_file(file_path, title, columns):
        try:
            preview_window = tk.Toplevel(root)
            preview_window.title(title)
            preview_window.geometry("600x400")

            tree = ttk.Treeview(preview_window, columns=columns, show="headings")
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor="center")
            tree.pack(fill="both", expand=True, padx=10, pady=10)

            scrollbar_y = ttk.Scrollbar(preview_window, orient="vertical", command=tree.yview)
            scrollbar_y.pack(side="right", fill="y")
            tree.configure(yscrollcommand=scrollbar_y.set)

            scrollbar_x = ttk.Scrollbar(preview_window, orient="horizontal", command=tree.xview)
            scrollbar_x.pack(side="bottom", fill="x")
            tree.configure(xscrollcommand=scrollbar_x.set)

            if file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path, engine="openpyxl")
            else:
                df = pd.read_csv(file_path)
            if df.empty:
                messagebox.showinfo("Informacja", "Plik jest pusty.")
                preview_window.destroy()
                return
            for _, row in df.iterrows():
                tree.insert("", "end", values=[row[col] for col in columns])
        except FileNotFoundError:
            messagebox.showerror("Błąd", f"Plik {file_path} nie istnieje.")
            preview_window.destroy()
        except PermissionError:
            messagebox.showerror("Błąd", f"Brak uprawnień do pliku {file_path}.")
            preview_window.destroy()
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas wczytywania pliku: {str(e)}")
            preview_window.destroy()

    def preview_products():
        preview_file("database/products.xlsx", "Podgląd produktów", ["id", "name", "price", "stock"])

    def preview_customers():
        preview_file("database/customer.csv", "Podgląd klientów", ["ID", "NAME", "E-MAIL", "PHONE"])

    tk.Label(root, text="Dodaj produkt", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
    tk.Label(root, text="ID:").grid(row=1, column=0, sticky="e")
    tk.Label(root, text="Nazwa:").grid(row=2, column=0, sticky="e")
    tk.Label(root, text="Cena:").grid(row=3, column=0, sticky="e")
    tk.Label(root, text="Stan:").grid(row=4, column=0, sticky="e")

    entry_product_id = tk.Entry(root)
    entry_product_name = tk.Entry(root)
    entry_product_price = tk.Entry(root)
    entry_product_stock = tk.Entry(root)

    entry_product_id.grid(row=1, column=1, pady=2)
    entry_product_name.grid(row=2, column=1, pady=2)
    entry_product_price.grid(row=3, column=1, pady=2)
    entry_product_stock.grid(row=4, column=1, pady=2)

    tk.Button(root, text="Dodaj produkt", command=add_product_gui).grid(row=5, column=0, columnspan=2, pady=10)

    tk.Label(root, text="Usuń produkt", font=("Arial", 12, "bold")).grid(row=6, column=0, columnspan=2, pady=5)
    tk.Label(root, text="ID:").grid(row=7, column=0, sticky="e")
    tk.Label(root, text="Nazwa:").grid(row=8, column=0, sticky="e")

    entry_remove_product_id = tk.Entry(root)
    entry_remove_product_name = tk.Entry(root)

    entry_remove_product_id.grid(row=7, column=1, pady=2)
    entry_remove_product_name.grid(row=8, column=1, pady=2)

    tk.Button(root, text="Usuń produkt", command=remove_product_gui).grid(row=9, column=0, columnspan=2, pady=10)

    tk.Label(root, text="Statystyki produktów", font=("Arial", 12, "bold")).grid(row=10, column=0, columnspan=2, pady=5)
    tk.Button(root, text="Pokaż statystyki", command=show_product_stats).grid(row=11, column=0, columnspan=2, pady=5)

    tk.Label(root, text="Rejestracja klienta", font=("Arial", 12, "bold")).grid(row=0, column=2, columnspan=2, pady=5)
    tk.Label(root, text="Imię i nazwisko:").grid(row=1, column=2, sticky="e")
    tk.Label(root, text="E-mail:").grid(row=2, column=2, sticky="e")
    tk.Label(root, text="Telefon (opcjonalnie):").grid(row=3, column=2, sticky="e")

    entry_customer_name = tk.Entry(root)
    entry_customer_email = tk.Entry(root)
    entry_customer_phone = tk.Entry(root)

    entry_customer_name.grid(row=1, column=3, pady=2)
    entry_customer_email.grid(row=2, column=3, pady=2)
    entry_customer_phone.grid(row=3, column=3, pady=2)

    tk.Button(root, text="Zarejestruj klienta", command=register_customer_gui).grid(row=4, column=2, columnspan=2, pady=10)

    tk.Label(root, text="Usuń klienta", font=("Arial", 12, "bold")).grid(row=5, column=2, columnspan=2, pady=5)
    tk.Label(root, text="ID:").grid(row=6, column=2, sticky="e")
    tk.Label(root, text="Imię i nazwisko:").grid(row=7, column=2, sticky="e")

    entry_remove_customer_id = tk.Entry(root)
    entry_remove_customer_name = tk.Entry(root)

    entry_remove_customer_id.grid(row=6, column=3, pady=2)
    entry_remove_customer_name.grid(row=7, column=3, pady=2)

    tk.Button(root, text="Usuń klienta", command=remove_customer_gui).grid(row=8, column=2, columnspan=2, pady=10)

    tk.Label(root, text="Podgląd danych", font=("Arial", 12, "bold")).grid(row=9, column=2, columnspan=2, pady=5)
    tk.Button(root, text="Podgląd produktów", command=preview_products).grid(row=10, column=2, columnspan=2, pady=5)
    tk.Button(root, text="Podgląd klientów", command=preview_customers).grid(row=11, column=2, columnspan=2, pady=5)
