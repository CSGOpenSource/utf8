# makefile

CFLAGS = -g

all: guess_utf8 nonascii

guess_utf8: guess_utf8.o guess_utf8_main.o

nonascii: nonascii.o nonascii_main.o

clean:
	rm *.o guess_utf8
