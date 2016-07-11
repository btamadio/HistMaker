#!/usr/bin/env python
import os
from massDict import massDict
i = 0
for mG in range(1000,2000,50):
    for mX in range(50,mG,50):
        runNumber = 403615+i
        i+=1
        if mG in massDict:
            cmd='echo "'+str(runNumber)+': ('+str(mG)+','+str(mX)+','+str(massDict[mG][0])+','+str(massDict[mG][1])+'),">>pointDictTruth.py'
            os.system(cmd)
print runNumber
i = 0
for mG in range(800,1000,50):
    for mX in range(50,mG,50):
        runNumber = 404185+i
        i+=1
        if mG in massDict:
            cmd='echo "'+str(runNumber)+': ('+str(mG)+','+str(mX)+','+str(massDict[mG][0])+','+str(massDict[mG][1])+'),">>pointDictTruth.py'
            os.system(cmd)
