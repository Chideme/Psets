// Helper functions for music

#include <cs50.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>


#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    char num[2];
    char den[2];
    num[0] =  fraction[0];
    num[1] = '\0';
    den[0] = fraction[2];
    den[1] = '\0';
    int d = (atoi(num) * 8)/ atoi(den);
    return d;
}

// Calculates frequency (in Hz) of a note
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

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if(s[0] == '\0')
    {
        return true;
    }
    else
    {
        return false;
    }
}
