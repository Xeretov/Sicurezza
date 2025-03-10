//Per compilare: gcc stackoverflow.c
//Per compilare e generare assembler: gcc -S stackoverflow.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char * gets(char*);

int numero=100;
char nome[16] = "Franco";

char * login() {
    char username[32];
    printf("Username: ");
    gets(username);
    char * p = (char*)malloc(32);
    strcpy(p, username);
    return p;
}

int main() {
    char * username;
    username = login();
    printf("User: %s\n", username);
}
