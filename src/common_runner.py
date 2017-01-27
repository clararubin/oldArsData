# -*- coding: utf-8 -*-

# cd /Users/clararubin/Google Drive/**synced files/Work/corrected
import os
import setup
import graphing
import pdf_name_generator

reload(setup)
reload(graphing)
reload(pdf_name_generator)

# run make_subplots_each_question over each sec
def runBySection(PDF_FILENAME_PREFIX, section_list, is_cumulative, is_percent, arrayFiles, questions_data, responses_data):    
    #sections=[sections[0]]
    #os.chdir('../../output')
    for i, sec in enumerate(section_list):
        section_iterator = iter(range(sec[0],sec[1]+1))
        
        filename = pdf_name_generator.generate_pdf_name(PDF_FILENAME_PREFIX, i+1)
        
        cities, pvals = graphing.make_subplots_each_question(
                            section_iterator, arrayFiles, filename, is_cumulative, is_percent, questions_data, responses_data
                            )
    return pvals