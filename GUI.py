import pygame, sys
from player import SmartBot, DumbBot
from tictactoe import TicTacToe
from pygame import gfxdraw

# size should be a multiple of 3
SIZE = 510
SQUARE_SIZE = SIZE // 3
BG_COLOR = (95,157,161)
TEXT_COLOR = (255, 255, 255)
YELLOW = (222,184,134)
BLUE = (5,96,101)
FPS = 60
LINE_WIDTH = 2
O_COLOR = (241,241,241)
O_RADIUS = SIZE // 12
O_WIDTH = 8
X_COLOR = (5,96,101)
X_WIDTH = 15
X_SPACE = SIZE // 10
WINNING_LINE_WIDTH = 8
BUTTON_HEIGHT = 40

pygame.init()
pygame.font.init()
pygame.display.set_caption('TIC TAC TOE') 
screen = pygame.display.set_mode((SIZE, SIZE))
big_font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()


def draw_text(text, font, color, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect(center=(SIZE/2, y))
    screen.blit(text_obj, text_rect)


def draw_button(y, text, button):
    pygame.draw.rect(screen, YELLOW, button, 2)
    draw_text(text, small_font, TEXT_COLOR, y+BUTTON_HEIGHT//2)


def draw_lines():
    pygame.draw.line(screen, YELLOW, (0, SQUARE_SIZE), (SIZE, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, YELLOW, (0, SQUARE_SIZE*2), (SIZE, SQUARE_SIZE*2), LINE_WIDTH)
    pygame.draw.line(screen, YELLOW, (SQUARE_SIZE,0), (SQUARE_SIZE, SIZE), LINE_WIDTH)
    pygame.draw.line(screen, YELLOW, (SQUARE_SIZE*2, 0), (SQUARE_SIZE*2, SIZE), LINE_WIDTH)


def draw_figures(row, col, player):
    if player == 'o':
        pygame.draw.circle(screen, O_COLOR, (int(col*SQUARE_SIZE+SIZE/6), int(row*SQUARE_SIZE+SIZE/6)), O_RADIUS, int(O_WIDTH*0.8))

        for i in range(O_WIDTH):
            gfxdraw.aacircle(screen, int(col*SQUARE_SIZE+SIZE/6), int(row*SQUARE_SIZE+SIZE/6), O_RADIUS-i, O_COLOR)

       
    else:
        pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + X_SPACE, row * SQUARE_SIZE + SQUARE_SIZE - X_SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - X_SPACE, row * SQUARE_SIZE + X_SPACE), X_WIDTH )
        pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + X_SPACE, row * SQUARE_SIZE +  X_SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - X_SPACE, row * SQUARE_SIZE + SQUARE_SIZE - X_SPACE), X_WIDTH )


def draw_winning_line(outcome, row, col):
    if outcome == 'col':
        posX = col * SQUARE_SIZE + SIZE//6
        pygame.draw.line(screen, YELLOW, (posX, SQUARE_SIZE//5), (posX, SIZE - SQUARE_SIZE//5), WINNING_LINE_WIDTH)
    elif outcome == 'row':
        posY = row * SQUARE_SIZE + SIZE//6
        pygame.draw.line(screen, YELLOW, (SQUARE_SIZE//5, posY), ( SIZE - SQUARE_SIZE//5, posY), WINNING_LINE_WIDTH)
    elif outcome == 'asc':
        pygame.draw.line(screen, YELLOW, (SQUARE_SIZE//4, SIZE - SQUARE_SIZE//4), (SIZE - SQUARE_SIZE//4, SQUARE_SIZE//4), WINNING_LINE_WIDTH)
    elif outcome == 'desc':
        pygame.draw.line(screen, YELLOW, (SQUARE_SIZE//4, SQUARE_SIZE//4), (SIZE-SQUARE_SIZE//4, SIZE - SQUARE_SIZE//4), WINNING_LINE_WIDTH)
    


def main():
    click = False 
    while True:
        screen.fill(BG_COLOR)
        draw_text('Choose game mode', big_font, BLUE, SIZE/8 )

        mx, my = pygame.mouse.get_pos()

        button_easy = pygame.Rect((SIZE - SIZE / 3)/2, SIZE*2/8, SIZE / 3, BUTTON_HEIGHT)
        button_hard = pygame.Rect((SIZE - SIZE / 3)/2, SIZE*3/8, SIZE / 3, BUTTON_HEIGHT)
        button_friend = pygame.Rect((SIZE - SIZE / 3)/2, SIZE*4/8, SIZE / 3, BUTTON_HEIGHT)
        
        draw_button(SIZE*2/8, 'Easy', button_easy)
        draw_button(SIZE*3/8, 'Impossible', button_hard)
        draw_button(SIZE*4/8, 'Play with friend', button_friend)

        draw_text("Press R to end game and go back.", small_font, TEXT_COLOR, SIZE * 4 / 5 )
        
        if button_easy.collidepoint((mx, my)):
            if click:
                play_bot('easy')
        if button_hard.collidepoint((mx, my)):
            if click:
                play_bot('hard')
        if button_friend.collidepoint((mx, my)):
            if click:
                play_with_friend()

 
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


        pygame.display.update()
        clock.tick(FPS)


def play_bot(mode):
    running = True
    game_over = False
    bot = DumbBot('x') if mode == 'easy' else SmartBot('x')
    human_player = 'o'
    game = TicTacToe()
    screen.fill(BG_COLOR)
    draw_lines()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                clicked_row = int(my // SQUARE_SIZE)
                clicked_col = int(mx // SQUARE_SIZE)
                human_move = 3*clicked_row + clicked_col

                if game.is_available(human_move):
                    outcome = game.make_move(human_move, human_player)
                    draw_figures(clicked_row, clicked_col, human_player)               
                    if game.winner:
                        draw_winning_line(outcome, clicked_row, clicked_col)
                        game_over = True
                    elif game.board_full():
                        game_over = True
                    else:                        
                        bot_move = bot.make_move(game)
                        outcome = game.make_move(bot_move, bot.name)
                        draw_figures(bot_move // 3, bot_move % 3, bot.name)
                        if game.winner:
                            draw_winning_line(outcome, bot_move // 3, bot_move % 3)
                            game_over = True
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = False
        
        pygame.display.update()
        clock.tick(FPS)


def play_with_friend():
    running = True
    game_over = False
    x_player = 'x'
    o_player = 'o'
    game = TicTacToe()
    screen.fill(BG_COLOR)
    draw_lines()
    current_player = x_player

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                clicked_row = int(my // SQUARE_SIZE)
                clicked_col = int(mx // SQUARE_SIZE)
                move = 3*clicked_row + clicked_col
                if game.is_available(move):
                    outcome = game.make_move(move, current_player)
                    draw_figures(clicked_row, clicked_col, current_player)
                    if game.winner:
                        draw_winning_line(outcome, clicked_row, clicked_col)
                        game_over = True
                    elif game.board_full():
                        game_over = True
                    else:
                        current_player = o_player if current_player == x_player else x_player
                   
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = False
        
        pygame.display.update()
        clock.tick(FPS)
   

if __name__ == '__main__':
    main()