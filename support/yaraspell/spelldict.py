#!/usr/bin/python 
# -*- coding: utf-8 -*-
# Name:        spelltools
# Purpose:     functions and tools for Arabic spellchecker
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com) 
# Created:     2015-03-25
# Copyright:   (c) Taha Zerrouki 2015
# Licence:     GPL 
# Source : http://norvig.com/spell-correct.html 
#          How to Write a Spelling Corrector, 
#          Peter Norvig (GPL)
#---------------------------------------------------------------------

"""
    Arabic spell checker Class 
"""
from __future__ import (
            absolute_import,
                print_function,
                    unicode_literals,
                        division,
                            )
import re
import operator
import os
import sys
import string
sys.path.append("../lib")
sys.path.append("../")
import tashaphyne.stemming 
import pyarabic.araby as araby
from spelltools import edits1
from . import stem_const 
from . import spelltools
from . import spelldb
DICTFILENAME = os.path.join(os.path.dirname(os.path.realpath(__file__)), u"data/spellcheck.sqlite")
class spelldict:
    def __init__(self, dictfilename = DICTFILENAME):
        """
        Create spelldict instance
        @param dictfilename: the database file name
        @type dictfilename: string
        """
        # save file name
        self.dictfilename  =  dictfilename
        # a Cache for spelled words to avoid database over connecting
        self.worddict  = {}
        # A light stemmer to segment words
        self.stemmer = tashaphyne.stemming.ArabicLightStemmer()
        self.stemmer.set_prefix_list(stem_const.PREFIX_LIST);
        self.stemmer.set_suffix_list(stem_const.SUFFIX_LIST);
        # The database of spelling
        self.database = None
        self.database = spelldb.spellDictionary(self.dictfilename) 


    def __del__(self):
        """
        Delete spelldict instance
        """
        if self.database:
            self.database.__del__()     
        
    def lookup(self, word):
        """
        Lookup if the word is correct or not
        @param word: input word
        @type  word: unicode
        @return: True if word exists else False
        @rtype: Boolean
        """
        if not word: 
            return True
        if word.isdigit():
            return True
        for c in word:
            if c in string.punctuation:
                return True
        # test if the word is previouslly spelled
        # can get True or False
        if word in self.worddict:
            test = self.worddict.get(word, False)
        else:
            # if the word is not spelled
            word = araby.strip_tatweel(word)
            self.stemmer.segment(word)        
            # extract the affix 
            stem = self.stemmer.get_stem()
            affix = u"-".join([self.stemmer.get_prefix(), self.stemmer.get_suffix()])
            # lookup in the database
            test = self.database.lookup(word, stem, affix)
            self.worddict[word] = test
        return test
        

    def known_edits2(self, word):

        return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if self.lookup(e2))

    def known(self, words):
        """
        Test suggestions to be correct in dictionary 
        @param words: list of words
        @type  words: list of unicode
        @return: a list of correct suggestion words
        @rtype: list of unicode
        """
        # validate words by using arabic bigrams test
        words = filter(lambda x: spelltools.is_valid(x), words)
        # filter correct words from dictionnary
        return set(w for w in words if self.lookup(w))
        
    def correct(self, word):
        """
        Give suggestion to wrong word
        @param word: input word
        @type  word: unicode
        @return: a list of suggested words
        @rtype: list of unicode
        """
        candidates = self.known([word])
        if not candidates:
            candidates = self.known(edits1(word))
        #ToDo: implement the second error edits
        #if not candidates:
            #candidates =  self.known_edits2(word)
        if not candidates:
            candidates = [word]
        return sorted(candidates, key=lambda x: spelltools.phonetic_distance(word,x))
        #return sorted(candidates)


    def autocorrect(self, word, suggestions):
        """
        Test suggestions to be as autocorrection for given word  
        @param word: input word
        @type  word: unicode
        @param suggestions: list of words
        @type  suggestions: list of unicode
        @return: a list of correct suggestion words
        @rtype: list of unicode
        """
        normalize = spelltools.normalize
        # select autocorrect 
        normsource = normalize(word)
        #normlist = [ normalize(sug) for sug in suggestions]
        #for sug, normed in zip(suggestions,normlist):
        #    print u"\t".join([sug, normed]).encode("utf8")
        condidates = filter(lambda w: normalize(w) == normsource, suggestions)
        return condidates

    def add_to_custom(self, word):
        """
        Add a new word to custom dictionary
        @param word: the correct word to be added to custom dictionary
        @type word: unicode
        """
        self.database.add_to_costum(word)


     
def mainly():
    """
    main test
    """
    # Save a dictionary into a pickle file.
    speller = spelldict()
    # load is used only if we use files, it's very slow and heavy,
    # we use a database instead.
    # the database is loaded automaticly when speller object is created   
    #speller.load()


    print "affix dict len", len(speller.database.affixdict)
    print "word dict len", len(speller.database.stemdict)
    words =u""" أأجمعكما سلام يكتبون سلامتكمونا سلامتك الاسلامية داعش إستعمال ضلام علاقت صوة""".split(" ")
    words = u"""هذا احد الشباب الجزائري من مدينة بسكرة دائرة زريبة الوادي اسمه نور الدين شريط تعرض لصعقة كهربائية اثناء اداء عمله نجى منها من الموت المحقق الا انه بتر كلتى يداه.
الاخ نور الدين لا يريد الا اجراء عملية في الخارج ولكن التكاليف العملية قدرت بمليار سنتيم وهو من عائلة ميسورة الحال هو الان ينتضر الاعانة من الله اولا ثم من اخوانه الجزائريين.
لمزيد من المعلومات تجدونها في الصورة ادناه ان الله لا يضيع اجر المحسنين الخبوزية الجزائر""".split(" ")
    #words =[u"من", u"فككم", u"لا"]
    for word in words:
        exists = speller.lookup(word)
        print word.encode("utf8"), exists
        if not exists:
            suggests = speller.correct(word)
            print "suggestions\n", word.encode('utf8'),u" ".join(suggests).encode('utf8')
            if len(suggests) > 1:
                autosuggest = speller.autocorrect(word, suggests)
                if autosuggest:
                    print "autocorrect\n", word.encode('utf8'),u" ".join(autosuggest).encode('utf8')        
                else:
                    print "autocorrect\n", word.encode('utf8'), "No Autocorrect"
                    


if __name__ == "__main__":
    mainly()
