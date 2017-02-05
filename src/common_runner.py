# -*- coding: utf-8 -*-
import graphing, pdf_name_generator

reload(graphing)
reload(pdf_name_generator)

def sec_iter(endpoints, questions_data, responses_data):
    if len(endpoints) != 2:
        raise ValueError("endpoints must have length 2")
    for i in range(endpoints[0], endpoints[1]+1):
        question_pair = {'pre': questions_data.get('pre', i),
                        'post': questions_data.get('post', i)}
        response_pair = {'pre': responses_data.get('pre', i),
                        'post': responses_data.get('post', i)}
        yield {'question_pair': question_pair, 'response_pair': response_pair}
            
class GraphSettings():
    def __init__(self, is_cumulative = True, is_percent = True):
        self.is_cumulative = is_cumulative
        self.is_percent = is_percent

def runBySection(PDF_FILENAME_PREFIX, section_list, questions_data, responses_data, graph_settings):    
    for i, section_endpoints in enumerate(section_list):
        
        section_iterator = sec_iter(section_endpoints, questions_data, responses_data)
        PDF_FILENAME = pdf_name_generator.generate_pdf_name(PDF_FILENAME_PREFIX, i+1)
        
        print("~~~~~~~~~~~~~~~~~")
        print("\n\n\nPreparing PDF #%d:" % (i+1))
        print("    %s" % PDF_FILENAME)
        print("~~~~~~~~~~~~~~~~~")
        
        graphing.make_pdf_of_section(
                            section_iterator, PDF_FILENAME, graph_settings
                            )