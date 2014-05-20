#!/usr/bin/python
# -*- coding=utf-8 -*-
#
import re, string,sys
from arabic_const import *


pronouns=(
YEH,
KAF,
HEH,
KAF+MEEM,
KAF+NOON,
HEH+ALEF,
HEH+MEEM,
HEH+NOON,
NOON+ALEF,
KAF+MEEM+ALEF,
HEH+MEEM+ALEF,
);
jonction=(WAW,FEH);
prepositions=(BEH,KAF,LAM);
definition=(u''.join([ALEF,LAM]));

def generate_allforms(word,has_pronouns=True,has_jonction=True,has_preposition=True,has_definition=True,has_interrog=True):
    list_idafa=[word];
    if has_pronouns:
        for p in pronouns:
    # convert ALEF_mAKSURA to YEH
            list_idafa.append(word+"-"+p);
    if has_definition:
        list_idafa.append(ALEF+LAM+"-"+word)
    list2=[]
    if has_preposition :
        for w in list_idafa:
            list2.append(w)
            for pr in prepositions:
                list2.append(pr+"-"+w);
    else:
        list2=list_idafa;
    list3=[]
    if has_jonction :
        for w in list2:
            list3.append(w)
            for jo in jonction:
                list3.append(jo+"-"+w);
    list4=[]
    if has_interrog :
        for w in list3:
            list4.append(w)
            list4.append(ALEF_HAMZA_ABOVE+"-"+w);
    else:
        list4=list3;
    return list4;


def standardize_form(word):
    word=re.sub(u"%s-"%ALEF_MAKSURA,ALEF,word)
    word=re.sub(u"%s-"%TEH_MARBUTA,TEH,word)
    word=re.sub(u"%s-%s%s"%(LAM,ALEF,LAM),LAM+LAM,word)
    word=re.sub(u"-",'', word);
    return word;
def generate(word):
    genlist=generate_allforms(word);
    result_list=[];
    for oneword in genlist:
        result_list.append({'affixed':oneword,'standard':standardize_form(oneword)} )
    return result_list;

