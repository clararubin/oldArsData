import scipy.stats as stat

def compute_pval(correctPre, incorrectPre, correctPost, incorrectPost):
    print correctPre,incorrectPre,correctPost,incorrectPost
    num = (correctPre*incorrectPost - correctPost*incorrectPre) * \
          (correctPre*incorrectPost - correctPost*incorrectPre) * \
          (correctPre+incorrectPost + correctPost+incorrectPre)
    den = (correctPre+correctPost)     * \
          (incorrectPost+incorrectPre) * \
          (incorrectPost+correctPost)  * \
          (correctPre+incorrectPre)
    chi = float(num) / den
    pval = stat.distributions.chi2.sf(chi, 1)
    return pval
    
def get_pvals(response_pair, correctIndex, used_city_names):
    pvals=[]
    TOTcorrectPre=0
    TOTcorrectPost=0
    TOTincorrectPre=0
    TOTincorrectPost=0
    for city in used_city_names:
        print(city)
        correctPre = response_pair['pre'][city][correctIndex]
        incorrectPre=sum(response_pair['pre'][city])-correctPre
        correctPost=response_pair['post'][city][correctIndex]
        incorrectPost=sum(response_pair['post'][city])-correctPost
        TOTcorrectPre+=correctPre
        TOTcorrectPost+=correctPost
        TOTincorrectPre+=incorrectPre
        TOTincorrectPost+=incorrectPost
        pvals.append( compute_pval(correctPre,incorrectPre,correctPost,incorrectPost) )

    pvals.append( compute_pval(TOTcorrectPre,TOTincorrectPre,TOTcorrectPost,TOTincorrectPost) )
    return pvals