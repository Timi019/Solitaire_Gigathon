# Pasjans – Gra terminalowa w Pythonie

**Pasjans (znany też jako Klondike Solitaire)** to klasyczna gra karciana dla jednej osoby. Ten projekt to implementacja pasjansa w terminalu napisana w Pythonie.

## Etapy rozgrywki

1. **Uruchomienie gry**
   - Gracz uruchamia skrypt `solitaire.py`, co inicjalizuje nową grę.
   - Terminal zostaje wyczyszczony, a plansza startowa zostaje wyświetlona.

2. **Ułożenie kart**
   - Karty rozkładane są w 7 kolumnach (tzw. tableau), rosnąco: 1 do 7 kart.
   - Tylko ostatnia karta w każdej kolumnie jest odkryta.
   - Pozostałe karty trafiają do stosu rezerwowego (talia).

3. **Rozgrywka**
   Gracz wykonuje ruchy przy pomocy komend:
   - Dobiera karty ze stosu (`wyjmij`).
   - Przenosi odkryte karty między kolumnami (`przenies <skad> <dokad>`).
   - Przenosi kartę z odkrytego stosu do kolumny lub stosu końcowego (`stos_rezerwowy k <kolumna>` lub `stos_rezerwowy s <x>`).
   - Przenosi kartę z kolumny do stosu końcowego (`stos_koncowy <kolumna>`).

4. **Odkrywanie kart**
   - Po każdej udanej operacji karta, która znajduje się teraz na wierzchu kolumny, zostaje automatycznie odkryta (jeśli była zakryta).

5. **Warunek zwycięstwa**
   - Gracz wygrywa, jeśli wszystkie 52 karty zostaną przeniesione do czterech stosów końcowych w odpowiedniej kolejności i kolorze (od Asa do Króla).

6. **Zakończenie gry**
   - Gra kończy się komunikatem „Gratulacje! Wygrałeś” lub przez wpisanie komendy `wyjdz`.

---

## Funkcje gry

- Rozgrywka zgodna z klasycznymi zasadami Klondike.
- Kolorowe karty wyświetlane w terminalu (z użyciem ANSI escape codes).
- Dobieranie kart ze stosu rezerwowego.
- Przenoszenie kart między kolumnami.
- Przenoszenie kart do stosów końcowych.
- Automatyczne odkrywanie kart po przeniesieniu.
- Detekcja zwycięstwa.
- Obsługa tasowania zużytych kart.

---

## Wymagania

- Python 3.7 lub nowszy
- Terminal z obsługą kolorów ANSI:
  - Linux / macOS – działa natywnie
  - Windows – użyj terminala systemowego (Windows Terminal, PowerShell 5+)

---

## Jak uruchomić

1. Sklonuj repozytorium:
   ```bash
    git clone https://github.com/Timi019/Solitaire_Gigathon.git
    cd Solitaire_Gigathon
    python3 solitaire.py

## Dostępne komendy
| Komenda                      | Działanie                                                                      |
| ---------------------------- | ------------------------------------------------------------------------------ |
| `wyjmij`                     | Dobiera jedną kartę ze stosu rezerwowego                                       |
| `przenies <skad> <dokad>`    | Przenosi odkryty stos kart między kolumnami (np. `przenies 3 6`)               |
| `stos_rezerwowy k <kolumna>` | Przenosi kartę z odkrytego stosu do kolumny (np. `stos_rezerwowy k 1`)         |
| `stos_rezerwowy s <x>`       | Przenosi kartę z odkrytego stosu do stosu końcowego. x nie ma znaczenia (np. `stos_rezerwowy s 0`) |
| `stos_koncowy <kolumna>`     | Przenosi kartę z kolumny do stosu końcowego (np. `stos_koncowy 2`)             |
| `wyjdz`                      | Kończy grę                                                                     |
## Struktura projektu
```bash
pasjans-terminal/
├── solitaire.py             # Główna pętla gry (interfejs użytkownika)
├── src/
│   ├── Card.py         # Klasa reprezentująca pojedynczą kartę
│   ├── Deck.py         # Klasa talii (tworzenie i tasowanie kart)
│   └── Game.py         # Logika gry, zarządzanie stanem i ruchem kart
```
## Zrzut ekranu (terminal)
```Kolumny:
1: A♣ 
2:  🂠  A♠ 
3:  🂠   🂠  10♦ 
4:  🂠   🂠   🂠  10♣ 
5:  🂠   🂠   🂠   🂠  4♦ 
6:  🂠   🂠   🂠   🂠   🂠  2♠ 
7:  🂠   🂠   🂠   🂠   🂠   🂠  8♣ 

Stosy koncowe:
♠: pusto | ♥: pusto | ♦: pusto | ♣: pusto | 

Karta odkryta: pusto
Stos rezerwowy: zostalo 24 kart

Komenda (pomoc/wyjmij/przenies/stos_rezerwowy/stos_koncowy/wyjdz): 
```
## Autor
Tymek