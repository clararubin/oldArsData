NOT_APPLICABLE = 'n/a'
NO_CORRECT_ANSWER = 'none'
NO_RESPONSE = '-'
MULTIPLE_CHOICE_LETTERS = ['A','B','C','D','E','F','G','H']
DEGREE_LETTER_CHOICES = MULTIPLE_CHOICE_LETTERS
QFILE15 = '/Users/clararubin/Dropbox/___ARS - my copy/__ARS 15/corrected/questions.csv'
QFILE16 = '/Users/clararubin/Dropbox/___ARS - my copy/___ARS 16/mycorrected/input/questions2.csv'
QFILE = ''

#QFILE = 'questions.csv'
#QFILE = '/Users/clararubin/Dropbox/___ARS - my copy/__ARS Mood Dis 16- AZ/questions.csv'


arrayFiles16=['Atlanta.csv', 'Chicago.csv','Los Angeles.csv', 'Miami.csv', 'Houston.csv', 'Philadelphia.csv' , 'NYC.csv', 'DC.csv', 'USPC 2016.csv']
path16 = '/Users/clararubin/Dropbox/___ARS - my copy/___ARS 16/mycorrected/input/'
arrayFiles16=[ path16 + s for s in arrayFiles16]


arrayFiles15=['Anaheim.csv','Atlanta.csv','Boston.csv','Ft lauderdale.1.csv','Ft Lauderdale2.csv','Indianapolis.csv','Las Vegas.csv','Miami.csv','Nashville.csv','Philadelphia.csv','Richardson.csv','San Antonio.csv','scottsdale.csv','Southfield.csv','Springfield.csv','Syracuse.csv','Uniondale.csv','US psych.csv']
arrayFiles15=['Anaheim.csv','Atlanta.csv','Boston.csv','Ft Lauderdale2.csv','Indianapolis.csv' ,'Miami.csv','Nashville.csv' ,'Philadelphia.csv','Richardson.csv','San Antonio.csv','Scottsdale.csv','Southfield.csv','Springfield.csv','Syracuse.csv','Uniondale.csv' ]
path15 = '/Users/clararubin/Dropbox/___ARS - my copy/__ARS 15/corrected/'
arrayFiles15=[ path15 + s for s in arrayFiles15]



import pandas as pd
import numpy as np
from collections import OrderedDict
import datetime
import time
dt= str(datetime.date.today())+','+str(time.strftime("%H:%M"))
global qIDs 
qIDs="none"
global qDict
smSpace=.1
bigSpace=.2
colors=['#ab95d8','#f9cb8f','#cd7caa','#69caf4','#717263', 'red','purple', 'yellow']
sections16=[[0,2],[3,5],[6,9],[10,13],[14,16],[17,19]]
sections15=[[0,3],[4,7],[8,11],[12,15],[16,20],[21,24]]

#,[14,16],[17,19]
#pdfNameTemp='psych update 2016 ARS'+dt
#pdfNameTemp='scottsdale 2016 ARS'+dt
pdfNameTemp15='psych update 2015 ARS'+dt
pdfNameTemp16='psych update 2016 ARS'+dt

pdfNames15=[pdfNameTemp15+"part"+str(i)+'.pdf' for i in range(1,13)]
pdfNames16=[pdfNameTemp16+"part"+str(i)+'.pdf' for i in range(1,13)]

pdfNames = []


class Question:
    def __init__(self, questionText, topic, time, correctCharacter, arrayChoices,numCol,id):
        self.questionText = questionText
        self.correctCharacter = correctCharacter 
        self.topic = topic
        self.time = time 
        self.arrayMultipleChoices = arrayChoices
        self.numberOfChoices = len(self.arrayMultipleChoices)
        self.id=id
        self.numCol=min(100000,numCol)
        
    def __eq__(self, other):
        return True
    def __str__(self): 
        return self.questionText
    
class Time:
    pre, post, demo = ['pre','post','demo']
    
def getES(preC, preW, postC, postW):
    Npre = preC+preW
    Npost= postC+postW
    preScore = 1.0* preC/(Npre)
    
    postScore = 1.0* postC/(Npost)
    
    diff = postScore - preScore
    print "dif", diff

    pre = [1]*preC+[0]*preW
    post = [1]*postC+[0]*postW
    var=[np.var(pre,ddof=1),np.var(post,ddof=1)]
    pooledVar  = ((Npre) * (var[0]) + (Npost) * (var[1])) / (Npre + Npost )
    SD = np.sqrt(pooledVar)
    print "var", var
    ES = diff/SD
    return ES


def printQs(t):
    from shared import qIDs, qDict
    for q in qIDs[t]:
        print (qDict[t][q]).questionText
        print (qDict[t][q]).arrayMultipleChoices
        
