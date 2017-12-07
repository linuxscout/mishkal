#!/usr/bin/python
# -*- coding = utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Arabic Dictionary from Arramooz Al Waseet
# Purpose:     Sematic relations Dictionary.
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     21-03-2016
# Copyright:   (c) Taha Zerrouki 2016
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
Arabic Semantic relations Dictionary Class from Arramooz Al Waseet.
Used in multiporpus morpholigical treatment
"""
import re
import os, os.path
import sqlite3 as sqlite
import sys
if __name__  ==  '__main__':
    sys.path.append('../');
FILE_DB = u"../maskouk/data/semantic.sqlite"
import pyarabic.araby as araby
class SemanticDictionary:
    """
    Arabic Semntic relations dictionary Class
    Used to allow abstract acces to lexicon of arabic language, 
    can get indexed and hashed entries from the  basic lexicon
    add also, support to extract attributtes from entries
    """

    def __init__(self):
        """
        initialisation of dictionary from a data dictionary, create indexes 
        to speed up the access.

        """

        # get the database path
        if hasattr(sys, 'frozen'): # only when running in py2exe this exists
            base = sys.prefix
        else: # otherwise this is a regular python script
            base = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(base, FILE_DB)
        self.db_connect  = False
        if os.path.exists(file_path):
            try:
                self.db_connect = sqlite.connect(file_path)                
                self.db_connect.row_factory = sqlite.Row 
                self.cursor = self.db_connect.cursor()
            except  IOError:
                print "Fatal Error Can't find the database file", file_path
                if __name__  ==  '__main__':
                    sys.exit();
        else:
            print u" ".join(["Inexistant File", file_path, " current dir ", 
            os.curdir]).encode('utf8')
            if __name__  ==  '__main__':
                sys.exit();            

    def __del__(self):
        """
        Delete instance and close database connection
        
        """
        if self.db_connect:
            self.db_connect.close()


    def get_entry_by_id(self, idf):
        """ Get dictionary entry by id from the dictionary
        @param id :word identifier
        @type id: integer
        @return: all attributes
        @rtype: dict
        """
        # lookup for a word
        sql = u"select * FROM %s WHERE id='%s'" % (self.table_name, idf)
        try:
            self.cursor.execute(sql)
            if self.cursor:
                return self.cursor.fetchall()            
        except  sqlite.OperationalError:
            return False
        return False

    def get_attrib_by_id(self, idf, attribute):
        """ Get attribute value by id from the dictionary
        @param id :word identifier
        @type id: integer
        @param attribute :the attribute name
        @type attribute: unicode
        @return: The attribute
        value
        @rtype: mix.
        """
        # if the id exists and the attribute existe return the value, 
        sql = u"select * FROM %s WHERE id='%s'" % (self.table_name, idf)
        try:
            self.cursor.execute(sql)
            if self.cursor:
                for row in self.cursor:
                    return  row[attribute]                        
        except  sqlite.OperationalError:
            return False
        return False

    def lookup_rule(self, primate_word, second_word):
        """
        look up for the relation between first and secondword
        @param primate_word: the derived word.
        @type primate_word: unicode.
        @param second_word: the related word.
        @type second_word: unicode.
        @return: list of relations .
        @rtype: list.
        """
        rulelist = []
        # search for direct relation between first and second word
        sql = u"select rule FROM relations WHERE first='%s' and second ='%s'" % (primate_word,
         second_word)
        try:
            self.cursor.execute(sql)
            if self.cursor:
                for row in self.cursor:
                    rulelist.append(row['rule'])
                if rulelist:
                    return rulelist[0]
        except  sqlite.OperationalError:
            return []
        return False
    def get_original(self, primate_word):
        """
        look up for the original verb fo the given word
        @param primate_word: the derived word.
        @type primate_word: unicode.
        @return:  (verb, derivation type) .
        @rtype: tuple of unicode.
        """
        idlist = []
        sql = u"select verb, type FROM derivations WHERE derived = '%s'" % (primate_word)
        try:
            self.cursor.execute(sql)
            if self.cursor:
                for row in self.cursor:
                    idlist.append((row[0],row[1]))
                if idlist:
                    return idlist[0]
            
        except  sqlite.OperationalError:
            print "degat",  primate_word.encode('utf8')
            return ('','') 
        return ('','') 
    def lookup(self, primate_word, second_word):
        """
        look up for the relation between first and secondword
        @param primate_word: the derived word.
        @type primate_word: unicode.
        @param second_word: the related word.
        @param original:  if the lookup is made with original word
        @type second_word: unicode.
        @return: list of relations .
        @rtype: list.
        """
        rule = False
        # search for direct relation between first and second word
        rule = self.lookup_rule(primate_word, second_word)
        
        # look up if the first word is derived 
        if not rule:
           # look up if the first word is derived 
           # as subject
           original_primate_word, derivation_type = self.get_original(primate_word)
           if original_primate_word and second_word:
               rule = self.lookup_rule(original_primate_word, second_word)
               # test if rulelist is icompatible with derivation type
               if self.is_compatible(rule, derivation_type):
                    return rule
               else: 
                    rule = False
        return rule

        
    def is_compatible(self, rule, derivation_type):
        """
        Test if the rule is compatible to derivation type
        @param rule: the given rule.
        @type rule: unicode.
        @param derivation_type: the given derivation_type.
        @type derivation_type: unicode.
        @return: Boolean .
        @rtype: Boolean.
        """
        # Todo للعمل على
        # صيغة المبالغة
        # صفة مشبهة
        return rule == derivation_type       
#Class test
def mainly():
    """
    main test
    """
    #ToDo: use the full dictionary of arramooz
    VERB_DICTIONARY_INDEX = {
    u'id':0, 
    u'first':1, 
    u'second':2, 
    u'rule':3, 
    }
    #from   dictionaries.verb_dictionary  import *
    mydict = SemanticDictionary()
    wordlist = [
    [u"", u'استقل'],
    [u'اِسْتَعْمَلَ', u"قَلَمٌ"],
    [u'مُسْتَعْمَلٌ', u"قَلَمٌ"],
    [u'مُسْتَعْمِلٌ', u"قَلَمٌ"],
    [ u'شَرَّحَ', u"طَبِيبٌ"],
    [ u'شَرَّحَ', u"جَسَدٌ"],
    [u'نَشَّطَ', u"دَواءٌ"],
    [u'نَشَّطَ', u"دَوَاءٌ"],
    [u'مُنَشَّطٌ', u"دَوَاءٌ"],
    ]
    for words in wordlist:
        result = mydict.lookup( words[0], words[1])
        if result: 
            #~ print (u" ".join(result)).encode('utf8')
            print (u" ".join(words)).encode('utf8'), result
        else:
            print "No result", (u" ".join(words)).encode('utf8')
if __name__  ==  '__main__':
    mainly()
