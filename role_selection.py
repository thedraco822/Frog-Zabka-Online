import tkinter as tk
from gui import create_gui
from user_gui import create_user_gui

def create_role_selection_window(root, admin_callback, user_callback):
    """
    Tworzy okno wyboru roli (Admin lub Użytkownik).

    Args:
        root (tk.Tk): Główne okno Tkinter.
        admin_callback (callable): Funkcja wywoływana po wyborze roli Admin.
        user_callback (callable): Funkcja wywoływana po wyborze roli Użytkownik.
    """
    root.title("Żabka Online - Wybór roli")
    root.geometry("300x200")

    def select_admin():
        root.destroy() 
        admin_callback() 

    def select_user():
        root.destroy()  
        user_callback()

    tk.Label(root, text="Wybierz rolę:", font=("Arial", 14, "bold")).pack(pady=20)

    tk.Button(root, text="Admin", command=select_admin, width=15, font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="Użytkownik", command=select_user, width=15, font=("Arial", 12)).pack(pady=10)
