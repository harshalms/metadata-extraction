import nltk
import csv
import os 
import docx2txt
from nltk.tokenize import sent_tokenize
import pandas as pd 
import sys
import n2w
import numpy as np
import glob
import datetime
import re
import docx2txt
from utils import extract_amount, get_all_patern
import pdb
import pickle
import argparse


def get_aggrement_val(Aggrement_Value, sentence):
    if type(Aggrement_Value)==np.float64:
        response=extract_amount(sentence)
        if len(response)!=0:
            for item in response:
                if item[-1]==Aggrement_Value:
                    return (item[0][0],item[0][1],'Aggrement_Value')

def get_aggrement_start_date(Aggrement_Start_Date, sentence):
    if type(Aggrement_Start_Date)==str:
        temp_list=Aggrement_Start_Date.split(".")
        if len(temp_list)==3:
            temp_list=[int(a) for a in temp_list]
            all_pattern=get_all_patern(temp_list)
            for temp_date in all_pattern:
                k=sentence.find(temp_date)
                if k!=-1:
                    return (k,k+len(temp_date),'start_date')

def get_aggrement_end_date(Aggrement_End_Date, sentence):
    if type(Aggrement_End_Date)==str:
        temp_list=Aggrement_End_Date.split(".")
        if len(temp_list)==3:
            temp_list=[int(a) for a in temp_list]
            all_pattern=get_all_patern(temp_list)
            for temp_date in all_pattern:
                k=sentence.find(temp_date)
                if k!=-1:
                    return (k,k+len(temp_date),'start_date')

def get_renewal_notice(Renewal_Notice, sentence):
    
    if type(Renewal_Notice)==np.float64:
        all_possible_word=get_checklist_for_renewal(Renewal_Notice)
        if all_possible_word!=None:
            for duration in all_possible_word:    
                k=sentence.find(duration)
                if k!=-1:
                    return (k,k+len(duration),'Renewal_Notice')

def get_party_one(Party_One, sentence):
    if type(Party_One)==str and sentence.find(Party_One)!=-1 :
        i = 0
        one_party = []
        while(True):
            k=sentence[i:].find(Party_One)
            temp=(i+k,i+k+len(Party_One),'Party_one')
            i=i+k+1
            one_party.append(temp)
            if sentence[i:].find(Party_One) == -1:
                return one_party

def get_party_two(Party_Two, sentence):
    if type(Party_Two)==str and sentence.find(Party_Two)!=-1:
        i = 0
        two_party = []
        while(True):
            k=sentence[i:].find(Party_Two)
            two_party.append((i+k, i+k+len(Party_Two), 'Party_Two'))
            i=i+k+1
            if sentence[i:].find(Party_Two) == -1:
                return two_party

def get_checklist_for_renewal(Renewal_Notice):
    temp=np.int64(Renewal_Notice//30)
    return [str(temp)+" months",n2w.convert(temp)+" months",n2w.convert(temp)+" month", str(temp)+" month"]

def get_all_sentence(list_sentence, df_row):
    Aggrement_Value=df_row['Aggrement Value'].values[0]
    Aggrement_Start_Date, Aggrement_End_Date=df_row['Aggrement Start Date'].values[0], df_row['Aggrement End Date'].values[0]
    Renewal_Notice=df_row['Renewal Notice (Days)'].values[0]
    Party_One, Party_Two=df_row['Party One'].values[0], df_row['Party Two'].values[0] 

    total_data=[]
    for sentence in list_sentence:
        annotatation_list=[]
        '''Aggrement Value'''
        aggre_val = get_aggrement_val(Aggrement_Value, sentence)
        if aggre_val:
            annotatation_list.append(aggre_val)
        '''Aggrement Start Date'''
        start_date = get_aggrement_start_date(Aggrement_Start_Date, sentence)
        if start_date:
            annotatation_list.append(start_date)

        '''Aggrement End Date'''
        end_date = get_aggrement_end_date(Aggrement_End_Date, sentence)
        if end_date:
            annotatation_list.append(end_date)
        '''Renewal Notice (Days)'''
        notice = get_renewal_notice(Renewal_Notice, sentence)
        if notice:
            annotatation_list.append(notice)
        '''Party One'''
        party_one = get_party_one(Party_One, sentence)
        if party_one:
            _ = [annotatation_list.append(x) for x in party_one]
        '''Party Two'''
        party_two = get_party_two(Party_Two, sentence)
    
        if party_two:
            _ = [annotatation_list.append(x) for x in party_two]
        if len(annotatation_list)>0:
            total_data.append((sentence,{'entities':annotatation_list}))
    return total_data

def trim_entity_spans(data: list) -> list:
    invalid_span_tokens = re.compile(r'\s')

    cleaned_data = []
    for text, annotations in data:
        entities = annotations['entities']
        valid_entities = []
        for start, end, label in entities:
            valid_start = start
            valid_end = end
            while valid_start < len(text) and invalid_span_tokens.match(
                    text[valid_start]):
                valid_start += 1
            while valid_end > 1 and invalid_span_tokens.match(
                    text[valid_end - 1]):
                valid_end -= 1
            valid_entities.append([valid_start, valid_end, label])
        cleaned_data.append([text, {'entities': valid_entities}])

    return cleaned_data



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Meta-Data-Extraction")
    parser.add_argument(
        "--folder_path", type=str, default="", help="Path to the training data folder"
    )

    parser.add_argument(
        "--label_file_path", type=str, default="", help="Path to the label data file"
    )
    
    args = parser.parse_args()
    path = args.folder_path
    label_file = args.label_file_path
    if not os.path.exists(path):
        print("path does not exist: %s" % path)

    if not os.path.exists(label_file):
        print(" set proper label file path, path does not exists %s"%label_file)
        sys.exit(0)
    df=pd.read_csv(label_file)
    list_doc=glob.glob(path+"/*docx")
    new_label_data = []
    for file_path in list_doc:
        File_name=os.path.basename(file_path)[:-9]
        text = docx2txt.process(file_path)
        list_sentence = [x.replace("\n", " ") for x in sent_tokenize(text)]
        row=df.loc[df['File Name'] == File_name]
        label_data=trim_entity_spans(get_all_sentence(list_sentence, row))
        new_label_data+=label_data

    if not os.path.exists('pickle_files'):
        os.makedirs('pickle_files')
    pickle_file = '_'.join(path.strip().split('/')[-1].split()) + '.pickle'
    with open('pickle_files/' + pickle_file, 'wb') as f:
        pickle.dump(new_label_data, f)