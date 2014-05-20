#!/usr/bin/python
# -*- coding = utf-8 -*-
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

import sys
sys.path.append('../lib/')
import pyarabic.araby as araby
import analex_const 
class stemmedAffix:
	"""
	stemmedAffix represents the data resulted from the morpholocigal analysis
	"""
	def __init__(self, resultDict=None):

		# extracted affix attributes
		self.procletic =  u"",	# the syntaxic pprefix called procletic
		self.prefix =  u"",		# the conjugation or inflection prefix
		self.suffix =  u"", 	# the conjugation suffix of the word
		self.encletic =  u"",	# the syntaxic suffix
		self.type =  u"",		# the word type used with affix		
		self.tags =  u"", 		# tags of affixes and tags extracted form lexical dictionary

		if resultDict:
			aff = resultDict.get('affix', [])
			if aff:
				self.procletic	= aff[0];			
				self.prefix	= aff[1];
				self.suffix	= aff[2];
				self.encletic	= aff[3];
			self.affix  = u'-'.join([self.procletic	, self.prefix, 	self.suffix	, self.encletic]);
			self.tags	= resultDict.get('tags',u'');
			self.type	= resultDict.get('type',u'');

		# not noun or stopword 
		self.tagStopWord	= False
		self.tagNoun		= False		
		self.tag3rdperson 	= False;		
		self.tag3rdperson 	= False;
		self.tagMajzoum 	= False;
		self.tagPassive		= False;
		self.tagPast		= False;
		self.tagPresent		= False;
		self.tagDefined 	= False;
		self.tagMajrour		= False;
		self.tagTanwin		= False;
		self.tagJar			= False;		
		# calculated  attributes 
		self.tagVerb		= self._isVerb();
		if self.tagVerb:
			self.tag3rdperson 	= self._is3rdperson();			
			self.tagMajzoum 	= self._isMajzoum();
			self.tagPassive		= self._isPassive();
			self.tagPast		= self._isPast();
			self.tagPresent		= self._isPresent();
		else:

			self.tagNoun		= self._isNoun();
			if self.tagNoun:
				self.tagDefined = self._isDefined();
				self.tagMajrour	= self._isMajrour();
				self.tagTanwin	= self._isTanwin();				
				self.tagJar		= self._hasJar();
				
			else:
				self.tagStopWord	= self._isStopWord();
		self.tagAdded 		= self._isAdded();
		self.tagMansoub		= self._isMansoub();
		self.tagMarfou3		= self._isMarfou3();

		self.tagFeminin		= self._isFeminin();		
		self.tagPlural		= self._isPlural();

		self.tagMasculinPlural	= self._isMasculinPlural();
		self.tagFemininPlural	= self._isFemininPlural();
		self.tagDual			= self._isDual();


	#  tags extracted from word dictionary 
	#--------------------------
	def _isNoun(self):
		"""
		Return True if the word is a noun.
		@return: is a noun.
		@rtype: True/False;
		"""			
		return u'Noun' in self.getType()

	def _isStopWord(self):
		"""
		Return True if the word is a stop word.
		@return: is a noun.
		@rtype: True/False;
		"""			
		return u'STOPWORD' in self.getType()

	def _isVerb(self):
		"""
		Return True if the word is a verb.
		@return: is a verb.
		@rtype: True/False;
		"""			
		return  u'Verb' in self.getType()


	def _isMajrour(self):
		"""
		Return True if the word has the state majrour.
		@return: has the state majrour.
		@rtype: True/False;
		"""				
		return  u'مجرور' in self.getTags();

	def _isBrokenPlural(self):
		"""
		Return True if the word is broken  plural.
		@return: is broken plural.
		@rtype: True/False;
		"""
		return u'جمع تكسير' in self.getTags();

	#  tags extracted from affixes 
	#--------------------------
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
	def getProcletic(self,):
		"""
		Get the procletic 
		@return: the given procletic.
		@rtype: unicode string
		"""
		return self.procletic;
	def setProcletic(self,newprocletic):
		"""
		Set the procletic 
		@param newprocletic: the new given procletic.
		@type newprocletic: unicode string
		"""
		self.procletic = newprocletic;
	def hasProcletic(self,):
		"""
		return True if has procletic 
		@return: True if procletic not empty.
		@rtype: Boolean
		"""
		return self.procletic!=u'';	
	def getPrefix(self,):
		"""
		Get the prefix 
		@return: the given prefix.
		@rtype: unicode string
		"""
		return self.prefix;
	def setPrefix(self,newprefix):
		"""
		Set the prefix 
		@param newprefix: the new given prefix.
		@type newprefix: unicode string
		"""
		self.prefix = newprefix;

	def setStem(self,newstem):
		"""
		Set the stem word
		@param newstem: the new given stem.
		@type newstem: unicode string
		"""
		self.stem = newstem;
	def getSuffix(self,):
		"""
		Get the suffix 
		@return: the given suffix.
		@rtype: unicode string
		"""
		return self.suffix;
	def setSuffix(self,newsuffix):
		"""
		Set the suffix word
		@param newsuffix: the given suffix.
		@type newsuffix: unicode string
		"""
		self.suffix = newsuffix;
	def getEncletic(self,):
		"""
		Get the encletic 
		@return: the given encletic.
		@rtype: unicode string
		"""
		return self.encletic;
	def setEncletic(self,newencletic):
		"""
		Set the encletic 
		@param newencletic: the given encletic.
		@type newencletic: unicode string
		"""
		self.encletic = newencletic;			
		
	def hasEncletic(self,):
		"""
		return True if has encletic 
		@return: True if encletic not empty.
		@rtype: Boolean
		"""
		return self.encletic!=u'';

	def _isMajzoum(self):
		"""
		Return True if the word has the state majrour.
		@return: has the state majrour.
		@rtype: True/False;
		"""		
		return  u'مجزوم'in self.getTags();

	def _isMansoub(self):
		"""
		Return True if the word has the state mansoub.
		@return: has the state mansoub.
		@rtype: True/False;
		"""			
		return u'منصوب'in self.getTags();

	def _isMarfou3(self):
		"""
		Return True if the word has the state marfou3.
		@return: has the state marfou3.
		@rtype: True/False;
		"""		
		if u'مرفوع'in self.getTags():
			return True;
		return u'مضارع' in self.getTags() and not self._isMansoub() and not self._isMajzoum();

	def _isDefined(self):
		"""
		Return True if the word has the state definde.
		@return: has the state defined.
		@rtype: True/False;
		"""		
		return  u'تعريف'in self.getTags();


	def _isPast(self):
		"""
		Return True if the word has the tense past.
		@return: has the  tense past.
		@rtype: True/False;
		"""		
		return  u'ماضي'in self.getTags()


	def _isPassive(self):
		"""
		Return True if the word has the tense passive.
		@return: has the  tense passive.
		@rtype: True/False;
		"""	
		return  u'مجهول'in self.getTags()

	def _isPresent(self):
		"""
		Return True if the word has the tense present.
		@return: has the  tense present.
		@rtype: True/False;
		"""	
		return u'مضارع' in self.getTags()


	def _is3rdperson(self):
		"""
		Return True if the word has the 3rd person.
		@return: has the 3rd persontense.
		@rtype: True/False;
		"""	
		return (u':هي:' in self.getTags() or u':هو:' in self.getTags()) and not u'مفعول به' in self.getTags()



	def _isTanwin(self):
		"""
		Return True if the word has tanwin.
		@return: has tanwin.
		@rtype: True/False;
		"""		
		return  u'تنوين'in self.getTags()
	def _isMasculinPlural(self):
		"""
		Return True if the word is  Masculin plural.
		@return: is masculin plural.
		@rtype: True/False;
		"""
		return  u'جمع مذكر سالم' in self.getTags()
			
	def _isFemininPlural(self):
		"""
		Return True if the word is  Feminin plural.
		@return: is Feminin plural.
		@rtype: True/False;
		"""
		return u'جمع مؤنث سالم' in self.getTags()

	def _isDual(self):
		"""
		Return True if the word is  dual.
		@return: is  dual.
		@rtype: True/False;
		"""
		return u'مثنى' in self.getTags()

	def _hasJar(self):
		"""
		Return True if the word has a jar factor attached.
		@return: has jar.
		@rtype: True/False;
		"""		
		return  u'جر:'in self.getTags()


	# Mixed affix and dictionary attrrubutes
	#---------------------------------------
	def _isAdded(self):
		"""
		Return True if the word has the state added مضاف.
		@return: has the state added.
		@rtype: True/False;
		"""		
		return  u'مضاف' in self.getTags() or u'اسم إضافة' in self.getTags()

	def _isMasculin(self):
		"""
		Return True if the word is masculin.
		@return: is masculin.
		@rtype: True/False;
		"""
		return  not self._isFeminin();

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
		if u'مؤنث' in self.getTags():
			return True;
		return  u'جمع مؤنث سالم' in self.getTags()

	def _isPlural(self):
		"""
		Return True if the word is a plural.
		@return: is plural.
		@rtype: True/False;
		"""
		return  u'جمع' in self.getTags()

	def _isSingle(self):
		"""
		Return True if the word is single.
		@return: is  dual.
		@rtype: True/False;
		"""
		return not self._isPlural() and not self._isDual();




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

	######################################################################
	#{ Tags  Functions
	######################################################################		

	def isNoun(self):
		"""
		Return True if the word is a noun.
		@return: is a noun.
		@rtype: True/False;
		"""			
		return self.tagNoun;

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

	def isMajrour(self):
		"""
		Return True if the word has the state majrour.
		@return: has the state majrour.
		@rtype: True/False;
		"""				
		return self.tagMajrour;


	def isMajzoum(self):
		"""
		Return True if the word has the state majrour.
		@return: has the state majrour.
		@rtype: True/False;
		"""		
		return self.tagMajzoum;


	def isMansoub(self):
		"""
		Return True if the word has the state mansoub.
		@return: has the state mansoub.
		@rtype: True/False;
		"""			
		return self.tagMansoub;

	def isMarfou3(self):
		"""
		Return True if the word has the state marfou3.
		@return: has the state marfou3.
		@rtype: True/False;
		"""		
		return self.tagMarfou3;


	def isDefined(self):
		"""
		Return True if the word has the state definde.
		@return: has the state defined.
		@rtype: True/False;
		"""		
		return self.tagDefined;


	def isPast(self):
		"""
		Return True if the word has the tense past.
		@return: has the  tense past.
		@rtype: True/False;
		"""		
		return self.tagPast;


	def isPassive(self):
		"""
		Return True if the word has the tense passive.
		@return: has the  tense passive.
		@rtype: True/False;
		"""	
		return self.tagPassive;


	def isPresent(self):
		"""
		Return True if the word has the tense present.
		@return: has the  tense present.
		@rtype: True/False;
		"""	
		return self.tagPresent;

	def is3rdperson(self):
		"""
		Return True if the word has the 3rd person.
		@return: has the 3rd persontense.
		@rtype: True/False;
		"""	
		return self.tag3rdperson;

	def isAdded(self):
		"""
		Return True if the word has the state added مضاف.
		@return: has the state added.
		@rtype: True/False;
		"""		
		return self.tagAdded


	def isTanwin(self):
		"""
		Return True if the word has tanwin.
		@return: has tanwin.
		@rtype: True/False;
		"""		
		return self.tagTanwin;
	def hasJar(self):
		"""
		Return True if the word has tanwin.
		@return: has tanwin.
		@rtype: True/False;
		"""		
		return self.tagJar;

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
		return self.tagMasculinPlural;

			
	def isFemininPlural(self):
		"""
		Return True if the word is  Feminin plural.
		@return: is Feminin plural.
		@rtype: True/False;
		"""
		return self.tagFemininPlural;

	def isMasculin(self):
		"""
		Return True if the word is masculin.
		@return: is masculin.
		@rtype: True/False;
		"""
		return self.tagMasculin;

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



	def isDual(self):
		"""
		Return True if the word is  dual.
		@return: is  dual.
		@rtype: True/False;
		"""
		return self.tagDual;

	def isSingle(self):
		"""
		Return True if the word is single.
		@return: is  dual.
		@rtype: True/False;
		"""
		return self.tagSingle;


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
		stmword = self.__dict__
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
