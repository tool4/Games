#pragma once

class Pray
{
public:
    Pray(int maxx, int maxy)
    {
        this->maxx = maxx - 2;
        this->maxy = maxy - 2;
        ch = 4;
        srand((int)time(NULL));
        Reset();
    }
    void Reset()
    {
        x = (rand() % maxx) + 2;
        y = (rand() % maxy) + 2;
    }
    int maxx;
    int maxy;
    int x;
    int y;
    int ch;
};
