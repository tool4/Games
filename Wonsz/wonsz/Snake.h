#pragma once

#include "conio.h"
#include "Utils.h"
#include "Pray.h"

class Snake
{
public:
    Snake(int x, int y, int c)
    {
        p.x = x;
        p.y = y;
        ch = c;
        next = nullptr;
        prev = nullptr;
        len = 1;
        added = false;
        check_border = true;
        dead = false;
    }

    bool WrapScreen()
    {
        return !check_border;
    }

    void Add()
    {
        Snake *s = this;
        while (s->next != nullptr)
        {
            s = s->next;
        }
        s->next = new Snake(s->p.x, s->p.y, 'o');
        s->next->prev = s;
        this->prev = s->next;
        len++;
        added = true;
    }

    void Delete()
    {
        Snake *s = this->prev;
        while (s != this && s != nullptr)
        {
            Snake *prev = s->prev;
            delete s;
            LOG("elem deleted\n");
            s = prev;
        }
    }

    void Erase(Snake* snake)
    {
        if (snake)
        {
            gotoxy(snake->p.x, snake->p.y);
            putc(' ', stdout);
        }
    }

    void Draw()
    {
        Snake *s = this;
        while (s)
        {
            Draw(s);
            s = s->next;
        }
        // If we bite the tail need to draw head last
        if (dead)
        {
            SetConsoleTextAttribute(gc_console_handle, FOREGROUND_RED);
        }
        Draw(this);
        if (dead)
        {
            SetConsoleTextAttribute(
                gc_console_handle, 
                FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE);
                //FOREGROUND_INTENSITY | FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE );
        }
    }

    void Draw(Snake* snake, bool whole = false)
    {
        if (snake)
        {
            gotoxy(snake->p.x, snake->p.y);
            putc(snake->ch, stdout);
        }
    }

    void  Move(int x, int y)
    {
        int elem = 0;
        Snake *s = this;
        int x1 = x;
        int y1 = y;
        while (s != nullptr)
        {
            if (s->next == nullptr && added == false)
                Erase(s);
            int x2 = s->p.x;
            int y2 = s->p.y;
            s->p.x = x1;
            s->p.y = y1;
            x1 = x2;
            y1 = y2;
            ++elem;
            if (elem <= 2)
                Draw(s);
            s = s->next;
        }
        added = false;
    }

    void Catch(Pray &pray)
    {
        if (p.x == pray.x && p.y == pray.y)
        {
            Add();
            pray.Reset();
        }
    }

    bool CheckCollission(Screen &screen)
    {
        Snake *s = this;
        while (s)
        {
            if (check_border)
            {
                if (p.x <= screen.l || p.x >= screen.r ||
                    p.y <= screen.t || p.y >= screen.b)
                {
                    dead = true;
                    this->ch = 1; // dead head
                    break;
                }
                if (s != this && this->p.x == s->p.x && this->p.y == s->p.y)
                {
                    dead = true;
                    this->ch = 1; // dead head
                    break;
                }
            }
            s = s->next;
        }
        return dead;
    }

    int Len()
    {
        return len;
    }

private:
    Snake* next;
    Snake* prev;
    Point p;
    int ch;
    int len;
    bool added;
    bool check_border;
    bool dead;
};
