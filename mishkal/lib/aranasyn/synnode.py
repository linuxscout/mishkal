#!/usr/bin/python
# -*- coding=utf-8 -*-
#------------------------------------------------------------------------
# Name:        synNode
# Purpose:     representat data analyzed given by morphoanalyzer Qalsadi
# then by syntaxic analyzer
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     19-09-2012
# Copyright:   (c) Taha Zerrouki 2012
# Licence:     GPL
#------------------------------------------------------------------------
"""
synNode represents the regrouped data resulted from the 
morpholocigal analysis
"""
if __name__ == "__main__":
    import sys
    sys.path.append('../lib')

#~import aranasyn.syn_const as syn_const
#~import aranasyn.stemmedsynword
class SynNode:
    """
    synNode represents the regrouped data resulted from the 
    morpholocigal analysis
    """
    def __init__(self, case_list):
        """
        Create the synNode  from a list of StemmedSynword cases
        """
        self.case_count = len(case_list)
        #~""" the number of syntaxtical cases """

        self.verb_count = 0
        #~""" the number of syntaxtical verb cases """

        self.noun_count = 0
        #~""" the number of syntaxtical noun cases """

        self.stopword_count = 0
        #~""" the number of syntaxtical stopword cases """
        
        self.word = ''
        #~""" The unstemmed word """
        self.originals = {}
        self.word_type = {'verb':[], 
                        'noun':[], 
                        'pounct':[], 
                        'stopword':[], 
                        }
        self.breaks = []
        self.non_breaks = []
        self.syntax_mark = {'mansoub':[], 
                        'marfou3':[], 
                        'majrour':[], 
                        'majzoum':[], 
                        'tanwin_mansoub':[], 
                        'tanwin_marfou3':[], 
                        'tanwin_majrour':[],                     
                    
                        }
        #~""" The list of original words"""
        if case_list:
            self.word = case_list[0].get_word()
        for case in case_list:
            if self.originals.has_key(case.get_original()):
                self.originals[case.get_original()].append(case.get_order())
            else:
                self.originals[case.get_original()] = [case.get_order(), ]
            #indexing by word type
            if case.is_verb():
                self.word_type['verb'].append(case.get_order())
            elif case.is_noun():
                self.word_type['noun'].append(case.get_order())
            elif case.is_stopword():
                self.word_type['stopword'].append(case.get_order())
            elif case.is_pounct():
                self.word_type['pounct'].append(case.get_order())
            #indexing break and non break word cases
            if case.is_break():
                self.breaks.append(case.get_order())
            else:
                self.non_breaks.append(case.get_order())
            #indexing by syntax mark and tanwin
            if case.is_tanwin():
                if case.is_mansoub():
                    self.syntax_mark['tanwin_mansoub'].append(case.get_order())
                elif case.is_marfou3():
                    self.syntax_mark['tanwin_marfou3'].append(case.get_order())
                elif case.is_majrour():
                    self.syntax_mark['tanwin_majrour'].append(case.get_order())
            else:
                if case.is_mansoub():
                    self.syntax_mark['mansoub'].append(case.get_order())
                elif case.is_marfou3():
                    self.syntax_mark['marfou3'].append(case.get_order())
                elif case.is_majrour():
                    self.syntax_mark['majrour'].append(case.get_order())
                elif case.is_majzoum():                
                    self.syntax_mark['majzoum'].append(case.get_order())
            
                
                
        self.verb_count     = len(self.word_type['verb'])
        self.noun_count     = len(self.word_type['noun'])
        self.stopword_count = len(self.word_type['stopword'])                
        self.pounct_count = len(self.word_type['pounct'])            
        
    ######################################################################
    #{ Attributes Functions
    ###################################################################### 

    def set_case_count(self, count):
        """
        Set the case count.
        @param count: the number of stemmed word  cases
        @tyep count: integer
        """
        self.case_count = count
    def get_case_count(self):
        """
        get the case count.
        @return: the number of stemmed word  cases
        @tyep count: integer
        """
        return self.case_count
    def set_verb_count(self, count):
        """
        Set the verb count.
        @param count: the number of stemmed word cases as  verbs
        @tyep count: integer
        """
        self.verb_count = count
    def get_verb_count(self):
        """
        get the verb count.
        @return: the number of stemmed word cases as verbs
        @tyep count: integer
        """
        return self.verb_count
        
    def set_noun_count(self, count):
        """
        Set the noun count.
        @param count: the number of stemmed word cases as  nouns
        @tyep count: integer
        """
        self.noun_count = count
    def get_noun_count(self):
        """
        get the noun count.
        @return: the number of stemmed word cases as nouns
        @tyep count: integer
        """
        return self.noun_count
    def set_stopword_count(self, count):
        """
        Set the stopword count.
        @param count: the number of stemmed word cases as  stopwords
        @tyep count: integer
        """
        self.stopword_count = count
    def get_stopword_count(self):
        """
        get the stopword count.
        @return: the number of stemmed word cases as stopwords
        @tyep count: integer
        """
        return self.stopword_count
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
    def get_original(self, ):
        """
        Get the original forms of the input word
        @return: the given original.
        @rtype: unicode string
        """
        return self.originals.keys()

    def set_original(self, neworiginal):
        """
        Set the original words
        @param neworiginal: the new given original.
        @type neworiginal: unicode string list
        """
        self.originals = neworiginal

    ######################################################################
    #{ Tags extraction Functions
    ###################################################################### 
    def has_verb(self, ):
        """
        Return if all cases are verbs.
        @return:True if the node has verb in one case at least.
        @rtype:boolean
        """
        return self.verb_count > 0
    def has_noun(self, ):
        """
        Return if all cases are nouns.
        @return:True if the node has noun in one case at least.
        @rtype:boolean
        """
        return self.noun_count > 0

    def has_stopword(self, ):
        """
        Return if all cases are stopwords.
        @return:True if the node has stopword in one case at least.
        @rtype:boolean
        """
        return self.stopword_count > 0
    def has_pount(self, ):
        """
        Return if all cases are pounctuations
        @return:True if the node has pounctation in one case at least.
        @rtype:boolean
        """
        return self.pounct_count > 0        
    def is_verb(self, ):
        """
        Return if all cases are verbs.
        @return:True if the node is verb in alll cases.
        @rtype:boolean
        """
        return self.pounct_count == 0 and self.stopword_count == 0 and \
        self.verb_count and self.noun_count == 0
    def is_noun(self, ):
        """
        Return if all cases are nouns.
        @return:True if the node is noun in alll cases.
        @rtype:boolean
        """
        return self.pounct_count == 0 and self.stopword_count == 0 and \
        self.verb_count == 0 and self.noun_count
        

    def is_stopword(self, ):
        """
        Return if all cases are stopwords.
        @return:True if the node is stopword in alll cases.
        @rtype:boolean
        """
        return self.pounct_count == 0 and self.stopword_count and \
        self.verb_count == 0 and self.noun_count == 0
    def is_pount(self, ):
        """
        Return if all cases are pounctuations
        @return:True if the node is pounctation in alll cases.
        @rtype:boolean
        """
        return self.pounct_count and self.stopword_count == 0 and \
        self.verb_count == 0 and self.noun_count == 0
    def is_most_verb(self, ):
        """
        Return True if most  cases are verbs.
        @return:True if the node is verb in most cases.
        @rtype:boolean
        """
        
        return self.verb_count > self.noun_count and \
        self.verb_count > self.stopword_count
    def is_most_noun(self, ):
        """
        Return True if most  cases are nouns.
        @return:True if the node is noun in most cases.
        @rtype:boolean
        """
        return self.noun_count > self.verb_count  and \
        self.noun_count > self.stopword_count

    def is_most_stopword(self, ):
        """
        Return True if most cases are stopwords.
        @return:True if the node is stopword in most cases.
        @rtype:boolean
        """
        return self.stopword_count > self.verb_count  and \
        self.stopword_count > self.noun_count

    def get_word_type(self, ):
        """
        Return the word type.
        @return:the word type or mosttype.
        @rtype:string
        """
        if self.is_noun():
            return 'noun'
        elif self.is_verb():
            return 'verb'
        elif self.is_stopword():
            return 'stopword'
        elif self.is_pount():
            return 'pounct'            
        elif self.is_most_noun():
            return 'mostnoun'
        elif self.is_most_verb():
            return 'mostverb'
        elif self.is_most_stopword():
            return 'moststopword'
        else:
            return 'ambiguous'
    def get_break_type(self, ):
        """
        Return the word break type, 
        if the word break the sentences or not.
        @return:the word type or mosttype.
        @rtype:string
        """
        if len(self.breaks) > 0 and len(self.non_breaks) == 0 :
            return 'break'
        elif len(self.non_breaks) > 0 and len(self.breaks) == 0:
            return 'non_break'
        elif len(self.non_breaks) > len(self.breaks) :
            return 'mostNon_break'
        elif len(self.non_breaks) < len(self.breaks) :
            return 'most_break'
        else:
            return 'ambiguous'
    def __repr__(self):
        text = u"\n'%s':%s, [%s-%s]{V:%d, N:%d, S:%d} " % (
        self.__dict__['word'], u', '.join(self.originals), 
        self.get_word_type(), self.get_break_type(), self.verb_count, 
        self.noun_count, self.stopword_count)
        text += repr(self.syntax_mark)
        # for k in self.__dict__.keys():
            # text += u"\t'%s':\t%s, \n "%(k, self.__dict__[k])
        return text.encode('utf8') 

if __name__ == "__main__":
    print "Syn Node module"
