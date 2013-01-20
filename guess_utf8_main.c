/* guess_utf8_main.c */

#include <stdio.h>

int guess_utf8(FILE *);

int 
main(int argc, char *argv[])
    {
    FILE *the_file = stdin;
    int echo = 0;
    int rval = 0;
    if (argc > 1)
        {
        if (argv[1][0] == '-')
            echo = 1;
        else
            the_file = fopen(argv[1], "rb");
        }

    if (the_file == NULL)
        {
        if (argc > 1)
            perror(argv[1]);
        else
            fprintf(stderr, "Looks like stdin is NULL\n");
        return -1;
        }

    rval = guess_utf8(the_file);
    if (echo)
        printf(rval ? "yes" : "no");

    /* reverse logic for use in shell tools like find */
    return !rval;
    }

