#!/usr/bin/env python
import argparse,ROOT,os,glob,sys,subprocess
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
ROOT.gStyle.SetPaintTextFormat('2.1f')
ROOT.gROOT.SetBatch(True)
parser = argparse.ArgumentParser(add_help=False, description='Plot Systs')
parser.add_argument('input')
args = parser.parse_args()
filePath = args.input.strip('/')
systDict={'JET_EtaIntercalibration_NonClosure':'AkT4 #eta-intercalib Uncert (%)',
          'JET_GroupedNP_1':'AkT4 NP 1 Uncertainty (%)',
          'JET_GroupedNP_2':'AkT4 NP 2 Uncertainty (%)',
          'JET_GroupedNP_3':'AkT4 NP 3 Uncertainty (%)',
          'JET_JER_SINGLE_NP':'AkT4 JER Uncertainty (%)',
          'JET_RelativeNonClosure_AFII':'AkT4 AFII non-closure Uncertainty (%)',
          'JET_Rtrk_Baseline_All':'AkT10 R_{trk} Baseline Uncertainty (%)',
          'JET_Rtrk_Modelling_All':'AkT10 R_{trk} Modelling Uncertainty (%)',
          'JET_Rtrk_TotalStat_All':'AkT10 R_{trk} Statistics Uncertainty (%)',
          'JET_Rtrk_Tracking_All':'AkT10 R_{trk} Tracking Uncertainty (%)',
          'JMR_Smear':'AkT10 JMR Uncertainty (%)'}

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

mjHistNames=['h_MJ_4jSR','h_MJ_5jSR','h_MJ_4jSR_b1_0','h_MJ_5jSR_b1_0']

srNames = ['4jSR','5jSR','4jSRb1','5jSRb1']
canMJ=[]
pad1=[]
pad2=[]
legMJ=[]
ratHistUp=[]
ratHistDown=[]
#for use in file names
srLabs = ['m4_b9','m5_b9','m4_b1','m5_b1']

ci=0


for i in range(len(dsidList)):
   if i==i:
        nomFile = ROOT.TFile.Open(filePath+'/nominal.root')
        for j in range(25):
            for m in range(4,6):
                nomHist=nomFile.Get('h_MJ_'+str(m)+'jSR_b1_0_'+str(dsidList[i]))
                upHist = nomFile.Get('h_MJ_'+str(m)+'jSR_b1_'+str(2*j+2)+'_'+str(dsidList[i]))
                downHist = nomFile.Get('h_MJ_'+str(m)+'jSR_b1_'+str(2*j+1)+'_'+str(dsidList[i]))
                canMJ.append(ROOT.TCanvas('can_'+str(ci),'can_'+str(ci),800,800))
                canMJ[-1].cd()
                pad1.append(ROOT.TPad('pad1_'+str(ci),'pad1_'+str(ci),0,0.2,1,1.0))
                pad1[-1].Draw()
                pad1[-1].cd()
                pad1[-1].SetLogy()

                upHist.SetLineColor(ROOT.kBlue)
                upHist.SetLineWidth(2)
                
                nomHist.SetLineColor(ROOT.kBlack)
                nomHist.SetFillColor(ROOT.kGray)
                nomHist.SetLineWidth(2)
                if nomHist.GetNbinsX() == 150:
                    nomHist.Rebin(5)
                if upHist.GetNbinsX() == 150:
                    upHist.Rebin(5)
                if downHist.GetNbinsX() == 150:
                    downHist.Rebin(5)

                downHist.SetLineColor(ROOT.kRed)
                downHist.SetLineWidth(2)
                legMJ.append(ROOT.TLegend(0.5,0.7,0.75,0.85))
                legMJ[-1].SetBorderSize(0)
                legMJ[-1].SetFillStyle(0)
                legMJ[-1].SetTextSize(0.04)
                legMJ[-1].AddEntry(nomHist,'nominal','f')
                legMJ[-1].AddEntry(upHist,'b-tagging NP'+str(j+1)+' +1 #sigma','f')
                legMJ[-1].AddEntry(downHist,'b-tagging NP'+str(j+1)+' -1 #sigma','f')

                nomHist.Draw('hist')
                nomHist.GetYaxis().SetTitleOffset(1.5)
                nomHist.GetYaxis().SetTitle('Events')
                upHist.Draw('hist same')
                downHist.Draw('hist same')
                legMJ[-1].Draw()
                ROOT.ATLASLabel(0.47,0.88,'Simulation Internal')
                lumiLatex.DrawLatexNDC(0.675,0.6,lumiString)
                lumiLatex.DrawLatexNDC(0.75,0.5,srNames[m-2])
                mG = str(pointDict[int(dsidList[i])][0])
                mX = str(pointDict[int(dsidList[i])][1])
                massString='#splitline{RPV10}{#splitline{m_{#tilde{g}} = '+mG+'}{m_{#tilde{#chi}} = '+mX+'}}'                
                if mX == '0':
                    massString='#splitline{RPV6}{m_{#tilde{g}} = '+mG+'}'
                lumiLatex.DrawLatexNDC(0.2,0.85,massString)
                
                canMJ[-1].cd()

                pad2.append(ROOT.TPad('pad2_'+str(ci),'pad2_'+str(ci),0,0.05,1,0.3))
                pad2[-1].SetTopMargin(0)
                pad2[-1].SetBottomMargin(0.2)
                pad2[-1].SetGridy()
                pad2[-1].Draw()
                pad2[-1].cd() 
                ratHistUp.append(upHist.Clone('ratioUp_'+str(ci)))
                ratHistUp[-1].SetMarkerColor(ROOT.kBlue)
                ratHistUp[-1].SetFillColor(ROOT.kBlue-10)

                ratHistUp[-1].GetYaxis().SetTitle('(syst-nom)/nom')
                ratHistUp[-1].GetYaxis().SetNdivisions(505)
                ratHistUp[-1].GetYaxis().SetTitleSize(20)
                ratHistUp[-1].GetYaxis().SetTitleFont(43)
                ratHistUp[-1].GetYaxis().SetTitleOffset(1.55)
                ratHistUp[-1].GetYaxis().SetLabelFont(43)
                ratHistUp[-1].GetYaxis().SetLabelSize(15)
                ratHistUp[-1].GetXaxis().SetTitleSize(20)
                ratHistUp[-1].GetXaxis().SetTitleFont(43)
                ratHistUp[-1].GetXaxis().SetTitleOffset(3.5)
                ratHistUp[-1].GetXaxis().SetLabelFont(43)
                ratHistUp[-1].GetXaxis().SetLabelSize(15)
                ratHistUp[-1].GetXaxis().SetTitle('MJ [GeV]')
                endInt = ratHistUp[-1].GetNbinsX()+1
                for bin in range(1,ratHistUp[-1].GetNbinsX()):
                    if nomHist.Integral(bin,endInt)!=0:
                        ratHistUp[-1].SetBinContent(bin,upHist.Integral(bin,endInt)/nomHist.Integral(bin,endInt)-1)
                    else:
                        ratHistUp[-1].SetBinContent(bin,0.0)
                ratHistUp[-1].SetMaximum(0.1)
                ratHistUp[-1].SetMinimum(-0.1)

                ratHistUp[-1].Draw('HIST')

                ratHistDown.append(downHist.Clone('ratioDown_'+str(ci)))
                ratHistDown[-1].SetFillColorAlpha(ROOT.kRed-10,1.0)
                endInt = downHist.GetNbinsX()+1
                for bin in range(1,ratHistDown[-1].GetNbinsX()):
                    if nomHist.Integral(bin,endInt) != 0:
                        ratHistDown[-1].SetBinContent(bin,downHist.Integral(bin,endInt)/nomHist.Integral(bin,endInt)-1)
                    else:
                        ratHistDown[-1].SetBinContent(bin,0)
                ratHistDown[-1].Draw('hist same')
                ratHistDown[-1].Draw('axis same')
                outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_02/'+str(dsidList[i])+'/'
                outFileName+='MJ_'+srLabs[m-2]+'_btaggging_NP'+str(j+1)
                canMJ[-1].Print(outFileName+'.pdf')
                canMJ[-1].Print(outFileName+'.png')
                canMJ[-1].Print(outFileName+'.C')
                subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_02/'+str(dsidList[i])+'/*',shell=True)
                ci+=1
   for j in range(len(systList)):
        for k in range(len(mjHistNames)):
            if i==5000 and j==j and k==k:
                nomFile = ROOT.TFile.Open(filePath+'/nominal.root')
                upFile = ROOT.TFile.Open(filePath+'/'+systList[j]+'__1up.root')
                downFile=0
                if filePath+'/'+systList[j]+'__1down.root' in fileList:
                    downFile = ROOT.TFile.Open(filePath+'/'+systList[j]+'__1down.root')
                upHist = upFile.Get(mjHistNames[k]+'_'+str(dsidList[i]))
                nomHist = nomFile.Get(mjHistNames[k]+'_'+str(dsidList[i]))
                downHist=0
                if downFile:
                    downHist = downFile.Get(mjHistNames[k]+'_'+str(dsidList[i]))
                canMJ.append(ROOT.TCanvas('can_'+str(ci),'can_'+str(ci),800,800))
                canMJ[-1].cd()
                pad1.append(ROOT.TPad('pad1_'+str(ci),'pad1_'+str(ci),0,0.2,1,1.0))
                pad1[-1].Draw()
                pad1[-1].cd()
                pad1[-1].SetLogy()

                upHist.SetLineColor(ROOT.kBlue)
                upHist.SetLineWidth(2)
                if upHist.GetNbinsX()==150:
                    upHist.Rebin(5)

                nomHist.SetLineColor(ROOT.kBlack)
                nomHist.SetFillColor(ROOT.kGray)
                nomHist.SetLineWidth(2)
                if nomHist.GetNbinsX() == 150:
                    nomHist.Rebin(5)
                    nomHist.SetMaximum(nomHist.GetMaximum()*10)
                nomHist.SetMaximum(nomHist.GetMaximum()*10)
                if downHist:
                    downHist.SetLineColor(ROOT.kRed)
                    downHist.SetLineWidth(2)
                    if downHist.GetNbinsX() == 150:
                        downHist.Rebin(5)
                legMJ.append(ROOT.TLegend(0.5,0.7,0.75,0.85))
                legMJ[-1].SetBorderSize(0)
                legMJ[-1].SetFillStyle(0)
                legMJ[-1].SetTextSize(0.04)
                legMJ[-1].AddEntry(nomHist,'nominal','f')
                if j >= 0:
                    legMJ[-1].AddEntry(upHist,systDict[systList[j]]+' +1 #sigma','f')
                if downHist:
                    legMJ[-1].AddEntry(downHist,systDict[systList[j]]+' -1 #sigma','f')

                nomHist.Draw('hist')
                nomHist.GetYaxis().SetTitleOffset(1.5)
                nomHist.GetYaxis().SetTitle('Events')
                upHist.Draw('hist same')
                if downHist:
                    downHist.Draw('hist same')
                legMJ[-1].Draw()
                ROOT.ATLASLabel(0.47,0.88,'Simulation Internal')
                lumiLatex.DrawLatexNDC(0.675,0.6,lumiString)
                lumiLatex.DrawLatexNDC(0.75,0.5,srNames[k])
                mG = str(pointDict[int(dsidList[i])][0])
                mX = str(pointDict[int(dsidList[i])][1])
                massString='#splitline{RPV10}{#splitline{m_{#tilde{g}} = '+mG+'}{m_{#tilde{#chi}} = '+mX+'}}'                
                if mX == '0':
                    massString='#splitline{RPV6}{m_{#tilde{g}} = '+mG+'}'
                lumiLatex.DrawLatexNDC(0.2,0.85,massString)
                
                canMJ[-1].cd()

                pad2.append(ROOT.TPad('pad2_'+str(ci),'pad2_'+str(ci),0,0.05,1,0.3))
                pad2[-1].SetTopMargin(0)
                pad2[-1].SetBottomMargin(0.2)
                pad2[-1].SetGridy()
                pad2[-1].Draw()
                pad2[-1].cd() 
                ratHistUp = upHist.Clone('ratioUp_'+str(ci))
                ratHistUp.SetMarkerColor(ROOT.kBlue)
                ratHistUp.SetFillColor(ROOT.kBlue-10)

                ratHistUp.GetYaxis().SetTitle('(syst-nom)/nom')
                ratHistUp.GetYaxis().SetNdivisions(505)
                ratHistUp.GetYaxis().SetTitleSize(20)
                ratHistUp.GetYaxis().SetTitleFont(43)
                ratHistUp.GetYaxis().SetTitleOffset(1.55)
                ratHistUp.GetYaxis().SetLabelFont(43)
                ratHistUp.GetYaxis().SetLabelSize(15)
                ratHistUp.GetXaxis().SetTitleSize(20)
                ratHistUp.GetXaxis().SetTitleFont(43)
                ratHistUp.GetXaxis().SetTitleOffset(3.5)
                ratHistUp.GetXaxis().SetLabelFont(43)
                ratHistUp.GetXaxis().SetLabelSize(15)
                ratHistUp.GetXaxis().SetTitle('MJ [GeV]')
                endInt = ratHistUp.GetNbinsX()+1
                for bin in range(1,ratHistUp.GetNbinsX()):
                    if nomHist.Integral(bin,endInt)!=0:
                        ratHistUp.SetBinContent(bin,upHist.Integral(bin,endInt)/nomHist.Integral(bin,endInt)-1)
                    else:
                        ratHistUp.SetBinContent(bin,0.0)
                ratHistUp.SetMaximum(0.5)
                ratHistUp.SetMinimum(-0.5)

                ratHistUp.Draw('HIST')
                if downHist:
                    ratHistDown = downHist.Clone('ratioDown_'+str(ci))
                    ratHistDown.SetFillColorAlpha(ROOT.kRed-10,1.0)
                    endInt = downHist.GetNbinsX()+1
                    for bin in range(1,ratHistDown.GetNbinsX()):
                        if nomHist.Integral(bin,endInt) != 0:
                            ratHistDown.SetBinContent(bin,downHist.Integral(bin,endInt)/nomHist.Integral(bin,endInt)-1)
                        else:
                            ratHistDown.SetBinContent(bin,0)
                    ratHistDown.Draw('hist same')
                    ratHistDown.Draw('axis same')

                subprocess.call('mkdir -p /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_02/'+str(dsidList[i]),shell=True)
                subprocess.call('chmod a+rx /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_02/'+str(dsidList[i]),shell=True)

                outFileName='/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_02/'+str(dsidList[i])+'/'
                outFileName+='MJ_'+srLabs[k]+'_'+systList[j]
                canMJ[ci].Print(outFileName+'.pdf')
                canMJ[ci].Print(outFileName+'.png')
                canMJ[ci].Print(outFileName+'.C')
                subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_02/'+str(dsidList[i])+'/*',shell=True)
                ci+=1

