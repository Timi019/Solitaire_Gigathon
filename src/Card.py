# Kolory terminala
reset = "\033[0m"
bright_red = "\033[91m"
red = "\033[31m"
black = "\033[30m"
white_fg = "\033[97m"
white_bg = "\033[107m"

# Znaki
RED_SUITS = ['♥', '♦']
BLACK_SUITS = ['♠', '♣']

# Klasa karty
class Card:
    def __init__(self, rank, suit, face_up=False):
        self.rank = rank
        self.suit = suit
        self.face_up = face_up

    # Malowanie karty domyslne
    def __str__(self):
        if self.face_up:
            if self.suit in BLACK_SUITS:
                return f"{white_bg}{black}{self.rank}{self.suit}{reset}"
            elif self.suit in RED_SUITS:
                return f"{white_bg}{bright_red}{self.rank}{self.suit}{reset}"
        else:
            return f"{white_bg}{red} 🂠 {reset}"

    def show(self):
        if self.suit in BLACK_SUITS:
            return f"{white_bg}{black}{self.rank}{self.suit}{reset}"
        elif self.suit in RED_SUITS:
            return f"{white_bg}{bright_red}{self.rank}{self.suit}{reset}"
