#pragma once

extern const HANDLE gc_console_handle;

#ifdef _DEBUG
#define LOG(x) printf(x)
#else
#define LOG(x)
#endif

enum DIRECTION
{
    TOP = 0,
    LEFT,
    RIGHT,
    BOTTOM,
    INVALID
};

enum STATUS
{
    MENU,
    PLAY,
    HIGHSCORES,
    EXIT
};

struct Point
{
    int x;
    int y;
};

void gotoxy(short col, short row)
{
    COORD position = { col, row };
    SetConsoleCursorPosition(gc_console_handle, position);
}

void print_ascii()
{
    for (int i = 0; i < 32; i++)
    {
        for (int j = 0; j < 8; j++)
        {
            printf("%d: %c\t", i * 8 + j, i * 8 + j);
        }
        printf("\n");
    }
}

