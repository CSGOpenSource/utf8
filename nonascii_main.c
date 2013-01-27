/* nonascii_main.c */

#include <stdio.h>

int nonascii(FILE *, void (*)(int, int, int));

static void myprint(int c, int line, int pos)
    {
    printf("(%x) %d:%d\n", c, line, pos);
    }

int 
main(int argc, char *argv[])
    {
    void (*print)(int, int, int) = NULL;
    FILE *the_file = stdin;
    char *the_file_name = NULL;
    if (argc > 1)
        {
        if (argv[1][0] == '-')
            {
            print = myprint;
            if (argc > 2)
                {
                the_file_name = argv[2];
                the_file = fopen(argv[2], "rb");
                }
            }
        else
            {
            the_file_name = argv[1];
            the_file = fopen(argv[1], "rb");
            }
        }

    if (the_file == NULL)
        {
        if (the_file_name)
            perror(the_file_name);
        else
            fprintf(stderr, "Looks like stdin is NULL\n");
        return -1;
        }

    if (argc > 2)
        printf("Scanning %s:\n", argv[2]);

    /* reverse logic for shell */
    return !nonascii(the_file, print);
    }

