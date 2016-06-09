#!/usr/bin/env python
import argparse,ROOT,os,sys
parser = argparse.ArgumentParser(add_help=False, description='run histos')
parser.add_argument( '--isMC', dest='isMC',action='store_true',default=False,help='Running on MC')
parser.add_argument( '--sumWeights', dest='sumWeights',action='store_true',default=False,help='Use sum of weights as denominator')
parser.add_argument('input')
args = parser.parse_args()
i=0
denomDict = {} #dsid: denom
dsidPairs = [] #filename: dsid
if args.isMC:
    mdHistName = ''
    dsid = ''
    for line in open(args.input):
        f = ROOT.TFile.Open(line.rstrip())
        for key in f.GetListOfKeys():
            if 'MetaData_EventCount_' in key.GetName():
                mdHistName = key.GetName()
                dsid = mdHistName.split('_')[2]
        if not mdHistName:
            print 'MetaData Histogram not found. Did you use the --isMC flag for data?'
            sys.exit(1)                                
        if dsid in denomDict:
            denomDict[dsid] += f.Get(mdHistName).GetBinContent(1)
        else:
            denomDict[dsid] = f.Get(mdHistName).GetBinContent(1)
        dsidPairs.append((line.rstrip(),dsid))

else:
    for line in open(args.input):
        dsidPairs.append((line.rstrip(),1))

for p in dsidPairs:
    cmd = './RunHists '+p[0]+' output/output_'+str(i)+'.root'
    if args.isMC:
        cmd+=' '+str(denomDict[p[1]])
    else:
        f = ROOT.TFile.Open(p[0])
        initEvents = f.Get('MetaData_EventCount').GetBinContent(2)
        cmd+=' '+str(initEvents)
#    print cmd
    os.system(cmd)
    i+=1
