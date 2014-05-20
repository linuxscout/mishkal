#!/usr/bin/python
# -*- coding = utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        wordCase
# Purpose:     representat data analyzed given by morphoanalyzer Qalsadi
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     18-05-2014
# Copyright:   (c) Taha Zerrouki 2014
# Licence:     GPL
#-------------------------------------------------------------------------------
if __name__=="__main__":
	import sys
	sys.path.append('..');
import pyarabic.araby as araby
import pyarabic.arabrepr as arabrepr
arabicRepr = arabrepr.ArabicRepr()
import analex_const 

class wordCase:
	"""
	wordCase represents the data resulted from the morpholocigal analysis
	"""
	def __init__(self, resultDict=None):
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
		self.freq =  0,				
		"""the word frequency from Word Frequency database """
		self.type =  u"",
		""" the word type  """
 		self.original =  u""	
 		""" original word from lexical dictionary"""
		if resultDict:
			self.word	= resultDict.get('word',u'');
			self.vocalized	= resultDict.get('vocalized',u'');
			self.semivocalized	= resultDict.get('semivocalized',u'');
			self.stem	= resultDict.get('stem',u'');
			self.affix  = resultDict.get('affix',[])
			self.tags	= u':'.join([resultDict.get('tags',u''), resultDict.get('originaltags',u'')]);			
			self.freq 	= resultDict.get('freq',u'');
			self.type	= resultDict.get('type',u'');
			self.original	= resultDict.get('original',u'');

	######################################################################
	#{ Attribut Functions
	######################################################################
	def get(self, key, default= u''):
		return self.__dict__.get(key,default)
	def __getitem__(self, key):
		return self.__dict__.get(key,'')
	def __setitem__(self, key, value):
		self.__dict__[key] = value;
	def __contains__(self, item):
		return item in self.__dict__;
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
	def getStem(self,):
		"""
		Get the stem form of the input word
		@return: the given stem.
		@rtype: unicode string
		"""
		return self.stem;
	def setStem(self, stem):
		"""
		set the stem form of the input word
		@param stem: given stem
		@type stem: unicode
		@return: the given stem.
		@rtype: unicode string
		"""
		self.stem=stem;		
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
	def getAffix(self,):
		"""
		Get the affix  form of the input word
		@return: the given affix.
		@rtype: unicode string
		"""
		return self.affix;
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
		
	def getOriginal(self,):
		"""
		Get the original form of the input word
		@return: the given original.
		@rtype: unicode string
		"""
		return self.original;
		
 
	def setOriginal(self,neworiginal):
		"""
		Set the original word
		@param neworiginal: the new given original.
		@type neworiginal: unicode string
		"""
		self.original = neworiginal;

	######################################################################
	#{ Display Functions
	######################################################################
	def __dict__(self,):
		return  self.__dict__
	def __repr__(self):
		"""
		Display objects result from analysis
		@return: text
		@rtype : text
		"""	
		return arabicRepr.repr(self.__dict__);

	def dump():
		"""
		Dump the word case as a simple list
		"""
		return self.__dict__;
	def load(aList):
		"""
		load word case attributes from a simple list stored in cache data base
		"""
		self.__dict__ = aList;

if __name__=="__main__":
	print "test";
	rdict={}
	rdict = {"word": u"الحياة",		# input word
			"vocalized": u"الْحَيَاةُ",   # vocalized form of the input word 
			"procletic": u"ال",		# the syntaxic pprefix called procletic
			"prefix": u"",			# the conjugation or inflection prefix
			"stem": u"حياة",			# the word stem
			"suffix": u"ُ", 			# the conjugation suffix of the word
			"encletic": u"",			# the syntaxic suffix
			
			"tags": u"تعريف::مرفوع*", # tags of affixes and tags extracted form lexical dictionary
			"freq": 0,				# the word frequency from Word Frequency database 
			"root": u"",				# the word root; not yet used
			"template": u"",			# the template وزن 
			"type": u"Noun:مصدر",	# the word type
			"original": u"حَيَاةٌ",		#original word from lexical dictionary
			"syntax":u"",				# used for syntaxique analysis porpos
			u'semantic':u'',
			};
	stmwrd  =wordCase(rdict);
	print stmwrd.__dict__;
	
	stmwrd.setWord("4444");
	stmwrd.setVocalized("4444");
	stmwrd.setStem("4444");
	stmwrd.setTags("4444");
	stmwrd.setFreq("4444");
	stmwrd.setType("4444");
	stmwrd.setOriginal("4444");
	
	print stmwrd;
	
