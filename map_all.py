import spacy
import numpy as np
from spacy import displacy
from collections import Counter
import en_core_web_sm
import pandas as pd
import sys
from fuzzywuzzy import process
nlp = en_core_web_sm.load()

#inp = ''
inp = sys.stdin.readline()
inp = inp.rstrip()
doc = nlp(inp)
res = [(X.text, X.label_) for X in doc.ents]
print(res)
print(type(res))

dataframe1 = pd.read_csv('reg_cmp_acro_sec.csv')
new_df1 = pd.read_csv('reg_cmp_acro_sec.csv')
col1 = new_df1.columns
cols_reg = np.array(new_df1[col1[1]])
cols_cmp = np.array(new_df1[col1[2]])
cols_sec = np.array(new_df1[col1[4]])
len1 = len(new_df1.index)

dataframe2 = pd.read_csv('Comp_att.csv')
new_df2 = pd.read_csv('Comp_att.csv')
col2 = new_df2.columns
cols_cmp2 = np.array(new_df2[col2[1]])
cols_att = np.array(new_df2[col2[2]])
len2 = len(new_df2.index)

def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1

len_res = len(res)
i = 0

while i < len_res :
    if res[i][0] in inp :
        pos = find_str(inp,res[i][0])
        print(pos)
        len_sp = len(res[i][0])
        print(len_sp)
        inp1 = inp[0:pos]
        inp2 = inp[pos+len_sp:]
        inp = inp1 + inp2
    i = i + 1

print(inp)
k = 0
i = 0
flg_match = 0
pos_st = 0
pos_end = len2

if len_res == 1:
    if res[0][1] == 'ORG' or res[0][1] == 'PERSON':
        print('CMP')
        res_cmp = process.extractBests(res[0][0], cols_cmp, score_cutoff=80, limit=1)
        while i < len2:
            if res_cmp[0][0] == cols_cmp2[i] and flg_match == 0:
                flg_match = 1
                pos_st = i
            elif res_cmp[0][0] != cols_cmp2[i] and flg_match == 1:
                pos_end = i
                flg_match = 0
            i = i + 1
        k = k + 1
        print(pos_st, pos_end)
        new_df2 = new_df2.drop(new_df2.index[pos_end:len2])
        new_df2 = new_df2.drop(new_df2.index[0:pos_st])
        new_df2 = new_df2.drop('Id', axis=1)
        new_df2 = new_df2.drop('Company_Name', axis=1)
        res_att = process.extractBests(inp, cols_att, score_cutoff=70, limit=1)
        if res_att:
            i = 0
            len_att = pos_end - pos_st
            ar = [0] * len_att
            while i < len_att:
                if res_att[0][0] != cols_att[i + pos_st]:
                    ar[i] = 1
                i = i + 1
            i = i - 1
            while i >= 0:
                if ar[i] == 1:
                    new_df2 = new_df2.drop(new_df2.index[i])
                i = i - 1
            print(format(new_df2))
        else:
            print(format(new_df2))

    elif res[0][1] == 'GPE' or res[0][1] == 'LOC':
        print('REG')
        res_reg = process.extractBests(res[0][0], cols_reg, score_cutoff=80, limit=1)
        arr = [0] * len1
        print(len1)
        while i < len1:
            if res_reg[0][0] != cols_reg[i]:
                arr[i] = 1
            i = i + 1
        i = i - 1
        while i >= 0:
            if arr[i] == 1:
                new_df1 = new_df1.drop(new_df1.index[i])
            i = i - 1
        res_sec = process.extractBests(inp, cols_sec, score_cutoff=70, limit=1)
        i = 0
        if res_sec :
            len_sec = len(new_df1)
            ar = [0]*len_sec
            cols_sec = np.array(new_df1[col1[4]])
            while i < len_sec :
                if res_sec[0][0] != cols_sec[i] :
                    ar[i] = 1
                i = i + 1
            i = i - 1
            while i >= 0 :
                if ar[i] == 1 :
                    new_df1 = new_df1.drop(new_df1.index[i])
                i = i - 1
        print(format(new_df1))


elif len_res == 2:

    while i < len_res:
        if (res[i][1] == 'ORG' or res[i][1] == 'PERSON') and (res[i + 1][1] == 'GPE' or res[i + 1][1] == 'LOC'):
            res_cmp = process.extractBests(res[i][0], cols_cmp, score_cutoff=80, limit=1)
            res_reg = process.extractBests(res[i + 1][0], cols_reg, score_cutoff=80, limit=1)
            print(res_cmp, res_reg)
        elif (res[i][1] == 'ORG' or res[i][1] == 'PERSON') and (res[i - 1][1] == 'GPE' or res[i - 1][1] == 'LOC'):
            res_cmp = process.extractBests(res[i][0], cols_cmp, score_cutoff=80, limit=1)
            res_reg = process.extractBests(res[i - 1][0], cols_reg, score_cutoff=80, limit=1)
            print(res_cmp, res_reg)
        i = i + 1
    flg_match = 0
    pos_st = 0
    i = 0
    pos_end = len2
    k = 0
    while k < len1:
        if res_cmp[0][0] == cols_cmp[k] and res_reg[0][0] == cols_reg[k]:
            while i < len2:
                if res_cmp[0][0] == cols_cmp2[i] and flg_match == 0:
                    flg_match = 1
                    pos_st = i
                elif res_cmp[0][0] != cols_cmp2[i] and flg_match == 1:
                    pos_end = i
                    flg_match = 0
                i = i + 1
        k = k + 1
    print(pos_st, pos_end)
    new_df2 = new_df2.drop(new_df2.index[pos_end:len2])
    new_df2 = new_df2.drop(new_df2.index[0:pos_st])
    new_df2 = new_df2.drop('Id', axis=1)
    new_df2 = new_df2.drop('Company_Name', axis=1)

    res_att = process.extractBests(inp, cols_att, score_cutoff=70, limit=1)
    if res_att:
        i = 0
        len_att = pos_end - pos_st
        ar = [0] * len_att
        while i < len_att:
            if res_att[0][0] != cols_att[i + pos_st]:
                ar[i] = 1
            i = i + 1
        i = i - 1
        while i >= 0:
            if ar[i] == 1:
                new_df2 = new_df2.drop(new_df2.index[i])
            i = i - 1
        print(format(new_df2))
    else:
        print(format(new_df2))