#include <stdio.h>
#include <cs50.h>

// function
int get_height();
void print_row(int spaces, int bricks);

int main(){
    int height = get_height();

    for (int i = 0; i < height; i++)
    {
        int spaces = height - i - 1; // Calculate spaces
        int bricks = i + 1;          // Number of bricks in this row
        print_row(spaces, bricks);
    }
    return 0;
}

// height until it's >= 1
int get_height(){
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1);  // check for height >= 1 as per problem (no upper limit)
    return h;
}

// Prints a single row of the pyramid
void print_row(int spaces, int bricks)
{
    for (int i = 0; i < spaces; i++)
    {
        printf(" ");
    }
    for (int i = 0; i < bricks; i++)
    {
        printf("#");
    }
    printf("\n");
}

