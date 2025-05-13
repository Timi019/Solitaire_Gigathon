import os
from src.Game import Game

# kolory w terminalu
reset = "\033[0m"
red = "\033[91m"
black = "\033[30m"
white_fg = "\033[97m"
white_bg = "\033[107m"

# Glowna funkcja
if __name__ == "__main__":
    game = Game()
    os.system('cls' if os.name == 'nt' else 'clear')# Linia ktora czysci terminal
    game.display()
    while True:
        cmd = input("\nKomenda (pomoc/wyjmij/przenies/stos_rezerwowy/stos_koncowy/wyjdz): ").strip().lower()
        os.system('cls' if os.name == 'nt' else 'clear')

        if cmd == "wyjmij":
            game.draw_from_stock()
            game.display()
        
        elif cmd.startswith("przenies"):
            try:
                _, from_str, to_str = cmd.split()
                src = int(from_str) - 1
                dest = int(to_str) - 1
                if 0 <= src < 7 and 0 <= dest < 7:
                    game.move_tableau(src, dest)
                else:
                    print("Nie poprawny numer kolumn")
            except ValueError:
                print("Uzycie: przenies <skad> <dokad>")
            game.display()

        elif cmd.startswith("stos_rezerwowy"):
            try:
                parts = cmd.split()
                _, target, to_str = parts
                to_index = int(to_str) - 1
                is_tableau = target.lower() == "k"
                if is_tableau or target.lower() == "s":
                    game.move_from_waste(to_index, is_tableau)
                else:
                    print("Jako argument musisz podac s(stos koncowy) lub k(kolumny)")
                game.display()
            except ValueError:

                print("Uzycie: stos_rezerwowy <s/k> <numer kolumny(nie ma znaczenia przy s)>")
                game.display()

        elif cmd.startswith("stos_koncowy"):
            try:
                _, pile_str = cmd.split()
                pile_index = int(pile_str) - 1
                if 0 <= pile_index < 7:
                    game.move_to_foundation(pile_index)
                else:
                    print("Zla kolumna")
                game.display()
            except ValueError:
                print("Uzycie: stos_koncowy <numer kolumny>")

        elif cmd == "wyjdz":
            print("Dzieki za gre!")
            break

        elif cmd == "pomoc":
            print(f"""{white_bg}{black}
            Dostepne komendy:
            - wyjmij                -->  Dobierz karte ze stosu rezerwowego
            - przenies X Y          -->  Przenies odkryte karty z kolumny X do kolumny Y
            - stos_rezerwowy s/k N  -->  Przenies odkryta karte do stosu koncowego (s) lub kolumny N (k)
            - stos_koncowy N        -->  Przenies karte z kolumny N do stosu koncowego
            - wyjdz                 -->  Zakoncz gre
            {reset}""")

        
        else:
            print("Wpisz poprawna komende")
            game.display()

        # Check if the game is won
        if game.check_win():
            print("\nGratulacje! Wygrales")
            break

