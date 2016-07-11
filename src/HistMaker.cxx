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
     if (mcChannelNumber == 0){
       suffix="_"+to_string(runNumber);
     }
     else{
       suffix="_"+to_string(mcChannelNumber);
     }
   }
   Long64_t nentries = fChain->GetEntriesFast();
   TH1F *h_initEvents = new TH1F(("h_initEvents"+suffix).c_str(),"initial nEvents",1,0.5,1.5);
   h_initEvents->Fill(1,m_denom);
   
   TH1F *h_cutflow = new TH1F(("h_cutflow"+suffix).c_str(),"cutflow histogram",10,0.5,10.5);
   //For data: 2= every event looped over, 3= events that pass GRL
   //For MC: 1 = 2 = xsec*luminosity, 3= all events looped over
   h_cutflow->GetXaxis()->SetBinLabel(1,"CBC Selected");
   h_cutflow->GetXaxis()->SetBinLabel(2,"nEvents Looped over");
   h_cutflow->GetXaxis()->SetBinLabel(3,"GRL");
   h_cutflow->GetXaxis()->SetBinLabel(4,"event cleaning");
   h_cutflow->GetXaxis()->SetBinLabel(5,"trigger");
   h_cutflow->GetXaxis()->SetBinLabel(6,"p_T^{lead} > 440 GeV");
   h_cutflow->GetXaxis()->SetBinLabel(7,"n_{fatjet} #geq 5");
   h_cutflow->GetXaxis()->SetBinLabel(8,"b-tag");
   h_cutflow->GetXaxis()->SetBinLabel(9,"|#Delta #eta| < 1.4");
   h_cutflow->GetXaxis()->SetBinLabel(10,"MJ > 800 GeV");

   TH1F *h_CRyield = new TH1F(("h_CRyield"+suffix).c_str(),"CR yields",2,0.5,2.5);
   h_CRyield->GetXaxis()->SetBinLabel(1,"= 3 jet, b-veto");
   h_CRyield->GetXaxis()->SetBinLabel(2,"= 3 jet, b-tag, |#Delta #eta| > 1.4");


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


   TH1F* h_SRyield_unweighted = new TH1F(("h_SRyield_unweighted"+suffix).c_str(),"signal region yield",20,0.5,20.5);
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(1,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.6 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(2,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.65 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(3,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.7 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(4,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.75 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(5,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.8 TeV");

   h_SRyield_unweighted->GetXaxis()->SetBinLabel(6,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.6 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(7,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.65 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(8,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.7 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(9,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.75 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(10,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.8 TeV"); 

   h_SRyield_unweighted->GetXaxis()->SetBinLabel(11,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.6 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(12,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.65 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(13,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.7 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(14,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.75 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(15,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.8 TeV");

   h_SRyield_unweighted->GetXaxis()->SetBinLabel(16,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.6 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(17,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.65 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(18,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.7 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(19,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.75 TeV");
   h_SRyield_unweighted->GetXaxis()->SetBinLabel(20,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.8 TeV"); 

   TH1F *h_VRyield = new TH1F(("h_VRyield"+suffix).c_str(),"VR yields",20,0.5,20.5);
   h_VRyield->GetXaxis()->SetBinLabel(1,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.6 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(2,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.65 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(3,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.7 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(4,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.75 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(5,"n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.8 TeV");

   h_VRyield->GetXaxis()->SetBinLabel(6,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.6 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(7,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.65 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(8,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.7 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(9,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.75 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(10,"n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.8 TeV"); 

   h_VRyield->GetXaxis()->SetBinLabel(11,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.6 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(12,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.65 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(13,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.7 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(14,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.75 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(15,"n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.8 TeV");

   h_VRyield->GetXaxis()->SetBinLabel(16,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.6 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(17,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.65 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(18,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.7 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(19,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.75 TeV");
   h_VRyield->GetXaxis()->SetBinLabel(20,"n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.8 TeV"); 
   
   vector<TH1F*> h_MJ_4jSR_b1;
   vector<TH1F*> h_MJ_5jSR_b1;
   
   TH1F *h_MJ_4jSR = new TH1F(("h_MJ_4jSR"+suffix).c_str(),"MJ",150,0,1500);
   TH1F *h_MJ_5jSR = new TH1F(("h_MJ_5jSR"+suffix).c_str(),"MJ",150,0,1500);
   
   //MJ distributions for the two b-tag signal regions, for each b-tagging systematic variation
   for ( int i = 0; i < 51; i++){
     h_MJ_4jSR_b1.push_back(new TH1F(("h_MJ_4jSR_b1_"+to_string(i)+suffix).c_str(),"MJ",150,0,1500));
     h_MJ_5jSR_b1.push_back(new TH1F(("h_MJ_5jSR_b1_"+to_string(i)+suffix).c_str(),"MJ",150,0,1500));
   }

   //various dy histograms
   TH1F* h_dy_presel = new TH1F(("h_dy_presel"+suffix).c_str(),"#Delta #eta",100,0,5);
   TH1F* h_dy_n3_b0 = new TH1F(("h_dy_n3_b0"+suffix).c_str(),"#Delta #eta, n_{fatjet} == 3, b-veto",100,0,5);
   TH1F* h_dy_n3_b1 = new TH1F(("h_dy_n3_b1"+suffix).c_str(),"#Delta #eta, n_{fatjet} == 3, b-tag",100,0,5);
   TH1F* h_dy_m4_b1 = new TH1F(("h_dy_m4_b1"+suffix).c_str(),"#Delta #eta, n_{fatjet} #geq 4, b-tag",100,0,5);
   TH1F* h_dy_m4_b9 = new TH1F(("h_dy_m4_b9"+suffix).c_str(),"#Delta #eta, n_{fatjet} #geq 4, b-inc",100,0,5);
   TH1F* h_dy_m5_b1 = new TH1F(("h_dy_m5_b1"+suffix).c_str(),"#Delta #eta, n_{fatjet} #geq 5, b-tag",100,0,5);
   TH1F* h_dy_m5_b9 = new TH1F(("h_dy_m5_b9"+suffix).c_str(),"#Delta #eta, n_{fatjet} #geq 5, b-inc",100,0,5);

   //stuff for checking b-tagging efficiency
   TH1F* h_nTruB = new TH1F(("h_nTruB"+suffix).c_str(),"number of truth b-jets",5,-0.5,5.5);
   TH1F* h_bPt = new TH1F(("h_bPt"+suffix).c_str(),"pT of truth-tagged b-jets",200,0,2000);
   TH1F* h_bPt_tagged = new TH1F(("h_bPt_tagged"+suffix).c_str(),"pT of reco-tagged b-jets",200,0,2000);
   
   //various kinematic & substructure historams
   TH1F* h_nFatJet_presel = new TH1F(("h_nFatJet_presel"+suffix).c_str(),"n_{fat jet}",10,0.5,10.5);
   TH1F* h_MJ_presel = new TH1F(("h_MJ_presel"+suffix).c_str(),"MJ",150,0,1500);

   TH1F* h_fatjet_pt = new TH1F(("h_fatjet_pt"+suffix).c_str(),"fat jet pT [GeV]",30,0,2000);
   TH1F* h_fatjet_m = new TH1F(("h_fatjet_m"+suffix).c_str(),"fat jet mass [GeV]",30,0,250);
   TH1F* h_fatjet_eta = new TH1F(("h_fatjet_eta"+suffix).c_str(),"fat jet eta",50,-2.2,2.2);   
   TH1F* h_fatjet_phi = new TH1F(("h_fatjet_phi"+suffix).c_str(),"fat jet phi",50,-3.25,3.25);
   TH1F* h_fatjet_nTrimSubjets = new TH1F(("h_fatjet_nTrimSubjets"+suffix).c_str(),"fat jet nTrimSubjets",6,0.5,6.5);
   TH1F* h_fatjet_split12 = new TH1F(("h_fatjet_Split12"+suffix).c_str(),"fat jet Split12",30,0,120);
   TH1F* h_fatjet_split23 = new TH1F(("h_fatjet_Split23"+suffix).c_str(),"fat jet Split23",30,0,120);   
   TH1F* h_fatjet_split34 = new TH1F(("h_fatjet_Split34"+suffix).c_str(),"fat jet Split34",30,0,120);
   TH1F* h_fatjet_tau32_wta = new TH1F(("h_fatjet_tau32_wta"+suffix).c_str(),"fat jet tau32 wta",30,0,1.2);
   TH1F* h_fatjet_tau21_wta = new TH1F(("h_fatjet_tau21_wta"+suffix).c_str(),"fat jet tau21 wta",30,0,1.2);
   TH1F* h_fatjet_D2 = new TH1F(("h_fatjet_D2"+suffix).c_str(),"fat jet D2",30,0,8);
   TH1F* h_fatjet_C2 = new TH1F(("h_fatjet_C2"+suffix).c_str(),"fat jet C2",30,0,0.6);
   
   vector<TH1F*> h_fatjet_m_nTrim;
   vector<TH1F*> h_fatjet_split12_nTrim;
   vector<TH1F*> h_fatjet_split23_nTrim;
   vector<TH1F*> h_fatjet_split34_nTrim;
   vector<TH1F*> h_fatjet_tau32_nTrim;
   vector<TH1F*> h_fatjet_tau21_nTrim;
   vector<TH1F*> h_fatjet_D2_nTrim;
   vector<TH1F*> h_fatjet_C2_nTrim;

   for ( int i = 1; i <= 3; i++){
     h_fatjet_m_nTrim.push_back( new TH1F (("h_fatjet_m_nTrim_"+to_string(i)+suffix).c_str(),"fat jet mass",30,0,250));
     h_fatjet_split12_nTrim.push_back( new TH1F (("h_fatjet_split12_nTrim_"+to_string(i)+suffix).c_str(),"fat jet split12",30,0,120));
     h_fatjet_split23_nTrim.push_back( new TH1F (("h_fatjet_split23_nTrim_"+to_string(i)+suffix).c_str(),"fat jet split23",30,0,120));
     h_fatjet_split34_nTrim.push_back( new TH1F (("h_fatjet_split34_nTrim_"+to_string(i)+suffix).c_str(),"fat jet split34",30,0,120));
     h_fatjet_tau32_nTrim.push_back( new TH1F (("h_fatjet_tau32_nTrim_"+to_string(i)+suffix).c_str(),"fat jet tau32",30,0,1.2));
     h_fatjet_tau21_nTrim.push_back( new TH1F (("h_fatjet_tau21_nTrim_"+to_string(i)+suffix).c_str(),"fat jet tau21",30,0,1.2));
     h_fatjet_D2_nTrim.push_back( new TH1F (("h_fatjet_D2_nTrim_"+to_string(i)+suffix).c_str(),"fat jet D2",30,0,8));
     h_fatjet_C2_nTrim.push_back( new TH1F (("h_fatjet_C2_nTrim_"+to_string(i)+suffix).c_str(),"fat jet C2",30,0,0.6));
   }

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
      bool passLeadJet = false;
      int nFatJet = 0;
      vector<TLorentzVector> fj4mom;
      if (m_isMC){
	w = 1E6 * m_lumi * weight / m_denom;
	if(m_isCalibrated){ bw = w*weight_jet_SFFix70->at(0); }
	else{ bw = w; }
      }
      //GRL cut
      else{
	//for data, fill second bin for all events seen
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
      if(m_isCalibrated){
	for( auto s : *passedTriggers ){
	  if ( s.find("HLT_j360_a10")!=string::npos || s.find("HLT_j380_a10")!=string::npos || s.find("HLT_j400_a10")!=string::npos || s.find("HLT_j420_a10")!=string::npos ){
	    passTrig = true;
	  }
	}
      }
      else{
	passTrig = true;
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
      for( int i = 0; i < fatjet_pt->size(); i++){
	if(fatjet_pt->at(i) > m_fatJetPtCut && fabs(fatjet_eta->at(i)) < m_fatJetEtaCut && fatjet_m->at(i)/fatjet_pt->at(i) < m_fatJetMpTCut){
	  h_fatjet_pt->Fill(fatjet_pt->at(i),w);
	  h_fatjet_m->Fill(fatjet_m->at(i),w);
	  h_fatjet_eta->Fill(fatjet_eta->at(i),w);
	  h_fatjet_phi->Fill(fatjet_phi->at(i),w);
	  h_fatjet_nTrimSubjets->Fill(fatjet_NTrimSubjets->at(i),w);
	  h_fatjet_split12->Fill(fatjet_Split12->at(i),w);
	  h_fatjet_split23->Fill(fatjet_Split23->at(i),w);
	  h_fatjet_split34->Fill(fatjet_Split34->at(i),w);
	  h_fatjet_tau32_wta->Fill(fatjet_tau32_wta->at(i),w);
	  h_fatjet_tau21_wta->Fill(fatjet_tau21_wta->at(i),w);
	  h_fatjet_D2->Fill(fatjet_D2->at(i),w);
	  h_fatjet_C2->Fill(fatjet_C2->at(i),w);
	  int nTrimSubjets = fatjet_NTrimSubjets->at(i);
	  if (nTrimSubjets > 3){ nTrimSubjets = 3; }
	  h_fatjet_m_nTrim.at(nTrimSubjets-1)->Fill(fatjet_m->at(i),w);
	  h_fatjet_split12_nTrim.at(nTrimSubjets-1)->Fill(fatjet_Split12->at(i),w);
	  h_fatjet_split23_nTrim.at(nTrimSubjets-1)->Fill(fatjet_Split23->at(i),w);
	  h_fatjet_split34_nTrim.at(nTrimSubjets-1)->Fill(fatjet_Split34->at(i),w);
	  h_fatjet_tau32_nTrim.at(nTrimSubjets-1)->Fill(fatjet_tau32_wta->at(i),w);
	  h_fatjet_tau21_nTrim.at(nTrimSubjets-1)->Fill(fatjet_tau21_wta->at(i),w);
	  h_fatjet_D2_nTrim.at(nTrimSubjets-1)->Fill(fatjet_D2->at(i),w);
	  h_fatjet_C2_nTrim.at(nTrimSubjets-1)->Fill(fatjet_C2->at(i),w);
	}
      }
      //end of preselection
      if ( !passLeadJet ) { continue; }
      h_cutflow->Fill(++iCut,w);
      int nTruB = 0;
      //count the b-jets
      if(m_isCalibrated){
	for( int i = 0; i < jet_pt->size(); i++){
	  if ( jet_pt->at(i) > m_jetPtCut && fabs(jet_eta->at(i)) < m_jetEtaCut && jet_clean_passLooseBad->at(i) == 1){
	    //histograms of truth b-jets, to get b-tagging efficiency
	    if(abs(jet_PartonTruthLabelID->at(i)) == 5) { 
	      nTruB++;
	      h_bPt->Fill(jet_pt->at(i),w); 
	      if(jet_isFix70->at(i)){ h_bPt_tagged->Fill(jet_pt->at(i),bw); }
	    }
	    if (jet_isFix70->at(i) == 1){ 
	      nBTag ++; 
	    }
	  }
	}
      h_nTruB->Fill(nTruB,bw);
      }
      sort(fj4mom.begin(), fj4mom.end(), reorder);
      if ( fj4mom.size() >= 2 ) { dy = fabs(fj4mom.at(0).Eta() - fj4mom.at(1).Eta()); }
      int nJetLoop = 4;
      if (fj4mom.size() < 4){ nJetLoop = fj4mom.size(); }
      for( int i = 0; i < nJetLoop; i++){ mj += fj4mom.at(i).M(); }

      if(nFatJet >= 5){ 
	h_cutflow->Fill(++iCut,w); 
	if(nBTag >= 1){
	  h_cutflow->Fill(++iCut,bw);
	  if(dy < 1.4){
	    h_cutflow->Fill(++iCut,bw);
	    if(mj > 800){
	      h_cutflow->Fill(++iCut,bw);
	    }
	  }
	}
      }
      //fill CR yieds (2 CRs)
      if(nFatJet==3){
	if( nBTag == 0 ){
	  //b-veto CR
	  h_CRyield->Fill(1,bw);
	}
	else if( dy > 1.4 ){
	  //b-tag CR
	  h_CRyield->Fill(2,bw);
	}
      }
      //Fill SR yields
      int sr=0;
      if (nFatJet >= 4){
        if (nBTag >= 1){
      	  if (mj > 600){
      	    if (dy < 1.4){ 
	      h_SRyield->Fill(sr+1,bw); 
	      h_SRyield_unweighted->Fill(sr+1);
	    }

	    else{ h_VRyield->Fill(sr+1,bw); }
      	  }
      	  if (mj > 650){
	    if (dy < 1.4) { 
	      h_SRyield->Fill(sr+2,bw); 
	      h_SRyield_unweighted->Fill(sr+2);
	    }
	    else{ h_VRyield->Fill(sr+2,bw); }
      	  }
      	  if (mj > 700){
      	    if (dy < 1.4){ 
	      h_SRyield->Fill(sr+3,bw); 
	      h_SRyield_unweighted->Fill(sr+3);
	    }
	    else{ h_VRyield->Fill(sr+3,bw); }
      	  }
      	  if (mj > 750){
	    if (dy < 1.4) { 
	      h_SRyield->Fill(sr+4,bw); 
	      h_SRyield_unweighted->Fill(sr+4);
	    }
	    else{ h_VRyield->Fill(sr+4,bw); }
      	  }
      	  if (mj > 800){
      	    if (dy < 1.4) { 
	      h_SRyield->Fill(sr+5,bw); 
	      h_SRyield_unweighted->Fill(sr+5);
	    }
	    else{ h_VRyield->Fill(sr+5,bw); }
      	  }
      	}
      	//b-inclusive SRs
      	if (mj > 600){
      	  if (dy < 1.4){ 
	    h_SRyield->Fill(sr+6,w); 
	    h_SRyield_unweighted->Fill(sr+6);
	  }
	  else{ h_VRyield->Fill(sr+6,w); }
      	}
      	if (mj > 650){
      	  if (dy < 1.4) { 
	    h_SRyield->Fill(sr+7,w);
	    h_SRyield_unweighted->Fill(sr+7);
	  }
	  else{ h_VRyield->Fill(sr+7,w); }
      	}
      	if (mj > 700){
      	  if (dy < 1.4){ 
	    h_SRyield->Fill(sr+8,w); 
	    h_SRyield_unweighted->Fill(sr+8);
	  }
	  else{ h_VRyield->Fill(sr+8,w); }
      	}
      	if (mj > 750){
      	  if (dy < 1.4) { 
	    h_SRyield->Fill(sr+9,w); 
	    h_SRyield_unweighted->Fill(sr+9);
	  }
	  else{ h_VRyield->Fill(sr+9,w); }
      	}
      	if (mj > 800){
      	  if (dy < 1.4) { 
	    h_SRyield->Fill(sr+10,w); 
	    h_SRyield_unweighted->Fill(sr+10);
	  }
	  else{ h_VRyield->Fill(sr+10,w); }
      	}
      }
      sr=10;
      if (nFatJet >= 5){
        if (nBTag >= 1){
      	  if (mj > 600){
      	    if (dy < 1.4){ 
	      h_SRyield->Fill(sr+1,bw); 
	      h_SRyield_unweighted->Fill(sr+1);
	    }
	    else{ h_VRyield->Fill(sr+1,bw); }
      	  }
      	  if (mj > 650){
      	    if (dy < 1.4) { 
	      h_SRyield->Fill(sr+2,bw); 
	      h_SRyield_unweighted->Fill(sr+2);
	    }
	    else{ h_VRyield->Fill(sr+2,bw); }
      	  }
      	  if (mj > 700){
      	    if (dy < 1.4){ 
	      h_SRyield->Fill(sr+3,bw); 
	      h_SRyield_unweighted->Fill(sr+3);
	    }
	    else{ h_VRyield->Fill(sr+3,bw); }
      	  }
      	  if (mj > 750){
      	    if (dy < 1.4) { 
	      h_SRyield->Fill(sr+4,bw); 
	      h_SRyield_unweighted->Fill(sr+4);
	    }
	    else{ h_VRyield->Fill(sr+4,bw); }
      	  }
      	  if (mj > 800){
      	    if (dy < 1.4) { 
	      h_SRyield->Fill(sr+5,bw); 
	      h_SRyield_unweighted->Fill(sr+5);
	    }
	    else{ h_VRyield->Fill(sr+5,bw); }
      	  }
      	}
      	//b-inclusive SRs
      	if (mj > 600){
      	  if (dy < 1.4){ 
	    h_SRyield->Fill(sr+6,w); 
	    h_SRyield_unweighted->Fill(sr+6);
	  }
	  else{ h_VRyield->Fill(sr+6,w); }
      	}
      	if (mj > 650){
      	  if (dy < 1.4) { 
	    h_SRyield->Fill(sr+7,w); 
	    h_SRyield_unweighted->Fill(sr+7);
	  }
	  else{ h_VRyield->Fill(sr+7,w); }
      	}
      	if (mj > 700){
      	  if (dy < 1.4){ 
	    h_SRyield->Fill(sr+8,w); 
	    h_SRyield_unweighted->Fill(sr+8);
	  }
	  else{ h_VRyield->Fill(sr+8,w); }
      	}
      	if (mj > 750){
      	  if (dy < 1.4) { 
	    h_SRyield->Fill(sr+9,w); 
	    h_SRyield_unweighted->Fill(sr+9);
	  }
	  else{ h_VRyield->Fill(sr+9,w); }
      	}
      	if (mj > 800){
      	  if (dy < 1.4) { 
	    h_SRyield->Fill(sr+10,w); 
	    h_SRyield_unweighted->Fill(sr+10);
	  }
	  else{ h_VRyield->Fill(sr+10,w); }
      	}
      }
      if(dy < 1.4){
	if(nFatJet >= 4){ h_MJ_4jSR->Fill(mj,w); }
	if(nFatJet >= 5){ h_MJ_5jSR->Fill(mj,w); }
      }
      for(int i = 0; i < 51; i++){
	if ( dy < 1.4 && nBTag >= 1){
	  if(nFatJet >=4){ h_MJ_4jSR_b1.at(i)->Fill(mj,w*weight_jet_SFFix70->at(i)); }
	  if(nFatJet >=5){ h_MJ_5jSR_b1.at(i)->Fill(mj,w*weight_jet_SFFix70->at(i)); }
	}
      }
      h_nFatJet_presel->Fill(nFatJet,w);
      h_dy_presel->Fill(dy,w);
      h_MJ_presel->Fill(mj,w);
      if( nFatJet == 3 ){
	if(nBTag == 0){ h_dy_n3_b0->Fill(dy,bw); }
	else{ h_dy_n3_b1->Fill(dy,bw); }
      }
      if( nFatJet >= 4){
	h_dy_m4_b9->Fill(dy,w);
	if(nBTag >=1){ h_dy_m4_b1->Fill(dy,bw); }
      }
      if( nFatJet >= 5){
	h_dy_m5_b9->Fill(dy,w);
	if(nBTag >=1){ h_dy_m5_b1->Fill(dy,bw); }
      }
   }
   m_outFile->cd();
   m_outFile->Write();
   cout<<"File written: "<<m_outFileName<<endl;
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
