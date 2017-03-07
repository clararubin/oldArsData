import csv_parser, graphing, common_runner, shared, ARSData#, outside_data_2016

reload(csv_parser)
reload(graphing)
reload(common_runner)
#reload(outside_data_2016)
reload(shared)
reload(ARSData)


input_path = shared.getInputPath()
questions_filepath = input_path + 'questions2.csv'
cities =     ['Atlanta', 'Chicago','Los Angeles', 'Miami', 'Houston', 'Philadelphia' , 'NYC', 'San Francisco','DC', 'Boston', 'USPC 2016']
filepaths = [input_path + city + ".csv" for city in cities]
sections =   ([0,2],[3,5],[6,9],[10,13],[14,16],[17,19])


def run16():
    graph_settings = common_runner.GraphSettings(
                        is_cumulative = True, is_percent = True, partition = 'module')
    
    PDF_FILENAME_PREFIX = "perc psych update 2016 ARS"
    qdf = csv_parser.questions_df(questions_filepath)
    
    rdf = csv_parser.responses_df(zip(cities,filepaths))
    
    data = ARSData.ARSData(qdf, rdf)
    
    common_runner.runBySection(
            PDF_FILENAME_PREFIX, sections, data, graph_settings)


run16()
