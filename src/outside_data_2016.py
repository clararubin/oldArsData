def addArrays(a,b):
    #example inputs: [3,5,7], [1,2,3,4,5,6]
    #example output: [4,7,10]
    return map((lambda (x,y): x+y), zip(a,b))


'''TD module'''

#MEDSCAPE 2016 Q2
td_medsc_pre_q2 = [[224,226,1274,313,451],[180,28,46,2074,159],[392,321,735,236,803]]
td_medsc_post_q2 = [[15,15,2324,17,20],[15,3,12,2345,13],[16,2321,28,11,16]]


td_medsc_pre_q3 = [[262,270,1483,365,505],[213,43,51,2339,178],[425,436,856,257,910]]
td_medsc_post_q3 = [[15,19,3166,15,21],[18,4,14,3188,12],[15,3161,31,10,19]]

td_medsc_pre=[]
td_medsc_post=[]

for i in range(3):
    pre= addArrays(td_medsc_pre_q2[i], td_medsc_pre_q3[i])
    td_medsc_pre.append(pre)
    post= addArrays(td_medsc_post_q2[i], td_medsc_post_q3[i])
    td_medsc_post.append(post)


#MYCME
td_mycme_pre = [[48,34,134,21,48],[44,18,10,193,20],[58,39,61,26,101]]
td_mycme_post = [[0,0,259,0,0],[0,0,0,259,0],[0,259,0,0,0]]    



'''Managing Mixed Depression (Kraeplin & Beyond) module'''

#MYCME
kr_mycme_pre = [[110,78,93,51,77],[98,51,108,126,26],[59,72,87,108,83]]
kr_mycme_post = [[0,0,0,0,346],[0,0,0,346,0],[0,346,0,0,0]]

#MEDSCAPE 2016 Q2
kr_medsc_pre_q2 = [[224,194,278,67,470],[247,58,322,550,56],[83,230,242,401,277]]
kr_medsc_post_q2 = [[25,13,26,9,1782],[19,9,28,1787,11],[13,1761,27,26,28]]

#MEDSCAPE 2016 Q3
kr_medsc_pre_q3 = [[270,240,341,90,567],[309,76,375,678,70],[106,283,307,474,338]]
kr_medsc_post_q3 = post =[[21,19,23,9,2468],[19,11,25,2474,11],[14,2440,30,30,26]]

#ADD MEDSCAPE Q2 & Q3
kr_medsc_pre = []
kr_medsc_post = []

for i in range(3):
    pre= addArrays(kr_medsc_pre_q2[i], kr_medsc_pre_q3[i])
    kr_medsc_pre.append(pre)
    post= addArrays(kr_medsc_post_q2[i], kr_medsc_post_q3[i])
    kr_medsc_post.append(post)

def add_outside_responses(responses_data):
    responses_data.cityNames += ["Medscape", "myCME"]
    numQs = 19
    for i in range(numQs+1):
        if i in (0,1,2):
            responses_data.preAnswerByQ[i].append(kr_medsc_pre[i])
            responses_data.postAnswerByQ[i].append(kr_medsc_post[i])
            responses_data.preAnswerByQ[i].append(kr_mycme_pre[i])
            responses_data.postAnswerByQ[i].append(kr_mycme_post[i])
        elif i in (3,4,5):
            responses_data.preAnswerByQ[i].append(td_medsc_pre[i-3])
            responses_data.postAnswerByQ[i].append(td_medsc_post[i-3])
            responses_data.preAnswerByQ[i].append(td_mycme_pre[i-3])
            responses_data.postAnswerByQ[i].append(td_mycme_post[i-3])
        else:
            length = len(responses_data.preAnswerByQ[i][0])
            responses_data.preAnswerByQ[i].append([0]*length)
            responses_data.postAnswerByQ[i].append([0]*length)
            responses_data.preAnswerByQ[i].append([0]*length)
            responses_data.postAnswerByQ[i].append([0]*length)
