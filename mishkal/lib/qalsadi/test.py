#!/usr/bin/python
# -*- coding: UTF-8 -*-
import tashaphyne2
import stem_verb_const
conjStemmer=tashaphyne2.stemming.ArabicLightStemmer();
#conjStemmer=stemming2.ArabicLightStemmer();

# configure the stemmer object
conjStemmer.set_infix_letters(stem_verb_const.CONJ_INFIX_LETTERS);
conjStemmer.set_prefix_letters(stem_verb_const.CONJ_PREFIX_LETTERS);
conjStemmer.set_suffix_letters(stem_verb_const.CONJ_SUFFIX_LETTERS);
conjStemmer.set_max_prefix_length(stem_verb_const.CONJ_MAX_PREFIX);
conjStemmer.set_max_suffix_length(stem_verb_const.CONJ_MAX_SUFFIX);
conjStemmer.set_min_stem_length(stem_verb_const.CONJ_MIN_STEM);
conjStemmer.set_prefix_list(stem_verb_const.CONJ_PREFIX_LIST);
conjStemmer.set_suffix_list(stem_verb_const.CONJ_SUFFIX_LIST);
print 'stem_verb_const.CONJ_PREFIX_LETTERS', stem_verb_const.CONJ_PREFIX_LETTERS.encode('utf8');


wordlist=[u'يضرب', u"استقلّ", u'استقل', ]
for word in wordlist:
	conjStemmer.segment(word);
	print conjStemmer.get_affix_list();