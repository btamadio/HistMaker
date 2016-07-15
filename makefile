install: RunHists RunTruthHists

RunHists: obj/RunHists.o
	g++ -o RunHists obj/RunHists.o `root-config --libs`

obj/RunHists.o: src/HistMaker.cxx src/HistMaker.h src/RunHists.cxx
	g++ -c `root-config --cflags` src/RunHists.cxx
	mkdir -p obj
	mv RunHists.o obj

RunTruthHists: obj/RunTruthHists.o
	g++ -o RunTruthHists obj/RunTruthHists.o `root-config --libs`

obj/RunTruthHists.o: src/TruthHistMaker.cxx src/TruthHistMaker.h src/RunTruthHists.cxx
	g++ -c `root-config --cflags` src/RunTruthHists.cxx
	mkdir -p obj
	mv RunTruthHists.o obj

clean:
	rm obj/*.o RunHists RunTruthHists


