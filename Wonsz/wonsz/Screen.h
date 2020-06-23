#pragma once

#include "utils.h"

class Screen
{
public:
    Screen(int left, int right, int top, int bottom)
    {
        l = left;
        r = right;
        t = top;
        b = bottom;
    }

    void StatusB(int x, int line, const char *str)
    {
        gotoxy(x, b + line);
        printf(str);
    }

    void StatusM(int x, int line, const char *str)
    {
        gotoxy(x, l + line);
        printf(str);
    }

    inline void print_border();

    int l;
    int r;
    int b;
    int t;
};

inline void Screen::print_border()
{
    Screen &screen = *this;
    system("CLS");
    //TOP:
    gotoxy(screen.l, screen.t);
    printf("%c", 201);  // ╔
    for (int i = screen.l; i < screen.r - screen.l; i++)
    {
        gotoxy(screen.l + i, screen.t);
        printf("%c", 205); // ═
    }
    gotoxy(screen.r, screen.t);
    printf("%c", 187);  // ╗

    for (int i = screen.t + 1; i < screen.b + 5; i++)
    {
        gotoxy(screen.l, i);
        printf("%c", 186);  // ║
        gotoxy(screen.r, i);
        printf("%c", 186);  // ║
    }
    const int MID = 4;
    // BOTTOM
    gotoxy(screen.l, screen.b + MID);
    printf("%c", 200);  // ╚
    for (int i = screen.l; i < screen.r - screen.l; i++)
    {
        gotoxy(screen.l + i, screen.b + MID);
        printf("%c", 205); // ═
    }
    gotoxy(screen.r, screen.b + MID);
    printf("%c", 188);  // ╝

    // MID
    gotoxy(screen.l, screen.b);
    printf("%c", 204);  // ╠
    for (int i = screen.l; i < screen.r - screen.l; i++)
    {
        gotoxy(screen.l + i, screen.b);
        printf("%c", 205); // ═
    }
    gotoxy(screen.r, screen.b);
    printf("%c", 185);  // ╣
}
