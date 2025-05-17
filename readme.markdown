# Pakiet Frog - Żabka Online

## Opis
Pakiet Frog to aplikacja do zarządzania sklepem online Żabka. Umożliwia zarządzanie produktami, klientami oraz zakupami. Zawiera Partyjnie zawiera interfejs graficzny, system rabatowy, podgląd danych, statystyki produktów, historię zakupów oraz dokumentację.

## Struktura
- `main.py`: Główny moduł uruchamiający aplikację.
- `product_management.py`: Moduł zarządzania produktami (dodawanie, usuwanie, statystyki).
- `customer_management.py`: Moduł zarządzania klientami (rejestracja, usuwanie, zakupy).
- `utils.py`: Funkcje pomocnicze (logowanie, rabaty).
- `gui.py`: Interfejs graficzny.
- `database/`: Folder z danymi (products.xlsx, customer.csv, DATABASE/).

## Wymagania
- Python 3.8+
- Biblioteki: pandas, openpyxl, tkinter

## Instalacja
1. Sklonuj repozytorium: `git clone <URL>`
2. Zainstaluj zależności: `pip install pandas openpyxl`
3. Uruchom aplikację: `python main.py`

## Funkcjonalności
- Dodawanie i usuwanie produktów oraz klientów
- Zakup wielu produktów z rabatem
- Statystyki produktów (min, max, średnia cena i stan magazynowy)
- Historia zakupów klientów
- Sprawdzenie dostępności produktu
- Interfejs graficzny z podglądem produktów i klientów

## Autorzy
- Karol Filipkowski: Koordynacja, GUI, moduł główny
- Eryk Gawryjołek: Zarządzanie produktami, statystyki
- Arina Dzyuba: Zarządzanie klientami, zakupy