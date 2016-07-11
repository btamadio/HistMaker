#define TruthHistMaker_cxx
#include "TruthHistMaker.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
void TruthHistMaker::SetupOutput(){
  m_outFile = TFile::Open(m_outFileName.c_str(),"RECREATE");
}
void TruthHistMaker::Loop()
{
   if (fChain == 0) return;
   fChain->GetEntry(0);
   string suffix="_"+to_string(runNumber);

   TH1F* h_SRyield = new TH1F(("h_SRyield"+suffix).c_str(),"signal region yield",20,0.5,20.5);
   h_SRyield->GetXaxis()->SetBinLabel(1,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.6 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(2,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.65 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(3,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.7 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(4,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.75 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(5,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.8 TeV");

   h_SRyield->GetXaxis()->SetBinLabel(6,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.6 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(7,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.65 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(8,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.7 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(9,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.75 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(10,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.8 TeV"); 

   h_SRyield->GetXaxis()->SetBinLabel(11,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.6 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(12,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.65 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(13,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.7 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(14,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.75 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(15,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.8 TeV");

   h_SRyield->GetXaxis()->SetBinLabel(16,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.6 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(17,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.65 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(18,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.7 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(19,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.75 TeV");
   h_SRyield->GetXaxis()->SetBinLabel(20,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.8 TeV");

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;
   cout<<"m_lumi = "<<m_lumi<<"\t m_weight ="<<m_weight<<"\t xsec = "<<0.1*m_weight/m_lumi<<endl;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      float mj = 0;
      int nBTag = 0;
      float dy = 0;
      bool passLeadJet = false;
      int nFatJet = 0;
      vector<TLorentzVector> fj4mom;
      //fat jets
      for( int i = 0; i < fatjet_pt->size(); i++){
	if(fatjet_pt->at(i) > m_fatJetPtCut && fabs(fatjet_eta->at(i)) < m_fatJetEtaCut && fatjet_m->at(i)/fatjet_pt->at(i) < m_fatJetMpTCut){
	  TLorentzVector this4mom;
	  this4mom.SetPtEtaPhiM(fatjet_pt->at(i),fatjet_eta->at(i),fatjet_phi->at(i),fatjet_m->at(i));
	  fj4mom.push_back(this4mom);
	  nFatJet++;
	  if( fatjet_pt->at(i) > m_leadJetPtCut ) { passLeadJet = true; }
	}
      }      
      if ( !passLeadJet ) { continue; }
      for( int i = 0; i < jet_pt->size(); i++){
       	if ( jet_pt->at(i) > m_jetPtCut && fabs(jet_eta->at(i)) < m_jetEtaCut && jet_GhostBHadronsFinalCount->at(i) > 0){
	    nBTag ++; 
       	}
      }
      sort(fj4mom.begin(), fj4mom.end(), reorder);
      if ( fj4mom.size() >= 2 ) { dy = fabs(fj4mom.at(0).Eta() - fj4mom.at(1).Eta()); }
      int nJetLoop = 4;
      if (fj4mom.size() < 4){ nJetLoop = fj4mom.size(); }
      for( int i = 0; i < nJetLoop; i++){ mj += fj4mom.at(i).M(); }
      int sr=0;
      if (nFatJet >= 4 && dy < 1.4){
        if (nBTag >= 1){
      	  if (mj > 600){h_SRyield->Fill(sr+1,m_weight); }
      	  if (mj > 650){h_SRyield->Fill(sr+2,m_weight); }
      	  if (mj > 700){h_SRyield->Fill(sr+3,m_weight); }
      	  if (mj > 750){h_SRyield->Fill(sr+4,m_weight); }
      	  if (mj > 800){h_SRyield->Fill(sr+5,m_weight); }
      	}
      	if (mj > 600){ h_SRyield->Fill(sr+6,m_weight); }
	if (mj > 650){ h_SRyield->Fill(sr+7,m_weight); }
	if (mj > 700){ h_SRyield->Fill(sr+8,m_weight); }
	if (mj > 750){ h_SRyield->Fill(sr+9,m_weight); }
	if (mj > 800){ h_SRyield->Fill(sr+10,m_weight); }
      }
      sr=10;
      if (nFatJet >= 5 && dy < 1.4){
        if (nBTag >= 1){
      	  if (mj > 600){h_SRyield->Fill(sr+1,m_weight); }
      	  if (mj > 650){h_SRyield->Fill(sr+2,m_weight); }
      	  if (mj > 700){h_SRyield->Fill(sr+3,m_weight); }
      	  if (mj > 750){h_SRyield->Fill(sr+4,m_weight); }
      	  if (mj > 800){h_SRyield->Fill(sr+5,m_weight); }
      	}
      	if (mj > 600){ h_SRyield->Fill(sr+6,m_weight); }
	if (mj > 650){ h_SRyield->Fill(sr+7,m_weight); }
	if (mj > 700){ h_SRyield->Fill(sr+8,m_weight); }
	if (mj > 750){ h_SRyield->Fill(sr+9,m_weight); }
	if (mj > 800){ h_SRyield->Fill(sr+10,m_weight); }
      }
   }
   m_outFile->cd();
   m_outFile->Write();
}
bool TruthHistMaker::reorder(const TLorentzVector &a, const TLorentzVector &b)
{
   return a.Pt() > b.Pt();
}
