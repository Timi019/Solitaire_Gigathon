import random
from src.Card import Card

# Suits and Ranks
SUITS = ['♥', '♦', '♣','♠']
RANKS = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']


# Deck Class
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(rank,suit))
        random.shuffle(self.cards)# Create random deck of cards

    def draw(self):
        return self.cards.pop() if self.cards else None

    def is_empty(self):
        return not self.cards