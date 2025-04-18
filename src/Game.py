from src.Deck import Deck
from src.GameState import GameState
import random

# Suits and Ranks
RED_SUITS = ['♥', '♦']
BLACK_SUITS = ['♠', '♣']

# CLI Colors
bold = "\033[1m"
reset = "\033[0m"
red = "\033[91m"
black = "\033[30m"
white_fg = "\033[97m"
white_bg = "\033[107m"
pink = "\033[95m"

class Game:
    def __init__(self, max_undo_history=15):
        self.max_undo_history = max_undo_history  # Set the max undo history
        self.deck = Deck()
        self.tableau = [[] for _ in range(7)]
        self.foundations = {'♠': [], '♥': [], '♦': [], '♣': []}
        self.stock = []
        self.waste = []
        self.history = []  # Saves
        self.setup_tableau()
        self.setup_stock()
        self.save_state()  # Save the initial state

    def setup_tableau(self):
        for pile_index in range(7):
            for card_index in range(pile_index + 1):
                card = self.deck.draw()
                if card_index == pile_index:
                    card.face_up = True  # Top card faces up
                self.tableau[pile_index].append(card)

    def setup_stock(self):
        # Remaining cards go into the stock
        while not self.deck.is_empty():
            self.stock.append(self.deck.draw())
    # Display the game
    def display(self):
        print(f"{bold}{white_bg}{pink}Tableau:{reset}")
        for i, pile in enumerate(self.tableau):
            print(f"{i+1}: ", end="")
            for card in pile:
                print(card, end=" ")
            print()

        print(f"\n{bold}{white_bg}{pink}Foundations:{reset}")
        for suit, pile in self.foundations.items():
            top = pile[-1].show() if pile else "empty"
            print(f"{suit}: {top}", end=" | ")
        print()

        print(f"\n{bold}{white_bg}{pink}Waste:{reset}", end=" ")
        if self.waste:
            print(self.waste[-1].show())
        else:
            print("empty")

        print(f"{bold}{white_bg}{pink}Stock:{reset} {len(self.stock)} cards remaining")
    # Draw cards from stock to waste
    def draw_from_stock(self):
        if not self.stock and self.waste:
            print(f"{bold}{white_bg}{black}Recycling waste back into stock...{reset}")
            self.save_state()
            while self.waste:
                card = self.waste.pop()
                card.face_up = False
                self.stock.append(card)
            random.shuffle(self.stock)
        elif self.stock:
            self.save_state()
            card = self.stock.pop()
            card.face_up = True
            self.waste.append(card)
        else:
            print(f"{bold}{white_bg}{red}No cards to draw!{reset}")

    
    def can_stack(self, card1, card2):
        # Check if card1 can go on top of card2
        if not card2:
            return card1.rank == 'K'  # Only Kings can go on empty piles
        if self.same_color(card1, card2):
            return False
        return self.rank_value(card1) == self.rank_value(card2) - 1

    def same_color(self, card1, card2):
        return ((card1.suit in RED_SUITS and card2.suit in RED_SUITS) or
                (card1.suit in BLACK_SUITS and card2.suit in BLACK_SUITS))

    def rank_value(self, card):
        rank = card.rank.strip()
        rank_order = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,'6': 6, '7': 7, '8': 8, '9': 9, '10': 10,'J': 11, 'Q': 12, 'K': 13}
        return rank_order[rank]

    def move_tableau(self, src_index, dest_index):
        src = self.tableau[src_index]
        dest = self.tableau[dest_index]

        for i in range(len(src)):
            if src[i].face_up:
                break
        else:
            print(f"{bold}{white_bg}{red}No face-up card to move.{reset}")
            return

        moving_stack = src[i:]

        if not dest or self.can_stack(moving_stack[0], dest[-1]):
            self.save_state()
            dest.extend(moving_stack)
            del src[i:]

            if src and not src[-1].face_up:
                src[-1].face_up = True
        else:
            print(f"{bold}{white_bg}{red}Invalid move.{reset}")


    def can_add_to_foundation(self, card):
        # Check if the card can be added to any foundation
        if not card:
            return False

        foundation = self.foundations[card.suit]

        if not foundation:
            return card.rank == 'A'  # Only Ace can start a foundation
        return self.rank_value(card) == self.rank_value(foundation[-1]) + 1


    def move_from_waste(self, to_index, is_tableau=True):
        if not self.waste:
            print(f"{bold}{white_bg}{red}No cards in the waste pile to move.{reset}")
            return

        card = self.waste[-1]

        if is_tableau:
            if 0 <= to_index < 7:
                tableau_pile = self.tableau[to_index]
                if not tableau_pile or self.can_stack(card, tableau_pile[-1]):
                    self.save_state()
                    self.waste.pop()
                    tableau_pile.append(card)
                    print(f"{bold}{white_bg}{black}Moved{reset} {card} {bold}{white_bg}{black}to tableau pile {to_index+1}.{reset}")
                else:
                    print(f"{bold}{white_bg}{red}Cannot move{reset} {card} {bold}{white_bg}{red}to tableau pile {to_index+1}.{reset}")
            else:
                print(f"{bold}{white_bg}{red}Invalid tableau pile number.{reset}")
        else:
            if self.can_add_to_foundation(card):
                self.save_state()
                self.waste.pop()
                self.foundations[card.suit].append(card)
                print(f"{bold}{white_bg}{black}Moved {reset}{card}{bold}{white_bg}{black} to foundation {card.suit}.{reset}")
            else:
                print(f"{bold}{white_bg}{red}Cannot move {reset}{card}{bold}{white_bg}{red} to foundation.{reset}")


    def move_to_foundation(self, pile_index):
        pile = self.tableau[pile_index]

        if not pile or not pile[-1].face_up:
            print(f"{bold}{white_bg}{red}No face-up card to move.{reset}")
            return

        card = pile[-1]

        # Check if the card can be added to the foundation
        if self.can_add_to_foundation(card):
            self.save_state()  # Save the game state
            self.foundations[card.suit].append(card)  # Add the card to the appropriate foundation
            pile.pop()  # Remove the card from the tableau
            print(f"{bold}{white_bg}{black}Moved {reset}{card}{bold}{white_bg}{black} to foundation {card.suit}.{reset}")
        else:
            print(f"{bold}{white_bg}{red}Cannot move {reset}{card}{bold}{white_bg}{red} to foundation {card.suit}.{reset}")


    def check_win(self):
        # Check if the game is won
        for suit, foundation in self.foundations.items():
            # Check if foundation has exactly 13 cards and they are in order
            if len(foundation) != 13:
                return False
            for i in range(13):
                if self.rank_value(foundation[i]) != i + 1:
                    return False
        return True
    
    def save_state(self):
        # Save the current game state to history, with a limit
        if len(self.history) >= self.max_undo_history:
            self.history.pop(0)  # Remove the oldest state if we exceed the limit
        self.history.append(GameState(self.tableau, self.waste, self.stock, self.foundations))

    
    def undo(self):
        # Undo the last move
        if len(self.history) > 1:
            self.history.pop()  # Remove the current state
            last_state = self.history[-1]  # Get the previous state
            self.tableau = last_state.tableau
            self.waste = last_state.waste
            self.stock = last_state.stock
            self.foundations = last_state.foundations
            print(f"{bold}{white_bg}{black}Undone the last move.{reset}")
        else:
            print(f"{bold}{white_bg}{red}No moves to undo.{reset}")