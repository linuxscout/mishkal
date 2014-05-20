#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        stemmedWord
# Purpose:     representat data analyzed given by morphoanalyzer Qalsadi then by syntaxic analyzer
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     19-09-2012
# Copyright:   (c) Taha Zerrouki 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
import sys
sys.path.append('../lib');
import qalsadi.stemmedword as stemmedword

import syn_const
import pyarabic.araby as araby
import math
class stemmedSynWord (stemmedword.stemmedWord):
	"""
	stemmedWord represents the data resulted from the morpholocigal analysis
	"""
	def __init__(self, resultDict=None, order=-1):
		# ToDo
		# copy the super class attributes to curesultDictrrent classe
		#stemmedword.stemmedWord.__init__(self, resultDict.getDict())
		self.unvocalized= u""
		self.unvoriginal= u""

		
		if resultDict: 
			self.__dict__=resultDict.__dict__.copy()
			self.unvocalized= araby.stripTashkeel(self.vocalized);
			self.unvoriginal= araby.stripTashkeel(self.original);
		if self.tagStopWord:
			self.tagDirectJar 	=  self._isDirectJar();
			self.tagJar 		=  self._isJar();
			self.tagDirectNaseb 	=  self._isDirectNaseb();
			self.tagDirectRafe3 	=  self._isDirectRafe3();			
			self.tagDirectNominalFactor = self.tagJar or self.tagDirectJar  or self.tagDirectNaseb or self.tagDirectRafe3 or  self._isDirectNominalFactor();
			self.tagNominalFactor =  self._isNominalFactor();

			#verbal factor
			self.tagDirectJazem 	=  self._isDirectJazem();
			self.tagDirectVerbNaseb =  not self.tagDirectJazem and self._isDirectVerbNaseb();
			self.tagDirectVerbRafe3 =  not self.tagDirectVerbNaseb and self._isDirectVerbRafe3();
			self.tagVerbalFactor = self.tagDirectJazem or self.tagDirectVerbNaseb or self.tagDirectVerbRafe3 or  self._isVerbalFactor();
			self.tagDirectVerbalFactor = self.tagDirectJazem or self.tagDirectVerbNaseb or self.tagDirectVerbRafe3 or  self._isDirectVerbalFactor();

			self.tagJazem 	=  self._isJazem();
			self.tagNaseb 	=  not self.tagJazem and self._isNaseb();
			self.tagRafe3 	=  not self.tagNaseb and self._isRafe3();
			self.tagKanaRafe3 	=  self._isKanaRafe3();		
			self.tagVerbNaseb =  self._isVerbNaseb();
			self.tagVerbRafe3 = not self.tagVerbNaseb and self._isVerbRafe3();
		else:
			self.tagDirectJar 	= False
			self.tagDirectJazem 	= False
			self.tagDirectNaseb 	= False
			self.tagDirectNominalFactor = False
			self.tagDirectRafe3 	= False
			self.tagDirectVerbNaseb = False
			self.tagDirectVerbRafe3 = False
			self.tagNominalFactor = False
			self.tagJar 	= False
			self.tagJazem 	= False
			self.tagNaseb 	= False
			self.tagRafe3 	= False
			self.tagKanaRafe3 	= 	False	
			self.tagVerbNaseb = False
			self.tagVerbRafe3 = False			


		self.tagDirectAddition 	= self._isDirectAddition();
		self.tagAddition 	= self._isAddition();				

		self.tagBreak		= self._isBreak(); 
		self.tagKanaNoun		=False; # اسم كان
		self.tagInnaNoun		=False; # اسم إنّ
		self.setOrder(order);
		self.forcedWordCase=False;
		self.syntax = u""				# used for syntaxique analysis porpos
		self.semantic = u""			# used for semantic analysis porposes
		
		#self.order			= order;
		self.next			= {};
		self.previous		= {};
		# to ,specify semantic relations
		self.semNext		= {};
		self.semPrevious	= {};
		self.score 			= 0;

	def __del__(self,):
		""" desctructor """
		pass;
	######################################################################
	#{ Attributes Functions
	######################################################################		
	def getUnvocalized(self,):
		"""
		Get the unvocalized form of the input word
		@return: the given unvocalized.
		@rtype: unicode string
		"""
		if self.unvocalized:
			return self.unvocalized;
		else:
			if self.vocalized:
				self.unvocalized=araby.stripTashkeel(self.vocalized);
			else :
				return u"";
		return self.unvocalized;
	def setUnvocalized(self,newunvocalized):
		"""
		Set the unvocalized word
		@param newunvocalized: the new given unvocalized.
		@type newunvocalized: unicode string
		"""
		self.unvocalized = newunvocalized;
		
	def getUnvOriginal(self,):
		"""
		Get the unvocalized  original form of the input word
		@return: the given unvocalized original.
		@rtype: unicode string
		"""
		if self.unvoriginal:
			return self.unvoriginal;			
		else :
			if self.original:
				self.unvoriginal = araby.stripTashkeel(self.original);
			else:
				return u"";
			return self.unvoriginal;

	def setOrder(self, order):
		"""
		Add a position number in the case word list.
		@param order: the order of  the stemmed word in the word case list.
		@tyep order: integer;
		"""
		#self.syntax = ':'.join([self.syntax,'O%d'%order]);
		self.order=order;

	def getOrder(self):
		"""
		Add a position number in the case word list.
		@param order: the order of  the stemmed word in the word case list.
		@tyep order: integer;
		"""
		return self.order;

	def setScore(self, Score):
		"""
		Set the word case score
		@param Score: the Score of  the stemmed word in the word case list.
		@tyep Score: integer;
		"""
		self.score=Score;

	def getScore(self):
		"""
		get the case word score
		@param Score: the Score of  the stemmed word in the word case list.
		@tyep Score: integer;
		"""
		return self.score;
	def getSyntax(self,):
		"""
		Get the syntax form of the input word
		@return: the given syntax.
		@rtype: unicode string
		"""
		return self.syntax;
		
	def setSyntax(self,newsyntax):
		"""
		Set the syntax word
		@param newsyntax: the new given syntax.
		@type newsyntax: unicode string
		"""
		self.syntax = newsyntax;
	def addSyntax(self, tag):
		"""
		Add a new tag to syntax field
		@param tag: the new added tag.
		@tyep tag: unicode;
		"""
		self.syntax = ':'.join([self.syntax,tag]);		
	def getSemantic(self,):
		"""
		Get the semantic form of the input word
		@return: the given semantic.
		@rtype: unicode string
		"""
		return self.semantic;
		
	def setSemantic(self,newsemantic):
		"""
		Set the semantic word
		@param newsemantic: the new given semantic.
		@type newsemantic: unicode string
		"""
		self.semantic = newsemantic;
	def addNext(self, next, weight=1):
		"""
		Add  next word position number, if the word is realted
		@param next: the next of  the stemmed word in the word case list.
		@tyep next: integer;
		"""
		#self.syntax = ':'.join([self.syntax,'N%d[%d]'%(next,weight)]);
		self.next[next]=weight;

	def getNext(self):
		"""
		get the next positions.
		@param next: the next of  the stemmed word in the word case list.
		@tyep next: integer;
		"""
		return self.next.keys();

	def hasNext(self, next=None):
		"""
		get True if current word has next relations. If The next is given, it returns if the next has relation with current. 
		@param next: a stemmedsynword as next of the current word case. if it's None, the fucntion return if there are relation.
		@type next: stemmedsynword.
		@return: if the word has next relations
		@rtype: boolean;
		"""
		if not next:
			return self.next!={};
		else:
			return self.next.has_key(next.getOrder());
	def hasPrevious(self, previous=None):
		"""
		get True if current word has previous relations. If The previous is given, it returns if the previous has relation with current. 
		@param previous: a stemmedsynword as previous of the current word case. if it's None, the fucntion return if there are relation.
		@type previous: stemmedsynword.
		@return: if the word has previous relations
		@rtype: boolean;
		"""
		if not previous:
			return self.previous!={};
		else:
			return self.previous.has_key(next.getOrder());

	def addPrevious(self, previous, weight=1):
		"""
		Add the previous position of the related word.
		@param previous: the previous of  the stemmed word in the word case list.
		@tyep previous: integer;
		"""
		#self.syntax = ':'.join([self.syntax,'P%d[%d]'%(previous,weight)]);
		self.previous[previous]=weight;

	def getPrevious(self):
		"""
		Add a position number in the case word list.
		@param previous: the previous of  the stemmed word in the word case list.
		@tyep previous: integer;
		"""
		return self.previous.keys();		

	def addSemNext(self, next, weight=1):
		"""
		Add  next word position number, if the word is semanticly related
		@param next: the next of  the stemmed word in the word case list.
		@tyep next: integer;
		"""
		#self.syntax = ':'.join([self.syntax,'SN%d[%d]'%(next,weight)]);
		self.semNext[next]=weight;

	def getSemNext(self):
		"""
		get the next positions.
		@param next: the next of  the stemmed word in the word case list.
		@tyep next: integer;
		"""
		return self.semNext.keys();


	def hasSemNext(self):
		"""
		get True if current word has semantic next relations
		@return: if the word has next relations
		@rtype: boolean;
		"""
		return self.semNext!={};

	def addSemPrevious(self, previous, weight=1):
		"""
		Add the previous position of the semantic related word.
		@param previous: the previous of  the stemmed word in the word case list.
		@tyep previous: integer;
		"""
		#self.syntax = ':'.join([self.syntax,'SP%d[%d]'%(previous,weight)]);
		self.semPrevious[previous]= weight;

	def getSemPrevious(self):
		"""
		Add a position number in the case word list.
		@param previous: the previous of  the stemmed word in the word case list.
		@tyep previous: integer;
		"""
		return self.semPrevious.keys();
	def forcedCase(self):
		"""
		Add a new tag to syntax field as foced case
		@param tag: the new added tag.
		@tyep tag: unicode;
		"""
		self.forcedWordCase=True;
		#if u"*" not in self.syntax: self.addSyntax(u"*");

	def forcedWordType(self):
		"""
		Add a new tag to syntax field as foced word type (noun, verb)
		@param tag: the new added tag.
		@tyep tag: unicode;
		"""
		self.forcedWordType=True;
		# self.addSyntax(u"#");
		
	def isForcedCase(self):
		"""
		verify if the word is a forced word type (noun, verb)
		@return: True/False
		@tyep tag: Boolean;
		"""
		return self.forcedWordCase#=True;
		# return u"*" in self.syntax;

	def isForcedWordType(self):
		"""
		verify if the word is a forced word type (noun, verb)
		@return: True/False
		@tyep tag: Boolean;
		"""
		return self.forcedWordType; #u"#" in self.syntax;
	######################################################################
	#{ Tags extraction Functions
	######################################################################		




	def _isJar(self):
		"""
		Return True if the word is a  Jar.
		@return:  Jar.
		@rtype: True/False;
		"""	
		if (not self.hasEncletic()) and u"حرف جر" in self.getTags():	
			return True;
		if (not self.hasEncletic()) and u"ظرف مكان" in self.getTags():	
			return True;
		if (not self.hasEncletic()) and u"اسم إضافة" in self.getTags():	
			return True;			
		if self.getUnvocalized() in syn_const.JAR_LIST:
			return True;
		# if (not self.hasEncletic()) and self.getUnvOriginal() in syn_const.JAR_LIST:	
			# return True;
		return False;

	def _isVerbNaseb(self):
		"""
		Return True if the word is a  Naseb of verb.
		@return:  Naseb.
		@rtype: True/False;
		"""	
		if self.getVocalized() in syn_const.VERB_NASEB_LIST :
			return True;
		if (not self.hasEncletic() and self.getOriginal() in syn_const.VERB_NASEB_LIST ):
			return True;
		return False;


	def _isJazem(self,):
		"""
		Return True if the word is a  Jazem.
		@return:  Jazem.
		@rtype: True/False;
		"""

		if self.getUnvocalized() in syn_const.JAZEM_LIST  :
			return True;
		if (not self.hasEncletic() and self.getUnvOriginal() in syn_const.JAZEM_LIST  ):
			return True;
		return False;

	def _isNaseb(self):
		"""
		Return True if the word is a  Naseb of noun.
		@return:  Naseb of noun.
		@rtype: True/False;
		"""
		if self.getUnvocalized() in syn_const.NOUN_NASEB_LIST :
			return True;
		elif (not self.hasEncletic()) and u"إن و أخواتها" in self.getTags():	
			return True;
		elif (not self.hasEncletic() and self.getUnvOriginal() in syn_const.NOUN_NASEB_LIST ):
			return True;
		return False;


	def _isRafe3(self):
		"""
		Return True if the word is a  Rafe3.
		@return:  Rafe3.
		@rtype: True/False;
		"""
		if self.getUnvocalized() in syn_const.RAFE3_LIST or (not self.hasEncletic() and self.getUnvOriginal() in syn_const.RAFE3_LIST ):
			return True;
		elif (not self.hasEncletic()) and u"كان و أخواتها" in self.getTags():	
			return True;

		return False;

	def _isKanaRafe3(self):
		"""
		Return True if the word is a  Rafe3.
		@return:  Rafe3.
		@rtype: True/False;
		"""
		if (not self.hasEncletic()) and u"كان و أخواتها" in self.getTags():	
			return True;
		return False;



	def _isVerbRafe3(self):
		"""
		Return True if the word is a  Rafe3 of verb
		@return:  Rafe3 of verb.
		@rtype: True/False;
		"""
		if self.getUnvocalized() in syn_const.VERB_RAFE3_LIST or (not self.hasEncletic() and self.getUnvOriginal() in syn_const.VERB_RAFE3_LIST ):
			return True;
		return False;
		
	def _isNominalFactor(self):
		"""
		Return True if the word is a  nominal factor.
		@return:  is a  nominal factor.
		@rtype: True/False;
		"""
		if self.getUnvocalized() in syn_const.NOMINAl_FACTOR_LIST or (not self.hasEncletic() and self.getUnvOriginal() in syn_const.NOMINAl_FACTOR_LIST ):
			return True;
		elif self._isJar() or self._isNaseb() or self._isRafe3() or self._isInitial():
			return True; 
		return False;		
	def _isAddition(self):
		"""
		Return True if the word is a  nominal addition اسم إضافة مثل نحو ومعاذ
		@rtype: True/False;
		"""
		if u'اسم إضافة' in self.getTags() and not self.hasEncletic():
			return True;
		return False;

	def _isVerbalFactor(self):
		"""
		Return True if the word is a  verbal factor.
		@return:  is a  verbal factor.
		@rtype: True/False;
		"""	
		#if the stopword is a  verb factor
		# without vocalization
		if self.getUnvocalized() in syn_const.VERBAL_FACTOR_LIST :
			return True;
		# with encletics
		elif self.hasEncletic() and self.getUnvOriginal() in syn_const.VERBAL_FACTOR_LIST :
			return True;
		# with encletic and Harakat			
		elif self.hasEncletic() and self.getOriginal() in syn_const.VERBAL_FACTOR_LIST:
			return True;
		elif self._isJazem() or self._isVerbNaseb() or self._isVerbRafe3():
			return True; 			
		return False;

	def _isDirectJar(self):
		"""
		Return True if the word is a direct Jar.
		@return: direct Jar.
		@rtype: True/False;
		"""	
		if (not self.hasEncletic()) and u"حرف جر" in self.getTags():	
			return True;
		if (not self.hasEncletic()) and u"ظرف مكان" in self.getTags():	
			return True;
		# if self.getUnvocalized() in syn_const.JAR_LIST:
			# return True;
		# if (not self.hasEncletic()) and self.getUnvOriginal() in syn_const.JAR_LIST:	
			# return True;
		return False;

	def _isDirectVerbNaseb(self):
		"""
		Return True if the word is a direct Naseb of verb.
		@return: direct Naseb.
		@rtype: True/False;
		"""	
		if self.getUnvocalized() in syn_const.DIRECT_VERB_NASEB_LIST :
			return True;
		if (not self.hasEncletic() and self.getUnvOriginal() in syn_const.DIRECT_VERB_NASEB_LIST ):
			return True;
		return False;


	def _isDirectJazem(self,):
		"""
		Return True if the word is a direct Jazem.
		@return: direct Jazem.
		@rtype: True/False;
		"""

		if self.getUnvocalized() in syn_const.DIRECT_JAZEM_LIST  :
			return True;
		if (not self.hasEncletic() and self.getUnvOriginal() in syn_const.DIRECT_JAZEM_LIST  ):
			return True;
		return False;

	def _isDirectNaseb(self):
		"""
		Return True if the word is a direct Naseb of noun.
		@return: direct Naseb of noun.
		@rtype: True/False;
		"""
		if self.getUnvocalized() in syn_const.DIRECT_NOUN_NASEB_LIST :
			return True;
		elif (not self.hasEncletic()) and u"إن و أخواتها" in self.getTags():	
			return True;
		elif (not self.hasEncletic() and self.getUnvOriginal() in syn_const.DIRECT_NOUN_NASEB_LIST ):
			return True;
		return False;


	def _isDirectRafe3(self):
		"""
		Return True if the word is a direct Rafe3.
		@return: direct Rafe3.
		@rtype: True/False;
		"""
		if self.getUnvocalized() in syn_const.DIRECT_RAFE3_LIST or (not self.hasEncletic() and self.getUnvOriginal() in syn_const.DIRECT_RAFE3_LIST ):
			return True;
		elif (not self.hasEncletic()) and u"كان و أخواتها" in self.getTags():	
			return True;

		return False;


	def _isDirectVerbRafe3(self):
		"""
		Return True if the word is a direct Rafe3 of verb
		@return: direct Rafe3 of verb.
		@rtype: True/False;
		"""
		if self.getUnvocalized() in syn_const.DIRECT_VERB_RAFE3_LIST or (not self.hasEncletic() and self.getUnvOriginal() in syn_const.DIRECT_VERB_RAFE3_LIST ):
			return True;
		return False;
		
	def _isDirectNominalFactor(self):
		"""
		Return True if the word is a direct nominal factor.
		@return:  is a direct nominal factor.
		@rtype: True/False;
		"""
		if self.getUnvocalized() in syn_const.DIRECT_NOMINAl_FACTOR_LIST or (not self.hasEncletic() and self.getUnvOriginal() in syn_const.DIRECT_NOMINAl_FACTOR_LIST ):
			return True;
		elif self._isDirectJar() or self._isDirectNaseb() or self._isDirectRafe3() or self._isInitial():
			return True; 
		return False;		
	def _isDirectAddition(self):
		"""
		Return True if the word is a direct nominal addition اسم إضافة مثل نحو ومعاذ
		@rtype: True/False;
		"""
		if u'اسم إضافة' in self.getTags() and not self.hasEncletic():
			return True;
		return False;

	def _isDirectVerbalFactor(self):
		"""
		Return True if the word is a direct verbal factor.
		@return:  is a direct verbal factor.
		@rtype: True/False;
		"""	
		#if the stopword is a direct verb factor
		# without vocalization
		if self.getUnvocalized() in syn_const.DIRECT_VERBAL_FACTOR_LIST :
			return True;
		# with encletics
		elif self.hasEncletic() and self.getUnvOriginal() in syn_const.DIRECT_VERBAL_FACTOR_LIST :
			return True;
		# with encletic and Harakat			
		elif self.hasEncletic() and self.getOriginal() in syn_const.DIRECT_VERBAL_FACTOR_LIST:
			return True;
		elif self._isDirectJazem() or self._isDirectVerbNaseb() or self._isDirectVerbRafe3():
			return True; 			
		return False;

		
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
		if self.isDirectJar():
			return True;
		elif self.hasProcletic() and self.hasJar():
			return True;
		elif u'عطف' in self.getTags() or araby.WAW in self.getProcletic() or araby.FEH in self.getProcletic():
			return True;
		elif self.isPounct() and 'break' in self.getTags():
			return True;
		elif self.isStopWord():
			return True;
		else:
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


	def isDirectJar(self):
		"""
		Return True if the word is a direct Jar.
		@return: direct Jar.
		@rtype: True/False;
		"""	

		return self.tagDirectJar;

	def isDirectVerbNaseb(self):
		"""
		Return True if the word is a direct Naseb of verb.
		@return: direct Naseb.
		@rtype: True/False;
		"""	
		return self.tagDirectVerbNaseb;


	def isDirectJazem(self,):
		"""
		Return True if the word is a direct Jazem.
		@return: direct Jazem.
		@rtype: True/False;
		"""

		return self.tagDirectJazem;

	def isDirectNaseb(self):
		"""
		Return True if the word is a direct Naseb of noun.
		@return: direct Naseb of noun.
		@rtype: True/False;
		"""
		return self.tagDirectNaseb;


	def canHaveTanwin(self,):
		"""
		return True if the word accept Tanwin
		"""
		return u'ينون' in self.getTags();

	def isDirectRafe3(self):
		"""
		Return True if the word is a direct Rafe3.
		@return: direct Rafe3.
		@rtype: True/False;
		"""
		return self.tagDirectRafe3;


	def isDirectVerbRafe3(self):
		"""
		Return True if the word is a direct Rafe3 of verb
		@return: direct Rafe3 of verb.
		@rtype: True/False;
		"""
		return self.tagDirectVerbRafe3;
		
	def isDirectNominalFactor(self):
		"""
		Return True if the word is a direct nominal factor.
		@return:  is a direct nominal factor.
		@rtype: True/False;
		"""
		return self.tagDirectNominalFactor;		
	def isDirectAddition(self):
		"""
		Return True if the word is a direct Addition اسم إضافة مثل نحو ومعاذ.
		@return:  is a direct addition.
		@rtype: True/False;
		"""
		return self.tagDirectAddition;	

	def isDirectVerbalFactor(self):
		"""
		Return True if the word is a direct verbal factor.
		@return:  is a direct verbal factor.
		@rtype: True/False;
		"""	
		return self.tagDirectVerbalFactor;

		
	def isJar(self):
		"""
		Return True if the word is a  Jar.
		@return:  Jar.
		@rtype: True/False;
		"""	
		return self.tagJar;

	def isVerbNaseb(self):
		"""
		Return True if the word is a  Naseb of verb.
		@return:  Naseb.
		@rtype: True/False;
		"""	
		return self.tagVerbNaseb;


	def isJazem(self,):
		"""
		Return True if the word is a  Jazem.
		@return:  Jazem.
		@rtype: True/False;
		"""

		return self.tagJazem;

	def isNaseb(self):
		"""
		Return True if the word is a  Naseb of noun.
		@return:  Naseb of noun.
		@rtype: True/False;
		"""
		return self.tagNaseb;




	def isRafe3(self):
		"""
		Return True if the word is a  Rafe3.
		@return:  Rafe3.
		@rtype: True/False;
		"""
		return self.tagRafe3;


	def isKanaRafe3(self):
		"""
		Return True if the word is a  Rafe3.
		@return:  Rafe3.
		@rtype: True/False;
		"""
		return self.tagKanaRafe3;

	def isVerbRafe3(self):
		"""
		Return True if the word is a  Rafe3 of verb
		@return:  Rafe3 of verb.
		@rtype: True/False;
		"""
		return self.tagVerbRafe3;
		
	def isNominalFactor(self):
		"""
		Return True if the word is a  nominal factor.
		@return:  is a  nominal factor.
		@rtype: True/False;
		"""
		return self.tagNominalFactor;		
	def isAddition(self):
		"""
		Return True if the word is a  Addition اسم إضافة مثل نحو ومعاذ.
		@return:  is a  addition.
		@rtype: True/False;
		"""
		return self.tagAddition;	

	def isKanaNoun(self):
		"""
		Return True if the word is a  Kana Noun اسم كان منصوب.
		@return:  is a  Kana Noun.
		@rtype: True/False;
		"""
		return self.tagKanaNoun;

	def setKanaNoun(self):
		"""
		Set True to the word to be  Kana Noun اسم كان منصوب.
		"""
		self.tagKanaNoun = True;

	def isInnaNoun(self):
		"""
		Return True if the word is a  Inna Noun اسم إنّ مرفوع.
		@return:  is a  Inna Noun.
		@rtype: True/False;
		"""
		return self.tagInnaNoun;

	def setInnaNoun(self):
		"""
		Set True to the word to be  Inna Noun اسم إنّ.
		"""
		self.tagInnaNoun = True;

	def isVerbalFactor(self):
		"""
		Return True if the word is a  verbal factor.
		@return:  is a  verbal factor.
		@rtype: True/False;
		"""	
		return self.tagVerbalFactor;

	def ajustTanwin(self):
		"""
		ajust the Tanwin case, if the word is independent from the next one.
		@return:  Nothing.
		@rtype: ;
		"""	
		if self.isNoun() and not self.isStopWord() and not self.isDefined() and not self.hasEncletic() and not self.isMamnou3():
			#self.vocalized+='4';
			if self.vocalized.endswith(araby.DAMMA):
				self.vocalized=self.vocalized[:-1]+araby.DAMMATAN;
			elif self.vocalized.endswith(araby.KASRA):
				self.vocalized=self.vocalized[:-1]+araby.KASRATAN;
			elif self.vocalized.endswith(araby.TEH_MARBUTA+araby.FATHA):
				self.vocalized=self.vocalized[:-1]+araby.FATHATAN;
			elif self.vocalized.endswith(araby.FATHA+araby.ALEF):
				self.vocalized=self.vocalized[:-2]+araby.FATHATAN+araby.ALEF;
		

	def recalculateScore(self, previousCasePosition, previousScore):
		"""
		Recalculate score according to previous node.
		@param previousCasePosition: the pervious position in previos table
		@type  previousCasePosition: integer;
		@param previousScore: the word case previous score
		@type  previousScore: integer.
		@return: nothing
		@rtype: void
		"""
		#self.score = 0;
		
		# the score is calculated
		# syntaxic relations
		score  = 1;
		# if the current node has relation with previous as semantic
		if self.semPrevious.has_key(previousCasePosition):
			self.semPrevious[previousCasePosition]=max(self.previous[previousCasePosition],previousScore*2);
			score += self.semPrevious[previousCasePosition]
		# if the current node has relation with previous as synatxic
		if self.previous.has_key(previousCasePosition):
			self.previous[previousCasePosition]= max(self.previous[previousCasePosition], previousScore *1);
			score += self.previous[previousCasePosition*1]
		# case if the previous has no relation with the current*
		score+= len(self.semPrevious)*2 +len(self.previous)*1
		# To prefere semantic nexts relation then
		# to favorize syntaxic next relations
		score  *= (len(self.semNext)*2+len(self.next)*1)

		# Add frequency value as logarithm
		score *= round(math.log(self.freq+1), 2);
		# favorize the word if it's stopword
		#score += self.isStopWord()*50
		
		# the the max between acutal score and given score
		self.score = max(self.score, score);
		
		#self.addSyntax("Scr:"+str(self.score));


	def calculateScore(self, ):
		"""
		Recalculate score.
		@return: nothing
		@rtype: void
		"""
		self.score = 0;
		
		# the score is calculated
		#
		#self.score = max(len(self.next), 1)*max(len(self.previous), 1) * max(len(self.semPrevious), 1) * max(len(self.semNext), 1) * max(self.freq, 1)
		#self.score = len(self.next)*5+ len(self.previous)*5 + len(self.semPrevious)*10 + len(self.semNext)*10 + freq_score
		# syntaxic relations
		self.score  = len(self.next)*10 #self.hasNext()*10
		self.score += len(self.previous)*10#(self.previous>0)*10
		self.score += len(self.semPrevious)*100 #(self.semPrevious>0)
		self.score += len(self.semNext)*100 # self.hasSemNext()*100 
		self.score += round(math.log(self.freq+1), 2);
		self.score += self.isStopWord()*50
		self.addSyntax("Scr:"+str(self.score));

	def getScore(self):
		return self.score;
	def getDict(self,):
		syntax=u','.join(['O'+repr(self.getOrder()),self.getSyntax(), 'SP'+repr(self.semPrevious), 'SN'+repr(self.semNext)	, 'P'+repr(self.previous)	, 'N'+repr(self.next)])
		retDict=self.__dict__
		retDict['syntax']=syntax;
		return retDict;
	def __repr__(self):
		text=u"'%s':%s,\n "%(self.__dict__['order'],self.__dict__['vocalized']);
		for k in self.__dict__.keys():
			text += u"\t'%s':\t%s,\n "%(k,self.__dict__[k]);
		return text.encode('utf8'); 
		#return repr(self.__dict__);
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
	rdict=stemmedword.stemmedWord(rdict);
	stmwrd=stemmedSynWord(rdict);	
	print stmwrd.getDict();
	print stmwrd.is3rdperson();
	print stmwrd.isAdded();
	print stmwrd.isDefined();
	print stmwrd.isDirectJar();
	print stmwrd.isDirectJazem();
	print stmwrd.isDirectNaseb();
	print stmwrd.isDirectNominalFactor();
	print stmwrd.isDirectRafe3();
	print stmwrd.isDirectVerbalFactor();
	print stmwrd.isDirectVerbNaseb();
	print stmwrd.isDirectVerbRafe3();
	print stmwrd.isInitial();
	print stmwrd.isMajrour();
	print stmwrd.isMajzoum();
	print stmwrd.isMansoub();
	print stmwrd.isMarfou3();
	print stmwrd.isNoun();
	print stmwrd.isPassive();
	print stmwrd.isPast();
	print stmwrd.isPounct();
	print stmwrd.isPresent();
	print stmwrd.isTanwin();
	print stmwrd.isTransparent();
	print stmwrd.isVerb()	;
	print stmwrd;
