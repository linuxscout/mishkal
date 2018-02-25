#!/usr/bin/python
# -*- coding  =  utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        stemmedAffix
# Purpose:     representat affix data analyzed given by morphoanalyzer  Qalsadi
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     19-09-2012
# Copyright:   (c) Taha Zerrouki 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
stemmedAffix represents the data resulted from the morpholocigal analysis
"""
import sys
sys.path.append('../lib/')
import pyarabic.araby as araby


#~import qalsadi.analex_const
class StemmedAffix:
    """
    stemmedAffix represents the data resulted from the morpholocigal analysis
    """

    def __init__(self, result_dict=None):

        # extracted affix attributes
        self.procletic = u""  # the syntaxic pprefix called procletic
        self.prefix = u""  # the conjugation or inflection prefix
        self.suffix = u""  # the conjugation suffix of the word
        self.encletic = u""  # the syntaxic suffix
        self.tag_type = 0  # the word type used with affix
        self.tag_tense = 0
        self.tags = u""
        self.tag_break = False
        # tags of affixes and tags extracted form lexical dictionary

        if result_dict:
            aff = result_dict.get('affix', [])
            if aff:
                self.procletic = aff[0]
                self.prefix = aff[1]
                self.suffix = aff[2]
                self.encletic = aff[3]
            self.affix = u'-'.join(
                [self.procletic, self.prefix, self.suffix, self.encletic])
            self.tags = result_dict.get('tags', u'')
            #word type
            self.tag_type = self.__get_type(result_dict.get('type', u''))
            if self.is_verb():
                self.tag_tense = self.__get_tense(
                    result_dict.get('tense', u''))
                #~print "tense:",   result_dict.get('tense', u'').encode('utf8')
        # grouped attributes
        self.tag_number = self.__get_number()  #number (single, dual, plural)
        # majrour, majzoum, marfou3, mansoub, mabni
        self.tag_inflect = self.__get_inflect()
        self.tag_gender = self.__get_gender()

        # not noun or stopword
        self.tag3rdperson = False
        self.tag1stperson = False
        self.tag_defined = False
        self.tag_tanwin = False
        self.tag_jar = False
        self.tag_istfham = False
        # calculated  attributes
        if self.is_verb():
            self.tag3rdperson = self.__is3rdperson()
            self.tag1stperson = self.__is1stperson()
        else:
            if self.is_noun():
                self.tag_defined = self.__is_defined()
                self.tag_tanwin = self.__is_tanwin()
        # used for nouns and stop words
        self.tag_jar = self.__has_jar()
        self.tag_added = self.__is_added()
        #~self.tag_feminin         =  self.__is_feminin()
        self.tag_break = self.__is_break()
        self.tag_3tf = self.__is_3tf()
        self.tag_istfham = self.__has_istfham()

    #  tags extracted from word dictionary
    #--------------------------

    #  tags extracted from affixes
    #--------------------------
    def get_type(self, ):
        """
        Get the type form of the input word
        @return: the given type.
        @rtype: unicode string
        """
        return self.tag_type

    def get_procletic(self, ):
        """
        Get the procletic
        @return: the given procletic.
        @rtype: unicode string
        """
        return self.procletic

    def set_procletic(self, newprocletic):
        """
        Set the procletic
        @param newprocletic: the new given procletic.
        @type newprocletic: unicode string
        """
        self.procletic = newprocletic

    def has_procletic(self, ):
        """
        return True if has procletic
        @return: True if procletic not empty.
        @rtype: Boolean
        """
        return self.procletic != u''

    def get_prefix(self, ):
        """
        Get the prefix
        @return: the given prefix.
        @rtype: unicode string
        """
        return self.prefix

    def set_prefix(self, newprefix):
        """
        Set the prefix
        @param newprefix: the new given prefix.
        @type newprefix: unicode string
        """
        self.prefix = newprefix

    def get_suffix(self, ):
        """
        Get the suffix
        @return: the given suffix.
        @rtype: unicode string
        """
        return self.suffix

    def set_suffix(self, newsuffix):
        """
        Set the suffix word
        @param newsuffix: the given suffix.
        @type newsuffix: unicode string
        """
        self.suffix = newsuffix

    def get_encletic(self, ):
        """
        Get the encletic
        @return: the given encletic.
        @rtype: unicode string
        """
        return self.encletic

    def set_encletic(self, newencletic):
        """
        Set the encletic
        @param newencletic: the given encletic.
        @type newencletic: unicode string
        """
        self.encletic = newencletic

    def has_encletic(self, ):
        """
        return True if has encletic
        @return: True if encletic not empty.
        @rtype: Boolean
        """
        return self.encletic != u'' or self.prefix.startswith(u'ل')

    def __get_inflect(self, ):
        """
        Return int code of iflection state.
        the inflected cases are coded in binary like
        not defined        : 0  00000
        Invariable (mabni) : 1  00001
        marfou3            : 2  00010
        mansoub            : 4  00100
        majrour            : 8  01000
        majzoum            :16  10000
        mabni              :32 100000
        this codification allow to have two inflection for the same case,
        like feminin plural which ahve the same mark for Nasb and jar
        هذا الترمزي يسمح بتركيب حالتين إعرابيتين معا،
 مثل إعراب جمع المؤنث السالم بالكسرة في
        النصب والجر
        @return: inflection state numeric code
        @rtype: int
        """
        # غير محدد
        self.tag_inflect = 0
        # invariable
        # if verb
        if u'الماضي' in self.get_tags():
            self.tag_inflect += 1
        elif u'الأمر' in self.get_tags():
            self.tag_inflect += 1
        elif u'مؤكد' in self.get_tags():
            self.tag_inflect += 1
        # invariable noun
        elif u'مبني' in self.get_tags() and  u"مجهول" not in self.get_tags():
            self.tag_inflect += 1
        # marfou3
        if u'مرفوع' in self.get_tags():
            self.tag_inflect += 2
        # if is a imperfect and not mansoub or majzoum =>marfou3
        #ToDo:
        # use tense class instead of tag search
        elif u'مضارع' in self.get_tags() and  u'منصوب'not in self.get_tags()\
           and u'مجزوم' not in self.get_tags():
            self.tag_inflect += 2
        # mansoub
        # noun and verb
        if u'منصوب' in self.get_tags():
            self.tag_inflect += 4
        # majrour
        # noun
        if u'مجرور' in self.get_tags():
            self.tag_inflect += 8
        # a Verb, verb can't be majrour
        elif u'مجزوم' in self.get_tags():
            self.tag_inflect += 16
        return self.tag_inflect

    def __get_number(self, ):
        """
        Return the int code of the number state.
        the number cases are coded in binary like
        not defined        : 0  00000
        single  : 1  00001
        dual    : 2  00010
        plural  : 4  00100
        masculin plural: 8  01000
        feminin plural : 16 10000
        this codification allow to have two marks for the same case,
        like irregular plural and single can have the same mark
        هذا الترميز يسمح بترميز المفرد وجمع التكسير معا
        @return: get the number state .
        @rtype: int
        """
        # غير محدد
        self.tag_number = 0
        if u'مفرد' in self.get_tags():
            self.tag_number += 1
        if u'مثنى' in self.get_tags():
            self.tag_number += 2
        if u'جمع' in self.get_tags():
            self.tag_number += 4
            if u'جمع مذكر سالم' in self.get_tags():
                self.tag_number += 8
            if u'جمع مؤنث سالم' in self.get_tags():
                self.tag_number += 16
        # here the single is not defaut value
        # because it can be used as irregular plural affix
        return self.tag_number

    def __get_type(self, input_type):
        """
        Return the numeric code of word type.
        the number cases are coded in binary like
        not defined        : 0  00000
        stopword  : 1  00001
        verb    : 2  00010
        noun  : 4  00100
        this codification allow to have two types for the same case,
        like a stop word can be a noun, the correspendant code is 101
        هذا الترميز يسمح بترميز الحروف والأسماء،
        بعض الأدوات هي أسماء
        @return: numeric code of type .
        @rtype: int
        """
        # غير محدد
        self.tag_type = 0
        if not input_type:
            return 0
        if u'STOPWORD' in input_type:
            self.tag_type += 1
        if u'Verb' in input_type:
            self.tag_type += 2
        if u'Noun' in input_type:
            self.tag_type += 4
        return self.tag_type

    def __get_tense(self, input_tense):
        """
        Return the numeric code of tense.
        the number cases are coded in binary like
        not defined        : 0  00000
        past        : 1  00001
        imperfect   : 2  00010    present and future
        imperative  : 4  00100
        passive     : 8  01000
        confirmed   : 16 10000
        this codification allow to have many tense attributes for the same case,
        like a imperfect passive and confirmed, the correspendant
        code is 11010 => 26
        @param input_tense : given tense
        @type input_tense: unicode
        @return: tense numeric code .
        @rtype: int
        """
        # غير محدد
        self.tag_tense = 0
        if not input_tense:
            return 0
        if u'ماضي' in input_tense:
            self.tag_tense = 1
        elif u'مضارع' in input_tense:
            self.tag_tense = 2
        elif u'أمر' in input_tense:
            self.tag_tense = 4
        # passive
        if u'مجهول' in input_tense:
            self.tag_tense += 8
        if u'مؤكد' in input_tense:
            self.tag_tense += 16
        return self.tag_tense

    def __get_gender(self, ):
        """
        Return the int code of the gender state.
        the number cases are coded in binary like
        not defined        : 0  00000
        masculin  : 1  00001
        feminin    : 2  00010
        this codification allow to have case in the same word
        @return: get the numeric gender state .
        @rtype: int
        """
        # غير محدد
        self.tag_gender = 0
        if u'مذكر' in self.get_tags():
            self.tag_gender += 1
        if u'مؤنث' in self.get_tags():
            self.tag_gender += 2
        elif u'جمع مؤنث سالم' in self.get_tags():
            self.tag_gender += 2

        return self.tag_gender

    def __is_defined(self):
        """
        Return True if the word has the state definde.
        @return: has the state defined.
        @rtype: True/False
        """
        return u'تعريف' in self.get_tags() or u'مضاف' in self.get_tags()

    def __is3rdperson(self):
        """
        Return True if the word has the 3rd person.
        @return: has the 3rd persontense.
        @rtype: True/False
        """
        return u':هي:' in self.get_tags() or u':هو:' in self.get_tags()

    def __is1stperson(self):
        """
        Return True if the word has the 1st person.
        @return: has the 1st persontense.
        @rtype: True/False
        """
        return u':أنا:' in self.get_tags()

    def is3rdperson_masculin(self):
        """
        Return True if the word has the 3rd person.
        @return: has the 3rd persontense.
        @rtype: True/False
        """
        return u':هو:' in self.get_tags()

    def is3rdperson_fem(self):
        """
        Return True if the word has the 3rd person feminin.
        @return: has the 3rd person feminin.
        @rtype: True/False
        """
        return u':هي:' in self.get_tags()

    def __is_tanwin(self):
        """
        Return True if the word has tanwin.
        @return: has tanwin.
        @rtype: True/False
        """
        return u'تنوين' in self.get_tags()

    def __has_jar(self):
        """
        Return True if the word has a jar factor attached.
        @return: has jar.
        @rtype: True/False
        """
        return u'جر:' in self.get_tags(
        )  #or self.procletic.startswith(araby.LAM)

    def __has_istfham(self):
        """
        Return True if the word has a istfham factor attached.
        @return: has jar.
        @rtype: True/False
        """
        return u'استفهام' in self.get_tags()

    def __is_break(self):
        """
        Return True if the word has break.

        @return: is break.
        @rtype: True/False
        """
        #تكون الكلمة فاصلة
        #إذا كانت منفصلة عمّا قبلها.
        # الحالات التي تقطع
        # - حرف جر متصل
        # فاصلة أو نقطة
        if self.has_procletic() and self.has_jar():
            return True
        elif u'عطف' in self.get_tags() or araby.WAW in self.get_procletic() \
        or araby.FEH in self.get_procletic():
            return True
        elif self.__has_istfham():
            return True
        return False

    # Mixed affix and dictionary attrrubutes
    #---------------------------------------
    def __is_added(self):
        """
        Return True if the word has the state added مضاف.
        @return: has the state added.
        @rtype: True/False
        """
        return u'مضاف' in self.get_tags() or u'اسم إضافة' in self.get_tags()

    def __is_3tf(self):
        """
        Return True if the word is a plural.
        @return: is plural.
        @rtype: True/False
        """
        return u'عطف' in self.get_tags()

    def is_3tf(self):
        """
        Return True if the word is a plural.
        @return: is plural.
        @rtype: True/False
        """
        return self.tag_3tf

    #~def __is_plural(self):
    #~"""
    #~Return True if the word is a plural.
    #~@return: is plural.
    #~@rtype: True/False
    #~"""
    #~return  u'جمع' in self.get_tags()

    def get_tags(self, ):
        """
        Get the tags form of the input word
        @return: the given tags.
        @rtype: unicode string
        """
        return self.tags

    def set_tags(self, newtags):
        """
        Set the tags word
        @param newtags: the new given tags.
        @type newtags: unicode string
        """
        self.tags = newtags

    ######################################################################
    #{ Tags  Functions
    ######################################################################
    def is_stopword(self):
        """
        Return True if the word is a stop word.
        @return: is a noun.
        @rtype: True/False
        """
        return bool(self.tag_type % 2)

    def is_verb(self):
        """
        Return True if the word is a verb.
        @return: is a verb.
        @rtype: True/False
        """
        return bool(self.tag_type / 2 % 2)

    def is_noun(self):
        """
        Return True if the word is a noun.
        @return: is a noun.
        @rtype: True/False
        """
        return bool(self.tag_type / 4 % 2)

    def is_invariable(self):
        """
        Return True if the word has the state invariable (مبني).
        @return: has the state invariable.
        @rtype: True/False
        """
        return bool(self.tag_inflect % 2)

    def is_marfou3(self):
        """
        Return True if the word has the state marfou3.
        @return: has the state marfou3.
        @rtype: True/False
        """
        return bool(self.tag_inflect / 2 % 2)

    def is_mabni(self):
        """
        Return True if the word has the state mabni.
        @return: has the state mabni.
        @rtype: True/False
        """
        return self.is_invariable()

    def is_mansoub(self):
        """
        Return True if the word has the state mansoub.
        @return: has the state mansoub.
        @rtype: True/False
        """
        return bool(self.tag_inflect / 4 % 2) or self.is_invariable()

    def is_majrour(self):
        """
        Return True if the word has the state majrour.
        @return: has the state majrour.
        @rtype: True/False
        """
        return bool(self.tag_inflect / 8 % 2)  #or self.is_invariable()

    def is_majzoum(self):
        """
        Return True if the word has the state majrour.
        @return: has the state majrour.
        @rtype: True/False
        """
        return bool(self.tag_inflect / 16 % 2) or self.is_invariable()

    def is_defined(self):
        """
        Return True if the word has the state definde.
        @return: has the state defined.
        @rtype: True/False
        """
        return self.tag_defined

    def is_past(self):
        """
        Return True if the word has the tense past.
        @return: has the  tense past.
        @rtype: True/False
        """
        return bool(self.tag_tense % 2)
        #~return   u'ماضي'in self.get_tags()

    def is_present(self):
        """
        Return True if the word has the tense present.
        @return: has the  tense present.
        @rtype: True/False
        """
        return bool(self.tag_tense / 2 % 2)
        #~return  u'مضارع' in self.get_tags()

    def is_passive(self):
        """
        Return True if the word has the tense passive.
        @return: has the  tense passive.
        @rtype: True/False
        """
        return bool(self.tag_tense / 8 % 2)
        #~return  u'مجهول'in self.get_tags()

    def is3rdperson(self):
        """
        Return True if the word has the 3rd person.
        @return: has the 3rd persontense.
        @rtype: True/False
        """
        return self.tag3rdperson

    def is1stperson(self):
        """
        Return True if the word has the 1st person.
        @return: has the 1st persontense.
        @rtype: True/False
        """
        return self.tag1stperson

    def is_added(self):
        """
        Return True if the word has the state added مضاف.
        @return: has the state added.
        @rtype: True/False
        """
        return self.tag_added

    def is_tanwin(self):
        """
        Return True if the word has tanwin.
        @return: has tanwin.
        @rtype: True/False
        """
        return self.tag_tanwin

    def has_jar(self):
        """
        Return True if the word has tanwin.
        @return: has tanwin.
        @rtype: True/False
        """
        return self.tag_jar

    def has_istfham(self):
        """
        Return True if the word has istfham.
        @return: has tanwin.
        @rtype: True/False
        """
        return self.tag_istfham

    def is_break(self):
        """
        Return True if the word has break.
        @return: is break.
        @rtype: True/False
        """
        #تكون الكلمة فاصلة إذا كانت منفصلة عمّا قبلها.
        # الحالات التي تقطع
        # - حرف جر متصل
        # فاصلة أو نقطة
        return self.tag_break

    def is_feminin(self):
        """
        Return True if the word is Feminin.
        @return: is Feminin.
        @rtype: True/False
        """
        #~return self.tag_feminin
        return bool(self.tag_gender / 2 % 2)

    def is_dual(self):
        """
        Return True if the word is  dual.
        @return: is  dual.
        @rtype: True/False
        """
        #~return self.tag_dual
        return bool(self.tag_number / 2 % 2)

    def is_plural(self):
        """
        Return True if the word is a plural.
        @return: is plural.
        @rtype: True/False
        """
        #~return self.tag_plural
        return bool(self.tag_number / 4 % 2)

    def is_masculin_plural(self):
        """
        Return True if the word is  Masculin plural.
        @return: is masculin plural.
        @rtype: True/False
        """
        #~return self.tag_masculin_plural
        return bool(self.tag_number / 8 % 2)

    def is_feminin_plural(self):
        """
        Return True if the word is  Feminin plural.
        @return: is Feminin plural.
        @rtype: True/False
        """
        #~return self.tag_feminin_plural
        return bool(self.tag_number / 16 % 2)

    ######################################################################
    #{ Display Functions
    ######################################################################
    def get_dict(self, ):
        """
        get attributes dict
        """
        return self.__dict__

    def __repr__(self):
        """
        Display objects result from analysis
        @return: text
        @rtype : text
        """
        text = u"{"
        stmword = self.__dict__
        for key in stmword.keys():
            text += u"\n\t\tu'%s'  =  u'%s', " % (key, stmword[key])
        text += u'\n\t\t}'
        return text.encode('utf8')


if __name__ == "__main__":
    print("test")
    RDICT = {
        "word": "الحياة",  # input word
        "vocalized": "الْحَيَاةُ",  # vocalized form of the input word
        "procletic": "ال",  # the syntaxic pprefix called procletic
        "prefix": "",  # the conjugation or inflection prefix
        "stem": "حياة",  # the word stem
        "suffix": "ُ",  # the conjugation suffix of the word
        "encletic": "",  # the syntaxic suffix
        "tags": "تعريف::مرفوع*",
        # tags of affixes and tags extracted form lexical dictionary
        "freq": 0,  # the word frequency from Word Frequency database
        "root": "",  # the word root not yet used
        "template": "",  # the template وزن
        "type": "Noun:مصدر",  # the word type
        "original": "حَيَاةٌ",  #original word from lexical dictionary
        "syntax": "",  # used for syntaxique analysis porpos
        u'semantic': '',
    }

    #~print stmwrd
