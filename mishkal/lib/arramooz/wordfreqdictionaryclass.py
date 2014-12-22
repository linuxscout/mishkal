#!/usr/bin/python
# -*- coding = utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Arabic Dictionary from Arramooz Al Waseet
# Purpose:     Morphological porpus Dictionary.
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     16-12-2013
# Copyright:   (c) Taha Zerrouki 2013
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
Arabic Word frequency Dictionary Class from Arramooz Al Waseet.
Used in multiporpus morpholigical treatment
"""
import re
import sys, os
if __name__  ==  '__main__':
  sys.path.append('../')  
import sqlite3 as sqlite
FILE_DB_FREQ = u"data/wordfreq.sqlite"
import pyarabic.araby as araby
WORDFREQ_DICTIONARY_INDEX = {
u'id':0, # id
u'vocalized':1, # the vocalized word
u'unvocalized':2, # the unvocalized form
u'word_type':3, # the word frequency
u'freq':4, # the word class
u'future_type':5, # the haraka for verb    
#u'trans':5, # translation
}
class WordFreqDictionary:
    """
        Arabic dictionary Class
        Used to allow abstract acces to lexicon of arabic language, 
        can get indexed and hashed entries from the  basic lexicon
        add also, support to extract attributtes from entries
    """

    def __init__(self, table_name, attrib_index, key_attribute = 'unvocalized'):
        """
        initialisation of dictionary from a data dictionary, 
        create indexes to speed up the access.

        """
        # load data from the brut dictionary into
        # a new dictionary with numeric ids
        self.dictionary = {}
        self.attrib_index = attrib_index
        self.key_attribute =  key_attribute
        self.attrib_num_index = {}
        # create the attribute num index
        # attrib_index:         attrib_num_index
        # vocalized: 0        0: vocalized
        #unvocalized: 1        1: unvocalized
        #
        for k in self.attrib_index.keys():
            val = self.attrib_index[k]
            self.attrib_num_index[val] = k
        self.table_name = table_name
        # get the database path
        if hasattr(sys, 'frozen'): # only when running in py2exe this exists
            base  =  sys.prefix
        else: # otherwise this is a regular python script
            base  =  os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(base, FILE_DB_FREQ)
        
        if os.path.exists(file_path):
            try:
                self.db_connect  =  sqlite.connect(file_path)
                self.db_connect.row_factory  =  sqlite.Row                 
                self.cursor  =  self.db_connect.cursor()
            except IOError:
                print "Fatal Error Can't find the database file", file_path

        else:
            print u" ".join(["Inexistant File", file_path, " current dir ",
             os.curdir]).encode('utf8')
        #create index to speed up search
        index_field = 'unvocalized'
        self.create_table_index(index_field)

        # if self.create_table_index(index_field):
            # print 'Index created'
        # else:
            # print (' Cant create index', self.table_name, index_field)

    def __del__(self):
        """
        Delete instance and close database connection
        
        """
        if self.db_connect:
            self.db_connect.close()

            
            
    def create_table_index(self, index_field):
        """ create the database index if not exists
        @param index_field: the given to be indexed field
        @type index_field: text
        @return: void
        @rtype: void
        """
        sql  =  u"create index if not exists myindex on %s (%s)" % (
        self.table_name, index_field)
        try:
            self.cursor.execute(sql)
            if self.cursor:
                return True
                
        except sqlite.OperationalError:
            return False

    def get_entry_by_id(self, idf):
        """ Get dictionary entry by id from the dictionary
        @param id :word identifier
        @type id: integer
        @return: all attributes
        @rtype: dict
        """
        # if the id exists and the attribute existe return the value, 
        #else return False
        # The keys in the dictinary are numeric, for comression reason, 
        # then we use text keys in output, according 
        # to the self.attrib_num_index
        # eg.
        # entry  = {0:"kataba", 1:"ktb"}
        # output entry  = {'vocalized':'kataba', 'unvocalized':'ktb'}
        sql  =  u"select * FROM %s WHERE id='%s'" % (self.table_name, idf)
        try:
            self.cursor.execute(sql)
            if self.cursor:
                return self.cursor.fetchall()
                # for row in self.cursor:
                    # entry_dict = {}
                    # for numKey in self.attrib_num_index:
                        # textKey  =  self.attrib_num_index[numKey]
                        # entry_dict[textKey]  =  row[numKey]
                    # return entry_dict
        except sqlite.OperationalError:
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
        # if the given attribute existes on the attrib index
        #in order to redure the dictionary size we use numecric 
        #index to show the attributes
        # like
        #NOUN_DICTIONATY_INDEX = {u'vocalized':0, u'unvocalized':1, 
        #~u'wordtype':2,
         #~u'root':3, u'original':4, u'mankous':5, u'feminable':6, u'number':7,
         # u'dualable':8,
         #~u'masculin_plural':9,
         #~u'feminin_plural':10, u'broken_plural':11, u'mamnou3_sarf':12,
         #~u'relative':13, u'w_suffix':14, u'hm_suffix':15, u'kal_prefix':16, 
        #~u'ha_suffix':17, u'k_suffix':18, u'annex':19, u'definition':20, 
        #u'note':21, }
         #~#NOUN_DICTIONARY = {
          #~#u'مفرد/تكسير':{0:u'مفرد/تكسير', 1:u'مفرد/تكسير', 2:u'اسم فاعل', 
          #3:u'',
         #~4:u'', 5:u'المنقوص', 6:u'التأنيث', 7:u'جمع تكسير', 8:u'التثنية', 
         #9:u'"ج. مذ. س."'
        #~, 10:u'"ج. مؤ. س."', 11:u'الجمع', 12:u'', 13:u'نسب', 14:u'ـو', 1
        #5:u'هم'
        #~, 16:u'كال', 17:u'ها', 18:u'ك', 19:u'"إض. لف."', 20:u'', 
        #~21:u':لا جذر:لا مفرد:لا تشكيل:لا شرح', }, 
                #~#u'شَاذّ':{0:u'شَاذّ', 1:u'شاذ', 2:u'اسم فاعل', 3:u'',
         #~4:u'', 5:u'', 6:u'Ta', 7:u'جمع تكسير', 8:u'DnT', 9:u'Pm', 
        #~10:u'Pf', 11:u'":شواذ"', 12:u'', 13:u'', 14:u'', 15:u'', 
        #~16:u'', 17:u'', 18:u'', 19:u'', 20:u'', 
        #21:u':لا جذر:لا مفرد:لا شرح', }, 

        # if self.attrib_index.has_key(attribute):
            # attnum = self.attrib_index[attribute]
        # else:
            # return False
        # if the id exists and the attribute existe return the value,
        # else return False
        sql  =  u"select * FROM %s WHERE id='%d'" % (self.table_name, idf)
        try:
            self.cursor.execute(sql)
        except sqlite.OperationalError:
            print "Fatal Error on query: wordfreq dict error 12"
            return False 
        if self.cursor:
            for row in self.cursor:
                return  row[attribute]
        return False

    def lookup(self, text, word_type = ''):
        """
        look up for all word forms in the dictionary, according to word_type
            - 'verb': lookup for verb only.
            - 'noun': look up for nouns.
            - 'unknown': the word is not alayzed, then search for unvocalized word.
            - '': look for voaclize word without type
        @param text:vocalized word.
        @type text: unicode.
        @param word_type: the word type can take 'verb', 'noun', 'unknwon', ''.
        @type word_type: unicode.        
        @return: list of dictionary entries IDs.
        @rtype: list.
        """
        idlist = []
        # strip the last haraka from the text to ensure the search
        #
        if araby.is_haraka(text[-1:]):
            text = text[:-1]
        # homogoneize with word typography
        # strip all fatha before alef into 
        text = re.sub(araby.FATHA+araby.ALEF, araby.ALEF, text)
        if word_type == 'unknown':
            sql  =  u"select * FROM %s WHERE unvocalized='%s'" % (
            self.table_name, text)
        else:
            sql  =  u"select * FROM %s WHERE vocalized='%s'" % (
            self.table_name, text)            
            if word_type == 'verb':
                sql += " AND word_type='verb' "
            elif word_type == 'noun':
                sql += " AND word_type!='verb' "
        try:
            self.cursor.execute(sql)
        except sqlite.OperationalError:
            print "Fatal Error can't execute query: file: wordfrequencydictionary"
            return []
        if self.cursor:
            # return self.curser.fetchall()
            for row in self.cursor:
                idlist.append(row)
        return idlist

    def get_freq(self, text, word_type = ''):
        """
        return the word frequency from the in the dictionary
        @param text:vocalized word.
        @type text: unicode.
        @param word_type: the word type can take 'verb', 'noun', 'unknwon', ''.
        @type word_type: unicode.        
        @return: word freq.
        @rtype: integer.
        """
        idlist = []
        #if araby.is_haraka(text[-1:]): text = text[:-1]
        idlist = self.lookup(text, word_type)
        # if there are many take the first
        #~print text.encode('utf8'), word_type, len (idlist)
        if idlist:
            #~freq = self.get_attrib_by_id(idlist[0], u'freq')
            freq = idlist[0]['freq']
            #~print text.encode('utf8'), word_type, freq
            return freq 
        else: 
            return 0
def mainly():
    """
    main test
    """
    #ToDo: use the full dictionary of arramooz
    WORDFREQ_DICTIONARY_INDEX = {
    u'id':0, # id
    u'vocalized':1, # the vocalized word
    u'unvocalized':2, # the unvocalized form
    u'word_type':3, # the word frequency
    u'freq':4, # the word class
    u'future_type':5, # the haraka for verb    
    #u'trans':5, # translation
    }
    #from   dictionaries.verb_dictionary  import *
    mydict = WordFreqDictionary('wordfreq', WORDFREQ_DICTIONARY_INDEX)
    wordlist = [u"صلاة", u'كرة', u"قَطَرً", u"أَرْض"]
    
    for word in wordlist:
        print "jjjjjjjj"
        print "word freq", mydict.get_freq(word)
        idlist = mydict.lookup(word)
        #~print "id list", idlist
        for idf in idlist:
            print 'frequency', idf['freq']
            print idf
   
#Class test
if __name__  ==  '__main__':
    mainly()

