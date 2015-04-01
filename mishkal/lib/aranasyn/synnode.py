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
def ispunct(word):
    return word in u'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~،؟'
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

        self.word = ''
        #~""" The unstemmed word """
        self.previous_nodes = {}
        # the  syntaxical previous nodes 
        self.next_nodes = {}
        # the  syntaxical next nodes         
        self.originals = {}
        #~ Orginals word from dictionary
        # will be used to extarct semantic relations
        self.guessed_type_tag =""
        # guessed word type tag given by the word tagger
        self.break_end = False
        # the break position at he end or at the begining
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
                                
        #~""" The list of original words"""
        if case_list:
            self.word = case_list[0].get_word()
        for case in case_list:
            #extract originals lists
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
            if self.word and ispunct(self.word[0]):
                self.break_end = True
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
    def has_pount(self, ):
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
        return self.count["pounct"] == 0 and self.count["stopword"] == 0 and \
        self.count["verb"] and self.count["noun"] == 0
    def is_noun(self, ):
        """
        Return if all cases are nouns.
        @return:True if the node is noun in alll cases.
        @rtype:boolean
        """
        return self.count["pounct"] == 0 and self.count["stopword"] == 0 and \
        self.count["verb"] == 0 and self.count["noun"]
        

    def is_stopword(self, ):
        """
        Return if all cases are stopwords.
        @return:True if the node is stopword in alll cases.
        @rtype:boolean
        """
        return self.count["pounct"] == 0 and self.count["stopword"] and \
        self.count["verb"] == 0 and self.count["noun"] == 0
    def is_pounct(self, ):
        """
        Return if all cases are pounctuations
        @return:True if the node is pounctation in alll cases.
        @rtype:boolean
        """
        return self.count["pounct"] and self.count["stopword"] == 0 and \
        self.count["verb"] == 0 and self.count["noun"] == 0
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
        return self.count["noun"] > self.count["verb"]  and \
        self.count["noun"] > self.count["stopword"]

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
    def is_break_end(self,):
        return self.break_end
    def is_break(self,):
        return self.get_break_type() in ("break", "mostBreak")
    def __repr__(self):
        text = u"\n'%s':%s, [%s-%s]{V:%d, N:%d, S:%d} " % (
        self.__dict__['word'], u', '.join(self.originals), 
        self.get_word_type(), self.get_break_type(), self.count["verb"], 
        self.count["noun"], self.count["stopword"])
        text += repr(self.syntax_mark)
        return text.encode('utf8') 

if __name__ == "__main__":
    print "Syn Node module"
