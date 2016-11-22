import shared as sh
import matplotlib.pyplot as plt
import sys

#******************************
#********* GRAPHING ************
#******************************

def set_ticks(cityNames,ax,majorTickLabels, numchoices, width, smSpace, bigSpace,fontsize ,pvals,percent):
    minorticks=[]
    pretick=width*(numchoices)/2
    posttick=(pretick+smSpace+ width*(numchoices))
    majorticks=[(pretick+posttick)/2]
    minorticks.append(pretick)
    minorticks.append(posttick)
    while len(majorticks)<(len(majorTickLabels)+1):
        pretick=(posttick+bigSpace+ width*(numchoices))
        posttick=(pretick+smSpace+ width*(numchoices))
        majorticks.append((pretick+posttick)/2)
        minorticks.append(pretick)
        minorticks.append(posttick)
    ax.set_xticks(minorticks, minor = True)
    ax.set_xticklabels(['pre','post']*(len(majorTickLabels)+1), minor=True, fontsize=fontsize-1)
    ax.set_xticks(majorticks)
    #ax.set_yticks(range(0,101,20))
    #ax.set_yticklabels(range(0,101,20),fontsize=fontsize)
    labelsWithNewline=[]
    for i in range(len(majorTickLabels)):
        if pvals[0]==-1:
            labelsWithNewline.append('\n'+((cityNames[majorTickLabels[i]])+'\n**'))
        elif pvals[i]<0.05:
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
    if(percent==True):  
        ax.set_ylabel('%')
    else:
        ax.set_ylabel('# Responses')
    
    font=5
    if(len(cityNames)<2):
        font=9
    ax.set_xticklabels(labelsWithNewline, fontsize=font)
#     ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.f%%'))
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(which = 'major', direction = 'out')
    plt.tick_params(which='minor', length=0)
    
def set_data(ax,numchoices,numcit,responsespre, responsespost, colors, width,smSpace, bigSpace,q,doCumu,percent):
    print "**** LENGTH OF RESP PRE0"
    print len(responsespre[0])
    ID=sh.qIDs['pre'][q]
    Ques=sh.qDict['pre'][ID]
    
    blankcities=0
    usedcitynames=[]
    color=0
    responsesprePercent=[]
    responsespostPercent=[]
    totalPre=[]
    totalPost=[]
    for citnum in range(len(responsespre)):
        totpre = sum(responsespre[citnum])
        totpost= sum(responsespost[citnum])
        totalPre.append(totpre)
        totalPost.append(totpost)
        temp=[]
        if totpre!=0:
            for choice in responsespre[citnum]:
                temp.append(1.*choice)
        responsesprePercent.append(temp)
        temp=[]
        if totpost!=0:
            for choice in responsespost[citnum]:
                temp.append(1.*choice)
        responsespostPercent.append(temp)
    btracker=[]
    print "total pre is:"
    print totalPre
    print "total post is:"
    print totalPost
    for choicenum in range(numchoices): #A
        Xvals=[]
        Yvals=[]
        preCumulative=0
        postCumulative=0
        for citnum in range(numcit):
            if(totalPre[citnum]==0): #city did not answe this q-- check during 'A' series
                if choicenum==0: 
                    blankcities+=1
                    btracker.append(1)
            else:
                if(choicenum==0):
                    usedcitynames.append(citnum)
                    btracker.append(0)
                #p?rint "cit/ch", citnum ,choicenum
                preCumulative+=responsespre[citnum][choicenum]
                postCumulative+=responsespost[citnum][choicenum]
                if(percent==True):
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
                temp=((citnum-blanksofar)*(2*width*numchoices +smSpace+bigSpace)+ choicenum*width )    
                Xvals.append(temp)
                Xvals.append(temp + width*numchoices +smSpace )    
        if(len(Ques.correctCharacter)>1 or ord(Ques.correctCharacter)-65!=choicenum): #no correct answer
            thiscolor=colors[color]
            color+=1
            edgecolor='none'
        elif ord(Ques.correctCharacter)-65==choicenum:
            thiscolor='lime'
            edgecolor='none'
        else:
            sys.stderr.write("color err")
            SystemExit()
        #add cumulative field
        temp=((citnum+1-blankcities)*(2*width*numchoices +smSpace+bigSpace)+ choicenum*width )    
        Xvals.append(temp)
        Xvals.append(temp + width*numchoices +smSpace ) 
        # **** DETERMINE CUMULATIVE ***
        if(doCumu):
            Yvals.append(100.0*preCumulative/sum(totalPre))
            Yvals.append(100.0*postCumulative/sum(totalPost))
        else:
            Xvals=Xvals[0:-2]
        series=ax.bar(Xvals, Yvals, color=thiscolor,width=.8*width, label=Ques.arrayMultipleChoices[choicenum],edgecolor = edgecolor, linewidth=.7)
        #cumulativeData=[preCumulative,sum(totalPre),postCumulative,sum(totalPost)]
        #p?rint "CCC",cumulativeData
        #p?rint q, choicenum, Yvals
        import numpy as np
        np.set_printoptions(precision=0)
        #p?rint sh.MULTIPLE_CHOICE_LETTERS[choicenum]
        #p?rint "y",
        #p?rint ["%.0f" % y for y in Yvals]
        #p?rint "x",
        #p?rint ["%.2f" % x for x in Xvals]        
    #ax.annotate('pre:  N='+str(sum(totalPre))+'\npost: N='+str(sum(totalPost)), xy=(2.95, 1), xycoords=ax.get_xaxis_transform(), fontsize=6, va='top')
    
    #endPost=Xvals[-1]
    #endPre=Xvals[-2]
    #respWidth=1.0*numchoices*width
    #nPost =1.0*endPost-respWidth/2
    #nPre =1.0*endPre-respWidth/2
    #p?rint "NNN",nPre, nPost
    #ax.annotate('N=\n'+str(sum(totalPre)), xy=(nPre, .8), xycoords=ax.get_xaxis_transform(), fontsize=6, ha='left')
    #ax.annotate('N=\n'+str(sum(totalPost)), xy=(nPost, .8), xycoords=ax.get_xaxis_transform(), fontsize=6, ha='right')
    
    nLoc = Xvals[-3]+2*width
    #nLoc = Xvals[-2]-4*width
    nLocY = .9
    if(numcit<2):
        nLoc=.8
    
    summed_totalPre = sum(totalPre)
    summed_totalPost = sum(totalPost)
    
    #ax.annotate('pre:  N='+str(sum(totalPre))+'\npost: N='+str(sum(totalPost)), xy=(nLoc, nLocY), xycoords=ax.get_xaxis_transform(), fontsize=6, va='top')
    ax.annotate('pre:  N='+str(summed_totalPre)+'\npost: N='+str(summed_totalPost), xy=(nLoc, nLocY), xycoords=ax.get_xaxis_transform(), fontsize=6, va='top')

    #ax.text(Xvals[len(Xvals)-2], height_nVal, 'N=\n'+str(sum(totalPre)), fontsize=6,ha='center')
    #ax.text(Xvals[len(Xvals)-1], height_nVal, 'N=\n'+str(sum(totalPost)),fontsize=6,ha='center')
    Xmax=Xvals[len(Xvals)-1]+width
    return usedcitynames, Xmax

def set_legend(q, numchoices,fontsize):
    legH=1.05
    legW=0.5
    legfontsize=fontsize-1
    ID=sh.qIDs['pre'][q]
    Ques=sh.qDict['pre'][ID]
    col=Ques.numCol
    legend=plt.legend(loc='upper center',bbox_to_anchor=(legW, legH),ncol=col, fontsize=legfontsize) 
    legend.get_frame().set_facecolor('none')
    legend.get_frame().set_linewidth(.5)

    
def set_title(ax,Ques):
    #set title

    wholeString = (Ques.questionText).split()
    h=0
    newString=''
    while h<len(wholeString):
        firstline=''
        while len(firstline)<115 and h<len(wholeString):
            firstline+=(wholeString[h]+' ')
            h+=1
        newString+=firstline
        newString+=('\n')
    print "setting title", newString
    ax.set_title(newString, fontsize=8)
    
def get_pvals(correctPre,incorrectPre,correctPost,incorrectPost):
    print (correctPre,incorrectPre,correctPost,incorrectPost)
    chi= 1.*(correctPre*incorrectPost - correctPost*incorrectPre)*(correctPre*incorrectPost - correctPost*incorrectPre)*(correctPre+incorrectPost+correctPost+incorrectPre)
    denom=1.0*((correctPre+correctPost)*(incorrectPost+incorrectPre)*(incorrectPost+correctPost)*(correctPre+incorrectPre))
    if denom==0:
        sys.stderr.write( 'ZEROZERO')
        #p?rint correctPre,incorrectPost,correctPost,incorrectPre
        chi=-1
    chi = chi/denom
    import scipy.stats as stat
    pval=stat.distributions.chi2.sf(chi,1)
    return pval
    
def get_stats(responsespre,responsespost,correctIndex,usedcitynames):
    pvals=[]
    TOTcorrectPre=0
    TOTcorrectPost=0
    TOTincorrectPre=0
    TOTincorrectPost=0
    for citnum in usedcitynames:
        correctPre=responsespre[citnum][correctIndex]
        incorrectPre=sum(responsespre[citnum])-correctPre
        correctPost=responsespost[citnum][correctIndex]
        incorrectPost=sum(responsespost[citnum])-correctPost
        TOTcorrectPre+=correctPre
        TOTcorrectPost+=correctPost
        TOTincorrectPre+=incorrectPre
        TOTincorrectPost+=incorrectPost
        pval=get_pvals(correctPre,incorrectPre,correctPost,incorrectPost)
        pvals.append(pval)

    #p?rint "III",TOTcorrectPre, TOTincorrectPre,TOTcorrectPost,TOTincorrectPost
    pval=get_pvals(TOTcorrectPre,TOTincorrectPre,TOTcorrectPost,TOTincorrectPost)
    pvals.append(pval)
    return pvals
    
def graph_pre_post(cityNames,ax,jpdf,fig,preAnswerByQ,postAnswerByQ, q,cumuData, doCumu,percent):
    responsespre=preAnswerByQ[q] #single q over different cities
    responsespost=postAnswerByQ[q]
  
    #setup
    smSpace=.1
    bigSpace=.2
    ID=sh.qIDs['pre'][q]
    Ques=sh.qDict['pre'][ID]

    numchoices=Ques.numberOfChoices

    width = (1 - bigSpace) / (numchoices*2)
    numcit=len(responsespre)
    fontsize=8
    colors=['#ab95d8','#f9cb8f','#cd7caa','#69caf4','#717263','#ffff66']

    #data & graphing functions
    usedcitynames, Xmax = set_data(ax,numchoices,numcit, responsespre, responsespost, colors, width,smSpace, bigSpace,q,doCumu,percent )
    if len(Ques.correctCharacter)>1:
        pvals=[-1]
    else:
        correctIndex=ord(Ques.correctCharacter)-65
        pvals=get_stats(responsespre,responsespost,correctIndex, usedcitynames)
        print "pvals are: " 
        print pvals
    
    set_ticks(cityNames,ax,usedcitynames, numchoices, width, smSpace, bigSpace, fontsize,pvals, percent)
    set_legend(q, numchoices,fontsize)
    set_title(ax,Ques)
    
    #plot
    plt.xlim(0, Xmax)
    if(percent==True):
        plt.ylim(0, 100)
    plt.tight_layout()
    return usedcitynames, pvals

def make_subplots_each_question(start,end,preAnswerByQ,postAnswerByQ,cityNames,arrayFiles,pdfName,cumuData,doCumu,percent):
    import os
    pvals=[]
    pdf = PdfPages(pdfName)
    stored_city_name=[]
    i=start
    while i<=end:
        print "\n\n\nprocess Q", i, 
        fig = plt.figure(figsize=(11,8.5), dpi=100)
        ax1 = fig.add_subplot(2,1,1)
        cit, pval = graph_pre_post(cityNames,ax1,pdf,fig,preAnswerByQ,postAnswerByQ,i,cumuData,doCumu,percent)
        stored_city_name.append(cit)
        pvals.append(pval)
        text= '* = change not significant (p$\geq$0.05)'
        text2='\ngreen = correct answer'
        pylab.figtext(0.01, .98, text, fontsize=8)
        pylab.figtext(0.01, .97, text2, fontsize=8, color='lime')
        i=i+1
        if i>start and i<=end :
            ax2 = fig.add_subplot(2,1,2)
            print "\n\n\n*process Q", i
            cit, pval =graph_pre_post(cityNames,ax2,pdf,fig,preAnswerByQ,postAnswerByQ,i,cumuData,doCumu,percent)
            stored_city_name.append(cit)
            pvals.append(pval)
            i=i+1
        pdf.savefig(fig, orientation='portrait')
    plt.close()
    pdf.close()
    return stored_city_name, pvals
    

import pylab
from matplotlib.backends.backend_pdf import PdfPages



def simplePlot(ax, data, cities,q):
    
    print "DATA", data, len(data) ,len(data[0])
    dim = len(data[0])
    w = 0.75
    dimw = w / dim
    ID=sh.qIDs['demo'][q]
    Ques=sh.qDict['demo'][ID]
    x = pylab.arange(len(data))
    for i in range(len(data[0])) :
        y = [d[i] for d in data]
        print "YYY",y
        ax.bar(x + i * dimw+ w / 2 , y, dimw, bottom=0.001,label=Ques.arrayMultipleChoices[i], color=sh.colors[i])
        
    pylab.gca().set_xticks(x + w )
    pylab.gca().set_xticklabels(cities, fontsize=5)
    set_legend2(q,10)
    set_title(ax,Ques)


def set_legend2(q,fontsize):
    legH=1.05
    legW=0.5
    legfontsize=fontsize-1
    ID=sh.qIDs['demo'][q]
    Ques=sh.qDict['demo'][ID]
    col=Ques.numCol
    legend=plt.legend(loc='upper center',bbox_to_anchor=(legW, legH),ncol=col, fontsize=legfontsize) 
    #legend.get_frame().set_facecolor('none')
    #legend.get_frame().set_linewidth(.5)




def graph_pre_post2(cityNames,ax,pdf,fig,demoAnswerByQ, q,cumuData, doCumu,percent):
    responsesdemo=demoAnswerByQ[q] #single q over different cities
  
    #setup
    smSpace=.1
    bigSpace=.2
    ID=sh.qIDs['demo'][q]
    Ques=sh.qDict['demo'][ID]

    numchoices=Ques.numberOfChoices

    width = (1 - bigSpace) / (numchoices)
    numcit=len(responsesdemo)
    fontsize=8
    colors=['#ab95d8','#f9cb8f','#cd7caa','#69caf4','#717263']

    #data & graphing functions
    #usedcitynames, Xmax = set_data(ax,numchoices,numcit, responsespre, responsespost, colors, width,smSpace, bigSpace,q,doCumu,percent )
    usedcitynames=cityNames
    simplePlot(ax, demoAnswerByQ[q], cityNames,q)
    #set_ticks(cityNames,ax,usedcitynames, numchoices, width, smSpace, bigSpace, fontsize,pvals, percent)
    #set_legend(q, numchoices,fontsize)
    #set_title(ax,Ques)
    
    #plot
    if(percent==True):
        plt.ylim(0, 100)
    plt.tight_layout()
    return usedcitynames

def make_subplots_each_question2(start,end,demoAnswerByQ,cityNames,arrayFiles,pdfName,cumuData,doCumu,percent):
    pdf = PdfPages(pdfName)
    stored_city_name=[]
    i=start
    while i<=end:
        print "\n\n\nprocess Q", i, 
        fig = plt.figure(figsize=(11,8.5), dpi=100)
        ax1 = fig.add_subplot(2,1,1)
        #######
        cit = graph_pre_post2(cityNames,ax1,pdf,fig,demoAnswerByQ,i,cumuData,doCumu,percent)
        
        stored_city_name.append(cit)
        i=i+1
        if i<=end:
            ax2 = fig.add_subplot(2,1,2)
            print "\n\n\n*process Q", i
            cit = graph_pre_post2(cityNames,ax2,pdf,fig,demoAnswerByQ,i,cumuData,doCumu,percent)
            stored_city_name.append(cit)
            i=i+1
        pdf.savefig(fig, orientation='portrait')
    plt.close()
    pdf.close()
    return stored_city_name
    
    

