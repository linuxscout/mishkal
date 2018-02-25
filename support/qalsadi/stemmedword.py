#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        stemmed_word
# Purpose:     representat data analyzed given by morphoanalyzer Qalsadi
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     19-09-2012
# Copyright:   (c) Taha Zerrouki 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
stemmed_word represents the data resulted from the morpholocigal analysis
"""
import pyarabic.araby as araby
import qalsadi.stemmedaffix as stemmedaffix
GLOBAL_AFFIXES = {}

class StemmedWord:
    """
    stemmed_word represents the data resulted from the morpholocigal analysis
    """

    def __init__(self, resultdict=None):
        # given word attributes
        self.word = u"",
        #~"""input word"""
        self.vocalized = u"",
        #~"""vocalized form of the input word """
        self.unvocalized = u""

        #~"""semivocalized form of the input word without inflection mark"""
        self.semivocalized = u""

        self.tags = u"",
        #~"""tags of affixes and tags extracted form lexical dictionary"""
        self.affix_key = u'-'
        affix_tags = u""
        #~"""tags of affixes"""

        # stemmed word attributes
        self.stem = u"",
        #~"""the word stem"""

        # _original word attributes from dictionary.
        self.original_tags = u"",
        #~""" tags extracted form lexical dictionary"""
        self.freq = 0,  # the word frequency from _word _frequency database
        self.type = u"",  # the word type
        self.original = u""  #original word from lexical dictionary
        self.tag_regular = True  # the stemmed word is regular or irregular سالم أو تكسير
        # تستعمل في الجمع
        if resultdict:

            self.word = resultdict.get('word', u'')
            self.vocalized = resultdict.get('vocalized', u'')
            self.semivocalized = resultdict.get('semivocalized', u'')
            self.stem = resultdict.get('stem', u'')
            self.affix = u'-'.join(resultdict.get('affix', []))

            affix_tags = resultdict.get('tags', u'')
            self.tags = u':'.join([
                resultdict.get('tags', u''),
                resultdict.get('originaltags', u'')
            ])
            self.freq = resultdict.get('freq', u'')
            self.type = resultdict.get('type', u'')
            self.original = resultdict.get('original', u'')
            # tags of stop word
            # action: the word role
            self.action = resultdict.get('action', u'')
            # object_type: the next word type if is submitted to the action
            # the type of next word needed by the actual stop word
            self.object_type = resultdict.get('object_type', u'')
            self.need = resultdict.get('need', u'')
            self.tag_type = self.__get_type(resultdict.get('type', u''))

        self.affix_key = self.affix

        # init
        self.tag_added = False
        self.tag_initial = False
        self.tag_transparent = False
        self.tag_mamnou3 = False
        self.tag_break = False
        self.tag_voice = False
        self.tag_mood = False
        self.tag_confirmed = False
        self.tag_pronoun = False
        self.tag_transitive = False
        self.tag_person = self.__get_person(resultdict.get('person', None))
        #~ x = resultdict.get('gender', None)
        #~ if x : print x.encode('utf8'), self.word.encode('utf8')
        self.tag_original_number = resultdict.get('number', None)
        self.tag_original_gender = resultdict.get('gender', None)
        self.tag_number = self.__get_number()
        self.tag_gender = self.__get_gender()
        if self.is_noun():
            self.tag_added = self._is_added()
            self.tag_mamnou3 = self._is_mamnou3()
            # grouped attributes
            self.affix_key = u'|'.join([self.affix_key, self.word])
        if self.is_verb():
            self.tag_tense = resultdict.get('tense', u'')
            self.tag_voice = resultdict.get('voice', u'')
            self.tag_mood = resultdict.get('mood', u'')
            self.tag_confirmed = resultdict.get('confirmed', u'')
            self.tag_pronoun = resultdict.get('pronoun', u'')
            self.tag_transitive = resultdict.get('transitive', False)
            #print ("stemmedword", self.tag_transitive)

            # #if the word is verb: we must add the tense and pronoun
            # to the affixkay.
            # #because for verbs, same affixes don't give same tags
            self.affix_key = u'|'.join([self.affix_key, affix_tags])
        if self.is_stopword():
            # #if the word is a stop word: we must add the word
            # to the affixkay.
            # #because for stopwords, same affixes don't give same tags
            self.affix_key = u'|'.join([self.affix_key, self.word])
        if self.affix_key not in GLOBAL_AFFIXES:
            GLOBAL_AFFIXES[self.affix_key] = stemmedaffix.StemmedAffix(
                resultdict)
            #~ self.tag_transitive     ='y' in self.get_tags()
        if self.is_stopword():
            self.tag_transparent = self._is_transparent()
        self.tag_initial = self._is_initial()

        #redandente
        self.tag_break = self._is_break()

    #  tags extracted from word dictionary
    #--------------------------
    def _is_initial(self):
        """Return True if the word mark the begin of next sentence."""
        word = self.get_word()
        return word == u"" or word[0] in (u'.', u'?', u'', u':')

    def __get_number(self):
        """
        Return the int code of the number state.
        the number cases are coded in binary like
        not defined        : 0  00000
        single  : 1  00001
        dual    : 2  00010
        plural  : 4  00100
        masculin plural: 8  01000
        feminin plural : 16 10000
        irregular plural : 32 100000
        this codification allow to have two marks for the same case,
        like irregular plural and single can have the same mark
        هذا الترميز يسمح بترميز المفرد وجمع التكسير معا
        @return: get the number state .
        @rtype: int
        """
        # غير محدد

        self.tag_number = 0
        # إذا لم يكن في الزوائد ما يدل على الجمع
        if not self._affix_is_plural() and not self._affix_is_dual():
            if u'مفرد' in self.get_tags() or (
                    u'مفرد' in self.tag_original_number):
                self.tag_number += 1
        if not self._affix_is_plural():
            if u'مثنى' in self.get_tags():
                self.tag_number += 2
        if self._affix_is_plural() or u'جمع' in self.get_tags() or (
                u'جمع' in self.tag_original_number):
            self.tag_number += 4
            if u'جمع مذكر سالم' in self.get_tags():
                self.tag_number += 8
            if u'جمع مؤنث سالم' in self.get_tags():
                self.tag_number += 16
            if u'جمع تكسير' in self.tag_original_number:
                self.tag_number += 32
        # if all previous case not used
        if self.tag_number == 0:
            self.tag_number += 1
        return self.tag_number

    def __get_person(self, given_person_tag=""):
        """
        Return the int code of the person state.
        the person cases are coded in binary like
        not defined        : 0  00000
        first  : 1  00001
        second    : 2  00010
        third  : 4  00100
        @return: get the person state .
        @rtype: int
        """
        self.tag_person = 0
        #~ print self.get_tags().encode('utf8')
        if u'متكلم' in self.get_tags() or (given_person_tag
                                           and u'متكلم' in given_person_tag):
            self.tag_person += 1
        if u'مخاطب' in self.get_tags() or (given_person_tag
                                           and u'مخاطب' in given_person_tag):
            self.tag_person += 2
        if u'غائب' in self.get_tags() or (given_person_tag
                                          and u'غائب' in given_person_tag):
            self.tag_person += 4
        if not self.tag_person:
            self.tag_person = 4 
        #~ print self.tag_person
        #tempdislay
        #~ print self.word.encode('utf8'), self.get_tags().encode('utf8'), self.tag_person
        #~ if given_person_tag: print "--",given_person_tag.encode('utf8')
        return self.tag_person

    def __get_regular(self, ):
        """
        Return the int code of the regular state.
        the regular cases are coded in binary like
        regular   : 1
        irregular  : 0
        @return: get the regular state .
        @rtype: int
        """
        # غير محدد
        self.tag_regular = True
        if u'جمع تكسير' in self.tag_original_number:
            self.tag_regular = False

        return self.tag_regular

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
        if (u'Noun' in input_type or u'اسم' in input_type
                or u'مصدر' in input_type):
            self.tag_type += 4
        if u'مصدر' in input_type:
            self.tag_type += 8
        # adjective
        #~ print "tags", self.get_word().encode('utf8'), self.get_tags().encode('utf8')
        if (u'صفة' in input_type or u'اسم مفعول' in input_type
                or u'اسم فاعل' in input_type or u'صيغة مبالغة' in input_type
                or u'فاعل' in input_type or u'اسم تفضيل' in input_type
                or u'منسوب' in self.get_tags()
                #~ or u'منسوب' in self.get_affix_tags()
                or u'منسوب' in input_type or "adj" in input_type):
            self.tag_type += 16
            #~ print "is adj", self.get_word().encode('utf8')
        if u'noun_prop' in input_type:
            self.tag_type += 32
        if u'POUNCT' in input_type:
            self.tag_type += 64
        if u'NUMBER' in input_type:
            self.tag_type += 128
        #~ print self.tag_type
        return self.tag_type

    def __get_gender(self, input_gender=""):
        """
        Return the int code of the gender state.
        the number cases are coded in binary like
        not defined        : 0  00000
        masculin  : 1  00001
        feminin    : 2  00010
        this codification allow to have case in the same word
        @return: get the numeric sex state .
        @rtype: int
        """
        # غير محدد
        self.tag_gender = 0
        # إذا كان الاسم مذكرا وغير  متصل بما يؤنثه
        if not self._affix_is_feminin():
            if u'مذكر' in self.tag_original_gender:
                self.tag_gender = 1
            elif (u'اسم فاعل' in self.get_type()
                  or u'اسم مفعول' in self.get_type()
                  or u'صفة مشبهة' in self.get_type()):
                self.tag_gender = 1
            # يكون المصدر مذكرا إذا لم يحتوي على تاء مربوطة و لم يكن جمع تكسير
            elif (u'مصدر' in self.get_type()
                  and araby.TEH_MARBUTA not  in self.get_original()
                  and u'جمع' not in self.tag_original_number):
                self.tag_gender = 1

        #يتحدد المؤنث
        # بزيادة التاء المربوطة
        # جمع مؤنث سالم
        # ما كات اصله تاء مربوطة
        # للعمل TODO
        # دالة حاصة للكلمات المؤنثة
        ##print "stemmedword", self.get_original(), (araby.TEH_MARBUTA in self.get_original())
        if araby.TEH_MARBUTA in self.get_original():
            self.tag_gender += 2
        elif u'مؤنث' in self.tag_original_gender or u'مؤنث' in self.get_tags():
            self.tag_gender += 2
        elif u'جمع مؤنث سالم' in self.get_tags():
            self.tag_gender += 2
        elif self._affix_is_feminin():  # إذا كان متصلا بمايؤنثه
            self.tag_gender += 2
        # الحالات غير المثبتة والتي نحاول استخلاصها بقاعدة
        elif (u'مصدر' in self.get_type()
              and (araby.TEH_MARBUTA in self.get_original()
                   or u'جمع' in self.tag_original_number)):
            self.tag_gender += 2
            
        # جمع التكسير للمصادر والجوامد مؤنث
        elif u'جمع' in self.tag_original_number and (
                u"جامد" in self.get_type() or u"مصدر" in self.get_type()):
            self.tag_gender += 2

        #~ print "gender", self.word.encode('utf8'), self.tag_gender
        return self.tag_gender

    def _is_transparent(self):
        """
        Return True if the word has the state transparent,
        which can trasnpose the effect of the previous factor.
        @return: has the state transparent.
        @rtype: True/False
        """
        #temporary,
        # the transparent word are stopwords like هذا وذلك
        # the stopword tags have اسم إشارة,
        # a pounctuation can has the transparent tag like quotes.,
        # which havent any gramatical effect.
        # Todo
        # حالة بذلك الرجل
        #return  (u'شفاف' in self.get_tags() or u'إشارة'in self.get_tags()  ) and self.has_jar()
        return u'شفاف' in self.get_tags()

    def _is_mamnou3(self):
        """
        Return True if the word is forbiden from Sarf ممنوع من الصرف.
        @return: is mamnou3 min sarf.
        @rtype: True/False
        """
        return u'ممنوع من الصرف' in self.get_tags() or "noun_prop" in self.get_type()

    def get_procletic(self, ):
        """Get the procletic"""
        # return self.procletic
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].get_procletic()
        return u""

    def has_jonction(self, ):
        """return if the word has jonction"""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_3tf()
        return u""

    def has_procletic(self, ):
        """return True if has procletic"""
        # return self.procletic! = u''
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].has_procletic()
        return False

    def is_transitive(self, ):
        """return True if the verb is transitive"""
        return self.tag_transitive

    def is_indirect_transitive(self, ):
        """return True if the verb is indirect transitive  متعدي بحرف"""
        return self.tag_transitive

    def get_prefix(self, ):
        """Get the prefix"""
        # return self.prefix
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].get_prefix()
        return u""

    def get_suffix(self, ):
        """Get the suffix"""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].get_suffix()
        return u""

    def get_encletic(self, ):
        """Get the encletic"""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].get_encletic()
        return u""

    def has_encletic(self, ):
        """return True if has encletic"""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].has_encletic()
        return False

    # Mixed affix and dictionary attrrubutes
    #---------------------------------------
    def _affix_is_added(self):
        """ Return True if the word has the state added مضاف."""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_added()
        return False

    def _is_added(self):
        """Return True if the word has the state added مضاف."""
        #~ return self._affix_is_added() or u'اسم إضافة' in self.get_tags()
        return self._affix_is_added()

    def _affix_is_feminin(self):
        """Return True if the word is Feminin."""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_feminin()
        return False

    def _affix_is_plural(self):
        """Return True if the word is a plural."""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_plural()
        return False

    def _affix_is_dual(self):
        """Return True if the word is a dual."""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_dual()
        return False

    def _is_break(self):
        """Return True if the word has break."""
        #تكون الكلمة فاصلة إذا كانت منفصلة عمّا قبلها.
        # الحالات التي تقطع
        # - حرف جر متصل
        # فاصلة أو نقطة
        result = False
        if self.is_pounct() and 'break' in self.get_tags():
            result = True
        elif self.is_stopword(
        ) and not self.is_noun() and not self.is_transparent():
            result = True
        elif self.affix_key in GLOBAL_AFFIXES and GLOBAL_AFFIXES[self.
                                                                 affix_key].is_break(
                                                                 ):
            result = True
        elif self.has_procletic():
            if self.has_jar() or self.has_istfham():
                result = True
        return result

    ######################################################################
    #{ Attribut Functions
    ######################################################################
    def get_word(self, ):
        """Get the input word given by user"""
        return self.word

    def set_word(self, newword):
        """Set the input word given by user"""
        self.word = newword

    def get_vocalized(self, ):
        """Get the vocalized form of the input word"""
        return self.vocalized

    def set_vocalized(self, newvocalized):
        """Set the vocalized word """
        self.vocalized = newvocalized
        self.unvocalized = araby.strip_tashkeel(newvocalized)

    def get_semivocalized(self, ):
        """
        Get the semi vocalized form of the input word
        """
        return self.semivocalized

    def get_stem(self, ):
        """
        Get the stem form of the input word
        """
        return self.stem

    def get_tags(self, ):
        """
        Get the tags form of the input word
        """
        return self.tags

    def get_tags_to_display(self, ):
        """
        Get the tags form of the input word
        """
        return self.tags + u"T%dG%dN%d" % (self.tag_type, self.tag_gender,
                                           self.tag_number)

    def set_tags(self, newtags):
        """
        Set the tags word
        """
        self.tags = newtags

    def get_affix_tags(self, ):
        """
        Get the affix tags form of the input word
        """
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].get_tags()
        return u""

    def get_affix(self, ):
        """
        Get the affix  form of the input word
        """
        return self.affix

    def get_action(self, ):
        """
        Get the action form of the input word
        """
        return self.action

    def get_object_type(self, ):
        """
        Get the object_type form of the input word
        """
        return self.object_type

    def get_need(self, ):
        """
        Get the need form of the input word
        """
        return self.need

    def get_freq(self, ):
        """
        Get the freq form of the input word
        """
        return self.freq

    def set_freq(self, newfreq):
        """
        Set the freq word
        """
        self.freq = newfreq

    def get_type(self, ):
        """
        Get the type form of the input word
        """
        return self.type

    def set_type(self, newtype):
        """
        Set the type word
        """
        self.type = newtype

    def get_original(self, ):
        """
        Get the original form of the input word
        """
        return self.original

    def get_tense(self, ):
        """
        Get the tense of the input verb
        """
        return self.tag_tense

    def get_pronoun(self, ):
        """
        Get the tense of the input verb
        """
        return self.tag_pronoun

    def get_attached_pronoun(self, ):
        """
        Get the tense of the input verb
        """
        return self.tag_pronoun


    def set_original(self, neworiginal):
        """Set the original word"""
        self.original = neworiginal

    ######################################################################
    #{ _tags  Functions
    ######################################################################
    def is_initial(self):
        """Return True if the word mark the begin of next sentence."""
        return self.tag_initial

    #  حالة المضاف إليه
    #--------------------------
    def is_unknown(self):
        """Return True if the word is unknown."""
        return u'unknown' in self.get_type()

    def is_stopword(self):
        """Return True if the word is a stop word."""
        return bool(self.tag_type % 2)

    def is_indirect_transitive_stopword(self):
        """Return True if the word is a stop word."""
        return self.is_stopword() and self.get_original() in (u'فِي', u'عَنْ',
                                                              u'إِلَى',
                                                              u'عَلَى')

    def is_verb(self):
        """Return True if the word is a verb."""
        return bool(self.tag_type / 2 % 2)

    def is_noun(self):
        """Return True if the word is a noun."""
        return bool(self.tag_type / 4 % 2)

    def is_masdar(self):
        """Return True if the word is a masdar."""
        return bool(self.tag_type / 8 % 2)

    def is_adj(self):
        """Return True if the word is an adjective."""
        return bool(self.tag_type / 16 % 2)

    def is_proper_noun(self):
        """Return True if the word is a proper noun."""
        return bool(self.tag_type / 32 % 2)

    def is_pounct(self):
        """Return True if the word is a pounctuation."""
        return bool(self.tag_type / 64 % 2)

    def is_number(self):
        """Return True if the word is a number."""
        return bool(self.tag_type / 128 % 2)

    def is_transparent(self):
        """Return True if the word has the state transparent,
        which can trasnpose the effect of the previous factor.
        """
        #temporary,
        # the transparent word are stopwords like هذا وذلك
        # the stopword tags have اسم إشارة,
        # a pounctuation can has the transparent tag like quotes.,
        # which havent any gramatical effect.
        # Todo
        # حالة بذلك الرجل
        return self.tag_transparent

        #----------------------------
        # affixes boolean attributes
        #----------------------------

    def is_majrour(self):
        """Return True if the word has the state majrour."""
        # Like بهذه بتلك
        #~ print "maj",self.get_word().encode('utf8'), self.has_jar()

        if self.is_mabni() or self.has_jar():
            return True
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_majrour()

        return False

    def is_mansoub(self):
        """Return True if the word has the state mansoub."""
        #~ print "mansoub",self.get_word().encode('utf8'), self.has_jar()
        if self.is_mabni():
            if self.has_jar():
                return False
            else:
                return True
        if u"منصوب" in self.get_tags() and self.is_feminin_plural():
            return True
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_mansoub()
        return False

    def is_marfou3(self):
        """Return True if the word has the state marfou3."""
        #~ print "marf3",self.get_word().encode('utf8'), self.has_jar()

        if self.is_mabni():
            if self.has_jar():
                return False
            else:
                return True
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_marfou3()
        return False

    def is_majzoum(self):
        """Return True if the word has the state majrour. """
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_majzoum()
        return False

    def is_mabni(self):
        """Return True if the word has the state mabni."""
        if u"مبني" in self.get_tags():
            return True
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_mabni()
        return False

    def is_defined(self):
        """Return True if the word has the state definde."""
        #~ المعرفة: ما يقصد منه معيّن: والمعرفة سبعة أقسام هي:
        #~ الضمير، العلم، اسم الإشارة، الاسم الموصول، المحلَّى بأل، المضاف إلى معرفة، المنادى.
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_defined()
        elif u"ضمير" in self.get_tags():
            return True
        elif u"اسم إشارة" in self.get_tags():
            return True
        elif u"اسم موصول" in self.get_tags():
            return True
        elif u"noun_prop" in self.get_tags():
            return True
        return False

    def is_past(self):
        """Return True if the word has the tense past."""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_past()
        return False

    def is_passive(self):
        """Return True if the word has the tense passive."""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_passive()
        return False

    def is_present(self):
        """Return True if the word has the tense present."""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_present()
        return False

    def is_speaker_person(self):
        """Return True if the word has the 1st person."""
        return bool(self.tag_person % 2)

    def is_present_person(self):
        """Return True if the word has the 2nd person."""
        return bool(self.tag_person / 2 % 2)

    def is_absent_person(self):
        """Return True if the word has the 3rd person."""

        return bool(self.tag_person / 4 % 2)

    def is1stperson(self):
        """Return True if the word has the 1st person."""
        return bool(self.tag_person % 2) and self.is_single()

    def is2ndperson(self):
        """Return True if the word has the 2nd person."""
        return bool(self.tag_person / 2 % 2) and self.is_single()

    def is3rdperson(self):
        """Return True if the word has the 3rd person."""
        #~ print "tag_person", self.tag_person, self.word.encode('utf8')
        return bool(self.tag_person / 4 % 2) and self.is_single()

    def is3rdperson_feminin(self):
        """Return True if the word has the 3rd person."""
        return bool(self.tag_person / 4 %
                    2) and self.is_single() and self.is_feminin()

    def is3rdperson_masculin(self):
        """Return True if the word has the 3rd person."""
        return bool(self.tag_person / 4 %
                    2) and self.is_single() and self.is_masculin()
        #~
        #~ if self.affix_key in GLOBAL_AFFIXES:
        #~ return GLOBAL_AFFIXES[self.affix_key].is3rdperson_masculin()
        #~ return False
    def has_imperative_pronoun(self):
        """Return True if the word has the 3rd person."""
        return bool(self.tag_person / 2 % 2)
        #~ return (u':أنت:' in self.get_tags() or u':أنتِ:' in self.get_tags()) \
        #~ and u'أنتما' in self.get_tags() and  u':أنتما مؤ:' in self.get_tags() \
        #~ and u':أنتم:' in self.get_tags() and  u':أنتن:' in self.get_tags()

    def is_tanwin(self):
        """Return True if the word has tanwin."""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_tanwin()
        return False

    def has_jar(self):
        """Return True if the word has tanwin."""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].has_jar()
        return False

    def has_istfham(self):
        """Return True if the word has tanwin."""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].has_istfham()
        return False

    def is_break(self):
        """Return True if the word has break."""
        #تكون الكلمة فاصلة إذا كانت منفصلة عمّا قبلها.
        # الحالات التي تقطع
        # - حرف جر متصل
        # فاصلة أو نقطة
        return self.tag_break

    def is_masculin_plural(self):
        """Return True if the word is  Masculin plural."""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_masculin_plural()
        return False

    def is_dual(self):
        """Return True if the word is  dual."""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_dual()
        return False

    def is_feminin_plural(self):
        """Return True if the word is  Feminin plural."""
        if self.affix_key in GLOBAL_AFFIXES:
            return GLOBAL_AFFIXES[self.affix_key].is_feminin_plural()
        return False

    #-----------------------------
    # Mixed extraction attributes tests
    #-----------------------------

    def is_masculin(self):
        """Return True if the word is masculin."""
        return bool(self.tag_gender % 2)

    def is_feminin(self):
        """Return True if the word is Feminin."""
        return bool(self.tag_gender / 2 % 2)

    def is_plural(self):
        """Return True if the word is a plural."""
        return bool(self.tag_number / 4 % 2)

    def is_broken_plural(self):
        """Return True if the word is broken  plural."""
        return bool(self.tag_number / 32 % 2)

    def is_mamnou3(self):
        """Return True if the word is Mamnou3 min Sarf."""
        return self.tag_mamnou3

    def is_single(self):
        """Return True if the word is single."""
        return not self.is_plural() and not self.is_dual()

    def is_added(self):
        """Return True if the word has the state added مضاف."""
        return self.tag_added

    ######################################################################
    #{ Display Functions
    ######################################################################
    def get_dict(self, ):
        """getdictionary function"""
        return self.__dict__

    def __repr__(self):
        """Display objects result from analysis"""
        return self.__str__()

    def __str__(self):
        """Display objects result from analysis"""
        text = u"{"
        stmword = self.__dict__
        stmword['affix'] = 'Taha'
        for key in stmword.keys():
            text += u"\n\t\tu'%s' = u'%s', " % (key, stmword[key])
        text += u'\n\t\t}'
        return text.encode('utf8')
        
    def __dict__(self):
        """get dict objects result from analysis"""
        return self.__dict__
        #~ text = u"{"
        #~ stmword = self.__dict__
        #~ stmword['affix'] = 'Taha'
        #~ for key in stmword.keys():
            #~ text += u"\n\t\tu'%s' = u'%s', " % (key, stmword[key])
        #~ text += u'\n\t\t}'
        #~ return text.encode('utf8')


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
        "freq": 0,  # the word frequency from _word _frequency database
        "root": "",  # the word root not yet used
        "template": "",  # the template وزن
        "type": "Noun:مصدر",  # the word type
        "original": "حَيَاةٌ",  #original word from lexical dictionary
        "syntax": "",  # used for syntaxique analysis porpos
        u'semantic': '',
    }
    stmwrd = StemmedWord(RDICT)
    print(stmwrd.get_dict())

    stmwrd.set_word("4444")
    stmwrd.set_vocalized("4444")
    stmwrd.set_tags("4444")
    stmwrd.set_freq("4444")
    stmwrd.set_type("4444")
    stmwrd.set_original("4444")

    print(stmwrd)
