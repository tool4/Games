// Main.cpp : Defines the entry point for the console application.
//

#include "windows.h"
#include "conio.h"
#include <iostream>  
#include "game.h"
#include "menu.h"

const HANDLE gc_console_handle = GetStdHandle(STD_OUTPUT_HANDLE);


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
    Screen screen(1, 40, 1, 20);
    Game game(screen);
    Menu menu(screen);

    while (exit != true)
    {
        int status = menu.ShowMenu();
        switch (status)
        {
        case PLAY: game.Play(); break;
        case HIGHSCORES: menu.ShowHighscores();  break;
        case EXIT: exit = true; break;
        }
    }
    system("CLS");
	return 0;
}

