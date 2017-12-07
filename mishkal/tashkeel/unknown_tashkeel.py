#!/usr/bin/python 
# -*- coding = utf-8 -*- 
#---------------------------------------------------------------------
# Name:        tashkeel 
# Purpose:     Arabic automatic vocalization. # 
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com) 
# Created:     2015-03-25
#  Copyright:   (c) Taha Zerrouki 2011 # Licence:     GPL 
#---------------------------------------------------------------------
"""
    Arabic Tashkeel Class of unkonwn words, based on wordlist
"""
import sys
sys.path.append('../lib')
sys.path.append('../')
import re
import unknown_const
import pyarabic.araby as araby
#debug = True
debug = False
class UnknownTashkeel:
    """
        Unknown Arabic Tashkeel Class
    """
    def __init__(self):
        pass
    def lookup(self, word):
        """
        return a vocalized form of an unknown word, from a word list
        """
        return unknown_const.Table.get(word, vocalize_foreign(word))
		
def vocalize_foreign(word):
    """
    vocalize a foreign names written in arabic
    @param word: given word
    @type  word:  unicode
    @return: the vocalized word
    @rtype: unicode
    """
    marks =[]
    previous = ""
    for c in word:
        if previous and not previous == araby.ALEF:
            #--------- add Harakat before letter
            if  c in (araby.ALEF, araby.ALEF_MAKSURA, araby.TEH_MARBUTA,):
                marks.pop()
                marks.append(araby.FATHA)
            elif c in (araby.WAW, araby.WAW_HAMZA):
                marks.pop()
                marks.append(araby.DAMMA)
            elif  c in( araby.YEH , araby.YEH_HAMZA ):
                marks.pop()
                marks.append(araby.KASRA)
        #--------- add Harakat before letter
        if c in (araby.ALEF_HAMZA_BELOW):
                marks.append(araby.KASRA)
        elif previous in (araby.ALEF_HAMZA_BELOW, araby.ALEF_HAMZA_ABOVE):
                marks.append(araby.SUKUN)
        elif previous in (araby.ALEF, araby.YEH, araby.WAW):
                if c == araby.YEH_HAMZA : 
                    marks.append(araby.KASRA)
        else:
                marks.append(araby.NOT_DEF_HARAKA)
        previous = c        
    #print len(word) ,len(marks)
    #print marks
    return araby.joint(word, u"".join(marks))
          
