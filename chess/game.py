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
WHITE       = (255,255,255)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
mouse = Controller()
pos = mouse.position
screen = pygame.display.set_mode((int(BOARD_SIZE * 1.1), int(BOARD_SIZE * 1.1)))

pygame.init()

class Field:
    X = 0
    Y = 0
    def Init(x, y):
        X = x
        Y = y
        pass

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
    global bg_black
    FIELD_SIZE  = int(BOARD_SIZE/8)
    SIDE_SIZE   = 50
    BORDER_SIZE = 2
    bg_white = pygame.image.load("img/light_board.png")
    bg_black = pygame.image.load("img/dark_board.jpg")
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
    bg_white = pygame.transform.scale(bg_white, (FIELD_SIZE, FIELD_SIZE))
    bg_black = pygame.transform.scale(bg_black, (FIELD_SIZE, FIELD_SIZE))
    pass

def mouse_over_board():
    pos = pygame.mouse.get_pos()
    x = "NO"
    y = "NO"
    if pos[0] < SIDE_SIZE or pos[0] > (SIDE_SIZE + BOARD_SIZE) or pos[1] < SIDE_SIZE or pos[1] > (SIDE_SIZE + BOARD_SIZE):
        return "OUT"
    else:
        x = int((pos[0] - SIDE_SIZE) / FIELD_SIZE)
        y = int((pos[1] - SIDE_SIZE) / FIELD_SIZE) + 1
        x = chr(ord('A') + x)
        return str(x) + str(y)

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
    info = pygame.display.get_wm_info()
    print(info)
    running = True
    lastRect = GetWindowRect(hwnd)
    lastTime = time.time_ns() / (10 ** 9)
    loop_count = 0
    moving_piece = None
    fps = 0
    while running:
        loop_count = loop_count + 1
        cur_time = time.time_ns() / (10 ** 9)
        if (cur_time - lastTime) > 1.0:
            print("\r%5d fps mouse: %5s, %5s, %4s" %(loop_count, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], mouse_over_board()), end = '')
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
        even = True
        for y in range(8):
            even = not even
            for x in range(8):
                even = not even
                if even:
                    screen.blit(bg_white, (SIDE_SIZE + FIELD_SIZE * x, SIDE_SIZE + FIELD_SIZE * y))
                else:
                    screen.blit(bg_black, (SIDE_SIZE + FIELD_SIZE * x, SIDE_SIZE + FIELD_SIZE * y))
            textsurface = myfont.render(chr(ord('A') + y), False, (0, 0, 0))
            screen.blit(textsurface, (80 + FIELD_SIZE * y, 0))
            textsurface = myfont.render(chr(ord('1') + y), False, (0, 0, 0))
            screen.blit(textsurface, (20, 80 + FIELD_SIZE * y))

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
                if mouse_over_board() == "E8":
                    moving_piece = black_queen
                    print("mouse down on %s" %mouse_over_board())
                if mouse_over_board() == "E1":
                    moving_piece = white_queen
                    print("mouse down on %s" %mouse_over_board())
                #if pygame.mouse.get_pressed()[0] and moving_piece != None:
                #    screen.blit(moving_piece, (pos[0] - rect.left - 40, pos[1] - rect.top -50))
            if event.type == pygame.MOUSEBUTTONUP:
                moving_piece = None
            #    print("mouse up")
            #if event.type == pygame.MOUSEMOTION:

        draw_piece(black_rook,   0, 7)
        draw_piece(black_rook,   7, 7)
        draw_piece(black_pawn,   0, 6)
        draw_piece(black_pawn,   1, 6)
        draw_piece(black_pawn,   1, 6)
        draw_piece(black_pawn,   2, 6)
        draw_piece(black_pawn,   3, 6)
        draw_piece(black_pawn,   4, 6)
        draw_piece(black_pawn,   5, 6)
        draw_piece(black_pawn,   6, 6)
        draw_piece(black_pawn,   7, 6)
        draw_piece(black_knight, 1, 7)
        draw_piece(black_knight, 6, 7)
        draw_piece(black_bishop, 2, 7)
        draw_piece(black_bishop, 5, 7)
        if not (pygame.mouse.get_pressed()[0] and moving_piece == black_queen):
            draw_piece(black_queen,  4, 7)
        draw_piece(black_king,   3, 7)
        draw_piece(white_pawn,   0, 1)
        draw_piece(white_pawn,   1, 1)
        draw_piece(white_pawn,   2, 1)
        draw_piece(white_pawn,   3, 1)
        draw_piece(white_pawn,   4, 1)
        draw_piece(white_pawn,   5, 1)
        draw_piece(white_pawn,   6, 1)
        draw_piece(white_pawn,   7, 1)
        draw_piece(white_rook,   0, 0)
        draw_piece(white_rook,   7, 0)
        draw_piece(white_knight, 1, 0)
        draw_piece(white_knight, 6, 0)
        draw_piece(white_bishop, 2, 0)
        draw_piece(white_bishop, 5, 0)
        if not (pygame.mouse.get_pressed()[0] and moving_piece == white_queen):
            draw_piece(white_queen,  4, 0)
        draw_piece(white_king,   3, 0)

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