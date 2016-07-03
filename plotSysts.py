#!/usr/bin/env python
import argparse,ROOT,os,glob,sys,subprocess
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
ROOT.gStyle.SetPaintTextFormat('2.1f')

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

mjHistNames=['h_MJ_4jSR','h_MJ_5jSR','h_MJ_4jSR_b1_0','h_MJ_5jSR_b1_0']
srNames = ['4jSR','5jSR','4jSRb1','5jSRb1']
canMJ=[]
pad1=[]
pad2=[]
legMJ=[]
ci=0
for i in range(len(dsidList)):
    for j in range(len(systList)):
        for k in range(4):
            if i==0 and j==j and k ==0:
                canMJ.append(ROOT.TCanvas('canMJ_'+str(ci),'canMJ_'+str(ci),800,800))
                canMJ[ci].cd()

                pad1.append(ROOT.TPad('pad1_'+str(ci),'pad1_'+str(ci),0,0.2,1,1.0))
                pad1[ci].Draw()
                pad1[ci].cd()
                pad1[ci].SetLogy()
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
                upHist.SetLineColor(ROOT.kBlue)
                upHist.Rebin(5)

                nomHist.SetLineColor(ROOT.kBlack)
                nomHist.Rebin(5)
                nomHist.SetMaximum(nomHist.GetMaximum()*10)
                if downHist:
                    downHist.SetLineColor(ROOT.kRed)
                    downHist.Rebin(5)
                legMJ.append(ROOT.TLegend(0.5,0.7,0.75,0.85))
                legMJ[ci].SetBorderSize(0)
                legMJ[ci].SetFillStyle(0)
                legMJ[ci].SetTextSize(0.04)
                legMJ[ci].AddEntry(nomHist,'nominal','f')
                legMJ[ci].AddEntry(upHist,systList[j]+' +1 #sigma','f')
                if downHist:
                    legMJ[ci].AddEntry(downHist,systList[j]+' -1 #sigma','f')
                nomHist.Draw('hist')
                nomHist.GetYaxis().SetTitleOffset(1.5)
                nomHist.GetYaxis().SetTitle('Events')
                upHist.Draw('hist same')
                if downHist:
                    downHist.Draw('hist same')
                legMJ[ci].Draw()
                ROOT.ATLASLabel(0.5,0.88,'Simulation Internal')
                lumiLatex.DrawLatexNDC(0.6,0.6,lumiString)
                lumiLatex.DrawLatexNDC(0.7,0.5,srNames[k])
                canMJ[ci].cd()
                pad2.append(ROOT.TPad('pad2_'+str(i),'pad2_'+str(i),0,0.05,1,0.3))
                pad2[ci].SetTopMargin(0)
                pad2[ci].SetBottomMargin(0.2)
                pad2[ci].SetGridy()
                pad2[ci].Draw()
                pad2[ci].cd() 
                
                ratHistUp = upHist.Clone('ratioUp')
                ratHistUp.SetMarkerColor(ROOT.kBlue)
                ratHistUp.SetMarkerStyle(21)
                ratHistUp.GetYaxis().SetTitle('syst/nom')
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
                for bin in range(1,ratHistUp.GetNbinsX()):
                    endInt = upHist.GetNbinsX()+1
                    ratHistUp.SetBinContent(bin,upHist.Integral(bin,endInt)/nomHist.Integral(bin,endInt))
                ratHistUp.SetMaximum(1.5)
                ratHistUp.SetMinimum(0.5)
                ratHistUp.Draw('hist')
                if downHist:
                    ratHistDown = downHist.Clone('ratioDown')
                    for bin in range(1,ratHistDown.GetNbinsX()):
                        endInt = downHist.GetNbinsX()+1
                        ratHistDown.SetBinContent(bin,downHist.Integral(bin,endInt)/nomHist.Integral(bin,endInt))
                        ratHistDown.Draw('hist same')
                canMJ[ci].Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_02/'+str(ci)+'.pdf')
                subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalSysts/07_02/*.pdf',shell=True)
                ci+=1

