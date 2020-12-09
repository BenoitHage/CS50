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
        status = "Usage: ./substitution key";
        printf("%s\n", status);
        exit(1);
    }
    else if (argc == 2)
// If argc is equal to 2, then check if it a capital letter
    {
        string keyCheck;
        keyCheck = (argv[1]);
        int keyLenght = 0;
        keyLenght = strlen(keyCheck);
        
        if (keyLenght > 26 || keyLenght < 26)
// Check if argv is 26 character long
        {
            string status;
            status = "Key must contain 26 characters.";
            printf("%s\n", status);
            exit(1);
        }
        
        int z = 0;        
        for (z = 0; z < keyLenght; z++)
// Check if argv is only letters from a to z and from A to Z
        {
            if ((keyCheck[z] < 97 || keyCheck[z] > 122) && (keyCheck[z] < 65 || keyCheck[z] > 90))
            {
                string status;
                status = "Usage: ./substitution key";
                printf("%s\n", status);
                exit(1);
            }
        }
    }
    
    string keySave01;
    string keySave02;
    keySave01 = (argv[1]);
    keySave02 = (argv[1]);
    
    int k = 0;
    int l = 0;
    int keyDuplicate = 0;
    
    for (k = 0; k < strlen(keySave01); k++)
// Check if there are duplicate in keys
    {
        for (l = 0; l < strlen(keySave02); l++)
        {
            if (keySave01[k] == keySave02[l])
            {
                keyDuplicate++;
            }
        }
    }
    
    if (keyDuplicate > 26)
    {
        printf("There are %i same characters in given key\n", (keyDuplicate - 26));
        exit(1);
    }
   
    string messagePlain;
    string messagePlain01;
    messagePlain = get_string("Enter text: ");
    messagePlain01 = messagePlain;
// Takes the user input and stores it to messagePlain
    
    string alphabetArray;
    alphabetArray = "abcdefghijklmnopqrstuvwxyz";

    int i = 0;
    int j = 0;
    
    for (i = 0; i < strlen(messagePlain01); i++)
// Substitute the message by the letter corresponding to their position in the key
    {
        for (j = 0; j < strlen(alphabetArray); j++)
        {
            if (islower(messagePlain01[i]) > 0)
            {
                if (tolower(messagePlain01[i]) == alphabetArray[j])
                {
                    messagePlain01[i] = tolower(argv[1][j]);
                    break;
                }               
            }
            else if (isupper(messagePlain01[i]) > 0)
            {
                if (tolower(messagePlain01[i]) == alphabetArray[j])
                {
                    messagePlain01[i] = toupper(argv[1][j]);
                    break;
                }
            }
        }
    }
    printf("ciphertext:  %s\n", messagePlain01);
}