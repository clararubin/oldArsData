import sys
sys.path.append("../../input")

import setup
import graphing
import shared as sh
import common_runner
import outside_data_2016 as out16
reload(setup)
reload(graphing)
reload(sh)
reload(common_runner)
reload(out16)

def run16():
    questions_filepath = sh.QFILE16    
    sh.qDict, sh.qIDs = setup.import_questions(questions_filepath)
    
    pdf_filenames = sh.pdf_name_list('psych update 2016 ARS')  
    
    ##following 2 lines prob dont work
    doCumu=True
    percent=True
    
    preAnswerByQ,postAnswerByQ,cityNames,cumuData,demoAnswerByQ = setup.responses_init(sh.arrayFiles16)
    
    cityNames += ["Medscape", "myCME"]
    numQs = 19
    
    for i in range(numQs+1):
        if i in (0,1,2):
            preAnswerByQ[i].append(out16.kr_medsc_pre[i])
            postAnswerByQ[i].append(out16.kr_medsc_post[i])
            preAnswerByQ[i].append(out16.kr_mycme_pre[i])
            postAnswerByQ[i].append(out16.kr_mycme_post[i])
        elif i in (3,4,5):
            preAnswerByQ[i].append(out16.td_medsc_pre[i-3])
            postAnswerByQ[i].append(out16.td_medsc_post[i-3])
            preAnswerByQ[i].append(out16.td_mycme_pre[i-3])
            postAnswerByQ[i].append(out16.td_mycme_post[i-3])
        else:
            length= len(preAnswerByQ[i][0])
            preAnswerByQ[i].append([0]*length)
            postAnswerByQ[i].append([0]*length)
            preAnswerByQ[i].append([0]*length)
            postAnswerByQ[i].append([0]*length)
    
    common_runner.runBySection(
            "perc", pdf_filenames, sh.sections16, preAnswerByQ, postAnswerByQ, cityNames,
            cumuData ,doCumu, percent, sh.arrayFiles16)


run16()
