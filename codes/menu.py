import pygame as p 
import sys

BOARD_WIDTH = 648
BOARD_HEIGHT = 648
DIMENSION = 8 
SQSIZE = BOARD_HEIGHT // DIMENSION
MOVE_LOG_PANEL_WIDTH = 220 
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
MAX_FPS = 15 
IMAGES = {}

color1 = p.Color("Tan")
color2 = p.Color("Sienna")
color3 = p.Color("PapayaWhip")
color4 = p.Color("CornflowerBlue")
color5 = p.Color("light grey")
color6 = p.Color("dim grey")
board_colors = [color5, color6] 

class Main():
    def __init__(self):
        p.init()
        self.menu_active = True 
        self.screen = p.display.set_mode((BOARD_WIDTH + 0, BOARD_HEIGHT))
        
    def show_menu(self):
        p.display.set_caption("Jeu de Lucie et les autres")
        game_state = GameState()
        board = game_state.board
        self.lastMove = None
        playerOne = True 
        playerTwo = False 
        
        background_image = p.image.load("codes/image echec/ISEP_Paris_2.jpg").convert()

        # couleurs
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GRAY = (200, 200, 200)

        #  button
        BUTTON_WIDTH, BUTTON_HEIGHT = 180, 70
        BUTTON_X = BOARD_WIDTH // 2 - BUTTON_WIDTH // 2
        BLACK_BUTTON_Y = BOARD_HEIGHT // 2 - BUTTON_HEIGHT // 2
        WHITE_BUTTON_Y = BOARD_HEIGHT // 2 + BUTTON_HEIGHT // 2 + 10
        BUTTON_SPACING = 20

        # Create font object
        font = p.font.Font("./chess/assets/Merriweather-Bold.ttf", 40)

        while self.menu_active:
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()

            # Blit the background image onto the screen
            self.screen.blit(background_image, (0, 0))

            # Calculs of verticals positions of buttons
            first_button_y = (BOARD_HEIGHT - (BUTTON_HEIGHT * 4 + BUTTON_SPACING * 3)) // 2
            black_button_y = first_button_y
            white_button_y = black_button_y + BUTTON_HEIGHT + BUTTON_SPACING
            button_pvp_y = white_button_y + BUTTON_HEIGHT + BUTTON_SPACING

            # Draw buttons
            black_button = p.draw.rect(self.screen, BLACK, (BUTTON_X, black_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
            white_button = p.draw.rect(self.screen, WHITE, (BUTTON_X, white_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
            button_pvp = p.draw.rect(self.screen, p.Color('gray'), (BUTTON_X, button_pvp_y, BUTTON_WIDTH, BUTTON_HEIGHT))

            # Draw buttons labels
            black_text = font.render("AI", True, WHITE)
            black_text_rect = black_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, black_button_y + BUTTON_HEIGHT // 2))
            self.screen.blit(black_text, black_text_rect)

            white_text = font.render("AI", True, BLACK)
            white_text_rect = white_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, white_button_y + BUTTON_HEIGHT // 2))
            self.screen.blit(white_text, white_text_rect)

            black_text_pvp = font.render("PVP", True, p.Color('dim gray'))
            black_text_rect_pvp = black_text_pvp.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, button_pvp_y + BUTTON_HEIGHT // 2))
            self.screen.blit(black_text_pvp, black_text_rect_pvp)

            # Draw the title
            title_text_shadow = font.render("Vous préférez jouer...", True, BLACK)
            title_text = font.render("Vous préférez jouer...", True, WHITE)
            title_text_rect = title_text.get_rect(center=(BOARD_WIDTH // 2, 50))
            title_text_shadow_rect = title_text_shadow.get_rect(center=(BOARD_WIDTH // 2 + 2, 52))
            self.screen.blit(title_text_shadow, title_text_shadow_rect)
            self.screen.blit(title_text, title_text_rect)

            # Check if buttons are clicked
            mouse_pos = p.mouse.get_pos()
            if black_button.collidepoint(mouse_pos):
                if p.mouse.get_pressed()[0]:
                    # Black button clicked
                    # start the game black (reverse the board)
                    # playerOne : False & playerTwo : True
                    self.main_game(playerOne=False, playerTwo=True)

            if white_button.collidepoint(mouse_pos):
                if p.mouse.get_pressed()[0]:
                    # White button clicked
                    # start the game
                    # playerOne : True & playerTwo : False
                    self.main_game(playerOne=True, playerTwo=False)
                    
            if button_pvp.collidepoint(mouse_pos):
                if p.mouse.get_pressed()[0]:
                    # Button PVP clicked
                    # start the game
                    # playerOne : True & playerTwo : True
                    self.main_game(playerOne=True, playerTwo=True)

            # Update the display
            p.display.flip()
    
    def load_images(self):
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ',]
        for piece in pieces:
            IMAGES[piece] = p.transform.scale(p.image.load("codes/image echec/pieces/" + piece + ".png"), (SQSIZE, SQSIZE))
            
    """ 
    Graphic Part : 
    """

    def draw_game_state(self, screen, game_state, validMoves, sqSelected, moveLogFont):
        self.draw_board(self.screen) # draw squares on board
        self.highlightSquares(screen, game_state, validMoves, sqSelected)
        self.draw_pieces(screen, game_state.board) # draw pieces on board
        self.drawMoveLog(screen, game_state, moveLogFont)
        
    def draw_board(self, screen):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                color = board_colors[((r+c) % 2)]
                p.draw.rect(screen, color, p.Rect(c * SQSIZE, r * SQSIZE, SQSIZE, SQSIZE))
        
    """ Highlight square selected and moves for piece """
    def highlightSquares(self, screen, game_state, validMoves, sqSelected):
        if sqSelected != ():
            r, c = sqSelected
            # sqSelected is a piece that can be moved
            if game_state.board[r][c][0] == ('w' if game_state.whiteToMove else 'b'):
                s = p.Surface((SQSIZE, SQSIZE))
                s.set_alpha(100)  # transparency value
                s.fill(p.Color('blue'))  # choice color
                self.screen.blit(s, (c * SQSIZE, r * SQSIZE))
                # highlight move from that square
                s.fill(p.Color('green'))  # choice color
                for move in validMoves:
                    if move.initialRow == r and move.initialCol == c:
                        self.screen.blit(s, (move.finalCol * SQSIZE, move.finalRow * SQSIZE))

        if self.lastMove is not None:  # Highlight the last move
            s = p.Surface((SQSIZE, SQSIZE))
            s.set_alpha(100)  # transparency value
            s.fill(p.Color('yellow'))  # choice color
            self.screen.blit(s, (self.lastMove.initialCol * SQSIZE, self.lastMove.initialRow * SQSIZE))
            self.screen.blit(s, (self.lastMove.finalCol * SQSIZE, self.lastMove.finalRow * SQSIZE))
            
        if game_state.inCheck:
            kingRow, kingCol = game_state.whiteKingLocation if game_state.whiteToMove else game_state.blackKingLocation
            s = p.Surface((SQSIZE, SQSIZE))
            s.set_alpha(100)  # transparency value
            s.fill(p.Color('red'))  # choice color
            self.screen.blit(s, (kingCol * SQSIZE, kingRow * SQSIZE))
                        
    def draw_pieces(self, screen, board):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                piece = board[r][c]
                if piece != "--": # not an empty square
                    screen.blit(IMAGES[piece], p.Rect(c * SQSIZE, r * SQSIZE, SQSIZE, SQSIZE))
                    
