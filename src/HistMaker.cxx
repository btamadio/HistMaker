#define HistMaker_cxx
#include "HistMaker.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TString.h>
#include <string>
#include <utility>
#include <map>
#include <algorithm>
void HistMaker::SetupOutput(){
  m_outFile = TFile::Open(m_outFileName.c_str(),"RECREATE");
  cout<<"Opened output file "<<m_outFileName<<endl;
}
void HistMaker::Loop(){
   if (fChain == 0) return;
   string cutflowName = "h_cutflow";
   string suffix = "";
   if(!m_isMC){
     fChain->GetEntry(0);
     suffix="_"+to_string(runNumber);
     readGRL();
   }
   else{
     fChain->GetEntry(0);
     suffix="_"+to_string(mcChannelNumber);
   }
   Long64_t nentries = fChain->GetEntriesFast();
   TH1F *h_cutflow = new TH1F(("h_cutflow"+suffix).c_str(),"cutflow histogram",12,0.5,12.5);
   //For data: 2= every event looped over, 3= events that pass GRL
   //For MC: 1 = 2 = xsec*luminosity, 3= all events looped over
   h_cutflow->GetXaxis()->SetBinLabel(1,"CBC Selected");
   h_cutflow->GetXaxis()->SetBinLabel(2,"nEvents Looped over");
   h_cutflow->GetXaxis()->SetBinLabel(3,"GRL");
   h_cutflow->GetXaxis()->SetBinLabel(4,"event cleaning");
   h_cutflow->GetXaxis()->SetBinLabel(5,"trigger");
   h_cutflow->GetXaxis()->SetBinLabel(6,"p_T^{lead} > 440 GeV");
   h_cutflow->GetXaxis()->SetBinLabel(7,"n_{fatjet} == 3");
   h_cutflow->GetXaxis()->SetBinLabel(8,"n_{fatjet} == 3 && b-tag");
   h_cutflow->GetXaxis()->SetBinLabel(9,"n_{fatjet} == 4 && MJ < 600");
   h_cutflow->GetXaxis()->SetBinLabel(10,"n_{fatjet} == 4 && MJ < 600 && b-tag");
   h_cutflow->GetXaxis()->SetBinLabel(11,"n_{fatjet} #geq 5 && MJ < 600");
   h_cutflow->GetXaxis()->SetBinLabel(12,"n_{fatjet} #geq 5 && MJ < 600 && b-tag");

   TH1F *h_eventCat = new TH1F(("h_eventcat"+suffix).c_str(),"event categories",18,0.5,18.5);
   h_eventCat->GetXaxis()->SetBinLabel(1,"= 3 jet, b-veto, total");
   h_eventCat->GetXaxis()->SetBinLabel(2,"= 3 jet, b-tag, total");
   h_eventCat->GetXaxis()->SetBinLabel(3,"= 3 jet, b-inc, total");
   h_eventCat->GetXaxis()->SetBinLabel(4,"= 3 jet, b-veto, 200 < MJ < 600");
   h_eventCat->GetXaxis()->SetBinLabel(5,"= 3 jet, b-tag, 200 < MJ < 600");
   h_eventCat->GetXaxis()->SetBinLabel(6,"= 3 jet, b-inc, 200 < MJ < 600");
   h_eventCat->GetXaxis()->SetBinLabel(7,"= 4 jet, b-veto, total");
   h_eventCat->GetXaxis()->SetBinLabel(8,"= 4 jet, b-tag, total");
   h_eventCat->GetXaxis()->SetBinLabel(9,"= 4 jet, b-inc, total");
   h_eventCat->GetXaxis()->SetBinLabel(10,"= 4 jet, b-veto, 200 < MJ < 600");
   h_eventCat->GetXaxis()->SetBinLabel(11,"= 4 jet, b-tag, 200 < MJ < 600");
   h_eventCat->GetXaxis()->SetBinLabel(12,"= 4 jet, b-inc, 200 < MJ < 600");
   h_eventCat->GetXaxis()->SetBinLabel(13,"#geq 5 jet, b-veto, total");
   h_eventCat->GetXaxis()->SetBinLabel(14,"#geq 5 jet, b-tag, total");
   h_eventCat->GetXaxis()->SetBinLabel(15,"#geq 5 jet, b-inc, total");
   h_eventCat->GetXaxis()->SetBinLabel(16,"#geq 5 jet, b-veto, 200 < MJ < 600");
   h_eventCat->GetXaxis()->SetBinLabel(17,"#geq 5 jet, b-tag, 200 < MJ < 600");
   h_eventCat->GetXaxis()->SetBinLabel(18,"#geq 5 jet, b-inc, 200 < MJ < 600");

   TH1F* h_sigYield = new TH1F(("h_sigyield"+suffix).c_str(),"signal yield",20,0.5,20.5);
   h_sigYield->GetXaxis()->SetBinLabel(1,"n_{fatjet} = 4, b-tag, M_{J}^{#Sigma} > 0.6 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(2,"n_{fatjet} = 4, b-tag, M_{J}^{#Sigma} > 0.65 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(3,"n_{fatjet} = 4, b-tag, M_{J}^{#Sigma} > 0.7 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(4,"n_{fatjet} = 4, b-tag, M_{J}^{#Sigma} > 0.75 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(5,"n_{fatjet} = 4, b-tag, M_{J}^{#Sigma} > 0.8 TeV");

   h_sigYield->GetXaxis()->SetBinLabel(6,"n_{fatjet} = 4, b-inc, M_{J}^{#Sigma} > 0.6 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(7,"n_{fatjet} = 4, b-inc, M_{J}^{#Sigma} > 0.65 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(8,"n_{fatjet} = 4, b-inc, M_{J}^{#Sigma} > 0.7 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(9,"n_{fatjet} = 4, b-inc, M_{J}^{#Sigma} > 0.75 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(10,"n_{fatjet} = 4, b-inc, M_{J}^{#Sigma} > 0.8 TeV"); 

   h_sigYield->GetXaxis()->SetBinLabel(11,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.6 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(12,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.65 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(13,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.7 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(14,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.75 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(15,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.8 TeV");

   h_sigYield->GetXaxis()->SetBinLabel(16,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.6 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(17,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.65 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(18,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.7 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(19,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.75 TeV");
   h_sigYield->GetXaxis()->SetBinLabel(20,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.8 TeV"); 

   TH1F* h_sigYield_dy = new TH1F(("h_sigyield_dy"+suffix).c_str(),"signal yield, with |#Delta #eta| < 0.7",20,0.5,20.5);
   h_sigYield_dy->GetXaxis()->SetBinLabel(1,"n_{fatjet} = 4, b-tag, M_{J}^{#Sigma} > 0.6 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(2,"n_{fatjet} = 4, b-tag, M_{J}^{#Sigma} > 0.65 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(3,"n_{fatjet} = 4, b-tag, M_{J}^{#Sigma} > 0.7 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(4,"n_{fatjet} = 4, b-tag, M_{J}^{#Sigma} > 0.75 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(5,"n_{fatjet} = 4, b-tag, M_{J}^{#Sigma} > 0.8 TeV");

   h_sigYield_dy->GetXaxis()->SetBinLabel(6,"n_{fatjet} = 4, b-inc, M_{J}^{#Sigma} > 0.6 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(7,"n_{fatjet} = 4, b-inc, M_{J}^{#Sigma} > 0.65 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(8,"n_{fatjet} = 4, b-inc, M_{J}^{#Sigma} > 0.7 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(9,"n_{fatjet} = 4, b-inc, M_{J}^{#Sigma} > 0.75 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(10,"n_{fatjet} = 4, b-inc, M_{J}^{#Sigma} > 0.8 TeV"); 

   h_sigYield_dy->GetXaxis()->SetBinLabel(11,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.6 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(12,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.65 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(13,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.7 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(14,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.75 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(15,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.8 TeV");

   h_sigYield_dy->GetXaxis()->SetBinLabel(16,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.6 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(17,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.65 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(18,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.7 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(19,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.75 TeV");
   h_sigYield_dy->GetXaxis()->SetBinLabel(20,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.8 TeV"); 

   TH1F* h_MJ3 = new TH1F(("h_MJ3"+suffix).c_str(),"M_{J}^{#Sigma}, n_{fatjet} #geq 3",150,0,1500);
   TH1F* h_MJ4 = new TH1F(("h_MJ4"+suffix).c_str(),"M_{J}^{#Sigma}, n_{fatjet} #geq 4",150,0,1500);
   TH1F* h_MJ = new TH1F(("h_MJ"+suffix).c_str(),"M_{J}^{#Sigma}",150,0,1500);
   TH1F* h_MJ_dy7 = new TH1F(("h_MJ_dy7"+suffix).c_str(),"M_{J}^{#Sigma}, |#Delta #eta| < 0.7, n_{fatjet} #geq 5",150,0,1500);
   TH1F* h_MJ4_dy7 = new TH1F(("h_MJ4_dy7"+suffix).c_str(),"M_{J}^{#Sigma}, |#Delta #eta| < 0.7, n_{fatjet} #geq 4",150,0,1500);
     
   TH1F* h_dy_presel = new TH1F(("h_dy_presel"+suffix).c_str(),"#Delta #eta",100,0,5);
   TH1F* h_dy_n3 = new TH1F(("h_dy_n3"+suffix).c_str(),"#Delta #eta, n_{fatjet} #geq 3",100,0,5);
   TH1F* h_dy_n4 = new TH1F(("h_dy_n4"+suffix).c_str(),"#Delta #eta, n_{fatjet} #geq 4",100,0,5);
   TH1F* h_dy_n5 = new TH1F(("h_dy_n5"+suffix).c_str(),"#Delta #eta, n_{fatjet} #geq 5",100,0,5);

   if (m_isMC){
     fChain->GetEntry(0);
     h_cutflow->SetBinContent(1,1E6*m_lumi*weight);
     h_cutflow->SetBinContent(2,1E6*m_lumi*weight);
     h_cutflow->GetXaxis()->SetBinLabel(1,"#sigma L");
     h_cutflow->GetXaxis()->SetBinLabel(2,"#sigma L");
     h_cutflow->GetXaxis()->SetBinLabel(3,"derivation");
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
      int iCut = 2;
      float ht = 0;
      float mj = 0;
      int nBTag = 0;
      float dy = 0;
      int eventCat = 0;
      bool passLeadJet = false;
      int nFatJet = 0;
      vector<TLorentzVector> fj4mom;
      if (m_isMC){
	w = 1E6 * m_lumi * weight / m_denom;
	bw = w*weight_jet_SFFix70->at(0);
      }
      //GRL cut
      else{
	//all event seen
	h_cutflow->Fill(2,1);
	if( !passGRL( runNumber, lumiBlock ) ){ continue; }
      }
      h_cutflow->Fill(++iCut,w);

      //event cleaning for data
      if(!m_isMC){
	if ( SCTError || LArError || TileError ){ continue; }
      }
      h_cutflow->Fill(++iCut,w);

      //trigger
      bool passTrig = false;
      for( auto s : *passedTriggers ){
	if ( s.find("HLT_j360_a10")!=string::npos || s.find("HLT_j380_a10")!=string::npos || s.find("HLT_j400_a10")!=string::npos || s.find("HLT_j420_a10")!=string::npos ){
	  passTrig = true;
	}
      }
      if ( !passTrig ){ continue; }
      h_cutflow->Fill(++iCut,w);

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
      h_cutflow->Fill(++iCut,w);
      
      //count the b-jets
      for( int i = 0; i < jet_pt->size(); i++){
       	if ( jet_pt->at(i) > m_jetPtCut && fabs(jet_eta->at(i)) < m_jetEtaCut && jet_clean_passLooseBad->at(i) == 1){
       	  if (jet_isFix70->at(i) == 1){ nBTag ++; }
       	}
      }

      sort(fj4mom.begin(), fj4mom.end(), reorder);
      if ( fj4mom.size() >= 2 ) { dy = fabs(fj4mom.at(0).Eta() - fj4mom.at(1).Eta()); }
      int nJetLoop = 4;
      if (fj4mom.size() < 4){ nJetLoop = fj4mom.size(); }
      for( int i = 0; i < nJetLoop; i++){ mj += fj4mom.at(i).M(); }
      iCut++;
      if(nFatJet == 3){ h_cutflow->Fill(iCut,w); }
      iCut++;
      if(nFatJet == 3 && nBTag >= 1){ h_cutflow->Fill(iCut,bw); }
      iCut++;
      if(nFatJet == 4 && mj < 600){ h_cutflow->Fill(iCut,w); }
      iCut++;
      if(nFatJet == 4 && nBTag >= 1 && mj < 600){ h_cutflow->Fill(iCut,bw); }
      iCut++;
      if(nFatJet >= 5 && mj < 600){ h_cutflow->Fill(iCut,w); }
      iCut++;
      if(nFatJet >= 5 && mj < 600 && nBTag >= 1){ h_cutflow->Fill(iCut,bw); }

      if (nFatJet == 3){
        if (nBTag == 0){ h_eventCat->Fill(1,bw); }
        else{ h_eventCat->Fill(2,bw);}
        h_eventCat->Fill(3,w);
	if (mj > 200 && mj < 600){
	  if (nBTag == 0){ h_eventCat->Fill(4,bw);}
	  else{h_eventCat->Fill(5,bw);}
	  h_eventCat->Fill(6,w);
	}
      }
      if (nFatJet == 4){
        if (nBTag == 0){ h_eventCat->Fill(7,bw); }
        else{ h_eventCat->Fill(8,bw);}
        h_eventCat->Fill(9,w);
	if (mj > 200 && mj < 600){
	  if (nBTag == 0){ h_eventCat->Fill(10,bw);}
	  else{h_eventCat->Fill(11,bw);}
	  h_eventCat->Fill(12,w);
	}
      }
      if (nFatJet >= 4){
        if (nBTag == 0){ h_eventCat->Fill(13,bw); }
        else{ h_eventCat->Fill(14,bw);}
        h_eventCat->Fill(15,w);
	if (mj > 200 && mj < 600){
	  if (nBTag == 0){ h_eventCat->Fill(16,bw);}
	  else{h_eventCat->Fill(17,bw);}
	  h_eventCat->Fill(18,w);
	}
      }
    
      //Fill SR yields
      int sr=0;
      if (nFatJet == 4 || nFatJet>=5){
	if (nFatJet>=5){ sr+=10; }
        if (nBTag >= 1){
	  if (mj > 600){
	    h_sigYield->Fill(sr+1,bw);
	    if (dy < 0.7){ h_sigYield_dy->Fill(sr+1,bw); }
	  }
	  if (mj > 650){
	    h_sigYield->Fill(sr+2,bw);
	      if (dy < 0.7) { h_sigYield_dy->Fill(sr+2,bw); }
	  }
	  if (mj > 700){
	    h_sigYield->Fill(sr+3,bw);
	    if (dy < 0.7){ h_sigYield_dy->Fill(sr+3,bw); }
	  }
	  if (mj > 750){
	    h_sigYield->Fill(sr+4,bw);
	      if (dy < 0.7) { h_sigYield_dy->Fill(sr+4,bw); }
	  }
	  if (mj > 800){
	    h_sigYield->Fill(sr+5,bw);
	      if (dy < 0.7) { h_sigYield_dy->Fill(sr+5,bw); }
	  }
	}
	  if (mj > 600){
	    h_sigYield->Fill(sr+6,bw);
	    if (dy < 0.7){ h_sigYield_dy->Fill(sr+6,bw); }
	  }
	  if (mj > 650){
	    h_sigYield->Fill(sr+7,bw);
	      if (dy < 0.7) { h_sigYield_dy->Fill(sr+7,bw); }
	  }
	  if (mj > 700){
	    h_sigYield->Fill(sr+8,bw);
	    if (dy < 0.7){ h_sigYield_dy->Fill(sr+8,bw); }
	  }
	  if (mj > 750){
	    h_sigYield->Fill(sr+9,bw);
	      if (dy < 0.7) { h_sigYield_dy->Fill(sr+9,bw); }
	  }
	  if (mj > 800){
	    h_sigYield->Fill(sr+10,bw);
	      if (dy < 0.7) { h_sigYield_dy->Fill(sr+10,bw); }
	  }
      }

      if (nFatJet >= 3 and nBTag >= 1){
        h_MJ3->Fill(mj,bw);
	h_dy_n3->Fill(dy,bw);
      }
      if(nFatJet >= 4 and nBTag >= 1){
	h_MJ4->Fill(mj,bw);
	h_dy_n4->Fill(dy,bw);
	if(dy < 0.7){
	  h_MJ4_dy7->Fill(mj,bw);
	}
      }
   }
   m_outFile->cd();
   m_outFile->Write();
}

bool HistMaker::reorder(const TLorentzVector &a, const TLorentzVector &b)
{
   return a.Pt() > b.Pt();
}

int HistMaker::readGRL(){
  Int_t RunNumber1 = 0, MinLum1 = 0, MaxLum1 = 0;
  TString line1;
  ifstream fGRL;
  fGRL.open(m_GRLFileName);
  if(!fGRL.is_open()){
    cout<<"ERROR opening GRL"<<endl;
    abort();
  }
  while(fGRL >> line1){
    if(line1.Contains("</Run>")){
      line1.ReplaceAll("PrescaleRD1=\"8\">", "");
      line1.ReplaceAll("<Run>", "");
      line1.ReplaceAll("</Run>", "");
      RunNumber1 = line1.Atoi();
      while(1){
        fGRL>>line1;
        if( line1.Contains("</LumiBlockCollection>") ) break;
        fGRL>>line1;
        line1.ReplaceAll("Start=\"", "");
        line1.ReplaceAll("\"", "");
        MinLum1 = line1.Atoi();
        fGRL>>line1;
        line1.ReplaceAll("End=\"", "");
        line1.ReplaceAll("\"/>", "");
        MaxLum1 = line1.Atoi();
	pair<int,int> goodLBs;
	goodLBs.first = MinLum1;
	goodLBs.second = MaxLum1;
	vector<pair<int,int> > emptyVec;
	if( m_GRL.find(RunNumber1) == m_GRL.end()){
	  m_GRL[RunNumber1]=emptyVec;
	}
	m_GRL[RunNumber1].push_back(goodLBs);
      }
    }
  }
  return 0;
}

bool HistMaker::passGRL(int run, int lb){
  for ( auto& x : m_GRL){
    if ( run == x.first ){
      for ( auto&  p : x.second ){
	if ( lb >= p.first && lb <= p.second ){
	  return true;
	}
      }
    }
  }
  return false;
}
