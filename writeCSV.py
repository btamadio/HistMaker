#!/usr/bin/env python
import ROOT,csv,argparse
import pyAMI.client
import pyAMI.atlas.api as AtlasAPI
from pyAMI.atlas.api import get_dataset_info

parser = argparse.ArgumentParser(add_help=False, description='make CSV from root file')
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()
f = ROOT.TFile.Open(args.input)
runList = []
client = pyAMI.client.Client('atlas')
AtlasAPI.init()

for key in f.GetListOfKeys():
    if 'h_cutflow' in key.GetName():
        runList.append(key.GetName().split('_')[2])

runList.sort()
with open(args.output,'wb') as csvfile:
    cwriter = csv.writer(csvfile,delimiter=',')
    cwriter.writerow(['run',
                      'luminosity',
                      'CBC selected',
                      'Initial',
                      'GRL',
                      'event cleaning',
                      'trigger',
                      'pT_lead',
                      'n_fatjet==3',
                      'n_fatjet==3 && b-tag',
                      'n_fatjet==4 && MJ < 600',
                      'nfatjet==4 && MJ < 600 && b-tag',
                      'n_fatjet >= 5 && MJ < 600',
                      'n_fatjet >= 5 && MJ < 600 && b-tag'])

    for run in runList:
        h = f.Get('h_cutflow_'+run)
        row = [h.GetBinContent(i) for i in range(1,h.GetNbinsX()+1)]
        row.insert(0,'')
        row.insert(0,int(run))
        dsName = 'data15_13TeV.00'+run+'.physics_Main.merge.DAOD_EXOT3.r7562_p2521_p2614'
        d=AtlasAPI.get_dataset_info(client,dsName)[0]
        totalEvents = int(d['totalEvents'])
        print 'DSID: %s, AMI = %i, CBC = %i, Initial = %i' % (run,totalEvents,row[2],row[3])
        cwriter.writerow(row)
