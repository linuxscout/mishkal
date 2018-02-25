#!/usr/bin/python
# -*- coding = utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        dictWord
# Purpose:     representat data analyzed given by morphoanalyzer Qalsadi
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     19-09-2012
# Copyright:   (c) Taha Zerrouki 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

import pyarabic.araby as araby

class dictWord:
    """
    dictWord represents the data got from the lexicon dictionary
    """
    def __init__(self, resultDict=None):
        # given word attributes
        self.word =  u"",       
        """input word"""
        self.vocalized =  u"",  
        """vocalized form of the input word """
        
        self.tags =  u"", 
        """tags of affixes and tags extracted form lexical dictionary"""

        # Original word attributes from dictionary.
        self.originalTags =  u"",
        """ tags extracted form lexical dictionary"""
        self.freq =  0,             # the word frequency from Word Frequency database 
        self.type =  u"",               # the word type
        self.original =  u""            #original word from lexical dictionary

        if resultDict:

            self.word   = resultDict.get('word',u'');
            self.vocalized  = resultDict.get('vocalized',u'');
            self.freq   = resultDict.get('freq',u'');
            self.type   = resultDict.get('type',u'');
            self.original   = resultDict.get('original',u'');

        # calculated  attributes 
        self.tagStopWord    = self._isStopWord();
        self.tagVerb        = False;
        self.tagNoun        = False;        
        if not self.tagStopWord:
            self.tagVerb    = self._isVerb();
            if not self.tagVerb:
                self.tagNoun    = self._isNoun();

        # init
        self.tagAdded        = False
        self.tagInitial      = False
        self.tagMasdar       = False
        self.tagProperNoun   = False
        self.tagAdj          = False
        self.tagPounct       = False
        self.tagTransparent  = False
        self.tagMasculin     = False
        self.tagFeminin      = False
        self.tagPlural       = False
        self.tagBrokenPlural = False
        self.tagMamnou3      = False
        self.tagSingle       = False
        self.tagBreak        = False
        
        if self.tagNoun:
            self.tagAdded       = self._isAdded();
            self.tagAdj         = self.tagNoun and self._isAdj();
            self.tagMasdar      = self.tagNoun and self._isMasdar();
            self.tagProperNoun  = self.tagNoun and self._isProperNoun();
            self.tagBrokenPlural= self._isBrokenPlural();           
            self.tagMamnou3     = self._isMamnou3();        
        elif self.tagStopWord:
            self.tagTransparent = self._isTransparent();
        else:
            self.tagPounct      = self._isPounct();
        self.tagInitial     = self._isInitial();

        self.tagFeminin     = self._isFeminin();
        # self.tagMasculin  = not self.tagFeminin #self._isMasculin();      
        self.tagPlural      = self.tagBrokenPlural or self._isPlural();
        # self.tagSingle        = not self.tagPlural or self._isSingle();   #redandente
        self.tagBreak       = self._isBreak();
        
    #  tags extracted from word dictionary 
    #--------------------------
    def _isInitial(self):
        """
        Return True if the word mark the begin of next sentence.
        @return: direct initial.
        @rtype: True/False;
        """
        word=self.getWord();
        return word==u"" or  word[0] in (u'.',u'?', u';', u':');

    def _isNoun(self):
        """
        Return True if the word is a noun.
        @return: is a noun.
        @rtype: True/False;
        """         
        return u'Noun' in self.getType()  or  u'اسم' in self.getTags();

    def _isAdj(self):
        """
        Return True if the word is a Adjective.
        @return: is a Adjective.
        @rtype: True/False;
        """
        type=self.getType();
        return u'صفة' in type or u'اسم مفعول' in type or u'اسم فاعل' in type or u'صيغة مبالغة' in type or u'منسوب' in type;
    def _isStopWord(self):
        """
        Return True if the word is a stop word.
        @return: is a noun.
        @rtype: True/False;
        """         
        return u'STOPWORD' in self.getType();

    def _isVerb(self):
        """
        Return True if the word is a verb.
        @return: is a verb.
        @rtype: True/False;
        """         
        return  u'Verb' in self.getType();

    def _isMasdar(self):
        """
        Return True if the word is a masdar.
        @return: is a masdar.
        @rtype: True/False;
        """         
        return u'مصدر' in self.getType();

    def _isProperNoun(self):
        """
        Return True if the word is a proper noun.
        @return: is a proper noun.
        @rtype: True/False;
        """         
        return u'noun_prop' in self.getType();



    def _isTransparent(self):
        """
        Return True if the word has the state transparent, which can trasnpose the effect of the previous factor.
        @return: has the state transparent.
        @rtype: True/False;
        """
        #temporary, 
        # the transparent word are stopwords like هذا وذلك
        # the stopword tags have اسم إشارة,
        # a pounctuation can has the transparent tag like quotes., which havent any gramatical effect.
        # Todo 
        # حالة بذلك الرجل
        return  u'شفاف' in self.getTags() or u'إشارة'in self.getTags();

    def _isBrokenPlural(self):
        """
        Return True if the word is broken  plural.
        @return: is broken plural.
        @rtype: True/False;
        """
        return  u'جمع تكسير' in self.getTags();

    def _isMamnou3(self):
        """
        Return True if the word is forbiden from Sarf ممنوع من الصرف.
        @return: is mamnou3 min sarf.
        @rtype: True/False;
        """
        return  u'ممنوع من الصرف' in self.getTags();

    def _isPlural(self):
        """
        Return True if the word is a plural.
        @return: is plural.
        @rtype: True/False;
        """
        return self._isBrokenPlural();

    def _isSingle(self):
        """
        Return True if the word is single.
        @return: is  dual.
        @rtype: True/False;
        """
        # return not self._isPlural() and not self._isDual();
        return not self.isPlural() and not self.isDual();

    def _isPounct(self):
        """
        Return True if the word is a pounctuation.
        @return: is a verb.
        @rtype: True/False;
        """         
        return  u'POUNCT' in self.getType();        
    def _isBreak(self):
        """
        Return True if the word has break.

        @return: is break.
        @rtype: True/False;
        """ 
        #تكون الكلمة فاصلة إذا كانت منفصلة عمّا قبلها.  
        # الحالات التي تقطع
        # - حرف جر متصل
        # فاصلة أو نقطة
        # if self.isDirectJar():
            # return True;
        # el
        # if self.hasProcletic() and self.hasJar():
        return self.isStopWord() \
            or (self.isPounct() and 'break' in self.getTags()); 

    def _isFeminin(self):
        """
        Return True if the word is Feminin.
        @return: is Feminin.
        @rtype: True/False;
        """
        #يتحدد المؤنث 
        # بزيادة التاء المربوطة
        # جمع مؤنث سالم
        # ما كات اصله تاء مربوطة
        # للعمل TODO
        # دالة حاصة للكلمات المؤنثة
        # if self._affixIsFeminin():
            # return True;
        # elif self.getUnvOriginal() and self.getUnvOriginal().endswith(araby.TEH_MARBUTA):
        return  araby.TEH_MARBUTA in self.getOriginal() ; 

    ######################################################################
    #{ Attribut Functions
    ######################################################################
    def getWord(self,):
        """
        Get the input word given by user
        @return: the given word.
        @rtype: unicode string
        """
        return self.word;
    def setWord(self,newword):
        """
        Set the input word given by user
        @param newword: the new given word.
        @type newword: unicode string
        """
        self.word = newword;
        
    def getVocalized(self,):
        """
        Get the vocalized form of the input word
        @return: the given vocalized.
        @rtype: unicode string
        """
        return self.vocalized;
        
    def setVocalized(self,newvocalized):
        """
        Set the vocalized word
        @param newvocalized: the new given vocalized.
        @type newvocalized: unicode string
        """
        self.vocalized  =  newvocalized;
        self.unvocalized  =  araby.stripTashkeel(newvocalized);

        
    def getTags(self,):
        """
        Get the tags form of the input word
        @return: the given tags.
        @rtype: unicode string
        """
        return self.tags;
        
    def setTags(self,newtags):
        """
        Set the tags word
        @param newtags: the new given tags.
        @type newtags: unicode string
        """
        self.tags = newtags;

    def getFreq(self,):
        """
        Get the freq form of the input word
        @return: the given freq.
        @rtype: unicode string
        """
        return self.freq;
        
    def setFreq(self,newfreq):
        """
        Set the freq word
        @param newfreq: the new given freq.
        @type newfreq: unicode string
        """
        self.freq = newfreq;
    def getTemplate(self,):
        """
        Get the template form of the input word
        @return: the given template.
        @rtype: unicode string
        """
        return self.template;
        
    def setTemplate(self,newtemplate):
        """
        Set the template word
        @param newtemplate: the new given template.
        @type newtemplate: unicode string
        """
        self.template = newtemplate;
    def getType(self,):
        """
        Get the type form of the input word
        @return: the given type.
        @rtype: unicode string
        """
        return self.type;
        
    def setType(self,newtype):
        """
        Set the type word
        @param newtype: the new given type.
        @type newtype: unicode string
        """
        self.type = newtype;
    def getRoot(self,):
        """
        Get the root form of the input word
        @return: the given root.
        @rtype: unicode string
        """
        return self.root;
        
    def setRoot(self,newroot):
        """
        Set the root word
        @param newroot: the new given root.
        @type newroot: unicode string
        """
        self.root = newroot;
        
    def getOriginal(self,):
        """
        Get the original form of the input word
        @return: the given original.
        @rtype: unicode string
        """
        return self.original;
        
 
    def setOriginal(self,neworiginal):
        """
        Set the original word
        @param neworiginal: the new given original.
        @type neworiginal: unicode string
        """
        self.original = neworiginal;

    ######################################################################
    #{ Tags  Functions
    ######################################################################      
    def isInitial(self):
        """
        Return True if the word mark the begin of next sentence.
        @return: direct initial.
        @rtype: True/False;
        """
        return self.tagInitial;

    #  حالة المضاف إليه     
    #--------------------------
    def isUnknown(self):
        """
        Return True if the word is unknown.
        @return: is a noun.
        @rtype: True/False;
        """         
        return (u'unknown' in self.getType());
    def isNoun(self):
        """
        Return True if the word is a noun.
        @return: is a noun.
        @rtype: True/False;
        """         
        return self.tagNoun;


    def isAdj(self):
        """
        Return True if the word is an adjective.
        @return: is a adjective.
        @rtype: True/False;
        """         
        return self.tagAdj;
    def isStopWord(self):
        """
        Return True if the word is a stop word.
        @return: is a noun.
        @rtype: True/False;
        """         
        return self.tagStopWord;
    def isVerb(self):
        """
        Return True if the word is a verb.
        @return: is a verb.
        @rtype: True/False;
        """         
        return self.tagVerb;

    def isMasdar(self):
        """
        Return True if the word is a masdar.
        @return: is a masdar.
        @rtype: True/False;
        """         
        return self.tagMasdar;
    def isProperNoun(self):
        """
        Return True if the word is a proper noun.
        @return: is a propoer noun.
        @rtype: True/False;
        """         
        return self.tagProperNoun;

    def isPounct(self):
        """
        Return True if the word is a pounctuation.
        @return: is a verb.
        @rtype: True/False;
        """         
        return self.tagPounct;


    def isTransparent(self):
        """
        Return True if the word has the state transparent, which can trasnpose the effect of the previous factor.
        @return: has the state transparent.
        @rtype: True/False;
        """
        #temporary, 
        # the transparent word are stopwords like هذا وذلك
        # the stopword tags have اسم إشارة,
        # a pounctuation can has the transparent tag like quotes., which havent any gramatical effect.
        # Todo 
        # حالة بذلك الرجل
        return self.tagTransparent;



    #-----------------------------
    # Mixed extraction attributes tests
    #-----------------------------

    def isMasculin(self):
        """
        Return True if the word is masculin.
        @return: is masculin.
        @rtype: True/False;
        """
        return not self.tagFeminin;

    def isFeminin(self):
        """
        Return True if the word is Feminin.
        @return: is Feminin.
        @rtype: True/False;
        """
        return self.tagFeminin;

    def isPlural(self):
        """
        Return True if the word is a plural.
        @return: is plural.
        @rtype: True/False;
        """
        return self.tagPlural;

    def isBrokenPlural(self):
        """
        Return True if the word is broken  plural.
        @return: is broken plural.
        @rtype: True/False;
        """
        return self.tagBrokenPlural;
    def isMamnou3(self):
        """
        Return True if the word is Mamnou3 min Sarf.
        @return: is Mamnou3 min Sarf.
        @rtype: True/False;
        """
        return self.tagMamnou3;

    def isSingle(self):
        """
        Return True if the word is single.
        @return: is  dual.
        @rtype: True/False;
        """
        return not self.isPlural() and not self.isDual();

    def isAdded(self):
        """
        Return True if the word has the state added مضاف.
        @return: has the state added.
        @rtype: True/False;
        """     
        return self.tagAdded

    ######################################################################
    #{ Display Functions
    ######################################################################
    def getDict(self,):
        return  self.__dict__
    def __repr__(self):
        """
        Display objects result from analysis
        @return: text
        @rtype : text
        """ 
        text=u"{";
        stmword = self.__dict__;
        stmword['affix']='Taha';
        for key in stmword.keys():
                text+= u"\n\t\tu'%s' = u'%s',"%(key, stmword[key]);
        text+= u'\n\t\t}';
        return text.encode('utf8');

if __name__=="__main__":
    print "test";
    rdict={}
    rdict = {"word": "الحياة",      # input word
            "vocalized": "الْحَيَاةُ",   # vocalized form of the input word 
            "procletic": "ال",      # the syntaxic pprefix called procletic
            "prefix": "",           # the conjugation or inflection prefix
            "stem": "حياة",         # the word stem
            "suffix": "ُ",          # the conjugation suffix of the word
            "encletic": "",         # the syntaxic suffix
            
            "tags": "تعريف::مرفوع*", # tags of affixes and tags extracted form lexical dictionary
            "freq": 0,              # the word frequency from Word Frequency database 
            "root": "",             # the word root; not yet used
            "template": "",         # the template وزن 
            "type": "Noun:مصدر",    # the word type
            "original": "حَيَاةٌ",      #original word from lexical dictionary
            "syntax":"",                # used for syntaxique analysis porpos
            u'semantic':'',
            };
    stmwrd=stemmedWord(rdict);
    print stmwrd.getDict();
    
    stmwrd.setWord("4444");
    stmwrd.setVocalized("4444");
    stmwrd.setProcletic("4444");
    stmwrd.setPrefix("4444");
    stmwrd.setStem("4444");
    stmwrd.setSuffix("4444");
    stmwrd.setEncletic("4444");
    stmwrd.setTags("4444");
    stmwrd.setFreq("4444");
    stmwrd.setRoot("4444");
    stmwrd.setTemplate("4444");
    stmwrd.setType("4444");
    stmwrd.setOriginal("4444");
    # stmwrd.setSyntax("4444");
    # stmwrd.setSyntax("4444");
    
    print stmwrd;
    
