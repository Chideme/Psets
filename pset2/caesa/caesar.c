# include <cs50.h>
# include <ctype.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>

int main(int argc, string argv[])
{
    if(argc == 2)
    {
        int k = atoi(argv[1]);
        string plain = get_string("plaintext: ");
        int n = strlen(plain);
        char cypher[n+1];

        for(int i = 0; i < n; i++)
        {
            if(isalpha(plain[i]))
            {
                if(isupper(plain[i]))
                {
                    int b = plain[i]- 65;
                    int p = 65 + ((b + k) % 26);
                    char c = p;
                    cypher[i] = c;
                }
                else
                {
                    int a = plain[i] - 97;
                    int z = 97 + ((a + k) % 26);
                    char d = z;
                    cypher[i] = d;
                }
            }
            else
            {
                cypher[i] = plain[i];
            }
        }
        cypher[n] = '\0';
        printf("ciphertext: %s\n",cypher);
        return 0;
    }
    else
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }
}

