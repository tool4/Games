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


BOARD_SIZE  = 800
FIELD_SIZE  = int(BOARD_SIZE/8)
SIDE_SIZE   = 50
BORDER_SIZE = 2
WHITE       = (255, 255, 255)
GREEN       = (0,   255, 0)

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
    def __init__(self, background, y, x, top, left):
        self.Background = background
        self.X = x
        self.Y = y
        self.Top = top
        self.Left = left
        self.Rect = (self.Left, self.Top, self.Left + FIELD_SIZE, self.Top + FIELD_SIZE)
        pass
    def Str(self):
        return str(chr(ord('A') + self.Y)) + str(self.X + 1)
    def SetPiece(self, piece):
        self.Piece = piece

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
    board[0][0].SetPiece(white_rook)
    board[0][1].SetPiece(white_knight)
    board[0][2].SetPiece(white_bishop)
    board[0][3].SetPiece(white_queen)
    board[0][4].SetPiece(white_king)
    board[0][5].SetPiece(white_bishop)
    board[0][6].SetPiece(white_knight)
    board[0][7].SetPiece(white_rook)
    for x in range(8):
        board[1][x].SetPiece(white_pawn)
        board[6][x].SetPiece(black_pawn)
    board[7][0].SetPiece(black_rook)
    board[7][1].SetPiece(black_knight)
    board[7][2].SetPiece(black_bishop)
    board[7][3].SetPiece(black_queen)
    board[7][4].SetPiece(black_king)
    board[7][5].SetPiece(black_bishop)
    board[7][6].SetPiece(black_knight)
    board[7][7].SetPiece(black_rook)

def setup_board():
    global FIELD_SIZE
    global SIDE_SIZE
    global BORDER_SIZE
    global black_rook
    global black_knight
    global white_knight
    global black_pawn
    global black_bishop
    global black_queen
    global black_king
    global white_pawn
    global white_rook
    global white_bishop
    global white_queen
    global white_king
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
                field = Field(bg_white, y, x, SIDE_SIZE + FIELD_SIZE * x, SIDE_SIZE + FIELD_SIZE * y)
            else:
                field = Field(bg_black, y, x, SIDE_SIZE + FIELD_SIZE * x, SIDE_SIZE + FIELD_SIZE * y)
            row.append(field)
        board.append(row)
    pass

def get_coord():
    pos = pygame.mouse.get_pos()
    x = -1
    y = -1
    if pos[0] < SIDE_SIZE or pos[0] > (SIDE_SIZE + BOARD_SIZE) or pos[1] < SIDE_SIZE or pos[1] > (SIDE_SIZE + BOARD_SIZE):
        return x, y
    else:
        x = int((pos[0] - SIDE_SIZE) / FIELD_SIZE)
        y = int((pos[1] - SIDE_SIZE) / FIELD_SIZE)
        #x = chr(ord('A') + x)
        return x, y

def is_black(piece):
    return (piece == black_pawn or piece == black_knight or
        piece == black_bishop or piece == black_rook or
        piece == black_queen or piece == black_king)

def is_white(piece):
    return (piece != None and not is_black(piece))

def get_valid_moves(board, piece, moving_from):
    x, y = moving_from
    valid_moves = []
    if piece == white_pawn and y < 7:
        if x < 7 and is_black(board[y + 1][x + 1].Piece):
            valid_moves.append((x + 1, y + 1))
        if x > 0 and is_black(board[y + 1][x - 1].Piece):
            valid_moves.append((x - 1, y + 1))
        if board[y + 1][x].Piece == None:
            valid_moves.append((x, (y + 1)))
            if y == 1 and board[y + 2][x].Piece == None:
                valid_moves.append((x, (y + 2)))
    if piece == black_pawn and y > 0:
        if x < 7 and is_white(board[y - 1][x + 1].Piece):
            valid_moves.append((x + 1, y - 1))
        if x > 0 and is_white(board[y - 1][x - 1].Piece):
            valid_moves.append((x - 1, y - 1))
        if board[y - 1][x].Piece == None:
            valid_moves.append((x, (y - 1)))
            if y == 6 and board[y - 2][x].Piece == None:
                valid_moves.append((x, (y - 2)))
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
    print(info)
    running = True
    lastRect = GetWindowRect(hwnd)
    lastTime = time.time_ns() / (10 ** 9)
    loop_count = 0
    moving_piece = None
    moved_from = -1, -1
    valid_moves = []
    fps = 0
    while running:
        loop_count = loop_count + 1
        cur_time = time.time_ns() / (10 ** 9)
        if (cur_time - lastTime) > 1.0:
            pos = get_coord()
            field_str = str(chr(ord('A') + pos[0])) + str(pos[1])
            #print("\r%5d fps mouse: %5s, %5s, %4s" %(loop_count, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], field_str), end = '')
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
            print("\rrect: %d %d, lastrec: %d %d" %(rect.left, rect.top, lastRect.left, lastRect.top), end = '\n')
            lastRect = rect
        pos = mouse.position

        for row in board:
            for field in row:
                screen.blit(field.Background, (field.Top, field.Left))
            textsurface = myfont.render(chr(ord('A') + field.Y), False, (0, 0, 0))
            screen.blit(textsurface, (80 + FIELD_SIZE * field.Y, 0))
            textsurface = myfont.render(chr(ord('1') + field.Y), False, (0, 0, 0))
            screen.blit(textsurface, (20, 80 + FIELD_SIZE * field.Y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                print("key down: %d %d" %(event.key, event.mod))
                if event.key == 27:
                    exit(0)
                if event.key == 270:  # +
                    BOARD_SIZE = BOARD_SIZE + 10
                    setup_board()
                if event.key == 269:  # -
                    BOARD_SIZE = BOARD_SIZE - 10
                    setup_board()
            if event.type == pygame.KEYUP:
                print("key up")
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = get_coord()
                if x >= 0 and y >= 0 and x <= 7 and y <= 7 and board[y][x] != None:
                    moving_piece = board[y][x].Piece
                    moved_from = x, y
                    board[y][x].Piece = None
                    print("\tmouse down on %s (%d, %d)" %(board[y][x].Str(), x, y))
                    valid_moves = get_valid_moves(board, moving_piece, moved_from)
                    print("valid moves: ", end = '')
                    print(valid_moves)

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = get_coord()
                valid_move = True
                valid_moves = get_valid_moves(board, moving_piece, moved_from)
                if (x, y) in valid_moves:
                    board[y][x].Piece = moving_piece
                else:
                    board[moved_from[1]][moved_from[0]].Piece = moving_piece
                moved_from = -1, -1
                moving_piece = None
                valid_moves = []

        for f in valid_moves:
            screen.blit(highlight_green, (board[f[1]][f[0]].Top, board[f[1]][f[0]].Left))

        for row in board:
            for field in row:
                if field.Piece != None:
                    screen.blit(field.Piece, (field.Top, field.Left))

        if pygame.mouse.get_pressed()[0] and moving_piece != None:
            screen.blit(moving_piece, (pos[0] - rect.left - 40, pos[1] - rect.top -50))

        pygame.display.flip()
        if fps > 0 and moving_piece == None:
            target_fps = 30.0
            if fps > target_fps:
                delay = 1.0/target_fps - 1.0/float(fps)
                time.sleep(delay)

if __name__=="__main__":
    main()