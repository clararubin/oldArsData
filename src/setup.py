import shared as sh
from collections import OrderedDict
import pandas as pd
import numpy as np

#******************************
#********* SETUP **************
#******************************



def import_questions(questions_filepath):
    sh.qDict={'demo':OrderedDict(),'pre':OrderedDict(), 'post':OrderedDict()}
    sh.qIDs={}
    print(questions_filepath)
    importedDataFrame = pd.DataFrame.from_csv(questions_filepath)
    cols = importedDataFrame.columns
    for i in cols:
        multipleChoiceAnswersArray = [
                    importedDataFrame.ix[k,i]
                    for k in sh.MULTIPLE_CHOICE_LETTERS
                    if importedDataFrame.ix[k,i] != sh.NO_RESPONSE
                    ]
        question = sh.Question( importedDataFrame.ix['question text',i], 
                                importedDataFrame.ix['topic',i],
                                importedDataFrame.ix['time',i], 
                                importedDataFrame.ix['correct character',i],
                                multipleChoiceAnswersArray,
                                int(importedDataFrame.ix['display cols',i]),
                                i)
        sh.qDict[question.time][question.id] = question
    for j in sh.qDict.keys():
          sh.qIDs[j]=sh.qDict[j].keys() 
    return sh.qDict, sh.qIDs

def responses_init(arrayFiles):
       
    tempCityNames=[((i.split('/'))[-1] ) for i in arrayFiles]
    cityNames=[((i.split('.'))[0] ) for i in tempCityNames]
       
    # load preByCity using qID['pre'] column names
    preByCity = [pd.DataFrame.from_csv(i, header=8).loc[:,sh.qIDs['pre']] for i in arrayFiles]
    postByCity= [pd.DataFrame.from_csv(i, header=8).loc[:,sh.qIDs['post']] for i in arrayFiles]
    demoByCity= [pd.DataFrame.from_csv(i, header=8).loc[:,sh.qIDs['demo']] for i in arrayFiles]

    # regroup from byCity to byQ
    preAnswerByQ=[[tally_responses(cit,'pre', q_id) for cit in preByCity] for q_id in sh.qIDs['pre']]
    postAnswerByQ=[[tally_responses(cit,'post', q_id) for cit in postByCity] for q_id in sh.qIDs['post']]
    demoAnswerByQ=[[tally_responses(cit,'demo', q_id) for cit in demoByCity] for q_id in sh.qIDs['demo']]

    cumuPreTally=[[sum(x) for x in zip(*[c for c in q])] for q in preAnswerByQ ]
    cumuPostTally=[[sum(x) for x in zip(*[c for c in q])] for q in postAnswerByQ ]

    cumuData = [cumuPreTally, cumuPostTally]
    return preAnswerByQ,postAnswerByQ, cityNames,cumuData,demoAnswerByQ


def tally_responses(inputFrame, time, q_id):   
    ''' Counts number of A's, B's, etc for a question
        inputFrame: whole file
        time: demo/pre/post, loads the proper array
        q_id: which question in the category
    '''
    numberOfChoices = (sh.qDict[time][q_id]).numberOfChoices
    if len(inputFrame) == 0:
        return np.zeros(numberOfChoices)
    arrayOfResponses = []
    for letter in sh.MULTIPLE_CHOICE_LETTERS[:numberOfChoices]:
        expr = q_id + ' =="' + letter + '"'
        arrayOfResponses.append(inputFrame.query(expr).count()[q_id])
    return arrayOfResponses