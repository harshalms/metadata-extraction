import spacy
import os
import pickle
import pandas as pd 
from spacy.gold import GoldParse
from spacy.scorer import Scorer
import glob
def evaluate(ner_model, examples):
    scorer = Scorer()
    for i in examples:
        input_=i[0]
        annot=i[1]['entities']
        doc_gold_text = ner_model.make_doc(input_)
        gold = GoldParse(doc_gold_text, entities=annot)
        pred_value = ner_model(input_)
        scorer.score(pred_value, gold)
    metric=scorer.scores
    total_metric=[['total accuracy:',metric['ents_p'],metric['ents_r'],metric['ents_f']]]
    NER_accuracy_per_field= metric['ents_per_type']
    for key in NER_accuracy_per_field:
        value=NER_accuracy_per_field[key]
        print(key,NER_accuracy_per_field[key])
        total_metric.append([key,value['p'],value['r'],value['f']])
    print(total_metric)
    df=pd.DataFrame(total_metric)
    df.to_csv(file_name_accuracy_matric,header=["field",'precision','recall','f score'])
    return scorer.scores

if __name__=='__main__':
    model_path='/home/user/Desktop/nlp/code/model'

    pkl_file='/home/user/Desktop/nlp/code/my_val_pickle.pickle'
    model=spacy.load(model_path)
    data=pickle.load(open(pkl_file,'rb'))
    file_to_save_accuracy='accuracy_spacy_'+os.path.basename(pkl_file)[:-3]+"csv"
    file_name_accuracy_matric=os.path.join(model_path,file_to_save_accuracy)


    metric=evaluate(model,data)