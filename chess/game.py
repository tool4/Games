import pygame
import os
from pynput.mouse import Button, Controller
import time
from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT

def init_piece(filename):
    piece = pygame.image.load(filename)
    piece = pygame.transform.scale(piece, (FIELD_SIZE, FIELD_SIZE))
    piece.set_alpha(None)
    piece.set_colorkey(WHITE)
    return piece

def draw_piece(piece, x, y):
    screen.blit(piece, (SIDE_SIZE + FIELD_SIZE * x, SIDE_SIZE + FIELD_SIZE * y))

VERB_LEVEL  = 1
BOARD_SIZE  = 800
FIELD_SIZE  = int(BOARD_SIZE/8)
SIDE_SIZE   = 50
BORDER_SIZE = 2
WHITE       = (255, 255, 255)
GREEN       = (0,   255, 0)

def LOG(v, str, end = '\n'):
    if v <= VERB_LEVEL:
        print(str, end)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
mouse = Controller()
pos = mouse.position
screen = pygame.display.set_mode((int(BOARD_SIZE * 1.1), int(BOARD_SIZE * 1.1)))
pygame.init()

bg_white = pygame.image.load("img/light_board.png")
bg_black = pygame.image.load("img/dark_board.jpg")
highlight_green = pygame.image.load("img/highlight_green.png")
black_rook = init_piece("img/black_rook.png")
black_knight = init_piece("img/black_knight.png")
white_knight = init_piece("img/white_knight.png")
black_pawn = init_piece("img/black_pawn.png")
black_bishop = init_piece("img/black_bishop.png")
black_queen = init_piece("img/black_queen.png")
black_king = init_piece("img/black_king.png")
white_pawn = init_piece("img/white_pawn.png")
white_rook = init_piece("img/white_rook.png")
white_bishop = init_piece("img/white_bishop.png")
white_queen = init_piece("img/white_queen.png")
white_king = init_piece("img/white_king.png")

class Field:
    Background = None
    X = 0
    Y = 0
    Top = 0
    Left = 0
    Piece = None
    Rect = None
    def __init__(self, background, x, y, left, top):
        self.Background = background
        self.X = x
        self.Y = y
        self.Top = top
        self.Left = left
        self.Rect = (self.Left, self.Top, FIELD_SIZE, FIELD_SIZE)
        pass
    def Str(self):
        return str(chr(ord('A') + self.Y)) + str(self.X + 1)
    def StrPiece(self):
        if self.Piece == white_pawn:
            return "white_pawn"
        if self.Piece == white_knight:
            return "white_knight"
        if self.Piece == white_bishop:
            return "white_bishop"
        if self.Piece == white_rook:
            return "white_rook"
        if self.Piece == white_queen:
            return "white_queen"
        if self.Piece == white_king:
            return "white_king"
        if self.Piece == black_pawn:
            return "black_pawn"
        if self.Piece == black_knight:
            return "black_knight"
        if self.Piece == black_bishop:
            return "black_bishop"
        if self.Piece == black_rook:
            return "black_rook"
        if self.Piece == black_queen:
            return "black_queen"
        if self.Piece == black_king:
            return "black_king"
        return "None"

board = []

def init_piece(filename):
    global FIELD_SIZE
    piece = pygame.image.load(filename)
    piece = pygame.transform.scale(piece, (FIELD_SIZE, FIELD_SIZE))
    piece.set_alpha(None)
    piece.set_colorkey(WHITE)
    return piece

def draw_piece(piece, x, y):
    global FIELD_SIZE
    global SIDE_SIZE
    global screen
    screen.blit(piece, (SIDE_SIZE + FIELD_SIZE * x, SIDE_SIZE + FIELD_SIZE * y))

def init_board():
    board[0][0].Piece = white_rook
    board[0][1].Piece = white_knight
    board[0][2].Piece = white_bishop
    board[0][3].Piece = white_queen
    board[0][4].Piece = white_king
    board[0][5].Piece = white_bishop
    board[0][6].Piece = white_knight
    board[0][7].Piece = white_rook
    for x in range(8):
        board[1][x].Piece = white_pawn
        board[6][x].Piece = black_pawn
    board[7][0].Piece = black_rook
    board[7][1].Piece = black_knight
    board[7][2].Piece = black_bishop
    board[7][3].Piece = black_queen
    board[7][4].Piece = black_king
    board[7][5].Piece = black_bishop
    board[7][6].Piece = black_knight
    board[7][7].Piece = black_rook

def setup_board():
    global FIELD_SIZE
    global SIDE_SIZE
    global BORDER_SIZE
    global bg_white
    global highlight_green
    global bg_black
    FIELD_SIZE  = int(BOARD_SIZE/8)
    SIDE_SIZE   = 50
    BORDER_SIZE = 2
    bg_white = pygame.transform.scale(bg_white, (FIELD_SIZE, FIELD_SIZE))
    bg_black = pygame.transform.scale(bg_black, (FIELD_SIZE, FIELD_SIZE))
    highlight_green = pygame.transform.scale(highlight_green, (FIELD_SIZE, FIELD_SIZE))
    highlight_green.set_colorkey(WHITE)
    even = True
    for y in range(8):
        row = []
        even = not even
        for x in range(8):
            even = not even
            if even:
                field = Field(bg_white, x, y, SIDE_SIZE + FIELD_SIZE * x, SIDE_SIZE + FIELD_SIZE * y)
            else:
                field = Field(bg_black, x, y, SIDE_SIZE + FIELD_SIZE * x, SIDE_SIZE + FIELD_SIZE * y)
            row.append(field)
        board.append(row)
    pass

def get_coord(white_player):
    pos = pygame.mouse.get_pos()
    x = -1
    y = -1
    if pos[0] < SIDE_SIZE or pos[0] > (SIDE_SIZE + BOARD_SIZE) or pos[1] < SIDE_SIZE or pos[1] > (SIDE_SIZE + BOARD_SIZE):
        return x, y
    else:
        x = int((pos[0] - SIDE_SIZE) / FIELD_SIZE)
        if white_player:
            y = 7 - int((pos[1] - SIDE_SIZE) / FIELD_SIZE)
        else:
            y = int((pos[1] - SIDE_SIZE) / FIELD_SIZE)
        return x, y

def is_black(piece):
    return (piece == black_pawn or piece == black_knight or
        piece == black_bishop or piece == black_rook or
        piece == black_queen or piece == black_king)

def is_white(piece):
    return (piece != None and not is_black(piece))

def is_same_color(piece1, piece2):
    return (is_black(piece1) and is_black(piece2)) or (is_white(piece1) and is_white(piece2))

def add_move_if_valid(board, piece, x, y, valid_moves):
    if y >= 0 and x >= 0 and x <= 7 and y <= 7:
        if not is_same_color(piece, board[y][x].Piece):
            valid_moves.append((x, y))

def find_valid_moves(board, piece, moving_from, en_passant):
    x, y = moving_from
    valid_moves = []
    if piece == white_pawn and y < 7:
        if x < 7 and is_black(board[y + 1][x + 1].Piece) or (y == 4 and en_passant == (x + 1, y + 1)):
            valid_moves.append((x + 1, y + 1))
        if x > 0 and is_black(board[y + 1][x - 1].Piece) or (y == 4 and en_passant == (x - 1, y + 1)):
            valid_moves.append((x - 1, y + 1))
        if board[y + 1][x].Piece == None:
            valid_moves.append((x, (y + 1)))
            if y == 1 and board[y + 2][x].Piece == None:
                valid_moves.append((x, (y + 2)))
    if piece == black_pawn and y > 0:
        if x < 7 and is_white(board[y - 1][x + 1].Piece) or (y == 3 and en_passant == (x + 1, y - 1)):
            valid_moves.append((x + 1, y - 1))
        if x > 0 and is_white(board[y - 1][x - 1].Piece) or (y == 3 and en_passant == (x - 1, y - 1)):
            valid_moves.append((x - 1, y - 1))
        if board[y - 1][x].Piece == None:
            valid_moves.append((x, (y - 1)))
            if y == 6 and board[y - 2][x].Piece == None:
                valid_moves.append((x, (y - 2)))
    if piece == black_rook or piece == white_rook or piece == black_queen or piece == white_queen or piece == black_king or piece == white_king:
        for i in range(y):
            add_move_if_valid(board, piece, x , y - i - 1, valid_moves)
            if board[y - i - 1][x].Piece != None or piece == black_king or piece == white_king:
                break
        for i in range(7 - y):
            add_move_if_valid(board, piece, x , y + i + 1, valid_moves)
            if board[y + i + 1][x].Piece != None or piece == black_king or piece == white_king:
                break
        for i in range(x):
            add_move_if_valid(board, piece, x - i - 1, y, valid_moves)
            if board[y][x - i - 1].Piece != None or piece == black_king or piece == white_king:
                break
        for i in range(7 - x):
            add_move_if_valid(board, piece, x + i + 1, y, valid_moves)
            if board[y][x + i + 1].Piece != None or piece == black_king or piece == white_king:
                break
    if piece == black_bishop or piece == white_bishop or piece == black_queen or piece == white_queen or piece == black_king or piece == white_king:
        for i in range(y):
            add_move_if_valid(board, piece, x - i - 1, y - i - 1, valid_moves)
            if y - i > 0 and x - i > 0:
                if board[y - i - 1][x - i - 1].Piece != None or piece == black_king or piece == white_king:
                    break
        for i in range(y):
            add_move_if_valid(board, piece, x + i + 1, y - i - 1, valid_moves)
            if y - i > 0 and x + i < 7:
                if board[y - i - 1][x + i + 1].Piece != None or piece == black_king or piece == white_king:
                    break
        for i in range(7 - y):
            add_move_if_valid(board, piece, x + i + 1, y + i + 1, valid_moves)
            if y + i < 7 and x + i < 7:
                if board[y + i + 1][x + i + 1].Piece != None or piece == black_king or piece == white_king:
                    break
        for i in range(7 - y):
            add_move_if_valid(board, piece, x - i - 1, y + i + 1, valid_moves)
            if y + i < 7 and x - i > 0:
                if board[y + i + 1][x - i - 1].Piece != None or piece == black_king or piece == white_king:
                    break
    if piece == black_knight or piece == white_knight:
        add_move_if_valid(board, piece, x + 1, y + 2, valid_moves)
        add_move_if_valid(board, piece, x + 2, y + 1, valid_moves)
        add_move_if_valid(board, piece, x - 1, y + 2, valid_moves)
        add_move_if_valid(board, piece, x - 2, y + 1, valid_moves)
        add_move_if_valid(board, piece, x - 1, y - 2, valid_moves)
        add_move_if_valid(board, piece, x - 2, y - 1, valid_moves)
        add_move_if_valid(board, piece, x + 1, y - 2, valid_moves)
        add_move_if_valid(board, piece, x + 2, y - 1, valid_moves)
    return valid_moves

def main():
    global BOARD_SIZE
    logo = pygame.image.load("img/light_board.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Chess game")
    hwnd = pygame.display.get_wm_info()["window"]
    prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
    paramflags = (1, "hwnd"), (2, "lprect")
    GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)
    setup_board()
    init_board()
    info = pygame.display.get_wm_info()
    LOG(2, info)
    running = True
    lastRect = GetWindowRect(hwnd)
    lastTime = time.time_ns() / (10 ** 9)
    loop_count = 0
    moving_piece = None
    moved_from = -1, -1
    valid_moves = []
    en_passant = None
    show_fps = False
    white_player = True
    white_moves = True
    verbose = 0
    fps = 0
    while running:
        loop_count = loop_count + 1
        cur_time = time.time_ns() / (10 ** 9)
        if (cur_time - lastTime) > 1.0:
            pos = get_coord(white_player)
            field_str = str(chr(ord('A') + pos[0])) + str(pos[1])
            if show_fps:
                print("\r%5d fps mouse: %5s, %5s, %4s" %(loop_count, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], field_str), end = '')
            lastTime = time.time_ns() / (10 ** 9)
            fps = loop_count
            loop_count = 0
        screen.fill(WHITE)
        pygame.draw.rect(
            screen,
            (0,0,0),
            (SIDE_SIZE - BORDER_SIZE, SIDE_SIZE - BORDER_SIZE, BOARD_SIZE + BORDER_SIZE * 2, BOARD_SIZE + BORDER_SIZE * 2) )
        rect = GetWindowRect(hwnd)
        if rect.left != lastRect.left and rect.top != lastRect.top:
            LOG(2, "\rrect: %d %d, lastrec: %d %d" %(rect.left, rect.top, lastRect.left, lastRect.top), end = '\n')
            lastRect = rect
        pos = mouse.position

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                LOG(1, "key down: %d %d" %(event.key, event.mod))
                if event.key == 27 or event.key == 113: #esc or q
                    exit(0)
                if event.key == 114: # r
                    white_player = not white_player
                if event.key == 270:  # +
                    BOARD_SIZE = BOARD_SIZE + 10
                    setup_board()
                if event.key == 269:  # -
                    BOARD_SIZE = BOARD_SIZE - 10
                    setup_board()
            if event.type == pygame.KEYUP:
                LOG(2, "key up")
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = get_coord(white_player)
                if x >= 0 and y >= 0 and x <= 7 and y <= 7 and board[y][x] != None:
                    if white_moves and not is_white(board[y][x].Piece):
                        continue
                    if not white_moves and not is_black(board[y][x].Piece):
                        continue
                    moving_piece = board[y][x].Piece
                    moved_from = x, y
                    board[y][x].Piece = None
                    LOG(2, "\tmouse down on %s (%d, %d)" %(board[y][x].Str(), x, y))
                    valid_moves = find_valid_moves(board, moving_piece, moved_from, en_passant)
                    LOG(2, "valid moves: ", end = '')
                    LOG(2, valid_moves)
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = get_coord(white_player)
                #valid_moves = find_valid_moves(board, moving_piece, moved_from, en_passant)
                if (x, y) in valid_moves:
                    board[y][x].Piece = moving_piece
                    if moving_piece == white_pawn and y == 7:
                        board[y][x].Piece = white_queen
                    if moving_piece == black_pawn and y == 0:
                        board[y][x].Piece = black_queen
                    if moving_piece == black_pawn and moved_from[1] == 3 and en_passant == (x, y):
                        print("En Passant!")
                        if board[3][x].Piece == white_pawn:
                            board[3][x].Piece = None
                        else:
                            print("Invalid condition for En Passant! ")
                    if moving_piece == white_pawn and moved_from[1] == 4 and en_passant == (x, y):
                        print("En Passant!!")
                        if board[4][x].Piece == black_pawn:
                            board[4][x].Piece = None
                        else:
                            print("Invalid condition for en passant!")
                    if moving_piece == white_pawn and moved_from[1] == 1 and y == 3:
                        en_passant = x, 2
                    elif moving_piece == black_pawn and moved_from[1] == 6 and y == 4:
                        en_passant = x, 5
                    else:
                        en_passant = None
                    print("%s moved from %s to %s" %(board[y][x].StrPiece(), board[moved_from[1]][moved_from[0]].Str(), board[y][x].Str()))
                    white_moves = not white_moves
                else:
                    if moved_from[1] >= 0 and moved_from[0] >= 0:
                        board[moved_from[1]][moved_from[0]].Piece = moving_piece
                moved_from = -1, -1
                moving_piece = None
                valid_moves = []

        for row in board:
            for field in row:
                screen.blit(field.Background, (field.Left, field.Top))
            textsurface = myfont.render(chr(ord('1') + field.Y), False, (0, 0, 0))
            screen.blit(textsurface, (80 + FIELD_SIZE * field.Y, 0))
            textsurface = myfont.render(chr(ord('A') + field.Y), False, (0, 0, 0))
            if white_player:
                screen.blit(textsurface, (20, BOARD_SIZE - 20 - FIELD_SIZE * field.Y))
            else:
                screen.blit(textsurface, (20, 80 + FIELD_SIZE * field.Y))

        for f in valid_moves:
            if white_player:
                screen.blit(highlight_green, (board[f[1]][f[0]].Left, BOARD_SIZE - board[f[1]][f[0]].Top))
            else:
                screen.blit(highlight_green, (board[f[1]][f[0]].Left, board[f[1]][f[0]].Top))

        for row in board:
            for field in row:
                if field.Piece != None:
                    if white_player:
                        screen.blit(field.Piece, (field.Left, BOARD_SIZE - field.Top))
                    else:
                        screen.blit(field.Piece, (field.Left, field.Top))

        if pygame.mouse.get_pressed()[0] and moving_piece != None:
            screen.blit(moving_piece, (pos[0] - rect.left - FIELD_SIZE/2, pos[1] - rect.top - FIELD_SIZE + 10))

        pygame.display.flip()
        if fps > 0 and moving_piece == None:
            target_fps = 30.0
            if fps > target_fps:
                delay = 1.0/target_fps - 1.0/float(fps)
                time.sleep(delay)

if __name__=="__main__":
    main()