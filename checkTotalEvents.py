#!/usr/bin/env python
import ROOT,csv,argparse
import pyAMI.client
import pyAMI.atlas.api as AtlasAPI
from pyAMI.atlas.api import get_dataset_info
parser = argparse.ArgumentParser(add_help=False, description='print event yields')
parser.add_argument('input')
args = parser.parse_args()
totEvents = {}
numFiles = {}
runList = []
client = pyAMI.client.Client('atlas')
AtlasAPI.init()

dsNameDict = {297730:'data16_13TeV.00297730.physics_Main.merge.DAOD_EXOT3.f694_m1583_p2667',
298595:'data16_13TeV.00298595.physics_Main.merge.DAOD_EXOT3.f698_m1594_p2667',
298609:'data16_13TeV.00298609.physics_Main.merge.DAOD_EXOT3.f698_m1594_p2667',
298633:'data16_13TeV.00298633.physics_Main.merge.DAOD_EXOT3.f698_m1594_p2667',
298687:'data16_13TeV.00298687.physics_Main.merge.DAOD_EXOT3.f698_m1594_p2667',
298690:'data16_13TeV.00298690.physics_Main.merge.DAOD_EXOT3.f698_m1594_p2667',
298771:'data16_13TeV.00298771.physics_Main.merge.DAOD_EXOT3.f698_m1594_p2667',
298773:'data16_13TeV.00298773.physics_Main.merge.DAOD_EXOT3.f698_m1594_p2667',
298862:'data16_13TeV.00298862.physics_Main.merge.DAOD_EXOT3.f696_m1588_p2667',
298967:'data16_13TeV.00298967.physics_Main.merge.DAOD_EXOT3.f696_m1588_p2667',
299055:'data16_13TeV.00299055.physics_Main.merge.DAOD_EXOT3.f698_m1594_p2667',
299144:'data16_13TeV.00299144.physics_Main.merge.DAOD_EXOT3.f698_m1594_p2667',
299147:'data16_13TeV.00299147.physics_Main.merge.DAOD_EXOT3.f698_m1594_p2667',
299184:'data16_13TeV.00299184.physics_Main.merge.DAOD_EXOT3.f698_m1594_p2667',
299243:'data16_13TeV.00299243.physics_Main.merge.DAOD_EXOT3.f698_m1594_p2667',
299584:'data16_13TeV.00299584.physics_Main.merge.DAOD_EXOT3.f703_m1600_p2667',
300279:'data16_13TeV.00300279.physics_Main.merge.DAOD_EXOT3.f705_m1606_p2667',
300345:'data16_13TeV.00300345.physics_Main.merge.DAOD_EXOT3.f705_m1606_p2667',
300415:'data16_13TeV.00300415.physics_Main.merge.DAOD_EXOT3.f705_m1606_p2667',
300418:'data16_13TeV.00300418.physics_Main.merge.DAOD_EXOT3.f705_m1606_p2667',
300487:'data16_13TeV.00300487.physics_Main.merge.DAOD_EXOT3.f705_m1606_p2667',
300540:'data16_13TeV.00300540.physics_Main.merge.DAOD_EXOT3.f705_m1606_p2667',
300571:'data16_13TeV.00300571.physics_Main.merge.DAOD_EXOT3.f705_m1606_p2667',
300600:'data16_13TeV.00300600.physics_Main.merge.DAOD_EXOT3.f708_m1606_p2667',
300655:'data16_13TeV.00300655.physics_Main.merge.DAOD_EXOT3.f708_m1606_p2667',
300687:'data16_13TeV.00300687.physics_Main.merge.DAOD_EXOT3.f708_m1606_p2667',
300784:'data16_13TeV.00300784.physics_Main.merge.DAOD_EXOT3.f708_m1606_p2667',
300800:'data16_13TeV.00300800.physics_Main.merge.DAOD_EXOT3.f708_m1606_p2667',
300863:'data16_13TeV.00300863.physics_Main.merge.DAOD_EXOT3.f708_m1606_p2667',
300908:'data16_13TeV.00300908.physics_Main.merge.DAOD_EXOT3.f708_m1606_p2667'}

for line in open(args.input):
    f = ROOT.TFile.Open(line.rstrip())
    if not f:
        print 'File not found. Exiting.',f
        sys.exit(1)
    t = f.Get('outTree/nominal')
    if not t:
        print 'TTree not found. Exiting.',f
        sys.exit(1)
    nEntries = t.GetEntries()
    t.GetEntry(0)
    if t.runNumber in totEvents:
        totEvents[t.runNumber]+=nEntries
        numFiles[t.runNumber]+=1
    else:
        totEvents[t.runNumber]=nEntries
        numFiles[t.runNumber]=1
        runList.append(t.runNumber)
for run in sorted(runList):
    dsName = 'data15_13TeV.00'+str(run)+'.physics_Main.merge.DAOD_EXOT3.r7562_p2521_p2667'
    if run >= 297730:
        dsName = dsNameDict[run]
        #dsName = 'data16_13TeV.00'+str(run)+'.physics_Main.merge.DAOD_EXOT3.r7562_p2521_p2667'
    d=AtlasAPI.get_dataset_info(client,dsName)[0]
    totEventsAMI = int(d['totalEvents'])
    print 'DSID: %s, nFiles = %i, AMI = %i, NTUP = %i, diff = %i' % (run,numFiles[run],totEventsAMI,totEvents[run],totEvents[run]-totEventsAMI)
    
