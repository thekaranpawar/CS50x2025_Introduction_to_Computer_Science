// Implements a dictionary's functionality

#include <stdbool.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include <string.h>
#include "dictionary.h"

#define HASH_SIZE 10000 // You can increase this to reduce collisions

// Represents a node in a hash table
typedef struct node{
    char word[LENGTH + 1];
    struct node *next;
} node;

node *table[HASH_SIZE];

unsigned int word_count = 0;

// Hashes word to a number using djb2 hash function (case-insensitive)
unsigned int hash(const char *word){
    unsigned long hash = 5381;
    int c;
    while ((c = *word++)){
        c = tolower(c); // case-insensitive
        hash = ((hash << 5) + hash) + c; // hash * 33 + c
    }
    return hash % HASH_SIZE;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (!file)
    {
        return false;
    }

    char word[LENGTH + 1];
    // Read each word from the file
    while (fscanf(file, "%s", word) != EOF){
        // Create a new node
        node *new_node = malloc(sizeof(node));
        if (!new_node){
            fclose(file);
            return false;
        }

        // Copy word into node
        strcpy(new_node->word, word);

        // Hash word to get index
        unsigned int index = hash(word);

        // Insert node into hash table at the beginning of the list
        new_node->next = table[index];
        table[index] = new_node;

        word_count++;
    }

    fclose(file);
    return true;
}

// Returns true if word is in dictionary, else false
bool check(const char *word){
    char lower_word[LENGTH + 1];
    int len = strlen(word);

    for (int i = 0; i < len; i++){
        lower_word[i] = tolower(word[i]);
    }
    lower_word[len] = '\0';

    unsigned int index = hash(lower_word);

    // Traverse linked list at hash index
    node *cursor = table[index];
    while (cursor != NULL){
        if (strcasecmp(cursor->word, lower_word) == 0){
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

unsigned int size(void){
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void){
    for (int i = 0; i < HASH_SIZE; i++){
        node *cursor = table[i];
        while (cursor != NULL){
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}



