import csv_parser, graphing, shared, ARSData#, outside_data_2016

reload(csv_parser)
reload(graphing)
#reload(outside_data_2016)
reload(shared)
reload(ARSData)


input_path = shared.getInputPath()
PDF_FILENAME_PREFIX = "perc psych update 2016 ARS"
questions_filepath = input_path + 'questions2.csv'
cities =     ['Atlanta', 'Chicago', 'Los Angeles', 'Miami', 'Houston', 'Philadelphia', 'NYC', 'San Francisco', 'DC', 'Boston', 'USPC 2016']
filepaths = [input_path + city + ".csv" for city in cities]
#sections =   ([0,2],[3,5],[6,9],[10,13],[14,16],[17,19])
degree_map = {'A':'MD', 'B':'DO', 'C':'RN', 'D':'NP', 'E':'PA', 'F':'PhD', 'G':'Other'}


def run16():
    graph_settings = graphing.GraphSettings(
                        is_cumulative = True,
                        is_percent = True,
                        partition = 'module',
                        )
   
    #Uncomment the following to graph by degree instead of by city
    #            
    #graph_settings = graphing.GraphSettings(
    #                    is_cumulative = True,
    #                    is_percent = True,
    #                    partition = 'Q3',
    #                    category_map = degree_map
    #                    )

    qdf = csv_parser.questions_df(questions_filepath)
    
    rdf = csv_parser.responses_df(zip(cities,filepaths))
    
    data = ARSData.ARSData(qdf, rdf)
    
    graphing.make_pdfs(
            PDF_FILENAME_PREFIX, data, graph_settings)


run16()
