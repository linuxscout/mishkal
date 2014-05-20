#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        tashkeel
# Purpose:     Arabic automatic vocalization.
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
import sys
sys.path.append('../lib');
sys.path.append('../');
import re
import pyarabic.araby as araby
import tashkeel_const
import qalsadi.analex
import aranasyn.anasyn 
import asmai.anasem 
import collocations.collocations as collocations
import pyarabic.number
import pyarabic.named
# to debug program
debug= True;
class TashkeelClass:
	"""
        Arabic Tashkeel Class
	"""

	def __init__(self):
		# to display internal messages for debugging
		debug=False;
		# limit of words to vocalize, default value is 1000 words.
		self.limit=1000
		
		#  set the option value to enable the Last mark on voaclize words in output
		# default value is True, can be disabled for debuging porpus
		self.enabledLastMark= True;
		
		# set the option to do statistical vocalization based on collocations
		# default value is True, can be disabled for debuging porpus
		self.enabledStatTashkeel= True;	
			
		# set the option to show the collocations marks
		# default value is False, can be enabled for debuging porpus
		self.enabledShowCollocationMark= False;
		
		# set the option to use scoring teashkeel chosing.
		self.selectByScoreEnabled= False;
		# set the option to do syntaxic Analysis
		# default value is True, can be disabled for debuging porpus
		self.enabledSyntaxicAnalysis= True;

		# set the option to do allow ajusting voaclization result, for التقاء الساكنين
		# default value is True, can be disabled for debuging porpus
		self.enabledAjustVocalization=True;		

		# set the option to do Semantic Analysis
		# default value is True, can be disabled for debuging porpus		
		self.enabledSemanticAnalysis= True;

		# enable the last mark (Harakat Al-I3rab) 
		self.allowSyntaxLastMark = True; 

		# lexical analyzer
		self.analyzer=qalsadi.analex.analex();

		# syntaxic analyzer
		self.anasynt=aranasyn.anasyn.SyntaxAnalyzer();
		# semantic analyzer
		self.anasem=asmai.anasem.SemanticAnalyzer();		
		#set the lexical analzer debugging
		self.analyzer.set_debug(debug);
		#set the lexical analzer  word limit
		self.analyzer.set_limit(self.limit);
		#collocations dictionary for statistical tashkeel
		self.collo = collocations.CollocationClass(self.enabledShowCollocationMark);

	
	def set_limit(self, limit):
		"""
		set the limit length of words to vocalize
		"""
		self.limit=limit;
		#set the lexical analzer  wrd limit
		self.analyzer.set_limit(self.limit);

	def enableStatTashkeel(self):
		"""
		Enable the stat tasheel option.
		"""
		self.enabledStatTashkeel=True;
	def disableStatTashkeel(self):
		"""
		disable the stat tasheel option.
		"""
		self.enabledStatTashkeel= False;
	def getEnabledStatTashkeel(self):
		"""
		return the  the stat tasheel option value.
		@return: True if enabled, false else.
		@rtype: boolean.
		"""
		return self.enabledStatTashkeel;
	def enableShowCollocationMark(self):
		"""
		Enable the show the collocation mark option.
		"""
		self.enabledShowCollocationMark=True;
		self.collo.enableShowDelimiter();
	def disableShowCollocationMark(self):
		"""
		disable the show the collocation mark option.
		"""
		self.enabledShowCollocationMark = False;
		self.collo.disableShowDelimiter();
	def getEnabledShowCollocationMark(self):
		"""
		return the  the show the collocation mark option value.
		@return: True if enabled, false else.
		@rtype: boolean.
		"""
		return self.enabledShowCollocationMark;
	def enableLastMark(self):
		"""
		Enable the last mark option.
		"""
		self.enabledLastMark=True;
	def disableLastMark(self):
		"""
		disable the last mark vocalization  option.
		"""
		self.enabledLastMark=False;
	def getEnabledLastMark(self):
		"""
		return the  the last mark vocalization option value.
		@return: True if enabled, false else.
		@rtype: boolean.
		"""
		return self.enabledLastMark;
	def enableSyntaxicAnalysis(self):
		"""
		Enable the syntaxic analysis option.
		"""
		self.enabledSyntaxicAnalysis=True;
	def disableSyntaxicAnalysis(self):
		"""
		disable the syntaxic analysis option.
		"""
		self.enabledSyntaxicAnalysis=False;
	def getEnabledSyntaxicAnalysis(self):
		"""
		return the  the syntaxic analysis option value.
		@return: True if enabled, false else.
		@rtype: boolean.
		"""
		return self.enabledSyntaxicAnalysis;
	def enableSemanticAnalysis(self):
		"""
		Enable the Semantic analysis option.
		"""
		self.enabledSemanticAnalysis=True;
	def disableSemanticAnalysis(self):
		"""
		disable the Semantic analysis option.
		"""
		self.enabledSemanticAnalysis=False;
	def getEnabledSemanticAnalysis(self):
		"""
		return the  the Semantic analysis option value.
		@return: True if enabled, false else.
		@rtype: boolean.
		"""
		return self.enabledSemanticAnalysis;
		
	def enableAjustVocalization(self):
		"""
		Enable the Ajust Vocalization option.
		"""
		self.enabledAjustVocalization=True;
	def disableAjustVocalization(self):
		"""
		disable the Ajust Vocalization option.
		"""
		self.enabledAjustVocalization=False;
	def getEnabledAjustVocalization(self):
		"""
		return the  the Ajust Vocalization option value.
		@return: True if enabled, false else.
		@rtype: boolean.
		"""
		return self.enabledAjustVocalization;

	def fullStemmer(self, text):
		"""
		Do the lexical, syntaxic  and semantic analysis of the text.
		@param text: input text.
		@type text: unicode.
		@return: syntaxic and lexical tags.
		rtype: list of list of stemmedSynWord class.
		"""
		result=[];
		result=self.analyzer.check_text(text);
		if self.getEnabledSyntaxicAnalysis():
			result, synodelist = self.anasynt.analyze(result);
			# in this stpe we can't do semantic analysis without syntaxic analysis
			# we think it's can be done,
			# To do: do semantic analysis without syntaxic one
			if self.getEnabledSemanticAnalysis():
				result = self.anasem.analyze(result);	
		return result, synodelist;

	def tashkeel(self,inputtext,suggestion=False, format='text'):
		"""
		Vocalize the text and give suggestion to improve tashkeel by user.
		@param text: input text.
		@type text: unicode.
		@return: vocalized text.
		rtype: dict of dict or text.
		"""
		inputtext = self.preTashkeel(inputtext);
		# print "PreTashkeel", inputtext.encode('utf8');
		# The statistical tashkeel must return a text.
		#comment this after tests
		if self.getEnabledStatTashkeel():
			inputtext = self.statTashkeel(inputtext);
	
		#split texts into phrases to treat one phrase in time
		texts=self.analyzer.splitIntoPhrases(inputtext);
		# texts=[inputtext,]
		vocalized_text=u"";
		previous=None;
		outputSuggestList=[]
		ChosenList=[]	
		suggestsList=[]	
		for text in texts:
			
			#morpholigical analysis of text
			detailled_syntax, synodelist = self.fullStemmer(text);

			# calculate scores to enalbe chosing tashkeel by scoring
			# if self.enabledSyntaxicAnalysis and self.enabledSemanticAnalysis:
				# detailled_syntax = self.anasem.calculateScores(detailled_syntax);

			previous = None;
			nextNode = None;
			preNode  = None;
			for wordCasesList in detailled_syntax:

				#wordCasesList = self.anasynt.exclode_cases(wordCasesList)
				currentChosen = self.choose_tashkeel(wordCasesList,previous,preNode, nextNode);
				# ajust tanwin case
				# if previous and previous.canHaveTanwin() and not self.anasynt.isRelated(previous, currentChosen):
					# #vocalized_text+="1";
					# ChosenList[len(ChosenList)-1].ajustTanwin(); 
				# o ajust relation between words
				# if the actual word is transparent don't change the previous
				# add this to Sytaxic Analyser
				if not currentChosen.isTransparent():
					previous = currentChosen;
				ChosenList.append(currentChosen);

				# create a suggest list
				suggest=[];
				for item in wordCasesList:
					# ITEM IS A stemmedSynWord instance
					voc=item.getVocalized();
					suggest.append(voc);
					# if item.canHaveTanwin():
						# # يمكن لهذا أن يولد صيغا جديدة بها تنوي
						# # في بعض الحالات قد لا يكون شيئا جديدا 
						# # نقارنه مع الكلمة السابقة منوّنة ومن ثمّ نقرر إضافتها أولا
						# item.ajustTanwin();
						# vocTnwn = item.getVocalized()
						# if vocTnwn!=voc:
							# suggest.append(vocTnwn);
				suggest.sort();
				suggestsList.append(suggest);
		outputSuggestList=[]
		#create texts from chosen cases
		for i in range(len(ChosenList)):
			word = ChosenList[i].getVocalized();
			# omit the last haraka if the option LastMark is False
			if not self.getEnabledLastMark():
				word = araby.stripLastHaraka(word);
			vocalized_text=u" ".join([vocalized_text,self.display(word,format)]);
			outputSuggestList.append({'chosen':word,'suggest':u";".join(suggestsList[i])});
		
		# correct the resulted text to ajust some case of consonant neighbor
		#معالجة حالات التقاء الساكنين
		if self.getEnabledAjustVocalization():
			vocalized_text = self.ajustVocalizedResult(vocalized_text);
		if suggestion:
			outputSuggestList = self.ajustVocalizedSuggestionResult(outputSuggestList);
			return outputSuggestList;
		else:
			return vocalized_text;

	def choose_tashkeel(self, currentCasesList, previousChosenCase=None, preNode=None, nextNode=None):
		"""
		Choose a tashkeel for the current word, according to the previous one.
		@param : list of steming result of the word.
		@type currentCasesList: list of stemmedSynword;
		@param : the choosen previous word stemming.
		@type previousChosenCase:stemmedSynword;
		@return: the choosen stemming of the current word.
		@rtype:stemmedSynword.
		"""
		# toDo
		#currentCasesList = self.anasynt.isRelated(previousChosenCase,currentCasesList);

		# select the first chosen tashkeel
		# if len(currentCasesList)>0:
			# chosen= currentCasesList[0];
		chosen    = None;
		previous =previousChosenCase;
		# test selct by score
		if self.selectByScoreEnabled:
			chosen = self.selectByScore(currentCasesList, previous);
			if chosen: return chosen 
		chosen = False;
		# and lets other methode to choices by semantic and syntaxic
		if not previous or previous.isInitial():
			currentCasesList = self.filterForInitial(currentCasesList)

		# print "before Semantic", len(currentCasesList)
		if  self.getEnabledSyntaxicAnalysis() and self.getEnabledSemanticAnalysis():
			currentCasesList = self.filterBySemantic(currentCasesList, previous)

		# filter results accorind to  word frequency
		# print "After Semantic", len(currentCasesList)		
		if  self.getEnabledSyntaxicAnalysis():
			currentCasesList = self.filterBySyntaxic(currentCasesList, previous)
			# print "After Syntax", len(currentCasesList)
			currentCasesList = self.frequencyFilter(currentCasesList);
		# print "After Frequency", len(currentCasesList)
		#todo select the evident case if exists.
		forced=False;
		# How to choose a vocalized case
		# and lets other methode to choices by semantic and syntaxic
		# choose a case is a stop, word and has next relation					
		if   self.getEnabledSyntaxicAnalysis():
			if not chosen:
				for current in currentCasesList:
					if current.isStopWord() and current.hasNext():
						chosen=current;
						break; 

		# choose a case with two semantic  relation previous and next
		if   self.getEnabledSyntaxicAnalysis() and self.getEnabledSemanticAnalysis():
			for current in currentCasesList:
				if self.anasem.isRelated(previous, current) and current.hasSemNext():
					chosen=current
					break; 
			# choose a case with one semantic  relation previous, and the previous has a syntaxic relation
			if not chosen:
				for current in currentCasesList:
					if self.anasem.isRelated(previous, current) and previous.hasNext():
						chosen=current
						break; 
			# choose a case with one semantic  relation previous
			if not chosen:
				for current in currentCasesList:
					if self.anasem.isRelated(previous, current):
						chosen=current
						break; 
			# choose a case with one semantic  relation  next with a syntaxic relation between previous and current					
			if not chosen:
				for current in currentCasesList:
					if self.anasynt.isRelated(previous, current) and current.hasSemNext():
						chosen=current;
						break; 
			# choose a case with one semantic  relation  next					
			if not chosen:
				for current in currentCasesList:
					if  current.hasSemNext():
						# print "15", current.getVocalized().encode('utf8');
						chosen=current;
						break; 
		if  self.getEnabledSyntaxicAnalysis():
			# choose a case with two syntaxic  relation previous and next					
			if not chosen :
				for current in currentCasesList:
					if self.anasynt.isRelated(previous, current) and current.hasNext() and not current.isPassive():
						chosen=current;
						break;
				else:
					for current in currentCasesList:
						if self.anasynt.isRelated(previous, current) and current.hasNext():
							chosen=current;
							break;
					else:
					# choose a case with one syntaxic  relation previous 
					#select active voice
						for current in currentCasesList:
							if self.anasynt.isRelated(previous, current) and not current.isPassive():
								chosen=current;
								break;
						else:
			#select passive voice
							for current in currentCasesList:
								if self.anasynt.isRelated(previous, current) :
									chosen=current;
									break; 						
			# choose a case with one syntaxic  relation next										
			if not chosen:
				for current in currentCasesList:
					if current.hasNext():
						chosen=current;
						break; 
				else:
				#---------------------------
				#no relation no nexts
				#----------------------------
				# choose a case of stop word
					for current in currentCasesList:
						if current.isStopWord():
							# print "25"
							# # if previous: previous.vocalized+="*";
							chosen=current;
							break; 
					else:
				# choose a case with mansoub Noun
						for current in currentCasesList:
							if current.isNoun() and current.isMansoub():
								chosen=current;
								break; 
						else:
						# choose a case marfou3 verb
							for current in currentCasesList:
								if current.isVerb() and not current.isPassive() and current.isMarfou3():
									chosen=current;
									break; 
							else:
							# choose a case verb
								for current in currentCasesList:
									if current.isVerb() and not current.isPassive()and (current.isMarfou3() or current.isPast()):
										chosen=current;
										break; 
								else:
								# choose a case marfou3 verb if there are no active voice
									for current in currentCasesList:
										if current.isVerb():
											chosen=current;
											break;
		if not chosen and len(currentCasesList)>0:
			chosen= currentCasesList[0];		
		return chosen;
		
	def choose_tashkeel222222222222(self, currentCasesList, previousChosenCase=None, NextCasesList=None):
		"""
		Choose a tashkeel for the current word, according to the previous one.
		@param currentCasesList: list of steming result of the word.
		@type currentCasesList: list of stemmedSynword;
		@param : the chosen previous word stemming.
		@type previousChosenCase:stemmedSynword;
		@return: the chosen stemming of the current word.
		@rtype:stemmedSynword.
		"""

		# select the first chosen tashkeel
		if not currentCasesList:
			return None;
		lenCCS =len(currentCasesList); # Len CCS
		
		# if there are one case only
		if lenCCS==1:
			chosen= currentCasesList[0];
			return chosen;
		
		chosen    =None;
		previous =previousChosenCase;
		
		# test selct by score
		if self.selectByScoreEnabled:
			chosen = self.selectByScore(currentCasesList, previous);
			if chosen: return chosen 

		# and lets other methode to choices by semantic and syntaxic
		# if not previous or previous.isInitial():
			# currentCasesList = self.filterForInitial(currentCasesList)
		# print "before Semantic", len(currentCasesList)
		#currentCasesList = self.filterBySemantic(currentCasesList, previous)
		# filter results accorind to  word frequency
		# print "After Semantic", len(currentCasesList)		
		#currentCasesList = self.filterBySyntaxic(currentCasesList, previous)
		# print "After Syntax", len(currentCasesList)
		#currentCasesList = self.frequencyFilter(currentCasesList);
		# print "After Frequency", len(currentCasesList)


		#todo select the evident case if exists.
		forced  = False;


		# How to choose a vocalized case
		# and lets other methode to choices by semantic and syntaxic
		# choose a case is a stopword and has next relation
		if not chosen:
			for current in currentCasesList:
				if current.isStopWord() and current.hasNext():
					chosen=current;
					break; 

		if not chosen:
			chosenList=[];
			if not previous or previous.isInitial():
				condidateSemList= [] # semantic previous
				#condidateSynList= [] # syntaxic previous			
				condidateSynList=[i for i in range(lenCCS) if currentCasesList[i].hasPrevious()]
				print 'initial cases', len(condidateSynList)
			else: #if previous:
				condidateSemList= previous.getSemNext();  # semantic previous
				condidateSynList= previous.getNext();  # syntaxic previous			

			condidateSemSemList=[]; #semantic previous semantic Next
			condidateSemSynList=[]; #semantic previous syntaxic Next
			condidateSynSemList=[]; #syntaxic previous semantic Next 
			condidateSynSynList=[]; #syntaxic previous syntaxic Next 			
			condidateNextSemList=[]; # only semantic Next 
			condidateNextSynList=[]; # only syntaxic Next 

			# look up for semantic semantic and semantic syntaxic 
			for i in condidateSemList:
				# one relation with previous
				if i<len(currentCasesList) and currentCasesList[i].hasNext():
				#one relation with a next
					condidateSemSynList.append(i); # semantic previous syntaxic Next				
					if currentCasesList[i].hasSemNext():
					#one relation with a next
						condidateSemSemList.append(i); # semantic previous semantic Next

			#lookup for syntaxic syntaxic and syntaxic semantic

			if condidateSynList and max(condidateSynList)>lenCCS:
				print "Warrning,----------------------------"
				print 'Nexts',condidateSynList;
				print 'curre',
				print hash(previous),previous.getWord().encode('utf8'),currentCasesList[0].getWord().encode('utf8');
				for i in range(lenCCS):
					print i,':',currentCasesList[i].getOrder(),',',
				print ;

			for i in condidateSynList:
				#print condidateSynList, i, len(currentCasesList), #currentCasesList[i].getOrder();
				# one relation with previous
				if i<len(currentCasesList) and  currentCasesList[i].hasNext():
				#one relation with a next
					condidateSynSynList.append(i); # syntaxic previous syntaxic Next
					if currentCasesList[i].hasSemNext():
					#one relation with a next
						condidateSynSemList.append(i); # syntic previous semantic Next

			#look up for Cases with only next smeantic or only next syntaxic
			for i in range(lenCCS):
				# one relation with previous
				if currentCasesList[i].hasNext():
				#one relation with a next
					condidateNextSynList.append(i); # syntaxic Next				
					if currentCasesList[i].hasSemNext():
					#one relation with a next
						condidateNextSemList.append(i); # semantic Next

			# priority to choose a table of cases
			#
			# previous/next	semantic	syntaxic	Not
			# semantic		1			2			3
			# syntaxic		4			6			7
			# not			5			8			9
			#1
			if condidateSemSemList:
				chosenList= condidateSemSemList;
			#2
			elif condidateSemSynList:
				chosenList= condidateSemSynList;
			#3
			elif condidateSemList:
				chosenList= condidateSemList;
			#4
			elif condidateSynSemList:
				chosenList= condidateSynSemList;
			#5
			elif condidateNextSemList:
				chosenList= condidateNextSemList;
			#6
			elif condidateSynSynList:
				chosenList= condidateSynSynList;
			#7
			elif condidateSynList:
				chosenList= condidateSynList;
			#8
			elif condidateNextSynList:
				chosenList= condidateNextSynList;
			#9
			else:
				chosenList=[];
			# look for a best case in condidates
			if chosenList:
				#to do select
				# temporary
				if debug: 
					print "chosen", len(chosenList), round(float(len(chosenList))*100/len(currentCasesList)), len(currentCasesList)
					for i in chosenList:
						print '\t', currentCasesList[i].getVocalized().encode('utf8'), currentCasesList[i].getFreq(),currentCasesList[i].isForcedCase()
				if chosenList[0]<len(currentCasesList): #valid cases
					if len(chosenList)==1:
						chosen = currentCasesList[chosenList[0]]
					else:
					#temporary
					#To do: use another method to select case
					# 1- Select high frequency
						highScore =     currentCasesList[chosenList[0]].getFreq();
						highScoreIndex = chosenList[0]
						for i in chosenList:
							if currentCasesList[i].getFreq()>highScore:
								highScore      = currentCasesList[chosenList[0]].getFreq();
								highScoreIndex = chosenList[0]
						chosen = currentCasesList[highScoreIndex]
				else: #warning chosen tashkeel out of range
					print "warning: chosen tashkeel out of range";

		#---------------------------
		#no relation no nexts
		#----------------------------
		#choose a case of stop word
		# and lets other methode to choices by semantic and syntaxic
		if not previous or previous.isInitial():
			currentCasesList = self.filterForInitial(currentCasesList)
		# print "before Semantic", len(currentCasesList)
		currentCasesList = self.filterBySemantic(currentCasesList, previous)
		# filter results accorind to  word frequency
		# print "After Semantic", len(currentCasesList)		
		currentCasesList = self.filterBySyntaxic(currentCasesList, previous)
		# print "After Syntax", len(currentCasesList)
		currentCasesList = self.frequencyFilter(currentCasesList);
		# print "After Frequency", len(currentCasesList)
		if not chosen:
			for current in currentCasesList:
				if current.isStopWord():
					chosen=current;
					break; 
			else:
			# choose a case with marfou3 verb
				for current in currentCasesList:
					if current.isNoun() and current.isMansoub():
						chosen=current;
						break; 
				else:
					for current in currentCasesList:
						if current.isVerb():
							if current.isPresent()  and not current.isPassive() and not (current.isMansoub() or current.isMajzoum()) :
								chosen=current;
								break;
							elif current.isPast() and not current.isPassive():
								chosen=current;
								break;
		if not chosen and len(currentCasesList)>0:
			chosen= currentCasesList[0];
		return chosen;
	def selectByScore(self,word_analyze_list, previous):
		"""
		Choose the word according a score estimation
		@param word_analyze_list: list of steming result of the word.
		@type word_analyze_list: list of  stemmedSynWord;
		@param previous: previous word.
		@type previous: stemmedSynWord;		
		@return: filtred list of stemming result.
		@rtype: list of stemmedSynWord.
		"""	

		#choose by score
		chosen = False;
		highScore = 0;
		# if previous has next, we choose from nexts only,
		# else we choose the highscore from the current word case
		if previous and (previous.hasNext() or previous.hasSemNext()):
			for current in word_analyze_list:
				currentScore = current.getScore();
				# if the current is related to previous
				# if not self.anasem.isRelated(previous, current)  and not  self.anasynt.isRelated(previous, current):
					# currentScore = 0;
				if self.anasem.isRelated(previous, current)  or  self.anasynt.isRelated(previous, current) :
					if currentScore > highScore:
						highScore = currentScore;
						chosen = current;
		else:
			for current in word_analyze_list:
				currentScore = current.getScore();
				if  currentScore > highScore:
					highScore = currentScore;
					chosen = current;
			
		return chosen;

		


	def filterBySemantic(self, word_analyze_list, previous):
		"""
		filter results according to the word semantic relation
		@param word_analyze_list: list of steming result of the word.
		@type word_analyze_list: list of  stemmedSynWord;
		@param previous: previous word.
		@type previous: stemmedSynWord;		
		@return: filtred list of stemming result.
		@rtype: list of stemmedSynWord.
		"""	
		tempList=[]
		for current in word_analyze_list:
			if  self.anasem.isRelated(previous, current):
				tempList.append(current);
			elif current.hasSemNext() or current.isStopWord():
				tempList.append(current);
		if tempList: return tempList;
		else: return word_analyze_list;

	def filterForInitial(self, word_analyze_list):
		"""
		filter results according to the initial position in the sentence
		@param word_analyze_list: list of steming result of the word.
		@type word_analyze_list: list of  stemmedSynWord;
		@return: filtred list of stemming result.
		@rtype: list of stemmedSynWord.
		"""	
		tempList=[]
		for current in word_analyze_list:
			if  current.isStopWord():
				tempList.append(current);
			elif current.isMarfou3() and not current.isPassive(): # noun or verb
				tempList.append(current);
			elif current.isPast():
				tempList.append(current);	
		if tempList: return tempList;
		else: return word_analyze_list;		
	def filterBySyntaxic(self, word_analyze_list, previous):
		"""
		filter results according to the word syntaxic relation
		@param word_analyze_list: list of steming result of the word.
		@type word_analyze_list: list of  stemmedSynWord;
		@param previous: previous word.
		@type previous: stemmedSynWord;		
		@return: filtred list of stemming result.
		@rtype: list of stemmedSynWord.
		"""	
		tempList=[]
		for current in word_analyze_list:
			if  self.anasynt.isRelated( previous, current):
				tempList.append(current);
			if  current.isStopWord():
				tempList.append(current);
			elif current.hasNext():
				tempList.append(current);
		if tempList: return tempList;
		else: return word_analyze_list;

	def frequencyFilter(self, word_analyze_list):
		"""
		filter results according to the word frequency
		@param : list of steming result of the word.
		@type word_analyze_list: list of dict;
		@return: filtred list of stemming result.
		@rtype: list of stemmedSynWord.
		"""	
		if word_analyze_list:
			chosen= word_analyze_list[0];
		else: return None;
		# select according to  word frequency
		freq=0;
		chosenFreq=0;
		#first chose the frequncy
		for item_dict in word_analyze_list:
			freq=item_dict.getFreq();
			if freq>=chosenFreq:
				chosenFreq=freq;
				
		newList=[];
		#sort the stemmed words
		# endlist is used to add forced case in the end of the list
		endList=[];
		for item_dict in word_analyze_list:
			# select max frequency
			if item_dict.getFreq()==chosenFreq:
				newList.append(item_dict);
			# add the forced cases
			elif  self.getEnabledSyntaxicAnalysis() and item_dict.isForcedCase() or item_dict.isForcedWordType() or item_dict.isStopWord():
				endList.append(item_dict);
		newList+=endList;
		return newList;

	def tashkeelOuputHtmlSuggest(self,text):
		"""
		Vocalize the text and give suggestion to improve tashkeel by user.
		@param text: input text.
		@type text: unicode.
		@return: vocalized text.
		rtype: dict of dict.
		"""
		return self.tashkeel(text,suggestion=True, format="html");
		
		
	def tashkeelOutputText(self,text):
		"""
		Vocalize the text witthout suggestion
		@param text: input text.
		@type text: unicode.
		@return: vocalized text.
		rtype: text.
		"""
		return self.tashkeel(text,suggestion=False, format="text");

	def ajustVocalizedResult(self, text):
		"""
		Ajust the resulted text after vocalization to correct some case like 'meeting of two queiscents= ألتقاء الساكنين'
		@param text: vocalized text
		@type text: unicode
		@return: ajusted text.
		@rtype: unicode
		"""
		# min => mina
		text= re.sub(ur'\sمِنْ\s+ا', u' مِنَ ا', text);
		# man => mani
		text= re.sub(ur'\sمَنْ\s+ا', u' مَنِ ا', text);
		#An => ani
		text= re.sub(ur'\sعَنْ\s+ا', u' عَنِ ا', text);
		#sukun + alef => kasra +alef
		text= re.sub(ur'\s%s\s+ا'%araby.SUKUN, u' %s ا'%araby.SUKUN, text);		
		#ajust pounctuation
		text= re.sub(ur" ([.?!,:;)”—]($| ))", ur"\1", text);
		#binu => bin 
		# temporary, to be analysed by syntaxical analyzer
		text= re.sub(ur'\sبْنُ\s', u' بْن ', text);		
		# # # اختصارات مثل حدثنا إلى ثنا وه تكثر في كتب التراث
		# text= re.sub(ur'\seثِنَا\s', u' ثَنَا ', text);		
		return text;

	def ajustVocalizedSuggestionResult(self, SuggestList):
		"""
		Ajust the resulted text after vocalization to correct some case like 'meeting of two queiscents= ألتقاء الساكنين'
		@param text: SuggestList
		@type text: list of dict of unicode
		@return: SuggestList.
		@rtype: list of dict of unicode
		"""
		for i in range(len(SuggestList)-1):
			if SuggestList[i]['chosen'] in (u'مَنْ', u'مِنْ', u'عَنْ'):
				if i+1<len(SuggestList) and SuggestList[i+1].has_key('chosen') and SuggestList[i+1]['chosen'].startswith(araby.ALEF):
					if SuggestList[i]['chosen']==u'مِنْ':
						SuggestList[i]['chosen']=u'مِنَ'
					elif SuggestList[i]['chosen']==u'عَنْ':
						SuggestList[i]['chosen']=u'عَنِ'
					elif SuggestList[i]['chosen']==u'مَنْ':
						SuggestList[i]['chosen']=u'مَنِ'
			# if SuggestList[i]['chosen'] == u'بْنُ':
				# SuggestList[i]['chosen'] = u'بْن'
		return SuggestList;
		






	def display(self, word, format="text"):
		"""
		format the vocalized word to be displayed on web interface.
		@param word: input vocalized word.
		@type word: unicode.
		@return: html code.
		rtype: unicode.
		"""
		format=format.lower();
		if format=="html":
			return u"<span id='vocalized' class='vocalized'>%s</span>"%word;
		elif format=='text':
			return word;
		else:
			return word;

	def assistanttashkeel(self,text):
		"""
		Vocalize the text.
		@param text: input text.
		@type text: unicode.
		@return: vocalized text.
		rtype: unicode.
		"""	
		detailled_syntax=self.fullStemmer(text);
		vocalized_text=u"";
		previous=None;

		for word_analyze_list in detailled_syntax:
			#word_analyze_list=self.anasynt.exclode_cases(word_analyze_list)		
			#word_stemming_dict=self.choose_tashkeel(word_analyze_list,previous);
			# o ajust relation between words 
			#previous=word_stemming_dict;
			for item in word_analyze_list:
				voc=item.getVocalized();
				vocalized_text=u";".join([vocalized_text,voc]);
		return vocalized_text;


	def preTashkeel(self,text):
		"""
		Vocalize the text by evident cases and by detecting numbers clauses
		@param text: input text.
		@type text: unicode.
		@return: statisticlly vocalized text.
		rtype: unicode.
		"""
		# get the word list
		# اختصارات مثل حدثنا إلى ثنا وه تكثر في كتب التراث
		for abr in tashkeel_const.CorrectedTashkeel.keys():
			text = re.sub(ur"\s%s\s"%abr, ur" %s "%tashkeel_const.CorrectedTashkeel[abr], text);
		wordlist = self.analyzer.tokenize(text);
		prevocalizedList = pyarabic.number.preTashkeelNumber(wordlist);
		#Todo ajust prevocalization of named enteties
		prevocalizedList = pyarabic.named.preTashkeelNamed(prevocalizedList);		
		return u" ".join(prevocalizedList);




	def statTashkeel(self,text):
		"""
		Vocalize the text by statistical method according to the collocation dictionary
		@param text: input text.
		@type text: unicode.
		@return: statisticlly vocalized text.
		rtype: unicode.
		"""
		text = self.collo.lookupForLongCollocations(text);
		
		# get the word list
		wordlist=self.analyzer.tokenize(text);
		vocalized_text=u"";
		previous=u"";
		list_dict=[]; # returned resultat
		# temporarly used
		suggest=[];
		liste=wordlist;
		# use a list as a stack,
		# give two element from the end.
		# test the tow elements if they are collocated,
		# if collocated return the vocalized text
		# if else, delete the last element, and return the other to the list.
		newlist= self.collo.lookup(wordlist);
		#todo: return a text from the statistical tashkeel
		text=u" ".join(newlist);
		return text;
		# is done temporaly to test statistical tashkeel
		#for word in newlist:
		#	vocalized_text=u" ".join([vocalized_text,self.display(word)]);
		#	list_dict.append({'chosen':word,'suggest':u";".join(suggest)});
		#return list_dict;

if __name__=="__main__":
	print "test";		
	vocalizer=TashkeelClass();
	# text=u"""تجف أرض السلام بالسلام الكبير.	مشى على كتاب السلام.
	# جاء الولد السمين من قاعة القسم الممتلئ""";
	text=u"يعبد الله تطلع الشمس"
	voc = vocalizer.tashkeel(text);
	print voc.encode('utf8');
