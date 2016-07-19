//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Jul  6 13:55:05 2016 by ROOT version 6.04/14
// from TTree nominal/nominal
// found on file: ../../MAF/submit/Truth/404250/data-tree/RPV_truthGrid100_TRUTH3.root
//////////////////////////////////////////////////////////

#ifndef TruthHistMaker_h
#define TruthHistMaker_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TLorentzVector.h>
#include "string"
// Header file for the classes stored in the TTree if any.
#include "vector"
#include "vector"
using namespace std;
class TruthHistMaker {
 private:

  static bool reorder(const TLorentzVector &, const TLorentzVector &);
  
  string m_outFileName = "";
  float m_weight = 1.0;
  float m_lumi = 5.8;
  float m_initEvents = 100000.0;
  TFile *m_outFile;
  bool m_isMC = false;
  float m_xsec = 1.0;
  float m_jetPtCut = 50.0;
  float m_fatJetPtCut = 200.0;
  float m_jetEtaCut = 2.5;
  float m_fatJetEtaCut = 2.0;
  float m_leadJetPtCut = 440.0;
  float m_fatJetMpTCut = 1.0;  
  vector<float> m_avgPDFweight;
 public :
  void SetupOutput();                                                                                                      
  void SetLumi(float lumi){ 
    m_lumi = lumi; 
    m_weight = m_xsec*m_lumi*1E6/m_initEvents;
  }
  void SetInitEvents(float initEvents){
    m_initEvents = initEvents;
    m_weight = m_xsec*m_lumi*1E6/m_initEvents;
  }
  
  TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t           runNumber;
   Long64_t        eventNumber;
   Int_t           lumiBlock;
   UInt_t          coreFlags;
   Int_t           mcEventNumber;
   Int_t           mcChannelNumber;
   Float_t         mcEventWeight;
   Float_t         weight_xs;
   vector<float>   *weight_pdf;
   Float_t         weight;
   Int_t           njets;
   vector<float>   *jet_E;
   vector<float>   *jet_m;
   vector<float>   *jet_pt;
   vector<float>   *jet_phi;
   vector<float>   *jet_eta;
   vector<int>     *jet_GhostBHadronsFinalCount;
   vector<int>     *jet_GhostBHadronsInitialCount;
   vector<int>     *jet_GhostBQuarksFinalCount;
   vector<float>   *jet_GhostBHadronsFinalPt;
   vector<float>   *jet_GhostBHadronsInitialPt;
   vector<float>   *jet_GhostBQuarksFinalPt;
   vector<int>     *jet_GhostCHadronsFinalCount;
   vector<int>     *jet_GhostCHadronsInitialCount;
   vector<int>     *jet_GhostCQuarksFinalCount;
   vector<float>   *jet_GhostCHadronsFinalPt;
   vector<float>   *jet_GhostCHadronsInitialPt;
   vector<float>   *jet_GhostCQuarksFinalPt;
   vector<int>     *jet_GhostTausFinalCount;
   vector<float>   *jet_GhostTausFinalPt;
   vector<int>     *jet_truth_pdgId;
   vector<float>   *jet_truth_partonPt;
   vector<float>   *jet_truth_partonDR;
   Int_t           nfatjets;
   vector<float>   *fatjet_E;
   vector<float>   *fatjet_m;
   vector<float>   *fatjet_pt;
   vector<float>   *fatjet_phi;
   vector<float>   *fatjet_eta;
   vector<float>   *fatjet_Split12;
   vector<float>   *fatjet_Split23;
   vector<float>   *fatjet_Split34;
   vector<float>   *fatjet_tau1_wta;
   vector<float>   *fatjet_tau2_wta;
   vector<float>   *fatjet_tau3_wta;
   vector<float>   *fatjet_tau21_wta;
   vector<float>   *fatjet_tau32_wta;
   vector<float>   *fatjet_ECF1;
   vector<float>   *fatjet_ECF2;
   vector<float>   *fatjet_ECF3;
   vector<float>   *fatjet_C2;
   vector<float>   *fatjet_D2;
   vector<float>   *fatjet_NTrimSubjets;

   // List of branches
   TBranch        *b_runNumber;   //!
   TBranch        *b_eventNumber;   //!
   TBranch        *b_lumiBlock;   //!
   TBranch        *b_coreFlags;   //!
   TBranch        *b_mcEventNumber;   //!
   TBranch        *b_mcChannelNumber;   //!
   TBranch        *b_mcEventWeight;   //!
   TBranch        *b_weight_xs;   //!
   TBranch        *b_weight_pdf; //!
   TBranch        *b_weight;   //!
   TBranch        *b_njets;   //!
   TBranch        *b_jet_E;   //!
   TBranch        *b_jet_m;   //!
   TBranch        *b_jet_pt;   //!
   TBranch        *b_jet_phi;   //!
   TBranch        *b_jet_eta;   //!
   TBranch        *b_jet_GhostBHadronsFinalCount;   //!
   TBranch        *b_jet_GhostBHadronsInitialCount;   //!
   TBranch        *b_jet_GhostBQuarksFinalCount;   //!
   TBranch        *b_jet_GhostBHadronsFinalPt;   //!
   TBranch        *b_jet_GhostBHadronsInitialPt;   //!
   TBranch        *b_jet_GhostBQuarksFinalPt;   //!
   TBranch        *b_jet_GhostCHadronsFinalCount;   //!
   TBranch        *b_jet_GhostCHadronsInitialCount;   //!
   TBranch        *b_jet_GhostCQuarksFinalCount;   //!
   TBranch        *b_jet_GhostCHadronsFinalPt;   //!
   TBranch        *b_jet_GhostCHadronsInitialPt;   //!
   TBranch        *b_jet_GhostCQuarksFinalPt;   //!
   TBranch        *b_jet_GhostTausFinalCount;   //!
   TBranch        *b_jet_GhostTausFinalPt;   //!
   TBranch        *b_jet_truth_pdgId;   //!
   TBranch        *b_jet_truth_partonPt;   //!
   TBranch        *b_jet_truth_partonDR;   //!
   TBranch        *b_nfatjets;   //!
   TBranch        *b_fatjet_E;   //!
   TBranch        *b_fatjet_m;   //!
   TBranch        *b_fatjet_pt;   //!
   TBranch        *b_fatjet_phi;   //!
   TBranch        *b_fatjet_eta;   //!
   TBranch        *b_fatjet_Split12;   //!
   TBranch        *b_fatjet_Split23;   //!
   TBranch        *b_fatjet_Split34;   //!
   TBranch        *b_fatjet_tau1_wta;   //!
   TBranch        *b_fatjet_tau2_wta;   //!
   TBranch        *b_fatjet_tau3_wta;   //!
   TBranch        *b_fatjet_tau21_wta;   //!
   TBranch        *b_fatjet_tau32_wta;   //!
   TBranch        *b_fatjet_ECF1;   //!
   TBranch        *b_fatjet_ECF2;   //!
   TBranch        *b_fatjet_ECF3;   //!
   TBranch        *b_fatjet_C2;   //!
   TBranch        *b_fatjet_D2;   //!
   TBranch        *b_fatjet_NTrimSubjets;   //!

   TruthHistMaker(TTree *tree=0,string outFileName="",float xsec=0,float lumi=5.8);
   virtual ~TruthHistMaker();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef TruthHistMaker_cxx
TruthHistMaker::TruthHistMaker(TTree *tree,string outFileName,float xsec,float lumi) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("../../MAF/submit/Truth/404250/data-tree/RPV_truthGrid100_TRUTH3.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("../../MAF/submit/Truth/404250/data-tree/RPV_truthGrid100_TRUTH3.root");
      }
      TDirectory * dir = (TDirectory*)f->Get("../../MAF/submit/Truth/404250/data-tree/RPV_truthGrid100_TRUTH3.root:/outTree");
      dir->GetObject("nominal",tree);
      
   }
   Init(tree);
   m_outFileName=outFileName;
   m_weight = xsec*lumi*1E6/m_initEvents;
   m_xsec=xsec;
}

TruthHistMaker::~TruthHistMaker()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t TruthHistMaker::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t TruthHistMaker::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void TruthHistMaker::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
  weight_pdf = 0;
  jet_E = 0;
   jet_m = 0;
   jet_pt = 0;
   jet_phi = 0;
   jet_eta = 0;
   jet_GhostBHadronsFinalCount = 0;
   jet_GhostBHadronsInitialCount = 0;
   jet_GhostBQuarksFinalCount = 0;
   jet_GhostBHadronsFinalPt = 0;
   jet_GhostBHadronsInitialPt = 0;
   jet_GhostBQuarksFinalPt = 0;
   jet_GhostCHadronsFinalCount = 0;
   jet_GhostCHadronsInitialCount = 0;
   jet_GhostCQuarksFinalCount = 0;
   jet_GhostCHadronsFinalPt = 0;
   jet_GhostCHadronsInitialPt = 0;
   jet_GhostCQuarksFinalPt = 0;
   jet_GhostTausFinalCount = 0;
   jet_GhostTausFinalPt = 0;
   jet_truth_pdgId = 0;
   jet_truth_partonPt = 0;
   jet_truth_partonDR = 0;
   fatjet_E = 0;
   fatjet_m = 0;
   fatjet_pt = 0;
   fatjet_phi = 0;
   fatjet_eta = 0;
   fatjet_Split12 = 0;
   fatjet_Split23 = 0;
   fatjet_Split34 = 0;
   fatjet_tau1_wta = 0;
   fatjet_tau2_wta = 0;
   fatjet_tau3_wta = 0;
   fatjet_tau21_wta = 0;
   fatjet_tau32_wta = 0;
   fatjet_ECF1 = 0;
   fatjet_ECF2 = 0;
   fatjet_ECF3 = 0;
   fatjet_C2 = 0;
   fatjet_D2 = 0;
   fatjet_NTrimSubjets = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("runNumber", &runNumber, &b_runNumber);
   fChain->SetBranchAddress("eventNumber", &eventNumber, &b_eventNumber);
   fChain->SetBranchAddress("lumiBlock", &lumiBlock, &b_lumiBlock);
   fChain->SetBranchAddress("coreFlags", &coreFlags, &b_coreFlags);
   fChain->SetBranchAddress("mcEventNumber", &mcEventNumber, &b_mcEventNumber);
   fChain->SetBranchAddress("mcChannelNumber", &mcChannelNumber, &b_mcChannelNumber);
   fChain->SetBranchAddress("mcEventWeight", &mcEventWeight, &b_mcEventWeight);
   fChain->SetBranchAddress("weight_xs", &weight_xs, &b_weight_xs);
   fChain->SetBranchAddress("weight_pdf", &weight_pdf, &b_weight_pdf);   
   fChain->SetBranchAddress("weight", &weight, &b_weight);
   fChain->SetBranchAddress("njets", &njets, &b_njets);
   fChain->SetBranchAddress("jet_E", &jet_E, &b_jet_E);
   fChain->SetBranchAddress("jet_m", &jet_m, &b_jet_m);
   fChain->SetBranchAddress("jet_pt", &jet_pt, &b_jet_pt);
   fChain->SetBranchAddress("jet_phi", &jet_phi, &b_jet_phi);
   fChain->SetBranchAddress("jet_eta", &jet_eta, &b_jet_eta);
   fChain->SetBranchAddress("jet_GhostBHadronsFinalCount", &jet_GhostBHadronsFinalCount, &b_jet_GhostBHadronsFinalCount);
   fChain->SetBranchAddress("jet_GhostBHadronsInitialCount", &jet_GhostBHadronsInitialCount, &b_jet_GhostBHadronsInitialCount);
   fChain->SetBranchAddress("jet_GhostBQuarksFinalCount", &jet_GhostBQuarksFinalCount, &b_jet_GhostBQuarksFinalCount);
   fChain->SetBranchAddress("jet_GhostBHadronsFinalPt", &jet_GhostBHadronsFinalPt, &b_jet_GhostBHadronsFinalPt);
   fChain->SetBranchAddress("jet_GhostBHadronsInitialPt", &jet_GhostBHadronsInitialPt, &b_jet_GhostBHadronsInitialPt);
   fChain->SetBranchAddress("jet_GhostBQuarksFinalPt", &jet_GhostBQuarksFinalPt, &b_jet_GhostBQuarksFinalPt);
   fChain->SetBranchAddress("jet_GhostCHadronsFinalCount", &jet_GhostCHadronsFinalCount, &b_jet_GhostCHadronsFinalCount);
   fChain->SetBranchAddress("jet_GhostCHadronsInitialCount", &jet_GhostCHadronsInitialCount, &b_jet_GhostCHadronsInitialCount);
   fChain->SetBranchAddress("jet_GhostCQuarksFinalCount", &jet_GhostCQuarksFinalCount, &b_jet_GhostCQuarksFinalCount);
   fChain->SetBranchAddress("jet_GhostCHadronsFinalPt", &jet_GhostCHadronsFinalPt, &b_jet_GhostCHadronsFinalPt);
   fChain->SetBranchAddress("jet_GhostCHadronsInitialPt", &jet_GhostCHadronsInitialPt, &b_jet_GhostCHadronsInitialPt);
   fChain->SetBranchAddress("jet_GhostCQuarksFinalPt", &jet_GhostCQuarksFinalPt, &b_jet_GhostCQuarksFinalPt);
   fChain->SetBranchAddress("jet_GhostTausFinalCount", &jet_GhostTausFinalCount, &b_jet_GhostTausFinalCount);
   fChain->SetBranchAddress("jet_GhostTausFinalPt", &jet_GhostTausFinalPt, &b_jet_GhostTausFinalPt);
   fChain->SetBranchAddress("jet_truth_pdgId", &jet_truth_pdgId, &b_jet_truth_pdgId);
   fChain->SetBranchAddress("jet_truth_partonPt", &jet_truth_partonPt, &b_jet_truth_partonPt);
   fChain->SetBranchAddress("jet_truth_partonDR", &jet_truth_partonDR, &b_jet_truth_partonDR);
   fChain->SetBranchAddress("nfatjets", &nfatjets, &b_nfatjets);
   fChain->SetBranchAddress("fatjet_E", &fatjet_E, &b_fatjet_E);
   fChain->SetBranchAddress("fatjet_m", &fatjet_m, &b_fatjet_m);
   fChain->SetBranchAddress("fatjet_pt", &fatjet_pt, &b_fatjet_pt);
   fChain->SetBranchAddress("fatjet_phi", &fatjet_phi, &b_fatjet_phi);
   fChain->SetBranchAddress("fatjet_eta", &fatjet_eta, &b_fatjet_eta);
   fChain->SetBranchAddress("fatjet_Split12", &fatjet_Split12, &b_fatjet_Split12);
   fChain->SetBranchAddress("fatjet_Split23", &fatjet_Split23, &b_fatjet_Split23);
   fChain->SetBranchAddress("fatjet_Split34", &fatjet_Split34, &b_fatjet_Split34);
   fChain->SetBranchAddress("fatjet_tau1_wta", &fatjet_tau1_wta, &b_fatjet_tau1_wta);
   fChain->SetBranchAddress("fatjet_tau2_wta", &fatjet_tau2_wta, &b_fatjet_tau2_wta);
   fChain->SetBranchAddress("fatjet_tau3_wta", &fatjet_tau3_wta, &b_fatjet_tau3_wta);
   fChain->SetBranchAddress("fatjet_tau21_wta", &fatjet_tau21_wta, &b_fatjet_tau21_wta);
   fChain->SetBranchAddress("fatjet_tau32_wta", &fatjet_tau32_wta, &b_fatjet_tau32_wta);
   fChain->SetBranchAddress("fatjet_ECF1", &fatjet_ECF1, &b_fatjet_ECF1);
   fChain->SetBranchAddress("fatjet_ECF2", &fatjet_ECF2, &b_fatjet_ECF2);
   fChain->SetBranchAddress("fatjet_ECF3", &fatjet_ECF3, &b_fatjet_ECF3);
   fChain->SetBranchAddress("fatjet_C2", &fatjet_C2, &b_fatjet_C2);
   fChain->SetBranchAddress("fatjet_D2", &fatjet_D2, &b_fatjet_D2);
   fChain->SetBranchAddress("fatjet_NTrimSubjets", &fatjet_NTrimSubjets, &b_fatjet_NTrimSubjets);
   Notify();
}

Bool_t TruthHistMaker::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void TruthHistMaker::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t TruthHistMaker::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef TruthHistMaker_cxx
