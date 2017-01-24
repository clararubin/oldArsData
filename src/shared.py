NOT_APPLICABLE = 'n/a'
NO_CORRECT_ANSWER = 'none'
NO_RESPONSE = '-'
MULTIPLE_CHOICE_LETTERS = ['A','B','C','D','E','F','G','H']

QFILE16 = '..\..\input\questions2.csv'
QFILE15 = ''

cities16 = ['Atlanta.csv', 'Chicago.csv','Los Angeles.csv', 'Miami.csv', 'Houston.csv', 'Philadelphia.csv' , 'NYC.csv', 'San Francisco.csv','DC.csv', 'Boston.csv','USPC 2016.csv']
cities15 = ['Anaheim.csv','Atlanta.csv','Boston.csv','Ft Lauderdale2.csv','Indianapolis.csv' ,'Miami.csv','Nashville.csv' ,'Philadelphia.csv','Richardson.csv','San Antonio.csv','Scottsdale.csv','Southfield.csv','Springfield.csv','Syracuse.csv','Uniondale.csv' ]

arrayFiles16=[ '..\..\input\%s' % (city) for city in cities16]
arrayFiles15=[ '..\..\input\%s' % (city) for city in cities15]

smSpace=.1
bigSpace=.2
colors=['#ab95d8','#f9cb8f','#cd7caa','#69caf4','#717263', 'red','purple', 'yellow']
sections16=[[0,2],[3,5],[6,9],[10,13],[14,16],[17,19]]
sections15=[[0,3],[4,7],[8,11],[12,15],[16,20],[21,24]]

def get_date_string():
    #example output: '2017-01-23__23-12'
    import datetime
    import time
    return str(datetime.date.today()) + '__' +str(time.strftime("%H-%M"))

def format_pdf_name(temp_name, index):
    #example inputs: 'psych update 2016 ARS', 1
    #example output: 'psych update 2016 ARS__2017-01-23__23-12__part1.pdf'
    pdf_title = "__".join((temp_name, get_date_string(), "part"+str(index)))
    return pdf_title + ".pdf"

def pdf_name_list(temp_name):
    SIZE = 12
    return [format_pdf_name(temp_name, i) for i in range(1,SIZE+1)]

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