# include <cs50.h>
# include <ctype.h>
# include <math.h>
# include <stdio.h>

int main(void)
{
    long long int c;
    long long int f;
    long long int x;
    int needed = 0;
    int counter = 0;
    int d = 0;
    int n;
    int b;
    int e;

// prompt for  number
    do
    {
        c = get_long_long("Number: ");
    }
    while (c < 0);

    x = c;
    f = c;

    c = c/10;

    while (c > 0)
    {
        n = (c % 10) *2;
        b = (n/10) + (n % 10);
        needed += b;
        c = c/10;
        c= c/10;

    }
     while (x > 0)
     {
        d += x % 10;
        x = x/10;
        x = x/10;
     }

     e = d + needed;

     while(f > 100)
     {
         f = f/ 10;
         counter++;
     }
     counter = counter +2;
     e = e  % 10;
    if(e != 0)
    {
       printf("INVALID\n");
    }
    else
    {
        // check for msater card
        if(f == 51 || f == 52 || f == 53 || f == 54 || f== 55)
        {
            printf("MASTERCARD\n");
        }
        //check for AMEX
        else if (f == 34 &&  counter == 15 || f == 37 && counter == 15)
        {
            printf("AMEX\n");
        }
        //check for VISA
        else if ( f / 10 == 4 && counter == 13 || f/10 ==4 && counter == 16 )
        {
            printf("VISA\n");
        }
        //Check for Invalid
        else
        {
            printf("INVALID\n");
        }
    }
     return 0;
}