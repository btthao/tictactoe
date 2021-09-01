class TicTacToe():
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.winner = None


    def print_board(self):
        for i in range(3):
            print(' | '.join(self.board[i*3:(i+1)*3]))
            if i != 2:
                print('─' * 9)


    @staticmethod
    def print_numbers():
        numbers = [str(x+1) for x in range(9)]
        print()
        for i in range(3):
            print(' | '.join(numbers[i*3:(i+1)*3]))
            if i != 2:
                print('─' * 9)


    def make_move(self, square, player):
        self.board[square] = player
        winning_move = self.is_winner(square, player)
        if winning_move:
            self.winner = player
            return winning_move
            

    def is_available(self, square):
        return square in range(9) and self.board[square] == ' '
    

    def available_moves(self):
        return [i for i in range(9) if self.board[i] == " "]


    def is_winner(self, square, player):
        if len(self.available_moves()) > 5:
            return False

        # check row
        row_idx = square // 3
        row = self.board[row_idx*3:(row_idx+1)*3]
        if all([x == player for x in row]):
            return 'row'

        # check col
        col_idx = square % 3
        col = [self.board[col_idx + 3*i] for i in range(3)]
        if all([x == player for x in col]):
            return 'col'

        # check diagonal
        if square % 2 == 0:
            # asc diagonal
            asc_diagonal = [2,4,6]
            if all([self.board[x] == player for x in asc_diagonal]):
                return 'asc'

            # desc diagonal
            desc_diagonal = [0,4,8]
            if all([self.board[x] == player for x in desc_diagonal]):
                return 'desc'
            
        
        return False

    def board_full(self):
        return " " not in self.board

