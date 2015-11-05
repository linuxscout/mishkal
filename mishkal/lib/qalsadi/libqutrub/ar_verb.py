#!/usr/bin/python
# -*- coding = utf-8 -*-
#************************************************************************
# $Id: ar_verb.py, v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
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
"""
Basic routines to treat verbs
ar_verb
"""
import re
import libqutrub.verb_const as vconst
# import ar_ctype 
import pyarabic.araby as araby
#~ from pyarabic.araby import *
from pyarabic.araby import FATHA, DAMMA, KASRA, SHADDA, SUKUN, HAMZA, ALEF, \
  WAW, ALEF_HAMZA_ABOVE, ALEF_MADDA, \
 YEH_HAMZA,   ALEF_MAKSURA, YEH, TEH,  \
LAM_ALEF, SIMPLE_LAM_ALEF, LAM_ALEF_HAMZA_ABOVE, \
SIMPLE_LAM_ALEF_HAMZA_ABOVE, LAM_ALEF_MADDA_ABOVE ,SIMPLE_LAM_ALEF_MADDA_ABOVE
#~ import libqutrub.verb_valid as verb_valid

def replace_pos (word, rep, pos):
    """
    Replace a letter in string in position
    @param word: given string
    @type word: unicode
    @param rep: replecment letter
    @type rep: unicode char
    @param pos: replemcment position
    @type pos: int
    @return: modified string
    @rtype: unicode string
    """
    return word[0:pos]+rep+word[pos+1:]
#####################################
#{ verb attributes conversion functions
#####################################

def get_bab_sarf_harakat(number):
    """
    Get the   the past and future marks by the bab sarf number
        - Bab: past  future
        - 1  : FATHA DAMMA
        - 2  : FATHA KASRA
        - 3  : FATHA FATHA
        - 4  : KASRA FATHA
        - 5  : DAMMA DAMMA
        - 6  : KASRA KASRA
    @param number: Bab sarf number (1-6).
    @type number: integer(1-6)
    @return:  a tuple of (past_mark, future_mark)
    @rtype: tuple
    """
    bab = None
    if number < 1 or number > 6:
        bab = None
    elif number == 1:
        bab = (FATHA, DAMMA)
    elif number == 2:
        bab = (FATHA, KASRA)
    elif number == 3:
        bab = (FATHA, FATHA)
    elif number == 4:
        bab = (KASRA, FATHA)
    elif number == 5:
        bab = (DAMMA, DAMMA)
    elif number == 6:
        bab = (KASRA, KASRA)
    return bab


def get_bab_sarf_number(past_haraka, future_haraka):
    """
    Get the bab sarf number by the past and future marks
        - Bab: past  future
        - 1  : FATHA DAMMA
        - 2  : FATHA KASRA
        - 3  : FATHA FATHA
        - 4  : KASRA FATHA
        - 5  : DAMMA DAMMA
        - 6  : KASRA KASRA
    @param past_haraka: past haraka of the verb.
    @type past_haraka: unicode
    @param future_haraka: future haraka of the verb.
    @type future_haraka: unicode
    @return: Bab sarf number (1-6)
    @rtype: integer
    """
    bab = 0
    if past_haraka == FATHA and future_haraka == DAMMA:
        bab = 1
    elif past_haraka == FATHA and future_haraka == KASRA:
        bab = 2
    elif past_haraka == FATHA and future_haraka == FATHA:
        bab = 3
    elif past_haraka == KASRA and future_haraka == FATHA:
        bab = 4
    elif past_haraka == DAMMA and future_haraka == DAMMA:
        bab = 5
    elif past_haraka == KASRA and future_haraka == KASRA:
        bab = 6
    return bab

def write_harakat_in_full(harakat):
    """
    Write the harakat name in full  in arabic
    @param harakat: list of harakat chars.
    @type  harakat: unicode  string
    @return: harakat in full
    @rtype: unicode
    """
    full = u""
    tab_harakat = {
    FATHA:u"فتحة", 
    DAMMA:u"ضمة", 
    KASRA:u"كسرة", 
    SUKUN:u"سكون", 
    vconst.ALEF_HARAKA:u"ألف", 
    vconst.WAW_HARAKA:u"واو", 
    vconst.YEH_HARAKA:u"ياء", 
    vconst.ALEF_YEH_HARAKA:u"ى", 
    vconst.ALEF_WAW_HARAKA:u"و", 
    vconst.ALEF_YEH_ALTERNATIVE:u"ئ", 
    }
    for hrk in harakat:
        if tab_harakat.has_key(hrk):
            full += u'-'+tab_harakat[hrk]
        else:
            full += u"*"
    return full


def get_past_harakat_by_babsarf(vtype):
    """
    Get the past harakat for the trileteral verb by bab sarf
        - Bab: past  future
        - 1  : FATHA DAMMA
        - 2  : FATHA KASRA
        - 3  : FATHA FATHA
        - 4  : KASRA FATHA
        - 5  : DAMMA DAMMA
        - 6  : KASRA KASRA
    @param vtype: the bab sarf codification.
    @type vtype: unicode a string of number
    @return: harakat
    @rtype: unicode
    """
    marks = KASRA*3 # make three kasraat by default
    if vtype in ('1', '2', '3'):
        marks = FATHA*3
    elif vtype in ('4', '6'):
        marks = u"".join([FATHA, KASRA, FATHA])
    elif vtype == '5':
        marks = u"".join([FATHA, DAMMA, FATHA])
    return marks

def get_future_harakat_by_babsarf(vtype):
    """
    Get the future harakat for the trileteral verb by bab sarf
        - Bab: past  future
        - 1  : FATHA DAMMA
        - 2  : FATHA KASRA
        - 3  : FATHA FATHA
        - 4  : KASRA FATHA
        - 5  : DAMMA DAMMA
        - 6  : KASRA KASRA
    @param vtype: the bab sarf codification.
    @type vtype: unicode a string of number
    @return: harakat
    @rtype: unicode
    """
    #ToDo Review
    marks = KASRA+KASRA+KASRA
    if vtype in ('1', '2', '3'):
        marks = FATHA+FATHA+FATHA
    elif vtype in ('4', '6'):
        marks = FATHA+KASRA+FATHA
    elif vtype == '5':
        marks = FATHA+DAMMA+FATHA
    return marks

def get_future_haraka_by_babsarf(vtype):
    """
    Get the future_type value from  different codifications. 
    used also in comand line
    in différent context the future_type is codified as:
    values
    or values used as Conjugation mode ( Bab Tasrif باب التصريف)
        - Bab: past  future
        - 1  : FATHA DAMMA
        - 2  : FATHA KASRA
        - 3  : FATHA FATHA
        - 4  : KASRA FATHA
        - 5  : DAMMA DAMMA
        - 6  : KASRA KASRA
    @param vtype: the bab sarf codification.
    @type vtype: unicode a string of number
    @return: haraka
    @rtype: unicode char
    """

    if vtype == '1':
        return DAMMA
    elif vtype in ('2', '6'):
        return KASRA
    elif vtype in ('3', '4'):
        return FATHA
    elif vtype in ('1', '5'):
        return DAMMA
    else:
        return ""


def get_haraka_by_name(haraka_name):
    """
    Convert an arabic named harakat to a real haraka
    values
        - Fahta:(فتحة)
        - DAMMA:(ضمة)
        - KASRA:(كسرة)
    @param haraka_name: the arabic name of haraka.
    @type haraka_name: unicode
    @return: the arabic name of haraka .
    @rtype: unicode char
    """
    if araby.is_shortharaka(haraka_name):
        return haraka_name
    if haraka_name == u"فتحة"  :
        return FATHA
    elif haraka_name == u"ضمة":
        return DAMMA
    elif haraka_name == u"كسرة":
        return KASRA
    elif haraka_name == u"سكون":
        return SUKUN
    else:
        return False


def get_future_type_by_name(haraka_name):
    """
    Get the future_type value by haraka arabic name.
    values
        - FATHA:(فتحة)
        - DAMMA:(ضمة)
        - KASRA:(كسرة)
    @param haraka_name: the arabic name of haraka.
    @type haraka_name: unicode
    @return: haraka
    @rtype: unicode char
    """
    haraka = get_haraka_by_name(haraka_name)
    if haraka:
        return haraka
    else:
        return FATHA


def get_future_type_entree(future_type):
    """
    Get the future_type value from  different codifications.
     used also in comand line
    in différent context the future_type is codified as:
    values
        - Fahta:(fatha, فتحة, ف, f)
        - DAMMA:(damma, ضمة, ض, d)
        - KASRA:(kasra, كسرة, ك, k)
    or values used as Conjugation mode ( Bab Tasrif باب التصريف)
        - Bab: past  future
        - 1  : FATHA DAMMA
        - 2  : FATHA KASRA
        - 3  : FATHA FATHA
        - 4  : KASRA FATHA
        - 5  : DAMMA DAMMA
        - 6  : KASRA KASRA
    @param future_type: the future_type codification.
    @type future_type: unicode
    @return: extract the future type mark
    @rtype: unicode char
    """
    future_type = u""+future_type.lower()
    if future_type in (u'fatha', u'فتحة', u'ف', u'f', u'3', u'4'):
        return FATHA
    if future_type in (u'damma', u'ضمة', u'ض', u'd', u'1', u'5'):
        return DAMMA
    if future_type in (u'kasra', u'كسرة', u'ك', u'k', u'2', u'6'):
        return KASRA
    else: return FATHA

def get_transitive_entree(transitive):
    """
    Get the transitive value from  different codifications.
    in différent context the transitivity is codified as:
        - "t", "transitive", 
        - u"متعدي", u"م", u"مشترك", u"ك"
        - True
    @param transitive: the transitive codification.
    @type transitive: unicode
    @return: True if is transitive
    @rtype: boolean
    """
    return transitive in (u"متعدي", u"م", u"مشترك",
      u"ك", "t", "transitive", True)

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


def normalize(word, wordtype = "affix"):
    """
    Normalize the word, by unifoming hamzat, Alef madda, shadda, and lamalefs.
    @param word: given word.
    @type word: unicode.
    @param type: if the word is an affix
    @type type: unicode.
    @return: converted word.
    @rtype: unicode.
    """
# تحويل الكلمة إلى شكلها النظري.
# الشكل اللإملائي للكلمة هو طريقة كتابتها حسب قواعد الإملاء
# الشكل النظري هو الشكل المتخيل للكلمة دون تطبيق قواعد اللغة
# ويخص عادة الأشكال المتعددة للهمزة، و التي تكتب همزة على السطر
# أمثلة
# إملائي        نظري
#إِمْلَائِي        ءِمْلَاءِي
#سَاَلَ        سَءَلَ
# الهدف : تحويل الكلمة إلى شكل نظري، 
#ومن ثم إمكانية تصريفها بعيدا عن قواعد الإملاء،
#وبعد التصريف يتم تطبيق قواعد الإملاء من جديد.
#الفرضية: الكلمات المدخلة مشكولة شكلا تاما.
#الطريقة:
# 1-تحويل جميع أنواع الهمزات إلى همزة على السطر
# 1-فك الإدغام
    i = 0
#   strip tatweel
# the tatweel is used to uniformate the affix 
# when the Haraka is used separetely
    if wordtype != "affix":
        word = araby.strip_tatweel(word)
## تستبدل الألف الممدودة في , ل الكلمة بهمزة قطع بعدها همزة أخرى
    if word.startswith(ALEF_MADDA):
        word = normalize_alef_madda(word)

    # ignore harakat at the begin of the word
    len_word = len(word)
    while i < len_word and araby.is_shortharaka(word[i]): # in HARAKAT:
        i += 1
    word = word[i:]
    # convert all Hamza from into one form
    word = araby.normalize_hamza(word)
    #Convert All LAM ALEF Ligature into separate letters
    word = word.replace(LAM_ALEF, SIMPLE_LAM_ALEF)
    word = word.replace(LAM_ALEF_HAMZA_ABOVE, SIMPLE_LAM_ALEF_HAMZA_ABOVE)
    word = word.replace(LAM_ALEF_MADDA_ABOVE, SIMPLE_LAM_ALEF_MADDA_ABOVE)
    return word


def uniformate_alef_origin(marks, word_nm, future_type = KASRA):
    """
    Convert toi its origin according to the future type haraka
    @param marks: given marks.
    @type marks: unicode.
    @param word_nm: given word unvocalized.
    @type word_nm: unicode.
    @param future_type: The future mark of the triletiral verb.
    @type future_type: unicode char, default KASRA.
    @return: converted marks.
    @rtype: unicode.
    """
    if len(marks) != 2:
        return marks
# الحرف ماقبل الأخير علة
    elif marks[len(marks)-2] == vconst.ALEF_HARAKA:
        if future_type == KASRA:
            marks = marks[:-2]+vconst.ALEF_YEH_HARAKA+marks[-1:]
        elif future_type == DAMMA:
            marks = marks[:-2]+vconst.ALEF_WAW_HARAKA+marks[-1:]
# الحرف الأخير علة
    if len(word_nm) == 3 and word_nm[-1:] == ALEF:
        word_nm = word_nm[:-1]+vconst.ALEF_MAMDUDA
    elif len(word_nm)>3 and word_nm[-1:] == ALEF:
        word_nm = word_nm[:-1]+YEH#ALEF_MAKSURA
    elif word_nm[-1:] == ALEF_MAKSURA:
        word_nm = word_nm[:-1]+ALEF_MAKSURA
    return marks

#--------------------------------------
# Predecated function
#--------------------------------------
def normalize_affix(word):
    """
    Replace shadda by SUKUN +SHADDA
    @param word: given word.
    @type word: unicode.
    @return: converted word.
    @rtype: unicode.
    """
    # convert SHadda to sukun shadda
    word = word.replace(SHADDA, SUKUN+SHADDA)

    return word


def uniformate_suffix(word):
    """ separate the harakat and the letters of the given word, 
    it return two strings ( the word without harakat and the harakat).
    If the weaked letters are reprsented as long harakat and striped 
    from the word.
    """
    ## type : affix : uniformate affixes
##    word = normalize_affix(word)
    word = word.replace(SHADDA, SUKUN+SHADDA)
    shakl = u""
    word_nm = u""
    i = 0
    len_word = len(word)
#    print "len word", len(word)
    while i < len_word:
        if not araby.is_shortharaka(word[i]):  # not in HARAKAT:
            word_nm += word[i]
            if i+1 < len(word) and araby.is_shortharaka(word[i+1]):
                if word[i+1] == FATHA :
                    if i+2 < len(word) and word[i+2] == ALEF and \
                                 i+3 < len(word):
                        shakl += vconst.ALEF_HARAKA
                        i += 3
                    else :
                        shakl += FATHA
                        i += 2
                elif word[i+1] == DAMMA and i+2 < len(word) and \
                       word[i+2] == WAW:
                    if i+3 >= len(word) or not araby.is_shortharaka(word[i+3]):
                        shakl += vconst.WAW_HARAKA
                        i += 3
                    else :
                        shakl += DAMMA
                        i += 2
                elif word[i+1] == KASRA and i+2 < len(word) and \
                 word[i+2] == YEH:
                    if i+3 >= len(word) or not araby.is_shortharaka(word[i+3]):
                        shakl += vconst.YEH_HARAKA
                        i += 3
                    else :
                        shakl += KASRA
                        i += 2
                else :
                    shakl += word[i+1]
                    i += 2

            elif  i+1 < len(word) and araby.is_haraka(word[i+1]):
                shakl += word[i+1]
            else:
                shakl += vconst.NOT_DEF_HARAKA
                i += 1
        else: i += 1
    if len(word_nm) == len(shakl):
        return (word_nm, shakl)
    else: return (u"", u"")


def uniformate_verb(word):
    """
    Separate the harakat and the letters of the given word, 
    it return two strings ( the word without harakat and the harakat).
    If the weaked letters are reprsented as long harakat 
    and striped from the word.
    @param word: given word.
    @type word: unicode.
    @return: (letters, harakat).
    @rtype: tuple of unicode.
    """
    if word == "":
        return ("", "")
    #normalize ALEF MADDA
    if word.startswith(ALEF_MADDA):
        word = word.replace(ALEF_MADDA, HAMZA+HAMZA)
    else:
        word = word.replace(ALEF_MADDA, HAMZA+ALEF)

    word_nm = araby.strip_harakat(word)
    length = len(word_nm)
    if len(word_nm) != 3:
        # تستعمل الهمزات لتخمين حركات الفعل الثلاثي
        # normalize hamza here, because we use it to 
        # detect harakat on the trilateral verb.
        word_nm = vconst.HAMZAT_PATTERN.sub(HAMZA, word_nm)
    # length of word after normalization

    # اهمزات تستعمل لكشف تشكيل الفعل، يتم توحيدها لاحقا
    if length == 3:
        if word_nm[1]in (ALEF, ALEF_HAMZA_ABOVE) or \
         word_nm[2] in (ALEF_MAKSURA, ALEF_HAMZA_ABOVE, ALEF):
            marks = FATHA+FATHA+FATHA
        elif word[1] == YEH_HAMZA or word[2] in (YEH, YEH_HAMZA):
            marks = FATHA+KASRA+FATHA
        else:
            # let the verb haraka
            i = 0
        ## ignore harakat at the began of the word
            while araby.is_shortharaka(word[i]):# in HARAKAT:
                i += 1
        # الحرف الأول
            if not araby.is_shortharaka(word[i]):#not in HARAKAT:
                i += 1
        # الحركة الأولى
            while araby.is_shortharaka(word[i]):#word[i] in HARAKAT:
                i += 1
        # الحرف الثاني
            if not araby.is_shortharaka(word[i]):#word[i] not in HARAKAT:
                i += 1
        #الحركة الثانية
            if not araby.is_shortharaka(word[i]):#word[i] not in HARAKAT:
            #وجدنا مشاكل في تصريف الفعل المضاعف في الماضي
            # نجعل الحركة الثانية فتحة مؤقتا
            #ToDo: review this case
                secondharaka = FATHA
            else:
                secondharaka = word[i]
            marks = u''.join([FATHA, secondharaka, FATHA])
        # تستعمل الهمزات لتخمين حركات الفعل الثلاثي
        # normalize hamza here, because we use it to 
        # detect harakat on the trilateral verb.
        word_nm = vconst.HAMZAT_PATTERN.sub(HAMZA, word_nm)

    elif length == 4:
        marks = vconst.UNIFORMATE_MARKS_4
    elif length == 5:
        if word_nm.startswith(TEH):
            marks = vconst.UNIFORMATE_MARKS_5TEH
        else :
            marks = vconst.UNIFORMATE_MARKS_5
    elif length == 6:
        marks = vconst.UNIFORMATE_MARKS_6
    else:
        marks = FATHA*len(word_nm)

    i = 1
# first added automaticlly
    new_word = word_nm[0]
    new_harakat = marks[0]
# between the first and the last
    while i < length-1:
        if word_nm[i] == ALEF:
            new_harakat = new_harakat[:-1]+vconst.ALEF_HARAKA
        else:
            new_harakat += marks[i]
            new_word += word_nm[i]
        i += 1
# the last letter
##  حالة الفعل عيا، أعيا، عيّا والتي يتحول إلى ياء بدلا عن واو
    if word_nm[i] == ALEF:
        if len(word_nm) == 3 and word_nm[1] != YEH:
            new_word += vconst.ALEF_MAMDUDA
        else:
            new_word += YEH
    else:
        new_word += word_nm[i]
    new_harakat += marks[i]
##    new_word += word_nm[i]
    return (new_word, new_harakat)


#####################################
#{verb conjugation output treatment functions
#####################################
def standard_harakat(word):
    """
    Treat Harakat on the word before output.
    معالجة الحركات قبل الإخراج،
    @param word: given vocalized word.
    @type word: unicode.
    @return: <vocalized word with ajusted harakat.
    @rtype: unicode.
    """
    k = 1
    new_word = word[0]
    len_word = len(word)
    while k < len_word:
# الحروف من دون العلة لا تؤخذ بيعين الاعتبار، كما لا تؤخذ إذا كانت في أول الكلمة
        if word[k] not in (ALEF, YEH, WAW, ALEF_MAKSURA):
            new_word += word[k]
        else:
    ##إذا كان الحرف علة ولم يكن في أول الكلمة
    ##إذا كان ما قبله ليس حركة، ومابعده ليس حركة، أو انتهت الكلمة
            if not araby.is_shortharaka(word[k-1]) and \
            (k+1 >= len_word or not araby.is_shortharaka(word[k+1])) :
                if word[k] == ALEF:
                    new_word += FATHA+ALEF
                elif word[k] == WAW :
                    new_word += DAMMA+WAW
                elif word[k] == YEH:
                    new_word += KASRA+YEH
                else:
                    new_word += word[k]
            else:
                new_word += word[k]
        k += 1
    return new_word


def geminating(word_nm, harakat):
    """ treat geminating cases
    المدخلات هي من كلمة غير مشكولة يقابلها حركاتها
    والحرف المضعف يمثل بشدة
    وإذا كانت الحالة تستوجب الفك، استبدلت الشدة بالحرف المضعف،
    أمّا إذا كانت لا تستوجب الفك، 
فتُعدّل حركة الحرف المضعف الأول إلى حركة ملغاة، 
تحذف في دالة الرسم الإملائي فيما بعد
    @param word_nm: given unvocalized word.
    @type word_nm: unicode.
    @param harakat: given harakat.
    @type harakat: unicode.
    @return: (letters, harakat).
    @rtype: tuple of unicode.
    """
    new_word = u""
    new_harakat = u""
    i = 0
    length = len(word_nm)
    ##    has_shadda = False
    ##    has_shadda = False
    if word_nm.find(SHADDA) < 0:
        return (word_nm, harakat)
    ##has_shadda and
    while i < length:
    # نعالج الحالات التي فيها الحرف الحالي متبوع بحرف شدة،
    # ندرس الحالات التي يجب فيها فك الإدغام
        if (i > 0 and i+1 < length and word_nm[i+1] == SHADDA and \
        harakat[i] in (SUKUN, FATHA, KASRA, DAMMA)):
            # treat ungeminating case

#إذا كان الحرف المضعف الأول غير ساكن والحرف المضعّف الثاني (ممثلا بشدة)ساكنا،
# يفك الإدغام.أمّا إذا كانت لا تستوجب الفك، 

            if  harakat[i] != SUKUN and harakat[i+1] == SUKUN:
                #ungeminating
                new_word += word_nm[i]
                word_nm = replace_pos(word_nm, word_nm[i], i+1)
                new_harakat += harakat[i]
                i += 1

            elif  harakat[i] == SUKUN and harakat[i+1] == SUKUN:
                #no geminating
                new_word += word_nm[i]
                word_nm = replace_pos(word_nm, word_nm[i], i+1)
                new_harakat += FATHA
                i += 1
            else:

    # عندما يكون الحرف السابق ساكنا فإنه يستعيع
    #يض عن حركته بحركة الحرف الأول
                if i-1 >= 0 and new_harakat[i-1] == SUKUN:
                    new_word += word_nm[i]+SHADDA
                    if harakat[i] != SUKUN:
                        new_harakat = new_harakat[:-1]+harakat[i]+ \
                           vconst.NOT_DEF_HARAKA+harakat[i+1]
                    else:
                        new_harakat = new_harakat[:-1]+FATHA+ \
                        vconst.NOT_DEF_HARAKA+harakat[i+1]
    ## يتم الإدغام إذا كان الحرف السابق ذو حركة طويلة
                elif i-1 >= 0 and new_harakat[i-1] in \
                (vconst.ALEF_HARAKA, vconst.WAW_HARAKA, \
                vconst.YEH_HARAKA):
                    new_word += word_nm[i]+SHADDA
                    new_harakat += vconst.NOT_DEF_HARAKA+harakat[i+1]

                elif harakat[i] == SUKUN:
                    new_word += word_nm[i]+SHADDA
                    new_harakat += vconst.NOT_DEF_HARAKA+harakat[i+1]
                else:
    ## مؤقت حتى يتم حل المشكلة
                    new_word += word_nm[i]+SHADDA
                    new_harakat += vconst.NOT_DEF_HARAKA+harakat[i+1]
    ##TODO
    ## منع الإدغام في بعض الحالات التي لا يمكن فيها الإدغام
    ##مثل حالة سكتتا ، أي الحرفات متحركان وما قبلهاما متحرك
    ## تم حل هذه المشكلة من خلال خوارزمية التجانس بين التصريفات
                i += 2
        elif i > 0 and i+1 < length and word_nm[i+1] == word_nm[i] and \
        harakat[i]  == SUKUN and harakat[i+1] in (FATHA, DAMMA, KASRA):
            # treat geminating case
            new_word += word_nm[i]+SHADDA
            new_harakat += vconst.NOT_DEF_HARAKA+harakat[i+1]
            i += 2
        else :
            new_word += word_nm[i]
            new_harakat += harakat[i]
            i += 1
    return (new_word, new_harakat)


def standard2(word_nm, harakat):
    """ join the harakat and the letters to the give word
     in the standard script, 
    it return one strings ( the word with harakat and the harakat).

    @param word_nm: given unvocalized word.
    @type word_nm: unicode.
    @param harakat: given harakat.
    @type harakat: unicode.
    @return: vocalized word.
    @rtype: unicode.
    """
    if len(word_nm) != len(harakat):
        return u""
    else:
        word = u""
        i = 0
        word_nm, harakat = geminating(word_nm, harakat)
        if len(word_nm) != len(harakat):
            return u""
    ## حالة عدم الابتداء بسكون
    ##إذا كان الحرف الثاني مضموما  تكون الحركة الأولى مضمومة، وإلا تكون مكسورة
        if len(harakat) != 0 and harakat.startswith(SUKUN):
            word_nm = ALEF+word_nm
            if len(harakat) >= 2 and harakat[1] in \
                    (DAMMA, vconst.WAW_HARAKA):
                harakat = DAMMA+harakat
            else:
                harakat = KASRA+harakat

    ##        word_nm = tahmeez2(word_nm, harakat)
        if len(word_nm) != len(harakat):
            return u""
        word_before = word_nm
        harakat_before = harakat
        word_nm, harakat = homogenize(word_nm, harakat)
        if len(word_nm) != len(harakat):
            print "len word: ", len(word_nm), word_nm.encode('utf8') 
            print "len harakat: ", len(harakat), repr(harakat)
            print repr(harakat_before), word_before.encode('utf8')
            return u""
        word_nm = tahmeez2(word_nm, harakat)

        len_word_nm = len(word_nm)
        while i < len_word_nm:
            # للعمل :
    # هذه حالة الألف التي أصلها ياء
    # وقد استغنينا عنها بأن جعلنا الحرف الناقص من الفعل الناقص حرفا تاما
            if vconst.WRITTEN_HARAKA.has_key(harakat[i]):
                word += word_nm[i]+vconst.WRITTEN_HARAKA[harakat[i]]
            else:
                word += word_nm[i]+harakat[i]
            i += 1

    #-تحويل همزة القطع على الألف بعدها فتحة 
#وهمزة القطع على الألف بعدها سكون إلى ألف ممدودة
    for (pat, rep) in vconst.STANDARD_REPLACEMENT:
        word = word.replace( pat, rep)


    return word


def tahmeez2(word_nm, harakat):
    """ Transform hamza on the standard script. 
    in entry the word without harakat and the harakat seperately
    return the word with non uniform hamza.
    إعلال و إبدال الهمزة.
    @param word_nm: given unvocalized word.
    @type word_nm: unicode.
    @param harakat: given harakat.
    @type harakat: unicode.
    @return: (letters, harakat) after treatment.
    @rtype: tuple of unicode.
    """
    # the harakat length  != letters length
    if len(word_nm) != len(harakat):
        return u""
    # if no hamza, no tahmeez
    elif  HAMZA not in word_nm:
        return word_nm
    else:
        ha2 = u""
        #eliminate some altenative of HARAKAT to standard.
        for hrk in harakat:
            if hrk == vconst.ALEF_YEH_HARAKA or \
              hrk == vconst.ALEF_WAW_HARAKA:
                hrk = vconst.ALEF_HARAKA
            ha2 += hrk
        harakat = ha2
        word = u""
        for i in range(len(word_nm)):
            if word_nm[i] != HAMZA and word_nm[i] != ALEF_HAMZA_ABOVE:
                word += word_nm[i]
            else:
                if i == 0:
                    actual = harakat[i]
                    swap = vconst.INITIAL_TAHMEEZ_TABLE[actual]
                else:
                    before = harakat[i-1]
                    actual = harakat[i]

                    if i+1 < len(word_nm):
    # if the hamza have shadda, it will take the harakat of shadda.
                        if actual == vconst.NOT_DEF_HARAKA or \
                         actual == SUKUN:
                            if word_nm[i+1] == SHADDA and \
                            harakat[i+1] != SUKUN:
                                actual = harakat[i+1]
                        if before == vconst.NOT_DEF_HARAKA:
                            before = FATHA
                        if actual == vconst.NOT_DEF_HARAKA:
                            actual = FATHA

                        if  vconst.MIDDLE_TAHMEEZ_TABLE.has_key(before) and\
                       vconst.MIDDLE_TAHMEEZ_TABLE[before].has_key(actual):
                            swap = vconst.MIDDLE_TAHMEEZ_TABLE[before][actual]
                        else :
                            swap = word_nm[i]
                    else :
                        if before == vconst.NOT_DEF_HARAKA:
                            before = FATHA
                        if actual == vconst.NOT_DEF_HARAKA: 
                            actual = FATHA

                        if  vconst.FINAL_TAHMEEZ_TABLE.has_key(before) and \
                         vconst.FINAL_TAHMEEZ_TABLE[before].has_key(actual):
                            swap = vconst.FINAL_TAHMEEZ_TABLE[before][actual]
                        else :
                            swap = word_nm[i]
                word += swap
    return word

def treat_sukun2(word_nm, harakat):
    """ Treat the rencontre of sukun. 
    in entry the word without harakat and the harakat seperately,
     and the probably haraka
    return the new sequence of harakat

    @param word_nm: given unvocalized word.
    @type word_nm: unicode.
    @param harakat: given harakat.
    @type harakat: unicode.
    @return: (letters, harakat).
    @rtype: tuple of unicode.
    """
    # if no sukun, to treat
    if harakat.find(SUKUN) < 0:
        return harakat
    len_word = len(word_nm)
    len_harakat = len(harakat)

    if len_word != len_harakat:
        return harakat
    else:
        new_harakat = u""
        for i in range(len_word):
            if i+1 < len_harakat and harakat[i+1] == SUKUN:
                if harakat[i] == vconst.ALEF_HARAKA:
                    #  other conditions
                      # إذا كان حرف الألف ثانيا مثل خاف يقلب كسرة،
                    #أما إذا كان ثالثا أو رابعا فيصبح فتحة،
                    # مثل خاف لا تخف
                    # حالة الألف بعدها حرف مشدد
                    if i+2 < len_word and word_nm[i+2] == SHADDA:
                        new_harakat += vconst.ALEF_HARAKA
                    elif i == 0 :
                        new_harakat += KASRA
                    else:
                        new_harakat += FATHA
                # if the actual haraka is in table use table conversion
                elif vconst.CONVERSION_TABLE.has_key(harakat[i]):
                    new_harakat += vconst.CONVERSION_TABLE[harakat[i]]
                else :
                    new_harakat += harakat[i]
            else :
                new_harakat += harakat[i]
    return new_harakat



def homogenize(word_nm, harakat):
    """ لإreat the jonction of WAW, YEH.
    معالجة التحولات التي تطرا على الياء أو الوا في وسط الكلمة أو في اخرها
    @param word_nm: given unvocalized word.
    @type word_nm: unicode.
    @param harakat: given harakat.
    @type harakat: unicode.
    @return: (letters, harakat)after treatment.
    @rtype: tuple of unicode.
    """
    # inequal length between letters and harakat
    if len(word_nm) != len(harakat):
        print "Homogenize:inequal length", len(word_nm), len(harakat)
        return (word_nm, harakat)
    # word without weak letters doesn't need treatment
    elif not re.search(ur'[%s%s%s%s]'%(ALEF_MAKSURA, vconst.ALEF_MAMDUDA, \
     YEH, WAW), word_nm):
        return (word_nm, harakat)
    # treatment
    else:
        new_harakat = harakat[0]
        new_word = word_nm[0]
        # نبدأ من الحرف الثاني لأن الحرف الأول لا يعالج
        i = 1
        ## دراسة حالات الياء والواو قبل النهاية
        len_word_nm = len(word_nm)
        while i < len_word_nm-1:
            actual_letter = word_nm[i]            # Actual letter
            actual_haraka = harakat[i]            # Actual haraka
            if i-1 >= 0 :
                previous_letter = word_nm[i-1]    # previous letter
                previous_haraka = harakat[i-1]    # previous letter
            else:
                previous_letter = ''
                previous_haraka = ''
            if i+1 < len_word_nm:
                next_letter = word_nm[i+1]        # next letter
                next_haraka = harakat[i+1]        # next haraka
            else:
                next_letter = ''
                next_haraka = ''
            # إذا كان الحرف التالي مضعف
            if i+2 < len_word_nm and word_nm[i+2] == SHADDA:
                shadda_in_next = True
            else:
                shadda_in_next = False

            if  actual_letter == ALEF_MAKSURA or actual_letter == YEH:
 #إذا كانت الياء ساكنة أو مكسورة (كسرا قصيرا أو طويلا)،
# وكان ما قبلها مكسورا، يأخذ ماقبلها كسرة طويلة            #مثال :
            # بِ +يْ  = > بِي
            #بِ +يِ   = > بِي
            #بِ +يي  = > بِي

                if actual_letter == ALEF_MAKSURA and next_haraka == SUKUN:
                    new_harakat += ""
                elif  (actual_haraka in(SUKUN, KASRA, vconst.YEH_HARAKA)) and \
                 previous_haraka == KASRA and not shadda_in_next:
                    new_harakat = new_harakat[:-1]+vconst.YEH_HARAKA
                elif  (actual_haraka in(KASRA)) and previous_haraka == KASRA \
                  and shadda_in_next:
                    new_harakat += ''
                # حالة هو تيسّر في المضارع المبني للمجهول
                elif  actual_letter == YEH and previous_haraka == DAMMA and \
                actual_haraka  == DAMMA  and  shadda_in_next:
                    #pass
                    new_harakat += DAMMA
                    new_word += YEH
                # # مثل تؤدّينّ
                # elif  previous_haraka in (KASRA, FATHA) and
                # actual_haraka  == DAMMA  and  shadda_in_next:
                    # new_harakat += FATHA
                    # new_word += YEH
                # ToDO review
                #سقّى، يُسقُّون
                elif  actual_haraka  == DAMMA  and  shadda_in_next:
                    new_harakat = new_harakat[:-1]+DAMMA
                #تحويل الياء إلى واو ساكنة
                #2 - إذا كانت الياء مضمومة (ضما قصيرا أو طويلا)،
# وكان ما قبلها مفتوحا، تتحول الياء إلى واو ساكنة.                #مثال :
                # بَ +يُ  = > بَِوْ
                #بَ +يو   = > بَوْ

                elif (actual_haraka in (DAMMA, vconst.WAW_HARAKA))and\
                  previous_haraka == FATHA and not shadda_in_next:
                    new_harakat += SUKUN
                    new_word += WAW
                elif (actual_haraka in (DAMMA, vconst.WAW_HARAKA))and \
                 previous_haraka == FATHA and shadda_in_next:
                    new_harakat += actual_haraka
                    new_word += WAW
                #إذا كانت ساكنة، وماقبلها مضموما،
# ولم يكن ما بعدها ياء، أخذ ما قبلها ضمة طويلة.
                #مثال :
                # بُ +يُت  = >بُوت


                elif  (actual_haraka  == SUKUN) and previous_haraka == DAMMA \
                 and next_letter != YEH and not shadda_in_next:
                    new_harakat = new_harakat[:-1]+vconst.WAW_HARAKA

                elif (actual_haraka  == vconst.YEH_HARAKA)and \
                previous_haraka == FATHA:
                    new_harakat += SUKUN
                    new_word += YEH
                elif  (actual_haraka  == vconst.WAW_HARAKA) and \
                 previous_haraka == KASRA :
                    new_harakat = new_harakat[:-1]+vconst.WAW_HARAKA

                else :
                    new_harakat += actual_haraka
                    new_word += YEH

            elif   actual_letter == vconst.ALEF_MAMDUDA or \
             actual_letter == WAW:
                if actual_letter == vconst.ALEF_MAMDUDA and \
                next_haraka == SUKUN:
                    new_harakat += ""
                elif actual_letter == vconst.ALEF_MAMDUDA and \
                (actual_haraka in(SUKUN, DAMMA, vconst.WAW_HARAKA))and\
                 (previous_haraka == DAMMA) and not shadda_in_next:
                    new_harakat = new_harakat[:-1]+vconst.WAW_HARAKA
                elif actual_letter == WAW and (actual_haraka in(SUKUN, DAMMA))\
                 and (previous_haraka == DAMMA) and not shadda_in_next:
                    new_harakat = new_harakat[:-1]+vconst.WAW_HARAKA
                #تحويل الواو المضمومة  أو الطويلة إلى واو ساكنة
                elif  (actual_haraka in (DAMMA, vconst.WAW_HARAKA)) \
                and previous_haraka == FATHA :
                    new_harakat += SUKUN
                    new_word += WAW
                # حالة وجع ايجع
                elif (actual_haraka  == (SUKUN))and \
                (previous_haraka == KASRA)and not shadda_in_next:
                    new_harakat = new_harakat[:-1]+vconst.YEH_HARAKA
                elif  (actual_haraka == KASRA)and shadda_in_next:
                    new_harakat = new_harakat[:-1]+KASRA
                elif  actual_letter == vconst.ALEF_MAMDUDA and \
                (actual_haraka == DAMMA)and shadda_in_next:
                    new_harakat = new_harakat[:-1]+DAMMA
                elif  actual_letter == vconst.ALEF_MAMDUDA and \
                (actual_haraka == vconst.YEH_HARAKA) and \
                 not shadda_in_next:
                    new_harakat = new_harakat[:-1]+vconst.YEH_HARAKA
                elif  actual_letter == WAW and (actual_haraka == DAMMA) and\
                 shadda_in_next:
                    new_harakat += DAMMA
                    new_word += WAW
                else :
                    new_harakat += actual_haraka
                    new_word += WAW
            else:
                new_harakat += actual_haraka
                new_word += actual_letter
            i += 1
    # end of while
    # we have to treat the last letter
    ## دراسة حالة الحرف الأخير
        # Actual letter
        last_letter = word_nm[i]
        # Actual haraka
        last_haraka = harakat[i]
        if i-1 >= 0 :
            # previous letter
            previous_letter = word_nm[i-1]
            # previous haraka
            previous_haraka = harakat[i-1]
        else:
            previous_letter = ''
            previous_haraka = ''
        if  last_letter == ALEF_MAKSURA or last_letter == YEH :
            if  (last_haraka in(KASRA, DAMMA))  and previous_haraka == KASRA:
                new_harakat = new_harakat[:-1]+vconst.YEH_HARAKA
            elif  (last_haraka in(vconst.YEH_HARAKA)) and\
             previous_haraka == KASRA :
                new_harakat = new_harakat[:-1]+vconst.YEH_HARAKA
            #حذف حركة الحرف الأخير إذا كان ساكنا
            elif (last_haraka == SUKUN):
            ## pass
                new_harakat += ''
                new_word += ''
            elif  previous_letter == YEH and \
            (last_haraka in(KASRA, DAMMA, FATHA)) and previous_haraka == FATHA:
                new_harakat += vconst.NOT_DEF_HARAKA
                new_word += ALEF
            elif  previous_letter != YEH and \
            (last_haraka in(KASRA, DAMMA, FATHA)) and previous_haraka == FATHA:
                new_harakat += vconst.NOT_DEF_HARAKA
                new_word += ALEF_MAKSURA
            elif  (last_haraka in(vconst.WAW_HARAKA)) and \
            previous_haraka == KASRA:
                new_harakat = new_harakat[:-1]+vconst.WAW_HARAKA
            #حالة تصريف الفعل الناقص في المضارع المجزوم مع أنت للمؤنث
            elif  (last_haraka == vconst.YEH_HARAKA) and  \
            previous_haraka == FATHA:
                new_harakat += SUKUN
                new_word += YEH
            else :
                new_harakat += last_haraka
                new_word += YEH

        elif last_letter == vconst.ALEF_MAMDUDA :
            if (last_haraka in(DAMMA, KASRA, vconst.WAW_HARAKA)) and \
            previous_haraka == DAMMA :
                new_harakat = new_harakat[:-1]+vconst.WAW_HARAKA
            elif (last_haraka in(vconst.ALEF_HARAKA)) and \
             previous_haraka == DAMMA:
            ##                pass
                new_harakat = new_harakat[:-1]+vconst.YEH_HARAKA
            elif  (last_haraka == vconst.YEH_HARAKA):
                new_harakat = new_harakat[:-1]+vconst.YEH_HARAKA
                new_word += ''
            elif (last_haraka == SUKUN) and previous_haraka == KASRA :
                pass

            elif (last_haraka == SUKUN):
                new_harakat += ''
                new_word += ''
            elif (last_haraka == FATHA)and previous_haraka == FATHA:
                new_harakat += vconst.NOT_DEF_HARAKA
                new_word += vconst.ALEF_MAMDUDA
            else :
                new_harakat += last_haraka
                new_word += WAW
                #new_word += vconst.ALEF_MAMDUDA
        else:
            new_harakat += harakat[i]
            new_word += word_nm[i]
        return (new_word, new_harakat)


def is_triliteral_verb(verb):
    """ Test if the verb is  triliteral, 
    used in selectionof verbs from the triliteral verb dictionnary
    @param verb: given verb.
    @type verb: unicode.
    @return: True if the verb is triliteral.
    @rtype: Boolean.
    """
    verb_nm = araby.strip_harakat(verb)
    verb_nm = verb_nm.replace(ALEF_MADDA, HAMZA+ALEF)
    if len(verb_nm) == 3:
        return True
    else : return False





