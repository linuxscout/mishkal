#!/usr/bin/python
# -*- coding=utf-8 -*-
#************************************************************************
# $Id: ar_ctype.py,v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2009, Arabtechies, Arabeyes Taha Zerrouki
#
#  Elementary function to manipulate arabic texte
#
# -----------------
# Revision Details:    (Updated by Revision Control System)
# -----------------
#  $Date: 2009/06/02 01:10:00 $
#  $Author: Taha Zerrouki $
#  $Revision: 0.7 $
#  $Source: arabtechies.sourceforge.net
#
#***********************************************************************/

import re, string,sys
import types
from arabic_const import *
#from verb_const import *

#!/usr/bin/python
# -*- coding=utf-8 -*-
#---

#--------------------------------------
def replace_pos (word,rep, pos):
	return word[0:pos]+rep+word[pos+1:];
#--------------------------------------
def chomp(s):
  if (s.endswith('\n')):
    return s[:-1]
  else:
    return s;
HARAKAT_pat =re.compile(ur"^[%s%s%s%s%s%s%s%s]$"%(FATHATAN,DAMMATAN,KASRATAN,FATHA,DAMMA,KASRA,SUKUN,SHADDA) )
HARAKAT_NO_SHADDA_pat =re.compile(ur"^[%s%s%s%s%s%s%s]$"%(FATHATAN,DAMMATAN,KASRATAN,FATHA,DAMMA,KASRA,SUKUN) )
#--------------------------------------
def ar_isvowel(w):
	" return True if the letter is an arabic vowel. SHADDA is  a vowel."
	res=HARAKAT_pat.match(w);
	if res:return True;
	else: return False;

# return True if the letter is a tatweel.
#--------------------------------------
def ar_istatweel(w):
	"return True if the letter is a tatweel."
	if w==TATWEEL :  return True;
	else :return False;

#--------------------------------------
def ar_strip_vowel(w):
	"strip vowel from a word and return a result word"
	return HARAKAT_pat.sub('', w)


#strip tatweel from a word and return a result word
#--------------------------------------
def ar_strip_tatweel(w):
	"strip tatweel from a word and return a result word"
	return re.sub(ur'[%s]' % TATWEEL,	'', w)

#strip tatweel and vowel from a word and return a result word but keep shadda
#--------------------------------------
def ar_strip_marks_keepshadda(w):
	return re.sub(ur'[%s%s%s%s%s%s%s%s]' % (FATHATAN, DAMMATAN, TATWEEL,
                                            KASRATAN, FATHA, DAMMA, KASRA, SUKUN),	'', w)


#strip tatweel and vowel from a word and return a result word
#--------------------------------------
def ar_strip_marks(w):
	"strip tatweel and vowel from a word and return a result word"
	return re.sub(ur'[%s%s%s%s%s%s%s%s%s]' % (FATHATAN, DAMMATAN, TATWEEL,
                                            KASRATAN, FATHA, DAMMA, KASRA, SUKUN,SHADDA),	'', w)



#strip pounctuation from the text
#--------------------------------------
def ar_strip_punct(w):
    return re.sub(r'[%s%s%s%s\\]' % (string.punctuation, string.digits,
                                     string.ascii_letters, string.whitespace),
                  ' ', w)

def ar_before_last_letter(word):
    return word[-2:-1];

# return True if the given word have the same or the partial vocalisation like the pattern
#------------------------------------------------
def vocalizedlike( vocalized,word):
	vocalized=re.sub(u"[%s]"%FATHA,u"[%s]?"%FATHA,vocalized)
	vocalized=re.sub(u"[%s]"%KASRA,u"[%s]?"%KASRA,vocalized)
	vocalized=re.sub(u"[%s]"%DAMMA,u"[%s]?"%DAMMA,vocalized)
	vocalized=re.sub(u"[%s]"%SUKUN,u"[%s]?"%SUKUN,vocalized)
	vocalized=re.sub(u"[%s]"%SHADDA,u"[%s]?"%SHADDA,vocalized)
	vocalized="^"+vocalized+"$";
	pat=re.compile(vocalized);
	res=pat.match(word);
	if res : return True;
	else : return False;

# this function is to replace all letters non vowel to an unique symbole, to be used for test vowlization
#--------------------------------------
def replace_letters(word0):
	return re.sub(ur'[^%s%s%s%s%s%s%s%s]' % (FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA,
                                            SUKUN,SHADDA),	u'-', word0)
# للمقارنة بين كلمتين متساويتين في الطول إذا كانتا متشاكلتان: أي يتطابق تشكيلهما جزئيا أو كليا.
# لا يهم إن كانتا غير متساويتين في الحروف
# if verify_vowel_only is True: verify only the vowels
#else verify letters too,
#--------------------------------------
def equal_shakl(word0,wazn0,verify_vowel_only=False):
	if not verify_vowel_only :
		word=ar_strip_marks(word0);
		wazn=ar_strip_marks(wazn0);
		if word!=wazn : return False;
	else :
		if len(ar_strip_marks(word0))!=len(ar_strip_marks(wazn0)):
			return False;
		word=replace_letters(word0);
		wazn=replace_letters(wazn0);
	# j :word index
#	print 1;
	j=0;
	i=0;
	while i< len(wazn) and j<len(word):
#		print 2;
		wazn_i_isvowel=ar_isvowel(wazn[i]);
		word_j_isvowel=ar_isvowel(word[j]);
		if (wazn_i_isvowel) and (word_j_isvowel):
			if wazn[i]!=word[j]:
#				print 3;
				return False;
			else: j+=1;
		elif (wazn_i_isvowel) and (not word_j_isvowel):
#			print 4;
			pass;
		elif (not wazn_i_isvowel) and ( word_j_isvowel):
#			print 5;
			while (ar_isvowel(word[j])) :  j+=1;
			if  (wazn[i]!=word[j]): return False;
			else : j+=1;
		elif  (not wazn_i_isvowel) and (not word_j_isvowel):
			if wazn[i]!=word[j]:
#				print 7;
				return False;
			else: j+=1;
		i+=1;
		#strip last vowel
	while ( j<len(word) and ar_isvowel(word[j]) ):  j+=1;
	if(j<len(word)): return False;
	return True;

#--------------------------------------
#
#
#
#---------------------------------------
def is_valid_arabic_word(word):
    if len(word)==0: return False;
    word_nm=ar_strip_marks_keepshadda(word);
    # the alef_madda is  considered as 2 letters
    word_nm=word_nm.replace(ALEF_MADDA,HAMZA+ALEF);
    if word[0] in (WAW_HAMZA,YEH_HAMZA,FATHA,DAMMA,SUKUN,KASRA):
        return False;
#  إذا كانت الألف المقصورة في غير آخر الفعل
    if re.match(u"^(.)*[%s](.)+$"%ALEF_MAKSURA,word):
        return False;
    if re.match(u"^(.)*[%s]([^%s%s%s])(.)+$"%(TEH_MARBUTA,DAMMA,KASRA,FATHA),word):
        return False;
##    i=0;

    if re.search(u"([^\u0621-\u0652%s%s%s])"%(LAM_ALEF, LAM_ALEF_HAMZA_ABOVE,LAM_ALEF_MADDA_ABOVE),word):
        return False;
    if re.match(u"([\d])+",word):
        return False;
    return True;


