import os
import setup
import graphing
import shared as sh
from common_runner import *

reload(setup)
reload(graphing)
reload(sh)

#doCumu=False
#percent=False
#runBySection("abs ",sh.sections15)
#

def run15():
    sh.QFILE=sh.QFILE15
    sh.qDict,sh.qIDs = setup.import_questions() #import all basic info about questions
    os.chdir('/Users/clararubin/Dropbox/___ARS - my copy/__ARS 15/corrected')
    print os.getcwd()
    sh.pdfNames = sh.pdfNames15
    sh.QFILE=sh.QFILE15
    doCumu=False
    percent=True
    preAnswerByQ,postAnswerByQ,cityNames,cumuData,demoAnswerByQ = setup.setupResp(sh.arrayFiles15)
    import outside_data_2015 as out15


    cityNames+=["Medscape"]
    cityNames+=["myCME"]
    cityNames+=["fCME/CMEU"]
    cityNames+=["Cumulative"]
    for i in range(25):
        #print i
        if(i<4):
            length= len(preAnswerByQ[i][0])
            preAnswerByQ[i].append(out15.bp_medsc_pre[i])
            postAnswerByQ[i].append(out15.bp_medsc_post[i])
            preAnswerByQ[i].append(out15.bp_mycme_pre[i])
            postAnswerByQ[i].append(out15.bp_mycme_post[i])
        elif(i==16 or i==17):
            preAnswerByQ[i].append(out15.cog_medsc_pre[i-16])
            postAnswerByQ[i].append(out15.cog_medsc_post[i-16])
            preAnswerByQ[i].append(out15.cog_mycme_pre[i-16])
            postAnswerByQ[i].append(out15.cog_mycme_post[i-16])
        elif(i==19 or i==20):
            preAnswerByQ[i].append(out15.cog_medsc_pre[i-17])
            postAnswerByQ[i].append(out15.cog_medsc_post[i-17])
            preAnswerByQ[i].append(out15.cog_mycme_pre[i-17])
            postAnswerByQ[i].append(out15.cog_mycme_post[i-17])
        else:
            length= len(preAnswerByQ[i][0])
            preAnswerByQ[i].append([0]*length)
            preAnswerByQ[i].append([0]*length)
            postAnswerByQ[i].append([0]*length)  
            postAnswerByQ[i].append([0]*length)  
        #add each cmeuq
        preAnswerByQ[i].append(out15.cmeu_pre[i])
        postAnswerByQ[i].append(out15.cmeu_post[i])
        cumuPre = [sum(x) for x in zip(*preAnswerByQ[i])]
        cumuPost = [sum(x) for x in zip(*postAnswerByQ[i])]
        preAnswerByQ[i].append(cumuPre)
        postAnswerByQ[i].append(cumuPost)
        
        del(preAnswerByQ[i][17])
    #    del(preAnswerByQ[i][16])
        del(postAnswerByQ[i][17])
    #    del(postAnswerByQ[i][16])
    del(cityNames[17])
    #del(cityNames[16])
    print(cityNames)
    print(len(preAnswerByQ[0]))
    print(len(postAnswerByQ[0]))
    print(len(cityNames))
    #printCSV(preAnswerByQ, postAnswerByQ, cityNames, '2015data.csv')
    #printCSVpercent(preAnswerByQ, postAnswerByQ, cityNames, '2015dataPercent.csv')
    runBySection("perc ",sh.sections15,preAnswerByQ,postAnswerByQ,cityNames,cumuData,doCumu,percent,sh.arrayFiles15)
    #return (cityNames, preAnswerByQ)
