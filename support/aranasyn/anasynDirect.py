#!/usr/bin/python
# -*- coding = utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        syn_const
# Purpose:     Arabic syntaxic analyser.
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------

import syn_const
import stemmedword
import stemmedsynword
import pyarabic.araby as araby
debug = False;
class SyntaxAnalyzer:
	"""
        Arabic Syntax analyzer
	"""
	def __init__(self):
		pass;
	def analyze(self, detailed_stemming_dict):
		"""
		Syntaxic analysis of stemming results.
		morphological Result is a list of list of dict.
		The list contains all possible morphological analysis as a dict
		[
		[
		 {
			"word": "الحياة",		# input word
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
			"original": "حَيَاةٌ"		#original word from lexical dictionary
			"syntax":""				# used for syntaxique analysis porpos
			},
		 {"vocalized": "الْحَيَاةِ", "suffix": "ِ", "tags": "تعريف::مجرور", "stem": "حياة", "prefix": "", "freq": 0, "encletic": "", "word": "الحياة", "procletic": "ال", "root": "", "template": "", "type": "Noun:مصدر", "original": "حَيَاةٌ", "syntax":""}, 
		 {"vocalized": "الْحَيَاةَ", "suffix": "َ", "tags": "تعريف::منصوب", "stem": "حياة", "prefix": "", "freq": 0, "encletic": "", "word": "الحياة", "procletic": "ال", "root": "", "template": "", "type": "Noun:مصدر", "original": "حَيَاةٌ", "syntax":""}
		],
		[ 
		 {"vocalized": "جَمِيلَةُ", "suffix": "َةُ", "tags": "::مؤنث:مرفوع:ممنوع من الصرف", "stem": "جميل", "prefix": "", "freq": 63140, "encletic": "", "word": "جميلة", "procletic": "", "root": "", "template": "", "type": "Noun:صيغة مبالغة", "original": "جَمِيلٌ", "syntax":""}, 
		 {"vocalized": "جَمِيلَةِ", "suffix": "َةِ", "tags": "::مؤنث:مجرور:ممنوع من الصرف", "stem": "جميل", "prefix": "", "freq": 63140, "encletic": "", "word": "جميلة", "procletic": "", "root": "", "template": "", "type": "Noun:صيغة مبالغة", "original": "جَمِيلٌ"}, {"vocalized": "جَمِيلَةَ", "suffix": "َةَ", "tags": "::مؤنث:منصوب:ممنوع من الصرف", "stem": "جميل", "prefix": "", "freq": 63140, "encletic": "", "word": "جميلة", "procletic": "", "root": "", "template": "", "type": "Noun:صيغة مبالغة", "original": "جَمِيلٌ", "syntax":""}
		]
		 
		],
		 The syntaxic result have the same structure, but we add a field named 'syntax' to every word steming dictioionary
		@param detailed_stemming_dict: detailed stemming dict.
		@type detailed_stemming_dict:list of list of dict;
		@return: detailed syntaxic result with syntaxic tags.
		@rtype: list of list of dict;
		"""
		return self.context_analyze(detailed_stemming_dict);

	def context_analyze(self,detailed_stemming_dict):
		"""
		Syntaxic analysis of stemming results.
		@param detailed_stemming_dict: detailed stemming dict.
		@type detailed_stemming_dict:list of dict of dict;
		@return: detailed syntaxic result with syntaxic tags.
		@rtype: list of dict of dict;
		"""
		# ignore if the current word is transparent
		ignore = False;
		counter = 0;
		# create stemmed word instances
		stemmedSynWordListList = [];
		# convert objects from stemmedWord to stemmedSynWord in order to add syntaxic proprities
		for stemmingList in detailed_stemming_dict:
			tmpList = [];
			order=0;
			for order in range(len(stemmingList)):
				tmpList.append( stemmedsynword.stemmedSynWord(stemmingList[order], order) );
			stemmedSynWordListList.append(tmpList);
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
							
					if debug: print "stmword.getSyntax",stmword.getSyntax()
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
		return stemmedSynWordListList;

	def bigramAnalyze(self,previous, current, previousPosition=0, currentPosition=0):
		"""
		Syntaxic analysis of stemming results, two words.
		the positions are use to join related cases.
		@param previous	: the first item in bigram.
		@type previous	: stemmedSynWord
		@param current	: the second item in bigram.
		@type current	: stemmedSynWord
		@param previous	: the first item position in the word case list.
		@type previous	: stemmedSynWord
		@param current	: the second item position in the word case list.
		@type current	: stemmedSynWord		
		@return: the updated previous and current stemmedSynWord.
		@rtype: (previous, current);
		"""
		# Todo treat the actual word according to the previous word
		
		# treat the initial case when previous =None
		if debug: print current.isBreak(), 		current.isPounct()
		# to save the forced case to link previous and current word.
		# the word can be forced before this treatement, 
		# the this variable is used to indicate if the word is forced during the actual process.
		forcedCase = False
		if not previous or previous.isInitial():
			if current.isMarfou3() or current.isPast() or current.isStopWord():
			 # if  current.isMajrour():
				current.forcedCase();
				# add to the current word case a pointer to the previous word order.							
				#p for previous
				# if the previous is None, that means that the previous is initiatl state
				# the current word is prefered, we add previous pointer to 0 position.
				current.addPrevious(0);
			
			return (previous, current);
			
		if not current:
			# if the current word is end of clause or end of line, (None)
			# and the previous is not followed by a word, 
			# the previous will have a next relation. 
			# إذا كانت الكلم الأولى بعدها لا كلمة، أي نهاية العبارة، نضع لها راطة لاحقة إلى لاشيء
			# تستعمل هذه في ضبط أواخر الجمل
			# مثلا
			# جاء ولد
			# تحولّ إلى ثنائيات
			# [None. جاء]، [جاء، ولد]، [ولد، None]

			if debug:print current.isBreak(), current.isPounct() 
			# if the pounct is a break, the tanwin is prefered
			# the previous will have twnin
	
			if current.isBreak() and previous.isTanwin():
				if debug: print current.isBreak(), "case 51"
				previous.forcedCase();
				forcedCase = True;
			# add a relation to previous
			previous.addNext(0);
			return (previous, current);				
		elif current.isPounct():
			#if the word is pounctuation and it's transparent, the effect of previous factor will be kept
			#then we ignore this word in the next step, 
			#the variable 'previous' will not take the actual word.
			if debug:print current.isBreak(), current.isPounct() 
			# if the pounct is a break, the tanwin is prefered
			# the previous will have twnin
	
			if current.isBreak() and previous.isTanwin():
				if debug: print current.isBreak(), "case 51"
				previous.forcedCase();
				forcedCase = True;				
		#the stop word is factors, others no, if the previous is not stop word return.
		if previous.isStopWord():
			if current.isStopWord():
				current.forcedCase();
				forcedCase = True;			
			if current.isNoun():# and previous.isDirectNominalFactor():
				if debug: print 'is noun';
				if not current.hasProcletic() or current.getProcletic()==u'ال':
	
					if (previous.isDirectJar() or previous.isDirectAddition()) and  current.isMajrour():
					 # if  current.isMajrour():						
						current.forcedCase();
						previous.addSyntax(u'جار');
						forcedCase = True;				
						if debug: print 'add syntax *';							
					elif previous.isDirectNaseb() and  current.isMansoub():
						current.forcedCase();
						forcedCase = True;				
						if debug: print 'add syntax *';									
					elif previous.isInitial() and  current.isMarfou3():
						current.forcedCase();	
						forcedCase = True;				
						if debug: print 'add syntax *';									
					elif previous.isDirectRafe3() and current.isMarfou3():
						if debug: print 'add syntax *';								
						current.forcedCase();
						forcedCase = True;
			#verb
			elif current.isVerb() and previous.isDirectVerbalFactor():
				if  not current.hasProcletic() or current.getProcletic()==u'ال':
					if previous.isDirectJazem()  and  current.isMajzoum():
						current.forcedCase();
						forcedCase = True;					
					elif previous.isDirectVerbNaseb() and  current.isMansoub():
						current.forcedCase();
						forcedCase = True;					
					elif previous.isDirectVerbRafe3() and current.isMarfou3():
						current.forcedCase();
						forcedCase = True;					
		else: # previous is not a stopword
			if current.isVerb():
				# الجارية فعل والسابق مبتدأ
				# 
				if previous.isNoun():
					if current.isMarfou3():
					# Todo treat the actual word
						current.forcedCase();
						forcedCase = True;
			elif current.isNoun():
				# المضاف والمضاف إليه
				# إضافة لفظية
				# مثل لاعبو الفريق			
				if current.isMajrour() and (current.getProcletic() == u"ال"  or not current.hasProcletic()):
					if previous.isAdded():
					# Todo treat the actual word
						#previous.forcedCase();
						current.forcedCase();
						forcedCase = True;
					elif previous.isNoun() and not previous.isDefined() and  not previous.isAdded() and not previous.isTanwin() :
						# Todo treat the actual word
						#previous.forcedCase();						
						current.forcedCase();
						forcedCase = True;
				# منعوت والنعت
				#  تحتاج إلى إعادة نظر
				# بالاعتماد على خصائص الاسم الممكن أن يكون صفة
				if previous.isNoun() :#and previous.isDefined():
					# Todo treat the actual word
					if self.areCompatible(previous, current):
							current.forcedCase();
							forcedCase = True;
					
					# if current.isAdj() and current.getProcletic() == u"ال" :# or current.getProcletic() == u"وال"):
						# if (current.isMajrour() and previous.isMajrour()) or (current.isMansoub() and previous.isMansoub()) or (current.isMarfou3()and previous.isMarfou3()):
							# current.forcedCase();						
							# #previous.forcedCase();
							# forcedCase = True;
				# to do حالة التعت والمنعوت النكرة
				if previous.isNoun() :#and previous.isDefined():
					# Todo treat the actual word
					if self.areCompatible(previous, current):
							current.forcedCase();
							forcedCase = True;
				if previous.isVerb():
					if previous.is3rdperson():
						# Todo treat the actual word
						# الفعل والفاعل أو نائبه
						if (not current.hasProcletic() or current.getProcletic() == u"ال"):
							if current.isMarfou3():
								current.forcedCase();
								forcedCase = True;
					# الفعل والمفعول به
					if (not current.hasProcletic() or current.getProcletic() == u"ال"):
						if current.isMansoub():
							current.forcedCase();
							forcedCase = True;
		if forcedCase :
			# add to the previous a pointer to the next word order.
			# N for next
			previous.addNext(currentPosition);
			# add to the current word case a pointer to the previous word order.							
			#p for previous
			current.addPrevious(previousPosition);
		return previous,current;

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
		if ( previous and  current ) and previous.getOrder() in current.getPrevious() and current.getOrder() in previous.getNext():
			return True;
		else: False;
	# # deprecated
	# def isRelated(self,preStemDict, word_result):
		# """
		# study the relation between the actual word is related to the previous.
		# @param preStemDict: The steming dict of the previous word.
		# @type preStemDict: ;
		# @param word_result: The steming dict of the previous word.
		# @type word_result: list of stemmedSynWord class;
		# @return: the word result dictionary with related tags.
		# @rtype: list of dict;
		# """		
	# # المضاف والمضاف إليه
		# # إضافة لفظية
		# # مثل لاعبو الفريق
		# if preStemDict and  preStemDict.isAdded():
			# for stemDict in word_result:
				# # Todo treat the actual word
				# if stemDict.isNoun() and stemDict.isMajrour() and (stemDict.getProcletic() == u"ال" or not stemDict.hasProcletic()):
						# stemDict.forcedCase();
		# elif preStemDict and preStemDict.isNoun() and not preStemDict.isDefined() and  not preStemDict.isAdded() and not preStemDict.isTanwin() :
			# for stemDict in word_result:
				# # Todo treat the actual word
				# if stemDict.isNoun() and stemDict.isMajrour() and (stemDict.getProcletic() == u"ال"  or not stemDict.hasProcletic()):
						# stemDict.forcedCase();
	# # منعوت والنعت
	 # # تحتاج إلى إعادة نظر
	# # بالاعتماد على خصائص الاسم الممكن أن يكون صفة
		# if preStemDict and preStemDict.isNoun() and preStemDict.isDefined():
			# for stemDict in word_result:
				# # Todo treat the actual word
				# if stemDict.isAdj() and (stemDict.getProcletic() == u"ال" or stemDict.getProcletic() == u"وال"):
					# if stemDict.isMajrour() and preStemDict.isMajrour():
						# stemDict.forcedCase();						
					# if stemDict.isMansoub() and preStemDict.isMansoub():
						# stemDict.forcedCase();				
					# if stemDict.isMarfou3()and preStemDict.isMarfou3():
						# stemDict.forcedCase();
	# # الفعل والفاعل أو نائبه
		# if preStemDict and preStemDict.isVerb() and preStemDict.is3rdperson():
			# for stemDict in word_result:
				# # Todo treat the actual word
				# if stemDict.isNoun() and (stemDict.getProcletic() == u"ال" or not stemDict.hasProcletic()):
					# if stemDict.isMarfou3():
						# stemDict.forcedCase();
	
		# return word_result;
	def areCompatible(self, previous, current):
		"""
		verify the gramatica relation between the two words.
		دراسة الترابط النخوي بين الكلمتين، اي توافقهما في الجمع والنوع، والحركة
		If the current word is related with the previous word, return True.
		The previous word can contain a pointer to the next word. the current can have a pointer to the previous if they ara realated
		@param previous: the previous stemmed word, choosen by the tashkeel process.
		@type previous:stemmedSynWord class ;
		@param current: the current stemmed word.
		@type current:stemmedSynWord class ;
		@return: return if the two words are related syntaxicly.
		@rtype: boolean;
		"""
		#الكلمتان اسمان
		if not (previous.isNoun() and current.isNoun()):
			return False;
		compatible = False;
		# التعريف
		# إمّا معرفان معا، أو نكرتان معا
		if (current.isDefined() and previous.isDefined()) or (not current.isDefined() and not previous.isDefined()):
			compatible = True;
		else:
			return False;
		# الحركة
		# تساوي الحالة الإعرابية
		if (current.isMajrour() and previous.isMajrour()) or (current.isMansoub() and previous.isMansoub()) or (current.isMarfou3()and previous.isMarfou3()):
			compatible = True;
		else: 
			return False;
		# الكلمة الثانية  غير مسبوقة بسابقة غير التعريف
		# هذا التحقق جاء بعد التحقق من التعريف أو التنكير
		if not current.hasProcletic() or current.getProcletic() in (u"ال", u"فال" , u"وال",u"و",u"ف"):
			compatible = True;
		else:
			return False;
		# التنوين
		if (current.isTanwin() and previous.isTanwin()) or (not current.isTanwin() and not previous.isTanwin()):
			compatible = True;
		else:
			return False;
		# والتثنية والإفراد الجمع
		# التذكير والتأنيث
		if (current.isFeminin() and previous.isFeminin()) or (current.isMasculin() and previous.isMasculin()):
			compatible = True;
		else: return False;
		return compatible;
 
	def exclode_cases(self, word_result):
		"""
		exclode imcompatible cases
		@param word_result: The steming dict of the previous word.
		@type word_result: list of dict;
		@return: the filtred word result dictionary with related tags.
		@rtype: list of dict;
		"""		
	# حالة تحديد نمط الكلمة من السياق
		new_word_result = [];
		for stemming_dict in word_result:
			if "#" in stemming_dict.getSyntax():
				new_word_result.append(stemming_dict);
		if len(new_word_result)>0:
			return new_word_result;
		else:
			return word_result;
		return word_result;
		
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
	# print "test";
	# sa = SyntaxAnalyzer();
	# result1 = [
		# [
		 # {
			# "word": u"الحياة",		# input word
			# "vocalized": u"الْحَيَاةُ",   # vocalized form of the input word 
			# "procletic": u"ال",		# the syntaxic pprefix called procletic
			# "prefix": u"",			# the conjugation or inflection prefix
			# "stem": u"حياة",			# the word stem
			# "suffix": u"ُ", 			# the conjugation suffix of the word
			# "encletic": u"",			# the syntaxic suffix
			
			# "tags": u"تعريف::مرفوع*", # tags of affixes and tags extracted form lexical dictionary
			# "freq": 0,				# the word frequency from Word Frequency database 
			# "root": u"",				# the word root; not yet used
			# "template": u"",			# the template وزن 
			# "type": u"Noun:مصدر",	# the word type
			# "original": u"حَيَاةٌ",		#original word from lexical dictionary
			# "syntax":""				# used for syntaxique analysis porpos
			# },
		 # {"vocalized": u"الْحَيَاةِ", u"suffix": u"ِ", u"tags": u"تعريف::مجرور", u"stem": u"حياة", u"prefix": u"", u"freq": 0, u"encletic": u"", u"word": u"الحياة", u"procletic": u"ال", u"root": u"", u"template": u"", u"type": u"Noun:مصدر", u"original": u"حَيَاةٌ", u"syntax":""}, 
		 # {"vocalized": u"الْحَيَاةَ", u"suffix": u"َ", u"tags": u"تعريف::منصوب", u"stem": u"حياة", u"prefix": u"", u"freq": 0, u"encletic": u"", u"word": u"الحياة", u"procletic": u"ال", u"root": u"", u"template": u"", u"type": u"Noun:مصدر", u"original": u"حَيَاةٌ", u"syntax":""}
		# ],
		# [ 
		 # {"vocalized": u"جَمِيلَةُ", u"suffix": u"َةُ", u"tags": u"::مؤنث:مرفوع:ممنوع من الصرف", u"stem": u"جميل", u"prefix": u"", u"freq": 63140, u"encletic": u"", u"word": u"جميلة", u"procletic": u"", u"root": u"", u"template": u"", u"type": u"Noun:صيغة مبالغة", u"original": u"جَمِيلٌ", u"syntax":""}, 
		 # {"vocalized": u"جَمِيلَةِ", u"suffix": u"َةِ", u"tags": u"::مؤنث:مجرور:ممنوع من الصرف", u"stem": u"جميل", u"prefix": u"", u"freq": 63140, u"encletic": u"", u"word": u"جميلة", u"procletic": u"", u"root": u"", u"template": u"", u"type": u"Noun:صيغة مبالغة", u"original": u"جَمِيلٌ"}, {"vocalized": u"جَمِيلَةَ", u"suffix": u"َةَ", u"tags": u"::مؤنث:منصوب:ممنوع من الصرف", u"stem": u"جميل", u"prefix": u"", u"freq": 63140, u"encletic": u"", u"word": u"جميلة", u"procletic": u"", u"root": u"", u"template": u"", u"type": u"Noun:صيغة مبالغة", u"original": u"جَمِيلٌ", u"syntax":""}
		# ],
		 
		# ];
	# synresult = sa.analyze(result1);
	# for synlist in synresult:	
		# for item in synlist:
			# print item.getDict()
	# #test syn 
	text = u"أن السلام سيعتبر مفيدا أن يركبوا في السن"
	import qalsadi.analex 	
	result = [];
	analyzer = qalsadi.analex.analex()
	anasynt = SyntaxAnalyzer();
	result = analyzer.check_text(text);
	result = anasynt.analyze(result);
	# the result contains objets
	#print repr(result);
	TextToDisplay  =  anasynt.display(result);
	print TextToDisplay.encode('utf8');
