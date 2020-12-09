#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, char **argv)
{
    if (argc > 2 || argc < 2)
// Check if argument counter is smaller or bigger than 2
    {
        string status;
        status = "Usage: ./caesar key";
        printf("%s\n", status);
        exit(1);
    }
    else if (argc == 2)
// If argc is equal to 2, then check if it is a ASCII number
    {
        string keyCheck;
        keyCheck = argv[1];
        int keyLenght = 0;
        keyLenght = strlen(keyCheck);
        int j = 0;
        for (j = 0; j < keyLenght; j++)
        {
            if (keyCheck[j] < 48 || keyCheck[j] > 57)
            {
                string status;
                status = "Usage: ./caesar key";
                printf("%s\n", status);
                exit(1);
            }
        }
    }

    string messagePlain;
    string messagePlain01;
    messagePlain = get_string("Enter text: ");
    messagePlain01 = messagePlain;

    int key;
    key = atoi(argv[1]);
// Get second argument vector and convert it to a integer

    int i = 0;
    int lenght = 0;
    lenght = strlen(messagePlain01);
    string messageEncrypted;

    int newKey = 0;
    if (key >= 26)
    {
        newKey = (key % 26);
    }
    else
    {
        newKey = key;
    }

    for (i = 0; i < lenght; i++)
// Iterate through text
    {
        if (messagePlain01[i] >= 65 && messagePlain01[i] <= 90)
        {
            if ((messagePlain01[i] + newKey) > 90)
            {
                messagePlain01[i] -= 26;
            }
            messagePlain01[i] += newKey;
        }

        else if (messagePlain01[i] >= 97 && messagePlain01[i] <= 122)
        {
            if ((messagePlain01[i] + newKey) > 122)
            {
                messagePlain01[i] -= 26;
            }
            messagePlain01[i] += newKey;
        }
    }
    messageEncrypted = messagePlain01;
    printf("ciphertext: %s\n", messageEncrypted);
}

