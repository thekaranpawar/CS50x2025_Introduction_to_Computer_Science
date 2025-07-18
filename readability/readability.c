#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void){
    string text = get_string("Text: ");

    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    float L = (float) letters / words * 100;
    float S = (float) sentences / words * 100;

    float index = 0.0588 * L - 0.296 * S - 15.8;
    int grade = round(index);

    // result
    if (grade < 1){
        printf("Before Grade 1\n");
    } else if (grade >= 16){
        printf("Grade 16+\n");
    } else{
        printf("Grade %i\n", grade);
    }
}

// Count alphabetic letters
int count_letters(string text){
    int count = 0;
    for (int i = 0; i < strlen(text); i++){
        if (isalpha(text[i])){
            count++;
        }
    }
    return count;
}

// Count words based on spaces + 1
int count_words(string text){
    int count = 1; // Start from 1 because last word doesn't have a space
    for (int i = 0; i < strlen(text); i++){
        if (isspace(text[i])){
            count++;
        }
    }
    return count;
}

// Count sentences based on '.', '!', or '?'
int count_sentences(string text){
    int count = 0;
    for (int i = 0; i < strlen(text); i++){
        if (text[i] == '.' || text[i] == '!' || text[i] == '?'){
            count++;
        }
    }
    return count;
}

