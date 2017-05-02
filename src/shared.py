import os 

NOT_APPLICABLE = 'n/a'
NO_CORRECT_ANSWER = 'none'
NO_RESPONSE = '-'
MULTIPLE_CHOICE_LETTERS = ['A','B','C','D','E','F','G','H']

SMALL_SPACE = .1
BIG_SPACE = .2
CORRECT_COLOR = 'lime'
COLORS = ['#ab95d8','#f9cb8f','#cd7caa','#69caf4','#717263','#ffff66']
FONT_SIZE = 7
TITLE_FONT_SIZE = 8


GRAPH_TEXT_1 = '* = change not significant (p$\geq$0.05)'
GRAPH_TEXT_2 = '\ngreen = correct answer'

#change working directory to location of this file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def getInputPath():
    return os.path.join(os.getcwd(), "../../input/")

def getOutputPath():
    return os.path.join(os.getcwd(), "../../output/")
    
def iter_doubler(iterr):
    iterr = iter(iterr)
    for i in iterr:
        try:
            yield (i, next(iterr))
        except StopIteration:
            yield (i,)




        