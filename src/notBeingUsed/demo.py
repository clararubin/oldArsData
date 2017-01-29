import os
import setup
import graphing
import shared as sh
from common_runner import *

reload(setup)
reload(graphing)
reload(sh)



def runDemo(yr):
    if yr==15:
        arFi = sh.arrayFiles15
        sh.QFILE=sh.QFILE15
    elif yr==16:
        arFi = sh.arrayFiles16
        sh.QFILE=sh.QFILE16
    #elif yr=="16az":
    #    arFi = [ '/Users/clararubin/Dropbox/___ARS - my copy/__ARS Mood Dis 16- AZ/Scottsdale Mood Disorders 2016.csv']
    sh.qDict,sh.qIDs = setup.import_questions() #import all basic info about questions
    print arFi
    preAnswerByQ,postAnswerByQ,cityNames,cumuData,demoAnswerByQ = setup.setupResp(arFi)
    return demoAnswerByQ,cityNames
    start=0
    end=len(sh.qIDs['demo'])-1
    doCumu=False
    percent=False
    graphing.make_subplots_each_question2(start,end,demoAnswerByQ,cityNames,arFi,"TTTTTaz.pdf",cumuData,doCumu,percent)


def printDemo(q,cnames, fname):
    f = open(fname, 'w')
    f = open(fname, 'a')
    ids = sh.qIDs['demo']
    for item in range(len(q)):
        qt = sh.qDict['demo'][ids[item]].questionText
        mc = sh.qDict['demo'][ids[item]].arrayMultipleChoices
        df = DataFrame(q[item], columns=mc, index=cnames)
        df = df.loc[(df!=0).any(1)]
        f.write("%s\n\n" % qt)
        df.to_csv(f, mode='a', header =qt)
        f.write("\n\n\n")
    f.close()