import tkinter as tk
from role_selection import create_role_selection_window, create_user_gui
from gui import create_gui
from product_management import add_product, remove_product, get_product_stats, check_product_availability
from projekt_customers import register_customer, remove_customer

def start_admin_gui():
    """Uruchamia GUI dla administratora."""
    admin_root = tk.Tk()
    create_gui(
        admin_root,
        add_product,
        remove_product,
        register_customer,
        remove_customer,
        get_product_stats,
        check_product_availability
    )
    admin_root.mainloop()

def start_user_gui():
    """Uruchamia GUI dla użytkownika."""
    user_root = tk.Tk()
    create_user_gui(user_root)
    user_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    create_role_selection_window(root, start_admin_gui, start_user_gui)
    root.mainloop()