import random
import math
import time

class Player():
    def __init__(self, name):
        self.name = name
    

class Human(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def make_move(self, game):
        move = None
        while move not in game.available_moves():
            try:
                possible_move = int(input("Your next move (1-9): "))
                if game.is_available(possible_move - 1):
                    move = possible_move - 1
                else:
                    raise ValueError
            except ValueError:
                print('Invalid move!')
        return move


class DumbBot(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def make_move(self, game):
        time.sleep(0.7)
        move = random.choice(game.available_moves())
        return move


class SmartBot(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def make_move(self, game):
        time.sleep(0.7)
        best_score = -math.inf
        best_move = None
        for possible_move in game.available_moves():
            game.make_move(possible_move, self.name)
            score = self.minimax(game, 9, False)
            if score > best_score:
                best_score = score
                best_move = possible_move
            game.board[possible_move] = ' '
            game.winner = None
        return best_move

    def minimax(self, game, multiplier, is_maximizing):
        human_player = 'o' if self.name == 'x' else 'x'

        if game.winner == self.name:
            return multiplier
        elif game.winner == human_player:
            return -1*multiplier
        elif game.board_full():
            return 0
        
        best_score = -math.inf if is_maximizing else math.inf

        for possible_move in game.available_moves():

            if is_maximizing:
                game.make_move(possible_move, self.name)
                score = self.minimax(game, multiplier - 1, False)
                best_score = max(best_score, score)
            else:
                game.make_move(possible_move, human_player)
                score = self.minimax(game, multiplier - 1, True)
                best_score = min(best_score, score)
            
            game.board[possible_move] = ' '
            game.winner = None
        
        
        return best_score

