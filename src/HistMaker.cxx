#define HistMaker_cxx
#include "HistMaker.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <string>

#include <algorithm>
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
   TH1F *h_cutflow = new TH1F(cutflowName.c_str(),"cutflow histogram",11,0.5,11.5);
   h_cutflow->GetXaxis()->SetBinLabel(1,"Initial");
   h_cutflow->GetXaxis()->SetBinLabel(2,"GRL");
   h_cutflow->GetXaxis()->SetBinLabel(3,"trigger");
   h_cutflow->GetXaxis()->SetBinLabel(4,"event cleaning");
   h_cutflow->GetXaxis()->SetBinLabel(5,"AkT4 presel");
   h_cutflow->GetXaxis()->SetBinLabel(6,"n_{fatjet} == 3");
   h_cutflow->GetXaxis()->SetBinLabel(7,"n_{fatjet} == 3 && b-tag");
   h_cutflow->GetXaxis()->SetBinLabel(8,"n_{fatjet} == 4 && 200 < MJ < 600");
   h_cutflow->GetXaxis()->SetBinLabel(9,"n_{fatjet} == 4 && b-tag && 200 < MJ < 600");
   h_cutflow->GetXaxis()->SetBinLabel(10,"n_{fatjet} #geq 5 && 200 < MJ < 60");
   h_cutflow->GetXaxis()->SetBinLabel(11,"n_{fatjet} #geq 5 && b-tag && 200 < MJ < 600");

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
      float bw = 1;
      int iCut = 1;
      float ht = 0;
      float mj = 0;
      int nBTag = 0;
      bool passLeadJet = false;
      int nFatJet = 0;
      vector<TLorentzVector> fj4mom;
      if (m_isMC){
	w = 1E6 * m_lumi * weight / m_denom;
	bw = w*weight_jet_SFFix70->at(0);
      }
      h_cutflow->Fill(++iCut,w);
      bool passTrig = false;
      for( auto s : *passedTriggers ){
	if ( s == "HLT_ht850_L1J100" || s == "HLT_ht850_L1J75" ){
	  passTrig = true;
	}
      }
      if ( !passTrig ){ continue; }
      h_cutflow->Fill(++iCut,w);
      if(!m_isMC){
	if ( SCTError == 1 || LArError == 1 || TileError == 1 ){ continue; }
      }
      h_cutflow->Fill(++iCut,w);
      for( int i = 0; i < jet_pt->size(); i++){
	if ( jet_pt->at(i) > m_jetPtCut && fabs(jet_eta->at(i)) < m_jetEtaCut && jet_clean_passLooseBad->at(i) == 1){
	  ht += jet_pt->at(i);
	  if (jet_isFix70->at(i) == 1){ nBTag ++; }
	  if ( jet_pt->at(i) > m_leadJetPtCut ){ passLeadJet = true; }
	}
      }
      if (ht < m_htCut || !passLeadJet){ continue; }
      h_cutflow->Fill(++iCut,w);
      for( int i = 0; i < fatjet_pt->size(); i++){
	if(fatjet_pt->at(i) > m_fatJetPtCut && fabs(fatjet_eta->at(i)) < m_fatJetEtaCut && fatjet_m->at(i)/fatjet_pt->at(i) < m_fatJetMpTCut){
	  TLorentzVector this4mom;
	  this4mom.SetPtEtaPhiM(fatjet_pt->at(i),fatjet_eta->at(i),fatjet_phi->at(i),fatjet_m->at(i));
	  fj4mom.push_back(this4mom);
	  nFatJet++;
	}
      }
      sort(fj4mom.begin(), fj4mom.end(), reorder);
      int nJetLoop = 4;
      if (fj4mom.size() < 4){
	nJetLoop = fj4mom.size();
      }
      for( int i = 0; i < nJetLoop; i++){
	mj += fj4mom.at(i).M();
      }
      iCut++;
      if(nFatJet == 3){ h_cutflow->Fill(iCut,w); }
      iCut++;
      if(nFatJet == 3 && nBTag >= 1){ h_cutflow->Fill(iCut,bw); }
      iCut++;
      if(nFatJet == 4 && mj > 200 && mj < 600){ h_cutflow->Fill(iCut,w); }
      iCut++;
      if(nFatJet == 4 && nBTag >= 1 && mj > 200 && mj < 600){ h_cutflow->Fill(iCut,bw); }
      iCut++;
      if(nFatJet >= 5 && mj > 200 && mj < 600){ h_cutflow->Fill(iCut,w); }
      iCut++;
      if(nFatJet == 5 && nBTag >=1 && mj > 200 && mj < 600){ h_cutflow->Fill(iCut,w); }
   }
   m_outFile->cd();
   m_outFile->Write();
}

bool HistMaker::reorder(const TLorentzVector &a, const TLorentzVector &b)
{
   return a.Pt() > b.Pt();
}
