# include <stdio.h>
# include <cs50.h>
# include <crypt.h>
# include <unistd.h>
# include <string.h>
# include <time.h>


int random(int u , int l, int c)
{
    int num;
    srand(time(0));
    for(int i =0;i < c; i++)
    {
        num = (rand() % (u -l +1 )) +l;
        return num;
    }

}

int main(void)
{
    int u = 7, l = 0, c = 2;
    printf("%d\n",random(u,l,c));
}