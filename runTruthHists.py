#!/usr/bin/env python
import argparse,ROOT,os,sys,subprocess,glob
from pointDictTruth import pointDictTruth

parser = argparse.ArgumentParser(add_help=False, description='run histos')
parser.add_argument('input')
args = parser.parse_args()
pattern = args.input.strip('/')+'/*/data-tree/RPV_truthGrid100_TRUTH3.root'
fileList = glob.glob(pattern)
for fileName in sorted(fileList):
    dsid=int(fileName.split('/')[4])
    if dsid > 404250:
        xsec=pointDictTruth[dsid][2]
#        cmd='./RunTruthHists '+fileName+' output/output_'+dsid+'.root '+str(xsec)+' nominal'
        cmd=['./RunTruthHists',fileName,'output/output_'+str(dsid)+'.root',str(xsec),'nominal']
        p=subprocess.Popen(cmd)
#        p.wait()
