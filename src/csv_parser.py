import pandas as pd

def df_of_city(x):
    city, path = x
    
    #turn csv into a pandas dataframe, with appropriate offsets for reading data
    df = pd.read_csv(path, header = 8, index_col = 0, na_values = '-')
    
    #delete users who never answer anything
    df.dropna(how = 'all', inplace = True)
    
    #clear weird cumulative totals some files have
    df.drop(labels = 'Participant List Averages', errors = 'ignore', inplace = True) 
    
    #add column for location
    df.insert(loc = 0, column = 'module', value = city) 
    
    return df

def responses_df(module_list): #module_list is a list of tuples of ('module', '..\filepath.csv')
    return pd.concat(map(df_of_city, module_list), ignore_index = True)

def questions_df(filepath): #filepath is a single filepath to the questions file

    settings = {
        'index_col'        : 0,
        'na_values'        : ('-', 'none'),
    }
    
    df = pd.read_csv(filepath, **settings)
    return df.T