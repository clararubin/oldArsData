import os 

NOT_APPLICABLE = 'n/a'
NO_CORRECT_ANSWER = 'none'
NO_RESPONSE = '-'
MULTIPLE_CHOICE_LETTERS = ['A','B','C','D','E','F','G','H']

SMALL_SPACE = .1
BIG_SPACE = .2
COLORS = ['#ab95d8','#f9cb8f','#cd7caa','#69caf4','#717263','#ffff66']


GRAPH_TEXT_1 = '* = change not significant (p$\geq$0.05)'
GRAPH_TEXT_2 = '\ngreen = correct answer'

def getInputPath():
    return '../../input/' if (os.name == 'posix') else '..\..\input\\'

def getOutputPath():
    return '../../output/' if (os.name == 'posix') else '..\..\output\\'
    
    


# 2015 stuff (TO BE MOVED)
cities15 = ['Anaheim.csv','Atlanta.csv','Boston.csv','Ft Lauderdale2.csv','Indianapolis.csv' ,'Miami.csv','Nashville.csv' ,'Philadelphia.csv','Richardson.csv','San Antonio.csv','Scottsdale.csv','Southfield.csv','Springfield.csv','Syracuse.csv','Uniondale.csv' ]
arrayFiles15=[ '..\..\input\%s' % (city) for city in cities15]
sections15=[[0,3],[4,7],[8,11],[12,15],[16,20],[21,24]]




        