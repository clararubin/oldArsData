import scipy.stats as stat
import pandas as pd

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
    
def func(data, section, partition, correct_character, q_numbers):
    pre_correct = int(data.count_responses(
            q_number = q_numbers[0],
            subset = (partition, section),
            response = correct_character
            ))
    pre_incorrect = int(data.count_responses(
            q_number = q_numbers[0],
            subset = (partition, section)
            ) - pre_correct)
    post_correct = int(data.count_responses(
            q_number = q_numbers[1],
            subset = (partition, section),
            response = correct_character
            ))
    post_incorrect = int(data.count_responses(
            q_number = q_numbers[1],
            subset = (partition, section)
            ) - post_correct)
    
    return compute_pval(pre_correct, pre_incorrect, post_correct, post_incorrect)
    
def get_pvals(data, pre_number, section_names, graph_settings):
    
    correct_character = data.correct_character(pre_number)
    if pd.isnull(correct_character):
        return None
    
    partition = graph_settings.partition
    q_numbers = data.pre_post_of_pre(pre_number)
         
    return [
        func(data, section, partition, correct_character, q_numbers)
        for section in section_names
        ] 