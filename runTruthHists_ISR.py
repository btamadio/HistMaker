#!/usr/bin/env python
import argparse,ROOT,os,sys,subprocess,glob
from pointDict import pointDict
parser = argparse.ArgumentParser(add_help=False, description='run histos')
parser.add_argument('input')
args = parser.parse_args()

varList = ['scup','scdw','fup','fdw','asup','asdw','pdup','pddw']
for var in varList:
    pattern = args.input.strip('/')+'/*/data-tree/RPV_'+var+'_TRUTH3.root'
    fileList = glob.glob(pattern)
    for fileName in sorted(fileList):
        dsid=int(fileName.split('/')[5])
        #check we're picking up the DSID correctly
        print dsid
        sys.exit(0)

        xsec=pointDict[dsid][2]
        cmd=['./RunTruthHists',fileName,'output/'+var+'_'+str(dsid)+'.root',str(xsec),'nominal']
        p=subprocess.call(cmd)
