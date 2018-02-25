#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        stem_unknown
# Purpose:     Arabic lexical analyser, provides feature for
#  stemming arabic word as unknown word
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
    Arabic unknown word stemmer.
    Unkown words are stemmed as nouns with another dictionary
"""
import re
import pyarabic.araby as araby
import tashaphyne.stemming
import tashaphyne.normalize
#~import analex_const
import qalsadi.stem_noun_const as snconst
#~import arramooz.arabicdictionary as arabicdictionary
import arramooz.wordfreqdictionaryclass as wordfreqdictionaryclass
import qalsadi.wordcase as wordcase
#Todo:  remove all individual constants of arabic letters, Done
NOUN_DICTIONARY_INDEX = {
    u'id': 0,
    u'vocalized': 1,
    u'unvocalized': 2,
    u'wordtype': 3,
    u'root': 4,
    u'normalized': 5,
    u'stamped': 6,
    u'original': 7,
    u'mankous': 8,
    u'feminable': 9,
    u'number': 10,
    u'dualable': 11,
    u'masculin_plural': 12,
    u'feminin_plural': 13,
    u'broken_plural': 14,
    u'mamnou3_sarf': 15,
    u'relative': 16,
    u'w_suffix': 17,
    u'hm_suffix': 18,
    u'kal_prefix': 19,
    u'ha_suffix': 20,
    u'k_suffix': 21,
    u'annex': 22,
    u'definition': 23,
    u'note': 24,
}


class UnknownStemmer:
    """
        Arabic unknown word stemmer.
        Unkown words are stemmed as nouns with another dictionary
    """

    def __init__(self, debug=False):
        # create a stemmer object for stemming enclitics and procletics
        self.comp_stemmer = tashaphyne.stemming.ArabicLightStemmer()
        # configure the stemmer object
        self.comp_stemmer.set_infix_letters(snconst.COMP_INFIX_LETTERS)
        self.comp_stemmer.set_prefix_letters(snconst.COMP_PREFIX_LETTERS)
        self.comp_stemmer.set_suffix_letters(snconst.COMP_SUFFIX_LETTERS)
        self.comp_stemmer.set_max_prefix_length(snconst.COMP_MAX_PREFIX)
        self.comp_stemmer.set_max_suffix_length(snconst.COMP_MAX_SUFFIX)
        self.comp_stemmer.set_min_stem_length(snconst.COMP_MIN_STEM)
        self.comp_stemmer.set_prefix_list(snconst.COMP_PREFIX_LIST)
        self.comp_stemmer.set_suffix_list(snconst.COMP_SUFFIX_LIST)

        # create a stemmer object for stemming conjugated verb
        self.conj_stemmer = tashaphyne.stemming.ArabicLightStemmer()
        # configure the stemmer object
        self.conj_stemmer.set_infix_letters(snconst.CONJ_INFIX_LETTERS)
        self.conj_stemmer.set_prefix_letters(snconst.CONJ_PREFIX_LETTERS)
        self.conj_stemmer.set_suffix_letters(snconst.CONJ_SUFFIX_LETTERS)
        self.conj_stemmer.set_max_prefix_length(snconst.CONJ_MAX_PREFIX)
        self.conj_stemmer.set_max_suffix_length(snconst.CONJ_MAX_SUFFIX)
        self.conj_stemmer.set_min_stem_length(snconst.CONJ_MIN_STEM)
        self.conj_stemmer.set_prefix_list(snconst.CONJ_PREFIX_LIST)
        self.conj_stemmer.set_suffix_list(snconst.CONJ_SUFFIX_LIST)
        #word frequency dictionary
        self.wordfreq = wordfreqdictionaryclass.WordFreqDictionary(
            'wordfreq', wordfreqdictionaryclass.WORDFREQ_DICTIONARY_INDEX)
        # use the word frequency dictionary as a dictionary for unkonwn words
        self.noun_dictionary = self.wordfreq

        self.debug = debug

    def stemming_noun(self, noun):
        """
        Analyze word morphologically as noun
        @param noun: the input noun.
        @type noun: unicode.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        #~list_found = []
        detailed_result = []
        #~display_conj_result = False
        noun = noun.strip()
        noun_list = [noun]
        if noun.find(araby.ALEF_MADDA) >= 0:
            noun_list.append(
                noun.replace(araby.ALEF_MADDA,
                             araby.ALEF_HAMZA_ABOVE + araby.ALEF_HAMZA_ABOVE))


#            noun_list.append(HAMZA+ALEF+noun[1:])
        for noun in noun_list:
            list_seg_comp = self.comp_stemmer.segment(noun)
            list_seg_comp = verify_affix(noun, list_seg_comp,
                                         snconst.COMP_NOUN_AFFIXES)

            for seg in list_seg_comp:
                procletic = noun[:seg[0]]
                stem = noun[seg[0]:seg[1]]
                encletic = noun[seg[1]:]
                #~secondsuffix = u''
                #~proaffix = u'-'.join([procletic, encletic])
                if self.debug:
                    print("\t", "-".join([procletic, stem,
                                          encletic]).encode("utf8"))

                # ajusting nouns variant
                list_stem = [stem]
                if encletic != "":
                    #~annexing = True
                    if stem.endswith(araby.YEH):
                        list_stem.append(stem + araby.NOON)
                    elif stem.endswith(araby.WAW):
                        list_stem.append(stem + araby.NOON)
                    elif stem.endswith(araby.ALEF):
                        list_stem.append(stem[:-1] + araby.ALEF_MAKSURA)
                    elif stem.endswith(araby.TEH):
                        list_stem.append(stem[:-1] + araby.TEH_MARBUTA)
                #~else: annexing = False
        # stem reduced noun : level two
                result = []
                for stem in list_stem:
                    result += self.steming_second_level(
                        noun, stem, procletic, encletic)
                detailed_result += result
        return detailed_result  #list_found

    def steming_second_level(self, noun, noun2, procletic, encletic):
        """
        Analyze word morphologically by stemming the conjugation affixes.
        @param noun: the input noun.
        @type noun: unicode.
        @param noun2: the noun stemed from syntaxic affixes.
        @type noun2: unicode.
        @param procletic: the syntaxic prefixe extracted in the fisrt stage.
        @type procletic: unicode.
        @param encletic: the syntaxic suffixe extracted in the fisrt stage.
        @type encletic: unicode.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        detailed_result = []
        #segment the coinjugated verb
        list_seg_conj = self.conj_stemmer.segment(noun2)
        # verify affix compatibility
        list_seg_conj = verify_affix(noun2, list_seg_conj,
                                     snconst.NOMINAL_CONJUGATION_AFFIX)

        # add vocalized forms of suffixes
        list_seg_conj_voc = []
        for seg_conj in list_seg_conj:
            prefix_conj = noun2[:seg_conj[0]]
            stem_conj = noun2[seg_conj[0]:seg_conj[1]]
            suffix_conj = noun2[seg_conj[1]:]
            #~affix_conj = prefix_conj+'-'+suffix_conj
            # get all vocalized form of suffixes
            for vocalized_suffix in \
            snconst.CONJ_SUFFIX_LIST_TAGS[suffix_conj]['vocalized']:
                seg_conj_voc = {
                    'prefix': '',
                    'suffix': vocalized_suffix,
                    'stem': stem_conj
                }
                # verify compatibility between procletics and afix
                if (is_compatible_proaffix_affix(procletic, encletic,
                                                 vocalized_suffix)):
                    # verify the existing of a noun stamp in the dictionary
                    # if self.NOUN_DICTIONARY_STAMP.has_key(stamp):
                    # list_seg_conj2.append(seg_conj)
                    list_seg_conj_voc.append(seg_conj_voc)
        list_seg_conj = list_seg_conj_voc
        for seg_conj in list_seg_conj:
            prefix_conj = seg_conj['prefix']
            stem_conj = seg_conj['stem']
            suffix_conj = seg_conj['suffix']
            #~has_plural_suffix = ((u"جمع" in \
            #~snconst.CONJ_SUFFIX_LIST_TAGS[suffix_conj]['tags']) or\
            #~( u"مثنى" in snconst.CONJ_SUFFIX_LIST_TAGS[suffix_conj]['tags']))
            #print "has_plural", has_plural_suffix
            #~affix_conj = '-'.join([prefix_conj, suffix_conj])
            # noirmalize hamza before gessing  deffirents origines
            stem_conj = tashaphyne.normalize.normalize_hamza(stem_conj)
            # generate possible stems
            # add stripped letters to the stem to constitute possible noun list
            possible_noun_list = get_stem_variants(stem_conj, \
            prefix_conj, suffix_conj)
            # search the noun in the dictionary
            # we can return the tashkeel
            infnoun_form_list = []
            for infnoun in possible_noun_list:
                # get the noun and get all its forms from the dict
                # if the noun has plural suffix, don't look up
                # in broken plural dictionary
                infnoun_foundlist = self.noun_dictionary.lookup(
                    infnoun, 'unknown')
                infnoun_form_list += infnoun_foundlist
            for noun_tuple in infnoun_form_list:
                # noun_tuple = self.noun_dictionary.getEntryById(id)
                infnoun = noun_tuple['vocalized']
                original_tags = ()
                #~original = noun_tuple['vocalized']
                wordtype = noun_tuple['word_type']
                vocalized = vocalize(infnoun, procletic, prefix_conj, suffix_conj, encletic)
                #print "v", vocalized.encode('utf8')
                detailed_result.append(wordcase.WordCase({
                    'word':noun,
                    'affix': (procletic, prefix_conj, suffix_conj, encletic),
                    'stem':stem_conj,
                    'original':infnoun, #original,
                    'vocalized':vocalized,
                    'semivocalized':vocalized,
                    'tags':u':'.join(snconst.COMP_PREFIX_LIST_TAGS[procletic]['tags']\
                    +snconst.COMP_SUFFIX_LIST_TAGS[encletic]['tags']+\
                    snconst.CONJ_SUFFIX_LIST_TAGS[suffix_conj]['tags']),
                    'type':u':'.join(['Noun', wordtype]), #'Noun',
                    'freq':noun_tuple['freq'],
                    'originaltags':u':'.join(original_tags),
                    'syntax':'',
                }))

        return detailed_result

    def set_debug(self, debug):
        """
        Set the debug attribute to allow printing internal analysis results.
        @param debug: the debug value.
        @type debug: True/False.
        """
        self.debug = debug


def vocalize(noun, proclitic, prefix, suffix, enclitic):
    """
    Join the  noun and its affixes, and get the vocalized form
    @param noun: noun found in dictionary.
    @type noun: unicode.
    @param proclitic: first level prefix.
    @type proclitic: unicode.
    @param prefix: second level suffix.
    @type prefix: unicode.
    @param suffix: second level suffix.
    @type suffix: unicode.
    @param enclitic: first level suffix.
    @type enclitic: unicode.
    @return: vocalized word.
    @rtype: unicode.
    """
    enclitic_voc = snconst.COMP_SUFFIX_LIST_TAGS[enclitic]["vocalized"][0]
    proclitic_voc = snconst.COMP_PREFIX_LIST_TAGS[proclitic]["vocalized"][0]
    suffix_voc = suffix
    #adjust some some harakat

    #strip last if tanwin or harakat
    if noun[-1:] in araby.HARAKAT:
        noun = noun[:-1]
    #completate the dictionary word vocalization
    # this allow to avoid some missed harakat before ALEF
    # in the dictionary form of word, all alefat are preceded by Fatha
    #~noun = araby.complet
    #~ print "stem_unknown.vocalize; before", noun.encode('utf8');
    noun = noun.replace(araby.ALEF, araby.FATHA + araby.ALEF)
    #~ print "stem_unknown.vocalize; 2", noun.encode('utf8');

    noun = noun.replace(araby.ALEF_MAKSURA, araby.FATHA + araby.ALEF_MAKSURA)
    noun = re.sub(ur"(%s)+" % araby.FATHA, araby.FATHA, noun)

    # remove initial fatha if alef is the first letter
    noun = re.sub(ur"^(%s)+" % araby.FATHA, "", noun)
    #~ print "stem_unknown.vocalize; 3", noun.encode('utf8');

    #add shadda if the first letter is sunny and the prefix
    #ends by al definition
    if proclitic.endswith(araby.ALEF + araby.LAM) and araby.is_sun(noun[0]):
        noun = u''.join([noun[0], araby.SHADDA, noun[1:]])
        #strip the Skun from the lam
        if proclitic_voc.endswith(araby.SUKUN):
            proclitic_voc = proclitic_voc[:-1]
    noun = get_word_variant(noun, suffix)
    noun = get_word_variant(noun, enclitic)
    suffix_voc = get_suffix_variant(noun, suffix_voc, enclitic)
    return ''.join([proclitic_voc, prefix, noun, suffix_voc, enclitic_voc])


def is_compatible_proaffix_affix(procletic, encletic, suffix):
    """
    Verify if proaffixes (sytaxic affixes) are compatable
    with affixes (conjugation)
    @param procletic: first level prefix.
    @type procletic: unicode.
    @param encletic: first level suffix.
    @type encletic: unicode.
    @param suffix: second level suffix.
    @type suffix: unicode.
    @return: compatible.
    @rtype: True/False.
    """
    if procletic == u'' and encletic == u'':
        return True
    procletic_tags = snconst.COMP_PREFIX_LIST_TAGS[procletic]['tags']
    encletic_tags = snconst.COMP_SUFFIX_LIST_TAGS[encletic]['tags']
    #prefix_tags = CONJ_PREFIX_LIST_TAGS[procletic]['tags']
    suffix_tags = snconst.CONJ_SUFFIX_LIST_TAGS[suffix]['tags']
    if u"تعريف" in procletic_tags and u"مضاف" in suffix_tags and \
    u'منسوب' not in suffix_tags:
        return False
    if u"تعريف" in procletic_tags and u"تنوين" in suffix_tags:
        return False
    if u"مضاف" in encletic_tags and u"تنوين" in suffix_tags:
        return False
    if u"مضاف" in encletic_tags and u"لايضاف" in suffix_tags:
        return False
    if u"جر" in procletic_tags and u"مجرور" not in suffix_tags:
        return False
    return True


def get_suffix_variant(word, suffix, enclitic):
    """
    Get the suffix variant to be joined to the word.
    For example: word  = مدرس, suffix = ة, encletic = ي.
    The suffix is convert to Teh.
    @param word: word found in dictionary.
    @type word: unicode.
    @param suffix: second level suffix.
    @type suffix: unicode.
    @param enclitic: first level suffix.
    @type enclitic: unicode.
    @return: variant of suffix.
    @rtype: unicode.
    """
    enclitic_nm = araby.strip_tashkeel(enclitic)
    #if the word ends by a haraka
    if suffix.find(araby.TEH_MARBUTA) >= 0 and len(enclitic_nm) > 0:
        suffix = re.sub(araby.TEH_MARBUTA, araby.TEH, suffix)
    if enclitic_nm == u"" and word[-1:] in (
            araby.ALEF_MAKSURA, araby.YEH,
            araby.ALEF) and suffix in araby.HARAKAT:
        suffix = u""
    return suffix


def get_word_variant(word, suffix):
    """
    Get the word variant to be joined to the suffix.
    For example: word  = ةمدرس, suffix = ي. The word is converted to مدرست.
    @param word: word found in dictionary.
    @type word: unicode.
    @param suffix: suffix ( firts or second level).
    @type suffix: unicode.
    @return: variant of word.
    @rtype: unicode.
    """
    word_stem = word
    suffix_nm = araby.strip_tashkeel(suffix)
    #if the word ends by a haraka
    if word_stem[-1:] in araby.HARAKAT:
        word_stem = word_stem[:-1]
    if word_stem.endswith(araby.TEH_MARBUTA) and suffix_nm in (
            araby.ALEF + araby.TEH, araby.YEH + araby.TEH_MARBUTA, araby.YEH,
            araby.YEH + araby.ALEF + araby.TEH):
        word_stem = word_stem[:-1]
    elif word_stem.endswith(araby.TEH_MARBUTA) and suffix_nm != u"":
        word_stem = word_stem[:-1] + araby.TEH
    elif word_stem.endswith(araby.ALEF_MAKSURA) and suffix_nm != u"":
        word_stem = word_stem[:-1] + araby.YEH
    elif word_stem.endswith(araby.HAMZA) and suffix_nm != u"":
        if suffix.startswith(araby.DAMMA):
            word_stem = word_stem[:-1] + araby.WAW_HAMZA
        elif suffix.startswith(araby.KASRA):
            word_stem = word_stem[:-1] + araby.YEH_HAMZA
        elif (word_stem.endswith(araby.YEH + araby.HAMZA)
              or word_stem.endswith(araby.YEH + araby.SUKUN + araby.HAMZA)
             ) and suffix.startswith(araby.FATHATAN):
            word_stem = word_stem[:-1] + araby.YEH_HAMZA
    return word_stem


def get_stem_variants(stem, prefix, suffix):
    """
    Generate the Noun stem variants according to the affixes.
    For example مدرستي = >مدرست+ي  = > مدرسة +ي.
    Return a list of possible cases.
    @param stem: the input stem.
    @type stem: unicode.
    @param prefix: prefixe.
    @type prefix: unicode.
    @param suffix: suffixe.
    @type suffix: unicode.
    @return: list of stem variants.
    @rtype: list of unicode.
    """
    #some cases must have some correction
    #determinate the prefix and suffix types
    # create a list, the first item is the verb without changes
    prefix_possible_noun_list = set([stem])
    # Prefix
    prefix = araby.strip_tashkeel(prefix)
    suffix = araby.strip_tashkeel(suffix)
    possible_noun_list = prefix_possible_noun_list
    if suffix in (araby.ALEF + araby.TEH, araby.YEH + araby.TEH_MARBUTA,
                  araby.YEH, araby.YEH + araby.ALEF + araby.TEH):
        possible_noun = stem + araby.TEH_MARBUTA
        possible_noun_list.add(possible_noun)
    if suffix == "" or suffix == araby.YEH+araby.NOON or \
       suffix == araby.WAW+araby.NOON:
        possible_noun = stem + araby.YEH
        possible_noun_list.add(possible_noun)
    if stem.endswith(araby.YEH):
        possible_noun = stem[:-1] + araby.ALEF_MAKSURA
        possible_noun_list.add(possible_noun)
    #to be validated
    validated_list = possible_noun_list
    return validated_list


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


    #~return filter (lambda s: '-'.join([word[:s[0]],
    #~word[s[1]:]]) in affix_list, list_seg)
def validate_tags(noun_tuple, affix_tags):
    """
    Test if the given word from dictionary is compabilbe with affixes tags.
    @param noun_tuple: the input word attributes given from dictionary.
    @type noun_tuple: dict.
    @param affix_tags: a list of tags given by affixes.
    @type affix_tags:list.
    @param procletic: first level prefix vocalized.
    @type procletic: unicode.
    @param encletic_nm: first level suffix vocalized.
    @type encletic_nm: unicode.
    @param suffix_nm: first level suffix vocalized.
    @type suffix_nm: unicode.
    @return: if the tags are compatible.
    @rtype: Boolean.
    """
    #~ procletic = araby.strip_tashkeel(procletic)
    #~ encletic = encletic_nm
    #~ suffix = suffix_nm

    if u'تنوين' in affix_tags and noun_tuple['word_type'] == "noun_prop":
        return False
    return True
