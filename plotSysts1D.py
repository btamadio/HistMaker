#!/usr/bin/env python
import argparse,ROOT,os,glob,sys,subprocess,math
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser(add_help=False, description='Plot Systs')
parser.add_argument('input')
args = parser.parse_args()
filePath = args.input.strip('/')


def drawHists(upHist,downHist,i,j,k):
    upHist.Draw('HIST')
    upHist.GetXaxis().SetTitle('m_{#tilde{g}} [TeV]')
    upHist.GetYaxis().SetTitle('% uncertainty')
    upHist.SetFillColor(ROOT.kBlue-10)
    upHist.SetLineColor(ROOT.kBlue)
    if upHist.GetMaximum() < 15:
        upHist.SetMaximum(15)
        upHist.SetMinimum(-15)
    elif upHist.GetMaximum() < 20:
        upHist.SetMaximum(20)
        upHist.SetMinimum(-20)
    else:
        mx = upHist.GetMaximum()
        upHist.SetMaximum(1.1*mx)
        upHist.SetMinimum(-1.1*mx)
                
    if downHist:
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
    if k!=-1:
        lat.DrawLatexNDC(0.525,0.8,systDict[systList[k]])
    else:
        lat.DrawLatexNDC(0.525,0.8,'JMS Total')        
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
systDict={'JET_EtaIntercalibration_NonClosure':'Small-R #eta-intercalibration',
          'JET_GroupedNP_1':'Small-R NP 1',
          'JET_GroupedNP_2':'Small-R NP 2',
          'JET_GroupedNP_3':'Small-R NP 3',
          'JET_JER_SINGLE_NP':'Small-R JER',
          'JET_RelativeNonClosure_AFII':'Small-R AFII non-closure',
          'JET_Rtrk_Baseline_All':'R_{trk} Baseline',
          'JET_Rtrk_Modelling_All':'R_{trk} Modelling',
          'JET_Rtrk_TotalStat_All':'R_{trk} Statistics',
          'JET_Rtrk_Tracking_All':'R_{trk} Tracking',
          'JMR_Smear':'Large-R JMR'}

#list of uncertainties to include in total JMS
jmsSystList = ['JET_Rtrk_Baseline_All',
               'JET_Rtrk_Modelling_All',
               'JET_Rtrk_TotalStat_All',
               'JET_Rtrk_Tracking_All']

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
canTot = []
jmsUpList = []
jmsDownList = []

for i in range(len(srNames)):
    for j in range(len(mjCutNames)):
        if i==i and j==j:
            jmsUpList.append(ROOT.TH1D('hTot_'+srLabs[i]+'_'+mjCutLabs[j]+'__1up','JMS up',10,0.850,1.850))
            jmsDownList.append(ROOT.TH1D('hTot_'+srLabs[i]+'_'+mjCutLabs[j]+'__1down','JMS down',10,0.850,1.850))
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
                upHist = ROOT.TH1D('h_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]+'__1up','systematics',10,0.850,1.850)
                downHist = ROOT.TH1D('h_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]+'__1down','systematics',10,0.850,1.850)
                for m in range(len(dsidList)):
                    nomSRyield = nomFile.Get('h_SRyield_'+str(dsidList[m]))
                    upSRyield = upFile.Get('h_SRyield_'+str(dsidList[m]))
                    downSRyield = 0
                    if downFile:
                        downSRyield = downFile.Get('h_SRyield_'+str(dsidList[m]))
                    mG = pointDict[int(dsidList[m])][0]
                    upPercent = 100*(upSRyield[srBin]-nomSRyield[srBin])/nomSRyield[srBin]
                    if upPercent == 0:
                        upPercent=1E-8
                    upHist.Fill(mG/1000.,upPercent)
                    if downFile:
                        downPercent=100*(downSRyield[srBin]-nomSRyield[srBin])/nomSRyield[srBin]
                        if downPercent==0:
                            downPercent=-1E-8
                        downHist.Fill(mG/1000.,downPercent)
                    if systList[k] in jmsSystList:
                        jmsUpList[-1].Fill(mG/1000.,upPercent*upPercent)
                        if downFile:
                            jmsDownList[-1].Fill(mG/1000.,downPercent*downPercent)
                if downFile:
                    drawHists(upHist,downHist,i,j,k)
                else:
                    drawHists(upHist,0,i,j,k)
                # upHist.Draw('HIST')
                # upHist.GetXaxis().SetTitle('m_{#tilde{g}} [TeV]')
                # upHist.GetYaxis().SetTitle('% uncertainty')
                # upHist.SetFillColor(ROOT.kBlue-10)
                # upHist.SetLineColor(ROOT.kBlue)
                # upHist.SetMaximum(15)
                # upHist.SetMinimum(-15)
                
                # if downFile:
                #     downHist.SetMarkerSize(1.5)
                #     downHist.Draw('HIST SAME')
                #     downHist.Draw('SAME AXIS')
                #     downHist.SetFillColorAlpha(ROOT.kRed-10,1.0)
                #     downHist.SetLineColor(ROOT.kRed)

                # gridLine = ROOT.TLine()
                # gridLine.SetLineColor(ROOT.kBlack)
                # gridLine.DrawLine(0.850,0,1.850,0)

                # ROOT.ATLASLabel(0.525,0.88,'Simulation Internal')
                # lat = ROOT.TLatex()
                # lat.DrawLatexNDC(0.525,0.8,systDict[systList[k]])
                # lat.DrawLatexNDC(0.7,0.72,srNames[i])
                # lat.DrawLatexNDC(0.7,0.65,mjCutNames[j])
                outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_02/RPV6/'
                outFileName+='uncert_RPV6_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]
                can[-1].Print(outFileName+'.pdf')
                can[-1].Print(outFileName+'.png')
                can[-1].Print(outFileName+'.C')
                subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_02/RPV6/*',shell=True)

        if i==i and j==j:
            canTot.append(ROOT.TCanvas('cTot_'+str(srBin),'cTot_'+str(srBin),800,600))
            canTot[-1].cd()
            jmsUpHist = jmsUpList[-1]
            jmsDownHist = jmsDownList[-1]
            for xBin in range(1,jmsUpHist.GetNbinsX()+1):
                binCup = jmsUpHist.GetBinContent(xBin)
                binCup = math.sqrt(binCup)
                jmsUpHist.SetBinContent(xBin,binCup)
                binCdown = jmsDownHist.GetBinContent(xBin)
                binCdown = math.sqrt(binCdown)
                jmsDownHist.SetBinContent(xBin,-1*binCdown)
            drawHists(jmsUpHist,jmsDownHist,i,j,-1)
            outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_02/RPV6/'
            outFileName+='uncert_RPV6_'+srLabs[i]+'_'+mjCutLabs[j]+'_JMSTotal'
            canTot[-1].Print(outFileName+'.pdf')
            canTot[-1].Print(outFileName+'.png')
            canTot[-1].Print(outFileName+'.C')
        srBin+=1
