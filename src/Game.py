from src.Deck import Deck
import random

# Kolory kart
RED_SUITS = ['♥', '♦']
BLACK_SUITS = ['♠', '♣']

# Kolory terminala
bold = "\033[1m"
reset = "\033[0m"
red = "\033[91m"
black = "\033[30m"
white_fg = "\033[97m"
white_bg = "\033[107m"
pink = "\033[95m"

class Game:
    def __init__(self): # Zmienne
        self.deck = Deck()
        self.tableau = [[] for _ in range(7)]
        self.foundations = {'♠': [], '♥': [], '♦': [], '♣': []}
        self.stock = []
        self.waste = []
        self.setup_tableau()
        self.setup_stock()

    def setup_tableau(self):
        for pile_index in range(7):# 7 Rzedow
            for card_index in range(pile_index + 1):# Liczaba kart zwieksza sie o 1 z kazdym rzedem
                card = self.deck.draw()
                if card_index == pile_index:
                    card.face_up = True# Karta odwrocona
                self.tableau[pile_index].append(card)

    def setup_stock(self):
        # Karty ktore zostaly ida do stosu rezerwowego
        while not self.deck.is_empty():
            self.stock.append(self.deck.draw())# Doklada karty dopoki sie nie skoncza
    # Wyswietla gre
    def display(self):
        print(f"{bold}{white_bg}{pink}Kolumny:{reset}")
        for i, pile in enumerate(self.tableau):
            print(f"{i+1}: ", end="")
            for card in pile:
                print(card, end=" ")
            print()

        print(f"\n{bold}{white_bg}{pink}Stosy koncowe:{reset}")
        for suit, pile in self.foundations.items():
            top = pile[-1].show() if pile else "pusto"
            print(f"{suit}: {top}", end=" | ")
        print()

        print(f"\n{bold}{white_bg}{pink}Karta odkryta:{reset}", end=" ")
        if self.waste:
            print(self.waste[-1].show())
        else:
            print("pusto")

        print(f"{bold}{white_bg}{pink}Stos rezerwowy: zostalo {len(self.stock)} kart{reset}")
    # Draw cards from stock to waste
    def draw_from_stock(self):
        if not self.stock and self.waste:
            print(f"{bold}{white_bg}{black}Tasowanie kart do stosu rezerwowego...{reset}")
            
            while self.waste:
                card = self.waste.pop()
                card.face_up = False
                self.stock.append(card)
            random.shuffle(self.stock)
        elif self.stock:
            
            card = self.stock.pop()
            card.face_up = True
            self.waste.append(card)
        else:
            print(f"{bold}{white_bg}{red}Skonczyly sie karty!{reset}")

    
    def can_stack(self, card1, card2):
        # Sprawdza czy karta(card1) moze pojsc na inna karte(card2)
        if not card2:
            return card1.rank == 'K'  # Jezeli karta jest krolem, to moze isc na puste miejsce
        if self.same_color(card1, card2):
            return False# Karty tego samego koloru nie moga byc na sobie
        return self.rank_value(card1) == self.rank_value(card2) - 1# Karty moga byc w kolejnosci malejacej na sobie

    def same_color(self, card1, card2):# Sprawdza czy karty sa tego samego koloru
        return ((card1.suit in RED_SUITS and card2.suit in RED_SUITS) or
                (card1.suit in BLACK_SUITS and card2.suit in BLACK_SUITS))

    def rank_value(self, card):# Przypisuje karta wartosci do sprawdzenia
        rank = card.rank.strip()
        rank_order = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,'6': 6, '7': 7, '8': 8, '9': 9, '10': 10,'J': 11, 'Q': 12, 'K': 13}
        return rank_order[rank]

    def move_tableau(self, src_index, dest_index):# przesuwa karty miedzy kolumnami
        src = self.tableau[src_index]
        dest = self.tableau[dest_index]

        for i in range(len(src)):# Zabiera najwieksza odkryta karte
            if src[i].face_up:
                break
        else:
            print(f"{bold}{white_bg}{red}Nie ma odwroconych kart do przeniesienia.{reset}")
            return

        moving_stack = src[i:]

        if not dest or self.can_stack(moving_stack[0], dest[-1]):# Sprawdz czy pierwsza karta moze pojsc nad ostatnia karte
            
            dest.extend(moving_stack)
            del src[i:]

            if src and not src[-1].face_up:
                src[-1].face_up = True
        else:# Jezeli nie to informujemy
            print(f"{bold}{white_bg}{red}Niemozliwy ruch.{reset}")


    def can_add_to_foundation(self, card):
        # Sprawdza czy karta moze zostac przeniesiona do stosu koncowego
        if not card:# Nie jezeli nie ma karty
            return False

        foundation = self.foundations[card.suit]# Karta moze isc tylko do stosu koncowego swojego koloru

        if not foundation:
            return card.rank == 'A'  # Tylko as moze byc pierwszy
        return self.rank_value(card) == self.rank_value(foundation[-1]) + 1# Sprawdza czy karta jest nastepna


    def move_from_waste(self, to_index, is_tableau=True):
        if not self.waste:
            print(f"{bold}{white_bg}{red}Nie ma odkrytej karty.{reset}")
            return

        card = self.waste[-1]# Mozna uzyc tylko ostatniej odkrytej karty

        if is_tableau:# Jezeli chcemy przeniesc karte do kolumny
            if 0 <= to_index < 7:# Jezeli karta ma prawidlowy indeks
                tableau_pile = self.tableau[to_index]
                if not tableau_pile or self.can_stack(card, tableau_pile[-1]):# jezeli karta moze sie przeniesc 
                    self.waste.pop()
                    tableau_pile.append(card)
                    print(f"{bold}{white_bg}{black}Przeniesiono {reset}{card}{bold}{white_bg}{black} do kolumny {to_index+1}.{reset}")
                else:
                    print(f"{bold}{white_bg}{red}Nie mozna preniesc{reset} {card} {bold}{white_bg}{red}do kolumny {to_index+1}.{reset}")
            else:
                print(f"{bold}{white_bg}{red}Nieprawidlowy numer kolumny{reset}")
        else:
            if self.can_add_to_foundation(card):# jezeli mozna dodac do stosu koncowego
                
                self.waste.pop()
                self.foundations[card.suit].append(card)
                print(f"{bold}{white_bg}{black}Przeniesiono {reset}{card}{bold}{white_bg}{black} do stosu koncowego {card.suit}.{reset}")
            else:
                print(f"{bold}{white_bg}{red}Nie mozna przeniesc {reset}{card}{bold}{white_bg}{red} do stosu koncowego.{reset}")


    def move_to_foundation(self, pile_index):
        pile = self.tableau[pile_index]

        if not pile or not pile[-1].face_up:
            print(f"{bold}{white_bg}{red}Nie ma zadnej karty do odwrocenia.{reset}")
            return

        card = pile[-1]

        # Sprawdza czy karta moze pojsc do stosu koncowego
        if self.can_add_to_foundation(card):
            self.foundations[card.suit].append(card)  # Dodaje karte do odpowiedniego stosu koncowego
            pile.pop()  # Usuwa karte z jej kolumny
            if pile:
                pile[-1].face_up = True

            print(f"{bold}{white_bg}{black}Przeniesiono {reset}{card}{bold}{white_bg}{black} do stosu koncowego {card.suit}.{reset}")
        else:
            print(f"{bold}{white_bg}{red}Nie mozna przeniesc {reset}{card}{bold}{white_bg}{red} do stosu koncowego {card.suit}.{reset}")


    def check_win(self):
        # Sprawdza czy gra sie skonczyla
        for suit, foundation in self.foundations.items():
            # Sprawdza czy w stosie konowym jest 13 kart tego samego koloru
            if len(foundation) != 13:
                return False
            for i in range(13):
                if self.rank_value(foundation[i]) != i + 1:
                    return False
        return True
