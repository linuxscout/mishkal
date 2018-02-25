#!/usr/bin/python
# -*- coding = utf-8 -*-
#-----------------------------------------------------------------------
# Name:        stem_verb
# Purpose:     Arabic lexical analyser, provides feature for
#  stemming arabic word as verb
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-----------------------------------------------------------------------
"""
    Arabic verb stemmer
"""
#~ import re
if __name__ == '__main__':
    import sys
    sys.path.append('../support')
    sys.path.append('support')
    sys.path.append('..')
import pyarabic.araby as ar
import tashaphyne.stemming
import qalsadi.stem_verb_const as SVC
#~import analex_const
import libqutrub.classverb
import arramooz.arabicdictionary as arabicdictionary
import qalsadi.wordcase as wordcase

#~ import  stemmedword


class VerbStemmer:
    """
        Arabic verb stemmer
    """

    def __init__(self, debug=False):
        # create a stemmer object for stemming enclitics and proclitics
        self.comp_stemmer = tashaphyne.stemming.ArabicLightStemmer()

        # configure the stemmer object
        self.comp_stemmer.set_prefix_list(SVC.COMP_PREFIX_LIST)
        self.comp_stemmer.set_suffix_list(SVC.COMP_SUFFIX_LIST)

        # create a stemmer object for stemming conjugated verb
        self.conj_stemmer = tashaphyne.stemming.ArabicLightStemmer()

        # configure the stemmer object
        self.conj_stemmer.set_prefix_list(SVC.CONJ_PREFIX_LIST)
        self.conj_stemmer.set_suffix_list(SVC.CONJ_SUFFIX_LIST)
        # enable the last mark (Harakat Al-I3rab)
        self.allow_syntax_lastmark = True

        # To show statistics about verbs
        #~statistics = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0,
        #~10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0,
        #~}
        # affixes compatibility
        self.compatibility_cache = {}
        #~ self.verb_dict_cache = {}

        self.debug = debug
        self.cache_verb = {'verb': {}}

        self.verb_dictionary = arabicdictionary.ArabicDictionary("verbs")

        self.verb_stamp_pat = SVC.VERB_STAMP_PAT



    def stemming_verb(self, verb_in):
        """
        Stemming verb
        @param verb_in: given verb
        @type verb_in: unicode
        @return : stemmed words
        @rtype:
        """
        #~ list_found = []
        detailed_result = []
        verb_list = [
            verb_in,
        ] + get_verb_variants(verb_in)

        #list of segmented words
        word_segmented_list = []
        for verb in verb_list:

            list_seg_comp = self.comp_stemmer.segment(verb)
            for seg in list_seg_comp:
                proclitic = verb[:seg[0]]
                stem = verb[seg[0]:seg[1]]
                enclitic = verb[seg[1]:]
                #~ print "stem_verb affix 93", "-".join([proclitic, stem, enclitic]).encode('utf8')
                #~secondsuffix = u''
                # حالة الفعل المتعدي لمفعولين
                if enclitic in SVC.TABLE_DOUBLE_TRANSITIVE_SUFFIX:
                    firstsuffix = \
                    SVC.TABLE_DOUBLE_TRANSITIVE_SUFFIX[enclitic]['first']
                    enclitic = firstsuffix

                list_stem = [stem] + get_in_stem_variants(stem, enclitic)
                #if enclitic, then transitive is ok
                transitive_comp = bool(enclitic)
                for stm in list_stem:
                    word_seg = {
                        "verb": verb,
                        "pro": proclitic,
                        "enc": enclitic,
                        'stem_comp': stm,
                        'trans_comp': transitive_comp,
                    }
                    word_segmented_list.append(word_seg)

        # second level for segmented word
        tmp_list = []
        #~ print 'first level', verb_in, len(word_segmented_list)
        for word_seg in word_segmented_list:
            verb2 = word_seg['stem_comp']
            # stem reduced verb : level two
            #segment the conjugated verb
            list_seg_conj = self.conj_stemmer.segment(verb2)

            # verify affix compatibility
            list_seg_conj = verify_affix(verb2, list_seg_conj,
                                         SVC.VERBAL_CONJUGATION_AFFIX)
            # verify proclitics and enclitecs
            # verify length pof stem
            for seg_conj in list_seg_conj:
                if (seg_conj[1] - seg_conj[0]) <= 6:

                    #word seg in level 2
                    word_seg_l2 = word_seg.copy()
                    word_seg_l2["prefix"] = verb2[:seg_conj[0]]
                    word_seg_l2["stem_conj"] = verb2[seg_conj[0]:seg_conj[1]]
                    word_seg_l2["suffix"] = verb2[seg_conj[1]:]
                    tmp_list.append(word_seg_l2)

        # verify compatibilty between proclitic and affixes
        word_segmented_list = tmp_list
        #~ print 'compatibility', verb_in, len(tmp_list)
        tmp_list = []
        for word_seg in word_segmented_list:
            # verify compatibility between proclitics and affixes
            proclitic = word_seg['pro']
            enclitic = word_seg['enc']
            affix_conj = u"-".join([word_seg['prefix'], word_seg['suffix']])
            if self.__check_clitic_affix(proclitic, enclitic, affix_conj):
                tmp_list.append(word_seg.copy())

        #~ print 'stamp', verb_in, len(tmp_list)
        # verify existance of condidate verb by stamp
        word_segmented_list = tmp_list
        tmp_list = []
        for word_seg in word_segmented_list:
            # verify existance of condidate verb by stamp
            if self.verb_dictionary.exists_as_stamp(word_seg['stem_conj']):
                tmp_list.append(word_seg.copy())

        #~ print 'infinitive', verb_in, len(tmp_list)
        # get infinitive of condidate verbs
        word_segmented_list = tmp_list
        tmp_list = []
        for word_seg in word_segmented_list:
            # get infinitive of condidate verb by stamp

            # search the verb in the dictionary by stamp
            # if the verb exists in dictionary,
            # The transitivity is consedered
            # if is trilateral return its forms and Tashkeel
            # if not return forms without tashkeel,
            #because the conjugator can vocalized it,
            # we can return the tashkeel if we don't need the
            #conjugation step
            infverb_dict = self.__get_infinitive_verb_by_stem(
                word_seg['stem_conj'], word_seg['trans_comp'])
            #~ print "list possible verbs", len(infverb_dict)
            #~ for item in infverb_dict:
            #~ print item['verb']
            # filter verbs
            infverb_dict = self.__verify_infinitive_verbs(
                word_seg['stem_conj'], infverb_dict)

            for item in infverb_dict:
                #The haraka from is given from the dict
                word_seg_l3 = word_seg.copy()
                word_seg_l3['inf'] = item['verb']
                word_seg_l3['haraka'] = item['haraka']
                word_seg_l3['transitive'] = bool(item['transitive'] in ('y',
                                                                        1))
                tmp_list.append(word_seg_l3)
                # conjugation step

        #~ print repr(tmp_list).replace('},','},\n').decode("unicode-escape")
        #~ print 'conj', verb_in, len(tmp_list)
        # get conjugation for every infinitive verb
        word_segmented_list = tmp_list
        tmp_list = []
        for word_seg in word_segmented_list:
            # ToDo, conjugate the verb with affix,
            # if exists one verb which match, return it
            # تصريف الفعل مع الزوائد
            # إذا توافق التصريف مع الكلمة الناتجة
            # تعرض النتيجة
            one_correct_conj = self.__generate_possible_conjug(
                word_seg['inf'], word_seg['stem_comp'],
                word_seg['prefix'] + '-' + word_seg['suffix'],
                word_seg['haraka'], word_seg['pro'], word_seg['enc'],
                word_seg['transitive'])

            #~ print "len correct_conj", len(one_correct_conj)
            for conj in one_correct_conj:
                word_seg_l4 = word_seg.copy()
                word_seg_l4['conj'] = conj.copy()
                tmp_list.append(word_seg_l4)

        #~ print 'result', verb_in, len(tmp_list)
        # generate all resulted data
        word_segmented_list = tmp_list

        #~ tmp_list = []
        for word_seg in word_segmented_list:
            conj = word_seg['conj']
            vocalized, semivocalized = vocalize(
                conj['vocalized'], word_seg['pro'], word_seg['enc'])
            tag_type = 'Verb'
            original_tags = "y" if conj['transitive'] else "n"

            detailed_result.append(wordcase.WordCase({
                'word':word_seg['verb'],
                'affix': (word_seg['pro'], word_seg['prefix'], word_seg['suffix'], word_seg['enc']),
                'stem':word_seg['stem_conj'],
                'original':conj['verb'],
                'vocalized':vocalized,
                'semivocalized':semivocalized,
                'tags':u':'.join((conj['tense'], conj['pronoun'])+\
                SVC.COMP_PREFIX_LIST_TAGS[proclitic]['tags']+\
                SVC.COMP_SUFFIX_LIST_TAGS[enclitic]['tags']),#\
                'type':tag_type,
                'number': conj['pronoun_tags'].get('number', ''),
                'gender': conj['pronoun_tags'].get('gender', ''),
                'person': conj['pronoun_tags'].get('person', ''),
                'tense2': conj['tense_tags'].get('tense', ''),
                'voice': conj['tense_tags'].get('voice', ''),
                'mood': conj['tense_tags'].get('mood', ''),
                'confirmed': conj['tense_tags'].get('confirmed', ''),
                'transitive': conj['transitive'],
                'tense': conj['tense'],
                'pronoun': conj['pronoun'],
                'freq':'freqverb',
                'originaltags':original_tags,
                'syntax':'',
            }))

        return detailed_result

    def __get_infinitive_verb_by_stem(self, verb, transitive):
        """
        Get the infinitive verb form by given stem, and transitivity
        @param verb: the given verb
        @type verb; unicode
        @param transitive: tranitive or intransitive
        @type transitive: boolean
        @return : list of infinitive verbs
        @rtype: list of unicode
        """
        # verb key
        #~ verb_key = u":".join([verb, str(transitive)])
        #~ if verb_key in self.verb_dict_cache:
        #~ return self.verb_dict_cache[verb_key]
        # a solution by using verbs stamps
        liste = []
        #~ print (u"* ".join([verb,])).encode('utf8')
        verb_id_list = self.verb_dictionary.lookup_by_stamp(verb)

        if len(verb_id_list):
            for verb_tuple in verb_id_list:
                #~ print "*****",verb_tuple['transitive']
                liste.append({
                    'verb': verb_tuple['vocalized'],
                    'transitive': verb_tuple['transitive'],
                    'haraka': verb_tuple['future_type'],
                    "stamp": verb_tuple['stamped']
                })
        #~ print "vs, 296", liste
        # if the verb in dictionary is vi and the stemmed verb is vt,
        #~don't accepot
        listetemp = liste
        liste = []
        for item in listetemp:
            #~ #print item['transitive'], transitive
            if item['transitive'] in (u'y', 1) or not transitive:
                liste.append(item)
        #~ self.verb_dict_cache[verb_key] = liste
        return liste

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

    def __verify_infinitive_verbs(self, stem_conj, infverb_dict):
        """
        verify if given infinitive verbs are compatible with stem_conj
        @param stem_conj: the stemmed verbs without conjugation affixes.
        @type stem_conj: unicode.
        @param infverb_dict: list of given infinitive verbs,
        each item contain 'verb' and 'type'.
        @type infverb_dict: list of dicts.
        @return: filtred  infinitive verbs
        @rtype: list of dict
        """
        tmp = []
        stem_stamp = self.verb_stamp(stem_conj)
        for item in infverb_dict:
            if self.verb_stamp(item['stamp']) == stem_stamp:
                tmp.append(item)
        return tmp

    def verb_stamp(self, word):
        """
        generate a stamp for a verb,
        the verb stamp is different of word stamp, by hamza noralization
        remove all letters which can change form in the word :
        - ALEF,
        - YEH,
        - WAW,
        - ALEF_MAKSURA
        - SHADDA
        @return: stamped word
        """
        word = ar.strip_tashkeel(word)
        #The vowels are striped in stamp function
        word = ar.normalize_hamza(word)
        if word.startswith(ar.HAMZA):
            #strip The first hamza
            word = word[1:]
        # strip the last letter if is doubled
        if word[-1:] == word[-2:-1]:
            word = word[:-1]
        return self.verb_stamp_pat.sub('', word)

    def __check_clitic_affix(self, proclitic, enclitic, affix):
        """
        Verify if proaffixes (sytaxic affixes) are compatable with affixes
        (conjugation)
        @param proclitic: first level prefix.
        @type proclitic: unicode.
        @param enclitic: first level suffix.
        @type enclitic: unicode.
        @param affix: second level affix.
        @type affix: unicode.
        @return: compatible.
        @rtype: True/False.
        """
        # proaffix key
        comp_key = u":".join([proclitic, enclitic, affix])
        if comp_key in self.compatibility_cache:
            return self.compatibility_cache[comp_key]
        if not proclitic and not enclitic:
            return True
        else:
            proclitic_compatible = False
            if not proclitic:
                proclitic_compatible = True
            elif proclitic in SVC.EXTERNAL_PREFIX_TABLE:
                #~ elif SVC.EXTERNAL_PREFIX_TABLE.has_key(proclitic):
                if affix == '-':
                    proclitic_compatible = True
                else:
                    for item in SVC.TABLE_AFFIX.get(affix, []):
                        #the tense item[0]
                        if item[0] in SVC.EXTERNAL_PREFIX_TABLE.get(
                                proclitic, ''):
                            proclitic_compatible = True
                            break
                    else:
                        proclitic_compatible = False
            if proclitic_compatible:
                if not enclitic:
                    self.compatibility_cache[comp_key] = True
                    return True
                elif enclitic in SVC.EXTERNAL_SUFFIX_TABLE:
                    #~ elif SVC.EXTERNAL_SUFFIX_TABLE.has_key(enclitic):
                    if affix == '-':
                        self.compatibility_cache[comp_key] = True
                        return True
                    else:
                        for item in SVC.TABLE_AFFIX.get(affix, []):
                            #the tense item[0]
                            if item[1] in SVC.EXTERNAL_SUFFIX_TABLE.get(
                                    enclitic, ''):
                                #~ return True
                                break
                        else:
                            self.compatibility_cache[comp_key] = False
                            return False
                        self.compatibility_cache[comp_key] = True
                        return True
        self.compatibility_cache[comp_key] = False
        return False

    def __check_clitic_tense(self, proclitic, enclitic, tense, pronoun,
                             transitive):
        """
        test if the given tenses are compatible with proclitics
        """
        # proaffix key
        comp_key = u":".join(
            [proclitic, enclitic, tense, pronoun,
             str(transitive)])
        if comp_key in self.compatibility_cache:
            return self.compatibility_cache[comp_key]
        # إذا كان الزمن مجهولا لا يرتبط مع الفعل اللازم
        if not transitive and tense in SVC.qutrubVerbConst.TablePassiveTense:
            self.compatibility_cache[comp_key] = False
            return False
        if not proclitic and not enclitic:
            self.compatibility_cache[comp_key] = True
            return True
        # The passive tenses have no enclitics
        #ﻷزمنة المجهولة ليس لها ضمائر متصلة في محل نصب مفعول به
        #لأنّ مفعولها يصبح نائبا عن الفاعل

        if enclitic and tense in SVC.qutrubVerbConst.TablePassiveTense:
            self.compatibility_cache[comp_key] = False
            return False

        #~ elif enclitic and think_trans and pronoun
        # لا سابقة
        # أو سابقة ، والزمن مسموح لها
        # لا لاحقة
        #أو زمن مسموح لتلك اللاحقة
        elif ((not proclitic
               or tense in SVC.EXTERNAL_PREFIX_TABLE.get(proclitic, ''))
              and (not enclitic
                   or pronoun in SVC.EXTERNAL_SUFFIX_TABLE.get(enclitic, ''))):
            self.compatibility_cache[comp_key] = True
            return True

        else:
            self.compatibility_cache[comp_key] = False
            return False

    def __generate_possible_conjug(self,
                                   infinitive_verb,
                                   unstemed_verb,
                                   affix,
                                   future_type=ar.FATHA,
                                   extern_prefix="-",
                                   extern_suffix="-",
                                   transitive=True):
        """
        generate possible conjugation for given verb to be stemmed
        """
        ##    future_type = FATHA
        #~ transitive = True
        list_correct_conj = []
        if infinitive_verb == "" or unstemed_verb == "" or affix == "":
            return set()
        vbc = libqutrub.classverb.VerbClass(infinitive_verb, transitive,
                                            future_type)
        # الألف ليست جزءا من السابقة، لأنها تستعمل لمنع الابتداء بساكن
        # وتصريف الفعل في الامر يولده
        if affix.startswith(ar.ALEF):
            affix = affix[1:]
        # get all tenses to conjugate the verb one time
        tenses = []
        if affix in SVC.TABLE_AFFIX:
            for pair in SVC.TABLE_AFFIX[affix]:
                tenses.append(pair[0])  #tense = pair[0]
        tenses = list(set(tenses))  # avoid duplicata

        if affix in SVC.TABLE_AFFIX:
            for pair in SVC.TABLE_AFFIX[affix]:
                tense = pair[0]
                pronoun = pair[1]
                test = self.__check_clitic_tense(extern_prefix, extern_suffix,
                                                 tense, pronoun, transitive)
                #~ print "stem_verb 529", (u", ".join([extern_prefix, extern_suffix,
                #~ tense, pronoun, str(transitive), "test",str(test)])).encode('utf8')
                if test:

                    conj_vocalized = vbc.conjugate_tense_for_pronoun(
                        tense, pronoun)
                    #strip all marks and shadda
                    conj_nm = ar.strip_tashkeel(conj_vocalized)
                    if conj_nm == unstemed_verb:
                        list_correct_conj.append({
                            'verb':
                            infinitive_verb,
                            'tense':
                            tense,
                            'pronoun':
                            pronoun,
                            'pronoun_tags':
                            vbc.get_pronoun_features(pronoun),
                            'tense_tags':
                            vbc.get_tense_features(tense),
                            'vocalized':
                            conj_vocalized,
                            'unvocalized':
                            conj_nm,
                            'transitive':
                            transitive
                        })
        return list_correct_conj


def verify_affix(word, list_seg, affix_list):
    """
    Verify possible affixes in the resulted segments
    according to the given affixes list.
    @param word: the input word.
    @type word: unicode.
    @param list_seg: list of word segments indexes (numbers).
    @type list_seg: list of pairs.
    @return: list of acceped segments.
    @rtype: list of pairs.
    """
    #~ for s in list_seg:
    #~ print "affix", '-'.join([word[:s[0]],word[s[0]:s[1]], word[s[1]:]])
    return [
        s for s in list_seg
        if '-'.join([word[:s[0]], word[s[1]:]]) in affix_list
    ]

def get_verb_variants(verb):
    """ return modified forms of input verb"""
    verb_list = []
    #cases like verb started with Alef madda, it can ءا or أأ
    if verb.startswith(ar.ALEF_MADDA):
        verb_list.append(ar.ALEF_HAMZA_ABOVE + ar.ALEF_HAMZA_ABOVE \
        +verb[1:])
        verb_list.append(ar.HAMZA + ar.ALEF + verb[1:])
    return verb_list

def get_in_stem_variants(stem, enclitic):
    """ return modified forms of input stem"""
    list_stem = []
    if enclitic:
        if stem.endswith(ar.TEH + ar.MEEM + ar.WAW):
            list_stem.append(stem[:-1])
        elif stem.endswith(ar.WAW):
            list_stem.append(stem + ar.ALEF)
        elif stem.endswith(ar.ALEF):
            list_stem.append(stem[:-1] + ar.ALEF_MAKSURA)
    if stem.startswith(ar.ALEF_MADDA):
        # االبداية بألف مد
        list_stem.append(ar.ALEF_HAMZA_ABOVE + \
        ar.ALEF_HAMZA_ABOVE + stem[1:])
        list_stem.append(ar.HAMZA + ar.ALEF + stem[1:])
    return list_stem

def get_enclitic_variant(word, enclitic):
    """
    Get the enclitic variant to be joined to the word.
    For example: word  =  أرجِهِ , enclitic = هُ.
    The enclitic  is convert to HEH+ KAsra.
    اعبارة في مثل أرجه وأخاه إلى يم الزينة
    @param word: word found in dictionary.
    @type word: unicode.
    @param enclitic: first level suffix vocalized.
    @type enclitic: unicode.
    @return: variant of enclitic.
    @rtype: unicode.
    """
    #if the word ends by a haraka
    if enclitic == ar.HEH+ar.DAMMA and (word.endswith(ar.KASRA)\
     or word.endswith(ar.YEH)):
        enclitic = ar.HEH + ar.KASRA
    return enclitic


def vocalize(verb, proclitic, enclitic):
    """
    Join the  verb and its affixes, and get the vocalized form
    @param verb: verb found in dictionary.
    @type verb: unicode.
    @param proclitic: first level prefix.
    @type proclitic: unicode.
    @param enclitic: first level suffix.
    @type enclitic: unicode.
    @return: (vocalized word, semivocalized).
    @rtype: (unicode, unicode).
    """
    enclitic_voc = SVC.COMP_SUFFIX_LIST_TAGS[enclitic]["vocalized"][0]
    enclitic_voc = get_enclitic_variant(verb, enclitic_voc)
    proclitic_voc = SVC.COMP_PREFIX_LIST_TAGS[proclitic]["vocalized"][0]
    #suffix_voc = suffix #CONJ_SUFFIX_LIST_TAGS[suffix]["vocalized"][0]
    # لمعالجة حالة ألف التفريق
    if enclitic and verb.endswith(ar.WAW + ar.ALEF):
        verb = verb[:-1]
    if enclitic and verb.endswith(ar.ALEF_MAKSURA):
        verb = verb[:-1] + ar.ALEF

    vocalized = ''.join([proclitic_voc, verb, enclitic_voc])
    semivocalized = ''.join(
        [proclitic_voc, ar.strip_lastharaka(verb), enclitic_voc])
    return (vocalized, semivocalized)


def mainly():
    """
    Test main"""
    #ToDo: use the full dictionary of arramooz
    wordlist = [
        #~ u'يضرب',
        u'يضربه',
        u'يضربك',
        #~ u"استقلّ",
        u'استقل',
        u'ويستخدمونها',
    ]
    verbstemmer = VerbStemmer()
    verbstemmer.set_debug(True)
    for word in wordlist:
        verbstemmer.conj_stemmer.segment(word)
        print(verbstemmer.conj_stemmer.get_affix_list())
    for word in wordlist:
        result = verbstemmer.stemming_verb(word)
        for analyzed in result:
            #~ print(repr(analyzed).encode('utf8'))
            #~ print(u'\n'.join(analyzed.__dict__.keys()))
            for key in analyzed.__dict__.keys():
                print(u'\t'.join([key, unicode(
                    analyzed.__dict__[key])]).encode('utf8'))
            print()
            print()


#Class test
if __name__ == '__main__':
    mainly()
