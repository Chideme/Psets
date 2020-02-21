# include <stdio.h>
# include <cs50.h>
# include <crypt.h>
# include <unistd.h>
# include <string.h>
# define _XOPEN_SOURCE

int random(int upper, int lower, int count);

int main(int argc, string argv[])
{
    if(argc == 2)
    {
        string hash = argv[1];
        char salt[3];
        salt[0] = hash[0];
        salt[1]= hash[1];
        salt[2] ='\0';
        string alpha = "ABCDEFGHIJKLMNOPQRSTVWXYZabcdefghijklmnopqrstvwxyz";
        int upper = strlen(alpha), lower = 0; count = 1;

        // for one letter passwords
        for(int i = 0; i < upper;i++ )
        {
            string key = alpha[i]
            if(crypt(key,salt)== hash)
            {
                printf("%s\n",key);
                break
            }
        }

    }
}
int random(int upper , int lower, int count)
{
    int num;
    srand(time(0));
    for(int i =0;i < c; i++)
    {
        num = (rand() % (upper -lower +1 )) +lower;
    }
    return num;
}