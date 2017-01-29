import os
import setup
import graphing
import shared as sh
from pandas import *

reload(setup)
reload(graphing)
reload(sh)

def printCSV(preQ, postQ,cnames, fname):
    f = open(fname, 'w')
    f = open(fname, 'a')
    ids = sh.qIDs['pre']
    for item in range(len(preQ)):
        qt = sh.qDict['pre'][ids[item]].questionText
        mc = sh.qDict['pre'][ids[item]].arrayMultipleChoices
        
        df = DataFrame(preQ[item], columns=mc, index=cnames)
        #tot=DataFrame(df.sum(),columns=["Cumulative"]).T
        #df=df.append(tot)
        df = df.loc[(df!=0).any(1)]

        f.write("%s\n\n" % qt)
        f.write("\nPRE:")
        df.to_csv(f, mode='a', header =qt)
        
        df = DataFrame(postQ[item], columns=mc, index=cnames)
        #tot=DataFrame(df.sum(),columns=["Cumulative"]).T
        #df=df.append(tot)
        df = df.loc[(df!=0).any(1)]

        f.write("\n\nPOST:")
        df.to_csv(f, mode='a', header =qt)
        f.write("\n\n\n\n")
    f.close()
    


def convertPerc(df):
    perc = DataFrame()
    rows = df.index
    for c in rows:
        perc[c]= df.loc[c].div(df.loc[c].sum()).mul(100)
    return perc.T

    
def printCSVpercent(preQ, postQ,cnames, fname):
    f = open(fname, 'w')
    f = open(fname, 'a')
    ids = sh.qIDs['pre']
    pandas.set_option('precision', 2)

    for item in range(len(preQ)):
        qt = sh.qDict['pre'][ids[item]].questionText
        mc = sh.qDict['pre'][ids[item]].arrayMultipleChoices
        
        pre = DataFrame(preQ[item], columns=mc, index=cnames)
        #tot=DataFrame(pre.sum(),columns=["Cumulative"]).T
        #pre=pre.append(tot)
        pre = convertPerc(pre)
        pre = pre.dropna()
        pre=pre.round(decimals=2)
        pre = pre .astype(str) + '%'
        
        #df['time']='pre'
        cols = pre.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        pre = pre[cols]

        f.write("%s\n\n" % qt)
        
        df = DataFrame(postQ[item], columns=mc, index=cnames)
        #tot=DataFrame(df.sum(),columns=["Cumulative"]).T
        #df=df.append(tot)
        df = convertPerc(df)
        df = df.dropna()
        df=df.round(decimals=2)
        df = df .astype(str) + '%'
        
        #df['time']='post'
        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]

        
        com = pandas.concat([pre,df],keys=['pre','post'])
        com=com.sortlevel(1)
        com=com.swaplevel(0,1)


        f.write("\n\n")
        com.to_csv(f, mode='a', header =qt)
        f.write("\n\n\n\n")

    f.close()