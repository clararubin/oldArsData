import pandas as pd

def df_of_city(x):
    city, path = x
    #print(city)
    df = pd.read_csv(path, header = 8, index_col = 0, na_values = '-')
    #df.rename(columns=lambda x: int(x[1:]), inplace=True) #relabel by ints instead of Qid
    df.dropna(how = 'all', inplace = True) #delete users who never answer anything
    df.drop(labels = 'Participant List Averages', errors = 'ignore', inplace = True) #clear weird cumulative totals
    df.insert(loc = 0, column = 'module', value = city) #add column for location
    #print(df)
    return df

def responses_df(module_list): #module_list is a list of tuples of ('module', '..\filepath.csv')
    return pd.concat(map(df_of_city, module_list), ignore_index = True)

def questions_df(filepath): #filepath is a single filepath to the questions file

    settings = {
        'index_col'        : 0,
        #'names'            : range(1,48),
        #'skiprows'         : 1,
        'na_values'        : ('-', 'none'),
    }
    
    df = pd.read_csv(filepath, **settings)
    return df.T