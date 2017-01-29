# -*- coding: utf-8 -*-
import graphing, pdf_name_generator

reload(graphing)
reload(pdf_name_generator)

# run make_subplots_each_question over each sec
def runBySection(PDF_FILENAME_PREFIX, section_list, questions_data, responses_data, is_cumulative = True, is_percent = True):    
    for i, sec in enumerate(section_list):
        section_iterator = iter(range(sec[0],sec[1]+1))
        
        PDF_FILENAME = pdf_name_generator.generate_pdf_name(PDF_FILENAME_PREFIX, i+1)
        
        cities, pvals = graphing.make_subplots_each_question(
                            section_iterator, PDF_FILENAME, is_cumulative, is_percent, questions_data, responses_data
                            )
    return pvals