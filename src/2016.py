import setup, graphing, common_runner, shared, outside_data_2016

reload(setup)
reload(graphing)
reload(common_runner)
reload(outside_data_2016)
reload(shared)


input_path = shared.getInputPath()

questions_filepath = input_path + 'questions2.csv'
cities =     ['Atlanta.csv', 'Chicago.csv','Los Angeles.csv', 'Miami.csv', 'Houston.csv', 'Philadelphia.csv' , 'NYC.csv', 'San Francisco.csv','DC.csv', 'Boston.csv', 'USPC 2016.csv']
file_array = [input_path + city for city in cities]
sections =   [[0,2],[3,5],[6,9],[10,13],[14,16],[17,19]]


def run16():
    graph_settings = common_runner.GraphSettings(
                        is_cumulative = True, is_percent = True)
    
    PDF_FILENAME_PREFIX = "perc psych update 2016 ARS"
    questions_data = setup.Questions_Data(questions_filepath)
    
    responses_data = setup.Responses_Data(file_array, questions_data)
    outside_data_2016.add_outside_responses(responses_data)
    if graph_settings.is_cumulative:
        responses_data.add_cumulative()
    
    common_runner.runBySection(
            PDF_FILENAME_PREFIX, sections, questions_data, responses_data, graph_settings)


run16()
