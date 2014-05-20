#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        synNode
# Purpose:     representat data analyzed given by morphoanalyzer Qalsadi then by syntaxic analyzer
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     19-09-2012
# Copyright:   (c) Taha Zerrouki 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
if __name__ == "__main__":
	import sys
	sys.path.append('../lib')

import syn_const
import stemmedsynword
class synNode:
	"""
	synNode represents the regrouped data resulted from the morpholocigal analysis
	"""
	def __init__(self, caseList, order=-1):
		"""
		Create the synNode  from a list of StemmedSynword cases
		"""
		self.caseCount=len(caseList);
		""" the number of syntaxtical cases """

		self.verbCount=0;
		""" the number of syntaxtical verb cases """

		self.nounCount=0;
		""" the number of syntaxtical noun cases """

		self.stopwordCount=0;
		""" the number of syntaxtical stopword cases """
		
		self.word=''
		""" The unstemmed word """
		self.originals={}
		self.wordType={'verb':[], 
						'noun':[],
						'pounct':[],
						'stopword':[],
						}
		self.breaks=[];
		self.nonBreaks=[];
		self.syntaxMark={'mansoub':[],
						'marfou3':[], 
						'majrour':[],
						'majzoum':[],
						'tanwin_mansoub':[],
						'tanwin_marfou3':[], 
						'tanwin_majrour':[],						
					
						}
		""" The list of original words"""
		if caseList:
			self.word=caseList[0].getWord();
		for case in caseList:
			if self.originals.has_key(case.getOriginal()):
				self.originals[case.getOriginal()].append(case.getOrder());
			else:
				self.originals[case.getOriginal()]= [case.getOrder(),];
			#indexing by word type
			if case.isVerb():
				self.wordType['verb'].append(case.getOrder());
			elif case.isNoun():
				self.wordType['noun'].append(case.getOrder());
			elif case.isStopWord():
				self.wordType['stopword'].append(case.getOrder());
			elif case.isPounct():
				self.wordType['pounct'].append(case.getOrder());
			#indexing break and non break word cases
			if case.isBreak():
				self.breaks.append(case.getOrder());
			else:
				self.nonBreaks.append(case.getOrder());
			#indexing by syntax mark and tanwin
			if case.isTanwin():
				if case.isMansoub():
					self.syntaxMark['tanwin_mansoub'].append(case.getOrder());
				elif case.isMarfou3():
					self.syntaxMark['tanwin_marfou3'].append(case.getOrder());
				elif case.isMajrour():
					self.syntaxMark['tanwin_majrour'].append(case.getOrder());
			else:
				if case.isMansoub():
					self.syntaxMark['mansoub'].append(case.getOrder());
				elif case.isMarfou3():
					self.syntaxMark['marfou3'].append(case.getOrder());
				elif case.isMajrour():
					self.syntaxMark['majrour'].append(case.getOrder());
				elif case.isMajzoum():				
					self.syntaxMark['majzoum'].append(case.getOrder());				
			
				
				
		self.verbCount     = len(self.wordType['verb']);
		self.nounCount     = len(self.wordType['noun']);
		self.stopwordCount = len(self.wordType['stopword']);				
		self.pounctCount = len(self.wordType['pounct']);			
		
	######################################################################
	#{ Attributes Functions
	######################################################################		

	def setCaseCount(self, count):
		"""
		Set the case count.
		@param count: the number of stemmed word  cases
		@tyep count: integer;
		"""
		self.caseCount=count;
	def getCaseCount(self):
		"""
		get the case count.
		@return: the number of stemmed word  cases
		@tyep count: integer;
		"""
		return self.caseCount;
	def setVerbCount(self, count):
		"""
		Set the verb count.
		@param count: the number of stemmed word cases as  verbs
		@tyep count: integer;
		"""
		self.verbCount=count;
	def getVerbCount(self):
		"""
		get the verb count.
		@return: the number of stemmed word cases as verbs
		@tyep count: integer;
		"""
		return self.verbCount;
		
	def setNounCount(self, count):
		"""
		Set the noun count.
		@param count: the number of stemmed word cases as  nouns
		@tyep count: integer;
		"""
		self.nounCount=count;
	def getNounCount(self):
		"""
		get the noun count.
		@return: the number of stemmed word cases as nouns
		@tyep count: integer;
		"""
		return self.nounCount;
	def setStopwordCount(self, count):
		"""
		Set the stopword count.
		@param count: the number of stemmed word cases as  stopwords
		@tyep count: integer;
		"""
		self.stopwordCount=count;
	def getStopwordCount(self):
		"""
		get the stopword count.
		@return: the number of stemmed word cases as stopwords
		@tyep count: integer;
		"""
		return self.stopwordCount;
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
	def getOriginal(self,):
		"""
		Get the original forms of the input word
		@return: the given original.
		@rtype: unicode string
		"""
		return self.originals.keys();

	def setOriginal(self,neworiginal):
		"""
		Set the original words
		@param neworiginal: the new given original.
		@type neworiginal: unicode string list
		"""
		self.originals = neworiginal;

	######################################################################
	#{ Tags extraction Functions
	######################################################################		
	def hasVerb(self,):
		"""
		Return if all cases are verbs.
		@return:True if the node has verb in one case at least.
		@rtype:boolean
		"""
		return self.verbCount>0;
	def hasNoun(self,):
		"""
		Return if all cases are nouns.
		@return:True if the node has noun in one case at least.
		@rtype:boolean
		"""
		return self.nounCount>0;

	def hasStopword(self,):
		"""
		Return if all cases are stopwords.
		@return:True if the node has stopword in one case at least.
		@rtype:boolean
		"""
		return self.stopwordCount>0;
	def hasPounct(self,):
		"""
		Return if all cases are pounctuations
		@return:True if the node has pounctation in one case at least.
		@rtype:boolean
		"""
		return self.pounctCount>0;		
	def isVerb(self,):
		"""
		Return if all cases are verbs.
		@return:True if the node is verb in alll cases.
		@rtype:boolean
		"""
		return self.pounctCount==0 and self.stopwordCount==0 and self.verbCount and self.nounCount==0;
	def isNoun(self,):
		"""
		Return if all cases are nouns.
		@return:True if the node is noun in alll cases.
		@rtype:boolean
		"""
		return self.pounctCount==0 and self.stopwordCount==0 and self.verbCount==0 and self.nounCount;
		

	def isStopword(self,):
		"""
		Return if all cases are stopwords.
		@return:True if the node is stopword in alll cases.
		@rtype:boolean
		"""
		return self.pounctCount==0 and self.stopwordCount and self.verbCount==0 and self.nounCount==0;
	def isPounct(self,):
		"""
		Return if all cases are pounctuations
		@return:True if the node is pounctation in alll cases.
		@rtype:boolean
		"""
		return self.pounctCount and self.stopwordCount==0 and self.verbCount==0 and self.nounCount==0;
	def isMostVerb(self,):
		"""
		Return True if most  cases are verbs.
		@return:True if the node is verb in most cases.
		@rtype:boolean
		"""
		
		return self.verbCount> self.nounCount and self.verbCount> self.stopwordCount;
	def isMostNoun(self,):
		"""
		Return True if most  cases are nouns.
		@return:True if the node is noun in most cases.
		@rtype:boolean
		"""
		return self.nounCount >self.verbCount  and self.nounCount> self.stopwordCount;

	def isMostStopword(self,):
		"""
		Return True if most cases are stopwords.
		@return:True if the node is stopword in most cases.
		@rtype:boolean
		"""
		return self.stopwordCount > self.verbCount  and self.stopwordCount > self.nounCount;

	def getWordType(self,):
		"""
		Return the word type.
		@return:the word type or mosttype.
		@rtype:string
		"""
		if self.isNoun():
			return 'noun';
		elif self.isVerb():
			return 'verb';
		elif self.isStopword():
			return 'stopword';
		elif self.isPounct():
			return 'pounct';			
		elif self.isMostNoun():
			return 'mostnoun';
		elif self.isMostVerb():
			return 'mostverb';
		elif self.isMostStopword():
			return 'moststopword';
		else:
			return 'ambiguous'
	def getBreakType(self,):
		"""
		Return the word break type, if the word break the sentences or not.
		@return:the word type or mosttype.
		@rtype:string
		"""
		if len(self.breaks)>0 and len(self.nonBreaks) == 0 :
			return 'break';
		elif len(self.nonBreaks)>0 and len(self.breaks) == 0:
			return 'nonBreak';
		elif len(self.nonBreaks)> len(self.breaks) :
			return 'mostNonBreak';
		elif len(self.nonBreaks) < len(self.breaks) :
			return 'mostBreak';
		else:
			return 'ambiguous'
	def __repr__(self):
		text=u"\n'%s':%s, [%s-%s]{V:%d, N:%d, S:%d} "%(self.__dict__['word'],u', '.join(self.originals), self.getWordType(),self.getBreakType() , self.verbCount, self.nounCount, self.stopwordCount);
		text+=repr(self.syntaxMark)
		# for k in self.__dict__.keys():
			# text += u"\t'%s':\t%s,\n "%(k,self.__dict__[k]);
		return text.encode('utf8'); 

if __name__=="__main__":
	pass;
	print "Syn Node module"
