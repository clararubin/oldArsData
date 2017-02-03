import shared as sh
from collections import OrderedDict
import pandas as pd
import numpy as np


class Question:
    def __init__(self, questionText, topic, time, correctCharacter, arrayChoices, numCol, id):
        self.questionText         = questionText
        self.correctCharacter     = correctCharacter 
        self.topic                = topic
        self.time                 = time 
        self.arrayMultipleChoices = arrayChoices
        self.numberOfChoices      = len(self.arrayMultipleChoices)
        self.id                   = id
        self.numCol               = min(100000,numCol)
        
    def __str__(self): 
        return "Question %d: %s" % self.id, self.questionText


class Questions_Data:
    def __init__(self, questions_filepath):
        self.qDict = {'demo':[], 'pre':[], 'post':[]}
        
        df = pd.DataFrame.from_csv(questions_filepath)
        cols = df.columns
        
        for i in cols: #iterates over ('Q1', 'Q2', ... )
           
            multipleChoiceAnswersArray = [
                        df.ix[k,i]
                        for k in sh.MULTIPLE_CHOICE_LETTERS
                        if df.ix[k,i] != sh.NO_RESPONSE
                        ]
            
            question = Question(
                                df.ix['question text',i], 
                                df.ix['topic',i],
                                df.ix['time',i], 
                                df.ix['correct character',i],
                                multipleChoiceAnswersArray,
                                int(df.ix['display cols',i]),
                                i
                                )
            
            self.qDict[question.time].append(question)
    
    def get(self, time, i = None):
        if i == None:
            return self.qDict[time]
        return self.qDict[time][i]
        
    def get_question_id_list(self, time):
        return map(lambda q: q.id, self.qDict[time])
            

class Responses_Data:
    def __init__(self, array_files, questions_data):
                
        #following line checks for either / or \ in filepath because of different OS's
        #TODO: make less hacky
        tempCityNames=[((i.split('/' if '/' in i else '\\'))[-1] ) for i in array_files]
        self.cityNames=[((i.split('.'))[0] ) for i in tempCityNames]
        
        ids = {
        'pre': questions_data.get_question_id_list('pre'),
        'post': questions_data.get_question_id_list('post'),
        'demo': questions_data.get_question_id_list('demo'),
        }
        
        # load preByCity using qID['pre'] column names
        data_frames = {}
        for time in ('pre', 'post', 'demo'):
            data_frames[time] = {}
            for city_name, city_file in zip(self.cityNames, array_files):
                data_frames[time][city_name] = pd.DataFrame.from_csv(city_file, header=8).loc[:,ids[time]]
    
        # regroup from byCity to byQ
        # this object will be accessed like self[time][q_index][city_name]
        # e.g. responses_data['pre'][3]['Atlanta']
        # and will return a list containing the number of occurances of each
        #    answer to that question by that city
        self.responses_by_question = {}
        for time in ('pre', 'post', 'demo'):
            self.responses_by_question[time] = []
            for i, _ in enumerate(questions_data.get(time)):
                self.responses_by_question[time].append(OrderedDict())
                for city_name, city_data_frame in data_frames[time].items():
                    self.responses_by_question[time][i][city_name] = self.tally_responses(city_data_frame, time, i, questions_data)
    
    def get(self, time, i):
        # returns an OrderedDict that is indexable by city names (strings)
        # and contains lists of integers corresposning to how many people
        # answered A/B/C/D/etc
        return self.responses_by_question[time][i]
    
    def tally_responses(self, inputFrame, time, q_index, questions_data):   
        ''' 
        Counts number of A's, B's, etc for a question.
        
        :param inputFrame: whole file's data
        :param time:       demo/pre/post, loads the proper array
        :param q_id:       which question in the category
        :returns:          array of counts for each mult choice answer
        '''
        question = questions_data.get(time, q_index)
        numberOfChoices = question.numberOfChoices
        
        if len(inputFrame) == 0:
            return np.zeros(numberOfChoices)
            
        arrayOfResponses = []
        for letter in sh.MULTIPLE_CHOICE_LETTERS[:numberOfChoices]:
            expr = '%s == "%s"' % (question.id, letter) 
            arrayOfResponses.append(inputFrame.query(expr).count()[question.id])
        return arrayOfResponses
        

