#!/usr/bin/env python
import ROOT,sys
from pprint import pprint
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
fullSimFile = ROOT.TFile.Open(sys.argv[1])
fastSimFile = ROOT.TFile.Open(sys.argv[2])
dsid = sys.argv[3]
labelDict = {'403558':'#splitline{m_{#tilde{g}} = 1.6 TeV}{m_{#tilde{#chi}} = 50 GeV}',
'403560':'#splitline{m_{#tilde{g}} = 1.6 TeV}{m_{#tilde{#chi}} = 450 GeV}',
'403563':'#splitline{m_{#tilde{g}} = 1.6 TeV}{m_{#tilde{#chi}} = 1050 GeV}'}
labList = ['','','','','','#splitline{n_{fatjet} #geq 5}{b-tag}','#splitline{#splitline{n_{fatjet} #geq 5}{b-tag}}{|#Delta#eta| < 1.4}',
'#splitline{n_{fatjet} #geq 5}{b-inc}','#splitline{#splitline{n_{fatjet} #geq 5}{b-inc}}{|#Delta#eta| < 1.4}']
labLatex = ROOT.TLatex()
histNames = ['h_fatjet_pt',
             'h_fatjet_eta',
             'h_fatjet_phi',
             'h_fatjet_m',
             'h_fatjet_nTrimSubjets',
             'h_MJ_m5_b1',
             'h_MJ_m5_b1_dy14',
             'h_MJ_m5_b9',
             'h_MJ_m5_b9_dy14']

c = [ ROOT.TCanvas('c'+str(i),'c'+str(i),800,800) for i in range(len(histNames))]
pad1 = []
pad2 = []
axis=[]
leg = ROOT.TLegend(0.7,0.8,0.85,0.9)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.04)

fullSimHists=[]
fastSimHists=[]
ratioHists = []
for i in range(len(histNames)):
    fullSimHists.append(fullSimFile.Get(histNames[i]+'_'+dsid))
    fastSimHists.append(fastSimFile.Get(histNames[i]+'_'+dsid))
    print histNames[i]+'_'+dsid
    if i == 0:
        leg.AddEntry(fullSimHists[i],'FullSim','pl')
        leg.AddEntry(fastSimHists[i],'AFII','pl')
    c[i].cd()
    pad1.append(ROOT.TPad('pad1_'+str(i),'pad1_'+str(i),0,0.2,1,1.0))
    pad1[i].Draw()
    pad1[i].cd()
    fullSimHists[i].SetLineColor(ROOT.kRed)
    fullSimHists[i].SetMarkerColor(ROOT.kRed)
    fullSimHists[i].SetMarkerStyle(20)
    if i<5:
        fullSimHists[i].GetYaxis().SetTitle('fraction of jets')
    else:
        fullSimHists[i].GetYaxis().SetTitle('Events')
    maxMult=1.2
    if i == 0:
        pad1[i].SetLogy()
        maxMult=10
    if i >= 5:
        fullSimHists[i].Rebin(10)
        fastSimHists[i].Rebin(10)
        fastSimHists[i].GetXaxis().SetTitle('MJ [GeV]')
        fastSimHists[i].GetYaxis().SetTitle('Events')
    fullSimHists[i].GetYaxis().SetTitleOffset(1.4)
    fastSimHists[i].SetLineColor(ROOT.kBlue)
    fastSimHists[i].SetMarkerColor(ROOT.kBlue)
    fastSimHists[i].SetMarkerStyle(20)
#    fullSimHists[i].Sumw2()
#    fastSimHists[i].Sumw2()
    if fullSimHists[i].Integral() != 0 and i!=5:
        fullSimHists[i].Scale(1./fullSimHists[i].Integral())
    if fastSimHists[i].Integral() != 0 and i!=5:
        fastSimHists[i].Scale(1./fastSimHists[i].Integral())
    fullSimHists[i].GetXaxis().SetLabelSize(0)
    fullSimHists[i].Draw('ehist')
    if i == 3:
        fullSimHists[i].GetXaxis().SetRangeUser(0,300)
    fastSimHists[i].Draw('ehist same')
    if fastSimHists[i].GetMaximum() > fullSimHists[i].GetMaximum():
        fullSimHists[i].SetMaximum(fastSimHists[i].GetMaximum()*maxMult)
    else:
        fullSimHists[i].SetMaximum(fullSimHists[i].GetMaximum()*maxMult)
    leg.Draw()
    label = ROOT.ATLASLabel(0.2,0.85,'Internal')
    labLatex.DrawLatexNDC(0.7,0.6,labelDict[dsid])
    labLatex.DrawLatexNDC(0.5,0.6,labList[i])
    c[i].cd()
    pad2.append(ROOT.TPad('pad2_'+str(i),'pad2_'+str(i),0,0.05,1,0.3))
    pad2[i].SetTopMargin(0)
    pad2[i].SetBottomMargin(0.2)
    pad2[i].SetGridy()
    pad2[i].Draw()
    pad2[i].cd() 
    ratioHists.append(fastSimHists[i].Clone('ratio_'+str(i)))
    if i >= 5:
        nBins = fastSimHists[i].GetNbinsX()
        for bin in range(1,nBins):
            num = fastSimHists[i].Integral(bin,nBins)
            den = fullSimHists[i].Integral(bin,nBins)
#            print bin,fullSimHists[i].GetBinLowEdge(bin),num,den,num/den
#            print ratioHists[i].GetBinLowEdge(bin),ratioHists[i].GetBinContent(bin)
            ratioHists[i].SetBinContent(bin,num/den)
            
            
    ratioHists[i].SetLineColor(ROOT.kBlack)
    ratioHists[i].SetMarkerColor(ROOT.kBlack)
    if i < 5:
        ratioHists[i].Divide(fullSimHists[i])
    ratioHists[i].SetMarkerStyle(21)
    if i < 5:
        ratioHists[i].SetMaximum(2)
        ratioHists[i].SetMinimum(0)
        ratioHists[i].Draw()
    else:
        ratioHists[i].SetMaximum(1.1)
        ratioHists[i].SetMinimum(0.9)
        ratioHists[i].Draw('hist')
    if i == 3:
        ratioHists[i].GetXaxis().SetRangeUser(0,300)
    ratioHists[i].GetYaxis().SetTitle('AFII/FullSim')
    ratioHists[i].GetYaxis().SetNdivisions(505)
    ratioHists[i].GetYaxis().SetTitleSize(20)
    ratioHists[i].GetYaxis().SetTitleFont(43)
    ratioHists[i].GetYaxis().SetTitleOffset(1.55)
    ratioHists[i].GetYaxis().SetLabelFont(43)
    ratioHists[i].GetYaxis().SetLabelSize(15)
    ratioHists[i].GetXaxis().SetTitleSize(20)
    ratioHists[i].GetXaxis().SetTitleFont(43)
    ratioHists[i].GetXaxis().SetTitleOffset(3.5)
    ratioHists[i].GetXaxis().SetLabelFont(43)
    ratioHists[i].GetXaxis().SetLabelSize(15)
    if i < 5:
        ratioHists[i].GetXaxis().SetTitle(fullSimHists[i].GetTitle())
    else:
        ratioHists[i].GetXaxis().SetTitle('MJ [GeV]')
    c[i].Update()
    if i < 10:
        c[i].Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/AFII_FullSim_Comparison/RPV/'+dsid+'/0'+str(i)+'_'+histNames[i]+'.pdf')
    else:
        c[i].Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/AFII_FullSim_Comparison/RPV/'+dsid+'/'+str(i)+'_'+histNames[i]+'.pdf')
