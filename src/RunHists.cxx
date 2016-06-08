#include <iostream>
#include <string>
#include <TFile.h>
#include <TTree.h>
#include "HistMaker.cxx"
#include <cstdlib>
using namespace std;
class TemplateMaker;
int main(int argc, char *argv[]){
  if (argc < 4){
    cout<<"Not enough command line arguments."<<endl;
    cout<<"usage: RunHists <infile> <outfile> <denom or initial events>"<<endl;
    return 0;
  }
  string inFileName = argv[1];
  string outFileName = argv[2];
  float denom = atof(argv[3]);
  TFile *f = TFile::Open(inFileName.c_str());
  TTree *t = (TTree*)f->Get("outTree/nominal");
  HistMaker h(t,outFileName,denom);
  h.SetupOutput();
  h.Loop();
  return 0;
}
