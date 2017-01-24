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
def runBySection(prefix, pdf_filenames, sections, preAnswerByQ,postAnswerByQ,cityNames,cumuData,doCumu,percent,arrayFiles):    
    #sections=[sections[0]]
    #os.chdir('../../output')
    for i, sec in enumerate(sections):
        start = sec[0]
        end = sec[1]
        filename = prefix + "__" + pdf_filenames[i]
        cities, pvals = graphing.make_subplots_each_question(
                            start, end, preAnswerByQ ,postAnswerByQ,
                            cityNames, arrayFiles, filename,
                            cumuData, doCumu, percent
                            )
    return pvals