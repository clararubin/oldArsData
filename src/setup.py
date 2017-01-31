import shared as sh
from collections import OrderedDict
import pandas as pd
import numpy as np


class Question:
    def __init__(self, questionText, topic, time, correctCharacter, arrayChoices,numCol,id):
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
        self.qDict = {'demo':OrderedDict(), 'pre':OrderedDict(), 'post':OrderedDict()}
        
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
            
            self.qDict[question.time][question.id] = question
    
    def get(self, time, i):
        question_id = self.get_question_id_list(time)[i]
        return self.qDict[time][question_id]
        
    def get_question_id_list(self, time):
        return self.qDict[time].keys()
            

class Responses_Data:
    def __init__(self, array_files, questions_data):
        #following line checks for either / or \ in filepath because of different OS's
        #TODO: make less hacky
        tempCityNames=[((i.split('/' if '/' in i else '\\'))[-1] ) for i in array_files]
        self.cityNames=[((i.split('.'))[0] ) for i in tempCityNames]
        
        pre_ids = questions_data.get_question_id_list('pre')
        post_ids = questions_data.get_question_id_list('post')
        demo_ids = questions_data.get_question_id_list('demo')
        
        # load preByCity using qID['pre'] column names
        preByCity = [pd.DataFrame.from_csv(i, header=8).loc[:,pre_ids] for i in array_files]
        postByCity= [pd.DataFrame.from_csv(i, header=8).loc[:,post_ids] for i in array_files]
        demoByCity= [pd.DataFrame.from_csv(i, header=8).loc[:,demo_ids] for i in array_files]
    
        # regroup from byCity to byQ
        self.preAnswerByQ=[[self.tally_responses(cit,'pre', q_id, questions_data) for cit in preByCity] for q_id in pre_ids]
        self.postAnswerByQ=[[self.tally_responses(cit,'post', q_id, questions_data) for cit in postByCity] for q_id in post_ids]
        self.demoAnswerByQ=[[self.tally_responses(cit,'demo', q_id, questions_data) for cit in demoByCity] for q_id in demo_ids]
    
        cumuPreTally=[[sum(x) for x in zip(*[c for c in q])] for q in self.preAnswerByQ ]
        cumuPostTally=[[sum(x) for x in zip(*[c for c in q])] for q in self.postAnswerByQ ]
    
        self.cumuData = [cumuPreTally, cumuPostTally]
    
    def tally_responses(self, inputFrame, time, q_id, questions_data):   
        ''' 
        Counts number of A's, B's, etc for a question.
        
        :param inputFrame: whole file's data
        :param time:       demo/pre/post, loads the proper array
        :param q_id:       which question in the category
        :returns:          array of counts for each mult choice answer
        '''
        numberOfChoices = (questions_data.qDict[time][q_id]).numberOfChoices
        
        if len(inputFrame) == 0:
            return np.zeros(numberOfChoices)
            
        arrayOfResponses = []
        for letter in sh.MULTIPLE_CHOICE_LETTERS[:numberOfChoices]:
            expr = '%s == "%s"' % (q_id, letter) 
            arrayOfResponses.append(inputFrame.query(expr).count()[q_id])
        return arrayOfResponses
        

