#pragma once

#include "time.h"
#include "Screen.h"
#include "Snake.h"
#include "Pray.h"

class Game
{
public:
    Game(Screen &sc) :
        screen(sc),
        pray(screen.r, screen.b),
        exit(false)
    {
        snake = nullptr;
        Reset();
    }

    ~Game()
    {
        snake->Delete();
        delete snake;
        snake = nullptr;
        LOG("Head deleted\n");
    }

    void Reset()
    {
        if (snake)
        {
            snake->Delete();
            delete snake;
        }
        count = 0;
        x = 15;
        y = 11;
        ch = 1;
        exit = false;
        snake = new Snake(x, y, 2);
        pray.Reset();
    }

    void draw_snake(Snake *snake)
    {
        snake->Draw();
    }

    void draw_pray(Pray &pray)
    {
        gotoxy(pray.x, pray.y);
        putc(pray.ch, stdout);
    }

    void Render()
    {
        draw_snake(snake);
        draw_pray(pray);
    }

    void Update()
    {
        if (snake->CheckCollission(screen))
        {
            exit = true;
            return;
        }

        snake->Catch(pray);
        Render();

        while (_kbhit())
        {
            int c = _getch();
            switch (c)
            {
            case 27: exit = true;                        break;
            case 80: if (d != TOP)      d = BOTTOM;      break;
            case 77: if (d != LEFT)     d = RIGHT;       break;
            case 72: if (d != BOTTOM)   d = TOP;         break;
            case 75: if (d != RIGHT)    d = LEFT;        break;
            case 'w': screen.b++; screen.print_border(); break;
            case 's': screen.b--; screen.print_border(); break;
            case 'd': screen.r++; screen.print_border(); break;
            case 'a': screen.r--; screen.print_border(); break;
            //case 49: cmps /= 1.1f;                       break;
            //case 50: cmps *= 1.1f;                       break;
            case ' ': debug_screen = !debug_screen; clear = !debug_screen;   break;
            }
            if (debug_screen)
            {
                gotoxy(0, screen.b + 2);
                printf("pressed: %d (%c)", c, c);
            }
        }
        if (debug_screen)
        {
            gotoxy(0, screen.b + 3);
            printf("x: %4d, y: %4d, ch: %4d, d: %4d, c: %4d speed: %.2f len: %d", x, y, ch, d, count, cmps, snake->Len());
        }
        else if (clear)
        {
            gotoxy(0, screen.b + 3);
            printf("%70s", "");
            gotoxy(0, screen.b + 2);
            printf("%40s", "");
            clear = false;
        }
        else
        {
            gotoxy(3, screen.b + 2);
            printf("SCORE:  %4d", snake->Len());
            gotoxy(20, screen.b + 2);
            printf("SPEED: %5.0f cm/s", cmps);
        }

        switch (d)
        {
        case TOP:       y--; break;
        case LEFT:      x--; break;
        case RIGHT:     x++; break;
        case BOTTOM:    y++; break;
        }

        if (snake->WrapScreen())
        {
            if (x <= screen.l)
                x = screen.r - 1;
            if (x >= screen.r)
                x = screen.l + 1;
            if (y <= screen.t)
                y = screen.b - 1;
            if (y >= screen.b)
                y = screen.t + 1;
        }
        snake->Move(x, y);
    }


    void Play(int level)
    {
        cmps = 7;
        switch (level)
        {
        case 0: cmps = 4;  break;
        case 1: cmps = 7;  break;
        case 2: cmps = 10; break;
        case 3: cmps = 15; break;
        }
        screen.print_border();
        Reset();
        while (exit == false)
        {
            double start = GetCurrentTime();
            Update();
            Render();
            count++;
            DWORD delay = 100;
            if (cmps > 1)
            {
                float ms_per_move = 1000 / cmps;
                delay = (DWORD)(start + ms_per_move - GetCurrentTime());
            }
            Sleep(delay);
        }
        screen.StatusB(15, 1, " GAME OVER... ");
        screen.StatusB(11, 3, " Press ESC to exit \n");
        gotoxy(3, screen.b + 3);
        while (_getch() != 27)
        {
        }
    }

private:
    int count;
    int x;
    int y;
    int ch;
    float cmps;
    Snake *snake;
    bool debug_screen = false;
    bool clear = false;
    DIRECTION d = RIGHT;
    Screen &screen;
    Pray   pray;
    bool exit;
};