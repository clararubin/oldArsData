class ARSData:
    def __init__(self, qdf, rdf):
        self.qdf = qdf
        self.rdf = rdf
    
    def remove_demo(self):
        self.qdf = self.qdf[self.qdf['time'] != 'demo']
        
    def get_topics(self):
        return self.qdf['topic'].unique()
    def get_pres_of_topic(self, topic):
        return self.qdf[self.qdf['topic'] == topic][self.qdf['time'] == 'pre'].index.tolist()
    def pre_post_of_pre(self, number):
        return self.qdf[self.qdf['question text'] == self.qdf.ix[number, 'question text']].index.tolist()
    def legend_columns(self, q_number):
        return int(self.qdf.ix[q_number, 'display cols'])
    def correct_character(self, q_number):
        return self.qdf.ix[q_number, 'correct character']
    def choice_list(self, q_number):
        return self.qdf.ix[q_number, 'A':].dropna().index.tolist()
    def answer_list(self, q_number):
        return self.qdf.ix[q_number, 'A':].dropna().tolist()
    def number_of_choices(self, q_number):
        return self.qdf.ix[q_number, 'A':].count()
    def get_question_text(self, q_number):
        return self.qdf.ix[q_number, 'question text']
        
    def get_category_names(self, partition):
        return self.rdf[partition].dropna().unique()
    def get_relevant_category_names(self, partition, q_number):
        return self.rdf[self.rdf[q_number].notnull()][partition].dropna().unique()
        
    def count_responses(self, q_number, subset = None, response = None):
        df = self.rdf
        if subset != None:
            if subset[1] == 'Cumulative':
                df = df[df[subset[0]].notnull()]
            else:
                df = df[df[subset[0]] == subset[1]]
        if response != None:
            df = df[df[q_number] == response]
        return df[q_number].count()