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

import re#, string,sys
from arabic_const import *
HARAKAT_pat =re.compile(ur"[%s%s%s%s%s%s%s%s]"%(FATHATAN,DAMMATAN,KASRATAN,FATHA,DAMMA,KASRA,SUKUN,SHADDA) )
HARAKAT_NO_SHADDA_pat =re.compile(ur"[%s%s%s%s%s%s%s]"%(FATHATAN,DAMMATAN,KASRATAN,FATHA,DAMMA,KASRA,SUKUN) )



#strip tatweel from a word and return a result word
#--------------------------------------
def ar_strip_tatweel(w):
	"strip tatweel from a word and return a result word"
	return w.replace(TATWEEL,	'')

#strip tatweel and vowel from a word and return a result word but keep shadda
#--------------------------------------
def ar_strip_marks_keepshadda(w):
	return HARAKAT_NO_SHADDA_pat.sub('',w);
##	return re.sub(ur'[%s%s%s%s%s%s%s%s]' % (FATHATAN, DAMMATAN, TATWEEL,
##                                            KASRATAN, FATHA, DAMMA, KASRA, SUKUN),	'', w)


#strip tatweel and vowel from a word and return a result word
#--------------------------------------
def ar_strip_marks(w):
	"strip tatweel and vowel from a word and return a result word"
	return HARAKAT_pat.sub('',w);
##	return re.sub(ur'[%s%s%s%s%s%s%s%s%s]' % (FATHATAN, DAMMATAN, TATWEEL,
##                                            KASRATAN, FATHA, DAMMA, KASRA, SUKUN,SHADDA),	'', w)



#strip pounctuation from the text
#--------------------------------------
def ar_strip_punct(w):
    return re.sub(r'[%s%s%s%s\\]' % (string.punctuation, string.digits,
                                     string.ascii_letters, string.whitespace),
                  ' ', w)


#--------------------------------------
def replace_pos (word,rep, pos):
	return word[0:pos]+rep+word[pos+1:];

def is_valid_arabic_word(word):
    if word=="": return False;
##    word_nm=ar_strip_marks_keepshadda(word);
##    # the alef_madda is  considered as 2 letters
##    word_nm=word_nm.replace(ALEF_MADDA,HAMZA+ALEF);
    # in arabic ranges
##    if re.search(u"([^\u0621-\u0652%s%s%s])"%(LAM_ALEF, LAM_ALEF_HAMZA_ABOVE,LAM_ALEF_MADDA_ABOVE),word):
    if re.search(u"([^\u0621-\u0652\ufefb\ufef7\ufef5])",word):

        return False;

    elif re.match(u"([\d])+",word):
        return False;
##    elif word[0] in (WAW_HAMZA,YEH_HAMZA,FATHA,DAMMA,SUKUN,KASRA):
##        return False;
###  إذا كانت الألف المقصورة في غير آخر الفعل
    elif re.match(u"^(.)*[%s](.)+$"%ALEF_MAKSURA,word):
        return False;
    elif re.match(u"^(.)*[%s]([^%s%s%s])(.)+$"%(TEH_MARBUTA,DAMMA,KASRA,FATHA),word):
        return False;
    return True;


