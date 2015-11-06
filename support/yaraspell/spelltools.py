#!/usr/bin/python 
# -*- coding: utf-8 -*-
# Name:        spelltools
# Purpose:     functions and tools for Arabic spellchecker
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com) 
# Created:     2015-03-25
# Copyright:   (c) Taha Zerrouki 2015
# Licence:     GPL 
# Source : http://norvig.com/spell-correct.html How to Write a Spelling Corrector, Peter Norvig (GPL)
#---------------------------------------------------------------------

"""
    Arabic spell checker functions 
"""
import re
from collections import Counter
alphabet = u'ذضصثقفغعهخحجدطكمنتالبيسشظزوةىرؤءئأإآ'
forbiden_bigrams=u"""هغ
هإ
هأ
هء
هخ
هح
أء
ىع
ىظ
ىغ
ىر
ىذ
ىس
ىز
ىص
ىش
ىط
ىض
ىة
ىب
ىث
ىت
ىح
ىج
ىد
ىخ
ىأ
ىآ
ىإ
ىؤ
ىا
ىئ
ىى
ىو
ىي
ىف
ىك
ىق
ىم
ىل
ىه
ىن
حء
قإ
حأ
قخ
قغ
حخ
يإ
مإ
ؤئ
ؤؤ
ؤإ
ؤآ
ؤأ
ؤء
ؤغ
ؤظ
ؤع
ؤض
ةع
ةظ
ةغ
ةر
ةذ
ةس
ةز
ةص
ةش
ةط
ةض
ةة
ةب
ةث
ةت
ةح
ةج
ةد
ةخ
ةء
ةأ
ةآ
ةإ
ةؤ
ةا
ةئ
ةى
ةو
ةي
ةف
ةك
ةق
ةم
ةل
ةه
ةن
جإ
جء
ظخ
اآ
شض
شث
شإ
اى
نء
نإ
آإ
آا
آآ
آأ
آض
آظ
آع
دإ
دظ
دط
دض
دص
دذ
إة
إإ
إؤ
إا
إئ
إء
إأ
إآ
قء
إى
ظث
ظد
ظج
ظح
ظأ
ظء
تإ
تء
عغ
غح
غخ
غؤ
غإ
غئ
غء
غآ
غأ
غع
غغ
حإ
حئ
حع
حغ
ذز
ذس
ذض
ذط
ذش
ذص
ذغ
ذظ
ذإ
ذث
ثح
ثظ
صظ
صش
صض
صذ
صس
صز
صج
صث
صإ
صء
صآ
ظإ
ظز
ظس
ظذ
ظض
ظط
ظش
ظص
ثإ
ظق
ثس
ثز
ثذ
ثط
ثض
ثص
ثش
ئء
ئآ
ئأ
ئؤ
ئإ
ئئ
سظ
سز
سض
سص
سث
سإ
ءء
ءإ
ءؤ
ءئ
ءث
ءح
ءج
ءد
ءخ
ءر
ءذ
ءس
ءز
ءص
ءش
ءط
ءض
ءع
ءظ
ءغ
خح
خء
خأ
خإ
خئ
خظ
خغ
ءف
ءق
ضء
ضإ
ضث
ضذ
ضز
ضس
ضش
ضص
رإ
عح
عخ
عء
عأ
عآ
عإ
عؤ
عئ
زش
زص
زض
زذ
زظ
زإ
زث
طإ
طث
طض
طص
طذ
طظ
""".split("\n")
def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)
def getbigrams(word):
    """
    extract all bigrams from the word with stats
    """
    text = " "+word+" "
    bigrams = Counter(x+y for x, y in zip(*[text[i:] for i in range(2)]))
    return bigrams

def is_valid(word):
    # test if the word is arabic form
    if not araby.is_arabicword(word):
        return False
    # test some cases 
    # the teh marbuta is before any arabic letter
    # the hamza online is after 
    bigrams = getbigrams(word)
    for bi in bigrams:
        if bi in forbiden_bigrams:
            return False
    return True
import pyarabic.araby as araby

LETTER_MAP={
araby.ALEF_HAMZA_BELOW :u"a",
araby.ALEF:u"a",
araby.ALEF_HAMZA_ABOVE:u"a",
araby.ALEF_MADDA:u"a",

araby.HAMZA :u"e",
araby.WAW_HAMZA:u"e",
araby.YEH_HAMZA:u"e",

araby.ZAH:u"d",
araby.DAD:u"d",

araby.DAL:u"c",
araby.THAL:u"c",

araby.TEH_MARBUTA:u"t",
araby.TEH:u"t",

araby.TEH_MARBUTA:u"t",
araby.HEH:u"t",


araby.ALEF_MAKSURA:u"y",
araby.YEH:u"y",
}
def normalize(word):
    new_word =[]
    for c in word:
        new_word.append(LETTER_MAP.get(c,c))
    return u"".join(new_word)



"""
    Arabic spell checker distance
"""
"""
TRY	ًٍذضصثقفغعهخحجدطكمنتالبيسشظزوةىرؤءئأإآ
KEY ضصثقفغعهخحجد¦شسيبلاتنمكط¦ئءؤرﻻىةوزظ¦ضشئ¦صسء¦ثيؤ¦قبر¦فلﻻ¦غاى¦عتة¦هنو¦خمز¦حكظ¦جط

MAP 16
MAP ضص
MAP طظ
MAP ضظ
MAP فق
MAP غع
MAP خحج
MAP اأإآ
MAP أءؤئ
MAP ةه
MAP ةت
MAP يى
MAP ثت
MAP زر
MAP دذ
MAP ظز
MAP زذ

REP  80
REP ^إست است
REP إ ا
REP اا ا_ا
REP ى$ ي
REP ض ظ
REP ظ ض
REP ه$ ة
"""
import sys
sys.path.append("../lib")
import re
import pyarabic.araby as araby

LETTER_MAP={
araby.ALEF_HAMZA_BELOW :u"a",
araby.ALEF:u"a",
araby.ALEF_HAMZA_ABOVE:u"a",
araby.ALEF_MADDA:u"a",

araby.HAMZA :u"e",
araby.WAW_HAMZA:u"e",
araby.YEH_HAMZA:u"e",

araby.ZAH:u"d",
araby.DAD:u"d",

araby.DAL:u"c",
araby.THAL:u"c",

araby.TEH_MARBUTA:u"t",
araby.TEH:u"t",

araby.TEH_MARBUTA:u"t",
araby.HEH:u"t",


araby.ALEF_MAKSURA:u"y",
araby.YEH:u"y",
}
LIKEHOOD ={
# phonetic
"phone":[
u"ظض",
u"ضظ",
#u"تة",
u"أا",
u"ءأ",
u"ةت",
u"أآ",
u"إآ",
u"اآ",
u"أإ",
u"اإ",
u"اأ",
u"ؤئ",
u"ءئ",
u"أئ",
u"ءؤ",
u"أؤ",
u"أء",
u"ظز",
u"زذ"],

#graphic
'graph':[
u"شس",
u"ضص",
u"ضص",
u"طظ",
u"فق"
u"غع",
u"ةه",
u"يى",
u"ثت",
u"زر",
u"دذ",
u"حج",
u"خج",
u"خح",
], 
#keyboard
"key":[
u"ضش", u"شئ",
u"صس", u"سء",
u"ثي",u"يؤ",
u"قب", u"بر",
u"فل", u"لﻻ",
u"غا", u"اى",
u"عت", u"تة",
u"هن", u"نو",
u"خم", u"مز",
u"حك", u"كظ",
u"جط",
u'ضص',
u'صث',
u'ثق',
u'قف',
u'فغ',
u'غع',
u'عه',
u'هخ',
u'خح',
u'حج',
u'جد',

u'شس',
u'سي',
u'يب',
u'بل',
u'لا',
u'ات',
u'تن',
u'نم',
u'مك',
u'كط',


u'ئء',
u'ءؤ',
u'ؤر',
u'رﻻ',
u'ﻻى',
u'ىة',
u'ةو',
u'وز',
u'زظ',
]
}
def find_bigrams(input_list):
  bigram_list = []
  for i in range(len(input_list)-1):
      bigram_list.append((input_list[i], input_list[i+1]))
  return bigram_list
def normalize(word):
    new_word =[]
    for c in word:
        new_word.append(LETTER_MAP.get(c,c))
    return u"".join(new_word)
def like(c1, c2, mode = "phone"):
    """
    test likehood between two letters
    """
    c1c2 = "".join([c1,c2])
    c2c1 = "".join([c2,c1])
    return (c1c2 in LIKEHOOD[mode]) or (c2c1 in LIKEHOOD[mode]) 
KEYBOARD_DISTANCE  = 3
PHONETIC_DISTANCE  = 1
GRAPHIC_DISTANCE  = 2
REPLACE_DISTANCE = 4
def phonetic_distance(word1, word2):
    """
    calculate distan between two words
    """
    if len(word1) != len(word2):
        return min(len(word1), len(word2)) 
    else:
        phono_distance = 0
        for c,d in zip(word1, word2):
            if like(c,d, "phone") :
                phono_distance += PHONETIC_DISTANCE
            elif like(c,d, "graph") :
                phono_distance += GRAPHIC_DISTANCE
            elif like(c,d, "key") :
                phono_distance += KEYBOARD_DISTANCE
            elif c != d :
                phono_distance += REPLACE_DISTANCE
    return phono_distance               
                
            
def mainly():
    """
    main test
    """
    words =u"""ضلام ألام ضلال لام ظلام ضام غلام إلام نلام هلام ضخام سلام ملام ضلا ضمام تلام علام يلام ضلان كلام ضلتم""".split(" ")
    tests = u"""إنتظار	انتظار
الإستعمال	الاستعمال
الضلام	الصلام, الغلام, العلام, الحلام, الجلام, التلام, البلام, السلام, الظلام, الإلام, الآلام, الضمام, الضلال
يستخدمو	مستخدمو, يستخدمه, يستخدمك, يستخدمن
شلام	صلام, غلام, علام, حلام, جلام, تلام, سلام, ظلام, ألام, إلام, آلام, شهام, شمام, شيام, شلجم, شلتم, شلاق, شلاف, شلاه, شلاك, شلال
"""
    source = u"ضلام"
    normsource = normalize(source)
    normlist = [normalize(word) for word in words]
    for word in words:
        print u"\t".join([word, normalize(word)]).encode("utf8")
    words_dist = [(x, phonetic_distance(source,x)) for x in words]
    for word in words:
        print u"\t".join([word, str(phonetic_distance(source,word))]).encode("utf8")
    condidates = sorted(words, key=lambda x: phonetic_distance(source,x))
    print "-- ordred by phonetic ------------- "
    print u"\t".join(condidates)
    condidates = filter(lambda w: normalize(w) == normsource, words)
    print "condidates", u"\t".join(condidates).encode('utf8')
if __name__ == "__main__":
    mainly()
