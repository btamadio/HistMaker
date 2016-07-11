#!/usr/bin/env python
import ROOT,sys
from pointDict import pointDict
from pprint import pprint
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
f = ROOT.TFile.Open(sys.argv[1])
histName10 = 'h_MJ_m5_bUncert'
histName6 = 'h_MJ_m4_b1_dy14'
runList = []

bUncertUp = [ROOT.TH2F('h_up'+str(i),'h_up'+str(i),57,587.5,2012.5,9,-50,1750) for i in range(0,25)]
bUncertDown = [ROOT.TH2F('h_down'+str(i),'h_down'+str(i),57,587.5,2012.5,9,-50,1750) for i in range(0,25)]

totUp = ROOT.TH2F('h_up','h_up',57,587.5,2012.5,9,-50,1750)
totDown = ROOT.TH2F('h_down','h_down',57,587.5,2012.5,9,-50,1750)

for key in f.GetListOfKeys():
    if 'h_cutflow_' in key.GetName():
        runList.append(key.GetName().split('_')[2])
for run in sorted(runList):
    mG = pointDict[int(run)][0]
    mX = pointDict[int(run)][1]
    for i in range(1,50,2):
        hUp = f.Get(histName10+str(i)+'__'+run)
        hDown = f.Get(histName10+str(i+1)+'__'+run)
        hNom = f.Get(histName10+'0__'+run)
        binLow = hUp.FindBin(750)
        binUp = hUp.GetNbinsX()
        bUncertUp[(i-1)/2].Fill(mG,mX,hUp.Integral(binLow,binUp)/hNom.Integral(binLow,binUp)-1)
        bUncertDown[(i-1)/2].Fill(mG,mX,hDown.Integral(binLow,binUp)/hNom.Integral(binLow,binUp)-1)
