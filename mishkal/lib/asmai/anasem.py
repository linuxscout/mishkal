#!/usr/bin/python
# -*- coding = utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        anasem
# Purpose:     Arabic semantic analyzer Asmai
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     29-11-2012
# Copyright:   (c) Taha Zerrouki 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

import sys
sys.path.append('../');
sys.path.append('../lib');
import  sem_const
import  aranasyn.anasyn
import  qalsadi.stemmedword as stemmedword
import  aranasyn.stemmedsynword as stemmedsynword
debug = False;
#debug = True;
class SemanticAnalyzer:
	"""
        Arabic Semantic analyzer
	"""

	def __init__(self):
		pass;
	def analyze(self, detailed_stemming_dict):
		"""
		Semantic analysis of stemming and syntaxic results.

		morphological and analysis Result is a list of list of StemmedSynWord class.
		The semantic result have the same structure, but we add a field named 'semantic' to every word steming dictioionary
		@param detailed_stemming_dict: detailed stemming stemmedsynword.
		@type detailed_stemming_dict:list of list of stemmedsynword;
		@return: detailed semantic result with semantic tags.
		@rtype: list of list of stemmedsynword;
		"""
		return self.context_analyze(detailed_stemming_dict);


	def calculateScores(self, stemmedSynWordListList):
		"""
		Calculate scores for every case, in order to allow the scoring tashkeel choose.
		@param stemmedSynWordListList: detailed stemming, syntaxic and semantic details.
		@type stemmedSynWordListList: list of list of stemmedsynword class;
		@return: detailed semantic result with semantic tags.
		@rtype: list of list of stemmedsynword class;
		"""	
		initialScore =100;
		finalScore   =100;
		#initial = aranasyn.anasyn .stemmedsynword.stemmedSynWord();
		#initial.setScore(initialScore);
		counter = 0;
		previousIndex=0;
		# study the relations between words stemmings
		# first level
		for currentIndex in range(len(stemmedSynWordListList)):
			#index used to handle stmd position
			currentCasePosition=0;
			#second level
			for current in stemmedSynWordListList[currentIndex]:
				# initialize the current score to 0;
				current.score=0;
				if  currentIndex==0:  # the initial case
					""" the initial case"""
					counter+= 1;
					if 0 in current.previous:
						current.previous[0]= initialScore;
						current.score=initialScore;
				else:
					previousCasePosition =0 ; 
					for previous in stemmedSynWordListList[previousIndex]:
						counter+= 1;
						current.recalculateScore(previousCasePosition, previous.getScore());
							# current.previous[previousCasePosition]=previous.getScore();
							# current.setScore(max(current.getScore(),previous.getScore()+10));
						#previous, current  =  self.bigramAnalyze(previous, current, previousCasePosition, currentCasePosition);
						previousCasePosition +=1 ; 
				current.addSyntax(u'Scr:%d'%current.getScore());
				currentCasePosition +=1;
		return stemmedSynWordListList


	def context_analyze(self, stemmedSynWordListList):
		"""
		Semantic analysis of stemming results.
		@param stemmedSynWordListList: detailed stemming and syntaxic details.
		@type stemmedSynWordListList: list of list of stemmedsynword class;
		@return: detailed semantic result with semantic tags.
		@rtype: list of list of stemmedsynword class;
		"""
		# ignore if the current word is transparent
		ignore = False;
		counter = 0;

		previousIndex=0;	
		# study the relations between words stemmings
		for currentIndex in  range(len(stemmedSynWordListList)):
			#index used to handle stmd position
			stmwordCasePosition=0;
			for stmword in stemmedSynWordListList[currentIndex]:
				if  currentIndex==0:  # the initial case
					""" the initial case"""
					counter+= 1;
					stmword  =  self.bigramAnalyze(None, stmword)[1];
					
				else:
					previousCasePosition =0 ; 
					for previous in stemmedSynWordListList[previousIndex]:
						counter+= 1;
						previous, stmword  =  self.bigramAnalyze(previous, stmword, previousCasePosition, stmwordCasePosition);
						previousCasePosition +=1 ; 
							
					if debug: print u"stmword.getSyntax",stmword.getSyntax()
				# if the current word is transparent, ignore it and fix the previous index to the previous word.
				if stmword.isTransparent():
					ignore=True;
				else: ignore=False;
				stmwordCasePosition +=1;
			# if the current word ha sall its cases as transparent
			# الكلمة الشفافة مثل اسم الإشارة تنقل تأثير الكلمة السابقة لها للكلمة اللاحقة لها# م
			# مثل رأيت هذا الرجل
			# if not the word is not transprent, change the previous index.
			# else: change the ignore state and save the previous index as it.
			if not ignore:
				previousIndex = currentIndex;
			else:
				# previous index is mantained.
				ignore=False;

			# previousIndex = currentIndex;

			if debug:print previousIndex , currentIndex;
		if debug: print " counter total of items analyzed", counter;
		#
		# for stList in stemmedSynWordListList:
			# for st in stList:
				# st.calculateScore();
		#stemmedSynWordListList = self.calculateScores(stemmedSynWordListList);				
		return stemmedSynWordListList;

		


	def bigramAnalyze(self,previous, current, previousPosition=0, currentPosition=0):
		"""
		Syntaxic analysis of stemming results, two words.
		the positions are use to join related cases.
		@param previous	: the first item in bigram.
		@type previous	: stemmedSynWord
		@param current	: the second item in bigram.
		@type current	: stemmedSynWord
		@param previousPosition	: the first item position in the word case list.
		@type previousPosition	: integer
		@param currentPosition	: the second item position in the word case list.
		@type currentPosition	: integer
		@return: the updated previous and current stemmedSynWord.
		@rtype: (previous, current);
		"""
		# if the two words are related syntaxicly
		relation=""
		confirmed=''
		if self.isSynRelated(previous,current):
			# if the first word is a verb and the second is a noun,
			# the noun can be Suject of object or vice-object
			#إذا توالى فعل واسم، فيكون الاسم
			# إما فاعلا أو مفعولا أونائب فاعل
			#يكونفاعلا إذا كانت العلاقة فاعلية بين الفعل والاسم
			# ويكون مفعولا به أو نائب فعل إذا كانت العلاة مفعولية بين الفعل والاسم
			# تخزن المعلومات على شكل مصدر الفعل مضافا إلى الاسم
			# وجود الإضافة بين المصدر والاسم يدل على وجود علاقة الفاعلية أو المفعولية
			if previous.isVerb() and current.isNoun():
				confirmed="";
				relation =self.areSemRelated(previous, current);
				if relation:
					if relation==sem_const.Predicate :
						#نائب فاعل
						if previous.isPassive() and current.isMarfou3():
							confirmed="ok1"
						#مفعول به
						elif not previous.isPassive() and current.isMansoub():
							confirmed="ok2";
					elif relation==sem_const.Subject: 
						#فاعل
						if not previous.isPassive() and current.isMarfou3():
							confirmed="ok3"
					
					# print u'\t'.join([previous.getVocalized(), current.getVocalized(),  previous.getOriginal(),current.getOriginal(), relation, confirmed ]).encode('utf8');
			elif previous.isNoun() and current.isVerb():
				relation =self.areSemRelated(current, previous);
				confirmed="";
				if relation:
					if relation==sem_const.Predicate :
						#نائب فاعل
						if current.isPassive():
							confirmed="ok1"
						#مفعول به
						elif not current.isPassive():
							confirmed="ok2";
					elif relation==sem_const.Subject: 
						#فاعل
						if not current.isPassive():
							confirmed="ok3"
			elif previous.isNoun() and current.isNoun():
				relation =self.areSemRelated(current, previous);
				confirmed="";
				if relation:
					if relation==sem_const.Added :
						#مضاف إليه
						if current.isMajrour():
							confirmed="ok1"
					#Todo	#نعت
					elif relation == sem_const.Adj:
						if current.isAdj():
							confirmed='ok4' 
						#فاعل
				#		if not current.isPassive():
				#			confirmed="ok3"

				# if relation:
					# print u'\t'.join([previous.getVocalized(), current.getVocalized(),  previous.getOriginal(),current.getOriginal(), relation  ]).encode('utf8');
			
		# if previous and current:
			# print u'\t'.join([previous.getVocalized(), current.getVocalized(),  previous.getOriginal(),current.getOriginal(), unicode(relation), confirmed  ]).encode('utf8');				
		
		# # treat the initial case when previous =None
		# if debug: print current.isBreak(), 		current.isPounct()
		# # to save the forced case to link previous and current word.
		# # the word can be forced before this treatement, 
		# # the this variable is used to indicate if the word is forced during the actual process.
		# forcedCase = False
		# if not previous:
			# if current.isMarfou3():
			 # # if  current.isMajrour():
				# current.forcedCase();
			# return (previous, current);
			
		# if current.isPounct():
			# #if the word is pounctuation and it's transparent, the effect of previous factor will be kept
			# #then we ignore this word in the next step, 
			# #the variable 'previous' will not take the actual word.
			# if debug:print current.isBreak(), 		current.isPounct() 

			# # if the pounct is a break, the tanwin is prefered
			# # the previous will have twnin
	
			# if current.isBreak() and previous.isTanwin():
				# if debug: print current.isBreak(), "case 51"
				# previous.forcedCase();
				# forcedCase = True;					

		# #the stop word is factors, others no, if the previous is not stop word return.
		# if previous.isStopWord():
			# if current.isStopWord():
				# current.forcedCase();
				# forcedCase = True;			
			# if current.isNoun():
				# if debug: print 'is noun';
				# if previous.isDirectNominalFactor() and not current.hasProcletic():
					# current.forcedWordType()
					# forcedCase = True;				
					# if debug: print 'add syntax *';		
				
				# if previous.isDirectJar() and  current.isMajrour():
				 # # if  current.isMajrour():						
					# current.forcedCase();
					# previous.addSyntax(u'جار');
					# forcedCase = True;				
					# if debug: print 'add syntax *';							
				# elif previous.isDirectNaseb() and  current.isMansoub():
					# current.forcedCase();
					# forcedCase = True;				
					# if debug: print 'add syntax *';									
				# elif previous.isInitial() and  current.isMarfou3():
					# current.forcedCase();	
					# forcedCase = True;				
					# if debug: print 'add syntax *';									
				# elif previous.isDirectRafe3() and current.isMarfou3():
					# if debug: print 'add syntax *';								
					# current.forcedCase();
					# forcedCase = True;

			# #verb
			# elif current.isVerb():
				# if previous.isDirectVerbalFactor() and not current.hasProcletic():
					# current.forcedWordType()		
					# forcedCase = True;					
				# if previous.isDirectJazem()  and  current.isMajzoum():
					# current.forcedCase();
					# forcedCase = True;					
				# elif previous.isDirectVerbNaseb() and  current.isMansoub():
					# current.forcedCase();
					# forcedCase = True;					
				# elif previous.isDirectVerbRafe3() and current.isMarfou3():
					# current.forcedCase();
					# forcedCase = True;					
		# else: # previous is not a stopword

			# if current.isNoun():
				# # المضاف والمضاف إليه
				# # إضافة لفظية
				# # مثل لاعبو الفريق			
				# if current.isMajrour() and (current.getProcletic() == u"ال"  or not current.hasProcletic()):
					# if previous.isAdded():
					# # Todo treat the actual word
						# #previous.forcedCase();
						# current.forcedCase();
						# forcedCase = True;
					# elif previous.isNoun() and not previous.isDefined() and  not previous.isAdded() and not previous.isTanwin() :
						# # Todo treat the actual word
						# #previous.forcedCase();						
						# current.forcedCase();
						# forcedCase = True;

				# # منعوت والنعت
				# #  تحتاج إلى إعادة نظر
				# # بالاعتماد على خصائص الاسم الممكن أن يكون صفة
				# if previous.isNoun() :#and previous.isDefined():
					# # Todo treat the actual word
					# if self.areCompatible(previous, current):
							# current.forcedCase();						
							# forcedCase = True;						
					# # if current.isAdj() and current.getProcletic() == u"ال" :# or current.getProcletic() == u"وال"):
						# # if (current.isMajrour() and previous.isMajrour()) or (current.isMansoub() and previous.isMansoub()) or (current.isMarfou3()and previous.isMarfou3()):
							# # current.forcedCase();						
							# # #previous.forcedCase();
							# # forcedCase = True;
				# # to do حالة التعت والمنعوت النكرة
				# # الفعل والفاعل أو نائبه
				# if previous.isVerb() and previous.is3rdperson():
					# # Todo treat the actual word
					# if (not current.hasProcletic() or current.getProcletic() == u"ال"):
						# if current.isMarfou3():
							# current.forcedCase();
							# forcedCase = True;
						
		if relation and confirmed:
			#print u'\t'.join([previous.getVocalized(), current.getVocalized(),  previous.getOriginal(),current.getOriginal(), unicode(relation), confirmed  ]).encode('utf8');				
		
			# add to the previous a pointer to the next word order.
			# N for next
			#previous.addSyntax('@');
			#print '@';
			#current.addSyntax('@');			
			previous.addSemNext(currentPosition);
			# add to the current word case a pointer to the previous word order.							
			#p for previous
			current.addSemPrevious(previousPosition);
		return previous,current;

	def areSemRelated(self, previous, current):
		"""
		verify the semantic relation between the previous to current stemmed word.
		If the current word is related with the previous word, return True.
		The previous word can contain a pointer to the next word. the current can have a pointer to the previous if they ara realated
		@param previous: the previous stemmed word, choosen by the tashkeel process.
		@type previous:stemmedSynWord class ;
		@param current: the current stemmed word.
		@type current:stemmedSynWord class ;
		@return: return the relation between two words, else False
		@rtype: Unicode or False;
		"""
		preorigin = previous.getOriginal();
		if previous.isProperNoun():
			preorigin = u'فلان'
		curorigin = current.getOriginal();
		if current.isProperNoun():
			curorigin = u'فلان'
		key=u" ".join([preorigin, curorigin])
		relation = sem_const.SemanticTable.get(key,'');
		if debug: print u" ".join([key,unicode(relation)]).encode('utf8');
		
		if relation=='':
			return False;
		else: 
			return relation;

	def isSynRelated(self, previous, current):
		"""
		verify the syntaxic path from the previous to current stemmed word.
		If the current word is related with the previous word, return True.
		The previous word can contain a pointer to the next word. the current can have a pointer to the previous if they ara realated
		@param previous: the previous stemmed word, choosen by the tashkeel process.
		@type previous:stemmedSynWord class ;
		@param current: the current stemmed word.
		@type current:stemmedSynWord class ;
		@return: return if the two words are related syntaxicly.
		@rtype: boolean;
		"""
		if ( previous and  current ) and previous.getOrder() in current.getPrevious() and current.getOrder() in previous.getNext():
			return True;
		else: False;

	def isRelated(self, previous, current):
		"""
		verify the syntaxic path from the previous to current stemmed word.
		If the current word is related with the previous word, return True.
		The previous word can contain a pointer to the next word. the current can have a pointer to the previous if they ara realated
		@param previous: the previous stemmed word, choosen by the tashkeel process.
		@type previous:stemmedSynWord class ;
		@param current: the current stemmed word.
		@type current:stemmedSynWord class ;
		@return: return if the two words are related syntaxicly.
		@rtype: boolean;
		"""
		if ( previous and  current ) and previous.getOrder() in current.getSemPrevious() and current.getOrder() in previous.getSemNext():
			return True;
		else: False;		
		
	def decode(self, StemmedSynWordListList):
		"""
		Decode objects result from analysis. helps to display result.
		@param StemmedSynWordListList: list of  list of StemmedSynWord.
		@type word_result: list of  list of StemmedSynWord;
		@return: the list of list of dict to display.
		@rtype: list of  list of dict;
		"""	
		newResult = []
		for rlist in StemmedSynWordListList:
			tmplist = [];
			for item in rlist:
				tmplist.append(item.getDict());
			newResult.append(tmplist);	
		return  newResult;

	def display(self, StemmedSynWordListList):
		"""
		display objects result from analysis
		@param StemmedSynWordListList: list of  list of StemmedSynWord.
		@type word_result: list of  list of StemmedSynWord;
		"""	
		text = u"[";
		for rlist in StemmedSynWordListList:
			text+= u'\n\t[';
			for item in rlist:
				text+= u'\n\t\t{';
				stmword = item.getDict()
				for key in stmword.keys():
					text+= u"\n\t\tu'%s' = u'%s',"%(key, stmword[key]);
				text+= u'\n\t\t}';
			text+= u'\n\t]';
		text+= u'\n]';
		return text;

if __name__ == "__main__":
	text = u"يعبد الله منذ أن تطلع الشمس"

	import qalsadi.analex 	
	result = [];
	analyzer = qalsadi.analex.analex()
	anasynt = aranasyn.anasyn.SyntaxAnalyzer();
	anasem = SemanticAnalyzer();	
	result = analyzer.check_text(text);
	result = anasynt.analyze(result);
	# semantic result
	result = anasem.analyze(result);	
	# the result contains objets
	#print repr(result);
	TextToDisplay  =  anasynt.display(result);
	print TextToDisplay.encode('utf8');

