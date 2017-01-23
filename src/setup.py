import shared as sh
from collections import OrderedDict
import pandas as pd


#******************************
#********* SETUP **************
#******************************



def import_questions():
    sh.qDict={'demo':OrderedDict(),'pre':OrderedDict(), 'post':OrderedDict()}
    sh.qIDs={}
    print(sh.QFILE)
    importedDataFrame = pd.DataFrame.from_csv(sh.QFILE)
    cols=importedDataFrame.columns
    for i in cols:
        multipleChoiceAnswersArray=[importedDataFrame.ix[k,i] for k in sh.MULTIPLE_CHOICE_LETTERS if importedDataFrame.ix[k,i]!= sh.NO_RESPONSE]
        question = sh.Question(importedDataFrame.ix['question text',i], 
            importedDataFrame.ix['topic',i], importedDataFrame.ix['time',i], 
            importedDataFrame.ix['correct character',i], multipleChoiceAnswersArray,int(importedDataFrame.ix['display cols',i]),i)
        sh.qDict[question.time][question.id]=(question)
    for j in sh.qDict.keys():
          sh.qIDs[j]=sh.qDict[j].keys() 
    return sh.qDict,sh.qIDs

import numpy as np
def setupResp(arrayFiles):
    #temp = np.array([])
    #for i in arrayFiles:
    #    x = pd.DataFrame.from_csv(i, header=8).loc[:,sh.qIDs['pre']]
    #    temp.append(x)
   
    # load preByCity using qID['pre'] column names
    preByCity= [pd.DataFrame.from_csv(i, header=8).loc[:,sh.qIDs['pre']] for i in arrayFiles]
    postByCity= [pd.DataFrame.from_csv(i, header=8).loc[:,sh.qIDs['post']] for i in arrayFiles]
    demoByCity= [pd.DataFrame.from_csv(i, header=8).loc[:,sh.qIDs['demo']] for i in arrayFiles]

    # regroup from byCity to byQ
    preAnswerByQ=[[tally_responses(cit,'pre',q) for cit in preByCity] for q in sh.qIDs['pre']]
    postAnswerByQ=[[tally_responses(cit,'post',q) for cit in postByCity] for q in sh.qIDs['post']]
    demoAnswerByQ=[[tally_responses(cit,'demo',q) for cit in demoByCity] for q in sh.qIDs['demo']]


    # total N pre/post for each q
    #preSum=[(sum(sum(c) for c in q)) for q in preAnswerByQ]
    #postSum=[(sum(sum(c) for c in q)) for q in postAnswerByQ]

   
    cityNames=[((i.split('/'))[-1] ) for i in arrayFiles]
    cityNames=[((i.split('.'))[0] ) for i in cityNames]
    print "split"
    print cityNames
    cumuPreTally=[[sum(x) for x in zip(*[c for c in q])] for q in preAnswerByQ ]
    cumuPostTally=[[sum(x) for x in zip(*[c for c in q])] for q in postAnswerByQ ]
   
    
    cumuData=[cumuPreTally,cumuPostTally]
    return preAnswerByQ,postAnswerByQ, cityNames,cumuData,demoAnswerByQ


def tally_responses(inputFrame, time,Qcol):   
    ''' Counts number of A's, B's, etc for a question
        inputFrame: whole file
        category: demo/pre/post, loads the proper array
        columnNumber: which question in the category
    '''
    numberOfChoices = (sh.qDict[time][Qcol]).numberOfChoices
    if len(inputFrame) == 0:
        return np.zeros(numberOfChoices)
    arrayOfResponses = []
    for let in sh.MULTIPLE_CHOICE_LETTERS[:numberOfChoices]:
        expr = Qcol+' =='+'"'+let+'"'
        arrayOfResponses.append(inputFrame.query(expr).count()[Qcol])
    return arrayOfResponses