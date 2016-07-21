#!/usr/bin/env python
import argparse,ROOT,os,glob,sys,subprocess,math
from pointDict import pointDict
from pointDictTruth import pointDictTruth
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

ROOT.gROOT.SetBatch(True)

def drawHists(upHist,downHist,i,j,k=-1):
    ROOT.gStyle.SetPaintTextFormat('1.1f')
    upHist.Draw('TEXT')
    upHist.GetXaxis().SetTickLength(0)
    upHist.GetXaxis().SetTitle('m_{#tilde{g}} [TeV]')
    upHist.GetYaxis().SetTitle('m_{#tilde{#chi}} [GeV]')
    upHist.GetYaxis().SetTickLength(0)
    upHist.GetYaxis().SetLabelOffset(99)
    upHist.GetXaxis().SetLabelOffset(99)
    upHist.SetMarkerSize(0.8)
    t=ROOT.TText()
    t.SetTextAngle(0)
    t.SetTextSize(0.05)
    t.SetTextAlign(33)

    gridLine = ROOT.TLine()
    gridLine.SetLineStyle(2)
    gridLine.SetLineColor(ROOT.kGray)
    #vertical lines
    # for xi in range(650,1950,100):
    #     gridLine.DrawLine(xi,-200,xi,1800)
    # for yi in range(-50,1850,200):
    #     gridLine.DrawLine(550,yi,1950,yi)
    for xLab in range(700,2000,100):
        t.DrawText(xLab+50,-215,str(xLab/1000.))
    for yLab in range(50,1700,200):
        t.DrawText(535,(yLab+50),str(yLab))
    if downHist:
        downHist.SetMarkerSize(1.5)
        downHist.Draw('TEXT SAME')

    ROOT.ATLASLabel(0.2,0.88,'Simulation Internal')
    lat = ROOT.TLatex()

    lat.DrawLatexNDC(0.2,0.8,'PDF Uncertainty (%)')
    lat.DrawLatexNDC(0.2,0.72,srNames[i])
    lat.DrawLatexNDC(0.2,0.65,mjCutNames[j])

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

lumiLatex=ROOT.TLatex()
lumiString = '#int L dt = 5.8 fb^{-1}'

#for use in tlatex
srNames = ['4jSRb1','4jSR','5jSRb1','5jSR']
histNames = ['h_MJ_4jSR_b1_','h_MJ_4jSR','h_MJ_5jSR_b1_','h_MJ_5jSR']

mjCutNames=['MJ > 600 GeV','MJ > 650 GeV','MJ > 700 GeV','MJ > 750 GeV','MJ > 800 GeV']
#for use in file names
srLabs = ['m4_b1','m4_b9','m5_b1','m5_b9']
mjCutLabs = ['MJ_600_13000','MJ_650_13000','MJ_700_13000','MJ_750_13000','MJ_800_13000']

srBin = 1
can = []
canPDF = []
bTagUpList=[]
pdfList = []
for i in range(len(srNames)):
    for j in range(len(mjCutNames)):
        if i==i and j==j:
            nomFile=ROOT.TFile.Open(filePath+'/nominal.root')
            bTagUpList.append(ROOT.TH2D('hTotUp_'+srLabs[i]+'_'+mjCutLabs[j],'systematics',28,575,1975,43,-175,1975))
            pdfList.append(ROOT.TH2D('hPDF_'+srLabs[i]+'_'+mjCutLabs[j],'most discrepant PDF',28,575,1975,43,-175,1975))
            #print bTagUpList[-1].GetXaxis().GetBinCenter(10),bTagUpList[-1].GetYaxis().GetBinCenter(10)
            can.append(ROOT.TCanvas('c_'+str(len(can)),'c_'+str(len(can)),800,600))
            canPDF.append(ROOT.TCanvas('cPDF_'+str(len(can)),'cPDF_'+str(len(can)),800,600))

            for m in range(len(dsidList)):
                mG = pointDictTruth[int(dsidList[m])][0]
                mX = pointDictTruth[int(dsidList[m])][1]
                if mX == 0:
                    continue
                for k in range(5):
                    nomHist=nomFile.Get(histNames[i]+'0_'+str(dsidList[m]))
                    upHist=nomFile.Get(histNames[i]+str(k)+'_'+str(dsidList[m]))
                    if not nomHist:
                        print 'Could not find histogram',histNames[i]+'0_'+str(dsidList[m])
                        sys.exit(1)
                    elif not upHist:
                        print 'Could not find histogram',histNames[i]+str(k)+'_'+str(dsidList[m])
                        sys.exit(1)
                    mjCutList=[600,650,700,750,800]
                    endInt = upHist.GetNbinsX()
                    upInt = upHist.Integral(upHist.FindBin(mjCutList[j]),endInt)
                    nomInt = nomHist.Integral(nomHist.FindBin(mjCutList[j]),endInt)
                    upPercent=1E-8
                    if nomInt!=0:
                        upPercent = 100*abs(upInt/nomInt-1)
                    xBin = bTagUpList[-1].GetXaxis().FindBin(mG)
                    yBin = bTagUpList[-1].GetYaxis().FindBin(mX)
                    if upPercent > bTagUpList[-1].GetBinContent(xBin,yBin):
                        bTagUpList[-1].SetBinContent(xBin,yBin,upPercent)
                        pdfList[-1].SetBinContent(xBin,yBin,k)
            can[-1].cd()
            drawHists(bTagUpList[-1],0,i,j)
            canPDF[-1].cd()
            drawHists(pdfList[-1],0,i,j)
            outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/PDF_Reweighting/07_18/RPV10/'
            outFileName+='uncert_RPV10_'+srLabs[i]+'_'+mjCutLabs[j]+'_PDF'
            can[-1].Print(outFileName+'.pdf')
            can[-1].Print(outFileName+'.png')
            can[-1].Print(outFileName+'.C')
            subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/PDF_Reweighting/07_18/RPV10/*',shell=True)
