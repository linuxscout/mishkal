#!/usr/bin/python
# -*- coding  =  utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        stemmedAffix
# Purpose:     representat affix data analyzed given by morphoanalyzer  Qalsadi
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     19-09-2012
# Copyright:   (c) Taha Zerrouki 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
stemmedAffix represents the data resulted from the morpholocigal analysis
"""
import sys
sys.path.append('../lib/')
import pyarabic.araby as araby
#~import qalsadi.analex_const 
class StemmedAffix:
    """
    stemmedAffix represents the data resulted from the morpholocigal analysis
    """
    def __init__(self, result_dict = None):

        # extracted affix attributes
        self.procletic  =   u"", # the syntaxic pprefix called procletic
        self.prefix  =   u"", # the conjugation or inflection prefix
        self.suffix  =   u"", # the conjugation suffix of the word
        self.encletic  =   u"", # the syntaxic suffix
        self.type  =   u"", # the word type used with affix        
        self.tags  =   u"",
        self.tag_break = False
        # tags of affixes and tags extracted form lexical dictionary

        if result_dict:
            aff  =  result_dict.get('affix', [])
            if aff:
                self.procletic     =  aff[0]            
                self.prefix     =  aff[1]
                self.suffix     =  aff[2]
                self.encletic     =  aff[3]
            self.affix   =  u'-'.join([self.procletic, self.prefix, 
               self.suffix, self.encletic])
            self.tags     =  result_dict.get('tags', u'')
            self.type     =  result_dict.get('type', u'')

        # not noun or stopword 
        self.tag_stopword     =  False
        self.tag_noun         =  False        
        self.tag3rdperson      =  False        
        self.tag3rdperson      =  False
        self.tag_majzoum      =  False
        self.tag_passive         =  False
        self.tag_past         =  False
        self.tag_present         =  False
        self.tag_defined      =  False
        self.tag_majrour         =  False
        self.tag_tanwin         =  False
        self.tag_jar             =  False        
        # calculated  attributes 
        self.tag_verb         =  self._is_verb()
        if self.tag_verb:
            self.tag3rdperson      =  self._is3rdperson()            
            self.tag_majzoum      =  self._is_majzoum()
            self.tag_passive         =  self._is_passive()
            self.tag_past         =  self._is_past()
            self.tag_present         =  self._is_present()
        else:

            self.tag_noun         =  self._is_noun()
            if self.tag_noun:
                self.tag_defined  =  self._is_defined()
                self.tag_majrour     =  self._is_majrour()
                self.tag_tanwin     =  self._is_tanwin()                
                self.tag_jar         =  self._has_jar()
                
            else:
                self.tag_stopword     =  self._is_stopword()
        self.tag_added          =  self._is_added()
        self.tag_mansoub         =  self._is_mansoub()
        self.tag_marfou3         =  self._is_marfou3()

        self.tag_feminin         =  self._is_feminin()        
        self.tag_plural         =  self._is_plural()

        self.tag_masculin_plural     =  self._is_masculin_plural()
        self.tag_feminin_plural     =  self._is_feminin_plural()
        self.tag_dual             =  self._is_dual()
        self.tag_break = self._is_break()

    #  tags extracted from word dictionary 
    #--------------------------
    def _is_noun(self):
        """
        Return True if the word is a noun.
        @return: is a noun.
        @rtype: True/False
        """            
        return u'Noun' in self.get_type()

    def _is_stopword(self):
        """
        Return True if the word is a stop word.
        @return: is a noun.
        @rtype: True/False
        """            
        return u'STOPWORD' in self.get_type()

    def _is_verb(self):
        """
        Return True if the word is a verb.
        @return: is a verb.
        @rtype: True/False
        """            
        return  u'Verb' in self.get_type()


    def _is_majrour(self):
        """
        Return True if the word has the state majrour.
        @return: has the state majrour.
        @rtype: True/False
        """                
        return  u'مجرور' in self.get_tags()


    #  tags extracted from affixes 
    #--------------------------
    def get_type(self, ):
        """
        Get the type form of the input word
        @return: the given type.
        @rtype: unicode string
        """
        return self.type
        
    def set_type(self, newtype):
        """
        Set the type word
        @param newtype: the new given type.
        @type newtype: unicode string
        """
        self.type  =  newtype    
    def get_procletic(self, ):
        """
        Get the procletic 
        @return: the given procletic.
        @rtype: unicode string
        """
        return self.procletic
    def set_procletic(self, newprocletic):
        """
        Set the procletic 
        @param newprocletic: the new given procletic.
        @type newprocletic: unicode string
        """
        self.procletic  =  newprocletic
    def has_procletic(self, ):
        """
        return True if has procletic 
        @return: True if procletic not empty.
        @rtype: Boolean
        """
        return self.procletic != u''    
    def get_prefix(self, ):
        """
        Get the prefix 
        @return: the given prefix.
        @rtype: unicode string
        """
        return self.prefix
    def set_prefix(self, newprefix):
        """
        Set the prefix 
        @param newprefix: the new given prefix.
        @type newprefix: unicode string
        """
        self.prefix  =  newprefix


    def get_suffix(self, ):
        """
        Get the suffix 
        @return: the given suffix.
        @rtype: unicode string
        """
        return self.suffix
    def set_suffix(self, newsuffix):
        """
        Set the suffix word
        @param newsuffix: the given suffix.
        @type newsuffix: unicode string
        """
        self.suffix  =  newsuffix
    def get_encletic(self, ):
        """
        Get the encletic 
        @return: the given encletic.
        @rtype: unicode string
        """
        return self.encletic
    def set_encletic(self, newencletic):
        """
        Set the encletic 
        @param newencletic: the given encletic.
        @type newencletic: unicode string
        """
        self.encletic  =  newencletic            
        
    def has_encletic(self, ):
        """
        return True if has encletic 
        @return: True if encletic not empty.
        @rtype: Boolean
        """
        return self.encletic != u''

    def _is_majzoum(self):
        """
        Return True if the word has the state majrour.
        @return: has the state majrour.
        @rtype: True/False
        """        
        return  u'مجزوم'in self.get_tags()

    def _is_mansoub(self):
        """
        Return True if the word has the state mansoub.
        @return: has the state mansoub.
        @rtype: True/False
        """            
        return u'منصوب'in self.get_tags()

    def _is_marfou3(self):
        """
        Return True if the word has the state marfou3.
        @return: has the state marfou3.
        @rtype: True/False
        """        
        if u'مرفوع'in self.get_tags():
            return True
        return u'مضارع' in self.get_tags() and not self._is_mansoub() \
        and not self._is_majzoum()

    def _is_defined(self):
        """
        Return True if the word has the state definde.
        @return: has the state defined.
        @rtype: True/False
        """        
        return  u'تعريف'in self.get_tags()


    def _is_past(self):
        """
        Return True if the word has the tense past.
        @return: has the  tense past.
        @rtype: True/False
        """        
        return  u'ماضي'in self.get_tags()


    def _is_passive(self):
        """
        Return True if the word has the tense passive.
        @return: has the  tense passive.
        @rtype: True/False
        """    
        return  u'مجهول'in self.get_tags()

    def _is_present(self):
        """
        Return True if the word has the tense present.
        @return: has the  tense present.
        @rtype: True/False
        """    
        return u'مضارع' in self.get_tags()


    def _is3rdperson(self):
        """
        Return True if the word has the 3rd person.
        @return: has the 3rd persontense.
        @rtype: True/False
        """    
        return (u':هي:' in self.get_tags() or u':هو:' in self.get_tags()) \
        and not u'مفعول به' in self.get_tags()



    def _is_tanwin(self):
        """
        Return True if the word has tanwin.
        @return: has tanwin.
        @rtype: True/False
        """        
        return  u'تنوين'in self.get_tags()
    def _is_masculin_plural(self):
        """
        Return True if the word is  Masculin plural.
        @return: is masculin plural.
        @rtype: True/False
        """
        return  u'جمع مذكر سالم' in self.get_tags()
            
    def _is_feminin_plural(self):
        """
        Return True if the word is  Feminin plural.
        @return: is Feminin plural.
        @rtype: True/False
        """
        return u'جمع مؤنث سالم' in self.get_tags()

    def _is_dual(self):
        """
        Return True if the word is  dual.
        @return: is  dual.
        @rtype: True/False
        """
        return u'مثنى' in self.get_tags()

    def _has_jar(self):
        """
        Return True if the word has a jar factor attached.
        @return: has jar.
        @rtype: True/False
        """        
        return  u'جر:'in self.get_tags()

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
        if self.has_procletic() and self.has_jar():
            return True
        elif u'عطف' in self.get_tags() or araby.WAW in self.get_procletic() \
        or araby.FEH in self.get_procletic():
            return True
        return False

    # Mixed affix and dictionary attrrubutes
    #---------------------------------------
    def _is_added(self):
        """
        Return True if the word has the state added مضاف.
        @return: has the state added.
        @rtype: True/False
        """        
        return  u'مضاف' in self.get_tags() or u'اسم إضافة' in self.get_tags()

    def _is_masculin(self):
        """
        Return True if the word is masculin.
        @return: is masculin.
        @rtype: True/False
        """
        return  not self._is_feminin()

    def _is_feminin(self):
        """
        Return True if the word is Feminin.
        @return: is Feminin.
        @rtype: True/False
        """
        #يتحدد المؤنث 
        # بزيادة التاء المربوطة
        # جمع مؤنث سالم
        # ما كات اصله تاء مربوطة
        # للعمل TODO
        # دالة حاصة للكلمات المؤنثة
        if u'مؤنث' in self.get_tags():
            return True
        return  u'جمع مؤنث سالم' in self.get_tags()

    def _is_plural(self):
        """
        Return True if the word is a plural.
        @return: is plural.
        @rtype: True/False
        """
        return  u'جمع' in self.get_tags()


    def get_tags(self, ):
        """
        Get the tags form of the input word
        @return: the given tags.
        @rtype: unicode string
        """
        return self.tags
        
    def set_tags(self, newtags):
        """
        Set the tags word
        @param newtags: the new given tags.
        @type newtags: unicode string
        """
        self.tags  =  newtags

    ######################################################################
    #{ Tags  Functions
    ######################################################################

    def is_noun(self):
        """
        Return True if the word is a noun.
        @return: is a noun.
        @rtype: True/False
        """            
        return self.tag_noun

    def is_stopword(self):
        """
        Return True if the word is a stop word.
        @return: is a noun.
        @rtype: True/False
        """            
        return self.tag_stopword
    def is_verb(self):
        """
        Return True if the word is a verb.
        @return: is a verb.
        @rtype: True/False
        """            
        return self.tag_verb

    def is_majrour(self):
        """
        Return True if the word has the state majrour.
        @return: has the state majrour.
        @rtype: True/False
        """                
        return self.tag_majrour


    def is_majzoum(self):
        """
        Return True if the word has the state majrour.
        @return: has the state majrour.
        @rtype: True/False
        """        
        return self.tag_majzoum


    def is_mansoub(self):
        """
        Return True if the word has the state mansoub.
        @return: has the state mansoub.
        @rtype: True/False
        """            
        return self.tag_mansoub

    def is_marfou3(self):
        """
        Return True if the word has the state marfou3.
        @return: has the state marfou3.
        @rtype: True/False
        """        
        return self.tag_marfou3


    def is_defined(self):
        """
        Return True if the word has the state definde.
        @return: has the state defined.
        @rtype: True/False
        """        
        return self.tag_defined


    def is_past(self):
        """
        Return True if the word has the tense past.
        @return: has the  tense past.
        @rtype: True/False
        """        
        return self.tag_past


    def is_passive(self):
        """
        Return True if the word has the tense passive.
        @return: has the  tense passive.
        @rtype: True/False
        """    
        return self.tag_passive


    def is_present(self):
        """
        Return True if the word has the tense present.
        @return: has the  tense present.
        @rtype: True/False
        """    
        return self.tag_present

    def is3rdperson(self):
        """
        Return True if the word has the 3rd person.
        @return: has the 3rd persontense.
        @rtype: True/False
        """    
        return self.tag3rdperson

    def is_added(self):
        """
        Return True if the word has the state added مضاف.
        @return: has the state added.
        @rtype: True/False
        """        
        return self.tag_added


    def is_tanwin(self):
        """
        Return True if the word has tanwin.
        @return: has tanwin.
        @rtype: True/False
        """        
        return self.tag_tanwin
    def has_jar(self):
        """
        Return True if the word has tanwin.
        @return: has tanwin.
        @rtype: True/False
        """        
        return self.tag_jar

    def is_break(self):
        """
        Return True if the word has break.
        @return: is break.
        @rtype: True/False
        """    
        #تكون الكلمة فاصلة إذا كانت منفصلة عمّا قبلها.    
        # الحالات التي تقطع
        # - حرف جر متصل
        # فاصلة أو نقطة
        return self.tag_break
    def is_masculin_plural(self):
        """
        Return True if the word is  Masculin plural.
        @return: is masculin plural.
        @rtype: True/False
        """
        return self.tag_masculin_plural

            
    def is_feminin_plural(self):
        """
        Return True if the word is  Feminin plural.
        @return: is Feminin plural.
        @rtype: True/False
        """
        return self.tag_feminin_plural


    def is_feminin(self):
        """
        Return True if the word is Feminin.
        @return: is Feminin.
        @rtype: True/False
        """
        return self.tag_feminin        
    def is_plural(self):
        """
        Return True if the word is a plural.
        @return: is plural.
        @rtype: True/False
        """
        return self.tag_plural


    def is_dual(self):
        """
        Return True if the word is  dual.
        @return: is  dual.
        @rtype: True/False
        """
        return self.tag_dual


    ######################################################################
    #{ Display Functions
    ######################################################################
    def get_dict(self, ):
        """
        get attributes dict
        """
        return  self.__dict__
    def __repr__(self):
        """
        Display objects result from analysis
        @return: text
        @rtype : text
        """    
        text = u"{"
        stmword  =  self.__dict__
        for key in stmword.keys():
            text +=  u"\n\t\tu'%s'  =  u'%s', " % (key, stmword[key])
        text +=  u'\n\t\t}'
        return text.encode('utf8')

if __name__ == "__main__":
    print "test"
    RDICT  =  {"word": "الحياة", # input word
            "vocalized": "الْحَيَاةُ", # vocalized form of the input word 
            "procletic": "ال", # the syntaxic pprefix called procletic
            "prefix": "", # the conjugation or inflection prefix
            "stem": "حياة", # the word stem
            "suffix": "ُ", # the conjugation suffix of the word
            "encletic": "", # the syntaxic suffix
            
            "tags": "تعريف::مرفوع*", 
            # tags of affixes and tags extracted form lexical dictionary
            "freq": 0, # the word frequency from Word Frequency database 
            "root": "", # the word root not yet used
            "template": "", # the template وزن 
            "type": "Noun:مصدر", # the word type
            "original": "حَيَاةٌ", #original word from lexical dictionary
            "syntax":"", # used for syntaxique analysis porpos
            u'semantic':'', 
            }


    
    #~print stmwrd
