#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------
# Name:        stem_stop
# Purpose:     Arabic lexical analyser, provides feature for 
#~stemming arabic word as stop
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------
"""
    Arabic stop stemmer
"""
import re
import pyarabic.araby as araby
import tashaphyne.stemming
import tashaphyne.normalize
import qalsadi.stem_stopwords_const as ssconst
import arramooz.stopwordsdictionaryclass  as stopwordsdictionaryclass  
import qalsadi.wordcase as wordcase

class StopWordStemmer:
    """
        Arabic stop stemmer
    """
    def __init__(self, debug = False):
        # create a stemmer object for stemming enclitics and procletics
        self.comp_stemmer = tashaphyne.stemming.ArabicLightStemmer()
        # configure the stemmer object
        self.comp_stemmer.set_prefix_list(ssconst.COMP_PREFIX_LIST)
        self.comp_stemmer.set_suffix_list(ssconst.COMP_SUFFIX_LIST)
        # create a stemmer object for stemming conjugated verb
        self.conj_stemmer = tashaphyne.stemming.ArabicLightStemmer()
        # configure the stemmer object
        self.conj_stemmer.set_prefix_list(ssconst.CONJ_PREFIX_LIST)
        self.conj_stemmer.set_suffix_list(ssconst.CONJ_SUFFIX_LIST)

        # enable the last mark (Harakat Al-I3rab) 
        self.allow_syntax_lastmark = True 

        # stop dictionary
        #~self.stop_dictionary = stopwordsdictionaryclass.StopWordsDictionary("stopwords")   
        self.stop_dictionary = stopwordsdictionaryclass.StopWordsDictionary("classedstopwords")   

        # allow to print internal results.
        self.cache_dict_search = {}
        self.cache_affixes_verification = {}
        self.debug = debug

    def stemming_stopword(self, stop):
        """
        Analyze word morphologically as stop
        @param stop: the input stop.
        @type stop: unicode.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """    
        #~list_found = []
        detailed_result = []
        stop_list = [stop,]
        # if the word contains ALEF8MADDA, we convert it into 2 HAMZA above ALEF
        if araby.ALEF_MADDA in stop:
            stop_list.append(stop.replace(araby.ALEF_MADDA, 
            araby.ALEF_HAMZA_ABOVE*2))

        for stop in stop_list:
            list_seg_comp = self.comp_stemmer.segment(stop)
            list_seg_comp = verify_affix(stop, list_seg_comp, 
            ssconst.COMP_STOPWORDS_AFFIXES)
            # treat multi vocalization encletic
            #~list_seg_comp_voc = []
            for seg in list_seg_comp:
                procletic = stop[:seg[0]]
                stem = stop[seg[0]:seg[1]]
                encletic_nm = stop[seg[1]:]

                # ajusting stops variant
                list_stem = [stem]
                if encletic_nm: #  != ""
                    if stem.endswith(araby.ALEF):
                        list_stem.append(stem[:-1]+araby.ALEF_MAKSURA)
                    elif stem.endswith(araby.YEH):
                        list_stem.append(stem[:-1]+araby.ALEF_MAKSURA)
                    elif stem.endswith(araby.TEH):
                        list_stem.append(stem[:-1]+araby.TEH_MARBUTA)
                # treat gemination cases
                    if encletic_nm.startswith(araby.YEH):
                        list_stem.append(stem+araby.YEH)
                    elif encletic_nm.startswith(araby.NOON):
                        list_stem.append(stem+araby.NOON)

        # stem reduced stop : level two
                for stem in list_stem:
                    detailed_result.extend(self.steming_second_level(stop, 
                    stem, procletic, encletic_nm))
        return detailed_result #list_found
        

    def steming_second_level(self, stop, stop2, procletic, encletic_nm):
        """
        Analyze word morphologically by stemming the conjugation affixes.
        @param stop: the input stop.
        @type stop: unicode.
        @param stop2: the stop stemed from syntaxic affixes.
        @type stop2: unicode.
        @param procletic: the syntaxic prefixe extracted in the fisrt stage.
        @type procletic: unicode.
        @param encletic: the syntaxic suffixe extracted in the fisrt stage.
        @type encletic: unicode.
        @param encletic_nm: the syntaxic suffixe extracted in the 
        first stage (not vocalized).
        @type encletic_nm: unicode.        
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """    
        detailed_result = []
        #segment the coinjugated verb
        list_seg_conj = self.conj_stemmer.segment(stop2)
        # verify affix compatibility
        list_seg_conj = verify_affix(stop2, list_seg_conj, ssconst.STOPWORDS_CONJUGATION_AFFIX)
        # add vocalized forms of suffixes
        # and create the real affixes from the word
        #~list_seg_conj_voc = []
        for seg_conj in list_seg_conj:
            stem_conj = stop2[seg_conj[0]:seg_conj[1]]
            suffix_conj_nm = stop2[seg_conj[1]:]

            # noirmalize hamza before gessing  differents origines
            #~stem_conj = araby.normalize_hamza(stem_conj)

            # generate possible stems
            # add stripped letters to the stem to constitute possible stop list
            possible_stop_list = get_stem_variants(stem_conj, suffix_conj_nm)

            # search the stop in the dictionary
            # we can return the tashkeel
            infstop_form_list = []
            for infstop in set(possible_stop_list):
                # get the stop and get all its forms from the dict
                # if the stop has plural suffix, don't look up in 
                #broken plural dictionary
                if not self.cache_dict_search.has_key(infstop):
                    infstop_foundlist = self.stop_dictionary.lookup(infstop)
                    self.cache_dict_search[infstop] = create_dict_word(
                    infstop_foundlist)
                else: 
                    infstop_foundlist = self.cache_dict_search[infstop]        
                infstop_form_list.extend(infstop_foundlist)
            for stop_tuple in infstop_form_list:
                # stop_tuple = self.stop_dictionary.getEntryById(id)
                original = stop_tuple['vocalized']

                #test if the  given word from dictionary accept those
                # tags given by affixes
                # دراسة توافق الزوائد مع خصائص الاسم،
                # مثلا هل يقبل الاسم التأنيث.
                #~if validate_tags(stop_tuple, affix_tags, procletic, encletic_nm, suffix_conj_nm):
                for vocalized_encletic in ssconst.COMP_SUFFIX_LIST_TAGS[encletic_nm]['vocalized']:
                    for vocalized_suffix in ssconst.CONJ_SUFFIX_LIST_TAGS[suffix_conj_nm]['vocalized']:
                        # affixes tags contains prefixes and suffixes tags
                        affix_tags = ssconst.COMP_PREFIX_LIST_TAGS[procletic]['tags'] \
                                  +ssconst.COMP_SUFFIX_LIST_TAGS[vocalized_encletic]['tags'] \
                                  +ssconst.CONJ_SUFFIX_LIST_TAGS[vocalized_suffix]['tags']                            
                     ## verify compatibility between procletics and affix
                        if validate_tags(stop_tuple, affix_tags, procletic, vocalized_encletic , vocalized_suffix)  and \
                        (self.is_compatible_proaffix_affix(stop_tuple, procletic, vocalized_encletic, vocalized_suffix)):

                            vocalized, semi_vocalized = vocalize(original, procletic,  vocalized_suffix, vocalized_encletic)
                            vocalized = ajust_vocalization(vocalized)
                            #ToDo:
                            # if the stop word is inflected or not 
                            is_inflected = u"مبني" if stop_tuple['is_inflected'] == 0 else u"معرب"
                            #add some tags from dictionary entry as 
                            # use action and object_type
                            original_tags = u":".join ( [stop_tuple['word_type'], stop_tuple['word_class'],is_inflected, 
                                         stop_tuple['action'],] )
                            #~print "STOP_TUPEL[action]:", stop_tuple['action'].encode("utf8")
                            # generate word case
                            detailed_result.append(wordcase.WordCase({
                            'word':stop, 
                            'affix': (procletic, '', vocalized_suffix, 
                            vocalized_encletic),
                            'stem':      stem_conj, 
                            'original':  original, 
                            'vocalized': vocalized, 
                            'semivocalized':semi_vocalized,
                            'tags':      u':'.join(affix_tags), 
                            'type':      u':'.join( ['STOPWORD', stop_tuple['word_type']]),  
                            'freq':'freqstopword', # to note the frequency type 
                            'originaltags': original_tags,
                            "action":  stop_tuple['action'],
                            "object_type": stop_tuple['object_type'],
                            "need":  stop_tuple['need'], 
                            'syntax':'', 
                            }))
        return detailed_result








    def is_compatible_proaffix_affix(self, stop_tuple, procletic, encletic, 
    suffix):
        """
        Verify if proaffixes (sytaxic affixes) are compatable
        with affixes ( conjugation) 
        @param procletic: first level prefix.
        @type procletic: unicode.
        @param encletic: first level suffix.
        @type encletic: unicode.
        @param suffix: second level suffix.
        @type suffix: unicode.
        @return: compatible.
        @rtype: True/False.
        """ 
        #if not procletic and not encletic:  return True
        #use cache for affix verification
        affix = u'-'.join([procletic, encletic, suffix])
        if affix in self.cache_affixes_verification:
            return self.cache_affixes_verification[affix]
            
        # get procletics and enclitics tags
        procletic_tags = ssconst.COMP_PREFIX_LIST_TAGS[procletic]['tags']
        encletic_tags = ssconst.COMP_SUFFIX_LIST_TAGS[encletic]['tags']
        # in stops there is no prefix 
        suffix_tags = ssconst.CONJ_SUFFIX_LIST_TAGS[suffix]['tags']        

        if u"تعريف" in procletic_tags and u"مضاف" in suffix_tags :
            self.cache_affixes_verification[affix] = False
        elif u"تعريف" in procletic_tags and u"تنوين" in suffix_tags:
            self.cache_affixes_verification[affix] = False


    # الجر  في حالات الاسم المعرفة بال أو الإضافة إلى ضمير أو مضاف إليه
    # مما يعني لا يمكن تطبيقها هنا
        elif u"مضاف" in encletic_tags and u"تنوين" in suffix_tags:
            self.cache_affixes_verification[affix] = False
        elif u"مضاف" in encletic_tags and u"لايضاف" in suffix_tags:
            self.cache_affixes_verification[affix] = False
        #~elif u"جر" in procletic_tags and u"مجرور" not in suffix_tags:
            #~self.cache_affixes_verification[affix] = False
#ستعمل في حالة كسر هاء الضمير في الجر            

        elif  bool(u"لايجر" in encletic_tags) and  bool(u"مجرور" in \
        suffix_tags) :
            self.cache_affixes_verification[affix] = False
        elif  bool(u"مجرور" in encletic_tags) and  not bool(u"جر" in \
        stop_tuple['word_class']) :
            self.cache_affixes_verification[affix] = False             
        elif  bool(u"مجرور" in encletic_tags) and  not bool(u"مجرور" in \
        suffix_tags) :
            self.cache_affixes_verification[affix] = False 
              
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
    Generate the Stop stem variants according to the affixes.
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
    
    possible_stop_list = set([stem,])
    if not suffix_nm  or suffix_nm in (araby.YEH+araby.NOON, 
    araby.WAW+araby.NOON):
        possible_stop = stem+araby.YEH
        possible_stop_list.add(possible_stop)
    if stem.endswith(araby.YEH):
        possible_stop = stem[:-1]+araby.ALEF_MAKSURA
        possible_stop_list.add(possible_stop)
    #to be validated
    validated_list = possible_stop_list
    return validated_list

def get_suffix_variants(word, suffix, enclitic):
    """
    Get the suffix variant to be joined to the word.
    For example: word = مدرس, suffix = ة, encletic = ي. 
    The suffix is converted to Teh.
    @param word: word found in dictionary.
    @type word: unicode.
    @param suffix: second level suffix.
    @type suffix: unicode.
    @param enclitic: first level suffix.
    @type enclitic: unicode.        
    @return: variant of suffixes  (vocalized suffix and vocalized 
    suffix without I'rab short mark).
    @rtype: (unicode, unicode)
    """
    enclitic_nm = araby.strip_tashkeel(enclitic)
    newsuffix = suffix #default value
    #if the word ends by a haraka
    if     not enclitic_nm and word[-1:] in (araby.ALEF_MAKSURA, 
    araby.YEH, araby.ALEF) and araby.is_haraka(suffix):
        newsuffix = u""

    #gererate the suffix without I'rab short mark
    # here we lookup with given suffix because the new suffix is 
    # changed and can be not found in table
    if u'متحرك' in ssconst.CONJ_SUFFIX_LIST_TAGS[suffix]['tags']:
        suffix_non_irab_mark = araby.strip_lastharaka(newsuffix)
    else:
        suffix_non_irab_mark = newsuffix


    return newsuffix, suffix_non_irab_mark




def get_enclitic_variants(word, suffix, enclitic):
    """
    Get the enclitic variant to be joined to the word.
    For example: word = عن, suffix = , encletic = ني. 
    The word and enclitic are geminated.
    @param word: word found in dictionary.
    @type word: unicode.
    @param suffix: second level suffix.
    @type suffix: unicode.
    @param enclitic: first level suffix.
    @type enclitic: unicode.        
    @return: variant of suffixes  (vocalized suffix and vocalized 
    suffix without I'rab short mark).
    @rtype: (unicode, unicode)
    """
    #enclitic_nm = araby.strip_tashkeel(enclitic)
    #newsuffix = suffix #default value
    #if the word ends by a haraka
    # الإدغام في النون والياء في مثل فيّ، إليّ، عنّا ، منّا 
    if enclitic.startswith(araby.NOON) and word.endswith(araby.NOON) :
        enclitic = enclitic[1:] + araby.SHADDA
        print "xxxxxxxxxxx--1"
    if enclitic.startswith(araby.KASRA + araby.YEH) and word.endswith(araby.YEH)  :
        enclitic = enclitic[1:] + araby.SHADDA
        print "xxxxxxxxxxx--2"

    return enclitic

def get_word_variant(word, suffix):
    """
    Get the word variant to be joined to the suffix.
    For example: word = مدرسة, suffix = ي. The word is converted to مدرست.
    @param word: word found in dictionary.
    @type word: unicode.
    @param suffix: suffix ( firts or second level).
    @type suffix: unicode.
    @return: variant of word.
    @rtype: unicode.
    """
    word_stem = word
    suffix_nm = araby.strip_tashkeel(suffix)

    # تحويل الألف المقصورة إلى ياء في مثل إلى => إليك
    if word_stem.endswith(araby.ALEF_MAKSURA) and suffix_nm :
        if word_stem == u"سِوَى":
            word_stem = word_stem[:-1]+araby.ALEF
        else: 
            word_stem = word_stem[:-1]+araby.YEH + araby.SUKUN
    # تحويل الهمزة حسب موقعها           
    elif word_stem.endswith(araby.HAMZA) and suffix_nm :
        if suffix.startswith(araby.DAMMA):
            word_stem = word_stem[:-1] + araby.WAW_HAMZA
        elif suffix.startswith(araby.KASRA):
            word_stem = word_stem[:-1] + araby.YEH_HAMZA




    # this option is not used with stop words, because most of them are not inflected مبني
    #if the word ends by a haraka strip the haraka if the suffix is not null
    if suffix and suffix[0] in araby.HARAKAT:
        word_stem = araby.strip_lastharaka(word_stem)


    # الإدغام في النون والياء في مثل فيّ، إليّ، عنّا ، منّا 
    if suffix.startswith(araby.NOON) and word.endswith(araby.NOON + araby.SUKUN) :
        word_stem = araby.strip_lastharaka(word_stem)
    elif suffix.startswith(araby.KASRA + araby.YEH) and word.endswith(araby.YEH + araby.SUKUN)  :
        word_stem = araby.strip_lastharaka(word_stem)
         
    return word_stem
        
def vocalize( stop, proclitic,  suffix, enclitic):
    """
    Join the  stop and its affixes, and get the vocalized form
    @param stop: stop found in dictionary.
    @type stop: unicode.
    @param proclitic: first level prefix.
    @type proclitic: unicode.

    @param suffix: second level suffix.
    @type suffix: unicode.
    @param enclitic: first level suffix.
    @type enclitic: unicode.        
    @return: vocalized word.
    @rtype: unicode.
    """
    # procletic have only an uniq vocalization in arabic
    proclitic_voc = ssconst.COMP_PREFIX_LIST_TAGS[proclitic]["vocalized"][0]
    # enclitic can have many vocalization in arabic
    # like heh => عليهِ سواهُ
    # in this stage we consider only one,
    # the second situation is ajusted by vocalize_ajust
    enclitic_voc = ssconst.COMP_SUFFIX_LIST_TAGS[enclitic]["vocalized"][0]
    suffix_voc = suffix#CONJ_SUFFIX_LIST_TAGS[suffix]["vocalized"][0]

    
    # generate the word variant for some words witch ends by special 
    #letters like Alef_maksura, or hamza, 
    #the variant is influed by the suffix harakat, 
    # for example إلي +ك = إلى+ك
    stop = get_word_variant(stop, suffix+enclitic)

    # generate the suffix variant. if the suffix is removed for some letters like Alef Maqsura and Yeh 
    # for example        
    suffix_voc, suffix_non_irab_mark = get_suffix_variants(stop,
     suffix_voc, enclitic_voc)

    # generate the suffix variant. if the suffix is Yeh or Noon for geminating 
    # for example عنّي = عن+ني
    enclitic_voc = get_enclitic_variants(stop, suffix_voc, enclitic_voc)

    # generate the non vacalized end word: the vocalized word 
    # without the I3rab Mark
    # if the suffix is a short haraka 
    word_non_irab_mark = ''.join([ proclitic_voc,  stop, 
         suffix_non_irab_mark,   enclitic_voc])             
        
    word_vocalized = ''.join([proclitic_voc, stop, suffix_voc, 
       enclitic_voc])
    return word_vocalized, word_non_irab_mark 

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
    return [s for s in list_seg if '-'.join([word[:s[0]], word[s[1]:]]) in affix_list]

def validate_tags(stop_tuple, affix_tags, procletic, encletic_nm ,
 suffix_nm):
    """
    Test if the given word from dictionary is compabilbe with affixes tags.
    @param stop_tuple: the input word attributes given from dictionary.
    @type stop_tuple: dict.
    @param affix_tags: a list of tags given by affixes.
    @type affix_tags:list.
    @param procletic: first level prefix vocalized.
    @type procletic: unicode.        
    @param encletic_nm: first level suffix vocalized.
    @type encletic_nm: unicode.
    @param suffix_nm: first level suffix vocalized.
    @type suffix_nm: unicode.        
    @return: if the tags are compaatible.
    @rtype: Boolean.
    """
    procletic = araby.strip_tashkeel(procletic)
    encletic = encletic_nm
    suffix = suffix_nm

    if u"تعريف" in affix_tags and not stop_tuple['definition']:
        return False;
    if u"تعريف" in affix_tags and stop_tuple['defined']:
        return False;        
    #~preposition 
    if  u'جر'in affix_tags and not stop_tuple['preposition']:
        return False 
    if u"متحرك" in affix_tags  and  not stop_tuple['is_inflected']:
        return False  
    
    if u"مضاف" in affix_tags and not stop_tuple['pronoun']:
        return False 
    if u"مضاف" in affix_tags and stop_tuple['defined']:
        return False 
    # حين تكون الأداة متحركة فهي تقبل الاتصال بياء المتكلم مباشرة
    if encletic_nm == araby.YEH  and  not stop_tuple['is_inflected']:
        return False
    # noon wiqaya نون الوقاية
    # حين تكون الأداة غير متحركة فهي تلزم  الاتصال بنون الوقاية قبل ياء المتكلم مباشرة
    if u"وقاية" in affix_tags  and  ( stop_tuple['is_inflected'] or stop_tuple['word'].endswith(araby.YEH)) :
        return False
        #~interrog
    if u"استفهام" in affix_tags and not stop_tuple['interrog']:
        return False          
        #~conjugation                   
        #~qasam 

    
    if u"قسم" in affix_tags and not stop_tuple['qasam']:
        return False           
        #~
        #~defined 
        #~is_inflected  
        #~tanwin
    if u"تنوين" in affix_tags and not stop_tuple['tanwin']:
        return False        
        #~action  
        #~object_type  
        #~need 
    return True

def create_dict_word(dict_entries_list):
    """
    Create a list of dictWord objects from dictionary entries
    @param dict_entries_list: a list of entiers from lexicon
    @type  dict_entries_list: list of dict
    @return: a list of dictWord object
    @rtype: a list of dictWord object
    """
    return dict_entries_list


def ajust_vocalization( vocalized):
    """
    ajust vocalization 
    Temporary function
    @param vocalized: vocalized word.
    @type vocalized: unicode.        
    @return: ajusted vocalized word.
    @rtype: unicode.
    """
    ajusted = ssconst.AJUSTMENT.get(vocalized, vocalized)
    
    return ajusted
