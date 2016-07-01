#!/usr/bin/env python
import subprocess
treeNameList = ['nominal',
                'JET_EtaIntercalibration_NonClosure__1up',
                'JET_EtaIntercalibration_NonClosure__1down',
                'JET_RelativeNonClosure_AFII__1down',
                'JET_RelativeNonClosure_AFII__1up',
                'JET_Rtrk_Baseline_All__1up',
                'JET_Rtrk_Baseline_All__1down',
                'JET_Rtrk_Modelling_All__1up',
                'JET_Rtrk_Modelling_All__1down',
                'JET_Rtrk_TotalStat_All__1up',
                'JET_Rtrk_TotalStat_All__1down',
                'JET_Rtrk_Tracking_All__1up',
                'JET_Rtrk_Tracking_All__1down',
                'JET_GroupedNP_1__1up',
                'JET_GroupedNP_1__1down',
                'JET_GroupedNP_2__1up',
                'JET_GroupedNP_2__1down',
                'JET_GroupedNP_3__1up',
                'JET_GroupedNP_3__1down',
                'JET_JER_SINGLE_NP__1up',
                'JMR_Smear__1up']

fileList =  '/global/homes/s/sambt/workarea/RPV_2/files/RPV6_JMR_files.txt'
for treeName in treeNameList:
    cmdList = ['./runHists.py',fileList,treeName]
    p=subprocess.call(cmdList)
for treeName in treeNameList:
    p=subprocess.call('mkdir -p hists/RPV6',shell=True)
    p=subprocess.call('hadd hists/RPV6/'+treeName+'.root output/'+treeName+'/*.root',shell=True)
p = subprocess.call('rm -r output/*',shell=True)

fileList = '/global/homes/s/sambt/workarea/RPV_2/files/RPV10_JMR_files.txt'
for treeName in treeNameList:
    cmdList = ['./runHists.py',fileList,treeName]
    p=subprocess.call(cmdList)
for treeName in treeNameList:
    p=subprocess.call('mkdir -p hists/RPV10',shell=True)
    p=subprocess.call('hadd hists/RPV10/'+treeName+'.root output/'+treeName+'/*.root',shell=True)
p = subprocess.call('rm -r output/*',shell=True)
