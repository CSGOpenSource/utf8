#include <stdio.h>


int
nonascii(FILE *file, int should_print)
    {
    int line = 0;
    int pos = 0;
    int c = fgetc(file);
    int any_found = 0;
    while (c != EOF)
        {
        if (c != '\n')
            ++pos;
        else
            {
            pos = 0;
            ++line;
            }

        if (c > 127)
            {
            any_found = 1;
            if (should_print)
                printf("(%x) %d:%d\n", c, line, pos);
            else
                break;
            }

        c = fgetc(file);
        }
    return any_found;
    }

