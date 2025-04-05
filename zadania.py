from datetime import datetime
import time

def zmierz_czas(func):
    """
    Dekorator mierzący czas wykonania funkcji.
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        wynik = func(*args, **kwargs)
        end = time.time()
        print(f"⏱ Funkcja '{func.__name__}' wykonała się w {end - start:.4f} sekundy.")
        return wynik
    return wrapper


class Zadanie:
    """
    Klasa bazowa reprezentująca ogólne zadanie.
    """
    def __init__(self, tytul, opis, termin_wykonania="2025-04-20", **kwargs):
        self.tytul = tytul
        self.opis = opis
        self.termin_wykonania = datetime.strptime(termin_wykonania, "%Y-%m-%d")
        self.wykonane = False
        self.dodatkowe = kwargs

    def oznacz_jako_wykonane(self):
        """Oznacza zadanie jako wykonane."""
        self.wykonane = True

    def edytuj(self, nowy_tytul=None, nowy_opis=None, nowy_termin=None):
        """
        Edytuje zadanie (zmienia tylko podane dane).
        """
        if nowy_tytul:
            self.tytul = nowy_tytul
        if nowy_opis:
            self.opis = nowy_opis
        if nowy_termin:
            self.termin_wykonania = datetime.strptime(nowy_termin, "%Y-%m-%d")

    def __str__(self):
        status = "✓ Wykonane" if self.wykonane else "✗ Niewykonane"
        dodatkowe_info = ", ".join(f"{k}: {v}" for k, v in self.dodatkowe.items())
        return f"[{status}] {self.tytul} - {self.opis} (Termin: {self.termin_wykonania.date()}) {dodatkowe_info}"


class ZadaniePriorytetowe(Zadanie):
    """
    Zadanie z dodatkowym priorytetem.
    """
    def __init__(self, tytul, opis, termin_wykonania="2025-04-20", priorytet=3, **kwargs):
        super().__init__(tytul, opis, termin_wykonania, **kwargs)
        self.priorytet = priorytet

    def __str__(self):
        return f"(Priorytet {self.priorytet}) {super().__str__()}"


class ZadanieRegularne(Zadanie):
    """
    Zadanie powtarzalne.
    """
    def __init__(self, tytul, opis, termin_wykonania="2025-04-20", powtarzalnosc="co tydzień", **kwargs):
        super().__init__(tytul, opis, termin_wykonania, **kwargs)
        self.powtarzalnosc = powtarzalnosc

    def __str__(self):
        return f"(Powtarzalność: {self.powtarzalnosc}) {super().__str__()}"


class ManagerZadan:
    """
    Menadżer listy zadań.
    """
    def __init__(self):
        self.lista_zadan = []

    def __contains__(self, tytul):
        return any(z.tytul == tytul for z in self.lista_zadan)

    def dodaj_zadanie(self, zadanie):
        """Dodaje zadanie do listy."""
        self.lista_zadan.append(zadanie)

    def usun_zadanie(self, tytul):
        """Usuwa zadanie po tytule."""
        self.lista_zadan = [z for z in self.lista_zadan if z.tytul != tytul]

    def oznacz_jako_wykonane(self, tytul):
        """Oznacza zadanie jako wykonane."""
        for zadanie in self.lista_zadan:
            if zadanie.tytul == tytul:
                zadanie.oznacz_jako_wykonane()
                return True
        return False

    def edytuj_zadanie(self, tytul, nowy_tytul=None, nowy_opis=None, nowy_termin=None):
        """Edytuje wskazane zadanie."""
        for zadanie in self.lista_zadan:
            if zadanie.tytul == tytul:
                zadanie.edytuj(nowy_tytul, nowy_opis, nowy_termin)
                return True
        return False

    @zmierz_czas
    def zapisz_do_pliku(self, nazwa_pliku="zadania.txt"):
        """
        Zapisuje zadania do pliku tekstowego.
        :param nazwa_pliku: Nazwa pliku, domyślnie 'zadania.txt'
        """
        with open(nazwa_pliku, "w", encoding="utf-8") as plik:
            for zadanie in self.lista_zadan:
                typ = type(zadanie).__name__
                dane = [typ, zadanie.tytul, zadanie.opis, zadanie.termin_wykonania.strftime("%Y-%m-%d"), str(zadanie.wykonane)]
                if isinstance(zadanie, ZadaniePriorytetowe):
                    dane.append(str(zadanie.priorytet))
                elif isinstance(zadanie, ZadanieRegularne):
                    dane.append(zadanie.powtarzalnosc)
                plik.write("|".join(dane) + "\n")

    @zmierz_czas
    def wczytaj_z_pliku(self, nazwa_pliku="zadania.txt"):
        """
        Wczytuje zadania z pliku tekstowego.

        :param nazwa_pliku: Nazwa pliku, domyślnie 'zadania.txt'
        """
        try:
            with open(nazwa_pliku, "r", encoding="utf-8") as plik:
                for linia in plik:
                    czesci = linia.strip().split("|")
                    typ = czesci[0]
                    tytul = czesci[1]
                    opis = czesci[2]
                    termin = czesci[3]
                    wykonane = czesci[4] == "True"

                    if typ == "ZadaniePriorytetowe":
                        priorytet = int(czesci[5])
                        zadanie = ZadaniePriorytetowe(tytul, opis, termin, priorytet)
                    elif typ == "ZadanieRegularne":
                        powtarzalnosc = czesci[5]
                        zadanie = ZadanieRegularne(tytul, opis, termin, powtarzalnosc)
                    else:
                        zadanie = Zadanie(tytul, opis, termin)

                    zadanie.wykonane = wykonane
                    self.lista_zadan.append(zadanie)
            print("Zadania wczytane z pliku.")
        except FileNotFoundError:
            print("Plik nie istnieje. Zostanie utworzony przy pierwszym zapisie.")

    @zmierz_czas
    def wyswietl_zadania(self):
        """Wyświetla posortowaną listę zadań."""
        if not self.lista_zadan:
            print("Brak zadań.")
        else:
            for zadanie in sorted(self.lista_zadan, key=lambda z: z.termin_wykonania):
                print(zadanie)
