/* nonascii.c */

#include <stdio.h>


int
nonascii(FILE *file, void (*print)(int, int, int))
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
            if (print)
                print(c, line, pos);
            else
                break;
            }

        c = fgetc(file);
        }
    return any_found;
    }

