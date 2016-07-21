#!/usr/bin/env python
import argparse,ROOT,os,glob,sys,subprocess,math
from pointDict import pointDict
from pointDictTruth import pointDictTruth
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

ROOT.gROOT.SetBatch(True)
#converts DSID from truth grid to DSID from reco grid
#returns 0 if truth point not in reco grid
def truthToReco(dsid):
    mG = pointDictTruth[dsid][0]
    mX = pointDictTruth[dsid][1]
    for key in pointDict:
        if pointDict[key][0] == mG and pointDict[key][1] == mX and mX!=0:
            return key
    return 0

def drawHists(upHist,downHist,i,j,k):
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
        if k >= -1:
            gridLine.DrawLine(xi,-200,xi,1800)
        elif xi > 650:
            gridLine.DrawLine(xi,-50,xi,1750)
    for yi in range(-50,1850,200):
        if k >= -1:
            gridLine.DrawLine(550,yi,1950,yi)
        elif  yi > -50 and yi < 1600:
            gridLine.DrawLine(650,yi,1950,yi)
    for xLab in range(700,2000,100):
        if k >= -1:
            t.DrawText(xLab+50,-215,str(xLab/1000.))
        else:
            t.DrawText(xLab+50,-65,str(xLab/1000.))
    for yLab in range(50,1700,200):
        if k >=-1:
            t.DrawText(535,(yLab+50),str(yLab))
        else:
            t.DrawText(635,(yLab+50),str(yLab))
    if downHist:
        downHist.SetMarkerSize(1.5)
        downHist.Draw('TEXT SAME')

    ROOT.ATLASLabel(0.2,0.88,'Simulation Internal')
    lat = ROOT.TLatex()
    if k>=0:
        lat.DrawLatexNDC(0.2,0.8,systDict[systList[k]])
    elif k==-1:
        lat.DrawLatexNDC(0.2,0.8,'Total ISR Uncertainty (%)')
    lat.DrawLatexNDC(0.2,0.72,srNames[i])
    lat.DrawLatexNDC(0.2,0.65,mjCutNames[j])

parser = argparse.ArgumentParser(add_help=False, description='Plot Systs')
parser.add_argument('input')
args = parser.parse_args()
filePath = args.input.strip('/')
systDict={'scalefactor':'Scale Factor Uncert (%)',
          'pTmaxFudge':'p_{T} Max Fudge Uncertainty (%)',
          'alphaS':'#alpha_{s} Uncertainty (%)',
          'pTdampMatch':'p_{T} Damp Max Uncertainty (%)'}

jmsSystList = ['pTmaxFudge',
               'alphaS',
               'pTdampMatch']

#get list of systematics from file names
systList = []
#dsidList will contain DSIDs from pointDictTruth. Use truthToReco(dsid) to convert to reco grid
dsidList = []
fileList = glob.glob(filePath + '/*.root')
for f in fileList:
    systName = os.path.basename(f).split('.')[0].split('__')[0]
    if systName not in systList and systName != 'nominal':
        systList.append(systName)

#get list of signal points from nominal file
nomFile = ROOT.TFile.Open(filePath+'/nominal.root')
for key in nomFile.GetListOfKeys():
    if 'h_SRyield_4' in key.GetName():
        dsid = int(key.GetName().split('_')[2])
        if dsid not in dsidList and truthToReco(dsid) != 0:
            dsidList.append( dsid )
dsidList.sort()

#for use in tlatex
srNames = ['4jSRb1','4jSR','5jSRb1','5jSR']
mjCutNames=['MJ > 600 GeV','MJ > 650 GeV','MJ > 700 GeV','MJ > 750 GeV','MJ > 800 GeV']
#for use in file names
srLabs = ['m4_b1','m4_b9','m5_b1','m5_b9']
mjCutLabs = ['MJ_600_13000','MJ_650_13000','MJ_700_13000','MJ_750_13000','MJ_800_13000']

srBin = 1
can = []
canTot = []
jmsUpList = []
jmsDownList = []
canEff=[]
for i in range(len(srNames)):
    for j in range(len(mjCutNames)):
        if i==i and j==j:
            nomFile=ROOT.TFile.Open(filePath+'/nominal.root')
            jmsUpList.append(ROOT.TH2D('hTotUp_'+srLabs[i]+'_'+mjCutLabs[j],'systematics',14,550,1950,10,-200,1800))
            jmsDownList.append(ROOT.TH2D('hTotDown_'+srLabs[i]+'_'+mjCutLabs[j],'systematics',14,550,1950,10,-300,1700))
            jmsUpList[-1].SetDirectory(0)
            jmsDownList[-1].SetDirectory(0)
        for k in range(len(systList)):
            if i==i and j==j and k==k:
                nomFile = ROOT.TFile.Open(filePath+'/nominal.root')
                upFile = ROOT.TFile.Open(filePath+'/'+systList[k]+'__1up.root')
                downFile=0
                if filePath+'/'+systList[k]+'__1down.root' in fileList:
                    downFile = ROOT.TFile.Open(filePath+'/'+systList[k]+'__1down.root')
                can.append(ROOT.TCanvas('c_'+str(len(can)),'c_'+str(len(can)),800,600))
                can[-1].cd()
                upHist=ROOT.TH2D('h_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]+'__1up','systematics',14,550,1950,10,-200,1800)
                downHist=ROOT.TH2D('h_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]+'__1down','systematics',14,550,1950,10,-300,1700)
                for m in range(len(dsidList)):
                    nomSRyield = nomFile.Get('h_SRyield_'+str(dsidList[m]))
                    upSRyield = upFile.Get('h_SRyield_'+str(truthToReco(dsidList[m])))
                    downSRyield = 0
                    if downFile:
                        downSRyield = downFile.Get('h_SRyield_'+str(truthToReco(dsidList[m])))
                    mG = pointDictTruth[int(dsidList[m])][0]
                    mX = pointDictTruth[int(dsidList[m])][1]
                    upPercent = 100*(upSRyield[srBin]-nomSRyield[srBin])/nomSRyield[srBin]
                    if upPercent == 0:
                        upPercent=1E-8
                    upHist.Fill(mG,mX,upPercent)
                    if downFile:
                        downPercent=100*(downSRyield[srBin]-nomSRyield[srBin])/nomSRyield[srBin]
                        if downPercent==0:
                            downPercent=-1E-8
                        downHist.Fill(mG,mX,downPercent)
                    if systList[k] in jmsSystList:
                        jmsUpList[-1].Fill(mG,mX,upPercent*upPercent)
                        if downFile:
                            jmsDownList[-1].Fill(mG,mX,downPercent*downPercent)
                if downFile:
                    drawHists(upHist,downHist,i,j,k)
                else:
                    drawHists(upHist,0,i,j,k)

                outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/ISR_Uncertainty/07_21/RPV10/'
                outFileName+='uncert_RPV10_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]
                can[-1].Print(outFileName+'.pdf')
                can[-1].Print(outFileName+'.png')
                can[-1].Print(outFileName+'.C')
                subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/ISR_Uncertainty/07_21/RPV10/*',shell=True)
        if i==i and j==j:
            canTot.append(ROOT.TCanvas('cTot_'+str(srBin),'cTot_'+str(srBin),800,600))
            canTot[-1].cd()
            jmsUpHist = jmsUpList[-1]
            jmsDownHist = jmsDownList[-1]
            for xBin in range(1,jmsUpHist.GetNbinsX()+1):
                for yBin in range(1,jmsUpHist.GetNbinsY()+1):
                    binCup = jmsUpHist.GetBinContent(xBin,yBin)
                    binCup = math.sqrt(binCup)
                    jmsUpHist.SetBinContent(xBin,yBin,binCup)
                    binCdown = jmsDownHist.GetBinContent(xBin,yBin)
                    binCdown = math.sqrt(binCdown)
                    jmsDownHist.SetBinContent(xBin,yBin,-1*binCdown)
            drawHists(jmsUpHist,jmsDownHist,i,j,-1)
            outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/ISR_Uncertainty/07_21/RPV10/'
            outFileName+='uncert_RPV10_'+srLabs[i]+'_'+mjCutLabs[j]+'_ISRTotal'
            canTot[-1].Print(outFileName+'.pdf')
            canTot[-1].Print(outFileName+'.png')
            canTot[-1].Print(outFileName+'.C')
        srBin+=1

