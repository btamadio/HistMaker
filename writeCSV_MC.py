#!/usr/bin/env python
import ROOT,csv,argparse
parser = argparse.ArgumentParser(add_help=False, description='make CSV from root file')
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()
f = ROOT.TFile.Open(args.input)
runList = []

for key in f.GetListOfKeys():
    if 'h_cutflow' in key.GetName():
        runList.append(key.GetName().split('_')[2])

runList.sort()
with open(args.output,'wb') as csvfile:
    cwriter = csv.writer(csvfile,delimiter=',')
    cwriter.writerow(['sigmaL',
                      'sigmaL',
                      'derivation',
                      'event cleaning',
                      'trigger',
                      'pT_lead',
                      'n_fatjet==3',
                      'n_fatjet==3 && b-tag',
                      'n_fatjet==4',
                      'nfatjet==4 && b-tag',
                      'n_fatjet >= 5',
                      'n_fatjet >= 5 && b-tag'])

    for run in runList:
        h = f.Get('h_cutflow_'+run)
        row = [h.GetBinContent(i) for i in range(1,h.GetNbinsX()+1)]
        row.insert(0,'')
        row.insert(0,int(run))
        cwriter.writerow(row)
