#!/usr/bin/env python
import argparse,ROOT,os,sys,subprocess,glob
from pointDict import pointDict
from pointDictTruth import pointDictTruth

parser = argparse.ArgumentParser(add_help=False, description='run histos')
parser.add_argument('input')
args = parser.parse_args()
nFiles=15
#varList = ['scup','scdw','fup','fdw','asup','asdw','pdup','pddw','truthGrid100']
varList = ['asup']
for var in varList:
    pattern = args.input.strip('/')+'/'+var+'/*/data-tree/RPV_'+var+'_TRUTH3.root'
    fileList = glob.glob(pattern)
    print fileList
    for i in range(0,len(fileList),nFiles):
        for fileName in fileList[i:min(i+nFiles,len(fileList))]:
            dsid=int(fileName.split('/')[5])
            xsec = 1
            if dsid in pointDict:
                xsec=pointDict[dsid][2]
            elif dsid in pointDictTruth:
                xsec=pointDictTruth[dsid][2]
            else:
                print 'DSID %i not found' % dsid
                sys.exit(1)
            cmd=['./RunTruthHists',fileName,'output/'+var+'_'+str(dsid)+'.root',str(xsec),'nominal']
            p=subprocess.Popen(cmd)
        p.wait()
