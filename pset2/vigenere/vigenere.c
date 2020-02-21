# include <cs50.h>
# include <ctype.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>

int main(int argc, string argv[])
{
    if(argc == 2)
    {
        int a = strlen(argv[1]);
        char k[a + 1];
        for(int i= 0; i < strlen(argv[1]); i++)
        {
            if(isalpha(argv[1][i]))
            {
                k[i] = argv[1][i];
            }

            else
            {
                printf("Usage: ./vigenere k\n");
                return 1;
            }
        }
        k[a] = '\0';
        char key[strlen(k)];
        for(int i = 0; i< strlen(k); i++)
        {
            key[i] = toupper(k[i]);
        }
        string plain = get_string("plaintext: ");
        int z = strlen(plain);
        int p = 0;
        char cypher[z + 1];

        for(int i = 0; i < strlen(plain);i++)

        {
            if(isalpha(plain[i]))
            {
                if(isupper(plain[i]))
                {
                    int b = p % a;
                    int d = plain[i] - 65;
                    int e = key[b] - 65;
                    int f = 65 + ((d + e) % 26);
                    char c = f;
                    cypher[i] =c;
                    p = p + 1;
                }
                else
                {
                    int b = p % a;
                    int h = plain[i] - 97;
                    int o = key[b] - 65;
                    int m = 97 + ((h + o) % 26);
                    char l = m;
                    cypher[i] =l;
                    p = p + 1;

                }
            }

            else
            {
                cypher[i] = plain[i];


            }
        }
        cypher[z] = '\0';
        printf("ciphertext: %s\n",cypher);



    }
    else
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
}

