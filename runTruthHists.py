#!/usr/bin/env python
import argparse,ROOT,os,sys,subprocess,glob
from pointDict_xsec_nom import pointDict


parser = argparse.ArgumentParser(add_help=False, description='run histos')
parser.add_argument('input')
args = parser.parse_args()
pattern = args.input.strip('/')+'/*/data-tree/RPV_truthGrid100_TRUTH3.root'
fileList = glob.glob(pattern)
print len(fileList)
for i in range(0,626,20):
    for fileName in fileList[i:i+20]:
        dsid=fileName.split('/')[4]
        xsec=pointDict[int(dsid)]/1000.
#        cmd='./RunTruthHists '+fileName+' output/output_'+dsid+'.root '+str(xsec)+' nominal'
        cmd=['./RunTruthHists',fileName,'output/output_'+dsid+'.root',str(xsec),'nominal']
        p=subprocess.Popen(cmd)
    p.wait()

