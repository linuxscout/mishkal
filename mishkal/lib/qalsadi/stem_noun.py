#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        stem_noun
# Purpose:     Arabic lexical analyser, provides feature for stemming arabic word as noun
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
import tashaphyne.normalize
import analex_const
import stem_noun_const 
import arramooz.arabicdictionary as arabicdictionary 
#import arramooz.wordfreqdictionaryclass as wordfreqdictionaryclass
import wordCase
#~ import  stemmedword
import dictword

class nounStemmer:
	"""
        Arabic noun stemmer
	"""
	def __init__(self, debug=False):
		# create a stemmer object for stemming enclitics and procletics
		self.compStemmer = tashaphyne.stemming.ArabicLightStemmer();
		# configure the stemmer object
		self.compStemmer.set_infix_letters(stem_noun_const.COMP_INFIX_LETTERS);
		self.compStemmer.set_prefix_letters(stem_noun_const.COMP_PREFIX_LETTERS);
		self.compStemmer.set_suffix_letters(stem_noun_const.COMP_SUFFIX_LETTERS);
		self.compStemmer.set_max_prefix_length(stem_noun_const.COMP_MAX_PREFIX);
		self.compStemmer.set_max_suffix_length(stem_noun_const.COMP_MAX_SUFFIX);
		self.compStemmer.set_min_stem_length(stem_noun_const.COMP_MIN_STEM);
		self.compStemmer.set_prefix_list(stem_noun_const.COMP_PREFIX_LIST);
		self.compStemmer.set_suffix_list(stem_noun_const.COMP_SUFFIX_LIST);
		# create a stemmer object for stemming conjugated verb
		self.conjStemmer=tashaphyne.stemming.ArabicLightStemmer();
		# configure the stemmer object
		self.conjStemmer.set_infix_letters(stem_noun_const.CONJ_INFIX_LETTERS);
		self.conjStemmer.set_prefix_letters(stem_noun_const.CONJ_PREFIX_LETTERS);
		self.conjStemmer.set_suffix_letters(stem_noun_const.CONJ_SUFFIX_LETTERS);
		self.conjStemmer.set_max_prefix_length(stem_noun_const.CONJ_MAX_PREFIX);
		self.conjStemmer.set_max_suffix_length(stem_noun_const.CONJ_MAX_SUFFIX);
		self.conjStemmer.set_min_stem_length(stem_noun_const.CONJ_MIN_STEM);
		self.conjStemmer.set_prefix_list(stem_noun_const.CONJ_PREFIX_LIST);
		self.conjStemmer.set_suffix_list(stem_noun_const.CONJ_SUFFIX_LIST);

		# enable the last mark (Harakat Al-I3rab) 
		self.allowSyntaxLastMark =True; 

		# noun dictionary
		# self.nounDictionary=arabicdictionary.arabicDictionary("nouns", NOUN_DICTIONARY_INDEX)
		self.nounDictionary=arabicdictionary.arabicDictionary("nouns")		

		# allow to print internal results.
		self.CacheDictSearch={};
		self.CacheAffixesVerification={}
		self.debug=debug;

	def stemming_noun(self, noun):
		"""
		Analyze word morphologically as noun
		@param noun: the input noun.
		@type noun: unicode.
		@return: list of dictionaries of analyzed words with tags.
		@rtype: list.
		"""	
		list_found=[];
		detailed_result=[];
		noun_list = [noun,];
		# if the word contains ALEF8MADDA, we convert it into twoHAMZA above ALEF
		if araby.ALEF_MADDA in noun:
			noun_list.append(noun.replace(araby.ALEF_MADDA, araby.ALEF_HAMZA_ABOVE*2))
		for noun in noun_list:
			list_seg_comp = self.compStemmer.segment(noun);
			list_seg_comp = self.verify_affix(noun, list_seg_comp, stem_noun_const.COMP_NOUN_AFFIXES);
			# treat multi vocalization encletic
			list_seg_comp_voc = [];
			for seg in list_seg_comp:
				procletic = noun[:seg[0]];
				stem      = noun[seg[0]:seg[1]]
				encletic_nm  = noun[seg[1]:]


				# ajusting nouns variant
				list_stem=[stem];
				if encletic_nm: # !=""
					if stem.endswith(araby.ALEF):
						list_stem.append(stem[:-1]+araby.ALEF_MAKSURA);
					elif stem.endswith(araby.TEH):
						list_stem.append(stem[:-1]+araby.TEH_MARBUTA);				

		# stem reduced noun : level two
				for stem in list_stem:
					detailed_result.extend(self.steming_second_level(noun, stem, procletic, encletic_nm, encletic_nm));

		return detailed_result #list_found;
		

	def steming_second_level(self, noun, noun2, procletic, encletic, encletic_nm):
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
		@param encletic_nm: the syntaxic suffixe extracted in the fisrt stage (not vocalized).
		@type encletic_nm: unicode.		
		@return: list of dictionaries of analyzed words with tags.
		@rtype: list.
		"""	
		detailed_result=[];
		#segment the coinjugated verb
		list_seg_conj = self.conjStemmer.segment(noun2);
		# verify affix compatibility
		list_seg_conj = self.verify_affix(noun2, list_seg_conj, stem_noun_const.NOMINAL_CONJUGATION_AFFIX);
		# add vocalized forms of suffixes
		# and create the real affixes from the word
		list_seg_conj_voc=[];
		for seg_conj in list_seg_conj:
			stem_conj   = noun2[seg_conj[0]:seg_conj[1]]
			suffix_conj_nm = noun2[seg_conj[1]:]

			# noirmalize hamza before gessing  differents origines
			stem_conj = araby.normalizeHamza(stem_conj)

			# generate possible stems
			# add stripped letters to the stem to constitute possible noun list
			possible_noun_list=self.getStemVariants(stem_conj, suffix_conj_nm);

			# search the noun in the dictionary
			# we can return the tashkeel
			infnoun_form_list=[];
			for infnoun in set(possible_noun_list):
				# get the noun and get all its forms from the dict
				# if the noun has plural suffix, don't look up in broken plural dictionary
				if not self.CacheDictSearch.has_key(infnoun):
					infnoun_foundL = self.nounDictionary.lookup(infnoun);
					self.CacheDictSearch[infnoun]  = self.createDictWord(infnoun_foundL);
				else: 
					infnoun_foundL = self.CacheDictSearch[infnoun]  ;					
				infnoun_form_list.extend(infnoun_foundL);
			#print "len loooked up noun in dictionnary ",len(infnoun_form_list), len(set(infnoun_form_list));
			for noun_tuple in infnoun_form_list:
				# noun_tuple=self.nounDictionary.getEntryById(id);
				infnoun = noun_tuple['vocalized'];
				# affixes tags contains prefixes and suffixes tags
				affix_tags  =  stem_noun_const.COMP_PREFIX_LIST_TAGS[procletic]['tags'] \
								+stem_noun_const.COMP_SUFFIX_LIST_TAGS[encletic_nm]['tags'] \
								+stem_noun_const.CONJ_SUFFIX_LIST_TAGS[suffix_conj_nm]['tags']
				#test if the  given word from dictionary accept those tags given by affixes
				# دراسة توافق الزوائد مع خصائص الاسم،
				# مثلا هل يقبل الاسم التأنيث.
	
				if self.validateTags(noun_tuple, affix_tags, procletic, encletic_nm, suffix_conj_nm):
					## get all vocalized form of suffixes
					for vocalized_encletic in stem_noun_const.COMP_SUFFIX_LIST_TAGS[encletic_nm]['vocalized']:
						for vocalized_suffix in stem_noun_const.CONJ_SUFFIX_LIST_TAGS[suffix_conj_nm]['vocalized']:
							## verify compatibility between procletics and affix
							if (self.is_compatible_proaffix_affix(noun_tuple, procletic, vocalized_encletic, vocalized_suffix)):
								vocalized, semiVocalized = self.vocalize(infnoun, procletic,  vocalized_suffix, vocalized_encletic);
								vocalized_affix_tags  =  stem_noun_const.COMP_PREFIX_LIST_TAGS[procletic]['tags'] \
												+stem_noun_const.COMP_SUFFIX_LIST_TAGS[vocalized_encletic]['tags'] \
												+stem_noun_const.CONJ_SUFFIX_LIST_TAGS[vocalized_suffix]['tags']								
								
								#add some tags from dictionary entry as mamnou3 min sarf and broken plural
								originalTags=[];
								if noun_tuple['mamnou3_sarf']==u"ممنوع من الصرف":
									originalTags.append(u"ممنوع من الصرف");
								if noun_tuple['number']==u"جمع تكسير":
									originalTags.append(u"جمع تكسير");						
									# affix_tags+=(, );
								detailed_result.append(wordCase.wordCase({
								'word':noun, 
								#~ 'affix': analex_const.AffixTuple((procletic=procletic, encletic=vocalized_encletic, prefix='', suffix=vocalized_suffix)),								
								'affix': (procletic,  '', vocalized_suffix, vocalized_encletic),								
								#~ 'procletic': , 
								#~ 'encletic':  , 
								#~ 'prefix':    '', 
								#~ 'suffix':    vocalized_suffix, 
								'stem':      stem_conj, 
								'original':  infnoun, #original, 
								'vocalized': vocalized, 
								'semivocalized':semiVocalized,
								'tags':      u':'.join(vocalized_affix_tags), 
								'type':      u':'.join(['Noun', noun_tuple['wordtype']]), #'Noun', 
								#~ 'root':      '', 
								#~ 'template':  '', 
								'freq':'freqnoun', # to note the frequency type 
								'originaltags':u':'.join(originalTags), 
								'syntax':'', 
								}));
		return detailed_result;

	def createDictWord(self, dictEntriesList):
		"""
		Create a list of dictWord objects from dictionary entries
		@param dictEntriesList: a list of entiers from lexicon
		@type  dictEntriesList: list of dict
		@return: a list of dictWord object
		@rtype: a list of dictWord object;
		"""
		return dictEntriesList
		#ToDo
		return [dictword.dictWord(dict(lexiconEntry))  for  lexiconEntry in  dictEntriesList];
		#for lexiconEntry in dictEntriesList:
			#dictWordList.append(dictword.dictWord(dict(lexiconEntry)))
		## return dictWordList;

	def validateTags(self, noun_tuple, affix_tags, procletic, encletic_nm , suffix_nm):
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
		@return: if the tags are compaatible.
		@rtype: Boolean.
		"""
		procletic = araby.stripTashkeel(procletic);
		# encletic = araby.stripTashkeel(encletic);	
		# suffix   = araby.stripTashkeel(suffix);
		encletic = encletic_nm
		suffix   = suffix_nm
		if u'مؤنث' in affix_tags and not noun_tuple['feminable']:
			return False;
		if  u'جمع مؤنث سالم' in affix_tags and not noun_tuple['feminin_plural']:
			return False;
		if  u'جمع مذكر سالم' in affix_tags and not noun_tuple['masculin_plural']:
			return False;
		if  u'مثنى' in affix_tags and not noun_tuple['dualable']:
			return False;
		if  u'تنوين' in affix_tags and  noun_tuple['mamnou3_sarf']:
			return False;
		if  u'منسوب' in affix_tags and not noun_tuple['relative']:
			return False;
		#تدقيق الغضافة إلى الضمائر المتصلة
		if encletic==u"هم" and noun_tuple['hm_suffix']=='N':
			return False;
		if encletic==u"ه" and noun_tuple['ha_suffix']=='N':
			return False;
		if encletic==u"ك" and noun_tuple['k_suffix']=='N':
			return False;
		#حالة قابلية التشبيه
		if procletic.endswith(u"كال") and noun_tuple['kal_prefix']=='N':
			return False;
		# حالة المضاف إلى ما بعهده في حالة جمع المذكر السالم
		# مثل لاعبو، رياضيو
		if suffix==araby.WAW and not noun_tuple['w_suffix']:
			return False;
		#التاء المربوطة لا تتصل بجمع التكسير
		# if suffix==araby.TEH_MARBUTA and noun_tuple['broken_plural']:
			# return False;
		# elif  u'مضاف' in affix_tags and not noun_tuple['annex']:
			# return False;
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
		return True;

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

	def getStemVariants(self, stem, suffix_nm):
		"""
		Generate the Noun stem variants according to the affixes.
		For example مدرستي=>مدرست+ي => مدرسة +ي.
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
		suffix = suffix_nm
		
		possible_noun_list = set([stem,]);
		if suffix_nm in (araby.ALEF+araby.TEH, araby.YEH+araby.TEH_MARBUTA, araby.YEH, araby.YEH+araby.ALEF+araby.TEH):
			possible_noun = stem+araby.TEH_MARBUTA;
			possible_noun_list.add(possible_noun)
		if not suffix_nm  or suffix_nm in (araby.YEH+araby.NOON, araby.WAW+araby.NOON):
			possible_noun=stem+araby.YEH;
			possible_noun_list.add(possible_noun)
		if stem.endswith(araby.YEH):
			possible_noun=stem[:-1]+araby.ALEF_MAKSURA;
			possible_noun_list.add(possible_noun)
		#to be validated
		validated_list=possible_noun_list;
		return validated_list

 	def is_compatible_proaffix_affix(self, noun_tuple, procletic, encletic, suffix):
		"""
		Verify if proaffixes (sytaxic affixes) are compatable with affixes ( conjugation) 
		@param procletic: first level prefix.
		@type procletic: unicode.
		@param encletic: first level suffix.
		@type encletic: unicode.
		@param suffix: second level suffix.
		@type suffix: unicode.
		@return: compatible.
		@rtype: True/False.
		"""	
		#if not procletic and not encletic:  return True;
		#use cache for affix verification
		affix = u'-'.join([procletic, encletic, suffix, str(bool(noun_tuple['mamnou3_sarf']))]);
		if affix in self.CacheAffixesVerification:
			return self.CacheAffixesVerification[affix];
			
		# get procletics and enclitics tags
		procletic_tags = stem_noun_const.COMP_PREFIX_LIST_TAGS[procletic]['tags'];
		encletic_tags  = stem_noun_const.COMP_SUFFIX_LIST_TAGS[encletic]['tags'];
		# in nouns there is no prefix 
		suffix_tags    = stem_noun_const.CONJ_SUFFIX_LIST_TAGS[suffix]['tags'];		

		if u"تعريف" in procletic_tags and u"مضاف" in suffix_tags and not u'منسوب' in suffix_tags:
			self.CacheAffixesVerification[affix] = False;
		elif u"تعريف" in procletic_tags and u"تنوين" in suffix_tags:
			self.CacheAffixesVerification[affix] = False;
		# التنوين لا يتطابق مع الممنوع من الصرف
		elif ( u'تنوين' in suffix_tags)  and  noun_tuple['mamnou3_sarf']:
			self.CacheAffixesVerification[affix] = False;
	# الجر  في حالات الاسم المعرفة بال أو الإضافة إلى ضمير أو مضاف إليه
	# مما يعني لا يمكن تطبيقها هنا
		#~ elif (( not encletic and )or ( u'مجرور' in suffix_tags))  and  noun_tuple['mamnou3_sarf']:
			#~ self.CacheAffixesVerification[affix] = False;			
		elif u"مضاف" in encletic_tags and u"تنوين" in suffix_tags:
			self.CacheAffixesVerification[affix] = False;
		elif u"مضاف" in encletic_tags and u"لايضاف" in suffix_tags:
			self.CacheAffixesVerification[affix] = False;
		elif u"جر" in procletic_tags and u"مجرور" not in suffix_tags:
			self.CacheAffixesVerification[affix] = False;
#ستعمل في حالة كسر هاء الضمير في الجر			

		elif  bool(u"لايجر" in encletic_tags) and  bool(u"مجرور" in suffix_tags) :
			self.CacheAffixesVerification[affix] = False;
		elif  bool(u"مجرور" in encletic_tags) and  not bool(u"مجرور" in suffix_tags) :
			self.CacheAffixesVerification[affix] = False;	
		else:
			self.CacheAffixesVerification[affix] = True;
		return self.CacheAffixesVerification[affix];



	def vocalize(self, noun, proclitic,  suffix, enclitic):
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
		# enclitic and procletric have only an uniq vocalization in arabic
		enclitic_voc  = stem_noun_const.COMP_SUFFIX_LIST_TAGS[enclitic]["vocalized"][0];
		proclitic_voc = stem_noun_const.COMP_PREFIX_LIST_TAGS[proclitic]["vocalized"][0];
		suffix_voc    = suffix;#CONJ_SUFFIX_LIST_TAGS[suffix]["vocalized"][0];
		#adjust some some harakat
		
		#strip last if tanwin or last harakat
		if araby.isHaraka(noun[-1:]):#(DAMMATAN, FATHATAN, KASRATAN, FATHA, DAMMA, KASRA):
			noun = noun[:-1];
		# convert Fathatan into one fatha, in some cases where the tanwin is not at the end: eg. محتوًى
		noun = noun.replace(araby.FATHATAN, araby.FATHA);

		#add shadda if the first letter is sunny and the procletic contains AL definition mark
		if (u'تعريف' in stem_noun_const.COMP_PREFIX_LIST_TAGS[proclitic]["tags"] and araby.isSun(noun[0])):
		#if (u'تعريف' in proclitic.endswith(araby.ALEF+araby.LAM) or proclitic.endswith(araby.LAM+araby.LAM)) and araby.isSun(noun[0]):
			noun = u''.join([noun[0], araby.SHADDA, noun[1:]]);
			#strip the Skun from the lam
			if proclitic_voc.endswith(araby.SUKUN):
				proclitic_voc=proclitic_voc[:-1];
		# generate the word variant for some words witch ends by special letters like Teh_marbuta or Alef_maksura, or hamza, the variant is influed by the suffix harakat, 
		# for example مدرسة+ي= مدرست+ي
		noun         = self.getWordVariant(noun, suffix+enclitic);

		# generate the suffix variant. if the suffix is Teh_marbuta or Alef_maksura, or hamza, the variant is influed by the enclitic harakat, 
		# for example مدرس+ة+ي=مدرس+ت+ي		
		suffix_voc, suffix_NonIrabMark   = self.getSuffixVariant(noun, suffix_voc, enclitic);

		#Get the enclitic variant to be joined to the word.
		#For example: word = مدرس, suffix=ِة, encletic=هُ. The enclitic  is convert to HEH+ KAsra.
		enclitic_voc = self.getEncliticVariant(noun, suffix_voc, enclitic_voc);

		# generate the non vacalized end word: the vocalized word without the I3rab Mark
		# if the suffix is a short haraka 
		wordNonIrabMark= ''.join([ proclitic_voc,  noun, suffix_NonIrabMark,   enclitic_voc])			 
			
		wordVocalized =''.join([ proclitic_voc, noun, suffix_voc, enclitic_voc]);
		return wordVocalized,wordNonIrabMark 
	
	def getSuffixVariant(self, word, suffix, enclitic):
		"""
		Get the suffix variant to be joined to the word.
		For example: word = مدرس, suffix=ة, encletic=ي. The suffix is converted to Teh.
		@param word: word found in dictionary.
		@type word: unicode.
		@param suffix: second level suffix.
		@type suffix: unicode.
		@param enclitic: first level suffix.
		@type enclitic: unicode.		
		@return: variant of suffixes  (vocalized suffix and vocalized suffix without I'rab short mark).
		@rtype: (unicode, unicode)
		"""
		enclitic_nm=araby.stripTashkeel(enclitic)
		newSuffix =suffix; #default value
		#if the word ends by a haraka
		if suffix.find(araby.TEH_MARBUTA)>=0 and len (enclitic_nm)>0:
			newSuffix=re.sub(araby.TEH_MARBUTA, araby.TEH, suffix);
		elif 	not enclitic_nm and word[-1:] in (araby.ALEF_MAKSURA, araby.YEH, araby.ALEF) and araby.isHaraka(suffix):
			newSuffix=u"";
		#gererate the suffix without I'rab short mark
		# here we lookup with given suffix because the new suffix is changed and can be not found in table
		if u'متحرك' in stem_noun_const.CONJ_SUFFIX_LIST_TAGS[suffix]['tags']:
			suffixNonIrabMark =araby.stripLastHaraka(newSuffix);
		else:
			suffixNonIrabMark = newSuffix
		return newSuffix, suffixNonIrabMark ;

	def getEncliticVariant(self, word, suffix, enclitic):
		"""
		Get the enclitic variant to be joined to the word.
		For example: word = مدرس, suffix=ِة, encletic=هُ. The enclitic  is convert to HEH+ KAsra.
		@param word: word found in dictionary.
		@type word: unicode.
		@param suffix: second level suffix vocalized.
		@type suffix: unicode.
		@param enclitic: first level suffix vocalized.
		@type enclitic: unicode.
		@return: variant of enclitic.
		@rtype: unicode.
		"""
		#if the word ends by a haraka
		# if enclitic.startswith(araby.HEH+araby.DAMMA) and (suffix.endswith(araby.KASRA) or suffix.endswith(araby.YEH) ):
			# enclitic = enclitic.replace(araby.HEH+araby.DAMMA, araby.HEH+araby.KASRA);

		return enclitic;
	def getWordVariant(self, word, suffix):
		"""
		Get the word variant to be joined to the suffix.
		For example: word = مدرسة, suffix=ي. The word is converted to مدرست.
		@param word: word found in dictionary.
		@type word: unicode.
		@param suffix: suffix ( firts or second level).
		@type suffix: unicode.
		@return: variant of word.
		@rtype: unicode.
		"""
		word_stem=word;
		# print word.encode('utf8');
		#HARAKAT=(FATHA, DAMMA, KASRA, SUKUN, DAMMA, DAMMATAN, KASRATAN, FATHATAN);
		suffix_nm=araby.stripTashkeel(suffix)
		#if the word ends by a haraka
		word_stem=araby.stripLastHaraka(word_stem);

		if word_stem.endswith(araby.TEH_MARBUTA) and suffix_nm in (araby.ALEF+araby.TEH, araby.YEH+araby.TEH_MARBUTA, araby.YEH, araby.YEH+araby.ALEF+araby.TEH):
			word_stem=word_stem[:-1];
		elif word_stem.endswith(araby.TEH_MARBUTA) and suffix_nm!=u"":
			word_stem=word_stem[:-1]+araby.TEH;
		elif word_stem.endswith(araby.ALEF_MAKSURA) and suffix_nm!=u"":
			word_stem = word_stem[:-1]+araby.YEH;			
		elif word_stem.endswith(araby.HAMZA) and suffix_nm!=u"":
			if suffix.startswith(araby.DAMMA):
				word_stem = word_stem[:-1] + araby.WAW_HAMZA;
			elif suffix.startswith(araby.KASRA):
				word_stem = word_stem[:-1] + araby.YEH_HAMZA;
				
		return word_stem;
		
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
