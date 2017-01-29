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
        self.qDict = {'demo':OrderedDict(),'pre':OrderedDict(), 'post':OrderedDict()}
        self.qIDs  = {}
        
        df = pd.DataFrame.from_csv(questions_filepath)
        cols = df.columns
        
        for i in cols:
           
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
        
        for j in self.qDict.keys():
            self.qIDs[j] = self.qDict[j].keys()
    
    def get(self, time, i):
        id = self.qIDs[time][i]
        ques = self.qDict[time][id]
        return ques
            

class Responses_Data:
    def __init__(self, array_files, questions_data):
        #following line checks for either / or \ in filepath because of different OS's
        #TODO: make less hacky
        tempCityNames=[((i.split('/' if '/' in i else '\\'))[-1] ) for i in array_files]
        self.cityNames=[((i.split('.'))[0] ) for i in tempCityNames]
        
        # load preByCity using qID['pre'] column names
        preByCity = [pd.DataFrame.from_csv(i, header=8).loc[:,questions_data.qIDs['pre']] for i in array_files]
        postByCity= [pd.DataFrame.from_csv(i, header=8).loc[:,questions_data.qIDs['post']] for i in array_files]
        demoByCity= [pd.DataFrame.from_csv(i, header=8).loc[:,questions_data.qIDs['demo']] for i in array_files]
    
        # regroup from byCity to byQ
        self.preAnswerByQ=[[tally_responses(cit,'pre', q_id, questions_data) for cit in preByCity] for q_id in questions_data.qIDs['pre']]
        self.postAnswerByQ=[[tally_responses(cit,'post', q_id, questions_data) for cit in postByCity] for q_id in questions_data.qIDs['post']]
        self.demoAnswerByQ=[[tally_responses(cit,'demo', q_id, questions_data) for cit in demoByCity] for q_id in questions_data.qIDs['demo']]
    
        cumuPreTally=[[sum(x) for x in zip(*[c for c in q])] for q in self.preAnswerByQ ]
        cumuPostTally=[[sum(x) for x in zip(*[c for c in q])] for q in self.postAnswerByQ ]
    
        self.cumuData = [cumuPreTally, cumuPostTally]
    

def tally_responses(inputFrame, time, q_id, questions_data):   
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