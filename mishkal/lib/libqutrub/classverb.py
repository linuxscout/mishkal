#!/usr/bin/python
# -*- coding=utf-8 -*-

#************************************************************************
# $Id: classverb.py, v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2009, Arabtechies, Arabeyes Taha Zerrouki
#
#  The Main class to do the conjugation
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
Verb Class for conjugation
@author: Taha Zerrouki
@contact: taha dot zerrouki at gmail dot com
@copyright: Arabtechies, Arabeyes, Taha Zerrouki
@license: GPL
@date:2009/06/02
@version: 0.9
"""
import copy
# from ar_ctype import *
#~ import sys
#~ import re
import pyarabic.araby as araby
from pyarabic.araby import FATHA, DAMMA, KASRA, SHADDA, SUKUN, HAMZA, ALEF, \
 NOON,  YEH_HAMZA, WAW, TATWEEL, MEEM, MEEM, YEH, TEH, ALEF_MAKSURA
#~ from libqutrub.ar_verb import *
import libqutrub.ar_verb as ar_verb 
#~ from libqutrub.verb_const import *
import  libqutrub.verb_const as vconst
import libqutrub.conjugatedisplay as conjugatedisplay


class ConjugStem:
    """
    A Class to represent a conjugated stem
    """
    # بنية جذع تصريف الجذع
    #تتكون من الزمن، الحروف والحركات
    # تستعمل لتخزين جذوع التصريف
    tense = u""
    #~ """ the actual tense"""
    letters = u""
    #~ """ letters of the conjugated stem"""
    marks = u""
    #~ """ marks of the conjugated stem"""    
    def __init__(self, tense, letters, marks):
        """ 
        init method
        @param tense: the given tense
        @type tense: unicode.
        @param letters: the word letters
        @type letters: unicode.        
        @param marks: the word marks; 
        @type marks: unicode.        
        """
        self.tense = tense
        self.letters = letters
        self.marks = marks
# a global cache for verbs conjigation
cache_standard = {'standard':{}, 
                    'sukun':{}, 
                    'suffix':{}}
class VerbClass:
    """
    Verb Class: represent a verb, prepare it to be conjugated and store the conjugation result
    """
    #~ verb = u""
    #~ #" internl verb : is the normalized form of the verb"
    #~ internal_verb = u""
    #~ word_letters = u""
    #~ word_marks = u""
    #~ unvocalized = u""
    #~ vlength = 0
    #~ vtype = u""
    #~ future_type = u''
    #~ transitive = u""
    #~ hamza_zaida = False
    #~ #deprecated
    #~ # teh_zaida=False
    #~ future_form = u""
    #~ conj_display = None
    #~ tab_conjug_stem = None
    def __init__(self, verb, transitive, future_type=FATHA):
        """ 
        init method
        @param verb: the given verb
        @type verb: unicode.
        @param transitive: the verb is transitive or not
        @type transitive: Boolean.        
        @param future_type: The mark of the third radical letter in the verb, 
        used for triletiral verb only. Default value is Fatha; 
        @type future_type: unicode; one arabic letter (Fatha, Damma, Kasra).        
        """    
        self.verb = verb
        # this cache is used to avoid duplicated operatioon in standardisation,
        # treat_sukun, and uniformate suffix
        self.cache_standard = cache_standard
        self.internal_verb = ar_verb.normalize(verb)
        self.future_type = ar_verb.get_future_type_by_name(future_type)
        (self.word_letters, self.word_marks) = ar_verb.uniformate_verb(verb)
        #Before last haraka in the past
        self.past_haraka = araby.secondlast_char(self.word_marks)
        self.word_marks = ar_verb.uniformate_alef_origin(self.word_marks, 
        self.internal_verb, self.future_type)

        self.transitive = transitive
        self.hamza_zaida = False
        self.tab_conjug_stem = {}
        verb = self.verb
        tab_type = [u"", u"", u"", u"فعل ثلاثي", u"فعل رباعي", u"فعل خماسي", 
        u"فعل سداسي", u"فعل سباعي", u"فعل ثماني", u"فعل تساعي"]
        verb = ar_verb.normalize(verb)

        self.unvocalized = araby.strip_harakat(verb)
        verb_nm = self.unvocalized
        self.vlength = len(verb_nm)
        self.vtype = tab_type[self.vlength]

        # الهمزة زائدة
        self.hamza_zaida = self._is_hamza_zaida(verb_nm)

        # التاء الزائدة
        #deprecated
        #self.teh_zaida=self.is_teh_zaida(verb_nm)

        # معالجة حالة الأفعال الشاذة
        # إذا كان الفعل من الشواذ، استخرجنا جذوع التصريف من جدوله
        #وإلا ولّدنا جذوع تصريفه
        # في المضارع والأمر فقط
        # أما الماضي فليس فيه شذوذ
        self.past_stem = ""
        self._prepare_past_stem()
        self._prepare_passive_past_stem()
        if self._is_irregular_verb():
            self._prepare_irregular_future_imperative_stem()

        else:
            self._prepare_future_imperative_stem()


        # display object
        self.conj_display = conjugatedisplay.ConjugateDisplay(self.verb)
        if self.transitive  :
            self.conj_display.add_attribut(u"اللزوم/التعدي", u"متعدي")
        else :
            self.conj_display.add_attribut(u"اللزوم/التعدي", u"لازم")
        self.conj_display.add_attribut(u"الفعل", self.verb)
        self.conj_display.add_attribut(u"نوع الفعل", self.vtype)
        self.future_form = self.conjugate_tense_pronoun(vconst.TenseFuture, 
        vconst.PronounHuwa)
        self.conj_display.set_future_form(self.future_form)
        if self.transitive :
            self.conj_display.settransitive()
        self.conj_display.setbab(self.future_type)


    def __del__(self):
        """
        Delete instance 
        
        """
        self.conj_display = None
        self.tab_conjug_stem = None


#####################################
#{ Attributes functions
#####################################
    def set_display(self, mode = 'Text'):
        """ 
        Set the display mode as:
            - 'Text':
            - 'HTML':
            - 'HTMLColoredDiacritics':
            - 'DICT':
            - 'CSV':
            - 'GUI':
            - 'TABLE':
            - 'XML':
            - 'TeX':
            - 'ROWS':
        @param mode: the given mode to display result
        """        
        self.conj_display.setmode(mode)



    def get_conj_display(self):
        """
        Get The conjugation display class with result.
        @return: an object with result.
        @rtype: conjugatedisplay class
        """
        return copy.copy(self.conj_display)
#####################################
#{ Extract information from verb functions
#####################################
    def _is_hamza_zaida(self, verb_normalized_unvocalized):
        """
        Function to determine if the first HAMZA in the verb is not original
            ترجع إذا كانت الهمزة الأولى في الفعل غير أصلية
        Determine if the verb starts with Hamza and the Teh is not
        @param verb_normalized_unvocalized: the unvovalized form f the verb.
        @type verb_normalized_unvocalized: unicde
        @return: return True if the start Teh is not original
        @rtype: boolean; 
        """
    # if the lenght of verb is exactely 4 letters and starts by hamza
    # and it is in the AF3Al wazn and not FA33al or FAA3la
    # ألوزن المعني هو أفعل
    # الأوزان غير المعنية هي فاعل وفعّل
    # الأوزان المشتقة هي أفعّ من أفعل
    # الخلاصة أن يكون الفعل رباعيا، حرفه الأول همزة
    # ولا يكون حرفه الثاني ألف، لمنع الوزن فاعل
    # ولا يكون حرفه الثالث شدة، لمنع الوزن فعّل
        verb = verb_normalized_unvocalized
        if len(verb) != 4 or  not verb.startswith(HAMZA):
            return False
        elif len(verb) == 4 and verb.startswith(HAMZA) and \
        verb[1]!=ALEF and verb[2]!=SHADDA:
            return True
        else :
            return False

    def _homogenize_harakat(self, original_harakat, applied_harakat):
        """ 
        Treat Harakat to be homogenized with letters in conjugation.
        إذا كان طول الحركات ألأصلية للفعل أقل من طول حركات الماضي المبني للمجهول
        هذا يعني وجود حركة طويلة
        نقوم بتحويل الحركة الطويلة إلى ما يوافقها

        @param original_harakat: given original harakatof the verb.
        @type original_harakat: unicode.
        @param applied_harakat: given harakat to be applied to  verb.
        @type applied_harakat: unicode.    
        @return: nesw harakat to be applied to the verb.
        @rtype: unicode.
        """    
        marks = original_harakat
        new_marks = applied_harakat
#  إذا كان طول الحركات ألأصلية للفعل أقل من طول حركات الماضي المبني للمجهول
# هذا يعني وجود حركة طويلة
# نقوم بتحويل الحركة الطويلة إلى ما يوافقها
        if len(marks) < len(new_marks):
            alef_haraka_pos = marks.find(vconst.ALEF_HARAKA)
            if alef_haraka_pos < 0:
                alef_haraka_pos = marks.find(vconst.ALEF_WAW_HARAKA)
            if alef_haraka_pos < 0:
                alef_haraka_pos = marks.find(vconst.ALEF_YEH_HARAKA)
            if alef_haraka_pos >= 0 and alef_haraka_pos + 1 < len(new_marks):
                first = new_marks[alef_haraka_pos]
                second = new_marks[alef_haraka_pos + 1]
                changed_haraka = \
                  vconst.HOMOGENIZE_ALEF_HARAKA_TABLE[first][second]
                new_marks = new_marks[:alef_haraka_pos] + changed_haraka \
                + new_marks[alef_haraka_pos+2:]
        return new_marks      
#####################################
#{ Preparing  conjugation stems for every tense functions
#####################################
    def _prepare_future_imperative_stem(self):
        """
        Prepare the conjugation stems for future tenses 
        (future, jussive, subjective) and imperative tense.
         Those stems will be concatenated with conjugation affixes.
          This function store results in self.tab_conjug_stem. 
          This function prepare conjugation stems for the following tenses:
            - vconst.TenseFuture :  تصريف الفعل المضارع 
            - vconst.TenseJussiveFuture : تصريف الفعل المضارع المجزوم 
            - vconst.TenseSubjunctiveFuture : تصريف الفعل المضارع المنصوب 
            - vconst.TenseConfirmedFuture: المضارع المؤكد الثقيل
            - vconst.TensePassiveFuture :تصريف الفعل المضارع المبني للمجهول
            - vconst.TensePassiveJussiveFuture: تصريف الفعل المضارع المجزوم المني للمجهول
            - vconst.TensePassiveSubjunctiveFuture:تصريف الفعل المضارع المنصوب 
            - vconst.TensePassiveConfirmedFuture:المضارع المؤكد الثقيل المنبي للمجهول
            - vconst.TenseImperative:الفعل الامر
            - vconst.TenseConfirmedImperative: الفعل الامر المؤكد.
        """
        letters = self.word_letters
        marks = self.word_marks
        future_letters = letters
        # حالة الفعل الثلاثي
        if self.vlength == 3:
            first_future_mark = FATHA
            first_passive_future_mark = DAMMA
            future_marks = SUKUN + self.future_type + FATHA
            passive_future_marks = SUKUN + FATHA + FATHA
        # معالجة الفعل المثال الواوي
        #ToDO

        # الفعل الرباعي
        elif self.vlength == 4:
            first_future_mark = DAMMA
            first_passive_future_mark = DAMMA
            future_marks = FATHA + SUKUN + KASRA + DAMMA
            passive_future_marks = FATHA + SUKUN + FATHA + DAMMA
        # الفعل الخماسي
        elif self.vlength == 5:
            first_future_mark = FATHA
            first_passive_future_mark = DAMMA
            if letters.startswith(TEH):
                future_marks = FATHA + FATHA + SUKUN + FATHA + DAMMA
                passive_future_marks = FATHA + FATHA + SUKUN + FATHA + DAMMA
            else :
                future_marks = FATHA + SUKUN + FATHA + KASRA + DAMMA
                passive_future_marks = FATHA + SUKUN + FATHA + FATHA + DAMMA
        #الفعل السداسي
        elif self.vlength == 6:
            first_future_mark = FATHA
            first_passive_future_mark = DAMMA
            future_marks = FATHA + SUKUN + FATHA + SUKUN + KASRA + DAMMA
            passive_future_marks = FATHA + SUKUN + FATHA + SUKUN + FATHA + DAMMA
        # معالجة الألفات في الفعل والحركات الطويلة
        #  إذا كان طول الحركات ألأصلية للفعل 
        # أقل من طول حركات الماضي المبني للمجهول
        # هذا يعني وجود حركة طويلة
        # نقوم بتحويل الحركة الطويلة إلى ما يوافقها
        if len(marks) < len(future_marks):
            future_marks = self._homogenize_harakat(marks, future_marks)
            passive_future_marks = self._homogenize_harakat(marks, 
                     passive_future_marks)
        imp_marks = future_marks
        imp_letters = future_letters
        # حالة الأفعال التي تبدأ بألف وصل
        if letters.startswith(ALEF) or self.hamza_zaida:
            future_letters = letters[1:]
            future_marks = future_marks[1:]
            passive_future_marks = passive_future_marks[1:]
            passive_letters = letters[1:]
        # حالة الفعل المثال
        elif self.vlength == 3 and self.word_letters.startswith(WAW) and \
        (self.future_type == KASRA or  (self.future_type==FATHA and \
        self.word_marks==FATHA+FATHA+FATHA and \
        not self.word_letters.endswith(SHADDA))):
            future_letters = letters[1:]
            future_marks = future_marks[1:]
##            passive_future_marks=passive_future_marks[1:]
            passive_letters = letters
        else:
            future_letters = letters
            passive_letters = letters
        new_marks = first_future_mark + future_marks
        passive_marks = first_passive_future_mark + passive_future_marks

        # حالة الأفعال التي تبدأ بألف وصل
        if imp_letters.startswith(ALEF):
            imp_letters = letters[1:]
            imp_marks = imp_marks[1:]
        elif self.vlength == 3 and self.word_letters.startswith(WAW) and \
        (self.future_type == KASRA or (self.future_type==FATHA and \
        self.word_marks==FATHA+FATHA+FATHA)):
            imp_letters = letters[1:]
            imp_marks = imp_marks[1:]
        else:
            imp_letters = letters

        # معالجة الفعل الناقص عند تصريفه في المجهول
        # تستبدل واو التاقص الذي حركة عين ماضيه فتحة بياء
##        passive_letters=future_letters
        if self.vlength == 3 and passive_letters.endswith(vconst.ALEF_MAMDUDA):
            passive_letters = passive_letters[:-1]+ALEF_MAKSURA
        #  القعل الأمر يأخذ نفس حركات الفعل المضارع دون حركة حرف المضارعة
##        imp_marks=future_marks
        ### معلجة إضافة حرف ألف الوصل في الأفعال المسبوقة بالسكون
##        new_marks=first_future_mark+future_marks
##        passive_marks=first_passive_future_mark+passive_future_marks
        self.tab_conjug_stem[vconst.TenseFuture] = ConjugStem(
        vconst.TenseFuture, future_letters, new_marks)
        # تصريف الفعل المضارع المنصوب والمجزوم
        self.tab_conjug_stem[vconst.TenseJussiveFuture] = ConjugStem(
        vconst.TenseJussiveFuture, future_letters, new_marks)
        self.tab_conjug_stem[vconst.TenseSubjunctiveFuture] = ConjugStem(
        vconst.TenseSubjunctiveFuture, future_letters, new_marks)
        # المضارع المؤكد الثقيل
        self.tab_conjug_stem[vconst.TenseConfirmedFuture] = ConjugStem(
        vconst.TenseConfirmedFuture, future_letters, new_marks)

        # المبني للمجهول
        self.tab_conjug_stem[vconst.TensePassiveFuture] = ConjugStem(
        vconst.TensePassiveFuture, passive_letters, passive_marks)
        # تصريف الفعل المضارع المنصوب والمجزوم المني للمجهول
        self.tab_conjug_stem[vconst.TensePassiveJussiveFuture] = ConjugStem(
        vconst.TensePassiveJussiveFuture, passive_letters, passive_marks)
        self.tab_conjug_stem[vconst.TensePassiveSubjunctiveFuture] = \
        ConjugStem(vconst.TensePassiveSubjunctiveFuture, passive_letters,
         passive_marks)
        # المضارع المؤكد الثقيل المنبي للمجهول
        self.tab_conjug_stem[vconst.TensePassiveConfirmedFuture] = ConjugStem(
        vconst.TensePassiveConfirmedFuture, passive_letters, passive_marks)

        # الفعل الامر
        self.tab_conjug_stem[vconst.TenseImperative] = ConjugStem(
        vconst.TenseImperative, imp_letters, imp_marks)
        # الفعل الامر المؤكد
        self.tab_conjug_stem[vconst.TenseConfirmedImperative] = ConjugStem(
        vconst.TenseConfirmedImperative, imp_letters, imp_marks)

    def _prepare_past_stem(self):
        """
        Prepare the conjugation stems for past tense.
        Those stems will be concatenated with conjugation affixes.
        This function store results in self.tab_conjug_stem. 
        This function prepare conjugation stems for the following tenses:
            - vconst.TensePast: الفعل الماضي.
        """    
        self.past_stem = self.internal_verb
        self.tab_conjug_stem[vconst.TensePast] = ConjugStem(
        vconst.TensePast, self.word_letters, self.word_marks)


    def _prepare_passive_past_stem(self):
        """
        Prepare the conjugation stems for past tense.
        Those stems will be concatenated with conjugation affixes.
        This function store results in self.tab_conjug_stem. 
        This function prepare conjugation stems for the following tenses:
            - vconst.TensePast: الفعل الماضي
        """        
        letters = self.word_letters
        marks = self.word_marks

        if len(letters) == 3 and letters.endswith(vconst.ALEF_MAMDUDA) \
        and marks[1] == FATHA:
            letters = letters[:-1] + ALEF_MAKSURA
        if self.vlength == 3:
            passive_marks = DAMMA + KASRA + FATHA
        elif self.vlength == 4:
            passive_marks = DAMMA + SUKUN + KASRA + FATHA
        elif self.vlength == 5:
            if letters.startswith(TEH):
                passive_marks = DAMMA + DAMMA + SUKUN + KASRA + FATHA
            else :
                passive_marks = DAMMA + SUKUN + DAMMA + KASRA + FATHA
        elif self.vlength == 6:
            passive_marks = DAMMA + SUKUN + DAMMA + SUKUN + KASRA + FATHA
#  إذا كان طول الحركات ألأصلية للفعل أقل من طول حركات الماضي المبني للمجهول
# هذا يعني وجود حركة طويلة
# نقوم بتحويل الحركة الطويلة إلى ما يوافقها
        if len(marks) < len(passive_marks):
            passive_marks = self._homogenize_harakat(marks, passive_marks)

# -    حالة الفعل الأجوف الذي حركة مضارعه فتحة أو كسرة،
#-    فيصبح في الماضي عند التقاء الساكنين كسرة،
 #لذا يجب تعديل ذلك في الماضي المجهول،
# بجعلها تتحول إلى ضمة عند التقاء الساكنين.
        if len(passive_marks) == 2 and passive_marks[0] == vconst.YEH_HARAKA \
        and  self.future_type in (FATHA, KASRA):
            passive_marks = vconst.ALTERNATIVE_YEH_HARAKA + FATHA
        self.tab_conjug_stem[vconst.TensePassivePast] = ConjugStem(\
        vconst.TensePassivePast, letters, passive_marks)

    def conjugate_tense_pronoun(self, tense, pronoun):
        """
        Conjugate a verb in a given tense with a pronoun.
        @param tense: given tense
        @type tense: unicode name of the tense
        @param pronoun: given pronoun
        @type pronoun: unicode name of the pronoun
        @return: conjugated verb
        @rtype: unicode;        
        """
        #prefix
        pre_val = vconst.TableTensePronoun[tense][pronoun][0] 
        #suffix
        suf_val = vconst.TableTensePronoun[tense][pronoun][1]
        stem_l = self.tab_conjug_stem[tense].letters
        stem_m = self.tab_conjug_stem[tense].marks
#deprecated
##        return self.join(stem_l, stem_m, prefix, suffix)
        # _m : marks
        #_l :letters
        if pre_val != u"":
            pre_val_l = pre_val
            pre_val_m = stem_m[0]
            stem_m = stem_m[1:]
        else:
            pre_val_l = u""
            pre_val_m = u""

        # the suffix already start by a HARAKA, 
        # we add Taweel to ensure valid word in the uniformate function
        suf_val = TATWEEL + suf_val
        #uniformate suffix
        # the case is used to avoid duplicated staddization
        if self.cache_standard['suffix'].has_key( suf_val): 
            (suf_val_l, suf_val_m) = self.cache_standard['suffix'][suf_val]
        else:
            (suf_val_l, suf_val_m) = ar_verb.uniformate_suffix(suf_val)
            self.cache_standard['suffix'][suf_val] = (suf_val_l, suf_val_m)
        # add affix to the stem
        conj_l = pre_val_l + stem_l + suf_val_l
        #The end of the stem marks takes the begining of the suffix marks
        conj_m = pre_val_m + stem_m[:-1] + suf_val_m
        # the begining of suffix letters is Tatweel, it will be striped
        conj_l = pre_val_l + stem_l + suf_val_l[1:]

        # Treat sukun
        # the case is used to avoid duplicated staddization
        key_cache = u'-'.join([conj_l, conj_m])
        if self.cache_standard['sukun'].has_key(key_cache):
            conj_m = self.cache_standard['sukun'][key_cache]
        else:
            #~ conj_m = ar_verb.treat_sukun2(conj_l, conj_m, self.future_type)
            conj_m = ar_verb.treat_sukun2(conj_l, conj_m)
            self.cache_standard['sukun'][key_cache] = conj_m
        # standard orthographic form
        # the case is used to avoid duplicated staddization
        key_cache = u'-'.join([conj_l, conj_m])
        if self.cache_standard['standard'].has_key(key_cache):
            conj = self.cache_standard['standard'][key_cache]
        else:    
            conj = ar_verb.standard2(conj_l, conj_m)
            self.cache_standard['standard'][key_cache] = conj
        return conj


#----------------------------------------------------------------
# التصريف في الأزمنة المختلفة،
# عند وضع قائمة خاصة بالأزمنة المختارة،
# تلقائيا كافة الأزمنة
#----------------------------------------------------------------
    def conjugate_all_tenses(self, listtense = None):
        """
        Conjugate a verb  with a list of tenses.
        @param listtense: given tense
        @type listtense: list of unicode
        @return: conjugated verb 
        @rtype: the type is given according to the display mode;        
        """
        if not listtense:
            listtense = vconst.TABLE_TENSE
        for tense in listtense:
            if tense == vconst.TensePast:
                conj_ana = self.conjugate_tense_pronoun(tense, 
                     vconst.PronounAna)
                self.conj_display.add(tense, vconst.PronounAna, conj_ana)
                conj_ana_without_last_mark = conj_ana[:-1]
                self.conj_display.add(tense, vconst.PronounAnta, 
                conj_ana_without_last_mark+FATHA)
                self.conj_display.add(tense, vconst.PronounAnti, 
                conj_ana_without_last_mark+KASRA)
                self.conj_display.add(tense, vconst.PronounAntuma, 
                conj_ana+MEEM+FATHA+ALEF)
                self.conj_display.add(tense, vconst.PronounAntuma_f, 
                conj_ana+MEEM+FATHA+ALEF)
                self.conj_display.add(tense, vconst.PronounAntum, 
                conj_ana+MEEM)
                self.conj_display.add(tense, vconst.PronounAntunna, 
                conj_ana+NOON+SHADDA+FATHA)
                self.conj_display.add(tense, vconst.PronounAna, conj_ana)

                conj_nahnu = self.conjugate_tense_pronoun(tense,
                   vconst.PronounNahnu)
                self.conj_display.add(tense, vconst.PronounNahnu, conj_nahnu)

                conj_hunna = self.conjugate_tense_pronoun(tense, 
                vconst.PronounHunna)
                self.conj_display.add(tense, vconst.PronounHunna, conj_hunna)

                conj_huma = self.conjugate_tense_pronoun(tense, 
                vconst.PronounHuma)
                self.conj_display.add(tense, vconst.PronounHuma, conj_huma)

                conj_hum = self.conjugate_tense_pronoun(tense, 
                vconst.PronounHum)
                self.conj_display.add(tense, vconst.PronounHum, conj_hum)

                conj_hunna = self.conjugate_tense_pronoun(tense, 
                vconst.PronounHunna)
                self.conj_display.add(tense, vconst.PronounHunna, conj_hunna)

                conj_huwa = self.conjugate_tense_pronoun(tense, 
                vconst.PronounHuwa)
                self.conj_display.add(tense, vconst.PronounHuwa, conj_huwa)
                conj_hya = self.conjugate_tense_pronoun(tense, 
                vconst.PronounHya)
                self.conj_display.add(tense, vconst.PronounHya, conj_hya)
                self.conj_display.add(tense, vconst.PronounHuma_f, 
                conj_hya[:-1]+FATHA+ALEF)
            elif tense == vconst.TensePassivePast:
                conj_ana = self.conjugate_tense_pronoun(tense, 
                vconst.PronounAna)
                self.conj_display.add(tense, vconst.PronounAna, conj_ana)
                conj_ana_without_last_mark = conj_ana[:-1]
                self.conj_display.add(tense, vconst.PronounAnta, 
                conj_ana_without_last_mark+FATHA)
                self.conj_display.add(tense, vconst.PronounAnti, 
                conj_ana_without_last_mark+KASRA)
                self.conj_display.add(tense, vconst.PronounAntuma, 
                conj_ana+MEEM+FATHA+ALEF)
                self.conj_display.add(tense, vconst.PronounAntuma_f, 
                conj_ana+MEEM+FATHA+ALEF)
                self.conj_display.add(tense, vconst.PronounAntum, 
                conj_ana+MEEM)
                self.conj_display.add(tense, vconst.PronounAntunna, 
                conj_ana+NOON+SHADDA+FATHA)
                self.conj_display.add(tense, vconst.PronounAna, conj_ana)

                conj_nahnu = self.conjugate_tense_pronoun(tense, 
                vconst.PronounNahnu)
                self.conj_display.add(tense, vconst.PronounNahnu, 
                conj_nahnu)

                conj_hunna = self.conjugate_tense_pronoun(tense, 
                vconst.PronounHunna)
                self.conj_display.add(tense, vconst.PronounHunna, 
                conj_hunna)

                conj_hunna = self.conjugate_tense_pronoun(tense, 
                vconst.PronounHunna)
                self.conj_display.add(tense, vconst.PronounHunna, 
                conj_hunna)

                conj_huwa = self.conjugate_tense_pronoun(tense, 
                vconst.PronounHuwa)
                self.conj_display.add(tense, vconst.PronounHuwa, conj_huwa)
# حالة الفعل مهموز الآخر
                if conj_huwa.endswith(YEH+HAMZA+FATHA) :
                    self.conj_display.add(tense, vconst.PronounHya, 
                    conj_huwa[:-2]+YEH_HAMZA+FATHA+TEH+SUKUN)
                    self.conj_display.add(tense, vconst.PronounHuma_f, 
                    conj_huwa[:-2]+YEH_HAMZA+FATHA+TEH+FATHA+ALEF)
##                       conj_huma=self.conjugate_tense_pronoun(tense, 
##                        vconst.PronounHuma)
                    self.conj_display.add(tense, vconst.PronounHuma, 
                    conj_huwa[:-2]+YEH_HAMZA+FATHA+ALEF)

##                       conj_hum=self.conjugate_tense_pronoun(tense,
#                             vconst.PronounHum)
                    self.conj_display.add(tense, vconst.PronounHum, 
                    conj_huwa[:-2]+YEH_HAMZA+DAMMA+WAW+ALEF)

                else :
                    self.conj_display.add(tense, vconst.PronounHya, 
                    conj_huwa+TEH+SUKUN)
                    self.conj_display.add(tense, vconst.PronounHuma_f, 
                    conj_huwa+TEH+FATHA+ALEF)
                    self.conj_display.add(tense, vconst.PronounHuma, 
                    conj_huwa+ALEF)
                    if conj_huwa.endswith(KASRA+YEH+FATHA):
                        self.conj_display.add(tense, vconst.PronounHum, 
                        conj_huwa[:-3]+DAMMA+WAW+ALEF)
                    else:
                        self.conj_display.add(tense, vconst.PronounHum, 
                        conj_huwa[:-1]+DAMMA+WAW+ALEF)
            elif tense in (vconst.TenseFuture, vconst.TensePassiveFuture, 
            vconst.TenseJussiveFuture, vconst.TenseSubjunctiveFuture, 
            vconst.TenseConfirmedFuture, vconst.TensePassiveJussiveFuture, 
            vconst.TensePassiveSubjunctiveFuture, 
            vconst.TensePassiveConfirmedFuture):
                conj_ana = self.conjugate_tense_pronoun(tense, 
                vconst.PronounAna)
                self.conj_display.add(tense, vconst.PronounAna, 
                conj_ana)

                conj_anta = self.conjugate_tense_pronoun(tense, 
                vconst.PronounAnta)
                self.conj_display.add(tense, vconst.PronounAnta, 
                conj_anta)
                conj_anta_without_future_letter = conj_anta[1:]
##                    self.conj_display.add(tense, vconst.PronounAnta, 
##                  TEH+conj_ana_without_future_letter)
                self.conj_display.add(tense, vconst.PronounNahnu, 
                NOON+conj_anta_without_future_letter)
                self.conj_display.add(tense, vconst.PronounHuwa, 
                YEH+conj_anta_without_future_letter)
                self.conj_display.add(tense, vconst.PronounHya, 
                TEH+conj_anta_without_future_letter)

                conj_anti = self.conjugate_tense_pronoun(tense, 
                vconst.PronounAnti)
                self.conj_display.add(tense, vconst.PronounAnti, 
                conj_anti)

                conj_antuma = self.conjugate_tense_pronoun(tense, 
                vconst.PronounAntuma)
                self.conj_display.add(tense, vconst.PronounAntuma, 
                conj_antuma)
                self.conj_display.add(tense, vconst.PronounAntuma_f, 
                conj_antuma)
                self.conj_display.add(tense, vconst.PronounHuma_f, 
                conj_antuma)
                self.conj_display.add(tense, vconst.PronounHuma, 
                YEH+conj_antuma[1:])

                conj_antum = self.conjugate_tense_pronoun(tense, 
                vconst.PronounAntum)
                self.conj_display.add(tense, vconst.PronounAntum, 
                conj_antum)
                self.conj_display.add(tense, vconst.PronounHum, 
                YEH+conj_antum[1:])

                conj_antunna = self.conjugate_tense_pronoun(tense, 
                vconst.PronounAntunna)
                self.conj_display.add(tense, vconst.PronounAntunna, 
                conj_antunna)
                self.conj_display.add(tense, vconst.PronounHunna, 
                YEH+conj_antunna[1:])
            elif tense == vconst.TenseImperative or \
             tense == vconst.TenseConfirmedImperative:
                for pron in  vconst.ImperativePronouns:
                    conj  =  self.conjugate_tense_pronoun(tense, pron)
                    self.conj_display.add(tense, pron, conj)
        if not self.transitive:
            for tense in vconst.TablePassiveTense:
                for pron in vconst.PronounsTableNotPassiveForUntransitive:
                    self.conj_display.add(tense, pron, u"")
# if the result is not diplyed directely on the screen, we return it
        result  =  self.conj_display.display(self.conj_display.mode, 
        listtense)
        if result:
            return result

    def conjugate_tense_for_pronoun(self, tense, pronoun):
        """
        Conjugate a verb  for a pronoun in specific tense, 
        we use an homoginized conjugation 
        @param tense: given tense
        @type tense: unicode
        @param pronoun: given pronoun
        @type pronoun: unicode
        @return: conjugated verb 
        @rtype: unicode;        
        """
        # the idea is to generate some conjugation from others
        #  in particalar cases, we can generate conjugation 
        # from others pronouns.
        #  for each tense we have two pronouns lists: 
        #    - direct conjugated pronouns.
        #    - indirect conjugated pronouns.

        if tense == vconst.TensePast:
            # direct concongated pronouns
            if pronoun in (vconst.PronounAna, vconst.PronounNahnu, 
            vconst.PronounHunna, vconst.PronounHuma , vconst.PronounHum,
             vconst.PronounHunna, vconst.PronounHuwa, vconst.PronounHya):
                conj = self.conjugate_tense_pronoun( tense, pronoun)
                self.conj_display.add(tense, pronoun, conj)
            # indirect conjugation
            # from Aana Pronoun
            elif pronoun in (vconst.PronounAnta, vconst.PronounAnta, 
            vconst.PronounAnti, vconst.PronounAntuma, vconst.PronounAntuma_f, 
            vconst.PronounAntum, vconst.PronounAntunna):
                # test if the verb is conjugated 
                conj_ana = self.conj_display.get_conj(tense, pronoun)
                if conj_ana == u"":
                    conj_ana = self.conjugate_tense_pronoun(tense, 
                    vconst.PronounAna)
                conj_ana_without_last_mark = conj_ana[:-1]
                if pronoun == vconst.PronounAnta:
                    self.conj_display.add(tense, vconst.PronounAnta, 
                    conj_ana_without_last_mark+FATHA)
                elif pronoun == vconst.PronounAnti:
                    self.conj_display.add(tense, vconst.PronounAnti, 
                    conj_ana_without_last_mark+KASRA)
                elif pronoun == vconst.PronounAntuma :
                    self.conj_display.add(tense, vconst.PronounAntuma,
                     conj_ana+MEEM+FATHA+ALEF)
                elif pronoun == vconst.PronounAntuma_f:
                    self.conj_display.add(tense, vconst.PronounAntuma_f,
                     conj_ana+MEEM+FATHA+ALEF)
                elif pronoun == vconst.PronounAntum:
                    self.conj_display.add(tense, vconst.PronounAntum,
                     conj_ana+MEEM)
                elif pronoun == vconst.PronounAntunna:
                    self.conj_display.add(tense, vconst.PronounAntunna,
                     conj_ana+NOON+SHADDA+FATHA)

            # indirect conjugation
            # from  Hya Pronoun
            elif pronoun ==  vconst.PronounHuma_f:
                # test if the verb is conjugated 
                conj_hya = self.conj_display.get_conj(tense, vconst.PronounHya)
                if conj_hya == u"":
                    conj_hya = self.conjugate_tense_pronoun(tense, 
                    vconst.PronounHya)
                self.conj_display.add(tense, vconst.PronounHuma_f, 
                conj_hya[:-1]+FATHA+ALEF)
        elif tense == vconst.TensePassivePast:
            # direct conjugation
            if pronoun in (vconst.PronounAna, vconst.PronounNahnu, 
            vconst.PronounHunna, vconst.PronounHunna, vconst.PronounHuwa):
                conj = self.conjugate_tense_pronoun(tense, pronoun)
                self.conj_display.add(tense, pronoun, conj)
            # indirect conjugation
            # Ana pronoun like conjugation
            elif pronoun in (vconst.PronounAnta, vconst.PronounAnti, 
            vconst.PronounAntuma, vconst.PronounAntuma_f, vconst.PronounAntum, 
            vconst.PronounAntunna):
                conj_ana = self.conj_display.get_conj(tense, vconst.PronounAna)
                if conj_ana == u"":
                    conj_ana = self.conjugate_tense_pronoun(tense, 
                    vconst.PronounAna)
                    self.conj_display.add(tense, vconst.PronounAna, 
                    conj_ana) 
                conj_ana_without_last_mark = conj_ana[:-1]
                if pronoun == vconst.PronounAnta:
                    self.conj_display.add(tense, vconst.PronounAnta, 
                    conj_ana_without_last_mark+FATHA)
                elif pronoun == vconst.PronounAnti:
                    self.conj_display.add(tense, vconst.PronounAnti, 
                    conj_ana_without_last_mark+KASRA)
                elif pronoun == vconst.PronounAntuma:
                    self.conj_display.add(tense, vconst.PronounAntuma, 
                    conj_ana+MEEM+FATHA+ALEF)
                elif pronoun == vconst.PronounAntuma_f:
                    self.conj_display.add(tense, vconst.PronounAntuma_f, 
                    conj_ana+MEEM+FATHA+ALEF)
                elif pronoun == vconst.PronounAntum:
                    self.conj_display.add(tense, vconst.PronounAntum, 
                    conj_ana+MEEM)
                elif pronoun == vconst.PronounAntunna:
                    self.conj_display.add(tense, vconst.PronounAntunna, 
                    conj_ana+NOON+SHADDA+FATHA)
            # indirect conjugation
            # Ana pronoun like conjugation
            elif pronoun in ( vconst.PronounHya, vconst.PronounHuma_f, 
            vconst.PronounHuma, vconst.PronounHum):
                conj_huwa = self.conj_display.get_conj(tense, 
                vconst.PronounHuwa)
                if conj_huwa == u"":
                    conj_huwa = self.conjugate_tense_pronoun(tense, 
                    vconst.PronounHuwa)
                    self.conj_display.add(tense, vconst.PronounHuwa, conj_huwa)
# حالة الفعل مهموز الآخر
                if conj_huwa.endswith(YEH+HAMZA+FATHA) :
                    self.conj_display.add(tense, vconst.PronounHya, 
                    conj_huwa[:-2]+YEH_HAMZA+FATHA+TEH+SUKUN)
                    self.conj_display.add(tense, vconst.PronounHuma_f, 
                    conj_huwa[:-2]+YEH_HAMZA+FATHA+TEH+FATHA+ALEF)
                    self.conj_display.add(tense, vconst.PronounHuma, 
                    conj_huwa[:-2]+YEH_HAMZA+FATHA+ALEF)

                    self.conj_display.add(tense, vconst.PronounHum, 
                    conj_huwa[:-2]+YEH_HAMZA+DAMMA+WAW+ALEF)

                else :
                    self.conj_display.add(tense, vconst.PronounHya, 
                    conj_huwa+TEH+SUKUN)
                    self.conj_display.add(tense, vconst.PronounHuma_f, 
                    conj_huwa+TEH+FATHA+ALEF)
                    self.conj_display.add(tense, vconst.PronounHuma, 
                    conj_huwa+ALEF)
                    if conj_huwa.endswith(KASRA+YEH+FATHA):
                        self.conj_display.add(tense, vconst.PronounHum, 
                        conj_huwa[:-3]+DAMMA+WAW+ALEF)
                    else:
                        self.conj_display.add(tense, vconst.PronounHum, 
                        conj_huwa[:-1]+DAMMA+WAW+ALEF)
        elif tense in (vconst.TenseFuture, vconst.TensePassiveFuture, 
        vconst.TenseJussiveFuture, vconst.TenseSubjunctiveFuture, 
        vconst.TenseConfirmedFuture, vconst.TensePassiveJussiveFuture, 
        vconst.TensePassiveSubjunctiveFuture, 
        vconst.TensePassiveConfirmedFuture):

            # direct pronouns conjugations
            if pronoun in (vconst.PronounAna, vconst.PronounAnta, 
            vconst.PronounAnti, vconst.PronounAntuma, vconst.PronounAntum,
             vconst.PronounAntunna):
                conj = self.conjugate_tense_pronoun(tense, pronoun)
                self.conj_display.add(tense, pronoun, conj)
            # indirect pronouns
            # Anta pronouns conjugation like
            elif pronoun in (vconst.PronounNahnu, vconst.PronounHuwa, 
            vconst.PronounHya):
                conj_anta = self.conj_display.get_conj(tense, 
                vconst.PronounAnta)
                if conj_anta == u"":
                    conj_anta = self.conjugate_tense_pronoun(tense, 
                    vconst.PronounAnta)
                    self.conj_display.add(tense, vconst.PronounAnta, 
                    conj_anta)

                conj_anta_without_future_letter = conj_anta[1:]
                if pronoun == vconst.PronounNahnu:
                    self.conj_display.add(tense, vconst.PronounNahnu, 
                    NOON+conj_anta_without_future_letter)
                elif pronoun == vconst.PronounHuwa:
                    self.conj_display.add(tense, vconst.PronounHuwa, 
                    YEH+conj_anta_without_future_letter)
                elif pronoun == vconst.PronounHya:
                    self.conj_display.add(tense, vconst.PronounHya, 
                    TEH+conj_anta_without_future_letter)
            # indirect pronouns
            # Antuma pronouns conjugation like
            elif pronoun in (vconst.PronounAntuma, vconst.PronounAntuma_f, 
            vconst.PronounHuma, vconst.PronounHuma_f ):
                conj_antuma = self.conj_display.get_conj(tense, 
                vconst.PronounAntuma)
                if conj_antuma == u"":
                    conj_antuma = self.conjugate_tense_pronoun(tense, 
                    vconst.PronounAntuma)
                    self.conj_display.add(tense, vconst.PronounAntuma, 
                    conj_antuma)
                if pronoun == vconst.PronounAntuma_f:
                    self.conj_display.add(tense, vconst.PronounAntuma_f, 
                    conj_antuma)
                if pronoun == vconst.PronounHuma_f:
                    self.conj_display.add(tense, vconst.PronounHuma_f, 
                    conj_antuma)
                if pronoun == vconst.PronounHuma:
                    self.conj_display.add(tense, vconst.PronounHuma, 
                    YEH+conj_antuma[1:])
            # indirect pronouns
            # Antum pronouns conjugation like
            elif pronoun == vconst.PronounHum:
                conj_antum = self.conj_display.get_conj(tense, 
                vconst.PronounAntum)
                if conj_antum == u"":
                    conj_antum = self.conjugate_tense_pronoun(tense, 
                    vconst.PronounAntum)
                    self.conj_display.add(tense, vconst.PronounAntum, 
                    conj_antum)
                self.conj_display.add(tense, vconst.PronounHum, 
                YEH+conj_antum[1:])
            # indirect pronouns
            # Antum pronouns conjugation like
            elif pronoun == vconst.PronounHunna:
                conj_antunna = self.conj_display.get_conj(tense, 
                vconst.PronounAntunna)
                if conj_antunna == u"":
                    conj_antunna = self.conjugate_tense_pronoun(tense, 
                    vconst.PronounAntunna)
                    self.conj_display.add(tense, vconst.PronounAntunna, 
                    conj_antunna)
                self.conj_display.add(tense, vconst.PronounHunna, 
                YEH+conj_antunna[1:])
        elif tense == vconst.TenseImperative or \
         tense == vconst.TenseConfirmedImperative:
            conj = self.conjugate_tense_pronoun(tense, pronoun)
            self.conj_display.add(tense, pronoun, conj)
        # the cnjugated form is stored in cnj_display
        return self.conj_display.get_conj(tense, pronoun)
#####################################
#{ Irregular verbs functions
#####################################        
    def _is_irregular_verb(self):
        """
        Return True if the verb is irregular, 
        founded in the irregular verb table
        إرجاع إّذا كان الفعل ضاذا.
        الأفعال العربية الخاصة هي
        رأى، أكل أمر سأل،
#        ج- إذا كان يتصرف من باب (مَنَعَ يَمْنَعُ)، 
تحذف واوه, نحو: وَضَعَ، يَضَعُ، وَجَأَ يَجَأُ،
 وَدَعَ يَدَعُ، وَزَعَ يَزَعُ، وَضَأَ يَضَأُ، وَطَأَ يَطَأُ، 
وَقَعَ يَقَعُ، وَلَغَ يَلَغُ، وَهَبَ يَهَبُ، 
عدا خمسة أفعال هي: (وَبَأ)، و(وَبَهَ)، و(وَجَعَ)، و(وَسَعَ)، و(وَهَلَ)،
 فلا تحذف منها الواو؛ فنقول: يَوْبَأُ، يَوْبَهُ، يَوْجَعُ، يَوْسَعُ، يَوْهَلُ.
  الأفعال (وَبَأ)، و(وَبَهَ)، و(وَجَعَ)، و(وَسَعَ)، و(وَهَلَ)، الفعل وبَأ يوبأ        
        @return:True if irregular
        @rtype: Boolean
        """        
        if len(self.word_letters) != 3:
            return False
        else:
            # the key is composed from the letters and past and future marks,
            # to identify irregular verb
            key = self.word_letters + self.past_haraka+self.future_type
            if vconst.IRREGULAR_VERB_CONJUG.has_key(key ):
                return True
        return False


    def _get_irregular_future_stem(self):
        """
        Get the future stem for irregular verb.
        @return: the future conjuagtion stem
        @rtype: unicode;        
        """        
      # the key is composed from the letters and past and future marks,
      # to identify irregular verb
        key = self.word_letters+self.past_haraka+self.future_type
        if  vconst.IRREGULAR_VERB_CONJUG.has_key(key):
            return vconst.IRREGULAR_VERB_CONJUG[key][vconst.TenseFuture]
        else:
            return self.word_letters


    def _get_irregular_passivefuture_stem(self):
        """
        Get the passive future stem for irregular verb.
        @return: the passive future conjuagtion stem
        @rtype: unicode;        
        """        
      # the key is composed from the letters and past and future marks, 
      # to identify irregular verb
        key = self.word_letters+self.past_haraka+self.future_type
        if vconst.IRREGULAR_VERB_CONJUG.has_key(key):
            return vconst.IRREGULAR_VERB_CONJUG[key][vconst.TensePassiveFuture]
        else:
            return self.word_letters


    def _get_irregular_imperative_stem(self):
        """
        Get the imperative stem for irregular verb.
        @return: the passive imperative conjuagtion stem
        @rtype: unicode;        
        """        
      # the key is composed from the letters and past and future marks, 
      # to identify irregular verb
        key = self.word_letters + self.past_haraka+self.future_type
        if  vconst.IRREGULAR_VERB_CONJUG.has_key(key):
            return vconst.IRREGULAR_VERB_CONJUG[key][vconst.TenseImperative]
        else:
            return self.word_letters

# prepare the irregular conjug for future and imperative
# تحضير جذوع التصريف في المضارع والأمر للأفعال الضاذة
    def _prepare_irregular_future_imperative_stem(self):
        """
        Prepare the conjugation stems for future tenses 
        (future, jussive, subjective) and imperative tense.
        Those stems will be concatenated with conjugation affixes.
        """            
        ##       if self.word_letters in vconst.IRREGULAR_VERB_CONJUG.keys():
        if self._is_irregular_verb():
            (letters, marks) = self._get_irregular_future_stem()
            #vconst.IRREGULAR_VERB_CONJUG[self.word_letters][vconst.TenseFuture]
            #تمت إضافة حركة حرف المضارعة إلى الجذع المستعمل في الفعل الشاذ
            self.tab_conjug_stem[vconst.TenseFuture] = ConjugStem(
            vconst.TenseFuture, letters, marks)
            self.tab_conjug_stem[vconst.TenseJussiveFuture] = ConjugStem(
            vconst.TenseJussiveFuture, letters, marks)
            self.tab_conjug_stem[vconst.TenseSubjunctiveFuture] = ConjugStem(
            vconst.TenseSubjunctiveFuture, letters, marks)
            self.tab_conjug_stem[vconst.TenseConfirmedFuture] = ConjugStem(
            vconst.TenseConfirmedFuture, letters, marks)

            (letters1,  marks1) = self._get_irregular_passivefuture_stem()
            #تمت إضافة حركة حرف المضارعة إلى الجذع المستعمل في الفعل الشاذ
            self.tab_conjug_stem[vconst.TensePassiveFuture] = ConjugStem(
            vconst.TensePassiveFuture, letters1,  marks1)
            self.tab_conjug_stem[vconst.TensePassiveJussiveFuture] = ConjugStem(
            vconst.TensePassiveJussiveFuture, letters1,  marks1)
            self.tab_conjug_stem[vconst.TensePassiveSubjunctiveFuture] = \
            ConjugStem(vconst.TensePassiveSubjunctiveFuture, letters1,  marks1)
            self.tab_conjug_stem[vconst.TensePassiveConfirmedFuture] = \
            ConjugStem(vconst.TensePassiveConfirmedFuture, letters1,  marks1)

            (letters2,  marks2) = self._get_irregular_imperative_stem()
            self.tab_conjug_stem[vconst.TenseImperative] = ConjugStem(
            vconst.TenseImperative, letters2,  marks2)
            self.tab_conjug_stem[vconst.TenseConfirmedImperative] = \
            ConjugStem(vconst.TenseConfirmedImperative, letters2,  marks2)
        return False


    def get_conj(self, tense, pronoun):
        """
        Get the conjugated verb by tense and pronoun.
        @param tense: tense of the added conjuagtion.
        @type tense: unicode
        @param pronoun: pronoun of the added conjuagtion.
        @type pronoun: unicode
        @return : conjugated form of verb if exists.
        @rtype : unicode
        """
        return self.conj_display.get_conj(tense, pronoun)

    def get_pronoun_features(self, pronoun):
        """
        Get the features of  given pronoun.
        @param pronoun: pronoun of conjuagtion.
        @type pronoun: unicode
        @return : dictionary of pronoun attributes.
        @rtype : dictionary
        """
        return vconst.PRONOUN_FEATURES.get(pronoun, None)
    def get_tense_features(self, tense):
        """
        Get the features of  given tense.
        @param tense: tense of the conjuagtion.
        @type tense: unicode
        @return : dictionary of tense attributes.
        @rtype : dictionary
        """
        return vconst.TENSE_FEATURES.get(tense, None)
