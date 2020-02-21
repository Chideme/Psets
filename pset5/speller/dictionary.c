// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"

// implement a node
typedef  struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

node *head = NULL;

node *hashtable[SIZE];
//initialize s and p
int s = 0;
int p;

// hash function
int hash_function(const char* word)
{
    int hash = 0;
    int n;
    for(int i = 0; word[i] != '\0'; i ++)
    {
        if(isalpha(word[i]))
        {
            n = word[i] - 'a' + 1;

        }
        else
        {
            n = 27;
        }

        hash = ((hash << 3) + n) % SIZE;

    }
     return hash;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int n = strlen(word);
    char temp[n + 1];
    for(int i = 0; i < n; i++)
    {
        temp[i] = tolower(word[i]);
    }

    temp[n] = '\0';

    int index = hash_function(temp);
    node *cursor = hashtable[index];

    if(hashtable[index] == NULL)
    {
        return false;
    }

    while(cursor != NULL)
    {
       if(strcmp(temp, cursor -> word) == 0)
       {
           return true;

       }
       else
       {
           cursor = cursor -> next;
       }



    }
     return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE* f = fopen(dictionary, "r");
    if(!f)
    {
        return false;
    }
    char w[LENGTH +1];
    //Read in word
    while(fscanf(f,"%s",w) != EOF)
    {
        s++;
        node *new_node = malloc(sizeof(node));
        if(new_node == NULL)
        {
            unload();
            return false;
        }
        strcpy(new_node -> word, w);
        new_node -> next = head;
        head = new_node;
        int index = hash_function(w);
        hashtable[index] = new_node;


    }
    fclose(f);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{


    return s;
}
// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for(int index = 0;index < SIZE; index++)
    {
        if(hashtable[index] == NULL)
        {
            index++;
        }

        else
        {
            node *cursor = hashtable[index];

            while(cursor != NULL)
            {
                node *temp = cursor;
                cursor = cursor -> next;
                free(temp);
            }
        }

    }

    return true;
}
