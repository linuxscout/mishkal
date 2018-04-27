#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        spellcheck
# Purpose:     Arabic automatic spellchecking.
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
import sys
sys.path.append('../lib');
sys.path.append('../');
import re
import pyarabic.araby as araby
import pyarabic.arabrepr as arabRepr
import spellcheck_const
import qalsadi.analex
import yaraspell.spelldict 
# to debug program
debug= True;
class SpellcheckClass:
    """
        Arabic Spellcheck Class
    """

    def __init__(self, cache_path=False):
        # to display internal messages for debugging
        debug=False;
        # limit of words to vocalize, default value is 1000 words.
        self.limit=1000
        #  set the option value to enable the Last mark on voaclize words in output
        # default value is True, can be disabled for debuging porpus
        self.enabledLastMark= True;
        # set the option to do statistical vocalization based on collocations
        # default value is True, can be disabled for debuging porpus
        self.enabledStatSpellcheck= True;       
        # set the option to show the collocations marks
        # default value is False, can be enabled for debuging porpus
        self.enabledShowCollocationMark= False;
        
        # set the option to use scoring teashkeel chosing.
        self.selectByScoreEnabled= False;
        # set the option to do syntaxic Analysis
        # default value is True, can be disabled for debuging porpus
        self.enabledSyntaxicAnalysis= True;
        # set the option to do allow ajusting voaclization result, for التقاء الساكنين
        # default value is True, can be disabled for debuging porpus
        self.enabledAjustVocalization=True;     
        # set the option to do Semantic Analysis
        # default value is True, can be disabled for debuging porpus        
        self.enabledSemanticAnalysis= True;
        # lexical analyzer
        self.analyzer=qalsadi.analex.Analex(cache_path)

        #speller based on yaraspell
        self.speller = yaraspell.spelldict.spelldict()
        # syntaxic analyzer
        # self.anasynt=aranasyn.anasyn.SyntaxAnalyzer();
        # semantic analyzer
        # self.anasem=asmai.anasem.SemanticAnalyzer();      
        #set the lexical analzer debugging
        self.analyzer.set_debug(debug);
        #set the lexical analzer  word limit
        self.analyzer.set_limit(self.limit);
        #collocations dictionary for statistical spellcheck
        # self.collo = collocations.CollocationClass(self.enabledShowCollocationMark);

    
    def set_limit(self, limit):
        """
        set the limit length of words to vocalize
        """
        self.limit=limit;
        #set the lexical analzer  wrd limit
        self.analyzer.set_limit(self.limit);

    def enableStatSpellcheck(self):
        """
        Enable the stat tasheel option.
        """
        self.enabledStatSpellcheck=True;
    def disableStatSpellcheck(self):
        """
        disable the stat tasheel option.
        """
        self.enabledStatSpellcheck= False;
    def getEnabledStatSpellcheck(self):
        """
        return the  the stat tasheel option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabledStatSpellcheck;
    def enableShowCollocationMark(self):
        """
        Enable the show the collocation mark option.
        """
        self.enabledShowCollocationMark=True;
        self.collo.enableShowDelimiter();
    def disableShowCollocationMark(self):
        """
        disable the show the collocation mark option.
        """
        self.enabledShowCollocationMark = False;
        self.collo.disableShowDelimiter();
    def getEnabledShowCollocationMark(self):
        """
        return the  the show the collocation mark option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabledShowCollocationMark;
    def enableLastMark(self):
        """
        Enable the last mark option.
        """
        self.enabledLastMark=True;
    def disableLastMark(self):
        """
        disable the last mark vocalization  option.
        """
        self.enabledLastMark=False;
    def getEnabledLastMark(self):
        """
        return the  the last mark vocalization option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabledLastMark;
    def enableSyntaxicAnalysis(self):
        """
        Enable the syntaxic analysis option.
        """
        self.enabledSyntaxicAnalysis=True;
    def disableSyntaxicAnalysis(self):
        """
        disable the syntaxic analysis option.
        """
        self.enabledSyntaxicAnalysis=False;
    def getEnabledSyntaxicAnalysis(self):
        """
        return the  the syntaxic analysis option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabledSyntaxicAnalysis;
    def enableSemanticAnalysis(self):
        """
        Enable the Semantic analysis option.
        """
        self.enabledSemanticAnalysis=True;
    def disableSemanticAnalysis(self):
        """
        disable the Semantic analysis option.
        """
        self.enabledSemanticAnalysis=False;
    def getEnabledSemanticAnalysis(self):
        """
        return the  the Semantic analysis option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabledSemanticAnalysis;
        
    def enableAjustVocalization(self):
        """
        Enable the Ajust Vocalization option.
        """
        self.enabledAjustVocalization=True;
    def disableAjustVocalization(self):
        """
        disable the Ajust Vocalization option.
        """
        self.enabledAjustVocalization=False;
    def getEnabledAjustVocalization(self):
        """
        return the  the Ajust Vocalization option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabledAjustVocalization;
    
    def fullStemmer(self, text):
        """
        Do the lexical, syntaxic  and semantic analysis of the text.
        @param text: input text.
        @type text: unicode.
        @return: syntaxic and lexical tags.
        rtype: list of list of stemmedSynWord class.
        """
        result=[];
        result=self.analyzer.check_text(text);
        return result;
    
    def spellcheck(self,inputtext,suggestion=False, format='text'):
        """
        Vocalize the text and give suggestion to improve spellcheck by user.
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: dict of dict or text.
        """
        texts=[inputtext, ];
        vocalized_text=u"";
        outputSuggestList=[]
        ChosenList=[]   
        suggestsList=[] 
        for text in texts:
            #morpholigical analysis of text
            detailled_syntax = self.fullStemmer(text);

            for wordCasesList in detailled_syntax:
                #wordCasesList = self.anasynt.exclode_cases(wordCasesList)
                currentChosen = wordCasesList[0]
                ChosenList.append(currentChosen);
                # create a suggest list
                suggest=[];
                if len(wordCasesList)==1 and wordCasesList[0].is_unknown():
                    if wordCasesList[0].is_unknown():
                        suggest = self.generateSuggest(currentChosen.get_word())
                suggest.sort();
                suggestsList.append(suggest);
        outputSuggestList=[]
        #create texts from chosen cases
        for i in range(len(ChosenList)):
            word = ChosenList[i].get_word();
            vocalized_text=u" ".join([vocalized_text,self.display(word,format)]);
            #~vocalized_text=u"".join([vocalized_text,self.display(word,format)]);
            outputSuggestList.append({'chosen':word,'suggest':u";".join(suggestsList[i])});
        if suggestion:
            return outputSuggestList;
        else:
            return vocalized_text;

    def yaraspellcheck(self,inputtext,suggestion=False, format='text'):
        """
        Vocalize the text and give suggestion to improve spellcheck by user.
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: dict of dict or text.
        """
        texts=[inputtext, ];
        vocalized_text=u"";
        outputSuggestList=[]
        ChosenList=[]    
        suggestsList=[]    
        autosuggestsList=[]
        for text in texts:
            #tokenize of text
            words = araby.tokenize(text);
            for word in words:
                suggests=[]
                autosuggest = []
                exists = self.speller.lookup(word)
                #~ print (u"'%s'\t%s"%(word, str(exists))).encode('utf8')
                if not exists:
                    suggests.append(word)
                    # create a suggest list
                    suggests.extend(self.speller.correct(word))
                    #print "suggestions\n", word.encode('utf8'),u" ".join(suggests).encode('utf8')
                    if len(suggests) > 1:
                        
                        autosuggest = self.speller.autocorrect(word, suggests)
                currentChosen = word
                ChosenList.append(currentChosen);
                suggestsList.append(suggests);
        outputSuggestList=[]
        #create texts from chosen cases
        for i in range(len(ChosenList)):
            word = ChosenList[i]
            vocalized_text=u" ".join([vocalized_text,self.display(word,format)]);
            #~vocalized_text=u"".join([vocalized_text,self.display(word,format)]);
            outputSuggestList.append({'chosen':word,'suggest':u";".join(suggestsList[i])});
        if suggestion:
            return outputSuggestList;
        else:
            return vocalized_text;
        

    def spellcheckOuputHtmlSuggest(self,text):
        """
        Vocalize the text and give suggestion to improve spellcheck by user.
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: dict of dict.
        """
        return self.yaraspellcheck(text,suggestion=True, format="html");
        
        
    def spellcheckOutputText(self,text):
        """
        Vocalize the text witthout suggestion
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: text.
        """
        return self.spellcheck(text,suggestion=False, format="text");


    def display(self, word, format="text"):
        """
        format the vocalized word to be displayed on web interface.
        @param word: input vocalized word.
        @type word: unicode.
        @return: html code.
        rtype: unicode.
        """
        format=format.lower();
        if format=="html":
            return u"<span id='vocalized' class='vocalized'>%s</span>"%word;
        elif format=='text':
            return word;
        else:
            return word;

    def edits1(self, word):
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in spellcheck_const.Alphabet if b]
        inserts    = [a + c + b     for a, b in splits for c in spellcheck_const.Alphabet]
        return set(deletes + transposes + replaces + inserts)

    def generateSuggest(self,word):
        """
        Generate word suggestion 
        @param word: input text.
        @type word: unicode.
        @return: generated suggestion.
        rtype: list of words.
        """
        wordlist=[word, araby.strip_tashkeel(word)];
        codidates=self.edits1(word)
        for condidate in codidates:
            if True :#self.accepted(condidate):
                wordlist.append(condidate);
        # commun letters error remplacement
        for tup in spellcheck_const.TabReplacment:
            sug =word.replace(tup[0], tup[1])
            if sug!=word: 
                # evaluate generated suggestion
                if self.accepted(sug):
                    wordlist.append(sug);
        wordlist = list(set(wordlist))
        return wordlist;
 
    def accepted(self,word):
        """
        test if  word is accecpted word (correct)
        @param word: input text.
        @type word: unicode.
        @return: True if word is accepted
        rtype: boolean.
        """
        result = self.analyzer.check_word(word);
        if result:
            # result has many cases
            if len(result)>1:
                return True;
            #one only case
            else :
                return not result[0].is_unknown();
        return False;





if __name__=="__main__":
    print "test";
    myrepr=arabRepr.ArabicRepr();
    speller=SpellcheckClass();
    text=u" اللغه العربيه"
    voc = speller.spellcheck(text, True);
    # print myrepr.repr(voc).encode('utf8')
    for itemd in voc:
        if itemd.get('suggest','') !='':
            for sug in itemd.get('suggest','').split(';'):
                print sug.encode('utf8'),'\t', araby.is_arabicword(sug)
