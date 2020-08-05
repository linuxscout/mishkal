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
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    division,
    )
if __name__ == "__main__":
    import sys
    sys.path.append('../lib')

def ispunct(word):
    return word in u'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~،؟'

from . import syn_const

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
        #~ print("case_list", len(case_list))
        self.word = ''
        #~""" The unstemmed word """
        self.previous_nodes = {}
        # the  syntaxical previous nodes 
        self.next_nodes = {}
        # the  syntaxical next nodes
        self.vocalizeds = []
        if case_list:        
            self.vocalizeds = [case.get_vocalized() for case in case_list]
            self.vocalizeds = list(set(self.vocalizeds))
            self.vocalizeds.sort()
        
        #~ all vocalized forms
        self.originals = {}
        #~ Orginals word from dictionary
        # will be used to extarct semantic relations
        self.guessed_type_tag = ""
        # guessed word type tag given by the word tagger
        self.break_end = False
        # the break position at the end or at the begining
        # the pounctuation is an end break 
        # a stop word is a start break
        
        self.word_type = {'verb':[], 
                        'noun':[], 
                        'pounct':[], 
                        'stopword':[], 
                        }
        self.count = {'verb':[], 
                        'noun':[], 
                        'pounct':[], 
                        'stopword':[], 
                        }                        
        # word type count after analysis
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
        self.syn_previous = {} # generate dict for whole list of cases
        # the syntaxic previous of cases after syntax analysis        
        self.syn_nexts = {} # generate dict for whole list of cases
        # the syntaxic nexts of cases after syntax analysis
        self.sem_previous = {} # generate dict for whole list of cases
        # the semantic previous of cases after semantic analysis        
        self.sem_nexts = {} # generate dict for whole list of cases
        # the semantic nexts of cases after semantic analysis
        
        self.chosen_indexes = list(range(len(case_list)))
        #~ print("chosen indexes", self.chosen_indexes, len(self.chosen_indexes), len(case_list))
        # used to choose specific cases 
                                
        #~""" The list of original words"""
        if case_list:
            self.word = case_list[0].get_word()
        
        for case in case_list:
            #extract originals lists
            idx = case.get_order()
            if case.get_original() in self.originals:
                self.originals[case.get_original()].append(idx)
            else:
                self.originals[case.get_original()] = [idx, ]
            #indexing by word type
            if case.is_verb():
                self.word_type['verb'].append(idx)
            if case.is_noun():
                self.word_type['noun'].append(idx)
            if case.is_stopword():
                self.word_type['stopword'].append(idx)
            if case.is_pounct():
                self.word_type['pounct'].append(idx)
            #indexing break and non break word cases
            if case.is_break():
                self.breaks.append(idx)
            else:
                self.non_breaks.append(idx)
            if self.word and ispunct(self.word[0]):
                self.break_end = True
            #indexing by syntax mark and tanwin
            if case.is_tanwin():
                if case.is_mansoub():
                    self.syntax_mark['tanwin_mansoub'].append(idx)
                elif case.is_marfou3():
                    self.syntax_mark['tanwin_marfou3'].append(idx)
                elif case.is_majrour():
                    self.syntax_mark['tanwin_majrour'].append(idx)
            else:
                if case.is_mansoub():
                    self.syntax_mark['mansoub'].append(idx)
                elif case.is_marfou3():
                    self.syntax_mark['marfou3'].append(idx)
                elif case.is_majrour():
                    self.syntax_mark['majrour'].append(idx)
                elif case.is_majzoum():                
                    self.syntax_mark['majzoum'].append(idx)
            # get all syntaxic relations
            if case.has_previous(): 
                self.syn_previous[idx] = case.get_previous()
            if case.has_next():
                self.syn_nexts[idx] = case.get_next()   
            if case.has_sem_previous(): 
                self.sem_previous[idx] = case.get_sem_previous()
            if case.has_sem_next():
                self.sem_nexts[idx] = case.get_sem_next()               
            
        self.count = {"verb":len(self.word_type['verb']), 
                    #~""" the number of syntaxtical verb cases """
                    "noun": len(self.word_type['noun']), 
                    #~""" the number of syntaxtical noun cases """
                    "stopword" : len(self.word_type['stopword']), 
                    #~""" the number of syntaxtical stopword cases """
                    "pounct": len(self.word_type['pounct'])  
        }

        # the sematic nexts of cases        
        
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

    def set_guessed_type_tag(self, tag):
        """
        Set the guessed type tag.
        @param tag: guessed type tag
        @type tag: unicode
        """
        self.guessed_type_tag = tag

    def get_guessed_type_tag(self):
        """
        get the guessed type tag.
        @return: guessed type tag
        @rtype: unicode
        """
        return self.guessed_type_tag
        
    def get_case_count(self):
        """
        get the guessed type tag.
        @return: guessed type tag
        @rtype tag: unicode        
        """
        return self.guessed_type_tag

    def set_verb_count(self, count):
        """
        Set the verb count.
        @param count: the number of stemmed word cases as  verbs
        @tyep count: integer
        """
        self.count["verb"] = count
    def get_verb_count(self):
        """
        get the verb count.
        @return: the number of stemmed word cases as verbs
        @tyep count: integer
        """
        return self.count["verb"]
        
    def set_noun_count(self, count):
        """
        Set the noun count.
        @param count: the number of stemmed word cases as  nouns
        @tyep count: integer
        """
        self.count["noun"] = count
    def get_noun_count(self):
        """
        get the noun count.
        @return: the number of stemmed word cases as nouns
        @tyep count: integer
        """
        return self.count["noun"]
    def set_stopword_count(self, count):
        """
        Set the stopword count.
        @param count: the number of stemmed word cases as  stopwords
        @tyep count: integer
        """
        self.count["stopword"] = count
    def get_stopword_count(self):
        """
        get the stopword count.
        @return: the number of stemmed word cases as stopwords
        @tyep count: integer
        """
        return self.count["stopword"]
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
        return list(self.originals.keys())
    def get_vocalizeds(self, ):
        """
        Get the vocalized forms of the input word
        @return: the given vocalizeds.
        @rtype: list of unicode string
        """
        return self.vocalizeds        

    def get_chosen_indexes(self, ):
        """
        Get the chosen_indexes forms of the input word
        @return: the given chosen_indexes.
        @rtype: unicode string
        """
        return self.chosen_indexes

    def set_chosen_indexes(self,indexes ):
        """
        Get the chosen_indexes forms of the input word
        @return: the given chosen_indexes.
        @rtype: unicode string
        """
        # verify that all indexes are in range
        for i in indexes:
            if i >= self.case_count or i < 0:
                break;
        else:
            self.chosen_indexes = indexes

    ######################################################################
    #{ Tags extraction Functions
    ###################################################################### 
    def has_verb(self, ):
        """
        Return if all cases are verbs.
        @return:True if the node has verb in one case at least.
        @rtype:boolean
        """
        return self.count["verb"] > 0

    def has_noun(self, ):
        """
        Return if all cases are nouns.
        @return:True if the node has noun in one case at least.
        @rtype:boolean
        """
        return self.count["noun"] > 0

    def has_stopword(self, ):
        """
        Return if all cases are stopwords.
        @return:True if the node has stopword in one case at least.
        @rtype:boolean
        """
        return self.count["stopword"] > 0

    def has_punct(self, ):
        """
        Return if all cases are pounctuations
        @return:True if the node has pounctation in one case at least.
        @rtype:boolean
        """
        return self.count["pounct"] > 0        

    def is_verb(self, ):
        """
        Return if all cases are verbs.
        @return:True if the node is verb in alll cases.
        @rtype:boolean
        """
        return (self.count["verb"] and not self.count["pounct"] and not self.count["stopword"] and
         not self.count["noun"] )

    def is_noun(self, ):
        """
        Return if all cases are nouns.
        @return:True if the node is noun in alll cases.
        @rtype:boolean
        """
        return not self.count["pounct"]  and not self.count["stopword"]  and  not\
        self.count["verb"]  and self.count["noun"]
        

    def is_stopword(self, ):
        """
        Return if all cases are stopwords.
        @return:True if the node is stopword in alll cases.
        @rtype:boolean
        """
        return not self.count["pounct"] and self.count["stopword"] and \
        not self.count["verb"]  and not self.count["noun"] 

    def is_pounct(self, ):
        """
        Return if all cases are pounctuations
        @return:True if the node is pounctation in alll cases.
        @rtype:boolean
        """
        return (self.count["pounct"] and not self.count["stopword"]  and 
            not self.count["verb"]  and not self.count["noun"] )

    def is_most_verb(self, ):
        """
        Return True if most  cases are verbs.
        @return:True if the node is verb in most cases.
        @rtype:boolean
        """
        
        return self.count["verb"] > self.count["noun"] and \
        self.count["verb"] > self.count["stopword"]

    def is_most_noun(self, ):
        """
        Return True if most  cases are nouns.
        @return:True if the node is noun in most cases.
        @rtype:boolean
        """
        return (self.count["noun"] > self.count["verb"]  and \
        self.count["noun"] > self.count["stopword"])

    def is_most_stopword(self, ):
        """
        Return True if most cases are stopwords.
        @return:True if the node is stopword in most cases.
        @rtype:boolean
        """
        return self.count["stopword"] > self.count["verb"]  and \
        self.count["stopword"] > self.count["noun"]

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
        elif self.is_pounct():
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
        #~if len(self.breaks) == 0 and len(self.non_breaks) == 0 :
            #~return 'ambiguous'
        #~elif 
        if self.breaks and not self.non_breaks:
            return 'break'
        # إذا كانت الكلمة مستبعدة ولم يكن لها علاقة دلالية بما قبلها
        elif self.has_stopword() and not self.sem_previous and not self.sem_nexts:
            return 'break'
        elif self.non_breaks and not self.breaks:
            return 'non_break'
        elif len(self.non_breaks) > len(self.breaks) :
            return 'mostNon_break'
        elif len(self.non_breaks) < len(self.breaks) :
            return 'most_break'
        else:
            return 'ambiguous'

    def is_break_end(self,):
        """
        The syn node is break end like puctuation, if it  hasn't any syntaxique or semantique 
        relation with the previous word
        """

        return self.break_end

    def is_break(self,):
        """
        The syn node is break, if it hasn't any syntaxique or semantique 
        relation with the previous word
        """
        #~ return not self.syn_previous and not self.sem_previous #or self.get_break_type() == "break"
        return self.get_break_type() in ("break", "mostBreak")

    def is_next_break(self,):
        """
        The syn node is next break, if it hasn't any syntaxique or semantique 
        relation with the next word
        """
        if not(self.syn_nexts or self.sem_nexts):
            return True
        else:
        # or only the relation is tanwin
            for key in self.syn_nexts:
                if self.syn_nexts[k] != syn_const.TanwinRelation:
                    return False
        return False
                
    def __repr__(self):
        text = u"\n'%s':%s, [%s-%s]{V:%d, N:%d, S:%d} " % (
            self.__dict__['word'], u', '.join(self.originals), 
            self.get_word_type(), self.get_break_type(), self.count["verb"], 
            self.count["noun"], self.count["stopword"], )
        text += repr(self.syntax_mark)
        text += "Indexes : "+ repr(self.chosen_indexes)
        return text

if __name__ == "__main__":
    print( "Syn Node module")
