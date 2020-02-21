# include <cs50.h>
# include <stdio.h>

int main(void)
{
    int height;
    // Prompt the user for input
    do
    {
        height = get_int("Please enter an interger: ");
    }
    while (height < 0 || height > 23);
    for (int i = 0; i < height ; i++)
    {
        // Initialiaze n, number of spaces
        int n = height -(i + 1);
        // Initialiaze p, number of hashes
        int p = i + 2;

        // Print out number of spaces
        for (int j = 0; j < n; j++ )
        {
            printf(" ");
        }
        //Print out number of hashes
        for (int k = 0; k < p; k++)
        {
            printf("#");
        }
        printf("\n");
    }

}


