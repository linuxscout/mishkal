#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        stem_verb
# Purpose:     Arabic lexical analyser, provides feature for stemming arabic word as verb
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
import re
import pyarabic.araby as araby
import tashaphyne.stemming
import stem_verb_const 
import analex_const 
import libqutrub.classverb   
import arramooz.arabicdictionary as arabicdictionary 
import wordCase
#~ import  stemmedword

class verbStemmer:
	"""
        Arabic verb stemmer
	"""

	def __init__(self, debug=False):
		# create a stemmer object for stemming enclitics and procletics
		self.compStemmer=tashaphyne.stemming.ArabicLightStemmer();

		# configure the stemmer object
		self.compStemmer.set_infix_letters(stem_verb_const.COMP_INFIX_LETTERS);
		self.compStemmer.set_prefix_letters(stem_verb_const.COMP_PREFIX_LETTERS);
		self.compStemmer.set_suffix_letters(stem_verb_const.COMP_SUFFIX_LETTERS);
		self.compStemmer.set_max_prefix_length(stem_verb_const.COMP_MAX_PREFIX);
		self.compStemmer.set_max_suffix_length(stem_verb_const.COMP_MAX_SUFFIX);
		self.compStemmer.set_min_stem_length(stem_verb_const.COMP_MIN_STEM);
		self.compStemmer.set_prefix_list(stem_verb_const.COMP_PREFIX_LIST);
		self.compStemmer.set_suffix_list(stem_verb_const.COMP_SUFFIX_LIST);


		# create a stemmer object for stemming conjugated verb
		self.conjStemmer=tashaphyne.stemming.ArabicLightStemmer();

		# configure the stemmer object
		self.conjStemmer.set_infix_letters(stem_verb_const.CONJ_INFIX_LETTERS);
		self.conjStemmer.set_prefix_letters(stem_verb_const.CONJ_PREFIX_LETTERS);
		self.conjStemmer.set_suffix_letters(stem_verb_const.CONJ_SUFFIX_LETTERS);
		self.conjStemmer.set_max_prefix_length(stem_verb_const.CONJ_MAX_PREFIX);
		self.conjStemmer.set_max_suffix_length(stem_verb_const.CONJ_MAX_SUFFIX);
		self.conjStemmer.set_min_stem_length(stem_verb_const.CONJ_MIN_STEM);
		self.conjStemmer.set_prefix_list(stem_verb_const.CONJ_PREFIX_LIST);
		self.conjStemmer.set_suffix_list(stem_verb_const.CONJ_SUFFIX_LIST);
		# enable the last mark (Harakat Al-I3rab) 
		self.allowSyntaxLastMark =True; 

		# To show statistics about verbs
		statistics={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 
		}

		self.debug=debug;
		self.cacheVerb={'verb':{}}
		
		self.verbDictionary=arabicdictionary.arabicDictionary("verbs")		

		self.VerbSTAMP_pat=re.compile(u"[%s%s%s%s%s]"%( araby.ALEF, araby.YEH,   araby.WAW,  araby.ALEF_MAKSURA, araby.SHADDA), re.UNICODE)

	def stemming_verb(self, verb):
		list_found = [];
		display_conj_result=False;
		detailed_result = [];
		verb			= verb.strip();
		verb_list		= [verb];
		if verb.startswith(araby.ALEF_MADDA):
			verb_list.append(araby.ALEF_HAMZA_ABOVE + araby.ALEF_HAMZA_ABOVE+verb[1:])
			verb_list.append(araby.HAMZA+araby.ALEF+verb[1:])

		for verb in verb_list:

			list_seg_comp=self.compStemmer.segment(verb);
			for seg in list_seg_comp:
				procletic=verb[:seg[0]];
				stem=verb[seg[0]:seg[1]]
				encletic=verb[seg[1]:]
				secondsuffix=u'';
				# حالة الفعل المتعدي لمفعولين
				if stem_verb_const.TableDoubleTransitiveSuffix.has_key(encletic ):
					firstsuffix=stem_verb_const.TableDoubleTransitiveSuffix[encletic]['first'];
					secondsuffix=stem_verb_const.TableDoubleTransitiveSuffix[encletic]['second'];
					encletic=firstsuffix;


				affix = u'-'.join([procletic, encletic])
				#if self.debug: print "\t", "-".join([procletic, stem, encletic]).encode("utf8") ;
				# ajusting verbs variant
				list_stem=[stem];
				if encletic:  #!="":
					transitive=True;
					if stem.endswith(araby.TEH + araby.MEEM + araby.WAW):
						list_stem.append(stem[:-1]);
					elif stem.endswith(araby.WAW):
						list_stem.append(stem+ araby.ALEF);
					elif stem.endswith( araby.ALEF):
						list_stem.append(stem[:-1]+ araby.ALEF_MAKSURA);

				else: transitive=False;
				if verb.startswith(araby.ALEF_MADDA):
					# االبداية بألف مد
					list_stem.append(araby.ALEF_HAMZA_ABOVE + araby.ALEF_HAMZA_ABOVE+verb[1:])
					list_stem.append(araby.HAMZA+ araby.ALEF+verb[1:])

		# stem reduced verb : level two
				result=[];
				for verb2 in list_stem:
					#segment the coinjugated verb
					list_seg_conj=self.conjStemmer.segment(verb2);

					# verify affix compatibility
					list_seg_conj = self.verify_affix(verb2, list_seg_conj, stem_verb_const.VERBAL_CONJUGATION_AFFIX);
					# verify procletics and enclitecs
					# verify length pof stem
					list_seg_conj2=[];
					for seg_conj in list_seg_conj:
						if (seg_conj[1] - seg_conj[0])<=6 :
							prefix_conj  = verb2[:seg_conj[0]];
							stem_conj    = verb2[seg_conj[0]:seg_conj[1]]
							suffix_conj  = verb2[seg_conj[1]:]
							affix_conj   = prefix_conj+'-'+suffix_conj;


						# verify compatibility between procletics and afix
							if (self.is_compatible_proaffix_affix(procletic, encletic, affix_conj)):
								# verify the existing of a verb stamp in the dictionary
								if self.verbDictionary.existsAsStamp(stem_conj):
									list_seg_conj2.append(seg_conj)

					list_seg_conj     = list_seg_conj2;
					list_correct_conj = [];

					for seg_conj in list_seg_conj:
						prefix_conj = verb2[:seg_conj[0]];
						stem_conj   = verb2[seg_conj[0]:seg_conj[1]]
						suffix_conj = verb2[seg_conj[1]:]
						affix_conj  = '-'.join([prefix_conj, suffix_conj])

							
						# search the verb in the dictionary by stamp
						# if the verb exists in dictionary, 
						# The transitivity is consedered
						# if is trilateral return its forms and Tashkeel
						# if not return forms without tashkeel, because the conjugator can vocalized it, 
						# we can return the tashkeel if we don't need the conjugation step						
						infverb_dict=self.getInfinitiveVerbByStem(stem_conj, transitive);

						infverb_dict = self.verifyInfinitiveVerbs(stem_conj, infverb_dict);
							

						for item in infverb_dict:
							#The haraka from is given from the dict
							inf_verb     = item['verb'];
							haraka       = item['haraka'];
							transtag     =  item['transitive'] #=='y'or not item['transitive']);
							transitive    =  (item['transitive']=='y'or not item['transitive']);

							originalTags = transtag; 
							# dict tag is used to mention word dictionary tags: the original word tags like transitive attribute
							unstemed_verb= verb2;

							# conjugation step

							# ToDo, conjugate the verb with affix, 
							# if exists one verb which match, return it
							# تصريف الفعل مع الزوائد
							# إذا توافق التصريف مع الكلمة الناتجة
							# تعرض النتيجة
							onelist_correct_conj = [];
							onelist_correct_conj = self.generate_possible_conjug(inf_verb, unstemed_verb, affix_conj, haraka, procletic, encletic, transitive);

							if len(onelist_correct_conj)>0:
								list_correct_conj+=onelist_correct_conj;
					# if 	not list_correct_conj :		print "No Verb Found ";
					for conj in list_correct_conj:
						result.append(conj['verb'])

						detailed_result.append(wordCase.wordCase({
						'word':verb, 
						'affix': ( procletic, prefix_conj, suffix_conj, encletic),						
						#~ 'procletic':procletic, 
						#~ 'encletic':encletic, 
						#~ 'prefix':prefix_conj, 
						#~ 'suffix':suffix_conj, 
						'stem':stem_conj, 
						'original':conj['verb'], 
						'vocalized':self.vocalize(conj['vocalized'], procletic, encletic), 
						'tags':u':'.join((conj['tense'], conj['pronoun'])+stem_verb_const.COMP_PREFIX_LIST_TAGS[procletic]['tags']+stem_verb_const.COMP_SUFFIX_LIST_TAGS[encletic]['tags']), 
						'type':'Verb', 
						#~ 'root':'', 
						#~ 'template':'', 
						'freq':'freqverb', 
						'originaltags':originalTags, 
						'syntax':'', 
						}));

	##				result+=detect_arabic_verb(verb2, transitive, prefix_conj, suffix_conj, debug);
				list_found+=result;

		list_found=set(list_found);
		return detailed_result

	
	def verify_affix(self, word, list_seg, affix_list):
		"""
		Verify possible affixes in the resulted segments according to the given affixes list.
		@param word: the input word.
		@type word: unicode.
		@param list_seg: list of word segments indexes (numbers).
		@type list_seg: list of pairs.
		@return: list of acceped segments.
		@rtype: list of pairs.
		"""	
		return filter (lambda s: '-'.join([word[:s[0]], word[s[1]:]]) in affix_list, list_seg)



	def getInfinitiveVerbByStem(self, verb, transitive):
		# a solution by using verbs stamps
		liste=[];
		
		verbIdList=self.verbDictionary.lookupByStamp(verb);

		if len(verbIdList):
			for verb_tuple in verbIdList:
				liste.append({'verb':verb_tuple['vocalized'], 'transitive':verb_tuple['transitive'], 'haraka':verb_tuple['future_type']});

		# if the verb in dictionary is vi and the stemmed verb is vt, don't accepot
		listetemp=liste;
		liste=[]
		for item in listetemp:
			##        print item['transitive'].encode("utf8"), transitive
			if item['transitive']==u'y' or  not transitive:
				liste.append(item);

		return liste;

	#----------------------------
	# generate possible conjugation
	# This function uses Qutrub conjugator
	#----------------------------

	def generate_possible_conjug(self, infinitive_verb, unstemed_verb , affix, future_type=araby.FATHA, externPrefix="-", externSuffix="-", transitive=True):
		"""
		"""
	##    future_type=FATHA;
		#~ transitive=True;
		list_correct_conj=[];
		if infinitive_verb=="" or unstemed_verb=="" or affix=="":
			return set();
		verb = infinitive_verb;
		future_type = libqutrub.ar_verb.get_future_type_entree(future_type);
		#print u"\t".join([verb, future_type]).encode('utf8');
		vb = libqutrub.classverb.verbclass(verb, transitive, future_type);
		# الألف ليست جزءا من السابقة، لأنها تستعمل لمنع الابتداء بساكن
		# وتصريف الفعل في الامر يولده
		if affix.startswith(araby.ALEF): affix=affix[1:]
		# get all tenses to conjugate the verb one time
		tenses=[];
		if stem_verb_const.Table_affix.has_key(affix):
			for pair in stem_verb_const.Table_affix[affix]:
				tenses.append(pair[0]);#tense=pair[0]
		tenses=list(set(tenses)); # avoid duplicata 


		if stem_verb_const.Table_affix.has_key(affix):
			for pair in stem_verb_const.Table_affix[affix]:
				tense=pair[0]
				pronoun=pair[1]
				if self.is_compatible_proaffix_tense(externPrefix, externSuffix, tense, pronoun, transitive):

					conj_vocalized = vb.conjugateTenseForPronoun( tense, pronoun)
					#strip all marks and shadda
					conj_nm =  araby.stripTashkeel(conj_vocalized);
					if conj_nm==unstemed_verb:
						list_correct_conj.append({'verb':infinitive_verb, 'tense':tense, 'pronoun':pronoun, 'vocalized':conj_vocalized, 'unvocalized':conj_nm});
		return list_correct_conj;


	def is_compatible_proaffix_affix(self, procletic, encletic, affix):
		"""
		Verify if proaffixes (sytaxic affixes) are compatable with affixes ( conjugation) 
		@param procletic: first level prefix.
		@type procletic: unicode.
		@param encletic: first level suffix.
		@type encletic: unicode.
		@param affix: second level affix.
		@type affix: unicode.
		@return: compatible.
		@rtype: True/False.
		"""	
		if not procletic and not encletic:  return True;
		else:
			procletic_compatible=False;
			if not procletic :
				procletic_compatible=True
			elif stem_verb_const.ExternalPrefixTable.has_key(procletic):
				if affix=='-':
					procletic_compatible=True;
				else:
					for item in stem_verb_const.Table_affix.get(affix, []):
						#the tense item[0];
						if item[0] in stem_verb_const.ExternalPrefixTable.get(procletic,''):
							procletic_compatible=True;
							break;
					else:
						procletic_compatible=False;

			if procletic_compatible:
				if not encletic :
					return True;
				elif stem_verb_const.ExternalSuffixTable.has_key(encletic):
					if affix=='-':
						return True;
					else: 
						for item in stem_verb_const.Table_affix.get(affix,[]):
							#the tense item[0];
							if item[1] in stem_verb_const.ExternalSuffixTable.get(encletic, ''):
								return True;
						else:
							return False;
		return False;


	def is_compatible_proaffix_tense(self, procletic, encletic, tense, pronoun, transitive):
		# إذا كان الزمن مجهولا لا يرتبط مع الفعل اللازم
		if not transitive and tense in stem_verb_const.qutrubVerbConst.TablePassiveTense:
			return False;
		if not procletic and not encletic:  return True;
		# The passive tenses have no encletics
		#ﻷزمنة المجهولة ليس لها ضمائر متصلة في محل نصب مفعول به
		#لأنّ مفعولها يصبح نائبا عن الفاعل
		
		if encletic and tense in stem_verb_const.qutrubVerbConst.TablePassiveTense:
			return False;
		elif (not procletic  or tense in stem_verb_const.ExternalPrefixTable.get(procletic, '') )\
			and ( not encletic or pronoun in stem_verb_const.ExternalSuffixTable.get(encletic, '')):
			return True;
		else:
			return False;


	def vocalize(self, verb, proclitic, enclitic):
		"""
		Join the  verb and its affixes, and get the vocalized form
		@param verb: verb found in dictionary.
		@type verb: unicode.
		@param proclitic: first level prefix.
		@type proclitic: unicode.
		@param enclitic: first level suffix.
		@type enclitic: unicode.		
		@return: vocalized word.
		@rtype: unicode.
		"""	
		enclitic_voc  = stem_verb_const.COMP_SUFFIX_LIST_TAGS[enclitic]["vocalized"][0];
		enclitic_voc  = self.getEncliticVariant(verb, enclitic_voc)
		proclitic_voc = stem_verb_const.COMP_PREFIX_LIST_TAGS[proclitic]["vocalized"][0];
		#suffix_voc=suffix;#CONJ_SUFFIX_LIST_TAGS[suffix]["vocalized"][0];
		# لمعالجة حالة ألف التفريق
		if enclitic and verb.endswith(araby.WAW+ araby.ALEF) :
			verb = verb[:-1];
		if enclitic and verb.endswith(araby.ALEF_MAKSURA):
			verb = verb[:-1]+araby.ALEF;
		return ''.join([ proclitic_voc, verb , enclitic_voc]);

		
	def getEncliticVariant(self, word, enclitic):

		"""
		Get the enclitic variant to be joined to the word.
		For example: word = أرجِهِ , encletic=هُ. The enclitic  is convert to HEH+ KAsra.
		اعبارة في مثل أرجه وأخاه إلى يم الزينة
		@param word: word found in dictionary.
		@type word: unicode.
		@param enclitic: first level suffix vocalized.
		@type enclitic: unicode.
		@return: variant of enclitic.
		@rtype: unicode.
		"""
		#if the word ends by a haraka
		if enclitic==araby.HEH+araby.DAMMA and (word.endswith(araby.KASRA) or word.endswith(araby.YEH)):
			enclitic=araby.HEH+araby.KASRA;
		return enclitic;

	def set_debug(self, debug):
		"""
		Set the debug attribute to allow printing internal analysis results.
		@param debug: the debug value.
		@type debug: True/False.
		"""
		self.debug=debug;
	def enableAllowSyntaxLastMark(self):
		"""
		Enable the syntaxic last mark attribute to allow use of I'rab harakat.
		"""
		self.allowSyntaxLastMark=True;

	def disableAllowSyntaxLastMark(self):
		"""
		Disable the syntaxic last mark attribute to allow use of I'rab harakat.
		"""
		self.allowSyntaxLastMark=False;


	def verifyInfinitiveVerbs(self, stem_conj, infverb_dict):
		"""
		verify if given infinitive verbs are compatible with stem_conj
		@param stem_conj: the stemmed verbs without conjugation affixes.
		@type stem_conj: unicode.
		@param infverb_dict: list of given infinitive verbs, each item contain 'verb' and 'type'.
		@type infverb_dict: list of dicts.
		@return: filtred  infinitive verbs
		@rtype: list of dict
		"""
		tmp=[];
		stemStamp=self.verbStamp(stem_conj);
		for item in infverb_dict:
			if self.verbStamp(item['verb'])==stemStamp:
				tmp.append(item);
		return tmp; 


	def verbStamp(self, word):
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
		word=araby.stripTashkeel(word);
		#The vowels are striped in stamp function
		word=araby.normalizeHamza(word);
		if word.startswith(araby.HAMZA):
			#strip The first hamza
			word=word[1:];
		# strip the last letter if is doubled
		if word[-1:]== word[-2:-1]:
			word=word[:-1];
		return self.VerbSTAMP_pat.sub('', word)


#Class test
if __name__ == '__main__':
	#ToDo: use the full dictionary of arramooz
	wordlist=[u'يضرب', u"استقلّ", u'استقل', ]
	verbstemmer=verbStemmer();
	verbstemmer.set_debug(True);
	for word in wordlist:
		verbstemmer.conjStemmer.segment(word);
		print verbstemmer.conjStemmer.get_affix_list();
	for word in wordlist:
		result=verbstemmer.stemming_verb(word);
		for analyzed in  result:
			print repr(analyzed);
			print u'\n'.join(analyzed.keys());
			for key in analyzed.keys():
				print u'\t'.join([key, unicode(analyzed[key])]).encode('utf8')
			print;
			print;
