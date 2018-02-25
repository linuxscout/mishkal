#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------
# Name:        stem_noun
# Purpose:     Arabic lexical analyser, provides feature for
#~stemming arabic word as noun
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------
"""
    Arabic noun stemmer
"""
import re
if __name__ == '__main__':
    import sys
    sys.path.append('../support')
    sys.path.append('support')
    sys.path.append('..')
import pyarabic.araby as ar
import tashaphyne.stemming
#~ import tashaphyne.normalize
import qalsadi.stem_noun_const as SNC
import arramooz.arabicdictionary as arabicdictionary
import qalsadi.wordcase as wordcase


class NounStemmer:
    """
        Arabic noun stemmer
    """

    def __init__(self, debug=False):
        # create a stemmer object for stemming enclitics and proclitics
        self.comp_stemmer = tashaphyne.stemming.ArabicLightStemmer()
        # configure the stemmer object
        self.comp_stemmer.set_prefix_list(SNC.COMP_PREFIX_LIST)
        self.comp_stemmer.set_suffix_list(SNC.COMP_SUFFIX_LIST)
        # create a stemmer object for stemming conjugated verb
        self.conj_stemmer = tashaphyne.stemming.ArabicLightStemmer()
        # configure the stemmer object
        self.conj_stemmer.set_prefix_list(SNC.CONJ_PREFIX_LIST)
        self.conj_stemmer.set_suffix_list(SNC.CONJ_SUFFIX_LIST)

        # enable the last mark (Harakat Al-I3rab)
        self.allow_syntax_lastmark = True

        # noun dictionary
        self.noun_dictionary = arabicdictionary.ArabicDictionary("nouns")

        # allow to print internal results.
        self.cache_dict_search = {}
        self.cache_affixes_verification = {}
        self.debug = debug


    def stemming_noun(self, noun_in):
        """
        Analyze word morphologically as noun
        @param noun_in: the input noun.
        @type noun_in: unicode.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        debug = False
        #~list_found = []
        detailed_result = []
        noun_list = [
            noun_in,
        ] + get_noun_variants(noun_in)
        word_segmented_list = []
        for noun in noun_list:
            list_seg_comp = self.comp_stemmer.segment(noun)
            # filter
            list_seg_comp = verify_affix(noun, list_seg_comp,
                                         SNC.COMP_NOUN_AFFIXES)
            # treat multi vocalization enclitic
            for seg in list_seg_comp:
                proclitic_nm = noun[:seg[0]]
                stem = noun[seg[0]:seg[1]]
                enclitic_nm = noun[seg[1]:]
                # ajusting nouns variant
                list_stem = [
                    stem,
                ] + get_in_stem_variants(stem, enclitic_nm)

                # stem reduced noun : level two
                for stem in list_stem:
                    word_seg = {
                        'noun': noun,
                        'stem_comp': stem,
                        'pro': proclitic_nm,
                        'enc': enclitic_nm,
                    }
                    word_segmented_list.append(word_seg)
        # level two
        tmp_list = []
        if debug: print("after first level")
        if debug:
            print(repr(word_segmented_list).replace(
                '},', '},\n').decode("unicode-escape"))

        for word_seg in word_segmented_list:

            #~ detailed_result.extend(
            #~ self.steming_second_level(word_seg['noun'], word_seg['stem_comp'],
            #~ word_seg['pro'], word_seg['enc']))
            #~ detailed_result_one = []
            #segment the coinjugated noun
            list_seg_conj = self.conj_stemmer.segment(word_seg['stem_comp'])
            # verify affix compatibility
            # filter
            list_seg_conj = verify_affix(word_seg['stem_comp'], list_seg_conj,
                                         SNC.NOMINAL_CONJUGATION_AFFIX)
            # add vocalized forms of suffixes
            # and create the real affixes from the word
            for seg_conj in list_seg_conj:
                stem_conj = word_seg['stem_comp'][:seg_conj[1]]
                suffix = word_seg['stem_comp'][seg_conj[1]:]
                stem_conj = ar.normalize_hamza(stem_conj)
                stem_conj_list = get_stem_variants(stem_conj, suffix)

                # generate possible stems
                # add stripped letters to the stem to constitute possible noun list
                for stem in stem_conj_list:
                    word_seg_l2 = word_seg.copy()
                    # normalize hamza before gessing  differents origines
                    word_seg_l2['stem_conj'] = stem
                    word_seg_l2['suffix'] = suffix
                    #affixes tags contains prefixes and suffixes tags
                    word_seg_l2['affix_tags'] = list(
                        set(SNC.COMP_PREFIX_LIST_TAGS[word_seg_l2['pro']]
                            ['tags'] + SNC.
                            COMP_SUFFIX_LIST_TAGS[word_seg_l2['enc']]['tags'] +
                            SNC.CONJ_SUFFIX_LIST_TAGS[word_seg_l2['suffix']]
                            ['tags']))
                    tmp_list.append(word_seg_l2)

        if debug: print("after second level")
        if debug:
            print(repr(tmp_list).replace('},',
                                         '},\n').decode("unicode-escape"))
        # lookup in dictionary
        word_segmented_list = tmp_list
        tmp_list = []
        for word_seg in word_segmented_list:
            # search the noun in the dictionary
            # we can return the tashkeel
            inf_noun = word_seg['stem_conj']
            # get the noun and get all its forms from the dict
            # if the noun has plural suffix, don't look up in
            #broken plural dictionary
            if inf_noun in self.cache_dict_search:
                infnoun_foundlist = self.cache_dict_search[inf_noun]
            else:
                infnoun_foundlist = self.noun_dictionary.lookup(inf_noun)
                self.cache_dict_search[inf_noun] = infnoun_foundlist

            for noun_tuple in infnoun_foundlist:
                word_seg_l3 = word_seg.copy()
                word_seg_l3["original"] = noun_tuple['vocalized']
                word_seg_l3["noun_tuple"] = dict(noun_tuple)
                tmp_list.append(word_seg_l3)

        if debug: print("after lookup dict")
        if debug:
            print(repr(tmp_list).replace('},',
                                         '},\n').decode("unicode-escape"))
        # test compatiblity noun_tuple with affixes and proaffixes
        # and generate vocalized affixes and suffixes
        word_segmented_list = tmp_list
        tmp_list = []
        for word_seg in word_segmented_list:
            #test if the  given word from dictionary accept those
            # tags given by affixes
            # دراسة توافق الزوائد مع خصائص الاسم،
            # مثلا هل يقبل الاسم التأنيث.
            if validate_tags(word_seg['noun_tuple'], word_seg['affix_tags'],
                             word_seg['pro'], word_seg['enc'],
                             word_seg['suffix']):
                ## get all vocalized form of suffixes
                for enc_voc in SNC.COMP_SUFFIX_LIST_TAGS[word_seg['enc']][
                        'vocalized']:
                    for suf_voc in SNC.CONJ_SUFFIX_LIST_TAGS[word_seg[
                            'suffix']]['vocalized']:
                        ## verify compatibility between proclitics and affix
                        if self.__check_clitic_affix(word_seg['noun_tuple'],
                                                     word_seg['pro'], enc_voc,
                                                     suf_voc):
                            # get affix tags
                            affix_tags_voc = SNC.COMP_PREFIX_LIST_TAGS[word_seg['pro']]['tags']\
                              +SNC.COMP_SUFFIX_LIST_TAGS[enc_voc]['tags']\
                              +SNC.CONJ_SUFFIX_LIST_TAGS[suf_voc]['tags']
                            word_seg_l4 = word_seg.copy()
                            word_seg_l4['suf_voc'] = suf_voc
                            word_seg_l4['enc_voc'] = enc_voc
                            word_seg_l4['affix_tags'] = affix_tags_voc
                            tmp_list.append(word_seg_l4)

        if debug: print("after check compatibility")
        if debug:
            print(repr(tmp_list).replace('},',
                                         '},\n').decode("unicode-escape"))
        # Generate results
        word_segmented_list = tmp_list
        tmp_list = []
        for word_seg in word_segmented_list:
            # get voalized and vocalized without inflection
            vocalized, semi_vocalized, _ = vocalize(
                word_seg['noun_tuple']['vocalized'], word_seg['pro'], word_seg['suf_voc'],
                word_seg['enc_voc'])

            #add some tags from dictionary entry as
            #mamnou3 min sarf and broken plural
            original_tags = []
            if word_seg['noun_tuple']['mankous'] == u"Tk":
                original_tags.append(u"منقوص")
            # if there are many cases like feminin plural with mansoub and majrour
            if 'cases' in SNC.CONJ_SUFFIX_LIST_TAGS[word_seg['suf_voc']]:
                list_cases = SNC.CONJ_SUFFIX_LIST_TAGS[word_seg['suf_voc']][
                    'cases']
            else:
                list_cases = ('', )
            for case in list_cases:
                voc_affix_case = word_seg['affix_tags'] + (case, )
                detailed_result.append(
                    wordcase.WordCase({
                        'word':
                        noun_in,
                        'affix': (word_seg['pro'], '', word_seg['suf_voc'],
                                  word_seg['enc_voc']),
                        'stem':
                        word_seg['stem_conj'],
                        'original':
                        word_seg['noun_tuple']['vocalized'],  #original,
                        'vocalized':
                        vocalized,
                        'semivocalized':
                        semi_vocalized,
                        'tags':
                        u':'.join(voc_affix_case),
                        'type':
                        u':'.join(['Noun', word_seg['noun_tuple']['wordtype']]),
                        'number':
                        word_seg['noun_tuple']['number'],
                        'gender':
                        word_seg['noun_tuple']['gender'],
                        'freq':
                        'freqnoun',  # to note the frequency type
                        'originaltags':
                        u':'.join(original_tags),
                        'syntax':
                        '',
                    }))
        if debug: print("after generate result")
        if debug: print(len(detailed_result))
        #~ if debug: print repr(detailed_result).replace('},','},\n').decode("unicode-escape")
        return detailed_result

    def __check_clitic_affix(self, noun_tuple, proclitic_nm, enclitic, suffix):
        """
        Verify if proaffixes (sytaxic affixes) are compatable
        with affixes ( conjugation)
        @param proclitic_nm: first level prefix.
        @type proclitic_nm: unicode.
        @param enclitic: first level suffix.
        @type enclitic: unicode.
        @param suffix: second level suffix.
        @type suffix: unicode.
        @return: compatible.
        @rtype: True/False.
        """
        # avoid Fathatan on no ALEF Tawnwin expect on Teh marbuta and Alef followed by Hamza
        # تجنب تنوين النصب على غير الألف ما عدا التاء المربوطة أو همزة بعد ألف
        if suffix == ar.FATHATAN and not (
                noun_tuple["unvocalized"].endswith(ar.TEH_MARBUTA)
                or noun_tuple["unvocalized"].endswith(ar.ALEF + ar.HAMZA)):
            return False
        # avoid masculin regular plural with unallowed case
        # تجنب جمع المذكر السالم للكلمات التي لا تقبلها
        if u'جمع مذكر سالم' in SNC.CONJ_SUFFIX_LIST_TAGS[suffix]['tags']\
          and not noun_tuple['masculin_plural']:
            return False
                    # التنوين لا يتطابق مع الممنوع من الصرف
        #~ print "stem_noun", noun_tuple["unvocalized"].encode('utf8'), noun_tuple['masculin_plural'],type(noun_tuple['masculin_plural']),    bool(noun_tuple['masculin_plural'])
        if u'تنوين' in SNC.CONJ_SUFFIX_LIST_TAGS[suffix]['tags'] and noun_tuple['mamnou3_sarf']:
            return False
        #if not proclitic and not enclitic:  return True
        #use cache for affix verification
        affix = u'-'.join([
            proclitic_nm, enclitic, suffix,
            str(bool(noun_tuple['mamnou3_sarf']))
        ])
        #~print affix.encode("utf8")
        if affix in self.cache_affixes_verification:
            return self.cache_affixes_verification[affix]

        # get proclitics and enclitics tags
        proclitic_tags = SNC.COMP_PREFIX_LIST_TAGS[proclitic_nm]['tags']
        enclitic_tags = SNC.COMP_SUFFIX_LIST_TAGS[enclitic]['tags']
        # in nouns there is no prefix
        suffix_tags = SNC.CONJ_SUFFIX_LIST_TAGS[suffix]['tags']
        # in some cases the suffixes have more cases
        # add this cases to suffix tags
        suffix_tags += SNC.CONJ_SUFFIX_LIST_TAGS[suffix].get("cases", ())
        if u"تعريف" in proclitic_tags and u"مضاف" in suffix_tags and \
        u'مضاف' not in enclitic_tags:
            self.cache_affixes_verification[affix] = False
        elif u"تعريف" in proclitic_tags and u"تنوين" in suffix_tags:
            self.cache_affixes_verification[affix] = False
        elif u"تعريف" in proclitic_tags and u"إضافة" in suffix_tags:
            self.cache_affixes_verification[affix] = False


    # الجر  في حالات الاسم المعرفة بال أو الإضافة إلى ضمير أو مضاف إليه
    # مما يعني لا يمكن تطبيقها هنا
    # بل في حالة التحليل النحوي
        elif u"مضاف" in enclitic_tags and u"تنوين" in suffix_tags:
            self.cache_affixes_verification[affix] = False
        elif u"مضاف" in enclitic_tags and u"لايضاف" in suffix_tags:
            self.cache_affixes_verification[affix] = False
        elif u"جر" in proclitic_tags and u"مجرور" not in suffix_tags:
            self.cache_affixes_verification[affix] = False


#ستعمل في حالة كسر هاء الضمير في الجر

#elif  bool(u"لايجر" in enclitic_tags) and  bool(u"مجرور" in \
#suffix_tags) :
#    self.cache_affixes_verification[affix] = False
#elif  bool(u"مجرور" in enclitic_tags) and  not bool(u"مجرور" in \
#suffix_tags) :
#    self.cache_affixes_verification[affix] = False
        else:
            self.cache_affixes_verification[affix] = True

        return self.cache_affixes_verification[affix]

    def set_debug(self, debug):
        """
        Set the debug attribute to allow printing internal analysis results.
        @param debug: the debug value.
        @type debug: True/False.
        """
        self.debug = debug

    def enable_syntax_lastmark(self):
        """
        Enable the syntaxic last mark attribute to allow use of I'rab harakat.
        """
        self.allow_syntax_lastmark = True

    def disable_syntax_lastmark(self):
        """
        Disable the syntaxic last mark attribute to allow use of I'rab harakat.
        """
        self.allow_syntax_lastmark = False


def get_stem_variants(stem, suffix_nm):
    """
    Generate the Noun stem variants according to the affixes.
    For example مدرستي = >مدرست+ي = > مدرسة +ي.
    Return a list of possible cases.
    @param stem: the input stem.
    @type stem: unicode.
    @param suffix_nm: suffix (no mark).
    @type suffix_nm: unicode.
    @return: list of stem variants.
    @rtype: list of unicode.
    """
    #some cases must have some correction
    #determinate the  suffix types
    #~suffix = suffix_nm

    possible_noun_list = set([
        stem,
    ])
    if suffix_nm in (ar.ALEF + ar.TEH, ar.YEH + ar.TEH_MARBUTA, ar.YEH,
                     ar.YEH + ar.ALEF + ar.TEH):
        possible_noun = stem + ar.TEH_MARBUTA
        possible_noun_list.add(possible_noun)
    if not suffix_nm or suffix_nm in (ar.YEH + ar.NOON, ar.WAW + ar.NOON):
        possible_noun = stem + ar.YEH
        possible_noun_list.add(possible_noun)
    if stem.endswith(ar.YEH):
        # إذا كان أصل الياء ألفا مقصورة
        possible_noun = stem[:-1] + ar.ALEF_MAKSURA
        possible_noun_list.add(possible_noun)

    if stem.endswith(ar.HAMZA):
        possible_noun = stem[:-1] + ar.YEH_HAMZA
        possible_noun_list.add(possible_noun)
    #to be validated
    validated_list = possible_noun_list
    return validated_list


def get_suffix_variants(word, suffix, enclitic, mankous=False):
    """
    Get the suffix variant to be joined to the word.
    For example: word = مدرس, suffix = ة, enclitic = ي.
    The suffix is converted to Teh.
    @param word: word found in dictionary.
    @type word: unicode.
    @param suffix: second level suffix.
    @type suffix: unicode.
    @param enclitic: first level suffix.
    @type enclitic: unicode.
    @param mankous: if the noun is mankous ends with Yeh منقوص.
    @type mankous: boolean.
    @return: variant of suffixes  (vocalized suffix and vocalized
    suffix without I'rab short mark).
    @rtype: (unicode, unicode)
    """
    #enclitic_nm = ar.strip_tashkeel(enclitic)
    enclitic_nm = enclitic  # given enclitic is not vocalized
    newsuffix = suffix  #default value
    #if the word ends by a haraka
    if suffix.find(ar.TEH_MARBUTA) >= 0 and enclitic_nm:
        newsuffix = re.sub(ar.TEH_MARBUTA, ar.TEH, suffix)

    elif not enclitic_nm and ar.is_haraka(suffix):
        if word[-1:] in (ar.YEH, ar.ALEF):
            newsuffix = u""
        elif mankous:
            # the word is striped from YEH المنقوص حذفت ياؤه قبل قليل
            # تحول حركته إلى تنوين كسر
            newsuffix = ar.KASRATAN
    #gererate the suffix without I'rab short mark
    # here we lookup with given suffix because the new suffix is
    # changed and can be not found in table
    if u'متحرك' in SNC.CONJ_SUFFIX_LIST_TAGS[suffix]['tags']:
        suffix_non_irab_mark = ar.strip_lastharaka(newsuffix)
    else:
        suffix_non_irab_mark = newsuffix
    return newsuffix, suffix_non_irab_mark


def get_enclitic_variant(enclitic_voc, suffix_voc):
    """
    Get the enclitix variant to be joined to the word.
    For example: word = كتاب, suffix = كسرة, enclitic = هم.
    The enclitic has a second form هِم.
    @param enclitic_voc: first level suffix vocalized.
    @type enclitic_voc: unicode.
    @param suffix_voc: second level suffix vocalized.
    @type suffix_voc: unicode.
    @return: variant of enclitic  (vocalized enclitic and vocalized
    enclitic without I'rab short mark).
    @rtype: (unicode, unicode)
    """
    #print (u"get enclit2 '%s' %d"%(enclitic_voc, len(enclitic_voc))).encode('utf8')
    encl_vo_no_inflect_mark = enclitic_voc
    if enclitic_voc.startswith(ar.HEH + ar.DAMMA) and suffix_voc.endswith(
            ar.KASRA):
        encl_vo_no_inflect_mark = enclitic_voc.replace(ar.HEH + ar.DAMMA,
                                                       ar.HEH)
        enclitic_voc = enclitic_voc.replace(ar.HEH + ar.DAMMA,
                                            ar.HEH + ar.KASRA)
        #print "ok"
    return enclitic_voc, encl_vo_no_inflect_mark


def get_word_variant(word, suffix, enclitic):
    """
    Get the word variant to be joined to the suffix.
    For example: word = مدرسة, suffix = ي. The word is converted to مدرست.
    @param word: word found in dictionary.
    @type word: unicode.
    @param suffix: suffix ( first level).
    @type suffix: unicode.
    @param enclitic: enclitic( second level).
    @type enclitic: unicode.
    @return: variant of word.
    @rtype: unicode.
    """
    word_stem = word

    suffix_nm = ar.strip_tashkeel(suffix)

    enclitic_nm = ar.strip_tashkeel(enclitic)
    long_suffix_nm = suffix_nm + enclitic_nm
    #if the word ends by a haraka
    word_stem = ar.strip_lastharaka(word_stem)

    # الاسم المؤنث بالتاء المروبطة نحذفها قبل اللاحقات مثل ات وية
    if word_stem.endswith(ar.TEH_MARBUTA):
        # حالة الاسماء مثل حياة وفتاة
        if word_stem.endswith(ar.ALEF + ar.TEH_MARBUTA):
            if suffix_nm in (ar.YEH, ar.YEH + ar.TEH_MARBUTA,
                             ar.YEH + ar.ALEF + ar.TEH):
                word_stem = word_stem[:-1] + ar.TEH
            elif suffix_nm == ar.ALEF + ar.TEH:
                #نحن بحاجة إلى حذف آخر حركة أيضا
                word_stem = ar.strip_lastharaka(word_stem[:-1])
            elif long_suffix_nm != u"":
                word_stem = word_stem[:-1] + ar.TEH

        elif suffix_nm in (ar.ALEF + ar.TEH, ar.YEH + ar.TEH_MARBUTA, ar.YEH,
                           ar.YEH + ar.ALEF + ar.TEH):
            #نحن بحاجة إلى حذف آخر حركة أيضا
            word_stem = ar.strip_lastharaka(word_stem[:-1])
        # الاسم المؤنث بالتاء المروبطة نفتحها قبل اللصق
        #مدرسة +ين = مدرستين
        elif long_suffix_nm != u"":
            word_stem = word_stem[:-1] + ar.TEH

    elif word_stem.endswith(ar.ALEF_MAKSURA):
        # الاسم المقصور إذا اتصل بلاحقة نحوية صارت ألف المقصورة ياء
        # مستوى +ان = مستويان
        # إذا كانت اللاحقة الصرفية ذات حروف تتحول الألف المقصورة إلى ياء
        if suffix_nm != u"":
            word_stem = word_stem[:-1] + ar.YEH
    # إذا كانت اللاحقة الصرفية حركات فقط والضمير المتصل  تتحول الألف المقصورة إلى ألف
        elif enclitic_nm != u"":
            word_stem = word_stem[:-1] + ar.ALEF
    elif word_stem.endswith(ar.KASRA + ar.YEH):
        # الاسم المنقوص ينتهي بياء قبلها مكسور
        # إذا كان لا ضمير واللاحقة فقط حركات
        # نحذف ال
        if not enclitic_nm and not suffix_nm:
            word_stem = ar.strip_lastharaka(word_stem[:-2])
    # الاسم المنقوص ينتهي بياء قبلها مكسور
    # إذا كانت اللاحقة ياء ونون
        elif suffix_nm in (ar.YEH + ar.NOON, ar.WAW + ar.NOON):
            word_stem = ar.strip_lastharaka(word_stem[:-2])

    #ضبط المنتهي بالهمزة حسب حركة اللاحقة النحوية
    elif word_stem.endswith(ar.HAMZA) and suffix_nm != u"":
        if suffix.startswith(ar.DAMMA):
            word_stem = word_stem[:-1] + ar.WAW_HAMZA
        elif suffix.startswith(ar.KASRA):
            word_stem = word_stem[:-1] + ar.YEH_HAMZA
        elif (word_stem.endswith(ar.YEH + ar.HAMZA)
              or word_stem.endswith(ar.YEH + ar.SUKUN + ar.HAMZA)
             ) and suffix.startswith(ar.FATHATAN):
            word_stem = word_stem[:-1] + ar.YEH_HAMZA
    return word_stem


def vocalize(noun, proclitic, suffix, enclitic):
    """
    Join the  noun and its affixes, and get the vocalized form
    @param noun: noun found in dictionary.
    @type noun: unicode.
    @param proclitic: first level prefix.
    @type proclitic: unicode.

    @param suffix: second level suffix.
    @type suffix: unicode.
    @param enclitic: first level suffix.
    @type enclitic: unicode.
    @return: vocalized word.
    @rtype: unicode.
    """
    # proclitic have only an uniq vocalization in arabic
    proclitic_voc = SNC.COMP_PREFIX_LIST_TAGS[proclitic]["vocalized"][0]
    # enclitic can be variant according to suffix
    #print (u"vocalize: '%s' '%s'"%(enclitic, noun)).encode('utf8')
    enclitic_voc = SNC.COMP_SUFFIX_LIST_TAGS[enclitic]["vocalized"][0]
    enclitic_voc, encl_voc_non_inflect = get_enclitic_variant(
        enclitic_voc, suffix)

    suffix_voc = suffix
    #adjust some some harakat

    #strip last if tanwin or last harakat
    if ar.is_haraka(noun[-1:]):
        #(DAMMATAN, FATHATAN, KASRATAN, FATHA, DAMMA, KASRA):
        noun = noun[:-1]
    # convert Fathatan into one fatha, in some cases where #
    #the tanwin is not at the end: eg. محتوًى
    noun = noun.replace(ar.FATHATAN, ar.FATHA)

    #add shadda if the first letter is sunny and the proclitic
    #contains AL definition mark
    if u'تعريف' in SNC.COMP_PREFIX_LIST_TAGS[proclitic]["tags"] and ar.is_sun(noun[0]):
        noun = u''.join([noun[0], ar.SHADDA, noun[1:]])
        #strip the Skun from the lam
        if proclitic_voc.endswith(ar.SUKUN):
            proclitic_voc = proclitic_voc[:-1]
    #completate the dictionary word vocalization
    # this allow to avoid some missed harakat before ALEF
    # in the dictionary form of word, all alefat are preceded by Fatha
    #~noun = ar.complet
    #~ print "stem_noun.vocalize; before", noun.encode('utf8');
    noun = noun.replace(ar.ALEF, ar.FATHA + ar.ALEF)
    #~ print "stem_noun.vocalize; 2", noun.encode('utf8');

    noun = noun.replace(ar.ALEF_MAKSURA, ar.FATHA + ar.ALEF_MAKSURA)
    noun = re.sub(u"(%s)+" % ar.FATHA, ar.FATHA, noun)
    # remove initial fatha if alef is the first letter
    noun = re.sub(u"^(%s)+" % ar.FATHA, "", noun)
    #~ print "stem_noun.vocalize; 3", noun.encode('utf8');

    # generate the word variant for some words witch ends by special
    #letters like Teh_marbuta or Alef_maksura, or hamza,
    #the variant is influed by the suffix harakat,
    # for example مدرسة+ي = مدرست+ي
    mankous = True if noun.endswith(ar.KASRA + ar.YEH) else False

    noun = get_word_variant(noun, suffix, enclitic)

    # generate the suffix variant. if the suffix is Teh_marbuta or
    #Alef_maksura, or hamza, the variant is influed by the enclitic harakat,
    # for example مدرس+ة+ي = مدرس+ت+ي
    suffix_voc, suffix_non_irab_mark = get_suffix_variants(
        noun, suffix_voc, enclitic, mankous)

    # generate the non vacalized end word: the vocalized word
    # without the I3rab Mark
    # if the suffix is a short haraka
    word_non_irab_mark = ''.join(
        [proclitic_voc, noun, suffix_non_irab_mark, encl_voc_non_inflect])

    #generate vocalized form

    word_vocalized = ''.join([proclitic_voc, noun, suffix_voc, enclitic_voc])
    #used for spelling purposes
    segmented = '-'.join([proclitic_voc, noun, suffix_voc, enclitic_voc])
    segmented = ar.strip_tashkeel(segmented)
    #~word_vocalized = ar.ajust_vocalization(word_vocalized)3
    for patrn, repl in SNC.AJUST_VOCAL_PATTERNS:
        word_vocalized = word_vocalized.replace(patrn, repl)
        word_non_irab_mark = word_non_irab_mark.replace(patrn, repl)

    return word_vocalized, word_non_irab_mark, segmented

def get_noun_variants(noun):
    """ generate noun varaintes """
    # if the word contains ALEF8MADDA, we convert it into 2 HAMZA above ALEF
    noun_list = []
    if ar.ALEF_MADDA in noun:
        noun_list.append(
            noun.replace(ar.ALEF_MADDA, ar.ALEF_HAMZA_ABOVE * 2))
    return noun_list

def get_in_stem_variants(stem, enclitic_nm):
    """ generate stem varaintes """
    list_stem = []
    if enclitic_nm:
        # حالة الاسم المقصور إذا كان به زيادة مثل سوى +ها = سواها
        if stem.endswith(ar.ALEF):
            list_stem.append(stem[:-1] + ar.ALEF_MAKSURA)
        # حالة المؤنث بالتاء قد يكون أصلها تاء مربوطة
        elif stem.endswith(ar.TEH):
            list_stem.append(stem[:-1] + ar.TEH_MARBUTA)
    # Case of Mankous Name حالة الاسم المنقوص
    # إذا لم يكن به زيادة ربما كان الاسم منقوصا منوّنا
    # قد يقبل السابقة مثل وقاضٍ
    # لكنه لا يقبل اللاحقة
    else:  # no enclitic
        list_stem.append(stem + ar.YEH)
    return list_stem


def verify_affix(word, list_seg, affix_list):
    """
    Verify possible affixes in the resulted segments according
    to the given affixes list.
    @param word: the input word.
    @type word: unicode.
    @param list_seg: list of word segments indexes (numbers).
    @type list_seg: list of pairs.
    @return: list of acceped segments.
    @rtype: list of pairs.
    """
    return [
        s for s in list_seg
        if '-'.join([word[:s[0]], word[s[1]:]]) in affix_list
    ]


def validate_tags(noun_tuple, affix_tags, proclitic_nm, enclitic_nm,
                  suffix_nm):
    """
    Test if the given word from dictionary is compabilbe with affixes tags.
    @param noun_tuple: the input word attributes given from dictionary.
    @type noun_tuple: dict.
    @param affix_tags: a list of tags given by affixes.
    @type affix_tags:list.
    @param proclitic: first level prefix vocalized.
    @type proclitic: unicode.
    @param enclitic_nm: first level suffix vocalized.
    @type enclitic_nm: unicode.
    @param suffix_nm: first level suffix vocalized.
    @type suffix_nm: unicode.
    @return: if the tags are compatible.
    @rtype: Boolean.
    """
    #~ proclitic = ar.strip_tashkeel(proclitic)
    proclitic = proclitic_nm
    #~ enclitic = enclitic_nm
    #~ suffix = suffix_nm
    if u'تنوين' in affix_tags and noun_tuple['mamnou3_sarf']:
        return False
    # ألجمع السالم لا يتصل بجمع التكسير
    if noun_tuple['number'] in (u'جمع', u'جمع تكسير'):

        if u'جمع مؤنث سالم' in affix_tags:
            return False
        if u'جمع مذكر سالم' in affix_tags:
            return False
        if u'مثنى' in affix_tags:
            return False
    #تدقيق الغضافة إلى الضمائر المتصلة
    if enclitic_nm in (u"هم", u"هن", u"كما", u"كم",
                       u"هما") and not noun_tuple['hm_suffix']:
        return False
    if enclitic_nm in (u"ه", u"ها") and not noun_tuple['ha_suffix']:
        return False
    #حالة قابلية السوابق  بدون تعريف
    if u"ال" not in proclitic and not noun_tuple['k_prefix']:
        return False
    #حالة قابلية السوابق  مع التعريف
    if proclitic.endswith(u"ال") and not noun_tuple['kal_prefix']:
        return False
    # حالة المضاف إلى ما بعهده في حالة جمع المذكر السالم
    # مثل لاعبو، رياضيو
    if suffix_nm == ar.WAW and not noun_tuple['w_suffix']:
        return False
    #التاء المربوطة لا تتصل بجمع التكسير
    if suffix_nm == ar.TEH_MARBUTA and noun_tuple['number'] == u"جمع":
        return False
    # elif  u'مضاف' in affix_tags and not noun_tuple['annex']:
    # return False


#todo
# u'mankous':8,
# u'feminable':9, *
# u'number':10,
# u'dualable':11, *
# u'masculin_plural':12, *
# u'feminin_plural':13, *
# u'broken_plural':14,
# u'mamnou3_sarf':15,
# u'relative':16,
# u'w_suffix':17,
# u'hm_suffix':18, *
# u'kal_prefix':19, *
# u'ha_suffix':20, *
# u'k_suffix':21, *
# u'annex':22,
    return True


def mainly():
    """
    Test main"""
    #ToDo: use the full dictionary of arramooz
    wordlist = [
        u'يضرب',
        u'الكتاب',
        u'الاستخدام',
        u"فاستعمالهم",
        u'ضرب',
        u'لأكلهم',
    ]
    nounstemmer = NounStemmer()
    nounstemmer.set_debug(True)
    for word in wordlist:
        nounstemmer.conj_stemmer.segment(word)
        print(nounstemmer.conj_stemmer.get_affix_list())
    for word in wordlist:
        result = nounstemmer.stemming_noun(word)
        for analyzed in result:
            #~ print(repr(analyzed).encode('utf8')) #.decode('unicode-escape')
            #~ print(u'\n'.join(analyzed.__dict__.keys()))
            for key in analyzed.__dict__.keys():
                print((u'\t'.join([
                    key,
                    repr(analyzed.__dict__[key]).decode('unicode-escape')
                ]))).encode('utf8')
            print()
            print()


#Class test
if __name__ == '__main__':
    mainly()
