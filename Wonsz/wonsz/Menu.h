#pragma once

#include "Utils.h"
#include "Screen.h"

class Menu
{
public:
    Menu(Screen &sc) :
        screen(sc),
        status(MENU)
    {
    }

    int ShowMenu()
    {
        screen.print_border();
        screen.StatusM(14, 5, "MENU");
        screen.StatusM(10, 6, "________________");
        screen.StatusM(10, 7, "PLAY");
        screen.StatusM(10, 8, "HIGHSCORES");
        screen.StatusM(10, 9, "EXIT");
        x = 10;
        y = 8;
        gotoxy(x, y);
        bool exit = false;
        while (!exit)
        {
            int c = _getch();
            switch (c)
            {
            case 27: status = EXIT; break;
            case 80: y++;    break; // DOWN
            case 77: break; // RIGHT
            case 72: y--;  break; // UP
            case 75: break; // LEFT
            case 10: exit = true;  break;
            case 13: exit = true; break;
            }
            if (y > 10)
                y = 8;
            if (y < 8)
                y = 10;
            gotoxy(x, y);
        }
        switch (y)
        {
        case 8: return PLAY;
        case 9: return HIGHSCORES;
        case 10: return EXIT;
        }
        return EXIT;
    }

    int ShowHighscores()
    {
        screen.print_border();
        screen.StatusM(14, 5, "HIGHSCORES");
        screen.StatusM(10, 6, "________________");
        screen.StatusM(10, 7, "Empty");
        screen.StatusM(10, 8, "Empty");
        screen.StatusM(10, 9, "Empty");

        int c = _getch();
        return MENU;
    }

private:
    Screen &screen;
    STATUS status;
    int x;
    int y;
};