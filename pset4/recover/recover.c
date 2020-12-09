#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Argument count must be two: I want to deal with one file at the time.
    if (argc > 2 || argc < 2)
    {
        fprintf(stderr, "Usage: ./recover image file name.extension\n");
        return 1;
    }

    // Opening file with fopen & check if it works and if not, returns false. "r" = Opens an existing text file for reading purpose.
    FILE *fileToCheck = fopen(argv[1], "r");
    if (fileToCheck == NULL)
    {
        fprintf(stderr, "File could not e opened: %s.\n", argv[1]);
        return 1;
    }

    // Call for image file to be checked
    FILE *imageToCheck;

    // Create array for nameOfFile of 10 characters.
    char nameOfFile[9];

    // Allocate memory with malloc for bitFinder.
    unsigned char *bitFinder = malloc(512);

    // Create a counter.
    int counter = 0;

    while (fread(bitFinder, 512, 1, fileToCheck))
    {
        // Test to check if it is a jpg file: see excercise.
        if (bitFinder[0] == 0xff && bitFinder[1] == 0xd8 && bitFinder[2] == 0xff && (bitFinder[3] & 0xf0) == 0xe0)
        {
            // If counter is superior to zero, close the imageToCheck.
            if (counter > 0)
            {
                fclose(imageToCheck);
            }

            // Send output of nameOfFile to pointed file.
            sprintf(nameOfFile, "%03d.jpg", counter);

            // Open image file and write.
            imageToCheck = fopen(nameOfFile, "w");

            // Check if imageToCheck is created. If not close file & free memory.
            if (imageToCheck == NULL)
            {
                fclose(fileToCheck);
                free(bitFinder);
                fprintf(stderr, "Could not create output JPG %s", nameOfFile);
                return 3;
            }

            counter++;
        }

        // If not jpg exists, start writing to current file.
        if (counter > 0)
        {
            fwrite(bitFinder, 512, 1, imageToCheck);
        }
    }

    // Close file and free memory.
    fclose(imageToCheck);
    fclose(fileToCheck);
    free(bitFinder);
    return 0;
}