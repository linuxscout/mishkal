#!/usr/bin/python
# -*- coding = utf-8 -*-
#************************************************************************
# $Id: verb_valid.py, v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2009, Arabtechies, Arabeyes Taha Zerrouki
#
#  Elementary function to validate verbs 
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
"""
Basic routines to validate verbs
ar_verb
"""
import re
# import string
# import sys
# import os
# import types
# from arabic_const import *
import libqutrub.verb_const as vconst #~ from verb_const import *
# import ar_ctype 
import pyarabic.araby as araby
from pyarabic.araby import FATHA,   SHADDA,  HAMZA, ALEF, \
 NOON,   ALEF_HAMZA_ABOVE, ALEF_HAMZA_BELOW, ALEF_MADDA, \
  ALEF_MAKSURA, BEH, DAD, DAL, DAMMATAN, FATHATAN, FEH, GHAIN, HAH, \
 HEH, JEEM, KAF, KASRATAN, KHAH, LAM, REH, SAD, SHEEN, TAH, TEH, \
 TEH_MARBUTA, THAL, THEH, YEH, ZAH, ZAIN
#used to
VALID_INFINITIVE_VERB6_PATTERN = \
re.compile(u"^است...|ا..ن..|ا..و..|ا..ا.ّ|ا....ّ|ا.ّ.ّ.|ا.ّا..$", re.UNICODE)

VALID_INFINITIVE_VERB4_PATTERN = re.compile(\
u"^([%s%s][^%s]{2}.|[^%s%s]%s[^%s%s].|[^%s%s]{2}%s[^%s]|[^%s%s]{4})$"\
%(ALEF_HAMZA_ABOVE, HAMZA, SHADDA, ALEF, SHADDA, ALEF, ALEF, SHADDA, ALEF,
 SHADDA, SHADDA, SHADDA, ALEF, SHADDA), re.UNICODE)

VALID_INFINITIVE_VERB5_PATTERN = re.compile( u"|".join([
                                    u"^ا...ّ$", 
            # حالة اتخذ أو اذّكر أو اطّلع
            u"^%s[%s%s%s]%s..$"%(ALEF, TEH, THAL, TAH, SHADDA), 
            # حالة اتخذ أو اذّكر أو اطّلع
           u"^ا[تذط]ّ[^اّ][^اّ]$", 
            # انفعل
            u"^ان...$", 
            #افتعل
            u"^(ازد|اصط|اضط)..$"
            u"^ا[^صضطظد]ت..$", 
            u"^ا...ّ$", 
            # حالة اتخذ أو اذّكر أو اطّلع
             u"^ا.ّ..$", 
             u"^ا...ى$", 
             ]) , re.UNICODE)

#####################################
#{validation functions
#####################################
def is_valid_infinitive_verb(word, vocalized = True):
    """
    Determine if the given word is a valid infinitive form of an arabic verb.
    A word is not valid  infinitive if
        - lenght < 3 letters.
        - starts with : ALEF_MAKSURA, WAW_HAMZA, YEH_HAMZA, HARAKAT
        - contains TEH_MARBUTA, Tanwin
        - contains non arabic letters.
        - contains ALEF_MAKSURA not in the end.
        - contains double haraka : a warning
    @param word: given word.
    @type word: unicode.
    @param is_vocalized: if the given word is vocalized.
    @type is_vocalized:Boolean, default(True).
    @return: True if the word is a valid infinitive form of verb.
    @rtype: Boolean.
    """
    # test if the word is an arabic valid word, 
    if not  araby.is_arabicword(word):
        return False
    if vocalized :
        word_nm  =  araby.strip_harakat(word)
    else:
        word_nm = word
    # the alef_madda is  considered as 2 letters

    word_nm = word_nm.replace(ALEF_MADDA, HAMZA+ALEF)
    length = len(word_nm)

    # lenght with shadda must be between 3 and 6
    if length < 3  or length >= 7:
        return False
    # a 3 length verb can't start by Alef or Shadda, 
    #and the second letter can't be shadda
    elif length == 3 and (word_nm[0] == ALEF or word_nm[0] == SHADDA \
    or word_nm[1] == SHADDA):
        return False

    # a 5 length verb must start by ALEF or TEH
    elif length == 5 and word_nm[0] not in (TEH, ALEF):
        return False
    # a 6 length verb must start by ALEF
    elif length == 6 and word_nm[0] !=  ALEF:
        return False

    # contains some invalide letters in verb
    elif re.search(u"[%s%s%s%s%s]"%(ALEF_HAMZA_BELOW, TEH_MARBUTA, 
    DAMMATAN, KASRATAN, FATHATAN), word):
        return False
    # contains some SHADDA sequence letters in verb
    # Like shadda shadda, shadda on alef, start  
    # by shadda, shadda on alef_ maksura, 
    # ALEF folowed by (ALEF, ALEF_MAKSURA)
    # ALEF Folowed by a letter and ALEF
    # end with ALEF folowed by (YEH, ALEF_MAKSURA)
    # first letter is alef and ALLw alef and two letters aand shadda
    elif re.search(u"([%s%s%s]%s|^%s|^%s..%s|^.%s|%s.%s|%s%s|%s[%s%s]$)"%(
    ALEF, ALEF_MAKSURA, SHADDA, SHADDA, SHADDA, ALEF, SHADDA, SHADDA, 
    ALEF, ALEF, ALEF, ALEF, ALEF, ALEF_MAKSURA, YEH), word_nm):
        return False


    # Invalid root form some letters :
    #~ # initial YEH folowed by 
    #~ ((THEH, JEEM, HAH, KHAH, THAL, ZAIN, SHEEN, SAD, DAD,
     #~ TAH, ZAH, GHAIN, KAF, HEH, YEH))
    elif re.search(u"^%s[%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s]"%(
    YEH, THEH, JEEM, HAH, KHAH, THAL, ZAIN, SHEEN, SAD, DAD, 
    TAH, ZAH, GHAIN, KAF, HEH, YEH), word_nm):
        return False


       # TEH After (DAL, THAL, TAH, ZAH, DAD)
    elif re.search(u"[%s%s%s%s%s]%s"%(DAL, THAL, DAD, TAH, ZAH, TEH), word_nm):
        return False
    # Contains invalid root sequence in arabic, near in phonetic
    # like BEH and FEH, LAM And REH
    elif re.search(u"%s%s|%s%s|%s%s|%s%s|%s%s|%s%s|%s%s"%(
    LAM, REH, REH, LAM, FEH, BEH, BEH, FEH, NOON,
     LAM, HEH, HAH, HAH, HEH), word_nm):
        return False


    # in non 5 letters verbs :initial TEH followed by  
    # (THEH, DAL, THAL, ZAIN, SHEEN, SAD, DAD, TAH, ZAH)
    elif length !=  5 and word_nm.startswith(TEH) and word_nm[1] in (
    TEH, THEH, DAL, THAL, ZAIN, SHEEN, SAD, DAD, TAH, ZAH):
        return False
    # if word start by the same letter doubled
    elif word_nm[0] == word_nm[1] and word[0] !=  TEH:
        return False

    #verify the wazn of the verb
    elif length == 3:
        if re.match("^[^%s][^%s].$"%(ALEF, SHADDA), word_nm):
            return True
    # الأوزان المقبولة هي فعل، فعّ،
    # الأوزان غير المقبولة
    # اعل، فّل
        else: return False
    elif length == 4:
    #1- أفعل، 2- فاعل، 3 فعّل 4 فعلل
        if re.match(\
        "^([%s%s][^%s]{2}.|[^%s%s]%s[^%s%s].|[^%s%s]{2}%s[^%s]|[^%s%s]{4})$"\
        %(ALEF_HAMZA_ABOVE, HAMZA, SHADDA, ALEF, SHADDA, ALEF, ALEF, SHADDA,
         ALEF, SHADDA, SHADDA, SHADDA, ALEF, SHADDA), word_nm):

            return True
    # الأوزان المقبولة هي فعل، فعّ،
    # الأوزان غير المقبولة
    #     افعل: يجب تثبيت همزة القطع
    #فّعل، فعلّ: الشدة لها موضع خاص
    # فعال، فعلا: للألف موضع خاص
        else: return False
    elif length == 5:

        if  word_nm.startswith(ALEF):
            if re.match(u"^ا...ّ$", word_nm):
                return True
            # حالة اتخذ أو اذّكر أو اطّلع
            if re.match(u"^%s[%s%s%s]%s..$"%(ALEF, TEH, THAL, TAH, SHADDA), \
             word_nm):
                return True

            # انفعل
            elif re.match(u"^ان...$", word_nm):
                return True
            #افتعل
            elif re.match(u"^(ازد|اصط|اضط)..$", word_nm):
                return True
            elif re.match(u"^ا[^صضطظد]ت..$", word_nm):
                return True
            elif re.match(u"^ا...ّ$", word_nm):
                return True
            # حالة اتخذ أو اذّكر أو اطّلع
            elif re.match(u"^ا.ّ..$", word_nm):
                return True
            elif re.match(u"^ا...ى$", word_nm):
                return True
            else: return False
        elif word_nm.startswith(TEH):
            return True
        else:
            return False

    # الأوزان المقبولة هي فعل، فعّ،
    # الأوزان غير المقبولة
    #للشدة موضع خاص: تفعّل، افتعّ
    # للألف مواضع خاصة،
    elif length == 6:
        if not (word_nm.startswith(ALEF) or word_nm.startswith(TEH)):
            return False
        if VALID_INFINITIVE_VERB6_PATTERN.match(word_nm):
            return True
    # الأوزان المقبولة هي فعل، فعّ،
    # الأوزان غير المقبولة
    #للشدة موضع خاص: تفعّل، افتعّ
    # للألف مواضع خاصة،
        else: return False
    return True


def suggest_verb(verb):
    """
    Generate a list of valid infinitive verb for an invalid infinitive form.
    @param verb: given verb, of invalid infinitive form.
    @type verb: unicode.
    @return: a list of suggested infinitive verb forms
    @rtype: list of unicode.
    """
    # the verb is invalid
    list_suggest = []
    # first strip harakat, shadda is not striped
    verb = araby.strip_harakat(verb)
    # second strip all inacceptable letters in an infinivive form
    verb = re.sub(u"[%s%s%s%s]"%( TEH_MARBUTA, DAMMATAN, KASRATAN, FATHATAN), \
     '', verb)
    # test the resulted verb if it's valid, if ok, 
    # add it to the suggestion list.
    if is_valid_infinitive_verb(verb):
        list_suggest.append(verb)
        return list_suggest
    # if the verb starts by ALEF_HAMZA_BELOW like إستعمل, 
    #replace if by an ALEF, because it's a common error.
    # if the result is valid add it to the suggestions list
    elif verb.startswith(ALEF_HAMZA_BELOW):
        verb = re.sub(ALEF_HAMZA_BELOW, ALEF, verb)
        if is_valid_infinitive_verb(verb):
            list_suggest.append(verb)
            return list_suggest
    # if the verb starts by ALEF like اضرب, 
    #replace if by an ALEF_HAMZA_ABOVE, because it's a common error.
    # if the result is valid add it to the suggestions list
    elif verb.startswith(ALEF):
        verb_one = re.sub(ALEF, ALEF_HAMZA_ABOVE+FATHA, verb, 1)
        if is_valid_infinitive_verb(verb_one):
            list_suggest.append(verb_one)
            return list_suggest
    # if the verb is 2 letters length, 
    # suggest to add the third letter as : 
    # Shadda, Alef, Alef Maksura, Yeh at the end
    # if the result is valid add it to the suggestions list
    elif len(verb) == 2:
        verb = re.sub(ALEF, ALEF_HAMZA_ABOVE, verb, 1)
        #suggest to add the third letter as : Shadda at the end
        verb_one = verb+SHADDA
        if is_valid_infinitive_verb(verb_one):
            list_suggest.append(verb_one)
        #suggest to add the third letter as : Alef Maksura
        verb_one = verb+ALEF_MAKSURA
        if is_valid_infinitive_verb(verb_one):
            list_suggest.append(verb_one)
        #suggest to add the third letter as :Alef at the end
        verb_one = verb+ALEF
        if is_valid_infinitive_verb(verb_one):
            list_suggest.append(verb_one)
        #suggest to add the third letter as :Alef in middle
        verb_one = verb[0]+ALEF+verb[1]
        if is_valid_infinitive_verb(verb_one):
            list_suggest.append(verb_one)
        return list_suggest
    elif len(verb) >= 6:
    # if the verb is more than 6 letters length, 
    #suggest to replace the over added letters by Alef
    # if the result is valid add it to the suggestions list
        for i in range(len(verb)-6):
            verb_one = ALEF+verb[i:i+5]
            if is_valid_infinitive_verb(verb_one):
                list_suggest.append(verb_one)
    elif len(verb) == 5:
    # if the verb is 5 letters length, suggest
    # if the result is valid add it to the suggestions list
        # ToDo: review this part
        for i in range(len(verb)-5):
            verb_one = ALEF+verb[i:i+4]
            if is_valid_infinitive_verb(verb_one):
                list_suggest.append(verb_one)
    elif len(verb) == 4:

    # if the verb is 5 letters length, 
    #suggest to replace the over added letters by Alef
    # if the result is valid add it to the suggestions list
    # فعال = > فاعل
    #فّعل = > فعّل
        if verb[2] == ALEF or verb[1] == SHADDA:
            verb_one = verb[0]+verb[2]+verb[1]+verb[3]
            if is_valid_infinitive_verb(verb_one):
                list_suggest.append(verb_one)
        if verb.endswith(SHADDA):
    # if the verb is 4 letters length, 
    #suggest to correct the alef and shadda position
    # if the result is valid add it to the suggestions list
    #فعلّ = > فعّل
            verb_one = verb[0]+verb[1]+verb[3]+verb[2]
            if is_valid_infinitive_verb(verb_one):
                list_suggest.append(verb_one)
        return list_suggest
    else:
    # else sugest to conjugate another verb
        list_suggest.append(u"كتب")
        return list_suggest
    return list_suggest

#####################################
#{verb pretreatment functions
#####################################
def  normalize_alef_madda(word):
    """
    Convert Alef madda into two letters.
    @param word: given word.
    @type word: unicode.
    @return: converted word.
    @rtype: unicode.
    """
    if word.startswith(ALEF_MADDA):
        word_nm = araby.strip_harakat(word)
        if len(word_nm) == 2:
            return word_nm.replace(ALEF_MADDA, HAMZA+ALEF)
        elif len(word_nm) == 3:
            if vconst.ALEF_MADDA_VERB_TABLE.has_key(word_nm):
                #return the first one only
                #mylist = ALEF_MADDA_VERB_TABLE[word_nm]
                return vconst.ALEF_MADDA_VERB_TABLE[word_nm][0]
            else:
                return  word_nm.replace(ALEF_MADDA, HAMZA+ALEF)
        else:
            return word_nm.replace(ALEF_MADDA, HAMZA+ALEF)
    else:
        return word_nm


