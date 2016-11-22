import os
import setup
import graphing
import shared as sh
import common_runner
import sys
sys.path.append("../../input")


reload(setup)
reload(graphing)
reload(sh)
reload(common_runner)
from common_runner import *

def run16():
    sh.QFILE=sh.QFILE16
    sh.qDict,sh.qIDs = setup.import_questions() #import all basic info about questions
    import outside_data_2016 as out16
    
    #os.chdir('/Users/clararubin/Dropbox/___ARS - my copy/___ARS 16/mycorrected')
    sh.pdfNames = sh.pdfNames16
    sh.QFILE = sh.QFILE16
    doCumu=True
    percent=True
    preAnswerByQ,postAnswerByQ,cityNames,cumuData,demoAnswerByQ = setup.setupResp(sh.arrayFiles16)
    
    cityNames+=["Medscape"]
    cityNames+=["myCME"]
    numQs = 19
    for i in range(numQs+1):
        if(i==0 or i==1 or i==2):
            preAnswerByQ[i].append(out16.kr_medsc_pre[i])
            postAnswerByQ[i].append(out16.kr_medsc_post[i])
            preAnswerByQ[i].append(out16.kr_mycme_pre[i])
            postAnswerByQ[i].append(out16.kr_mycme_post[i])
        elif(i==3 or i==4 or i==5):
            preAnswerByQ[i].append(out16.td_medsc_pre[i-3])
            postAnswerByQ[i].append(out16.td_medsc_post[i-3])
            preAnswerByQ[i].append(out16.td_mycme_pre[i-3])
            postAnswerByQ[i].append(out16.td_mycme_post[i-3])
        else:
            length= len(preAnswerByQ[i][0])
            preAnswerByQ[i].append([0]*length)
            postAnswerByQ[i].append([0]*length)
            preAnswerByQ[i].append([0]*length)
            postAnswerByQ[i].append([0]*length)
            
    #printCSV(preAnswerByQ, postAnswerByQ, cityNames, '2016data.csv')
    #printCSVpercent(preAnswerByQ, postAnswerByQ, cityNames, '2016dataPercent.csv')
    pvals = runBySection("perc ",sh.sections16,preAnswerByQ,postAnswerByQ,cityNames,cumuData,doCumu,percent,sh.arrayFiles16)
    return preAnswerByQ,postAnswerByQ,pvals #,demoAnswerByQ




def runAZ16():
    files =[ '/Users/clararubin/Dropbox/___ARS - my copy/__ARS Mood Dis 16- AZ/Scottsdale Mood Disorders 2016.csv']
    msections=[[0, 2], [3, 5], [6, 8], [9, 11], [12, 14], [15, 17], [18, 20], [21, 23], [24, 26], [27, 29], [30, 32]]
    doCumu=False
    percent=False
    preAnswerByQ,postAnswerByQ,cityNames,cumuData,demoAnswerByQ = setup.setupResp(files)
    runBySection("", msections,preAnswerByQ,postAnswerByQ,cityNames,cumuData,doCumu,percent,files)


run16()
