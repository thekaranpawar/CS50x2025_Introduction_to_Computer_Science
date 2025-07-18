#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

bool only_digits(string s);
char rotate(char c, int key);

int main(int argc, string argv[]){
    // check arguments
    if (argc != 2){
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // validate digits
    if (!only_digits(argv[1])){
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // convert to int
    int key = atoi(argv[1]);

    string plaintext = get_string("plaintext:  ");

    printf("ciphertext: ");

    // loop through characters and rotate
    for (int i = 0, len = strlen(plaintext); i < len; i++){
        printf("%c", rotate(plaintext[i], key));
    }

    printf("\n");
    return 0;
}

// function to check if all characters in a string are digits
bool only_digits(string s){
    for (int i = 0, len = strlen(s); i < len; i++){
        if (!isdigit(s[i])){
            return false;
        }
    }
    return true;
}

// function to rotate a character by key positions if it is a letter
char rotate(char c, int key){
    if (isupper(c)){
        return (char)(((c - 'A' + key) % 26) + 'A');
    } else if (islower(c))
    {
        return (char)(((c - 'a' + key) % 26) + 'a');
    } else{
        return c; // Leave non-alphabetical characters unchanged
    }
}
