# -*- coding: utf-8 -*-
import graphing, pdf_name_generator

reload(graphing)
reload(pdf_name_generator)

def sec_iter(some_range):
    '''
    yields pairs of numbers from a range as a tuple
    if range is odd length, last number is yielded as a monuple
    e.g. sec_iter(range(2,7)) will iterate over (2,3) -> (4,5) -> (6,)
    '''
    some_range = iter(some_range)
    while True:
        x = next(some_range)
        try:
            y = next(some_range)
            yield (x,y)
        except StopIteration:
            yield (x,)
            
class GraphSettings():
    def __init__(self, is_cumulative = True, is_percent = True):
        self.is_cumulative = is_cumulative
        self.is_percent = is_percent

# run make_subplots_each_question over each sec
def runBySection(PDF_FILENAME_PREFIX, section_list, questions_data, responses_data, graph_settings):    
    for i, sec in enumerate(section_list):
        section_iterator = sec_iter(range(sec[0],sec[1]+1))
        
        PDF_FILENAME = pdf_name_generator.generate_pdf_name(PDF_FILENAME_PREFIX, i+1)
        
        graphing.make_pdf_of_section(
                            section_iterator, PDF_FILENAME, graph_settings, questions_data, responses_data
                            )