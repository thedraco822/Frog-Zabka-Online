# Pakiet Frog - Żabka Online

## Opis
Pakiet Frog to aplikacja do zarządzania sklepem online Żabka, umożliwiająca zarządzanie produktami, klientami oraz zakupami. Aplikacja zawiera intuicyjny interfejs graficzny, system rabatowy, podgląd danych, statystyki produktów, historię zakupów oraz aktualizację stanów magazynowych po zakupach. Ostatnia aktualizacja: 18 maja 2025, 23:48 CEST.

## Struktura
- `main.py`: Główny moduł uruchamiający aplikację z wyborem roli (Admin/Użytkownik).
- `product_management.py`: Moduł zarządzania produktami (dodawanie, usuwanie, statystyki, sprawdzanie dostępności, aktualizacja stanów magazynowych).
- `projekt_customers.py`: Moduł zarządzania klientami (rejestracja, usuwanie, zakupy z aktualizacją stanów).
- `utils.py`: Funkcje pomocnicze (logowanie akcji, obliczanie rabatów).
- `gui.py`: Interfejs graficzny dla roli Admin.
- `user_gui.py`: Interfejs graficzny dla roli Użytkownik.
- `role_selection.py`: Moduł wyboru roli użytkownika.
- `database/`: Folder z danymi (products.xlsx, customer.csv, DATABASE/ z historią zakupów).

## Wymagania
- Python 3.8+
- Biblioteki: pandas, openpyxl, tkinter

## Instalacja
1. Sklonuj repozytorium: `git clone <URL>`
2. Zainstaluj zależności: `pip install pandas openpyxl`
3. Uruchom aplikację: `python main.py`

## Funkcjonalności
- **Zarządzanie produktami**: Dodawanie i usuwanie produktów, podgląd, statystyki (min, max, średnia cena i stan magazynowy).
- **Zarządzanie klientami**: Rejestracja, usuwanie, logowanie.
- **Zakupy**: Dodawanie produktów do koszyka, zakup z uwzględnieniem rabatów, automatyczna aktualizacja stanów magazynowych po zakupie.
- **Statystyki produktów**: Wyświetlanie minimalnej, maksymalnej i średniej ceny oraz stanu magazynowego.
- **Historia zakupów**: Przeglądanie zapisanej historii zakupów dla każdego klienta.
- **Sprawdzenie dostępności**: Weryfikacja dostępności produktów przed zakupem.
- **Interfejs graficzny**: Intuicyjne GUI dla obu ról z podglądem produktów i klientów.

## Autorzy
- Karol Filipkowski: Koordynacja, GUI, moduł główny
- Eryk Gawryjołek: Zarządzanie produktami, statystyki
- Arina Dzyuba: Zarządzanie klientami, zakupy