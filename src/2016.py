import sys
sys.path.append("../../input")
sys.path.append("../../output")
import setup
import graphing
import common_runner
import outside_data_2016 as out16
import os

reload(setup)
reload(graphing)
reload(common_runner)
reload(out16)


input_path = '..\..\input\\'

#check if running on Mac
if(os.name == 'posix'): 
    input_path = '../../input/'

questions_filepath = input_path + 'questions2.csv'
cities =     ['Atlanta.csv', 'Chicago.csv','Los Angeles.csv', 'Miami.csv', 'Houston.csv', 'Philadelphia.csv' , 'NYC.csv', 'San Francisco.csv','DC.csv', 'Boston.csv', 'USPC 2016.csv']
file_array = [ input_path + (city) for city in cities]
sections =   [[0,2],[3,5],[6,9],[10,13],[14,16],[17,19]]



def run16():
    PDF_FILENAME_PREFIX = "perc psych update 2016 ARS"
    
    questions_data = setup.Questions_Data(questions_filepath)
    
    responses_data = setup.Responses_Data(file_array, questions_data)
    out16.add_outside_responses(responses_data)
    
    is_cumulative = True
    is_percent = True    
    
    print(responses_data.cityNames)
    
    common_runner.runBySection(
            PDF_FILENAME_PREFIX, sections, is_cumulative, is_percent, file_array, questions_data, responses_data)


run16()
