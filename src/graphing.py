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

def set_ticks(ax, graph_settings, pvals, used_city_names):
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
    
def set_data(ax, graph_settings, data, pre_number):
    number_of_choices = data.number_of_choices(pre_number)
    
    cluster_width = (1 - sh.BIG_SPACE) / 2
    bar_width = cluster_width / number_of_choices 
    category_width = 2*cluster_width + sh.SMALL_SPACE + sh.BIG_SPACE
    
    q_nums = data.pre_post_of_pre(pre_number)
    correct_choice = data.correct_character(pre_number)
    choice_list = data.choice_list(pre_number)
    answer_list = data.answer_list(pre_number)
    
    partition = graph_settings.partition
    category_names = list(data.get_relevant_category_names(partition, pre_number))
    if graph_settings.is_cumulative: category_names.append('Cumulative')
    
    colors = iter(sh.COLORS)
    
    for choicenum, choice in enumerate(choice_list):
        #TODO clean this up with ranges        
        
        Xvals = [ index*category_width + choicenum*bar_width + time_offset
                  for index in range(len(category_names))
                  for time_offset in (0, cluster_width + sh.SMALL_SPACE)
                ]
       
        Yvals = []
        for category in category_names:
            for q_num in q_nums:
                height_scalar = 1
                if graph_settings.is_percent:
                    total_responses = data.count_responses(q_num, subset = (partition, category))
                    height_scalar = 100.0 / total_responses
                responses = data.count_responses(q_num, subset = (partition, category), response = choice)
                Yvals.append(responses * height_scalar)
        
        #set the color for this bar
        bar_color = next(colors) if correct_choice != choice else sh.CORRECT_COLOR
            
        ax.bar(Xvals, Yvals, color=bar_color, width=.8*bar_width, label = answer_list[choicenum], edgecolor = 'none', linewidth=.7)
       
    #TODO: wtf is this line
    nLocX = Xvals[-3] + 2*bar_width if len(category_names) >= 2 else .8
    nLocY = .9
    
    ax.annotate(
        'pre:  N=%d\n' % data.count_responses(q_nums[0], subset = (partition, 'Cumulative')) +
        'post: N=%d'   % data.count_responses(q_nums[1], subset = (partition, 'Cumulative')),
        xy          = (nLocX, nLocY),
        xycoords    = ax.get_xaxis_transform(),
        fontsize    = 6,
        va          = 'top'
        )

    Xmax = Xvals[-1] + bar_width
    return category_names, Xmax

def set_legend(number_of_columns):
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

    
def graph_pre_post(ax, graph_settings, data, pre_number):
    
    #data & graphing functions
    used_city_names, Xmax = set_data(
        ax, graph_settings, data, pre_number
        )
    
    #TODO
    pvals = stats.get_pvals(data, pre_number, used_city_names, graph_settings)
    
    set_ticks(ax, graph_settings, pvals, used_city_names)    
    set_legend(data.legend_columns(pre_number))
    set_title(ax, data.get_question_text(pre_number))
    
    #plot
    plt.xlim(0, Xmax)
    if graph_settings.is_percent: plt.ylim(0, 100)
    plt.tight_layout()
    
def make_pdf_of_section(pdfName, data, topic, graph_settings):  
    pdf = PdfPages(sh.getOutputPath() + pdfName)

    # iterates through the questions+response data 2 questions worth
    # at a time, or 1 if only 1 remaining
    pre_numbers = data.get_pres_of_topic(topic)
    
    for pre_tuple in sh.iter_doubler(pre_numbers):

        fig = plt.figure(figsize=(11,8.5), dpi=100)
        pylab.figtext(0.01, .98, sh.GRAPH_TEXT_1, fontsize=8)
        pylab.figtext(0.01, .97, sh.GRAPH_TEXT_2, fontsize=8, color='lime')
        
        for i, pre_number in enumerate(pre_tuple): #iterates over either 1 or 2 item
            ax = fig.add_subplot(2, 1, i+1)
            graph_pre_post(ax, graph_settings, data, pre_number)
        
        pdf.savefig(fig, orientation='portrait')

    plt.close()
    pdf.close()