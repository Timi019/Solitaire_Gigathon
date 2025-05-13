import random
from src.Card import Card

# Kolory i wartosci
SUITS = ['♥', '♦', '♣','♠']
RANKS = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']


# Klasa talii
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(rank,suit))
        random.shuffle(self.cards)# Tasuje karty ulozone w talie

    def draw(self):
        return self.cards.pop() if self.cards else None# Wyciaga karte z talii

    def is_empty(self):
        return not self.cards# Sprawdza czy w talii sa karty
    