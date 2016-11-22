# -*- coding: utf-8 -*-

# cd /Users/clararubin/Google Drive/**synced files/Work/corrected
import os
import setup
import graphing
import shared as sh

reload(setup)
reload(graphing)
reload(sh)


# run make_subplots_each_question over each sec
def runBySection(prefix,sections,preAnswerByQ,postAnswerByQ,cityNames,cumuData,doCumu,percent,arrayFiles):    
    #sections=[sections[0]]
    #os.chdir('../../output')
    k=0
    for sec in sections:
        start = sec[0]
        end = sec[1]
        cities, pvals = graphing.make_subplots_each_question(start,end,preAnswerByQ,postAnswerByQ,cityNames,arrayFiles,prefix+sh.pdfNames[k],cumuData,doCumu,percent)
        k+=1
    return pvals