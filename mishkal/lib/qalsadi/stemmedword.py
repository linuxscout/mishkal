#!/usr/bin/python
# -*- coding = utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        stemmedWord
# Purpose:     representat data analyzed given by morphoanalyzer Qalsadi
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     19-09-2012
# Copyright:   (c) Taha Zerrouki 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

import pyarabic.araby as araby
import analex_const 
import stemmedaffix
import wordCase
#used as a cache for affixes
# GlobalAffixes={'noun':{},
				# 'verb':{},
				# 'stopword':{},
				# }
GlobalAffixes={}				

class stemmedWord:
	"""
	stemmedWord represents the data resulted from the morpholocigal analysis
	"""
	def __init__(self, resultDict=None):
		# given word attributes
		self.word =  u"",		
		"""input word"""
		self.vocalized =  u"",  
		"""vocalized form of the input word """
		
		self.tags =  u"", 
		"""tags of affixes and tags extracted form lexical dictionary"""
		self.affixKey  = u'-'
		affixTags 	=u"" 	
		"""tags of affixes"""

		# stemmed word attributes
		self.stem =  u"",		
		"""the word stem"""

		# Original word attributes from dictionary.
		self.originalTags =  u"",
		""" tags extracted form lexical dictionary"""
		self.freq =  0,				# the word frequency from Word Frequency database 
		self.type =  u"",				# the word type
		self.original =  u""			#original word from lexical dictionary
		#~ if isinstance(resultDict, wordCase.wordCase):
			#~ resultDict = resultDict.__dict__
		if resultDict:

			self.word	= resultDict.get('word',u'');
			self.vocalized	= resultDict.get('vocalized',u'');
			self.semivocalized	= resultDict.get('semivocalized',u'');
			self.stem	= resultDict.get('stem',u'');
			self.affix  = u'-'.join(resultDict.get('affix',[]))

			affixTags = resultDict.get('tags',u'');
			self.tags	= u':'.join([resultDict.get('tags',u''), resultDict.get('originaltags',u'')]);			
			self.freq 	= resultDict.get('freq',u'');
			self.type	= resultDict.get('type',u'');
			self.original	= resultDict.get('original',u'');

		# calculated  attributes 
		self.tagStopWord	= self._isStopWord();
		self.tagVerb		= False;
		self.tagNoun		= False;		
		if not self.tagStopWord:
			self.tagVerb	= self._isVerb();
			if not self.tagVerb:
				self.tagNoun	= self._isNoun();

		self.affixKey=self.affix
		if self.tagVerb :
			# #if the word is verb: we must add the tense and pronoun to the affixkay.
			# #because for verbs, same affixes don't give same tags
			self.affixKey=u'|'.join([self.affixKey, affixTags]);
			
		if not GlobalAffixes.has_key(self.affixKey):
			GlobalAffixes[self.affixKey] = stemmedaffix.stemmedAffix(resultDict);
		# init
		self.tagAdded 		 = False
		self.tagInitial      = False
		self.tagMasdar		 = False
		self.tagProperNoun	 = False
		self.tagAdj		 	 = False
		self.tagPounct		 = False
		self.tagTransparent	 = False
		self.tagMasculin	 = False
		self.tagFeminin		 = False
		self.tagPlural		 = False
		self.tagBrokenPlural = False
		self.tagMamnou3	     = False
		self.tagSingle		 = False
		self.tagBreak		 = False
		
		if self.tagNoun:
			self.tagAdded 		= self._isAdded();
			self.tagAdj			= self.tagNoun and self._isAdj();
			self.tagMasdar		= self.tagNoun and self._isMasdar();
			self.tagProperNoun	= self.tagNoun and self._isProperNoun();
			self.tagBrokenPlural= self._isBrokenPlural();			
			self.tagMamnou3		= self._isMamnou3();		
		elif self.tagStopWord:
			self.tagTransparent	= self._isTransparent();
		else:
			self.tagPounct		= self._isPounct();
		self.tagInitial     = self._isInitial();

		self.tagFeminin		= self._isFeminin();
		# self.tagMasculin	= not self.tagFeminin #self._isMasculin();		
		self.tagPlural		= self.tagBrokenPlural or self._isPlural();
		# self.tagSingle		= not self.tagPlural or self._isSingle();	#redandente
		self.tagBreak		= self._isBreak();
		
	#  tags extracted from word dictionary 
	#--------------------------
	def _isInitial(self):
		"""
		Return True if the word mark the begin of next sentence.
		@return: direct initial.
		@rtype: True/False;
		"""
		word=self.getWord();
		return word==u"" or  word[0] in (u'.',u'?', u';', u':');

	def _isNoun(self):
		"""
		Return True if the word is a noun.
		@return: is a noun.
		@rtype: True/False;
		"""			
		return u'Noun' in self.getType()  or  u'اسم' in self.getTags();

	def _isAdj(self):
		"""
		Return True if the word is a Adjective.
		@return: is a Adjective.
		@rtype: True/False;
		"""
		type=self.getType();
		return u'صفة' in type or u'اسم مفعول' in type or u'اسم فاعل' in type or u'صيغة مبالغة' in type or u'منسوب' in type;
	def _isStopWord(self):
		"""
		Return True if the word is a stop word.
		@return: is a noun.
		@rtype: True/False;
		"""			
		return u'STOPWORD' in self.getType();

	def _isVerb(self):
		"""
		Return True if the word is a verb.
		@return: is a verb.
		@rtype: True/False;
		"""			
		return  u'Verb' in self.getType();

	def _isMasdar(self):
		"""
		Return True if the word is a masdar.
		@return: is a masdar.
		@rtype: True/False;
		"""			
		return u'مصدر' in self.getType();

	def _isProperNoun(self):
		"""
		Return True if the word is a proper noun.
		@return: is a proper noun.
		@rtype: True/False;
		"""			
		return u'noun_prop' in self.getType();

	def _isPounct(self):
		"""
		Return True if the word is a pounctuation.
		@return: is a verb.
		@rtype: True/False;
		"""			
		return  u'POUNCT' in self.getType();


	def _isTransparent(self):
		"""
		Return True if the word has the state transparent, which can trasnpose the effect of the previous factor.
		@return: has the state transparent.
		@rtype: True/False;
		"""
		#temporary, 
		# the transparent word are stopwords like هذا وذلك
		# the stopword tags have اسم إشارة,
		# a pounctuation can has the transparent tag like quotes., which havent any gramatical effect.
		# Todo 
		# حالة بذلك الرجل
		return  u'شفاف' in self.getTags() or u'إشارة'in self.getTags();


	# def _isMajrour(self):
		# """
		# Return True if the word has the state majrour.
		# @return: has the state majrour.
		# @rtype: True/False;
		# """				
		# if u'مجرور' in self.getTags():
			# return True;
		# else:
			# return False;

	def _isBrokenPlural(self):
		"""
		Return True if the word is broken  plural.
		@return: is broken plural.
		@rtype: True/False;
		"""
		return  u'جمع تكسير' in self.getTags();

	def _isMamnou3(self):
		"""
		Return True if the word is forbiden from Sarf ممنوع من الصرف.
		@return: is mamnou3 min sarf.
		@rtype: True/False;
		"""
		return  u'ممنوع من الصرف' in self.getTags();

	def getProcletic(self,):
		"""
		Get the procletic 
		@return: the given procletic.
		@rtype: unicode string
		"""
		# return self.procletic;
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].getProcletic()
		return u"";			
	# def setProcletic(self,newprocletic):
		# """
		# Set the procletic 
		# @param newprocletic: the new given procletic.
		# @type newprocletic: unicode string
		# """
		# self.procletic = newprocletic;
	def hasProcletic(self,):
		"""
		return True if has procletic 
		@return: True if procletic not empty.
		@rtype: Boolean
		"""
		# return self.procletic!=u'';
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].hasProcletic()
		return False;	
	def getPrefix(self,):
		"""
		Get the prefix 
		@return: the given prefix.
		@rtype: unicode string
		"""
		# return self.prefix;
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].getPrefix()
		return u"";			
	# def setPrefix(self,newprefix):
		# """
		# Set the prefix 
		# @param newprefix: the new given prefix.
		# @type newprefix: unicode string
		# """
		# self.prefix = newprefix;


	def getSuffix(self,):
		"""
		Get the suffix 
		@return: the given suffix.
		@rtype: unicode string
		"""
		# return self.suffix;
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].getSuffix()
		return u"";			
	def getEncletic(self,):
		"""
		Get the encletic 
		@return: the given encletic.
		@rtype: unicode string
		"""
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].getEncletic()
		return u"";		
		
	def hasEncletic(self,):
		"""
		return True if has encletic 
		@return: True if encletic not empty.
		@rtype: Boolean
		"""
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].hasEncletic()
		return False;			


	# Mixed affix and dictionary attrrubutes
	#---------------------------------------
	def _affixIsAdded(self):
		"""
		Return True if the word has the state added مضاف.
		@return: has the state added.
		@rtype: True/False;
		"""		
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isAdded()
		return False;	
	def _isAdded(self):
		"""
		Return True if the word has the state added مضاف.
		@return: has the state added.
		@rtype: True/False;
		"""		
		return  self._affixIsAdded() or u'اسم إضافة' in self.getTags();


	def _affixIsFeminin(self):
		"""
		Return True if the word is Feminin.
		@return: is Feminin.
		@rtype: True/False;
		"""		
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isFeminin()
		return False;	
	def _isFeminin(self):
		"""
		Return True if the word is Feminin.
		@return: is Feminin.
		@rtype: True/False;
		"""
		#يتحدد المؤنث 
		# بزيادة التاء المربوطة
		# جمع مؤنث سالم
		# ما كات اصله تاء مربوطة
		# للعمل TODO
		# دالة حاصة للكلمات المؤنثة
		if self._affixIsFeminin():
			return True;
		# elif self.getUnvOriginal() and self.getUnvOriginal().endswith(araby.TEH_MARBUTA):
		return  araby.TEH_MARBUTA in self.getOriginal() ; 

	def _affixIsPlural(self):
		"""
		Return True if the word is a plural.
		@return: is Feminin.
		@rtype: True/False;
		"""		
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isPlural()
		return False;	
	def _isPlural(self):
		"""
		Return True if the word is a plural.
		@return: is plural.
		@rtype: True/False;
		"""
		return self._affixIsPlural() or self._isBrokenPlural();

	def _isSingle(self):
		"""
		Return True if the word is single.
		@return: is  dual.
		@rtype: True/False;
		"""
		# return not self._isPlural() and not self._isDual();
		return not self.isPlural() and not self.isDual();

	def _isBreak(self):
		"""
		Return True if the word has break.

		@return: is break.
		@rtype: True/False;
		"""	
		#تكون الكلمة فاصلة إذا كانت منفصلة عمّا قبلها.	
		# الحالات التي تقطع
		# - حرف جر متصل
		# فاصلة أو نقطة
		# if self.isDirectJar():
			# return True;
		# el
		# if self.hasProcletic() and self.hasJar():
		return self.isStopWord() \
			or (self.isPounct() and 'break' in self.getTags())\
		    or (self.hasProcletic() and self.hasJar())
			# or (self.isPounct() and 'break' in self.getTags());		

	######################################################################
	#{ Attribut Functions
	######################################################################
	def getWord(self,):
		"""
		Get the input word given by user
		@return: the given word.
		@rtype: unicode string
		"""
		return self.word;
	def setWord(self,newword):
		"""
		Set the input word given by user
		@param newword: the new given word.
		@type newword: unicode string
		"""
		self.word = newword;
		
	def getVocalized(self,):
		"""
		Get the vocalized form of the input word
		@return: the given vocalized.
		@rtype: unicode string
		"""
		return self.vocalized;
		
	def setVocalized(self,newvocalized):
		"""
		Set the vocalized word
		@param newvocalized: the new given vocalized.
		@type newvocalized: unicode string
		"""
		self.vocalized  =  newvocalized;
		self.unvocalized  =  araby.stripTashkeel(newvocalized);
	# def getUnvocalized(self,):
		# """
		# Get the unvocalized form of the input word
		# @return: the given unvocalized.
		# @rtype: unicode string
		# """
		# if self.unvocalized:
			# return self.unvocalized;
		# else:
			# if self.vocalized:
				# self.vocalized=araby.stripTashkeel(self.vocalized);
			# else :
				# return u"";
	# def setUnvocalized(self,newunvocalized):
		# """
		# Set the unvocalized word
		# @param newunvocalized: the new given unvocalized.
		# @type newunvocalized: unicode string
		# """
		# self.unvocalized = newunvocalized;
	def getStem(self,):
		"""
		Get the stem form of the input word
		@return: the given stem.
		@rtype: unicode string
		"""
		return self.stem;
		
	def getTags(self,):
		"""
		Get the tags form of the input word
		@return: the given tags.
		@rtype: unicode string
		"""
		return self.tags;
		
	def setTags(self,newtags):
		"""
		Set the tags word
		@param newtags: the new given tags.
		@type newtags: unicode string
		"""
		self.tags = newtags;
	def getAffixTags(self,):
		"""
		Get the affix tags form of the input word
		@return: the given tags.
		@rtype: unicode string
		"""
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].getTags()
		return u"";
	def getAffix(self,):
		"""
		Get the affix  form of the input word
		@return: the given affix.
		@rtype: unicode string
		"""
		return self.affix;
		# return u"";
		# return self.affixTags;
		
	def setAffixTags(self,newtags):
		"""
		Set the tags word
		@param newtags: the new given tags.
		@type newtags: unicode string
		"""
		self.affixTags = newtags;

	def getFreq(self,):
		"""
		Get the freq form of the input word
		@return: the given freq.
		@rtype: unicode string
		"""
		return self.freq;
		
	def setFreq(self,newfreq):
		"""
		Set the freq word
		@param newfreq: the new given freq.
		@type newfreq: unicode string
		"""
		self.freq = newfreq;
	def getTemplate(self,):
		"""
		Get the template form of the input word
		@return: the given template.
		@rtype: unicode string
		"""
		return self.template;
		
	def setTemplate(self,newtemplate):
		"""
		Set the template word
		@param newtemplate: the new given template.
		@type newtemplate: unicode string
		"""
		self.template = newtemplate;
	def getType(self,):
		"""
		Get the type form of the input word
		@return: the given type.
		@rtype: unicode string
		"""
		return self.type;
		
	def setType(self,newtype):
		"""
		Set the type word
		@param newtype: the new given type.
		@type newtype: unicode string
		"""
		self.type = newtype;
	def getRoot(self,):
		"""
		Get the root form of the input word
		@return: the given root.
		@rtype: unicode string
		"""
		return self.root;
		
	def setRoot(self,newroot):
		"""
		Set the root word
		@param newroot: the new given root.
		@type newroot: unicode string
		"""
		self.root = newroot;
		
	def getOriginal(self,):
		"""
		Get the original form of the input word
		@return: the given original.
		@rtype: unicode string
		"""
		return self.original;
		
	# def getUnvOriginal(self,):
		# """
		# Get the unvocalized  original form of the input word
		# @return: the given unvocalized original.
		# @rtype: unicode string
		# """
		# if self.unvoriginal:
			# return self.unvoriginal;			
		# else :
			# if self.original:
				# self.unvoriginal = araby.stripTashkeel(self.original);
			# else:
				# return u"";
 
	def setOriginal(self,neworiginal):
		"""
		Set the original word
		@param neworiginal: the new given original.
		@type neworiginal: unicode string
		"""
		self.original = neworiginal;

	######################################################################
	#{ Tags  Functions
	######################################################################		
	def isInitial(self):
		"""
		Return True if the word mark the begin of next sentence.
		@return: direct initial.
		@rtype: True/False;
		"""
		return self.tagInitial;

	#  حالة المضاف إليه		
	#--------------------------
	def isUnknown(self):
		"""
		Return True if the word is unknown.
		@return: is a noun.
		@rtype: True/False;
		"""			
		return (u'unknown' in self.getType());
	def isNoun(self):
		"""
		Return True if the word is a noun.
		@return: is a noun.
		@rtype: True/False;
		"""			
		return self.tagNoun;


	def isAdj(self):
		"""
		Return True if the word is an adjective.
		@return: is a adjective.
		@rtype: True/False;
		"""			
		return self.tagAdj;
	def isStopWord(self):
		"""
		Return True if the word is a stop word.
		@return: is a noun.
		@rtype: True/False;
		"""			
		return self.tagStopWord;
	def isVerb(self):
		"""
		Return True if the word is a verb.
		@return: is a verb.
		@rtype: True/False;
		"""			
		return self.tagVerb;

	def isMasdar(self):
		"""
		Return True if the word is a masdar.
		@return: is a masdar.
		@rtype: True/False;
		"""			
		return self.tagMasdar;
	def isProperNoun(self):
		"""
		Return True if the word is a proper noun.
		@return: is a propoer noun.
		@rtype: True/False;
		"""			
		return self.tagProperNoun;

	def isPounct(self):
		"""
		Return True if the word is a pounctuation.
		@return: is a verb.
		@rtype: True/False;
		"""			
		return self.tagPounct;


	def isTransparent(self):
		"""
		Return True if the word has the state transparent, which can trasnpose the effect of the previous factor.
		@return: has the state transparent.
		@rtype: True/False;
		"""
		#temporary, 
		# the transparent word are stopwords like هذا وذلك
		# the stopword tags have اسم إشارة,
		# a pounctuation can has the transparent tag like quotes., which havent any gramatical effect.
		# Todo 
		# حالة بذلك الرجل
		return self.tagTransparent;

		#----------------------------
		# affixes boolean attributes
		#----------------------------

	def isMajrour(self):
		"""
		Return True if the word has the state majrour.
		@return: has the state majrour.
		@rtype: True/False;
		"""
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isMajrour();
		return False;


	def isMajzoum(self):
		"""
		Return True if the word has the state majrour.
		@return: has the state majrour.
		@rtype: True/False;
		"""
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isMajzoum()
		return False;


	def isMansoub(self):
		"""
		Return True if the word has the state mansoub.
		@return: has the state mansoub.
		@rtype: True/False;
		"""
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isMansoub()
		return False;


	def isMarfou3(self):
		"""
		Return True if the word has the state marfou3.
		@return: has the state marfou3.
		@rtype: True/False;
		"""
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isMarfou3()
		return False;



	def isDefined(self):
		"""
		Return True if the word has the state definde.
		@return: has the state defined.
		@rtype: True/False;
		"""
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isDefined()
		return False;


	def isPast(self):
		"""
		Return True if the word has the tense past.
		@return: has the  tense past.
		@rtype: True/False;
		"""
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isPast()
		return False;



	def isPassive(self):
		"""
		Return True if the word has the tense passive.
		@return: has the  tense passive.
		@rtype: True/False;
		"""	
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isPassive()
		return False;


	def isPresent(self):
		"""
		Return True if the word has the tense present.
		@return: has the  tense present.
		@rtype: True/False;
		"""	
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isPresent()
		return False;

	def is3rdperson(self):
		"""
		Return True if the word has the 3rd person.
		@return: has the 3rd persontense.
		@rtype: True/False;
		"""
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].is3rdperson()
		return False;		




	def isTanwin(self):
		"""
		Return True if the word has tanwin.
		@return: has tanwin.
		@rtype: True/False;
		"""		
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isTanwin()
		return False;
	def hasJar(self):
		"""
		Return True if the word has tanwin.
		@return: has tanwin.
		@rtype: True/False;
		"""		
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].hasJar()
		return False;

	def isBreak(self):
		"""
		Return True if the word has break.
		@return: is break.
		@rtype: True/False;
		"""	
		#تكون الكلمة فاصلة إذا كانت منفصلة عمّا قبلها.	
		# الحالات التي تقطع
		# - حرف جر متصل
		# فاصلة أو نقطة
		return self.tagBreak;



	def isMasculinPlural(self):
		"""
		Return True if the word is  Masculin plural.
		@return: is masculin plural.
		@rtype: True/False;
		"""
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isMasculinPlural()
		return False;
	def isDual(self):
		"""
		Return True if the word is  dual.
		@return: is  dual.
		@rtype: True/False;
		"""
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isDual()
		return False;		
		return self.tagDual;
			
	def isFemininPlural(self):
		"""
		Return True if the word is  Feminin plural.
		@return: is Feminin plural.
		@rtype: True/False;
		"""
		if GlobalAffixes.has_key(self.affixKey):
			return GlobalAffixes[self.affixKey].isFemininPlural()
		return False;



	#-----------------------------
	# Mixed extraction attributes tests
	#-----------------------------

	def isMasculin(self):
		"""
		Return True if the word is masculin.
		@return: is masculin.
		@rtype: True/False;
		"""
		return not self.tagFeminin;

	def isFeminin(self):
		"""
		Return True if the word is Feminin.
		@return: is Feminin.
		@rtype: True/False;
		"""
		return self.tagFeminin;

	def isPlural(self):
		"""
		Return True if the word is a plural.
		@return: is plural.
		@rtype: True/False;
		"""
		return self.tagPlural;

	def isBrokenPlural(self):
		"""
		Return True if the word is broken  plural.
		@return: is broken plural.
		@rtype: True/False;
		"""
		return self.tagBrokenPlural;
	def isMamnou3(self):
		"""
		Return True if the word is Mamnou3 min Sarf.
		@return: is Mamnou3 min Sarf.
		@rtype: True/False;
		"""
		return self.tagMamnou3;

	def isSingle(self):
		"""
		Return True if the word is single.
		@return: is  dual.
		@rtype: True/False;
		"""
		return not self.isPlural() and not self.isDual();

	def isAdded(self):
		"""
		Return True if the word has the state added مضاف.
		@return: has the state added.
		@rtype: True/False;
		"""		
		return self.tagAdded

	######################################################################
	#{ Display Functions
	######################################################################
	def getDict(self,):
		return  self.__dict__
	def __repr__(self):
		"""
		Display objects result from analysis
		@return: text
		@rtype : text
		"""	
		text=u"{";
		stmword = self.__dict__;
		stmword['affix']='Taha';
		for key in stmword.keys():
				text+= u"\n\t\tu'%s' = u'%s',"%(key, stmword[key]);
		text+= u'\n\t\t}';
		return text.encode('utf8');

if __name__=="__main__":
	print "test";
	rdict={}
	rdict = {"word": "الحياة",		# input word
			"vocalized": "الْحَيَاةُ",   # vocalized form of the input word 
			"procletic": "ال",		# the syntaxic pprefix called procletic
			"prefix": "",			# the conjugation or inflection prefix
			"stem": "حياة",			# the word stem
			"suffix": "ُ", 			# the conjugation suffix of the word
			"encletic": "",			# the syntaxic suffix
			
			"tags": "تعريف::مرفوع*", # tags of affixes and tags extracted form lexical dictionary
			"freq": 0,				# the word frequency from Word Frequency database 
			"root": "",				# the word root; not yet used
			"template": "",			# the template وزن 
			"type": "Noun:مصدر",	# the word type
			"original": "حَيَاةٌ",		#original word from lexical dictionary
			"syntax":"",				# used for syntaxique analysis porpos
			u'semantic':'',
			};
	stmwrd=stemmedWord(rdict);
	print stmwrd.getDict();
	
	stmwrd.setWord("4444");
	stmwrd.setVocalized("4444");
	stmwrd.setProcletic("4444");
	stmwrd.setPrefix("4444");
	stmwrd.setStem("4444");
	stmwrd.setSuffix("4444");
	stmwrd.setEncletic("4444");
	stmwrd.setTags("4444");
	stmwrd.setFreq("4444");
	stmwrd.setRoot("4444");
	stmwrd.setTemplate("4444");
	stmwrd.setType("4444");
	stmwrd.setOriginal("4444");
	# stmwrd.setSyntax("4444");
	# stmwrd.setSyntax("4444");
	
	print stmwrd;
	
