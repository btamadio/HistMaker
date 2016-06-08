install: RunHists

RunHists: obj/RunHists.o
	g++ -o RunHists obj/RunHists.o `root-config --libs`

obj/RunHists.o: src/HistMaker.cxx src/HistMaker.h src/RunHists.cxx
	g++ -c `root-config --cflags` src/RunHists.cxx
	mkdir -p obj
	mv RunHists.o obj

clean:
	rm obj/*.o RunHists


