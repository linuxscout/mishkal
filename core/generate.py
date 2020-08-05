#!/usr/bin/python
# -*- coding=utf-8 -*-
#
import re, string,sys
# from arabic_const import *
sys.path.append('mishkal/lib/');
from pyarabic.araby import *
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
	mylist=[word+FATHA, word+DAMMA, word+KASRA];
	temp=[];
	if has_preposition :
		for w in mylist:
			if w.endswith(KASRA):
#				temp.append(w)
				for pr in prepositions:
					temp.append(pr+"-"+w);
	mylist+=temp;
	temp=[];
	if has_jonction :
		for w in mylist:
#			temp.append(w)
			for jo in jonction:
				temp.append(jo+"-"+w);
	mylist+=temp;
	temp=[];
	if has_interrog :
		for w in mylist:
#			temp.append(w)
			temp.append(ALEF_HAMZA_ABOVE+"-"+w);
	mylist+=temp;
	temp=[];
	
	if has_pronouns:
		for word in mylist:
			for p in pronouns:
				if p==YEH and not word.endswith(KASRA):
					pass;
				else:
				# convert ALEF_mAKSURA to YEH
					if word.endswith(ALEF_MAKSURA):
						temp.append(word[:-1]+ALEF+"-"+p);
					elif word.endswith(HAMZA+KASRA):
						temp.append(word[:-2]+YEH_HAMZA+KASRA+"-"+p);
					elif word.endswith(HAMZA+DAMMA):
						temp.append(word[:-2]+WAW_HAMZA+DAMMA+"-"+p)
					else:
						temp.append(word+"-"+p);
			# add alef lam ta3rif
			if has_definition:
				temp.append(ALEF+LAM+"-"+word)
	mylist+=temp;
	return mylist;


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

