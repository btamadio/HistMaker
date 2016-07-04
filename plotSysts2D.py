#!/usr/bin/env python
import argparse,ROOT,os,glob,sys,subprocess,math
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

#ROOT.gROOT.SetBatch(True)
parser = argparse.ArgumentParser(add_help=False, description='Plot Systs')
parser.add_argument('input')
args = parser.parse_args()
filePath = args.input.strip('/')
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

jmsSystList = ['JET_Rtrk_Baseline_All',
               'JET_Rtrk_Modelling_All',
               'JET_Rtrk_TotalStat_All',
               'JET_Rtrk_Tracking_All']

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
canTot = []
upHist =0
downHist=0
for i in range(len(srNames)):
    for j in range(len(mjCutNames)):
        jmsUpList = []
        jmsDownList = []
        for k in range(len(systList)):
            if i==2 and j==4 and k==k:
                nomFile = ROOT.TFile.Open(filePath+'/nominal.root')
                upFile = ROOT.TFile.Open(filePath+'/'+systList[k]+'__1up.root')
                downFile=0
                if filePath+'/'+systList[k]+'__1down.root' in fileList:
                    downFile = ROOT.TFile.Open(filePath+'/'+systList[k]+'__1down.root')
                can.append(ROOT.TCanvas('c_'+str(len(can)),'c_'+str(len(can)),800,600))
                can[-1].cd()
                upHist = ROOT.TH2D('h_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]+'__1up','systematics',14,550,1950,10,-200,1800)
                downHist = ROOT.TH2D('h_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]+'__1down','systematics',14,550,1950,10,-300,1700)
                for m in range(len(dsidList)):
                    nomSRyield = nomFile.Get('h_SRyield_'+str(dsidList[m]))
                    upSRyield = upFile.Get('h_SRyield_'+str(dsidList[m]))
                    downSRyield = 0
                    if downFile:
                        downSRyield = downFile.Get('h_SRyield_'+str(dsidList[m]))
                    mG = pointDict[int(dsidList[m])][0]
                    mX = pointDict[int(dsidList[m])][1]
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
                    jmsUpList.append(upHist)
                    jmsDownList.append(downHist)
                    print jmsUpList
                    print jmsDownList

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
                #vertical grid lines
                for xi in range(650,1950,100):
                    gridLine.DrawLine(xi,-200,xi,1800)

                #horizontal grid lines
                for yi in range(-50,1850,200):
                    gridLine.DrawLine(550,yi,1950,yi)

                for xLab in range(700,2000,100):
                    t.DrawText(xLab+50,-215,str(xLab/1000.))
                for yLab in range(50,1700,200):
                    t.DrawText(535,(yLab+50),str(yLab))

                if downFile:
                    downHist.SetMarkerSize(1.5)
                    downHist.Draw('TEXT SAME')

                ROOT.ATLASLabel(0.2,0.88,'Simulation Internal')
                lat = ROOT.TLatex()
                lat.DrawLatexNDC(0.2,0.8,systDict[systList[k]])
                lat.DrawLatexNDC(0.2,0.72,srNames[i])
                lat.DrawLatexNDC(0.2,0.65,mjCutNames[j])

                outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_02/RPV10/'
                outFileName+='uncert_RPV10_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]
                can[-1].Print(outFileName+'.pdf')
                can[-1].Print(outFileName+'.png')
                can[-1].Print(outFileName+'.C')
                subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_02/RPV10/*',shell=True)
        # canTot.append(ROOT.TCanvas('cTot_'+str(srBin),'cTot_'+str(srBin),800,600))
        # canTot[-1].cd()
        # jmsUpHist = ROOT.TH2D('hTot_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]+'__1up','total JMS',14,550,1950,10,-200,1800)
        # jmsDownHist = ROOT.TH2D('hTot_'+srLabs[i]+'_'+mjCutLabs[j]+'_'+systList[k]+'__1down','total JMS',14,550,1950,10,-300,1700)
        # for mG in range(700,2000,100):
        #     for mX in range(50,1850,200):
        #         upTot = 0
        #         downTot = 0
        #         for hUp in jmsUpList:
        #             upTot += hUp.GetBinContent(hUp.FindBin(mG,mX)) * hUp.GetBinContent(hUp.FindBin(mG,mX))
        #         for hdown in jmsDownList:
        #             downTot += hDown.GetBinContent(hDown.FindBin(mG,mX)) * hDown.GetBinContent(hDown.FindBin(mG,mX))
        #         jmsUpHist.Fill(mG,mX,math.sqrt(upTot))
        #         jmsDownHist.Fill(mG,mX,math.sqrt(downTot))
        # jmsUpHist.Draw('TEXT')
        # jmsDownHist.Draw('TEXT SAME')
        srBin+=1
