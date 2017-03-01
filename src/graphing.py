# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pylab
import shared as sh
reload(sh)
import stats
reload(stats)
from matplotlib.backends.backend_pdf import PdfPages

def get_labels(used_city_names, pvals):
    labels = ['\n' + city for city in used_city_names]
    if pvals == None:
        labels = [label + '\n**' for label in labels]
    else:
        labels = [label + '\n*'*(pval > .05) for label,pval in zip(labels,pvals)]
    return labels

def set_ticks(ax, used_city_names, numchoices, pvals, graph_settings):
    cluster_width = (1 - sh.BIG_SPACE) / 2
    
    preticks = [cluster_width/2 + i*(sh.SMALL_SPACE + sh.BIG_SPACE + 2*cluster_width)
                for i in range(len(used_city_names))]
    postticks = [i + sh.SMALL_SPACE + cluster_width for i in preticks]
    
    #sets minorticks to an interleaving of preticks and postticks
    minorticks = [x for y in zip(preticks, postticks) for x in y]
    ax.set_xticks(minorticks, minor = True)
    ax.set_xticklabels(['pre','post'] * len(used_city_names), minor = True, fontsize = sh.FONT_SIZE)
    
    #sets majorticks to an average of preticks and postticks
    majorticks = [(x+y)/2 for x,y in zip(preticks, postticks)]
    ax.set_xticks(majorticks)
    
    ax.set_ylabel('%' if graph_settings.is_percent else '# Responses')
        
    labels = get_labels(used_city_names, pvals)
    ax.set_xticklabels(labels, fontsize = 5)
    
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(which = 'major', direction = 'out')
    ax.tick_params(which = 'minor', length=0)
    
def set_data(ax, numchoices, graph_settings, question_pair, response_pair):  
    cluster_width = (1 - sh.BIG_SPACE) / 2
    bar_width = cluster_width / numchoices 
    city_width = 2*cluster_width + sh.SMALL_SPACE + sh.BIG_SPACE
    
    correct_answer = question_pair['pre'].correctCharacter
    answer_list = question_pair['pre'].arrayMultipleChoices
    used_city_names = response_pair['pre'].keys()
    
    colors = iter(sh.COLORS)
    
    for choicenum in range(numchoices):
        Xvals = [ city_index*city_width + choicenum*bar_width + time_offset
                  for city_index in range(len(used_city_names))
                  for time_offset in (0, cluster_width + sh.SMALL_SPACE)
                ]
                
        Yvals = [ response_pair[time][city][choicenum] * height_scalar
                  for city in used_city_names
                  for time in ('pre','post')
                  for height_scalar in [100.0/sum(response_pair[time][city]) if graph_settings.is_percent else 1]
                ]
        
        #set the color for this bar 
        bar_color = sh.CORRECT_COLOR
        if (len(correct_answer) > 1) or (ord(correct_answer) - ord('A') != choicenum): #not the correct answer
            bar_color = next(colors)
            
        ax.bar(Xvals, Yvals, color=bar_color, width=.8*bar_width, label = answer_list[choicenum], edgecolor = 'none', linewidth=.7)
       
    #TODO: wtf is this line
    nLocX = Xvals[-3] + 2*bar_width if len(used_city_names) >= 2 else .8
    nLocY = .9
    
    ax.annotate( #TODO: make work for non-cumulative
        'pre:  N=%d\n' % sum(response_pair['pre']['Cumulative']) +
        'post: N=%d'   % sum(response_pair['post']['Cumulative']),
        xy          = (nLocX, nLocY),
        xycoords    = ax.get_xaxis_transform(),
        fontsize    = 6,
        va          = 'top'
        )

    Xmax = Xvals[-1] + bar_width
    return used_city_names, Xmax

def set_legend(number_of_columns, numchoices):
    legH = 1.05
    legW = 0.5
    legend = plt.legend(loc='upper center', bbox_to_anchor=(legW, legH), ncol=number_of_columns, fontsize=sh.FONT_SIZE) 
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
    ax.set_title(title, fontsize = sh.TITLE_FONT_SIZE)

    
def graph_pre_post(ax, graph_settings, question_pair, response_pair):
    #setup
    question = question_pair['pre']
    number_of_columns = question.numCol
    numchoices = question.numberOfChoices
    
    #data & graphing functions
    used_city_names, Xmax = set_data(
        ax, numchoices, graph_settings, question_pair, response_pair 
        )
    
    if question.correctCharacter == sh.NO_CORRECT_ANSWER:
        pvals = None
    else:
        correctIndex = ord(question.correctCharacter) - ord('A')
        pvals = stats.get_pvals(response_pair, correctIndex, used_city_names)
    
    set_ticks(ax, used_city_names, numchoices, pvals, graph_settings)    
    set_legend(number_of_columns, numchoices)
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