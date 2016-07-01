#!/usr/bin/env python
import ROOT,subprocess
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
fileName6 = 'hists/RPV6/nominal.root'
fileName10 = 'hists/RPV10/nominal.root'

file6 = ROOT.TFile.Open(fileName6)
file10 = ROOT.TFile.Open(fileName10)

histNameList = ['h_nFatJet_presel','h_dy_presel','h_MJ_presel']
xLabList = ['n_{fat jet}','|#Delta #eta|','MJ [GeV]']

c6 = [ ROOT.TCanvas('c6_'+str(i),'c6_'+str(i),800,600) for i in range(len(histNameList)) ]
dsid6=['403605','403608']

c10 = [ ROOT.TCanvas('c10_'+str(i),'c10_'+str(i),800,600) for i in range(len(histNameList)) ]
dsid10=['403553','403555','403573']
maxVals10=[0.5,0.25,0.15]

cols=[ROOT.kRed,ROOT.kBlue,ROOT.kGreen]

legLab6 = ['m_{#tilde{g}} = 900 GeV','m_{#tilde{g}} = 1200 GeV']
leg6=ROOT.TLegend(0.7,0.65,0.9,0.85)
leg6.SetHeader('RPV6')
leg6.SetBorderSize(0)
leg6.SetFillStyle(0)
leg6.SetTextSize(0.04)

legLab10 = ['#splitline{m_{#tilde{g}} = 1000 GeV}{m_{#tilde{#chi}} = 50 GeV}',
            '#splitline{m_{#tilde{g}} = 1000 GeV}{m_{#tilde{#chi}} = 450 GeV}',
            '#splitline{m_{#tilde{g}} = 1600 GeV}{m_{#tilde{#chi}} = 450 GeV}']

leg10=ROOT.TLegend(0.65,0.38,0.9,0.88)
leg10.SetHeader('RPV10')
leg10.SetBorderSize(0)
leg10.SetFillStyle(0)
leg10.SetTextSize(0.04)

for i in range(len(histNameList)):
    c6[i].cd()
    drawn=False
    hists=[]
    for j in range(len(dsid6)):
        h=file6.Get(histNameList[i]+'_'+dsid6[j])
        h.Scale(1.0/h.Integral())
        if i > 0:
            h.Rebin(5)
        h.SetLineColor(cols[j])
        h.SetLineWidth(2)
        h.GetXaxis().SetTitle(xLabList[i])
        h.GetYaxis().SetTitle('a.u.')
        h.GetYaxis().SetTitleOffset(1.5)
        if i == 0:
            leg6.AddEntry(h,legLab6[j],'f')
        if not drawn:
            h.Draw('hist')
            drawn=True
        else:
            h.Draw('hist same')
    leg6.Draw()
    ROOT.ATLASLabel(0.5,0.85,'Simulation Internal')
    c6[i].Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalComparison/RPV6_'+histNameList[i].split('_')[1]+'.pdf')
    c6[i].Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalComparison/RPV6_'+histNameList[i].split('_')[1]+'.png')
    c6[i].Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalComparison/RPV6_'+histNameList[i].split('_')[1]+'.C')

for i in range(len(histNameList)):
    c10[i].cd()
    drawn=False
    hists=[]
    for j in range(len(dsid10)):
        h=file10.Get(histNameList[i]+'_'+dsid10[j])
        h.Scale(1/h.Integral())
        if i > 0:
            h.Rebin(5)
        h.SetLineColor(cols[j])
        h.SetLineWidth(2)
        h.GetXaxis().SetTitle(xLabList[i])
        h.GetYaxis().SetTitle('a.u.')
        h.GetYaxis().SetTitleOffset(1.5)
        if i == 0:
            leg10.AddEntry(h,legLab10[j],'f')
        if not drawn:
            h.Draw('hist')
            h.SetMaximum(maxVals10[i])
            drawn=True
        else:
            h.Draw('hist same')

    leg10.Draw()
    ROOT.ATLASLabel(0.5,0.85,'Simulation Internal')
    c10[i].Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalComparison/RPV10_'+histNameList[i].split('_')[1]+'.pdf')
    c10[i].Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalComparison/RPV10_'+histNameList[i].split('_')[1]+'.png')
    c10[i].Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalComparison/RPV10_'+histNameList[i].split('_')[1]+'.C')



c2 = ROOT.TCanvas('c2','c2',800,600)
h=file10.Get('h_MJ_5jSR_403553')
h.Rebin(5)
h.Draw('hist')
h.SetLineWidth(2)
ROOT.ATLASLabel(0.5,0.85,'Simulation Internal')
lumiLat = ROOT.TLatex()
lumiLat.DrawLatexNDC(0.5,0.75,'#int L dt = 5.8 fb^{-1}')
lumiLat.DrawLatexNDC(0.6,0.65,'RPV10')
lumiLat.DrawLatexNDC(0.6,0.55,'#splitline{m_{#tilde{g}} = 1000 GeV}{m_{#tilde{#chi}} = 50 GeV}')
lumiLat.DrawLatexNDC(0.6,0.4,'#splitline{n_{fat jet} #geq 5}{|#Delta #eta| < 1.4}')

c2.Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalComparison/RPV10_mg_1000_mX_50_MJ_m5_b9_dy14.pdf')
c2.Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalComparison/RPV10_mg_1000_mX_50_MJ_m5_b9_dy14.png')
c2.Print('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalComparison/RPV10_mg_1000_mX_50_MJ_m5_b9_dy14.C')

p=subprocess.call('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalComparison/*',shell=True)
