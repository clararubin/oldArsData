import matplotlib.pyplot as plt
from matplotlib import pylab

from matplotlib.backends.backend_pdf import PdfPages

d=[[[20, 44, 25, 26, 7],
  [26, 54, 11, 23, 8],
  [12, 25, 16, 25, 8],
  [7, 18, 39, 14, 3]],
 [[77, 81], [34, 94], [38, 57], [60, 36]],
 [[67, 3, 7, 38, 9, 11, 24],
  [42, 4, 13, 31, 9, 9, 21],
  [60, 1, 5, 8, 8, 12, 9],
  [43, 5, 7, 20, 3, 9, 11]],
 [[98, 13, 19, 3, 8, 3, 1, 19],
  [60, 17, 13, 3, 11, 3, 2, 14],
  [49, 8, 15, 2, 9, 4, 2, 14],
  [63, 7, 7, 2, 6, 2, 0, 10]],
 [[27, 25, 24, 18, 77],
  [25, 13, 11, 12, 71],
  [16, 8, 5, 12, 61],
  [24, 13, 5, 12, 46]],
 [[14, 40, 42, 35, 32],
  [18, 30, 42, 19, 19],
  [24, 28, 20, 17, 16],
  [9, 19, 19, 29, 17]],
 [[79, 59, 20], [66, 58, 7], [62, 31, 7], [66, 27, 2]]]



fig = plt.figure(figsize=(11,8.5), dpi=100)
ax1 = fig.add_subplot(2,1,1)


def simplePlot2(ax, data):
    print "DATA", data, len(data) ,len(data[0])
    
    dim = len(data[0])
    w = 0.75
    dimw = w / dim
    
    x = pylab.arange(len(data))
    for i in range(len(data[0])) :
        y = [d[i] for d in data]
        print "Y", y
        ax.bar(x + i * dimw+ w / 2 , y, dimw, bottom=0.001)
    pylab.gca().set_xticks(x + w )
    
    plt.show()

#def simplePlot(data):
#    fig = plt.figure()
#    
#    
#    dim = len(data[0])
#    w = 0.75
#    dimw = w / dim
#    
#    x = pylab.arange(len(data))
#    for i in range(len(data[0])) :
#        y = [d[i] for d in data]
#        bar = pylab.bar(x + i * dimw+ w / 2 , y, dimw, bottom=0.001)
#    pylab.gca().set_xticks(x + w )
#    
#    plt.show()
    
    
#        series=ax.bar(Xvals, Yvals, color=thiscolor,width=.8*width, label=Ques.arrayMultipleChoices[choicenum],edgecolor = edgecolor, linewidth=.7)
simplePlot2(ax1,d[3])
    
#for dd in d:
#    simplePlot(dd)