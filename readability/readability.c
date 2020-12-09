#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

int main(void)
{
    string textMain;
    textMain = get_string("Enter text: ");

    int characterCounter = 0;
    int letterCounter = 0;
    int wordCounter = 1;
    int sentenceCounter = 0;
    
    characterCounter = strlen(textMain);
    
    int i = 0;
    for (i = 0; characterCounter > i; i++)
    {
        if ((textMain[i] >= 'a' && textMain[i] <= 'z') || (textMain[i] >= 'A' && textMain[i] <= 'Z'))
        {
            letterCounter++;
        }
        if (textMain[i] == ' ')
        {
            wordCounter++;
        }
        if (textMain[i] == '.' || textMain[i] == '!' || textMain[i] == '?')
        {
            sentenceCounter++;
        }
    }
    //printf("%i character(s)\n", characterCounter);
    //printf("%i letter(s)\n", letterCounter);
    //printf("%i word(s)\n", wordCounter);
    //printf("%i sentence(s)\n", sentenceCounter);

    float L = 0;
    float S = 0;
    
    L = ((float)letterCounter / (float)wordCounter) * 100;
    S = ((float)sentenceCounter / (float)wordCounter) * 100;
    //printf("%f, %f\n", L, S);
    
    int index = 0;
    index = round((0.0588 * L) - (0.296 * S) - 15.8);
    
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 1 && index <= 16)
    {
        printf("Grade %i\n", index);
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
     

}