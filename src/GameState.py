class GameState:
    def __init__(self, tableau, waste, stock, foundations):
        self.tableau = [pile[:] for pile in tableau]  # Copying each tableau pile
        self.waste = waste[:]  # Copy waste
        self.stock = stock[:]  # Copy stock
        self.foundations = {suit: foundation[:] for suit, foundation in foundations.items()}  # Copy foundations