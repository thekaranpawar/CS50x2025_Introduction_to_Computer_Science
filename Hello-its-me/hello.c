#include <stdio.h>
#include <cs50.h>

int main(){

    string name = get_string("What is ur name?");
    printf("hello, %s\n", name);
    return 0;
}
