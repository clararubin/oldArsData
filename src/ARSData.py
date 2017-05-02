class ARSData:
    def __init__(self, qdf, rdf):
        self.qdf = qdf
        self.rdf = rdf
    
    #def remove_demo(self):
    #    self.qdf = self.qdf[self.qdf['time'] != 'demo']
        
    def get_nondemo_topics(self):
        return self.qdf[self.qdf['time'] != 'demo']['topic'].unique()
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
        try:
            return self.choice_list(partition) + self.extra_category_names
        except KeyError:
            return self.rdf[partition].dropna().unique().tolist() + self.extra_category_names
    def get_relevant_category_names(self, partition, q_number):
        try:
            tgt = self.choice_list(partition) #TODO: make relevant
        except KeyError:
            tgt = self.rdf[self.rdf[q_number].notnull()][partition].dropna().unique().tolist()
        #####
        for i in self.extra_category_names:
            if q_number in self.outside_responses[i]:
                tgt.append(i)
        #####
        return tgt
        
    def count_responses(self, q_number, subset = None, response = None):
        df = self.rdf
        #####
        outside = 0
        #####
        if subset != None: #a subset of None means to include all categories of people
            if subset[1] == 'Cumulative':
                #####df = df[df[subset[0]].notnull()]
                return sum([self.count_responses(q_number, (subset[0], x), response)
                            for x in self.get_relevant_category_names(subset[0], q_number)])
            else:
                #####
                if subset[1] in self.extra_category_names:
                    extra = self.outside_responses[subset[1]]
                    if q_number in extra:
                        extra = extra[q_number]
                        if response == None:
                            outside = sum(extra)
                        else:
                            outside = extra[ord(response) - ord('A')]
                #####
                df = df[df[subset[0]] == subset[1]]
        if response != None: #a response on None means to include all different responses
            df = df[df[q_number] == response]
        #return df[q_number].count()
        tgt = df[q_number].count()
        return tgt + outside
    
    extra_category_names = []
    outside_responses = {}
    def add_outside_reponses(self, category_name, answer_dict):
        self.extra_category_names.append(category_name)
        self.outside_responses[category_name] = answer_dict