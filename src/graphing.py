# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import sys
import pylab
import shared as sh
reload(sh)
from matplotlib.backends.backend_pdf import PdfPages


def set_ticks(cityNames, ax, majorTickLabels, numchoices, width, fontsize, pvals, is_percent):
    minorticks=[]
    pretick=width*(numchoices)/2
    posttick=(pretick + sh.SMALL_SPACE + width*(numchoices))
    majorticks=[(pretick+posttick)/2]
    minorticks.append(pretick)
    minorticks.append(posttick)
    while len(majorticks)<(len(majorTickLabels)+1):
        pretick=(posttick+ sh.BIG_SPACE+ width*(numchoices))
        posttick=(pretick+ sh.SMALL_SPACE + width*(numchoices))
        majorticks.append((pretick+posttick)/2)
        minorticks.append(pretick)
        minorticks.append(posttick)
    ax.set_xticks(minorticks, minor = True)
    ax.set_xticklabels(['pre','post']*(len(majorTickLabels)+1), minor=True, fontsize=fontsize-1)
    ax.set_xticks(majorticks)
    labelsWithNewline=[]
    for i in range(len(majorTickLabels)):
        if pvals[0]==-1:
            labelsWithNewline.append('\n'+((cityNames[majorTickLabels[i]])+'\n**'))
        elif pvals[i]<.05:
            labelsWithNewline.append('\n'+((cityNames[majorTickLabels[i]])))
        elif pvals[i]>.05:
            labelsWithNewline.append('\n'+((cityNames[majorTickLabels[i]])+'\n*'))
        else: 
            sys.stderr.write( "pval error")
            SystemExit()
    if pvals[0]==-1:
        labelsWithNewline.append('\n Cumulative\n**')
    if pvals[-1]<.05:
        labelsWithNewline.append('\n Cumulative')
    else:
        labelsWithNewline.append('\n Cumulative\n*')
    if is_percent:  
        ax.set_ylabel('%')
    else:
        ax.set_ylabel('# Responses')
    
    font=5
    if(len(cityNames)<2):
        font=9
    ax.set_xticklabels(labelsWithNewline, fontsize=font)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(which = 'major', direction = 'out')
    plt.tick_params(which='minor', length=0)
    
def set_data(ax, numchoices, numcit, width, graph_settings, question_pair, response_pair):    
    question = question_pair['pre']
    blankcities=0
    usedcitynames=[]
    colors = iter(sh.COLORS)
    responsesprePercent=[]
    responsespostPercent=[]
    totalPre=[]
    totalPost=[]
    for citnum in range(len(response_pair['pre'])):
        totpre = sum(response_pair['pre'][citnum])
        totpost= sum(response_pair['post'][citnum])
        totalPre.append(totpre)
        totalPost.append(totpost)
        temp=[]
        if totpre!=0:
            for choice in response_pair['pre'][citnum]:
                temp.append(1.*choice)
        responsesprePercent.append(temp)
        temp=[]
        if totpost!=0:
            for choice in response_pair['post'][citnum]:
                temp.append(1.*choice)
        responsespostPercent.append(temp)
    btracker=[]
    print "total pre is:"
    print totalPre
    print "total post is:"
    print totalPost
    for choicenum in range(numchoices): #A
        Xvals = []
        Yvals = []
        preCumulative  = 0
        postCumulative = 0
        for citnum in range(numcit):
            if(totalPre[citnum] == 0): #city did not answer this q-- check during 'A' series
                if choicenum == 0: 
                    blankcities+=1
                    btracker.append(1)
            else:
                if choicenum == 0:
                    usedcitynames.append(citnum)
                    btracker.append(0)
                #p?rint "cit/ch", citnum ,choicenum
                preCumulative+= response_pair['pre'][citnum][choicenum]
                postCumulative+= response_pair['post'][citnum][choicenum]
                if graph_settings.is_percent :
                    Yvals.append(100.0*responsesprePercent[citnum][choicenum]/totalPre[citnum]) 
                    Yvals.append(100.0*responsespostPercent[citnum][choicenum]/totalPost[citnum]) 
                else:
                    Yvals.append( responsesprePercent[citnum][choicenum] ) 
                    Yvals.append( responsespostPercent[citnum][choicenum] ) 
                blanksofar=0
                z=0
                while z<citnum:
                    blanksofar+=btracker[z]
                    z+=1
                temp=((citnum-blanksofar)*(2*width*numchoices + sh.SMALL_SPACE + sh.BIG_SPACE) + choicenum*width )    
                Xvals.append(temp)
                Xvals.append(temp + width*numchoices + sh.SMALL_SPACE)    
        if (len(question.correctCharacter) > 1) or (ord(question.correctCharacter) - ord('A') != choicenum): #no correct answer
            thiscolor = next(colors)
        elif ord(question.correctCharacter)-65 == choicenum:
            thiscolor = 'lime'
        else:
            sys.stderr.write("color err")
            SystemExit()

        #add cumulative field
        if graph_settings.is_cumulative:
            temp=((citnum+1-blankcities)*(2*width*numchoices + sh.SMALL_SPACE + sh.BIG_SPACE)+ choicenum*width )    
            Xvals.append(temp)
            Xvals.append(temp + width*numchoices + sh.SMALL_SPACE ) 
            Yvals.append(100.0*preCumulative/sum(totalPre))
            Yvals.append(100.0*postCumulative/sum(totalPost))
            
        #ax.bar changes state of pdf
        ax.bar(Xvals, Yvals, color=thiscolor, width=.8*width, label = question.arrayMultipleChoices[choicenum], edgecolor = 'none', linewidth=.7)
       
    
    nLoc = Xvals[-3]+2*width
    nLocY = .9
    if(numcit<2):
        nLoc=.8
    
    summed_totalPre  = sum(totalPre)
    summed_totalPost = sum(totalPost)
    
    ax.annotate('pre:  N='+str(summed_totalPre)+'\npost: N='+str(summed_totalPost), xy=(nLoc, nLocY), xycoords=ax.get_xaxis_transform(), fontsize=6, va='top')

    Xmax = Xvals[len(Xvals)-1]+width
    return usedcitynames, Xmax

def set_legend(number_of_columns, numchoices, fontsize):
    legH = 1.05
    legW = 0.5
    legfontsize = fontsize-1
    legend = plt.legend(loc='upper center', bbox_to_anchor=(legW, legH), ncol=number_of_columns, fontsize=legfontsize) 
    legend.get_frame().set_facecolor('none')
    legend.get_frame().set_linewidth(.5)

def set_title(ax, question):
    
    def helper_function(line_list, new_word):
        '''
        helper function used for reduce, constructs list of lines containing
        not too many characters per line
        '''
        if len(line_list[-1]) < 115:
            line_list[-1] += new_word + ' '
            return line_list
        else:
            line_list.append(new_word + ' ')
            return line_list
    
    question_words = question.questionText.split()
    title_lines = reduce(helper_function, question_words, [''])
    title = '\n'.join(title_lines)
    
    # apparently the graphing code only works right if the title ends in a newline.
    # this is probably not a good thing but I don't know how to fix it yet
    title += '\n'
            
    print "Setting title to:", title
    ax.set_title(title, fontsize=8)
    
def get_pvals(correctPre, incorrectPre, correctPost, incorrectPost):
    print (correctPre,incorrectPre,correctPost,incorrectPost)
    chi= 1.*(correctPre*incorrectPost - correctPost*incorrectPre)*(correctPre*incorrectPost - correctPost*incorrectPre)*(correctPre+incorrectPost+correctPost+incorrectPre)
    denom=1.0*((correctPre+correctPost)*(incorrectPost+incorrectPre)*(incorrectPost+correctPost)*(correctPre+incorrectPre))
    if denom==0:
        sys.stderr.write('ZEROZERO')
        #p?rint correctPre,incorrectPost,correctPost,incorrectPre
        chi=-1
    chi = chi/denom
    import scipy.stats as stat
    pval=stat.distributions.chi2.sf(chi,1)
    return pval
    
def get_stats(response_pair, correctIndex, usedcitynames):
    pvals=[]
    TOTcorrectPre=0
    TOTcorrectPost=0
    TOTincorrectPre=0
    TOTincorrectPost=0
    for citnum in usedcitynames:
        correctPre = response_pair['pre'][citnum][correctIndex]
        incorrectPre=sum(response_pair['pre'][citnum])-correctPre
        correctPost=response_pair['post'][citnum][correctIndex]
        incorrectPost=sum(response_pair['post'][citnum])-correctPost
        TOTcorrectPre+=correctPre
        TOTcorrectPost+=correctPost
        TOTincorrectPre+=incorrectPre
        TOTincorrectPost+=incorrectPost
        pval=get_pvals(correctPre,incorrectPre,correctPost,incorrectPost)
        pvals.append(pval)

    pval=get_pvals(TOTcorrectPre,TOTincorrectPre,TOTcorrectPost,TOTincorrectPost)
    pvals.append(pval)
    return pvals
    
def graph_pre_post(ax, city_names, graph_settings, question_pair, response_pair):
    
    #setup
    question = question_pair['pre']
    number_of_columns = question.numCol
    numchoices = question.numberOfChoices
    width = (1 - sh.BIG_SPACE) / (numchoices*2)
    numcit = len(response_pair['pre'])
    fontsize = 8
    
    #data & graphing functions
    usedcitynames, Xmax = set_data(
        ax,numchoices,numcit, width, graph_settings, question_pair, response_pair 
        )
    
    if question.correctCharacter == sh.NO_CORRECT_ANSWER:
        pvals = [-1]
    else:
        correctIndex = ord(question.correctCharacter) - ord('A')
        pvals = get_stats(response_pair, correctIndex, usedcitynames)
    
    set_ticks(city_names, ax, usedcitynames, numchoices, width, fontsize,pvals, graph_settings.is_percent)
    
    
    set_legend(number_of_columns, numchoices, fontsize)
    set_title(ax, question)
    
    #plot
    plt.xlim(0, Xmax)
    if graph_settings.is_percent:
        plt.ylim(0, 100)
    plt.tight_layout()
    return usedcitynames, pvals


def addPlotToPage(index, fig, city_names, graph_settings, question_pair, response_pair, stored_city_name, pvals):
    '''
    :param index:             index of plot on page (1 or 2 bc there are only 2 plots per page)
    :param fig:               object (in this case equal to 1 page) which contains plots
    :param q:
    :param is_cumulative:
    :param is_percent:
    :param questions_data:
    :param responses_data:
    :param stored_city_name:
    :param pvals:
    '''
    ax = fig.add_subplot(2, 1, index)
    cit, pval = graph_pre_post(ax, city_names, graph_settings, question_pair, response_pair)
    stored_city_name.append(cit)
    pvals.append(pval)
    
    
def make_pdf_of_section(section_iter, pdfName, graph_settings, questions_data, responses_data):
    print("~~~~~~~~~~~~~~~~~")
    print(pdfName)
    print("~~~~~~~~~~~~~~~~~")
    
    pdf = PdfPages(sh.getOutputPath() + pdfName)
    stored_city_name=[]
    city_names = responses_data.cityNames
    pvals=[]

    #iterates through the range of section numbers 2 at a time, or 1 if only 1 remaining
    for q_index_pair in section_iter:
        print "\n\n\nProcess Q:", q_index_pair
        
        fig = plt.figure(figsize=(11,8.5), dpi=100)
        pylab.figtext(0.01, .98, sh.GRAPH_TEXT_1, fontsize=8)
        pylab.figtext(0.01, .97, sh.GRAPH_TEXT_2, fontsize=8, color='lime')
        
        for i,j in enumerate(q_index_pair):
            question_pair = {'pre': questions_data.get('pre', j), 'post': questions_data.get('post', j)}
            response_pair = {'pre': responses_data.preAnswerByQ[j], 'post': responses_data.postAnswerByQ[j]}
            addPlotToPage(i+1, fig, city_names, graph_settings, question_pair, response_pair, stored_city_name, pvals)
        
        pdf.savefig(fig, orientation='portrait')
        
    plt.close()
    pdf.close()
    return stored_city_name, pvals