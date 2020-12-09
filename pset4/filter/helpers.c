#include <math.h>
#include "helpers.h"


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float rgbToGrey;
    
    for (int a = 0; a < width; a++)
    {
        for (int b = 0; b < height; b++)
        {
// average then assign
            rgbToGrey = round((image[b][a].rgbtRed + image[b][a].rgbtGreen + image[b][a].rgbtBlue) / 3.00);
            image[b][a].rgbtRed = rgbToGrey;
            image[b][a].rgbtGreen = rgbToGrey;
            image[b][a].rgbtBlue = rgbToGrey;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaR;
    int sepiaG;
    int sepiaB;
    
    for (int a = 0; a < width; a++)
    {
        for (int b = 0; b < height; b++)
        {
// From excercice
            sepiaR = round((0.393 * image[b][a].rgbtRed) + (0.769 * image[b][a].rgbtGreen) + (0.189 * image[b][a].rgbtBlue));
            if (sepiaR > 255)
            {
                sepiaR = 255;
            }
            
            sepiaG = round((0.349 * image[b][a].rgbtRed) + (0.686 * image[b][a].rgbtGreen) + (0.168 * image[b][a].rgbtBlue));
            if (sepiaG > 255)
            {
                sepiaG = 255;
            }
            
            sepiaB = round((0.272 * image[b][a].rgbtRed) + (0.534 * image[b][a].rgbtGreen) + (0.131 * image[b][a].rgbtBlue));
            if (sepiaB > 255)
            {
                sepiaB = 255;
            }
            
            image[b][a].rgbtRed = sepiaR;
            image[b][a].rgbtGreen = sepiaG;
            image[b][a].rgbtBlue = sepiaB;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int tempArray[3];
    
    for (int a = 0; a < height; a++)
    {
        for (int b = 0; b < width / 2; b++) 
        {
// mirror to half then assign
            tempArray[0] = image[a][b].rgbtRed;
            tempArray[1] = image[a][b].rgbtGreen;
            tempArray[2] = image[a][b].rgbtBlue;
            
            image[a][b].rgbtRed = image[a][width - b - 1].rgbtRed;
            image[a][b].rgbtGreen = image[a][width - b - 1].rgbtGreen;
            image[a][b].rgbtBlue = image[a][width - b - 1].rgbtBlue;
            
            image[a][width - b - 1].rgbtRed = tempArray[0];
            image[a][width - b - 1].rgbtGreen = tempArray[1];
            image[a][width - b - 1].rgbtBlue = tempArray[2];
            
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int accumRed;
    int accumGreen;
    int accumBlue;
    float counter;
    
    RGBTRIPLE tempArray[height][width];
// temporary array
    
    for (int a = 0; a < width; a++)
    {
        for (int b = 0; b < height; b++)
        {
            accumRed = 0;
            accumGreen = 0;
            accumBlue = 0;
            counter = 0;
            
            for (int z = -1; z < 2; z++)
            {
// if out of pic and then move value to tempArray
                if (z + b < 0)
                {
                    continue;
                }
                // commenting to do
                if (z + b > height - 1)
                {
                    continue;
                }
                // commenting to do
                for (int y = -1; y < 2; y++)
                {
                    if (a + y < 0)
                    {
                        continue;
                    }
                    // commenting to do
                    if (a + y > width - 1)
                    {
                        continue;
                    }
                    // commenting to do
//accumulates
                    accumRed = accumRed + image[b + z][a + y].rgbtRed;
                    accumBlue = accumBlue + image[b + z][a + y].rgbtBlue;
                    accumGreen = accumGreen + image[b + z][a + y].rgbtGreen;
                    counter = counter + 1;
                }
            }
//assign the accumulator average
            tempArray[b][a].rgbtRed = round(accumRed / counter);
            tempArray[b][a].rgbtGreen = round(accumGreen / counter);
            tempArray[b][a].rgbtBlue = round(accumBlue / counter);
        }
    }
    
    for (int a = 0; a < width; a++)
    {
        for (int b = 0; b < height; b++) 
        {
// reassign values
            image[b][a].rgbtRed = tempArray[b][a].rgbtRed;
            image[b][a].rgbtGreen = tempArray[b][a].rgbtGreen;
            image[b][a].rgbtBlue = tempArray[b][a].rgbtBlue;
        }
    }
    return;
}
// I'm considering more comments
// commenting to do
