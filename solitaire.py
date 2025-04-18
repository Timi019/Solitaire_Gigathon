import os
from src.Game import Game

# CLI Colors
reset = "\033[0m"
red = "\033[91m"
black = "\033[30m"
white_fg = "\033[97m"
white_bg = "\033[107m"

# Testing
if __name__ == "__main__":
    game = Game()
    os.system('cls' if os.name == 'nt' else 'clear')
    game.display()
    while True:
        cmd = input("\nCommand (draw/quit/move/waste move/foundation move/undo): ").strip().lower()
        os.system('cls' if os.name == 'nt' else 'clear')

        if cmd == "draw":
            game.draw_from_stock()
            game.display()
        
        elif cmd.startswith("move"):
            try:
                _, from_str, to_str = cmd.split()
                src = int(from_str) - 1
                dest = int(to_str) - 1
                if 0 <= src < 7 and 0 <= dest < 7:
                    game.move_tableau(src, dest)
                else:
                    print("Invalid pile numbers.")
            except ValueError:
                print("Usage: move <from> <to>")
            game.display()

        elif cmd.startswith("waste move"):
            try:
                parts = cmd.split()
                if len(parts) != 4:
                    raise ValueError
                _, _, to_str, target = parts
                to_index = int(to_str) - 1
                is_tableau = target.lower() == "t"
                if is_tableau or target.lower() == "f":
                    game.move_from_waste(to_index, is_tableau)
                else:
                    print("Target must be 't' (tableau) or 'f' (foundation).")
                game.display()
            except ValueError:
                print("Usage: waste move <pile_number> <t/f>")

        elif cmd.startswith("foundation move"):
            try:
                _, _, pile_str = cmd.split()
                pile_index = int(pile_str) - 1
                if 0 <= pile_index < 7:
                    game.move_to_foundation(pile_index)
                else:
                    print("Invalid tableau pile number.")
                game.display()
            except ValueError:
                print("Usage: foundation move <pile_number>")

        elif cmd == "quit":
            print("Thanks for playing!")
            break

        elif cmd == "undo":
            game.undo()
            game.display()

        else:
            print("Unknown command.")
            game.display()

        # Check if the game is won
        if game.check_win():
            print("\nCongratulations! You've won the game!")
            break
