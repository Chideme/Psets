#include <cs50.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

#include "helpers.h"

int frequency(string note)
{
    if(strlen(note) == 2)
    {
        // A position
        char d[2];
        d[0] = note[1];
        d[1] = '\0';
        int n = (atoi(d) - 4) * 12;
        char list[12] = {'C','c','D','d','E','F','f','G','g','A','a','B'};
        int p; // index
        for(int i = 0; i < 12; i++)
        {
            if(list[i]== note[0])
            {
                p = i - 9;
            }
        }
        float x = (n + p);
        float y = pow(2,x/12);
        float f = y * 440;
        return round(f);
    }
    else
    {
        if(note[1] == '#')
        {
            char d[2];
            d[0] = note[2];
            d[1] = '\0';
            char newnote[3];
            newnote[0] = note[0];
            newnote[1] = note[2];
            newnote[2] = '\0';
            int n = (atoi(d) - 4) * 12;
            char list[12] = {'C','c','D','d','E','F','f','G','g','A','a','B'};
            int p; // index
            for(int i = 0; i < 12; i++)
            {
                if(list[i]== newnote[0])
                {
                    p = i - 9;
                }
            }
            p = p + 1;
            float x = (n + p);
            float y = pow(2,x/12);
            float f = y * 440;
            return round(f);

        }
        else
        {
            char d[2];
            d[0] = note[2];
            d[1] = '\0';
            char newnote[3];
            newnote[0] = note[0];
            newnote[1] = note[2];
            newnote[2] = '\0';
            int n = (atoi(d) - 4) * 12;
            char list[12] = {'C','c','D','d','E','F','f','G','g','A','a','B'};
            int p; // index
            for(int i = 0; i < 12; i++)
            {
                if(list[i]== newnote[0])
                {
                    p = i - 9;
                }
            }
            p = p - 1;
            float x = (n + p);
            float y = pow(2,x/12);
            float f = y * 440;
            return round(f);
        }
    }
}

int main(void)
{
   string g = get_string("Enter Note: ");
   int b = frequency(g);
   printf("%i\n",b);
}