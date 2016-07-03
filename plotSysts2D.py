#!/usr/bin/env python
import argparse,ROOT,os,glob,sys,subprocess
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

#ROOT.gROOT.SetBatch(True)
parser = argparse.ArgumentParser(add_help=False, description='Plot Systs')
parser.add_argument('input')
args = parser.parse_args()
filePath = args.input.strip('/')

#get list of systematics from file names
systList = []
dsidList = []
fileList = glob.glob(filePath + '/*.root')
for f in fileList:
    systName = os.path.basename(f).split('.')[0].split('__')[0]
    if systName not in systList and systName != 'nominal':
        systList.append(systName)

#get list of signal points from nominal file
nomFile = ROOT.TFile.Open(filePath+'/nominal.root')
for key in nomFile.GetListOfKeys():
    if 'h_cutflow_' in key.GetName():
        if int(key.GetName().split('_')[2]) not in dsidList:
            dsidList.append( int(key.GetName().split('_')[2] ) )
dsidList.sort()

lumiLatex=ROOT.TLatex()
lumiString = '#int L dt = 5.8 fb^{-1}'

#for use in tlatex
srNames = ['4jSRb1','4jSR','5jSRb1','5jSR']
mjCutNames=['MJ > 600 GeV','MJ > 650 GeV','MJ > 700 GeV','MJ > 750 GeV','MJ > 800 GeV']
#for use in file names
srLabs = ['m4_b1','m4_b9','m5_b1','m5_b9']
mjCutLabs = ['MJ_600_13000','MJ_650_13000','MJ_700_13000','MJ_750_13000','MJ_800_13000']

srBin = 1
can = []
for i in range(len(srNames)):
    for j in range(len(mjCutNames)):
        for k in range(len(systList)):
            if i==0 and j==0 and k==4:
                nomFile = ROOT.TFile.Open(filePath+'/nominal.root')
                upFile = ROOT.TFile.Open(filePath+'/'+systList[k]+'__1up.root')
                downFile=0
                if filePath+'/'+systList[k]+'__1down.root' in fileList:
                    downFile = ROOT.TFile.Open(filePath+'/'+systList[k]+'__1down.root')
                can.append(ROOT.TCanvas('c_'+str(len(can)),'c_'+str(len(can)),800,600))
                can[-1].cd()
                upHist = ROOT.TH2D('h_'+srLabs[i]+'_'+mjCutLabs[j]+'__1up','systematics',14,550,1950,10,-200,1800)
                downHist = ROOT.TH2D('h_'+srLabs[i]+'_'+mjCutLabs[j]+'__1down','systematics',14,550,1950,10,-300,1700)
                for m in range(len(dsidList)):
                    nomSRyield = nomFile.Get('h_SRyield_'+str(dsidList[m]))
                    upSRyield = upFile.Get('h_SRyield_'+str(dsidList[m]))
                    downSRyield = 0
                    if downFile:
                        downSRyield = downFile.Get('h_SRyield_'+str(dsidList[m]))
                    mG = pointDict[int(dsidList[m])][0]
                    mX = pointDict[int(dsidList[m])][1]
                    upHist.Fill(mG,mX,100*(upSRyield[srBin]-nomSRyield[srBin])/nomSRyield[srBin])
                    if downFile:
                        downHist.Fill(mG,mX,100*(downSRyield[srBin]-nomSRyield[srBin])/nomSRyield[srBin])
                ROOT.gStyle.SetPaintTextFormat('+1.1f\%')
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
                for xLab in range(700,2000,100):
                    t.DrawText(xLab+25,-215,str(xLab/1000.))
                for yLab in range(50,1700,200):
                    t.DrawText(535,(yLab+50),str(yLab))

                if downFile:
                    downHist.SetMarkerSize(1.5)
                    downHist.Draw('TEXT SAME')

                gridLine = ROOT.TLine()
                gridLine.SetLineStyle(2)
                #vertical grid lines
                for xi in range(650,1950,100):
                    gridLine.DrawLine(xi-25,-200,xi-25,1800)

                #horizontal grid lines
                for yi in range(-50,1850,200):
                    gridLine.DrawLine(550,yi,1950,yi)
        srBin+=1
