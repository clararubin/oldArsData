# -*- coding: utf-8 -*-
import graphing, pdf_name_generator

reload(graphing)
reload(pdf_name_generator)
            
class GraphSettings():
    def __init__(self, is_cumulative, is_percent, partition):
        self.is_cumulative = is_cumulative
        self.is_percent = is_percent
        self.partition = partition

def runBySection(PDF_FILENAME_PREFIX, section_list, data, graph_settings):
    data.remove_demo()
    for i, topic in enumerate(data.get_topics()):        

        PDF_FILENAME = pdf_name_generator.generate_pdf_name(PDF_FILENAME_PREFIX, i+1)
        
        print("\n~~~~~~~~~~~~~~~~~")
        print("Preparing PDF #%d: %s" % (i+1, PDF_FILENAME))
        print("~~~~~~~~~~~~~~~~~\n")
        
        graphing.make_pdf_of_section(
                            PDF_FILENAME, data, topic, graph_settings
                            )