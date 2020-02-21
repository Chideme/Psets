# include <stdio.h>
# include <stdlib.h>
# include <inttypes.h>

int main(int argc, char *argv[])
{
    // check usage
    if(argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    //remember and open card name
    FILE *file = fopen(argv[1],"r");
    if(file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n",argv[1]);
        return 2;
    }
    //allocate memory to buffer because i can,right?
    typedef uint8_t  BYTE;
    BYTE buffer[512];
    // keep count of file
    int file_count = 0;
    // create file pointer
    FILE *picture = NULL;
    char filename[8];

    //read raw file into buffer
    while(fread(buffer,512,1,file) == 1)
    {

        //check first four bytes
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if(picture != NULL && file_count > 0)
            {
                fclose(picture); //close the current file

            }
            //open new jpeg file

            sprintf(filename,"%003i.jpg",file_count);// name a new jpeg file
            picture = fopen(filename,"w");
            fwrite(buffer,512,1,picture);
            file_count ++; //increase file count by 1


        }
        else if(picture != NULL)
        {
            fwrite(buffer,512,1,picture);
        }
    }
    //close files
    fclose(picture);
    fclose(file);
    return 0;
}