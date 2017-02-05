# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import sys
import pylab
import shared as sh
reload(sh)
import stats
reload(stats)
from matplotlib.backends.backend_pdf import PdfPages

def set_ticks(ax, used_city_names, numchoices, width, fontsize, pvals, is_percent):
    minorticks=[]
    pretick=width*(numchoices)/2
    posttick=(pretick + sh.SMALL_SPACE + width*(numchoices))
    majorticks=[(pretick+posttick)/2]
    minorticks.append(pretick)
    minorticks.append(posttick)
    while len(majorticks)<(len(used_city_names)+1):
        pretick=(posttick+ sh.BIG_SPACE+ width*(numchoices))
        posttick=(pretick+ sh.SMALL_SPACE + width*(numchoices))
        majorticks.append((pretick+posttick)/2)
        minorticks.append(pretick)
        minorticks.append(posttick)
    ax.set_xticks(minorticks, minor = True)
    ax.set_xticklabels(['pre','post']*(len(used_city_names)+1), minor=True, fontsize=fontsize-1)
    ax.set_xticks(majorticks)
    labelsWithNewline=[]
    for i in range(len(used_city_names)):
        if pvals[0]==-1:
            labelsWithNewline.append('\n'+used_city_names[i]+'\n**')
        elif pvals[i]<.05:
            labelsWithNewline.append('\n'+used_city_names[i])
        elif pvals[i]>.05:
            labelsWithNewline.append('\n'+used_city_names[i]+'\n*')
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
    
    ax.set_xticklabels(labelsWithNewline, fontsize = 5)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(which = 'major', direction = 'out')
    plt.tick_params(which='minor', length=0)
    
def set_data(ax, numchoices, width, graph_settings, question_pair, response_pair):    
    correct_answer = question_pair['pre'].correctCharacter
    answer_list = question_pair['pre'].arrayMultipleChoices
    city_names = response_pair['pre'].keys()
    
    colors = iter(sh.COLORS)
    
    total_answers = {'pre': {}, 'post': {}}
    for city in city_names:
        for time in 'pre','post':
            total_answers[time][city] = sum(response_pair[time][city])
    print "total number of responses are: %s" % (total_answers)
    
    all_responses = {time: sum(v.values())
                     for time, v in total_answers.items()}
    
    for choicenum in range(numchoices):
        Xvals = []
        Yvals = []
        preCumulative  = 0
        postCumulative = 0
        for city_index, city in enumerate(city_names):
            preCumulative += response_pair['pre'][city][choicenum]
            postCumulative += response_pair['post'][city][choicenum]
            
            temp = city_index*(2*width*numchoices + sh.SMALL_SPACE + sh.BIG_SPACE) + choicenum*width  
            Xvals.append(temp)
            Xvals.append(temp + width*numchoices + sh.SMALL_SPACE)
            
            pre_height_scalar = 100.0/total_answers['pre'][city] if graph_settings.is_percent else 1
            post_height_scalar = 100.0/total_answers['post'][city] if graph_settings.is_percent else 1
            Yvals.append(response_pair['pre'][city][choicenum] * pre_height_scalar) 
            Yvals.append(response_pair['post'][city][choicenum] * post_height_scalar)

        #add cumulative field
        if graph_settings.is_cumulative:
            temp = len(city_names)*(2*width*numchoices + sh.SMALL_SPACE + sh.BIG_SPACE) + choicenum*width   
            Xvals.append(temp)
            Xvals.append(temp + width*numchoices + sh.SMALL_SPACE)
            
            pre_height_scalar  = 100.0/all_responses['pre']  if graph_settings.is_percent else 1
            post_height_scalar = 100.0/all_responses['post'] if graph_settings.is_percent else 1
            Yvals.append(preCumulative  * pre_height_scalar)
            Yvals.append(postCumulative * post_height_scalar)
        
        #set the color for this bar 
        thiscolor = 'lime'
        if (len(correct_answer) > 1) or (ord(correct_answer) - ord('A') != choicenum): #not the correct answer
            thiscolor = next(colors)
            
        #ax.bar changes state of pdf
        ax.bar(Xvals, Yvals, color=thiscolor, width=.8*width, label = answer_list[choicenum], edgecolor = 'none', linewidth=.7)
       
    
    nLocX = Xvals[-3] + 2*width if len(city_names) >= 2 else .8
    nLocY = .9
    
    ax.annotate('pre:  N=%d\npost: N=%d' % (all_responses['pre'], all_responses['post']),
        xy          = (nLocX, nLocY),
        xycoords    = ax.get_xaxis_transform(),
        fontsize    = 6,
        va          = 'top'
        )

    Xmax = Xvals[-1] + width
    return city_names, Xmax

def set_legend(number_of_columns, numchoices, fontsize):
    legH = 1.05
    legW = 0.5
    legfontsize = fontsize-1
    legend = plt.legend(loc='upper center', bbox_to_anchor=(legW, legH), ncol=number_of_columns, fontsize=legfontsize) 
    legend.get_frame().set_facecolor('none')
    legend.get_frame().set_linewidth(.5)

def set_title(ax, question_text):
    
    def line_iter(question_text):
        question_words = iter(question_text.split())
        while True:
            try:
                line = next(question_words)
            except StopIteration:
                pass
                
            while len(line) < 115:
                try:
                    line += ' ' + next(question_words)
                except StopIteration:
                    yield line
                    raise StopIteration
                    
            yield line
    
    title = '\n'.join(line_iter(question_text))
    title += '\n'
    
    print "Setting title to:", title
    ax.set_title(title, fontsize=8)

    
def graph_pre_post(ax, graph_settings, question_pair, response_pair):
    #setup
    question = question_pair['pre']
    number_of_columns = question.numCol
    numchoices = question.numberOfChoices
    width = (1 - sh.BIG_SPACE) / (numchoices*2)
    fontsize = 8
    
    #data & graphing functions
    used_city_names, Xmax = set_data(
        ax, numchoices, width, graph_settings, question_pair, response_pair 
        )
    
    if question.correctCharacter == sh.NO_CORRECT_ANSWER:
        pvals = [-1]
    else:
        correctIndex = ord(question.correctCharacter) - ord('A')
        pvals = stats.get_pvals(response_pair, correctIndex, used_city_names)
    
    set_ticks(ax, used_city_names, numchoices, width, fontsize, pvals, graph_settings.is_percent)    
    set_legend(number_of_columns, numchoices, fontsize)
    set_title(ax, question.questionText)
    
    #plot
    plt.xlim(0, Xmax)
    if graph_settings.is_percent:
        plt.ylim(0, 100)
    plt.tight_layout()


def addPlotToPage(index, fig, graph_settings, question_pair, response_pair):
    '''
    :param index:             index of plot on page (1 or 2 bc there are only 2 plots per page)
    :param fig:               object (in this case equal to 1 page) which contains plots
    :param graph_settings:
    :param questions_data:
    :param responses_data:
    '''
    ax = fig.add_subplot(2, 1, index)
    graph_pre_post(ax, graph_settings, question_pair, response_pair)
    
def make_pdf_of_section(section_iter, pdfName, graph_settings): #TODO: remove city_names as arg    
    pdf = PdfPages(sh.getOutputPath() + pdfName)

    # iterates through the questions+response data 2 questions worth
    # at a time, or 1 if only 1 remaining
    for q_r_tuple in sh.iter_doubler(section_iter):

        fig = plt.figure(figsize=(11,8.5), dpi=100)
        pylab.figtext(0.01, .98, sh.GRAPH_TEXT_1, fontsize=8)
        pylab.figtext(0.01, .97, sh.GRAPH_TEXT_2, fontsize=8, color='lime')
        
        for index, q_and_r_data in enumerate(q_r_tuple): #iterates over either 1 or 2 items 
            question_pair = q_and_r_data['question_pair']
            response_pair = q_and_r_data['response_pair']
            addPlotToPage(index+1, fig, graph_settings, question_pair, response_pair)
        
        pdf.savefig(fig, orientation='portrait')

    plt.close()
    pdf.close()