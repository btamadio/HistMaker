#include <iostream>
#include <string>
#include <TFile.h>
#include <TTree.h>
#include "TruthHistMaker.cxx"
#include <cstdlib>
using namespace std;

int main(int argc, char *argv[]){
  if (argc < 5){
    cout<<"Not enough command line arguments."<<endl;
    cout<<"usage: RunHists <infile> <outfile> <xsec> <treeName>"<<endl;
    return 0;
  }
  string inFileName = argv[1];
  string outFileName = argv[2];
  float xsec = atof(argv[3]);
  string treeName = argv[4];
  TFile *f = TFile::Open(inFileName.c_str());
  TTree *t = (TTree*)f->Get(("outTree/"+treeName).c_str());
  TruthHistMaker h(t,outFileName,xsec);
  h.SetLumi(5.8);
  h.SetInitEvents( t->GetEntries() );
  cout<<"infile: "<<inFileName<<"\t Initial events: "<<t->GetEntries()<<endl;
  h.SetupOutput();
  h.Loop();
  return 0;
}
