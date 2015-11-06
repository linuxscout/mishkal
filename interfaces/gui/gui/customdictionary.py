#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import re
import sys
sys.path.append('../lib/')
import pyarabic.araby as araby 
class CustomizedDictionary:
    """
    Class of customized words added by users for unrecognized word"""
    def __init__(self):
        self.filename = "/tmp/customfile.txt";
        self.dictio = {}
        self.cdfile = False
        try:
            #~if os.path.exists(self.filename):
            self.cdfile = open(self.filename, "a+")
        except: 
            print "loading: Can't open custom dictionary"                
        if self.cdfile:
            line = (self.cdfile.readline()).decode('utf8')
            while line:
                items = line.strip("\n").split("\t");
                if len(items)>=2:
                    self.dictio[items[0]] = items[1].split(":")
                line = (self.cdfile.readline()).decode('utf8')
            self.cdfile.close()



        
    def lookup(self, word):
        """
        look up for a vocalization given by user for unrecongnized words
        @return: vocalized word
        @rtype: list of unicode
        """
        word = araby.strip_tashkeel(word)
        if word in self.dictio:
            return self.dictio[word]
        else:
            return [word, ]
    def add(self, word):
        """
        add a new vocalization given by user for unrecongnized word
        @return: vocalized word
        @rtype: none
        """
        word_nm = araby.strip_tashkeel(word)
        if word_nm not in self.dictio:
            self.dictio[word_nm] = [word, ]
        else:
            if word not in self.dictio[word_nm]:
                self.dictio[word_nm].append(word)
        try:
            self.cdfile = open(self.filename, "a+")
            text = u"%s\t%s\n"%(word_nm, u':'.join(self.dictio[word_nm]))
            self.cdfile.write(text.encode('utf8'))
            self.cdfile.close()            
        except:
            print "updating:can't update cutom dictionary'"
    def __del__(self,):
        """
        When the object is deleted, update dictionnary
        """
        print "deleting custom dictionary"
        try:
            self.cdfile = open(self.filename, "w")
            for  word_nm in self.dictio:
                text = u"%s\t%s\n"%(word_nm, u':'.join(self.dictio[word_nm]))
                self.cdfile.write(text.encode('utf8'))
            self.cdfile.close()
        except:
            print "closing: Can't open dictionary file for update'"
        #~for  word_nm in self.dictio:
            #~text = u"%s\t%s"%(word_nm, u':'.join(self.dictio[word_nm]))
            #~self.cdfile.write(text)
        #~self.cdfile.close()            
if __name__ == '__main__':
    cd = CustomizedDictionary()
    cd.add(u"سَلامٌ")
    cd.add(u"سلامٍ")
    cd.add(u"سلامً")
    cd.add(u"سُلام")
    cd.add(u"عبيِرٌ")
    print cd.lookup(u'سلام')
