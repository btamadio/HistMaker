#define HistMaker_cxx
#include "HistMaker.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <string>
void HistMaker::SetupOutput(){
  m_outFile = TFile::Open(m_outFileName.c_str(),"RECREATE");
  cout<<"Opened output file "<<m_outFileName<<endl;
}
void HistMaker::Loop()
{
   if (fChain == 0) return;
   string cutflowName = "h_cutflow";

   if(!m_isMC){
     fChain->GetEntry(0);
     cutflowName += "_"+to_string(runNumber);
   }
   Long64_t nentries = fChain->GetEntriesFast();
   TH1F *h_cutflow = new TH1F(cutflowName.c_str(),"cutflow histogram",10,0.5,10.5);
   h_cutflow->GetXaxis()->SetBinLabel(1,"Initial");
   h_cutflow->GetXaxis()->SetBinLabel(2,"GRL");
   h_cutflow->GetXaxis()->SetBinLabel(3,"trigger");
   h_cutflow->GetXaxis()->SetBinLabel(4,"AkT4 presel");
   h_cutflow->GetXaxis()->SetBinLabel(5,"n_{fatjet} == 3");
   h_cutflow->GetXaxis()->SetBinLabel(6,"n_{fatjet} == 3 && b-tag");
   h_cutflow->GetXaxis()->SetBinLabel(7,"n_{fatjet} == 4");
   h_cutflow->GetXaxis()->SetBinLabel(8,"n_{fatjet} == 4 && b-tag");
   h_cutflow->GetXaxis()->SetBinLabel(9,"n_{fatjet} #geq 5");
   h_cutflow->GetXaxis()->SetBinLabel(10,"n_{fatjet} #geq 5 && b-tag");

   if (m_isMC){
     fChain->GetEntry(0);
     h_cutflow->SetBinContent(1,1E6*m_lumi*weight);
     h_cutflow->GetXaxis()->SetBinLabel(1,"#sigma L");
     h_cutflow->GetXaxis()->SetBinLabel(2,"derivation");
   }
   else{
     h_cutflow->SetBinContent(1,m_denom);
   }
   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      float w = 1;
      if (m_isMC){
	w = 1E6 * m_lumi * weight / m_denom;
      }
      h_cutflow->Fill(2,w);
   }
   m_outFile->cd();
   m_outFile->Write();
}
