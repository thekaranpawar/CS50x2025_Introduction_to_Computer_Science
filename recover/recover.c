#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define BLOCK_SIZE 512

// Function prototype
bool is_jpeg_header(uint8_t buffer[]);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open the memory card file
    FILE *input_file = fopen(argv[1], "r");
    if (input_file == NULL)
    {
        printf("Could not open file: %s\n", argv[1]);
        return 1;
    }

    // Declare buffer for 512 bytes
    uint8_t buffer[BLOCK_SIZE];

    // JPEG output file pointer
    FILE *output_file = NULL;

    // Filename buffer
    char filename[8];  // e.g., "000.jpg" + '\0'

    // File counter
    int file_count = 0;

    // Read 512 bytes at a time
    while (fread(buffer, sizeof(uint8_t), BLOCK_SIZE, input_file) == BLOCK_SIZE)
    {
        // Check if start of a new JPEG
        if (is_jpeg_header(buffer))
        {
            // Close previous file if open
            if (output_file != NULL)
            {
                fclose(output_file);
            }

            // Create new filename
            sprintf(filename, "%03i.jpg", file_count);

            // Open new file
            output_file = fopen(filename, "w");
            if (output_file == NULL)
            {
                printf("Could not create output file: %s\n", filename);
                fclose(input_file);
                return 1;
            }

            file_count++;
        }

        // If a JPEG file is open, write the block to it
        if (output_file != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), BLOCK_SIZE, output_file);
        }
    }

    // Close any remaining open files
    if (output_file != NULL)
    {
        fclose(output_file);
    }

    fclose(input_file);
    return 0;
}

// Check if the buffer contains a JPEG header
bool is_jpeg_header(uint8_t buffer[])
{
    return buffer[0] == 0xff &&
           buffer[1] == 0xd8 &&
           buffer[2] == 0xff &&
           (buffer[3] & 0xf0) == 0xe0;
}

