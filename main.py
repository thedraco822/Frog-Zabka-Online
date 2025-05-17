import tkinter as tk
from gui import create_gui
from product_management import add_product, remove_product, get_product_stats, check_product_availability
from customer_management import register_customer, remove_customer

if __name__ == "__main__":
    root = tk.Tk()
    create_gui(
        root,
        add_product,
        remove_product,
        register_customer,
        remove_customer,
        get_product_stats,
        check_product_availability
    )
    root.mainloop()