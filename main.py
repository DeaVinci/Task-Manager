from zadania import ManagerZadan, Zadanie, ZadaniePriorytetowe, ZadanieRegularne
from datetime import datetime

def menu():
    print("\n=== Menedżer Zadań ===")
    print("1. Dodaj zadanie")
    print("2. Usuń zadanie")
    print("3. Oznacz jako wykonane")
    print("4. Edytuj zadanie")
    print("5. Wyświetl zadania")
    print("6. Wyjdź")

def wprowadz_date():
    while True:
        termin = input("Podaj termin wykonania (YYYY-MM-DD) [domyślnie 2025-04-20]: ")
        if not termin:
            return "2025-04-20"
        try:
            datetime.strptime(termin, "%Y-%m-%d")
            return termin
        except ValueError:
            print("Błąd: Niepoprawny format daty!")

manager = ManagerZadan()
manager.wczytaj_z_pliku()

while True:
    menu()
    wybor = input("Wybierz opcję: ")

    if wybor == "1":
        tytul = input("Podaj tytuł: ")
        opis = input("Podaj opis: ")
        termin = wprowadz_date()
        lokalizacja = input("Lokalizacja (opcjonalnie): ")
        kategoria = input("Kategoria (opcjonalnie): ")

        typ = input("Typ zadania (1 - Priorytetowe, 2 - Regularne, Enter - Zwykłe): ")

        kwargs = {}
        if lokalizacja:
            kwargs["lokalizacja"] = lokalizacja
        if kategoria:
            kwargs["kategoria"] = kategoria

        if typ == "1":
            priorytet = int(input("Podaj priorytet (1-5): "))
            zadanie = ZadaniePriorytetowe(tytul, opis, termin, priorytet, **kwargs)
        elif typ == "2":
            powtarzalnosc = input("Podaj powtarzalność: ")
            zadanie = ZadanieRegularne(tytul, opis, termin, powtarzalnosc, **kwargs)
        else:
            zadanie = Zadanie(tytul, opis, termin, **kwargs)

        manager.dodaj_zadanie(zadanie)
        manager.zapisz_do_pliku()
        print("Dodano zadanie.")

    elif wybor == "2":
        tytul = input("Podaj tytuł zadania do usunięcia: ")
        if tytul in manager:
            manager.usun_zadanie(tytul)
            manager.zapisz_do_pliku()
            print("Zadanie usunięte.")
        else:
            print("Nie znaleziono zadania.")

    elif wybor == "3":
        tytul = input("Podaj tytuł zadania do oznaczenia jako wykonane: ")
        if manager.oznacz_jako_wykonane(tytul):
            manager.zapisz_do_pliku()
            print("Zadanie oznaczone jako wykonane.")
        else:
            print("Nie znaleziono zadania.")

    elif wybor == "4":
        tytul = input("Podaj tytuł zadania do edycji: ")
        if tytul in manager:
            nowy_tytul = input("Nowy tytuł (Enter by nie zmieniać): ")
            nowy_opis = input("Nowy opis (Enter by nie zmieniać): ")
            nowy_termin = input("Nowy termin (YYYY-MM-DD) (Enter by nie zmieniać): ")
            manager.edytuj_zadanie(tytul,
                                    nowy_tytul or None,
                                    nowy_opis or None,
                                    nowy_termin or None)
            manager.zapisz_do_pliku()
            print("Zadanie zaktualizowane.")
        else:
            print("Nie znaleziono zadania.")

    elif wybor == "5":
        manager.wyswietl_zadania()

    elif wybor == "6":
        print("Zamykanie aplikacji...")
        manager.zapisz_do_pliku()
        break

    else:
        print("Nieprawidłowa opcja, spróbuj ponownie.")
