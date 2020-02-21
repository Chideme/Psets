int frequency(string note)
{
    if(strlen(note) == 2)
    {
        int Aposition(string a)
        {
            char d[2];
            d[0] = a[1];
            d[1] = '\0';
            int n = (atoi(d) - 4) * 7;
            return n;
        }

        int index(char c)
        {
            char list[7] = {'C','D','E','F','G','A','B'};
            for(int i = 0; i < 7; i++)
            {
                if(list[i]== c)
                {
                    int p = i - 5;
                    return p;
                }
            }
         return -1;
        }

        int Nposition(string note)
        {
            char A[3];
            A[0] = 'A';
            A[1] = note[1];
            A[2] = '\0';
            int n = Aposition(A) + index(note[0]);
            return n;
        }
        int f = pow(2,Nposition(note)) * 440;
        return f;
    }
    else
    {
        if(note[1] == '#')
        {
            char newnote[3];
            newnote[0] = note[0];
            newnote[1] = note[2];
            newnote[2] = '\0';
            return frequency(newnote) + 440;
        }
        else
        {
            char newnote[3];
            newnote[0] = note[0];
            newnote[1] = note[2];
            newnote[2] = '\0';
            return frequency(newnote) - 440;
        }
    }
}
