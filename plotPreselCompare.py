#!/usr/bin/env python
import argparse,ROOT,os,glob,sys,subprocess,math
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

lumiLatex=ROOT.TLatex()

#for use in tlatex
srNames = ['4jSRb1','4jSR','5jSRb1','5jSR']
mjCutNames=['MJ > 600 GeV','MJ > 650 GeV','MJ > 700 GeV','MJ > 750 GeV','MJ > 800 GeV']
#for use in file names
srLabs = ['m4_b1','m4_b9','m5_b1','m5_b9']
mjCutLabs = ['MJ_600_13000','MJ_650_13000','MJ_700_13000','MJ_750_13000','MJ_800_13000']

def drawHists(upHist,downHist,i,j,k):
    ROOT.gStyle.SetPaintTextFormat('1.2f')
    upHist.Draw('TEXT')
    upHist.GetXaxis().SetTickLength(0)
    upHist.GetXaxis().SetTitle('m_{#tilde{g}} [TeV]')
    upHist.GetYaxis().SetTitle('m_{#tilde{#chi}} [GeV]')
    upHist.GetYaxis().SetTickLength(0)
    upHist.GetYaxis().SetLabelOffset(99)
    upHist.GetXaxis().SetLabelOffset(99)
    upHist.SetMarkerSize(1.5)
    t=ROOT.TText()
    t.SetTextAngle(0)
    t.SetTextSize(0.05)
    t.SetTextAlign(33)

    gridLine = ROOT.TLine()
    gridLine.SetLineStyle(2)
    gridLine.SetLineColor(ROOT.kGray)
    #vertical lines
    for xi in range(650,1950,100):
        if xi > 650:
            gridLine.DrawLine(xi,-50,xi,1750)
    for yi in range(-50,1850,200):
        if  yi > -50 and yi < 1600:
            gridLine.DrawLine(650,yi,1950,yi)
    for xLab in range(700,2000,100):
        t.DrawText(xLab+50,-65,str(xLab/1000.))
    for yLab in range(50,1700,200):
        t.DrawText(635,(yLab+50),str(yLab))
    if downHist:
        downHist.SetMarkerSize(1.5)
        downHist.Draw('TEXT SAME')
    ROOT.ATLASLabel(0.2,0.88,'Simulation Internal')
    lat = ROOT.TLatex()
    lat.DrawLatexNDC(0.2,0.8,'A^{reco}_{new}/A^{reco}_{old}')
    lat.DrawLatexNDC(0.2,0.72,'#bf{'+srNames[i]+'}')
    lat.DrawLatexNDC(0.2,0.65,mjCutNames[j])

parser = argparse.ArgumentParser(add_help=False, description='Plot Systs')
parser.add_argument('input_new')
parser.add_argument('input_old')
args = parser.parse_args()
filePathNew = args.input_new.strip('/')
filePathOld = args.input_old.strip('/')
nomFileNew = ROOT.TFile.Open(filePathNew+'/nominal.root')
dsidList = []

for key in nomFileNew.GetListOfKeys():
    if 'h_cutflow_' in key.GetName():
        if int(key.GetName().split('_')[2]) not in dsidList:
            dsidList.append( int(key.GetName().split('_')[2] ) )
dsidList.sort()
print dsidList
srBin=1
canMCStats=[]
for i in range(len(srNames)):
    for j in range(len(mjCutNames)):
        if i==i and j==j:
            nomFileNew=ROOT.TFile.Open(filePathNew+'/nominal.root')
            nomFileOld=ROOT.TFile.Open(filePathOld+'/nominal.root')
            mcStatsHist=ROOT.TH2D('h_MCStats_'+srLabs[i]+'_'+mjCutLabs[j],'MC stats',13,650,1950,9,-50,1750)
            canMCStats.append(ROOT.TCanvas('cMC_'+str(len(canMCStats)),'cMC_'+str(len(canMCStats)),800,600))
            for m in range(len(dsidList)):
                hSRyieldNew=nomFileNew.Get('h_SRyield_'+str(dsidList[m]))
                hSRyieldOld=nomFileOld.Get('h_SRyield_'+str(dsidList[m]))
                mG = pointDict[int(dsidList[m])][0]
                mX = pointDict[int(dsidList[m])][1]
                ratio = hSRyieldNew[srBin]/hSRyieldOld[srBin]
                mcStatsHist.Fill(mG,mX,ratio)
            canMCStats[-1].cd()
            drawHists(mcStatsHist,0,i,j,-2)
            outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/PreselectionComparison/07_15/'
            outFileName+='preselCompare_RPV10_'+srLabs[i]+'_'+mjCutLabs[j]
            canMCStats[-1].Print(outFileName+'.pdf')
            canMCStats[-1].Print(outFileName+'.png')
            canMCStats[-1].Print(outFileName+'.C')
        srBin+=1
subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/PreselectionComparison/07_15/*',shell=True)
