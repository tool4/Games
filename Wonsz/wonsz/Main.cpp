// Main.cpp : Defines the entry point for the console application.
//

#include "windows.h"
#include "conio.h"
#include <iostream>  
#include "game.h"
#include "menu.h"

const HANDLE gc_console_handle = GetStdHandle(STD_OUTPUT_HANDLE);

void InitConsole()
{
    SHORT x = 800;
    SHORT y = 600;
    CONSOLE_FONT_INFOEX cfi;
    COORD c = { x, y };
    SMALL_RECT windowSize = { 0, 0, x, y };
    cfi.cbSize = sizeof cfi;
    cfi.nFont = 0;
    cfi.dwFontSize.X = 0;
    cfi.dwFontSize.Y = 30;
    cfi.FontFamily = FF_DONTCARE;
    cfi.FontWeight = FW_NORMAL;
    wcscpy_s(cfi.FaceName, L"Lucida Console");
    SetCurrentConsoleFontEx(gc_console_handle, FALSE, &cfi);
    SetConsoleWindowInfo(gc_console_handle, TRUE, &windowSize);
    SetConsoleScreenBufferSize(gc_console_handle, c);
    SetConsoleDisplayMode(gc_console_handle, CONSOLE_FULLSCREEN_MODE, &c);
}

int main(int argc, char* argv[])
{
    printf("Strating...\n");

    bool exit = false;

    if (argc > 1 &&
        strcmp(argv[1], "-p") == 0)
    {
        print_ascii();
        return 0;
    }
    InitConsole();

    Screen screen(1, 40, 1, 20);
    Game game(screen);
    Menu menu(screen);

    while (exit != true)
    {
        int status = menu.ShowMenu();
        switch (status)
        {
        case PLAY:
        {
            int level = menu.ShowLevels();
            game.Play(level);
        }
        break;
        case HIGHSCORES:
        {
            int level = menu.ShowLevels();
            status = menu.ShowHighscores(level);
        }
        break;
        case EXIT:
            exit = true;
            break;
        }
    }
    system("CLS");
	return 0;
}

