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
import unkown_const


debug = False
class UnkownTashkeel:
    """
        Arabic Tashkeel Class
    """
    def __init__(self):
        pass
    def lookup(self, word):
        """
        return a vocalized form of an unknown word, from a word list
        """
        return unkown_const.Table.get(word, word)
        
