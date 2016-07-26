#!/usr/bin/env python
import argparse,ROOT,os,glob,sys,subprocess,math
from pointDict import pointDict
from pointDictTruth import pointDictTruth

ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser(add_help=False, description='Plot Systs')
parser.add_argument('input')
args = parser.parse_args()
filePath = args.input.strip('/')
#converts DSID from truth grid to DSID from reco grid
#returns 0 if truth point not in reco grid
def truthToReco(dsid):
    mG = pointDictTruth[dsid][0]
    mX = pointDictTruth[dsid][1]
    for key in pointDict:
        if pointDict[key][0] == mG and pointDict[key][1] == mX and mX == 0:
            return key
    return 0
def getInfo(dsid):
    if dsid in pointDictTruth:
        return pointDictTruth[dsid]
    else:
        return pointDict[dsid]
def drawHists(upHist,downHist,i,j,k):

    downHist.SetMarkerSize(1.5)
    downHist.SetFillColorAlpha(ROOT.kRed-10,1.0)
    downHist.SetLineColor(ROOT.kRed)
    upHist.Draw('HIST')
    upHist.Draw('E SAME')
    downHist.Draw('HIST SAME')
    downHist.Draw('E SAME')
    downHist.Draw('SAME AXIS')
    upHist.GetXaxis().SetTitle('m_{#tilde{g}} [TeV]')
    upHist.GetYaxis().SetTitle('% uncertainty')
    upHist.SetFillColor(ROOT.kBlue-10)
    upHist.SetLineColor(ROOT.kBlue)
    if upHist.GetMaximum() < 15:
        upHist.SetMaximum(15)
        upHist.SetMinimum(0)
        if downHist:
            upHist.SetMinimum(-15)
    else:
        mx = upHist.GetMaximum()
        upHist.SetMaximum(1.4*mx)
        upHist.SetMinimum(0)
        if downHist:
            upHist.SetMinimum(-1.4*mx)
                
        
    gridLine = ROOT.TLine()
    gridLine.SetLineColor(ROOT.kBlack)
    gridLine.DrawLine(0.850,0,1.850,0)

    ROOT.ATLASLabel(0.525,0.88,'Simulation Internal')
    lat = ROOT.TLatex()
    if k>=0:
        lat.DrawLatexNDC(0.525,0.8,systDict[systList[k]])
        lat.DrawLatexNDC(0.7,0.72,srNames[i])
        lat.DrawLatexNDC(0.7,0.65,mjCutNames[j])
    elif k==-1:
        lat.DrawLatexNDC(0.2,0.8,'AkT10 Total ISR Uncertainty (%)')
        lat.DrawLatexNDC(0.7,0.72,srNames[i])
        lat.DrawLatexNDC(0.7,0.65,mjCutNames[j])

#get list of systematics from file names
systList = []
dsidList = []
fileList = glob.glob(filePath + '/*.root')
for f in fileList:
    systName = os.path.basename(f).split('.')[0].split('__')[0]
    if systName not in systList and systName != 'nominal':
        systList.append(systName)

systDict={'scalefactor':'Scale Factor Uncert (%)',
          'pTmaxFudge':'p_{T} Max Fudge Uncertainty (%)',
          'alphaS':'#alpha_{s} Uncertainty (%)',
          'pTdampMatch':'p_{T} Damp Max Uncertainty (%)'}

jmsSystList = ['pTmaxFudge',
               'alphaS',
               'pTdampMatch']

#get list of signal points from nominal file
nomFile = ROOT.TFile.Open(filePath+'/nominal.root')
for key in nomFile.GetListOfKeys():
    if 'h_SRyield_4' in key.GetName():
        dsid = int(key.GetName().split('_')[2])
        if dsid not in dsidList and truthToReco(dsid) !=0:
            dsidList.append( dsid )
dsidList.sort()

#for use in tlatex
srNames = ['4jSRb1','4jSR','5jSRb1','5jSR']
mjCutNames=['MJ > 600 GeV','MJ > 650 GeV','MJ > 700 GeV','MJ > 750 GeV','MJ > 800 GeV']
#for use in file names
srLabs = ['m4_b1','m4_b9','m5_b1','m5_b9']
mjCutLabs = ['MJ_600_13000','MJ_650_13000','MJ_700_13000','MJ_750_13000','MJ_800_13000']

srBin = 0
can = []
canTot = []
jmsUpList = []
jmsDownList = []

for i in range(len(srNames)):
    for j in range(len(mjCutNames)):
        srBin+=1
        if i==i and j==j:
            nomFile=ROOT.TFile.Open(filePath+'/nominal.root')
            jmsUpList.append(ROOT.TH1D('hTot_'+srLabs[i]+'_'+mjCutLabs[j]+'__1up','JMS up',10,0.850,1.850))
            jmsDownList.append(ROOT.TH1D('hTot_'+srLabs[i]+'_'+mjCutLabs[j]+'__1down','JMS down',10,0.850,1.850))
        for k in range(len(systList)):
            if i==i and j==j and k==k:
                nomFile = ROOT.TFile.Open(filePath+'/nominal.root')
                upFile = ROOT.TFile.Open(filePath+'/'+systList[k]+'__1up.root')
                downFile = ROOT.TFile.Open(filePath+'/'+systList[k]+'__1down.root')
                can.append(ROOT.TCanvas('c_'+str(len(can)),'c_'+str(len(can)),800,600))
                can[-1].cd()
                upHist = ROOT.TH1D('h_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]+'__1up','systs',10,0.850,1.850)
                downHist = ROOT.TH1D('h_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]+'__1down','systs',10,0.850,1.850)
                for m in range(len(dsidList)):
                    mG = getInfo(dsidList[m])[0]
                    nomSRyield = nomFile.Get('h_SRyield_'+str(dsidList[m]))
                    nomSRyield_uw=nomFile.Get('h_SRyield_unweighted_'+str(dsidList[m]))
                    upSRyield = upFile.Get('h_SRyield_'+str(truthToReco(dsidList[m])))
                    upSRyield_uw = upFile.Get('h_SRyield_unweighted_'+str(truthToReco(dsidList[m])))
                    downSRyield = downFile.Get('h_SRyield_'+str(truthToReco(dsidList[m])))
                    downSRyield_uw = downFile.Get('h_SRyield_unweighted_'+str(truthToReco(dsidList[m])))

                    upNp = upSRyield_uw.GetBinContent(srBin)
                    dwNp = downSRyield_uw.GetBinContent(srBin)
                    nomNp = nomSRyield_uw.GetBinContent(srBin)

                    upN0 = 50000.
                    dwN0 = 50000.
                    nomN0 = 100000.

                    upEps = upNp/upN0
                    dwEps = dwNp/dwN0
                    nomEps = nomNp/nomN0

                    upUncert = upEps*(1-upEps)*upN0/(upNp*upNp)+nomEps*(1-nomEps)*nomN0/(nomNp*nomNp)
                    upUncert *= (2*upNp/nomNp)*(2*upNp/nomNp)
                    upUncert = 100*math.sqrt(upUncert)

                    dwUncert = dwEps*(1-dwEps)*dwN0/(dwNp*dwNp)+nomEps*(1-nomEps)*nomN0/(nomNp*nomNp)
                    dwUncert *= (2*dwNp/nomNp)*(2*dwNp/nomNp)
                    dwUncert = 100*math.sqrt(dwUncert)
                    

                    upYield = 0
                    downYield = 0
                    upPercent=0
                    downPercent=0
                    nomYield = nomSRyield.GetBinContent(srBin)
                    if upSRyield:
                        upYield = upSRyield.GetBinContent(srBin)
                        upPercent = 100*(upYield-nomYield)/nomYield
#                        if systList[k] in jmsSystList:
#                            jmsUpList[-1].Fill(mG/1000.,upPercent*upPercent)
                    if downSRyield:
                        downYield = downSRyield.GetBinContent(srBin)
                        downPercent = 100*(downYield-nomYield)/nomYield
#                        if systList[k] in jmsSystList:
#                            jmsDownList[-1].Fill(mG/1000.,downPercent*downPercent)
#                    print mG,systList[k],srBin,nomEps,upEps,dwEps,upUncert
                    upHist.Fill(mG/1000.,upPercent)
#                    print upHist.FindBin(mG/1000.)
                    upHist.SetBinError(upHist.FindBin(mG/1000.),upUncert)
                    downHist.Fill(mG/1000.,downPercent)
                    downHist.SetBinError(downHist.FindBin(mG/1000.),dwUncert)
                drawHists(upHist,downHist,i,j,k)
                outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/ISR_Uncertainty/07_22/RPV6/'
                outFileName+='uncert_RPV6_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]
                can[-1].Print(outFileName+'.pdf')
                can[-1].Print(outFileName+'.png')
                can[-1].Print(outFileName+'.C')
                subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/ISR_Uncertainty/07_22/RPV6/*',shell=True)

        if i==i and j==10000:
            canTot.append(ROOT.TCanvas('cTot_'+str(srBin),'cTot_'+str(srBin),800,600))
            canTot[-1].cd()
            jmsUpHist = jmsUpList[-1]
            jmsDownHist = jmsDownList[-1]
            for xBin in range(1,jmsUpHist.GetNbinsX()+1):
                binCup = jmsUpHist.GetBinContent(xBin)
                binCup = math.sqrt(binCup)
                jmsUpHist.SetBinContent(xBin,binCup)
                binCdown = jmsDownHist.GetBinContent(xBin)
                binCdown = -1*math.sqrt(abs(binCdown))
                jmsDownHist.SetBinContent(xBin,-1*binCdown)
            drawHists(jmsUpHist,jmsDownHist,i,j,-1)
            outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/ISR_Uncertainty/07_22/RPV6/'
            outFileName+='uncert_RPV6_'+srLabs[i]+'_'+mjCutLabs[j]+'_ISRTotal'
            #canTot[-1].Print(outFileName+'.pdf')
            #canTot[-1].Print(outFileName+'.png')
            #canTot[-1].Print(outFileName+'.C')
