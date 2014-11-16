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
sys.path.append('../lib')
import qalsadi.stemmedword as stemmedword

import aranasyn.syn_const as syn_const
import pyarabic.araby as araby
import math
class StemmedSynWord (stemmedword.StemmedWord):
    """
    stemmedWord represents the data resulted from the morpholocigal analysis
    """
    def __init__(self, result_dict = None, order = -1):
        # ToDo
        # copy the super class attributes to curesult_dictrrent classe
        #stemmedword.stemmedWord.__init__(self, result_dict.get_dict())
        
        if result_dict: 
            self.__dict__ = result_dict.__dict__.copy()
            self.unvocalized =  araby.strip_tashkeel(self.vocalized)
            self.unvoriginal =  araby.strip_tashkeel(self.original)
        self.tag_verbal_factor  =   0
        self.tag_nominal_factor =   0
        self.tag_kana_rafe3     =   False         
        if self.is_stopword():
            self.tag_kana_rafe3 =   self._is_kana_rafe3()  
            self.tag_nominal_factor = self.__get_nominal_factor()
            #verbal factor
            self.tag_verbal_factor  = self.__get_verbal_factor()

        #~self.tag_direct_addition =  self._is_direct_addition()
        self.tag_addition =  self._is_addition()                

        self.tag_break =  self._is_break() 
        self.tag_kana_noun = False # اسم كان
        self.tag_inna_noun = False # اسم إنّ
        #~self.set_order(order)
        self.forced_word_case = False
        self.syntax =  u""   # used for syntaxique analysis porpos
        self.semantic =  u""  # used for semantic analysis porposes
        #~self.unvocalized =  u""
        #~self.unvoriginal =  u""
        self.forced_wordtype = False        
        self.order =  order
        self.next =  {}
        self.previous =  {}
        # to , specify semantic relations
        self.sem_next =  {}
        self.sem_previous =  {}
        self.score =  0
 

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
    #~def set_unvocalized(self, newunvocalized):
        #~"""
        #~Set the unvocalized word
        #~@param newunvocalized: the new given unvocalized.
        #~@type newunvocalized: unicode string
        #~"""
        #~self.unvocalized =  newunvocalized
        
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
        #self.syntax =  ':'.join([self.syntax, 'O%d'%order])
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
        return self.next.keys()

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
            return self.next.has_key(nextw.get_order())
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
        #self.syntax =  ':'.join([self.syntax, 'P%d[%d]'%(previous, weight)])
        self.previous[previous] = weight

    def get_previous(self):
        """
        get all privous word list of relations.
        """
        return self.previous.keys()

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
        return self.sem_next.keys()


    def has_sem_next(self):
        """
        get True if current word has semantic next relations
        @return: if the word has next relations
        @rtype: boolean
        """
        return self.sem_next != {}

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
        return self.sem_previous.keys()
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
        if (not self.has_encletic()) and \
        u"كان و أخواتها" in self.get_tags():    
            return True
        return False


    def _is_addition(self):
        """
        Return True if the word is a  nominal addition اسم إضافة مثل نحو ومعاذ
        @rtype: True/False
        """
        if u'اسم إضافة' in self.get_tags() and not self.has_encletic():
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
        if self.get_unvocalized() in syn_const.VERBAL_FACTOR_LIST :
            self.tag_verbal_factor = 1
        # with encletics
        elif self.has_encletic() and \
        self.get_unvoriginal() in syn_const.VERBAL_FACTOR_LIST :
            self.tag_verbal_factor = 1
        # with encletic and Harakat            
        elif self.has_encletic() and \
        self.get_original() in syn_const.VERBAL_FACTOR_LIST:
            self.tag_verbal_factor = 1
            
        #~if self.tag_verbal_factor:
        #~if self._is_verb_rafe3():
        if self.get_vocalized() in syn_const.VERB_RAFE3_LIST or \
        (not self.has_encletic() and \
        self.get_original() in syn_const.VERB_RAFE3_LIST ): 
            self.tag_verbal_factor += 2 
            
        #~if self._is_verb_naseb() :
        if self.get_vocalized() in syn_const.VERB_NASEB_LIST \
         or (not self.has_encletic() and \
        self.get_original() in syn_const.VERB_NASEB_LIST ):                
            self.tag_verbal_factor += 4 

        #~if self._is_verb_jazem() :
        if self.get_vocalized() in syn_const.JAZEM_LIST  \
         or (not self.has_encletic() and \
         self.get_original() in syn_const.JAZEM_LIST  ):
                self.tag_verbal_factor += 16
                
            #~# if factor is different from 1 then is active
            #~if self.tag_verbal_factor > 1 :
                #~self.tag_verbal_factor += 32
                 
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
        Jazem              : 16 10000
        active             : 32 100000
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
        # Jazem     جازم                       NOMINAL_FACTOR_LIST
        if self.get_unvocalized() in syn_const.NOMINAL_FACTOR_LIST:
            self.tag_nominal_factor = 1
        # with encletics
        elif self.has_encletic() and \
        self.get_unvoriginal() in syn_const.NOMINAL_FACTOR_LIST:
            self.tag_nominal_factor = 1
        # with encletic and Harakat            
        elif self.has_encletic() and \
        self.get_original() in syn_const.NOMINAL_FACTOR_LIST:
            self.tag_nominal_factor = 1
            
        #~if self.tag_nominal_factor:
        #~if self._is_noun_rafe3():
        if self.get_unvocalized() in syn_const.RAFE3_LIST or \
        (not self.has_encletic() and \
        self.get_unvoriginal() in syn_const.RAFE3_LIST ) or \
         (not self.has_encletic()) and \
          u"كان و أخواتها" in self.get_tags():           
            self.tag_nominal_factor += 2 
            
        #~if self._is_noun_naseb() :
        if self.get_vocalized() in syn_const.NOUN_NASEB_LIST :
            self.tag_nominal_factor += 4 
        elif (not self.has_encletic()) and \
        u"إن و أخواتها" in self.get_tags():
            self.tag_nominal_factor += 4 
        elif (not self.has_encletic() and \
        self.get_original() in syn_const.NOUN_NASEB_LIST ):
            self.tag_nominal_factor += 4 

        #~if self._is_noun_jar() :
        if self.get_unvocalized() in syn_const.JAR_LIST or \
           self.get_original() in syn_const.JAR_LIST:
            self.tag_nominal_factor += 8        
        elif (not self.has_encletic()):
            if  u"حرف جر" in self.get_tags() or \
             u"ظرف مكان" in self.get_tags() or \
              u"اسم إضافة" in self.get_tags():
                self.tag_nominal_factor += 8        

            # if factor is different from 1 then is active
            #~if self.tag_nominal_factor > 1 :
                #~#self.tag_nominal_factor += 1
                #~self.tag_nominal_factor += 32
                 
        return self.tag_nominal_factor

        
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
        elif self.is_stopword():
            return True
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
        return self.get_unvoriginal() in syn_const.PRONOUN_LIST

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
        return bool(self.tag_nominal_factor / 8 % 2)

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

    def is_kana_noun(self):
        """
        Return True if the word is a  Kana Noun اسم كان منصوب.
        @return:  is a  Kana Noun.
        @rtype: True/False
        """
        return self.tag_kana_noun

    def set_kana_noun(self):
        """
        Set True to the word to be  Kana Noun اسم كان منصوب.
        """
        self.tag_kana_noun =  True

    def is_inna_noun(self):
        """
        Return True if the word is a  Inna Noun اسم إنّ مرفوع.
        @return:  is a  Inna Noun.
        @rtype: True/False
        """
        return self.tag_inna_noun

    def set_inna_noun(self):
        """
        Set True to the word to be  Inna Noun اسم إنّ.
        """
        self.tag_inna_noun =  True

    def is_verbal_factor(self):
        """
        Return True if the word is a  verbal factor.
        @return:  is a  verbal factor.
        @rtype: True/False
        """    
        #~return bool(self.tag_verbal_factor % 2)
        return bool(self.tag_verbal_factor)

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
        syntax = u', '.join(['O'+repr(self.get_order()), self.get_syntax(),
         'SP'+repr(self.sem_previous), 'SN'+repr(self.sem_next),
          'P'+repr(self.previous)    , 'N'+repr(self.next)])
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
    print "test"
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
    print stmwrd.get_dict()
    print stmwrd.is_initial()
    print stmwrd
if __name__ == "__main__":
    mainly()
    syn_const.NOMINAL_FACTOR_LIST
