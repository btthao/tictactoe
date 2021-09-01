from player import Human, SmartBot, DumbBot
from tictactoe import TicTacToe


def play(game, x_player, o_player):
    game.print_numbers()
    
    current_player = o_player

    while not game.board_full():

        print()
        print(current_player.name + "'s turn")
        
        square = current_player.make_move(game)

        
        game.make_move(square, current_player.name)

        game.print_board() 
         
        if game.winner:
            print()
            print('GAME OVER: ' + current_player.name + ' wins!')
            return current_player.name
            
        current_player = x_player if current_player == o_player else o_player
        
            

    print()
    print("GAME OVER: It's a tie")

    return 'tie'  
        




if __name__ == '__main__':
    
    game = TicTacToe()
    game_start = False

    while not game_start:
        mode = input('Choose game mode: easy(E), impossible(I), play with a friend(F): ').upper()
        game_start = True
        if mode == 'E':
            x_player = DumbBot('x')
            o_player = Human('o')
        elif mode == 'F':
            x_player = Human('x')
            o_player = Human('o')        
        elif mode == 'I':
            x_player = SmartBot('x')
            o_player = Human('o')  
        else:
            game_start = False
            print('Invalid input')

    play(game, x_player, o_player)



# if __name__ == '__main__':
#     x_wins = 0
#     o_wins = 0
#     ties = 0
#     for _ in range(1000):
#         x_player = SmartBot('x')
#         o_player = DumbBot('o')
#         t = TicTacToe()
#         result = play(t, x_player, o_player, print_game=False)
#         print(result)
#         if result == 'x':
#             x_wins += 1
#         elif result == 'o':
#             o_wins += 1
#         else:
#             ties += 1
#     print (f'x wins: {x_wins}, o wins: {o_wins}, tie: {ties}')