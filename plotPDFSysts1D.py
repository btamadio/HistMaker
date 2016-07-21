#!/usr/bin/env python
import argparse,ROOT,os,glob,sys,subprocess,math
from pointDictTruth import pointDictTruth
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
        upHist.SetMinimum(0)
    elif upHist.GetMaximum() < 10:
        upHist.SetMaximum(10)
        upHist.SetMinimum(0)
    else:
        mx = upHist.GetMaximum()
        upHist.SetMaximum(1.1*mx)
        upHist.SetMinimum(0)
        
    gridLine = ROOT.TLine()
    gridLine.SetLineColor(ROOT.kBlack)
    gridLine.DrawLine(0.850,0,1.850,0)

    ROOT.ATLASLabel(0.525,0.88,'Simulation Internal')
    lat = ROOT.TLatex()

    lat.DrawLatexNDC(0.5,0.8,'PDF Uncertainty (%)')
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
    if 'h_SRyield_4' in key.GetName():
        if int(key.GetName().split('_')[2]) not in dsidList:
            dsidList.append( int(key.GetName().split('_')[2] ) )
dsidList.sort()

#for use in tlatex
srNames = ['4jSRb1','4jSR','5jSRb1','5jSR']
mjCutNames=['MJ > 600 GeV','MJ > 650 GeV','MJ > 700 GeV','MJ > 750 GeV','MJ > 800 GeV']

#for use in file names
srLabs = ['m4_b1','m4_b9','m5_b1','m5_b9']
mjCutLabs = ['MJ_600_13000','MJ_650_13000','MJ_700_13000','MJ_750_13000','MJ_800_13000']

histNames = ['h_MJ_4jSR_b1_','h_MJ_4jSR','h_MJ_5jSR_b1_','h_MJ_5jSR']
srBin = 1
can = []

bTagUpList=[]

for i in range(len(srNames)):
    for j in range(len(mjCutNames)):
        if i==i and j==j:
            nomFile=ROOT.TFile.Open(filePath+'/nominal.root')
            bTagUpList.append(ROOT.TH1D('hTotUp_'+srLabs[i]+'_'+mjCutLabs[j],'systematics',24,0.775,1.975))
            can.append(ROOT.TCanvas('c_'+str(len(can)),'c_'+str(len(can)),800,600))
            can[-1].cd()
            for m in range(len(dsidList)):
                if dsidList[m] < 404251:
                    continue
                for k in range(5):
                    mG = pointDictTruth[int(dsidList[m])][0]/1000.
                    nomHist=nomFile.Get(histNames[i]+'0_'+str(dsidList[m]))
                    upHist=nomFile.Get(histNames[i]+str(k)+'_'+str(dsidList[m]))
                    mjCutList=[600,650,700,750,800]
                    endInt = upHist.GetNbinsX()
                    upInt = upHist.Integral(upHist.FindBin(mjCutList[j]),endInt)
                    nomInt = nomHist.Integral(nomHist.FindBin(mjCutList[j]),endInt)
                    upPercent=1E-8
                    if nomInt!=0:
                        upPercent =100*abs(upInt/nomInt-1)
                    xBin = bTagUpList[-1].GetXaxis().FindBin(mG)
#                    print xBin,mG,nomInt,upInt,upPercent
                    if upPercent > bTagUpList[-1].GetBinContent(xBin):
                        bTagUpList[-1].SetBinContent(xBin,upPercent)
            drawHists(bTagUpList[-1],0,i,j,k)
            outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/PDF_Reweighting/07_18/RPV6/'
            outFileName+='uncert_RPV6_'+srLabs[i]+'_'+mjCutLabs[j]+'_PDF'
            can[-1].Print(outFileName+'.pdf')
            can[-1].Print(outFileName+'.png')
            can[-1].Print(outFileName+'.C')
            subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/PDF_Reweighting/07_18/RPV6/*',shell=True)
