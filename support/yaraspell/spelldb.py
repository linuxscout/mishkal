#!/usr/bin/python
# -*- coding = utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        spelldb
# Purpose:     Database class for Arabic spellchecker
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     2015-03-30
# Copyright:   (c) Taha Zerrouki 2015
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
Database class for Arabic spellchecker
"""
import os
import sys
sys.path.append("../lib")
if __name__  ==  '__main__':
  sys.path.append('../')  
import sqlite3 as sqlite
#~ FILE_DB_SPELL = os.path.join(os.path.dirname(os.path.realpath(__file__)), u"../../data/spellcheck.sqlite")
FILE_DB_SPELL =  u"data/spellcheck.sqlite"
import pyarabic.araby as araby

class spellDictionary:
    """
        Arabic spell dictionary Class
        Used to allow abstract acces to lexicon of arabic language, 
        can get indexed and hashed entries from the  basic lexicon
        add also, support to extract attributtes from entries
    """

    def __init__(self, databasefile = FILE_DB_SPELL):
        """
        initialisation of dictionary from a data dictionary, 
        create indexes to speed up the access.
        @param databasefile: database file name
        @type databasefile: string
        """
        # this dict contains all affixes, it will be loaded in the first time,
        # when we ask for a correction
        self.affixdict = {}
        self.db_connect = None
        # this dict contains a cache for requested words, it will be updaterequested words,7
        # in order to reduce database access
        self.stemdict = {}

        # this list contains costomized words added by users,
        self.costumdict = []
        # get the database path
        
        if hasattr(sys, 'frozen'): # only when running in py2exe this exists
            base  =  sys.prefix
        else: # otherwise this is a regular python script
            base  =  os.path.dirname(os.path.realpath(__file__))
        self.file_path = os.path.join(base, databasefile)
        
        if os.path.exists(self.file_path):
            try:
                self.db_connect  =  sqlite.connect(self.file_path)
                self.db_connect.row_factory  =  sqlite.Row                 
                self.cursor  =  self.db_connect.cursor()
            except IOError:
                print "Fatal Error Can't find the database file", self.file_path

        else:
            print u" ".join(["Inexistant File", self.file_path, " current dir ",
             os.curdir]).encode('utf8')
            sys.exit()
    def __del__(self):
        """
        Delete instance and close database connection
        
        """
        if self.db_connect:
            self.db_connect.close()
    def __load_affix(self,):
        """
        load affix form data base into self.affixdict, to speed up search
        """
        sql  =  u"select * FROM affix"
        try:
            self.cursor.execute(sql)
        except sqlite.OperationalError:
            print "Fatal Error can't execute query: file: %s"%self.file_path
            return []
        if self.cursor:
            # get one row 
            for row in   self.cursor:
                   self.affixdict[row["affix"]] = row["flag"]  

            #print "affix", self.affixdict

    def __load_costum(self,):
        """
        load costum dictionary form data base into self.costumdict, to speed up search
        """
        sql  =  u"select * FROM costum"
        try:
            self.cursor.execute(sql)
        except sqlite.OperationalError:
            print "Fatal Error can't execute query: file: %s on costum"%self.file_path
            return []
        if self.cursor:
            # get one row 
            for row in   self.cursor:
                   self.costumdict.append(row["word"] )

    def lookup(self, word, stem, affix):
        """
        look up for word in the dictionary
        @param word: given word.
        @type word: unicode.
        @param stem: the stemmed word.
        @type stem: unicode.
        @param affix: the stemmed word.
        @type affix: unicode.       
        @return: True if exists.
        @rtype: Boolean.
        """
    
        if not self.costumdict:
            self.__load_costum()
        # test if the word is a costumed word
        if word in self.costumdict:
            return True
        if not self.affixdict:
            self.__load_affix()

        # the affix dict is not loaded, we load it 
        # if the affix dict is loaded, look up for the input affix in the dict
        flag = self.affixdict.get(affix, "")
        #print (u"flag '%s' '%s' '%s'" %(flag, affix, stem )).encode('utf8')
        if not flag:
            return False
        flags = self.stemdict.get(stem, [])

        if not flags:
            # if the stem if not looked up previously, let lookup for it a onc
            sql2  =  u"select * FROM words WHERE stem='%s'" % stem
            try:
                self.cursor.execute(sql2)
            except sqlite.OperationalError:
                print "Fatal Error can't execute query: file: %s"%self.file_path
                return []
            if self.cursor:
                # get one row 
                itemlist = []
                for row in   self.cursor:
                       itemlist.append(row)  
                #print itemlist  
                if not  itemlist:
                    self.stemdict["stem"] = [] # stem doesn't exist
                    return False 
                # extract flags 
                flags = itemlist[0]["flags"].split(";")
                # save data in stemdict to speed up future lookup
                self.stemdict["stem"] = flags
            if flag in flags:
                return True
            else:
                return False
        return False


    def add_to_custom(self, word):
        """
        Add a new word to custom dictionary
        @param word: the correct word to be added to custom dictionary
        @type word: unicode
        """
        self.cursor.execute.execute(u'INSERT OR IGNORE INTO costum (word) VALUES (?)', (word))

def mainly():
    """
    main test
    """
    sp = spellDictionary()
    afflist = [u"-", u'ال-ات', ]
    stemlist = [u"كلب", u'كلم', ]    
    for stem, aff in zip(stemlist, afflist):
        test = sp.lookup(stem, aff)
        print u"\t".join(["affix", aff, stem, str(test)]).encode('utf8')
   
#Class test
if __name__  ==  '__main__':
    mainly()

