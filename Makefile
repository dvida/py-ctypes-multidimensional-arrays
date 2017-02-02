CC = gcc
CFLAGS = -g -Wall -fPIC -lm -std=gnu99 -O3 -march=native -DCONJUGRAD_FLOAT=64

all: libmyfunc.so

m.PHONY : clean

libmyfunc.so: myfunc.o
	gcc -shared -Wl,-soname,$@ -o $@ $^

%.o: %.c
	$(CC) -c $(CFLAGS) $<

clean:
	rm -vf libmyfunc.so *.o
