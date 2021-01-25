
all: compil run

run: 
	./prog

compil: canevas_graphe.c
	gcc canevas_graphe.c -o prog -g -O2 -lm


clean:
	rm -rf *.o
	rm -rf *.dot
	rm -rf *.ps
	rm -rf prog

debug:
	valgrind ./prog

