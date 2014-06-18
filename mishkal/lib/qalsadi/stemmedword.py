#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        stemmed_word
# Purpose:     representat data analyzed given by morphoanalyzer Qalsadi
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     19-09-2012
# Copyright:   (c) Taha Zerrouki 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
stemmed_word represents the data resulted from the morpholocigal analysis
"""
import pyarabic.araby as araby
import qalsadi.stemmedaffix as stemmedaffix
GLOBAL_AFFIXES = {}                

class  StemmedWord:
    """
    stemmed_word represents the data resulted from the morpholocigal analysis
    """
    def __init__(self, resultdict = None):
        # given word attributes
        self.word =  u"", 
        #~"""input word"""
        self.vocalized =  u"", 
        #~"""vocalized form of the input word """
        self.unvocalized = u""
     
        self.tags =  u"", 
        #~"""tags of affixes and tags extracted form lexical dictionary"""
        self.affix_key  = u'-'
        affix_tags      = u""     
        #~"""tags of affixes"""

        # stemmed word attributes
        self.stem =  u"", 
        #~"""the word stem"""

        # _original word attributes from dictionary.
        self.original_tags =  u"", 
        #~""" tags extracted form lexical dictionary"""
        self.freq =  0, # the word frequency from _word _frequency database 
        self.type =  u"", # the word type
        self.original =  u""            #original word from lexical dictionary
        if resultdict:

            self.word    = resultdict.get('word', u'')
            self.vocalized    = resultdict.get('vocalized', u'')
            self.semivocalized    = resultdict.get('semivocalized', u'')
            self.stem    = resultdict.get('stem', u'')
            self.affix  = u'-'.join(resultdict.get('affix', []))

            affix_tags = resultdict.get('tags', u'')
            self.tags    = u':'.join([resultdict.get('tags', u''),
             resultdict.get('originaltags', u'')])            
            self.freq     = resultdict.get('freq', u'')
            self.type    = resultdict.get('type', u'')
            self.original    = resultdict.get('original', u'')

        # calculated  attributes 
        self.tag_stopword    = self._is_stopword()
        self.tag_verb        = False
        self.tag_noun        = False        
        if not self.tag_stopword:
            self.tag_verb    = self._is_verb()
            if not self.tag_verb:
                self.tag_noun    = self._is_noun()

        self.affix_key = self.affix
        if self.tag_verb :
            # #if the word is verb: we must add the tense and pronoun 
            # to the affixkay.
            # #because for verbs, same affixes don't give same tags
            self.affix_key = u'|'.join([self.affix_key, affix_tags])
            
        if not GLOBAL_AFFIXES.has_key(self.affix_key):
            GLOBAL_AFFIXES[self.affix_key] = stemmedaffix.StemmedAffix(
             resultdict)
        # init
        self.tag_added          = False
        self.tag_initial      = False
        self.tag_masdar         = False
        self.tag_proper_noun     = False
        self.tag_adj              = False
        self.tag_pounct         = False
        self.tag_transparent     = False
        self.tag_masculin     = False
        self.tag_feminin         = False
        self.tag_plural         = False
        self.tag_broken_plural = False
        self.tag_mamnou3         = False
        self.tag_single         = False
        self.tag_break         = False
        
        if self.tag_noun:
            self.tag_added         = self._is_added()
            self.tag_adj            = self.tag_noun and self._is_adj()
            self.tag_masdar        = self.tag_noun and self._is_masdar()
            self.tag_proper_noun    = self.tag_noun and self._is_proper_noun()
            self.tag_broken_plural =  self._is_broken_plural()            
            self.tag_mamnou3        = self._is_mamnou3()        
        elif self.tag_stopword:
            self.tag_transparent    = self._is_transparent()
        else:
            self.tag_pounct        = self._is_pounct()
        self.tag_initial     = self._is_initial()

        self.tag_feminin        = self._is_feminin()
        self.tag_plural        = self.tag_broken_plural or self._is_plural()
        #redandente
        self.tag_break        = self._is_break()
        
    #  tags extracted from word dictionary 
    #--------------------------
    def _is_initial(self):
        """
        Return True if the word mark the begin of next sentence.
        @return: direct initial.
        @rtype: True/False
        """
        word = self.get_word()
        return word == u"" or  word[0] in (u'.', u'?', u'', u':')

    def _is_noun(self):
        """
        Return True if the word is a noun.
        @return: is a noun.
        @rtype: True/False
        """            
        return u'Noun' in self.get_type()  or  u'اسم' in self.get_tags()

    def _is_adj(self):
        """
        Return True if the word is a Adjective.
        @return: is a Adjective.
        @rtype: True/False
        """
        wordtype = self.get_type()
        return u'صفة' in wordtype or u'اسم مفعول' in wordtype or \
        u'اسم فاعل' in wordtype or u'صيغة مبالغة' in wordtype \
        or u'منسوب' in wordtype
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

    def _is_masdar(self):
        """
        Return True if the word is a masdar.
        @return: is a masdar.
        @rtype: True/False
        """            
        return u'مصدر' in self.get_type()

    def _is_proper_noun(self):
        """
        Return True if the word is a proper noun.
        @return: is a proper noun.
        @rtype: True/False
        """            
        return u'noun_prop' in self.get_type()

    def _is_pounct(self):
        """
        Return True if the word is a pounctuation.
        @return: is a verb.
        @rtype: True/False
        """            
        return  u'POUNCT' in self.get_type()


    def _is_transparent(self):
        """
        Return True if the word has the state transparent, which can trasnpose the effect of the previous factor.
        @return: has the state transparent.
        @rtype: True/False
        """
        #temporary, 
        # the transparent word are stopwords like هذا وذلك
        # the stopword tags have اسم إشارة, 
        # a pounctuation can has the transparent tag like quotes.,
        # which havent any gramatical effect.
        # Todo 
        # حالة بذلك الرجل
        return  u'شفاف' in self.get_tags() or u'إشارة'in self.get_tags()


    def _is_broken_plural(self):
        """
        Return True if the word is broken  plural.
        @return: is broken plural.
        @rtype: True/False
        """
        return  u'جمع تكسير' in self.get_tags()

    def _is_mamnou3(self):
        """
        Return True if the word is forbiden from Sarf ممنوع من الصرف.
        @return: is mamnou3 min sarf.
        @rtype: True/False
        """
        return  u'ممنوع من الصرف' in self.get_tags()

    def get_procletic(self, ):
        """
        Get the procletic 
        @return: the given procletic.
        @rtype: unicode string
        """
        # return self.procletic
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].get_procletic()
        return u""            

    def has_procletic(self, ):
        """
        return True if has procletic 
        @return: True if procletic not empty.
        @rtype: Boolean
        """
        # return self.procletic! = u''
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].has_procletic()
        return False    
    def get_prefix(self, ):
        """
        Get the prefix 
        @return: the given prefix.
        @rtype: unicode string
        """
        # return self.prefix
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].get_prefix()
        return u""            
    # def set_prefix(self, newprefix):
        # """
        # Set the prefix 
        # @param newprefix: the new given prefix.
        # @type newprefix: unicode string
        # """
        # self.prefix = newprefix


    def get_suffix(self, ):
        """
        Get the suffix 
        @return: the given suffix.
        @rtype: unicode string
        """
        # return self.suffix
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].get_suffix()
        return u""            
    def get_encletic(self, ):
        """
        Get the encletic 
        @return: the given encletic.
        @rtype: unicode string
        """
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].get_encletic()
        return u""        
        
    def has_encletic(self, ):
        """
        return True if has encletic 
        @return: True if encletic not empty.
        @rtype: Boolean
        """
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].has_encletic()
        return False            


    # Mixed affix and dictionary attrrubutes
    #---------------------------------------
    def _affix_is_added(self):
        """
        Return True if the word has the state added مضاف.
        @return: has the state added.
        @rtype: True/False
        """        
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_added()
        return False    
    def _is_added(self):
        """
        Return True if the word has the state added مضاف.
        @return: has the state added.
        @rtype: True/False
        """        
        return  self._affix_is_added() or u'اسم إضافة' in self.get_tags()


    def _affix_is_feminin(self):
        """
        Return True if the word is Feminin.
        @return: is Feminin.
        @rtype: True/False
        """        
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_feminin()
        return False    
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
        if self._affix_is_feminin():
            return True
        return  araby.TEH_MARBUTA in self.get_original()  

    def _affix_is_plural(self):
        """
        Return True if the word is a plural.
        @return: is Feminin.
        @rtype: True/False
        """        
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_plural()
        return False    
    def _is_plural(self):
        """
        Return True if the word is a plural.
        @return: is plural.
        @rtype: True/False
        """
        return self._affix_is_plural() or self._is_broken_plural()

    def _is_single(self):
        """
        Return True if the word is single.
        @return: is  dual.
        @rtype: True/False
        """
        # return not self._is_plural() and not self._is_dual()
        return not self.is_plural() and not self.is_dual()

    def _is_break(self):
        """
        Return True if the word has break.

        @return: is break.
        @rtype: True/False
        """    
        #تكون الكلمة فاصلة إذا كانت منفصلة عمّا قبلها.    
        # الحالات التي تقطع
        # - حرف جر متصل
        # فاصلة أو نقطة
        # if self.isDirectJar():
            # return True
        # el
        # if self.has_procletic() and self.has_jar():
        return self.is_stopword() \
            or (self.is_pounct() and 'break' in self.get_tags())\
            or (self.has_procletic() and self.has_jar())
            # or (self.is_pounct() and 'break' in self.get_tags())        

    ######################################################################
    #{ Attribut Functions
    ######################################################################
    def get_word(self, ):
        """
        Get the input word given by user
        @return: the given word.
        @rtype: unicode string
        """
        return self.word
    def set_word(self, newword):
        """
        Set the input word given by user
        @param newword: the new given word.
        @type newword: unicode string
        """
        self.word = newword
        
    def get_vocalized(self, ):
        """
        Get the vocalized form of the input word
        @return: the given vocalized.
        @rtype: unicode string
        """
        return self.vocalized
        
    def set_vocalized(self, newvocalized):
        """
        Set the vocalized word
        @param newvocalized: the new given vocalized.
        @type newvocalized: unicode string
        """
        self.vocalized = newvocalized
        self.unvocalized = araby.strip_tashkeel(newvocalized)
    def get_stem(self, ):
        """
        Get the stem form of the input word
        @return: the given stem.
        @rtype: unicode string
        """
        return self.stem
        
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
        self.tags = newtags
    def get_affix_tags(self, ):
        """
        Get the affix tags form of the input word
        @return: the given tags.
        @rtype: unicode string
        """
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].get_tags()
        return u""
    def get_affix(self, ):
        """
        Get the affix  form of the input word
        @return: the given affix.
        @rtype: unicode string
        """
        return self.affix
        # return u""
        # return self.affix_tags


    def get_freq(self, ):
        """
        Get the freq form of the input word
        @return: the given freq.
        @rtype: unicode string
        """
        return self.freq
        
    def set_freq(self, newfreq):
        """
        Set the freq word
        @param newfreq: the new given freq.
        @type newfreq: unicode string
        """
        self.freq = newfreq
       

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
        self.type = newtype
       
    def get_original(self, ):
        """
        Get the original form of the input word
        @return: the given original.
        @rtype: unicode string
        """
        return self.original
        
    # def getUnv_original(self, ):
        # """
        # Get the unvocalized  original form of the input word
        # @return: the given unvocalized original.
        # @rtype: unicode string
        # """
        # if self.unvoriginal:
            # return self.unvoriginal            
        # else :
            # if self.original:
                # self.unvoriginal = araby.strip_tashkeel(self.original)
            # else:
                # return u""
 
    def set_original(self, neworiginal):
        """
        Set the original word
        @param neworiginal: the new given original.
        @type neworiginal: unicode string
        """
        self.original = neworiginal

    ######################################################################
    #{ _tags  Functions
    ###################################################################### 
    def is_initial(self):
        """
        Return True if the word mark the begin of next sentence.
        @return: direct initial.
        @rtype: True/False
        """
        return self.tag_initial

    #  حالة المضاف إليه        
    #--------------------------
    def is_unknown(self):
        """
        Return True if the word is unknown.
        @return: is a noun.
        @rtype: True/False
        """            
        return (u'unknown' in self.get_type())
    def is_noun(self):
        """
        Return True if the word is a noun.
        @return: is a noun.
        @rtype: True/False
        """            
        return self.tag_noun


    def is_adj(self):
        """
        Return True if the word is an adjective.
        @return: is a adjective.
        @rtype: True/False
        """            
        return self.tag_adj
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

    def is_masdar(self):
        """
        Return True if the word is a masdar.
        @return: is a masdar.
        @rtype: True/False
        """            
        return self.tag_masdar
    def is_proper_noun(self):
        """
        Return True if the word is a proper noun.
        @return: is a propoer noun.
        @rtype: True/False
        """            
        return self.tag_proper_noun

    def is_pounct(self):
        """
        Return True if the word is a pounctuation.
        @return: is a verb.
        @rtype: True/False
        """            
        return self.tag_pounct


    def is_transparent(self):
        """
        Return True if the word has the state transparent, which can trasnpose the effect of the previous factor.
        @return: has the state transparent.
        @rtype: True/False
        """
        #temporary, 
        # the transparent word are stopwords like هذا وذلك
        # the stopword tags have اسم إشارة, 
        # a pounctuation can has the transparent tag like quotes.,
        # which havent any gramatical effect.
        # Todo 
        # حالة بذلك الرجل
        return self.tag_transparent

        #----------------------------
        # affixes boolean attributes
        #----------------------------

    def is_majrour(self):
        """
        Return True if the word has the state majrour.
        @return: has the state majrour.
        @rtype: True/False
        """
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_majrour()
        return False


    def is_majzoum(self):
        """
        Return True if the word has the state majrour.
        @return: has the state majrour.
        @rtype: True/False
        """
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_majzoum()
        return False


    def is_mansoub(self):
        """
        Return True if the word has the state mansoub.
        @return: has the state mansoub.
        @rtype: True/False
        """
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_mansoub()
        return False


    def is_marfou3(self):
        """
        Return True if the word has the state marfou3.
        @return: has the state marfou3.
        @rtype: True/False
        """
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_marfou3()
        return False



    def is_defined(self):
        """
        Return True if the word has the state definde.
        @return: has the state defined.
        @rtype: True/False
        """
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_defined()
        return False


    def is_past(self):
        """
        Return True if the word has the tense past.
        @return: has the  tense past.
        @rtype: True/False
        """
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_past()
        return False



    def is_passive(self):
        """
        Return True if the word has the tense passive.
        @return: has the  tense passive.
        @rtype: True/False
        """    
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_passive()
        return False


    def is_present(self):
        """
        Return True if the word has the tense present.
        @return: has the  tense present.
        @rtype: True/False
        """    
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_present()
        return False

    def is3rdperson(self):
        """
        Return True if the word has the 3rd person.
        @return: has the 3rd persontense.
        @rtype: True/False
        """
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is3rdperson()
        return False        




    def is_tanwin(self):
        """
        Return True if the word has tanwin.
        @return: has tanwin.
        @rtype: True/False
        """        
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_tanwin()
        return False
    def has_jar(self):
        """
        Return True if the word has tanwin.
        @return: has tanwin.
        @rtype: True/False
        """        
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].has_jar()
        return False

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
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_masculin_plural()
        return False
    def is_dual(self):
        """
        Return True if the word is  dual.
        @return: is  dual.
        @rtype: True/False
        """
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_dual()
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
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_break()
        return False             
            
    def is_feminin_plural(self):
        """
        Return True if the word is  Feminin plural.
        @return: is Feminin plural.
        @rtype: True/False
        """
        if GLOBAL_AFFIXES.has_key(self.affix_key):
            return GLOBAL_AFFIXES[self.affix_key].is_feminin_plural()
        return False



    #-----------------------------
    # Mixed extraction attributes tests
    #-----------------------------

    def is_masculin(self):
        """
        Return True if the word is masculin.
        @return: is masculin.
        @rtype: True/False
        """
        return not self.tag_feminin

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

    def is_broken_plural(self):
        """
        Return True if the word is broken  plural.
        @return: is broken plural.
        @rtype: True/False
        """
        return self.tag_broken_plural
    def is_mamnou3(self):
        """
        Return True if the word is Mamnou3 min Sarf.
        @return: is Mamnou3 min Sarf.
        @rtype: True/False
        """
        return self.tag_mamnou3

    def is_single(self):
        """
        Return True if the word is single.
        @return: is  dual.
        @rtype: True/False
        """
        return not self.is_plural() and not self.is_dual()

    def is_added(self):
        """
        Return True if the word has the state added مضاف.
        @return: has the state added.
        @rtype: True/False
        """        
        return self.tag_added

    ######################################################################
    #{ Display Functions
    ######################################################################
    def get_dict(self, ):
        """
        getdictionary function
        """
        return  self.__dict__
    def __repr__(self):
        """
        Display objects result from analysis
        @return: text
        @rtype : text
        """    
        text = u"{"
        stmword = self.__dict__
        stmword['affix'] = 'Taha'
        for key in stmword.keys():
            text +=  u"\n\t\tu'%s' = u'%s', " % (key, stmword[key])
        text +=  u'\n\t\t}'
        return text.encode('utf8')

if __name__ == "__main__":
    print "test"

    RDICT = {"word": "الحياة", # input word
            "vocalized": "الْحَيَاةُ", # vocalized form of the input word 
            "procletic": "ال", # the syntaxic pprefix called procletic
            "prefix": "", # the conjugation or inflection prefix
            "stem": "حياة", # the word stem
            "suffix": "ُ", # the conjugation suffix of the word
            "encletic": "", # the syntaxic suffix
            
            "tags": "تعريف::مرفوع*", 
            # tags of affixes and tags extracted form lexical dictionary
            "freq": 0, # the word frequency from _word _frequency database 
            "root": "", # the word root not yet used
            "template": "", # the template وزن 
            "type": "Noun:مصدر", # the word type
            "original": "حَيَاةٌ", #original word from lexical dictionary
            "syntax":"", # used for syntaxique analysis porpos
            u'semantic':'', 
            }
    stmwrd = StemmedWord(RDICT)
    print stmwrd.get_dict()
    
    stmwrd.set_word("4444")
    stmwrd.set_vocalized("4444")
    stmwrd.set_tags("4444")
    stmwrd.set_freq("4444")
    stmwrd.set_type("4444")
    stmwrd.set_original("4444")
   
    print stmwrd
    
