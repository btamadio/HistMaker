#!/usr/bin/env python
import argparse,ROOT,os,glob,sys,subprocess,math
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

#ROOT.gROOT.SetBatch(True)
def drawHists(upHist,downHist,i,j,k):
    upHist.Draw('HIST')
    upHist.GetXaxis().SetTitle('m_{#tilde{g}} [TeV]')
    upHist.GetYaxis().SetTitle('% uncertainty')
    upHist.SetFillColor(ROOT.kBlue-10)
    upHist.SetLineColor(ROOT.kBlue)
    if upHist.GetMaximum() < 5:
        upHist.SetMaximum(5)
        upHist.SetMinimum(-5)
    elif upHist.GetMaximum() < 10:
        upHist.SetMaximum(10)
        upHist.SetMinimum(-10)
    else:
        mx = upHist.GetMaximum()
        upHist.SetMaximum(1.1*mx)
        upHist.SetMinimum(-1.1*mx)
        
    downHist.SetMarkerSize(1.5)
    downHist.Draw('HIST SAME')
    downHist.Draw('SAME AXIS')
    downHist.SetFillColorAlpha(ROOT.kRed-10,1.0)
    downHist.SetLineColor(ROOT.kRed)
        
    gridLine = ROOT.TLine()
    gridLine.SetLineColor(ROOT.kBlack)
    gridLine.DrawLine(0.850,0,1.850,0)

    ROOT.ATLASLabel(0.525,0.88,'Simulation Internal')
    lat = ROOT.TLatex()

    lat.DrawLatexNDC(0.5,0.8,'B-tagging Uncertainty (%)')
    lat.DrawLatexNDC(0.2,0.88,srNames[i])
    lat.DrawLatexNDC(0.2,0.8,mjCutNames[j])

parser = argparse.ArgumentParser(add_help=False, description='Plot Systs')
parser.add_argument('input')
args = parser.parse_args()
filePath = args.input.strip('/')
fileList = glob.glob(filePath + '/*.root')
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
            bTagUpList.append(ROOT.TH1D('hTotUp_'+srLabs[i]+'_'+mjCutLabs[j],'systematics',10,0.850,1.850))
            bTagDownList.append(ROOT.TH1D('hTotDown_'+srLabs[i]+'_'+mjCutLabs[j],'systematics',10,0.850,1.850))
            bTagUpList[-1].SetDirectory(0)
            bTagDownList[-1].SetDirectory(0)
            can.append(ROOT.TCanvas('c_'+str(len(can)),'c_'+str(len(can)),800,600))
            can[-1].cd()

            for m in range(len(dsidList)):
                for k in range(25):
                    mG = pointDict[int(dsidList[m])][0]
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
                    bTagUpList[-1].Fill(mG/1000.,upPercent*upPercent)
                    bTagDownList[-1].Fill(mG/1000.,downPercent*downPercent)

            for xBin in range(1,bTagUpList[-1].GetNbinsX()+1):
                binCup = bTagUpList[-1].GetBinContent(xBin)
                binCup = math.sqrt(binCup)
                binCdown = bTagDownList[-1].GetBinContent(xBin)
                binCdown = math.sqrt(binCdown)
                bTagUpList[-1].SetBinContent(xBin,100*binCup)
                bTagDownList[-1].SetBinContent(xBin,-100*binCdown)
            drawHists(bTagUpList[-1],bTagDownList[-1],i,j,k)
            outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_27/RPV6/'
            outFileName+='uncert_RPV6_'+srLabs[i]+'_'+mjCutLabs[j]+'_BTagging'
            can[-1].Print(outFileName+'.pdf')
            can[-1].Print(outFileName+'.png')
            can[-1].Print(outFileName+'.C')
            subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_27/RPV6/*',shell=True)
