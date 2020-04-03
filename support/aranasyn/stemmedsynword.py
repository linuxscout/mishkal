#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        stemmedWord
# Purpose:     representat data analyzed given by morphoanalyzer
# Qalsadi then by syntaxic analyzer
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     19-09-2012
# Copyright:   (c) Taha Zerrouki 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
stemmedWord represents the data resulted from the morpholocigal analysis
"""
import sys
sys.path.append('../')
sys.path.append('mishkal/lib')
sys.path.append('../lib')
#~print sys.path
import math
from operator import xor
import pyarabic.araby as araby
import aranasyn.syn_const as syn_const
import qalsadi
try:
    from  qalsadi import stemmedword #as stemmedword
except:
    pass;
class StemmedSynWord (qalsadi.stemmedword.StemmedWord):
    """
    stemmedWord represents the data resulted from the morpholocigal analysis
    """
    def __init__(self, result_dict = None, order = -1):
        # ToDo
        # copy the super class attributes to result_dict classe
        #~ stemmedword.StemmedWord.__init__(self, result_dict.get_dict())
        #~ stemmedword.StemmedWord.__init__(self, result_dict.__dict__)
        
        if result_dict: 
            self.__dict__ = result_dict.__dict__#.copy()
            self.unvocalized =  araby.strip_tashkeel(self.vocalized)
            self.unvoriginal =  araby.strip_tashkeel(self.original)
        self.tag_verbal_factor  =   0
        self.tag_nominal_factor =   0
        self.tag_kana_rafe3     =   False 
        if self.is_verb():
            self.tag_kana_rafe3 =   self._is_kana_rafe3() 
        if self.is_stopword():
            self.tag_kana_rafe3 =   self._is_kana_rafe3()  
            self.tag_nominal_factor = self.__get_nominal_factor()
            #verbal factor
            self.tag_verbal_factor  = self.__get_verbal_factor()

        self.tag_addition =  self._is_addition()                

        self.tag_break =  self._is_break() 
        self.forced_word_case = False
        self.syntax =  u""   # used for syntaxique analysis porpos
        self.semantic =  u""  # used for semantic analysis porposes
        self.forced_wordtype = False        
        self.order =  order
        self.next =  {}
        self.previous =  {}
        self.sem_next =  {}
        self.sem_previous =  {}
        self.score =  0
        self.rule = 0  # rule used to select the current case in vocalization

    def __del__(self, ):
        """ desctructor """
        pass
    #############################################################
    #{ Attributes Functions
    #############################################################
    def get_unvocalized(self, ):
        """
        Get the unvocalized form of the input word
        @return: the given unvocalized.
        @rtype: unicode string
        """
        if self.unvocalized:
            return self.unvocalized
        else:
            if self.vocalized:
                self.unvocalized = araby.strip_tashkeel(self.vocalized)
            else :
                return u""
        return self.unvocalized
        
    def get_unvoriginal(self, ):
        """
        Get the unvocalized  original form of the input word
        @return: the given unvocalized original.
        @rtype: unicode string
        """
        if self.unvoriginal:
            return self.unvoriginal            
        else :
            if self.original:
                self.unvoriginal =  araby.strip_tashkeel(self.original)
            else:
                return u""
            return self.unvoriginal

    def set_order(self, order):
        """
        Add a position number in the case word list.
        @param order: the order of  the stemmed word in the word case list.
        @tyep order: integer
        """
        self.order = order

    def get_order(self):
        """
        Add a position number in the case word list.
        @param order: the order of  the stemmed word in the word case list.
        @tyep order: integer
        """
        return self.order

    def set_score(self, _score):
        """
        Set the word case score
        @param _score: the _score of  the stemmed word in the word case list.
        @tyep _score: integer
        """
        self.score = _score

    def get_score(self):
        """
        get the case word score
        @param _score: the _score of  the stemmed word in the word case list.
        @tyep _score: integer
        """
        return self.score
    def get_syntax(self, ):
        """
        Get the syntax form of the input word
        @return: the given syntax.
        @rtype: unicode string
        """
        return self.syntax
        
    def set_syntax(self, newsyntax):
        """
        Set the syntax word
        @param newsyntax: the new given syntax.
        @type newsyntax: unicode string
        """
        self.syntax =  newsyntax
    def add_syntax(self, tag):
        """
        Add a new tag to syntax field
        @param tag: the new added tag.
        @tyep tag: unicode
        """
        self.syntax =  ':'.join([self.syntax, tag])        
    def get_semantic(self, ):
        """
        Get the semantic form of the input word
        @return: the given semantic.
        @rtype: unicode string
        """
        return self.semantic
        
    def set_semantic(self, newsemantic):
        """
        Set the semantic word
        @param newsemantic: the new given semantic.
        @type newsemantic: unicode string
        """
        self.semantic =  newsemantic
    def add_next(self, nextw, weight = 1):
        """
        Add  next word position number, if the word is realted
        @param next: the next of  the stemmed word in the word case list.
        @tyep next: integer
        """
        #self.syntax =  ':'.join([self.syntax, 'N%d[%d]'%(next, weight)])
        self.next[nextw] = weight

    def get_next(self):
        """
        get the next positions.
        @param next: the next of  the stemmed word in the word case list.
        @tyep next: integer
        """
        return list(self.next.keys())

    def has_next(self, nextw = None):
        """
        get True if current word has next relations. 
        If The next is given, it returns if the next has relation with current. 
        @param next: a stemmedsynword as next of the current word case.
         if it's None, the fucntion return if there are relation.
        @type next: stemmedsynword.
        @return: if the word has next relations
        @rtype: boolean
        """
        if not nextw:
            return self.next != {}
        else:
            #~ return self.next.has_key(nextw.get_order())
            return bool(set(self.next.keys()).intersection(nextw))
    def has_previous(self, previous = None):
        """
        get True if current word has previous relations.
         If The previous is given, it returns if the previous 
         has relation with current. 
        @param previous: a stemmedsynword as previous of 
        the current word case. if it's None, the fucntion 
        return if there are relation.
        @type previous: stemmedsynword.
        @return: if the word has previous relations
        @rtype: boolean
        """
        if not previous:
            return self.previous != {}
        else:
            return self.previous.has_key(previous.get_order())

    def add_previous(self, previous, weight = 1):
        """
        Add the previous position of the related word.
        @param previous: the previous of  the stemmed word in the word case list.
        @tyep previous: integer
        """
        self.previous[previous] = weight

    def get_rule(self):
        """
        get the selection rule.
        """
        return self.rule
        
    def set_rule(self, rule):
        """
        set the selection rule
        """
        self.rule = rule

    def get_previous(self):
        """
        get all privous word list of relations.
        """
        return list(self.previous.keys())
    def get_previous_relation(self, previous_order):
        """
        get the previous relation between the current case and the previous given by order
        @param previous_order: the previous of  the stemmed word 
        in the word case list.
        @tyep previous_order: integer
        """
        return self.previous.get(previous_order, 0)

    def get_next_relation(self, next_order):
        """
        get the next relation between the current case and the next given by order
        @param next_order: the next of  the stemmed word 
        in the word case list.
        @tyep next_order: integer
        """
        return self.next.get(next_order, 0)
        
    def add_sem_next(self, nextw, weight = 1):
        """
        Add  next word position number, if the word is semanticly related
        @param next: the next of  the stemmed word in the word case list.
        @tyep next: integer
        """
        #self.syntax =  ':'.join([self.syntax, 'SN%d[%d]'%(next, weight)])
        self.sem_next[nextw] = weight

    def get_sem_next(self):
        """
        get the next positions.
        @param next: the next of  the stemmed word in the word case list.
        @tyep next: integer
        """
        return list(self.sem_next.keys())

    def has_sem_previous(self):
        """
        get True if current word has semantic previout relations
        @return: if the word has previous relations
        @rtype: boolean
        """
        return self.sem_previous != {}
    def has_sem_next(self, nextw = None):
        """
        get True if current word has semantic next relations
        @return: if the word has next relations
        @rtype: boolean
        """
        if not nextw:
            return self.sem_next != {}
        #print("has_sem_next", self.sem_next.keys(), nextw)
        return bool(set(self.sem_next.keys()).intersection(nextw))

    def add_sem_previous(self, previous, weight = 1):
        """
        Add the previous position of the semantic related word.
        @param previous: the previous of  the stemmed word in 
        the word case list.
        @tyep previous: integer
        """
        #self.syntax =  ':'.join([self.syntax, 'SP%d[%d]'%(previous, weight)])
        self.sem_previous[previous] =  weight

    def get_sem_previous(self):
        """
        Add a position number in the case word list.
        @param previous: the previous of  the stemmed word in 
        the word case list.
        @tyep previous: integer
        """
        return list(self.sem_previous.keys())
    def forced_case(self):
        """
        Add a new tag to syntax field as foced case
        @param tag: the new added tag.
        @tyep tag: unicode
        """
        self.forced_word_case = True
        #if u"*" not in self.syntax: self.add_syntax(u"*")

    def force_wordtype(self):
        """
        Add a new tag to syntax field as foced word type (noun, verb)
        @param tag: the new added tag.
        @tyep tag: unicode
        """
        self.forced_wordtype = True
        
    def is_forced_case(self):
        """
        verify if the word is a forced word type (noun, verb)
        @return: True/False
        @tyep tag: Boolean
        """
        return self.forced_word_case

    def is_forced_wordtype(self):
        """
        verify if the word is a forced word type (noun, verb)
        @return: True/False
        @tyep tag: Boolean
        """
        return self.forced_wordtype
    ######################################################################
    #{ Tags extraction Functions
    ######################################################################

    def _is_kana_rafe3(self):
        """
        Return True if the word is a  Rafe3.
        @return:  Rafe3.
        @rtype: True/False
        """
        #print self.get_unvoriginal().encode('utf8')
        if (not self.has_encletic()) and \
        u"كان و أخواتها" in self.get_tags():    
            return True
        elif self.get_unvoriginal() in syn_const.KanaSisters_LIST:
            return True
        return False


    def _is_addition(self):
        """
        Return True if the word is a  nominal addition اسم إضافة مثل نحو ومعاذ
        @rtype: True/False
        """
        if (u'اسم إضافة' in self.get_tags() or u'إضافة' in self.get_tags()) and not self.has_encletic():
            return True
        return False
        
    def need_addition(self):
        """
        Return True if the word can be added like  مديرو and not مديرون
        @rtype: True/False
        """
        return self.is_addition() or not (u'لايضاف' in self.get_tags() or self.is_defined() or  self.is_tanwin() or self.has_encletic())
        
    def is_additionable(self):
        """
        Return True if the word can be an addition مضاف إليه
        @rtype: True/False
        """
        # مجرور
        if self.is_majrour() :
            # ليس صفة نكرة
            # يكون معرفة
            if not self.is_adj() or  self.is_defined():
                return True
        return False

    def __get_verbal_factor(self):
        """
        Return int code of verbal factor.
        the inflected cases are coded in binary like
        not defined        : 0  00000
        factor             : 1  00001      
        Rafe3              : 2  00010
        Naseb              : 4  00100
        Jar                : 8  01000
        Jazem              : 16 10000
        active             : 32 100000
        this codification allow to have two verb factor for the same case, 
        like feminin plural which ahve the same mark for Nasb and jar
هذا الترميز يرمز حالتين في وقت واحد
        النصب والجر
        @return: verbal factor state numeric code
        @rtype:        
        """    
        #if the stopword is a  verb factor
        # without vocalization
        # inactive عاطل
        # active عامل
        # Rafe3    رافع
        # Naseb    ناصب
        # Jazem     جازم
        if u"فعل" in self.get_object_type() and not self.has_encletic():
            self.tag_verbal_factor = 1
            # Naseb
            if u"رافع" in self.get_action():
                self.tag_verbal_factor += 2
            if u"ناصب" in self.get_action():
                self.tag_verbal_factor += 4
            if u"جازم" in self.get_action():
                self.tag_verbal_factor += 16 
            #~ if u"عاطل" in self.get_action():
                #~ self.tag_verbal_factor += 32 
                
        return self.tag_verbal_factor


    def __get_nominal_factor(self):
        """
        Return int code of nominal factor.
        the inflected cases are coded in binary like
        not defined        : 0  00000
        factor             : 1  00001      
        Rafe3              : 2  00010
        Naseb              : 4  00100
        Jar                : 8  01000
        this codification allow to have two noun factor for the same case, 
        like feminin plural which ahve the same mark for Nasb and jar
هذا الترميز يرمز حالتين في وقت واحد
        النصب والجر
        @return: nominal factor state numeric code
        @rtype:        
        """    
        #if the stopword is a  noun factor
        # without vocalization
        # inactive عاطل
        # active عامل
        # Rafe3    رافع
        # Naseb    ناصب
        # Jazem     جازم   

        if u"اسم" in self.get_object_type() :
            self.tag_nominal_factor = 1
            # rafe3
            if u"رافع" in self.get_action():
                if not self.has_encletic():
                    self.tag_nominal_factor += 2
                else:
                    self.tag_nominal_factor += 4                    
            if u"ناصب" in self.get_action():
                if  not self.has_encletic(): 
                    self.tag_nominal_factor += 4
                else: # الناصب يتحول إلى رافع إذا ألحق به ضمير متصل
# هذا ينبغي التحقق منه 
                    self.tag_nominal_factor += 2
            # اسم الإشارة المجرور مثل بذلك الرجل أو بهذا الرجل
            if u"اسم إشارة" in self.get_tags():
                if  u"جر" in self.get_tags(): 
                    self.tag_nominal_factor += 8
            
        if u"جار" in self.get_action() and not self.has_encletic():
            self.tag_nominal_factor += 8
        if u"ضمير" in self.get_tags():
            #Rafe3
            self.tag_nominal_factor = 1 + 2
                         
        return self.tag_nominal_factor

    def is_jonction(self,):
        """
        Return True if the word is jonction عطف منفصل.

        @return: is jonction.
        @rtype: True/False
        """
        return  u"متبع" in self.get_action() 
        
    def is_substituted(self,):
        """
        Return True if the word is substitute مبدل منه.

        @return: is substituted.
        @rtype: True/False
        """
        return  u"اسم إشارة" in self.get_tags()        
        
    def is_confirmation(self,):
        """
        Return True if the word is confirmation توكيد.

        @return: is confirmation.
        @rtype: True/False
        """
        return  u"توكيد" in self.get_tags()  
        
    def _is_break(self):
        """
        Return True if the word has break.

        @return: is break.
        @rtype: True/False
        """    
     #تكون الكلمة فاصلة 
    #إذا كانت منفصلة عمّا قبلها.  
                     # الحالات التي تقطع
            # - حرف جر متصل
            # فاصلة أو نقطة
        # if the affix is a break affix 
        if stemmedword.StemmedWord.is_break(self):
            return True
        #~if self.is_direct_jar():
            #~return True            
        elif self.is_pounct() and 'break' in self.get_tags():
            return True
        #~ elif self.is_stopword():
            #~ return True
        else:
            return False

    def is_break(self):
        """
        Return True if the word has break.
        @return: is break.
        @rtype: True/False
        """    
 #تكون الكلمة فاصلة 
#إذا كانت منفصلة عمّا قبلها.  
         # الحالات التي تقطع
        # - حرف جر متصل
        # فاصلة أو نقطة
        return self.tag_break

        

    ###############################################################
    #{ Tags  Functions
    ###############################################################
    def is_initial(self):
        """
        Return True if the word mark the begin of next sentence.
        @return: direct initial.
        @rtype: True/False
        """
        return self.tag_initial

    def is_pronoun(self):
        """
        Return True if the word has the 3rd person.
        @return: has the 3rd persontense.
        @rtype: True/False
        """
        return u"ضمير" in self.get_tags() or u'اسم موصول' in self.get_tags() or  u'اسم إشارة' in self.get_tags()
        #~return self.get_unvoriginal() in syn_const.PRONOUN_LIST

    def canhave_tanwin(self, ):
        """
        return True if the word accept Tanwin
        """
        return u'ينون' in self.get_tags()

    def is_verb_rafe3(self):
        """
        Return True if the word is a  Rafe3 of verb
        @return:  Rafe3 of verb.
        @rtype: True/False
        """
        return bool(self.tag_verbal_factor / 2 % 2)
        
    def is_verb_naseb(self):
        """
        Return True if the word is a  Naseb of verb.
        @return:  Naseb.
        @rtype: True/False
        """    
        return bool(self.tag_verbal_factor / 4 % 2)

    def is_jazem(self, ):
        """
        Return True if the word is a  Jazem.
        @return:  Jazem.
        @rtype: True/False
        """
        return bool(self.tag_verbal_factor / 16 % 2)
    def is_verb_jobless_factor(self):
        """
        Return True if the word is a  a jobless of verb.
        @return:  Njobless.
        @rtype: True/False
        """    
        return bool(self.tag_verbal_factor == 1)

    def is_nominal_factor(self):
        """
        Return True if the word is a  nominal factor.
        @return:  is a  nominal factor.
        @rtype: True/False
        """
        #~return bool(self.tag_nominal_factor % 2)   
        return bool(self.tag_nominal_factor)   

    def is_rafe3(self):
        """
        Return True if the word is a  Rafe3.
        @return:  Rafe3.
        @rtype: True/False
        """
        return bool(self.tag_nominal_factor / 2 % 2) 

    def is_naseb(self):
        """
        Return True if the word is a  Naseb of noun.
        @return:  Naseb of noun.
        @rtype: True/False
        """
        return bool(self.tag_nominal_factor / 4 % 2)
    
    def is_jar(self):
        """
        Return True if the word is a  Jar.
        @return:  Jar.
        @rtype: True/False
        """    
        return bool(self.tag_nominal_factor / 8 % 2) and not self.has_encletic()
    def is_condition_factor(self, ):
        """
        Return True if the word is a  condition factor.
        @return:  condition factor.
        @rtype: True/False
        """
        return self.get_original() in syn_const.CONDITION_FACTORS
        
    def is_kana_rafe3(self):
        """
        Return True if the word is a  Rafe3.
        @return:  Rafe3.
        @rtype: True/False
        """
        return self.tag_kana_rafe3

        
    def is_addition(self):
        """
        Return True if the word is a  Addition اسم إضافة مثل نحو ومعاذ.
        @return:  is a  addition.
        @rtype: True/False
        """
        return self.tag_addition    


    def is_verbal_factor(self):
        """
        Return True if the word is a  verbal factor.
        @return:  is a  verbal factor.
        @rtype: True/False
        """    
        return bool(self.tag_verbal_factor)
    
    def eq_defined(self, otherword):
        """
        Return True if the current word is equal in definition with otherword.
        @return:  equal or not.
        @rtype: True/False
        """          
        eq_defnd = not xor(self.is_defined() , otherword.is_defined())
        eq_tnwn  = not xor(self.is_tanwin() , otherword.is_tanwin())
        return eq_defnd and eq_tnwn
         
         
         
    def eq_case(self, otherword):
        """
        Return True if the current word is equal in case إعراب with otherword.
        @return:  equal or not.
        @rtype: True/False
        """          
        return ( (self.is_majrour() and otherword.is_majrour()) \
            or (self.is_mansoub() and otherword.is_mansoub()) \
            or (self.is_marfou3()and otherword.is_marfou3()))

    def eq_gender(self, otherword):
        """
        Return True if the current word is equal in gender النوع ذكر أنثى with otherword.
        @return:  equal or not.
        @rtype: True/False
        """          
        return ( (self.is_feminin() and otherword.is_feminin()) 
           or (self.is_masculin() and otherword.is_masculin())
        )
    def eq_number(self, otherword):
        """
        Return True if the current word is equal in number العدد مفرد مثنى جمع with otherword.
        @return:  equal or not.
        @rtype: True/False
        """          
        return ( (self.is_plural() and otherword.is_plural()) 
             or  (self.is_dual() and otherword.is_dual())
            or (self.is_single() and otherword.is_single())
             )
    def eq_person(self, otherword):
        """
        Return True if the current word is equal in person الشخض متكلم مخاطب غائب with otherword.
        @return:  equal or not.
        @rtype: True/False
        """          
        return ( (self.is_speaker_person() and otherword.is_speaker_person()) 
             or (self.is_present_person() and otherword.is_present_person())
             or (self.is_absent_person() and otherword.is_absent_person()))
                


    def ajust_tanwin(self):
        """
        ajust the Tanwin case, if the word is independent from the next one.
        @return:  Nothing.
        @rtype: 
        """    
        if self.is_noun() and not self.is_stopword() and not self.is_defined()\
        and not self.has_encletic() and not self.is_mamnou3():
            #self.vocalized += '4'
            if self.vocalized.endswith(araby.DAMMA):
                self.vocalized = self.vocalized[:-1]+araby.DAMMATAN
            elif self.vocalized.endswith(araby.KASRA):
                self.vocalized = self.vocalized[:-1]+araby.KASRATAN
            elif self.vocalized.endswith(araby.TEH_MARBUTA+araby.FATHA):
                self.vocalized = self.vocalized[:-1]+araby.FATHATAN
            elif self.vocalized.endswith(araby.FATHA+araby.ALEF):
                self.vocalized = self.vocalized[:-2]+araby.FATHATAN+araby.ALEF
        

    def recalculate_score(self, previous_case_position, previous_score):
        """
        Recalculate score according to previous node.
        @param previous_case_position: the pervious position in previos table
        @type  previous_case_position: integer
        @param previous_score: the word case previous score
        @type  previous_score: integer.
        @return: nothing
        @rtype: void
        """
        #self.score =  0
        
        # the score is calculated
        # syntaxic relations
        score =  1
        # if the current node has relation with previous as semantic
        if self.sem_previous.has_key(previous_case_position):
            self.sem_previous[previous_case_position] = max(
            self.previous[previous_case_position], previous_score*2)
            score +=  self.sem_previous[previous_case_position]
        # if the current node has relation with previous as synatxic
        if self.previous.has_key(previous_case_position):
            self.previous[previous_case_position] =  max(
            self.previous[previous_case_position], previous_score *1)
            score +=  self.previous[previous_case_position*1]
        # case if the previous has no relation with the current*
        score +=  len(self.sem_previous)*2 +len(self.previous)*1
        # To prefere semantic nexts relation then
        # to favorize syntaxic next relations
        score  *=  (len(self.sem_next)*2+len(self.next)*1)

        # Add frequency value as logarithm
        score *=  round(math.log(self.freq+1), 2)
        # favorize the word if it's stopword
        #score +=  self.is_stopword()*50
        
        # the the max between acutal score and given score
        self.score =  max(self.score, score)
        
        #self.add_syntax("Scr:"+str(self.score))


    def calculate_score(self, ):
        """
        Recalculate score.
        @return: nothing
        @rtype: void
        """
        self.score =  0
        
        # the score is calculated
        #
        # syntaxic relations
        self.score =  len(self.next)*10 #self.has_next()*10
        self.score +=  len(self.previous)*10#(self.previous>0)*10
        self.score +=  len(self.sem_previous)*100 #(self.sem_previous>0)
        self.score +=  len(self.sem_next)*100 # self.has_sem_next()*100 
        self.score +=  round(math.log(self.freq+1), 2)
        self.score +=  self.is_stopword()*50
        self.add_syntax("Scr:"+str(self.score))


    def get_dict(self, ):
        """
        get dictionary of attributes 
        """
        syntax = {"SP":self.sem_previous, 
                "SN":self.sem_next,
                "P":self.previous, 
                "N":self.next,
                }
        #syntax = u', '.join(['O'+repr(self.get_order()), self.get_syntax(),
        # 'SP'+repr(self.sem_previous), 'SN'+repr(self.sem_next),
        #  'P'+repr(self.previous)    , 'N'+repr(self.next)])
        ret_dict = self.__dict__
        ret_dict['syntax'] = syntax
        return ret_dict
    def __repr__(self):
        """
        represent the class as string
        """
        text = u"'%s':%s, \n " % (self.__dict__['order'], 
        self.__dict__['vocalized'])
        for k in self.__dict__.keys():
            text +=  u"\t'%s':\t%s, \n " % (k, self.__dict__[k])
        return text.encode('utf8') 
        #return repr(self.__dict__)

def mainly():
    """
    main test
    """
    print("test")
    rdict = {}
    rdict =  {"word": u"الحياة", # input word
            "vocalized": u"الْحَيَاةُ",
             # vocalized form of the input word 
            "procletic": u"ال", # the syntaxic pprefix called procletic
            "prefix": u"", # the conjugation or inflection prefix
            "stem": u"حياة", # the word stem
            "suffix": u"ُ", # the conjugation suffix of the word
            "encletic": u"", # the syntaxic suffix
            
            "tags": u"تعريف::مرفوع*", 
            # tags of affixes and tags extracted form lexical dictionary

            "freq": 0, # the word frequency from Word Frequency database 
            "root": u"", # the word root not yet used
            "template": u"", # the template وزن 
            "type": u"Noun:مصدر", # the word type
            "original": u"حَيَاةٌ", 
            #original word from lexical dictionary
            "syntax":u"", # used for syntaxique analysis porpos
            u'semantic':u'', 
            }
    rdict = stemmedword.StemmedWord(rdict)
    stmwrd = StemmedSynWord(rdict)    
    print(stmwrd.get_dict())
    print(stmwrd.is_initial())
    print(stmwrd)
if __name__ == "__main__":
    mainly()
    syn_const.NOMINAL_FACTOR_LIST
