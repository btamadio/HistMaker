#!/usr/bin/env python
import argparse,ROOT,os,glob,sys,subprocess,math
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

ROOT.gROOT.SetBatch(True)

def drawHists(upHist,downHist,i,j,k=-1):
    ROOT.gStyle.SetPaintTextFormat('+1.1f')
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
        gridLine.DrawLine(xi,-200,xi,1800)
    for yi in range(-50,1850,200):
        gridLine.DrawLine(550,yi,1950,yi)
    for xLab in range(700,2000,100):
        t.DrawText(xLab+50,-215,str(xLab/1000.))
    for yLab in range(50,1700,200):
        t.DrawText(535,(yLab+50),str(yLab))
        
    downHist.SetMarkerSize(1.5)
    downHist.Draw('TEXT SAME')

    ROOT.ATLASLabel(0.2,0.88,'Simulation Internal')
    lat = ROOT.TLatex()

    lat.DrawLatexNDC(0.2,0.8,'B-tagging Uncertainty (%)')
    lat.DrawLatexNDC(0.2,0.72,srNames[i])
    lat.DrawLatexNDC(0.2,0.65,mjCutNames[j])

parser = argparse.ArgumentParser(add_help=False, description='Plot Systs')
parser.add_argument('input')
args = parser.parse_args()
filePath = args.input.strip('/')
nomFile = ROOT.TFile.Open(filePath+'/nominal.root')

dsidList=[]
for key in nomFile.GetListOfKeys():
    if 'h_cutflow_' in key.GetName():
        if int(key.GetName().split('_')[2]) not in dsidList:
            dsidList.append( int(key.GetName().split('_')[2] ) )
dsidList.sort()

lumiLatex=ROOT.TLatex()
lumiString = '#int L dt = 14.8 fb^{-1}'

#for use in tlatex
srNames = ['4jSRb1','5jSRb1']
mjCutNames=['MJ > 600 GeV','MJ > 650 GeV','MJ > 700 GeV','MJ > 750 GeV','MJ > 800 GeV']
#for use in file names
srLabs = ['m4_b1','m5_b1']
mjCutLabs = ['MJ_600_13000','MJ_650_13000','MJ_700_13000','MJ_750_13000','MJ_800_13000']

srBin = 1
can = []

bTagUpList=[]
bTagDownList=[]

for i in range(len(srNames)):
    for j in range(len(mjCutNames)):
        if i==i and j==j:
            nomFile=ROOT.TFile.Open(filePath+'/nominal.root')
            bTagUpList.append(ROOT.TH2D('hTotUp_'+srLabs[i]+'_'+mjCutLabs[j],'systematics',14,550,1950,10,-200,1800))
            bTagDownList.append(ROOT.TH2D('hTotDown_'+srLabs[i]+'_'+mjCutLabs[j],'systematics',14,550,1950,10,-300,1700))
            bTagUpList[-1].SetDirectory(0)
            bTagDownList[-1].SetDirectory(0)
            can.append(ROOT.TCanvas('c_'+str(len(can)),'c_'+str(len(can)),800,600))
            can[-1].cd()

            for m in range(len(dsidList)):
                for k in range(25):
                    mG = pointDict[int(dsidList[m])][0]
                    mX = pointDict[int(dsidList[m])][1]
                    nomHist=nomFile.Get('h_MJ_'+str(i+4)+'jSR_b1_0_'+str(dsidList[m]))
                    upHist = nomFile.Get('h_MJ_'+str(i+4)+'jSR_b1_'+str(2*k+2)+'_'+str(dsidList[m]))
                    downHist = nomFile.Get('h_MJ_'+str(i+4)+'jSR_b1_'+str(2*k+1)+'_'+str(dsidList[m]))
                    mjCutList=[600,650,700,750,800]
                    endInt = upHist.GetNbinsX()
                    upInt = upHist.Integral(upHist.FindBin(mjCutList[j]),endInt)
                    nomInt = nomHist.Integral(nomHist.FindBin(mjCutList[j]),endInt)
                    downInt = downHist.Integral(downHist.FindBin(mjCutList[j]),endInt)
                    upPercent=1E-8
                    downPercent=1E-8
                    if nomInt!=0:
                        upPercent = upInt/nomInt-1
                        downPercent = downInt/nomInt-1
                    bTagUpList[-1].Fill(mG,mX,upPercent*upPercent)
                    bTagDownList[-1].Fill(mG,mX,downPercent*downPercent)

            for xBin in range(1,bTagUpList[-1].GetNbinsX()+1):
                for yBin in range(1,bTagUpList[-1].GetNbinsY()+1):
                    binCup = bTagUpList[-1].GetBinContent(xBin,yBin)
                    binCup = math.sqrt(binCup)
                    binCdown = bTagDownList[-1].GetBinContent(xBin,yBin)
                    binCdown = math.sqrt(binCdown)
                    bTagUpList[-1].SetBinContent(xBin,yBin,100*binCup)
                    bTagDownList[-1].SetBinContent(xBin,yBin,-100*binCdown)
            drawHists(bTagUpList[-1],bTagDownList[-1],i,j,k)
            outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_27/RPV10/'
            outFileName+='uncert_RPV10_'+srLabs[i]+'_'+mjCutLabs[j]+'_BTagging'
            can[-1].Print(outFileName+'.pdf')
            can[-1].Print(outFileName+'.png')
            can[-1].Print(outFileName+'.C')
            subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_27/RPV10/*',shell=True)
