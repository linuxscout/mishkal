#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  refactor.py
#  
#  Copyright 2014 zerrouki <zerrouki@majd>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 
from syn_const import *
tab=[
KanaSisters_LIST,
RAFE3_LIST,
JAR_LIST,
JAZEM_LIST,

VERB_NASEB_LIST,
VERB_RAFE3_LIST,
NOUN_NASEB_LIST,
VERBAL_FACTOR_LIST,

CONDITION_FACTORS,

DIRECT_JAR_LIST,
DIRECT_JAZEM_LIST,
DIRECT_VERB_NASEB_LIST,
DIRECT_VERB_NASEB_LIST,

DIRECT_VERB_RAFE3_LIST,
DIRECT_NOUN_NASEB_LIST,
DIRECT_VERBAL_FACTOR_LIST,
DIRECT_NOMINAl_FACTOR_LIST,

DIRECT_RAFE3_LIST,
]

tags={
    "KanaSisters_LIST" :"KS",
    "RAFE3_LIST" : "NR",
    "JAR_LIST" : "NJ",
    "JAZEM_LIST" : "VJ",

    "VERB_NASEB_LIST" : "VN",
    "VERB_RAFE3_LIST" : "VR",
    "NOUN_NASEB_LIST" : "NN",
    "VERBAL_FACTOR_LIST" : "VF",

    "CONDITION_FACTORS" : "CF",

    "DIRECT_JAR_LIST" : "DNJ",
    "DIRECT_JAZEM_LIST" : "DVN",
    "DIRECT_VERB_NASEB_LIST" : "DVN",

    "DIRECT_VERB_RAFE3_LIST" : "DVR",
    "DIRECT_NOUN_NASEB_LIST" : "DNN",
    "DIRECT_VERBAL_FACTOR_LIST" : "DVF",
    "DIRECT_NOMINAl_FACTOR_LIST" : "DNF",

    "DIRECT_RAFE3_LIST" : "DNR",
}

import repr as reprlib
class ArabicRepr(reprlib.Repr):
    """ Unicode representation"""
    def repr_unicode(self, obj, level):
        "Modify unicode display "
        return u"u'%s'" % obj
utf8repr = ArabicRepr()
from  syn_const import *
import sys
sys.path.append('../')
import pyarabic.araby as araby
factor_table = {}
def main():
    for table in tags.keys():
        for word in eval(table):
            word_nm = araby.strip_tashkeel(word)
            if not word_nm in factor_table:
                factor_table[word_nm]={word:[tags.get(table, ""),], }
            else:
                if not word in factor_table[word_nm]:
                    factor_table[word_nm][word]=[tags.get(table, ""), ]
                else:
                    factor_table[word_nm][word].append(tags.get(table, ""))
                    
    for item in factor_table:
        print (u"u'%s':"%item).encode("utf8"), utf8repr.repr(factor_table[item]).encode('utf8'), ','

if __name__ == '__main__':
    main()

