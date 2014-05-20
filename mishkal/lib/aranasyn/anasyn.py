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
if __name__ == "__main__":
	import sys
	sys.path.append('../lib')
import syn_const
import qalsadi.stemmedword as stemmedword
import stemmedsynword
import synnode
import pyarabic.araby as araby
debug = False;
# debug = True;
class SyntaxAnalyzer:
	"""
        Arabic Syntax analyzer
	"""
	def __init__(self):
		pass;
	def analyze(self, detailed_stemming_dict):
		"""
		Syntaxic analysis of stemming results.
		morphological Result is a list of stemmedword objects 
		 The syntaxic result have the same structure, but we add a field named 'syntax' to every word steming dictioionary
		@param detailed_stemming_dict: detailed stemming dict.
		@type detailed_stemming_dict:list of list of stemmedword objects;
		@return: detailed syntaxic result with syntaxic tags.
		@rtype: list of list of stemmedsynword;
		"""
		# create stemmed word instances
		stemmedSynWordListList = [];
		synNodeList=[];
		# convert objects from stemmedWord to stemmedSynWord in order to add syntaxic proprities
		for stemmingList in detailed_stemming_dict:
			tmpList = [stemmedsynword.stemmedSynWord(stemmingList[order], order) for order in range(len(stemmingList))];
			if not tmpList: 
				tmpList = [stemmedsynword.stemmedSynWord(stemmingList[0]),]
			stemmedSynWordListList.append(tmpList);
			#create the synode object from tmplist
			synNodeList.append(synnode.synNode(tmpList));
		#----
		#print synNodeList;
		#to test all possible grammars
		#self.detectAcceptedGrammar(synNodeList);
		
		#stemmedSynWordListList = self.studySyntax(stemmedSynWordListList);

		stemmedSynWordListList = self.studySyntaxBySyNode(stemmedSynWordListList, synNodeList);

		return stemmedSynWordListList, synNodeList

	def studySyntax(self, stemmedSynWordListList):
		"""
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
					stmword  =  self.bigramAnalyze(None, stmword )[1];
				else:
					previousCasePosition =0 ; 
					for previous in stemmedSynWordListList[previousIndex]:
						counter+= 1;
						previous, stmword  =  self.bigramAnalyze(previous, stmword, previousCasePosition, stmwordCasePosition);
						previousCasePosition +=1 ; 
							
					#if debug: print "stmword.getSyntax",stmword.getSyntax()
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
			#if debug:print previousIndex , currentIndex;
		#if debug: print " counter total of items analyzed", counter;
		return stemmedSynWordListList;



	def studySyntaxBySyNode(self, stemmedSynWordListList, synNodeList):
		"""
		Analyzing the texts words cases by one syntax node,
		
		"""
		#split the synodelist into small lists (chunks) according to break points
		#Break points are word with syntaxique procletics like WAW conjinctions, and Prepositions
		# treat chunks and choose relationship according to word type
		# verb + noun => verb + subject or verb + objects
		# noun + noun => noun adjective, or mubtad' wa Khabar
		# factor + noun,
		# factor + verb

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
					stmword  =  self.bigramAnalyze(None, stmword )[1];
				else:
					previousCasePosition =0 ; 
					for previous in stemmedSynWordListList[previousIndex]:
						counter+= 1;
						previous, stmword  =  self.bigramAnalyze(previous, stmword, previousCasePosition, stmwordCasePosition);
						previousCasePosition +=1 ; 
							
					#if debug: print "stmword.getSyntax",stmword.getSyntax()
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
			#if debug:print previousIndex , currentIndex;
		#if debug: print " counter total of items analyzed", counter;
		return stemmedSynWordListList;
		#~ return stemmedSynWordListList;


	def bigramAnalyze(self,previous, current, previousPosition=0, currentPosition=0):
		"""
		Syntaxic analysis of stemming results, two words.
		the positions are use to join related cases.
		@param previous	: the first item in bigram.
		@type previous	: stemmedSynWord
		@param current	: the second item in bigram.
		@type current	: stemmedSynWord
		@param currentSynode	: the current synode in The phrase.
		@type  currentSynode	: synnode object
		@param previous	: the first item position in the word case list.
		@type previous	: stemmedSynWord
		@param current	: the second item position in the word case list.
		@type current	: stemmedSynWord		
		@return: the updated previous and current stemmedSynWord.
		@rtype: (previous, current);
		"""
		# Todo treat the actual word according to the previous word
		# treat the initial case when previous =None
		#if debug: print current.isBreak(), 		current.isPounct()
		# to save the forced case to link previous and current word.
		# the word can be forced before this treatement, 
		# the this variable is used to indicate if the word is forced during the actual process.
		forcedCase = False
		weight = 0;
		if not previous or previous.isInitial():
			if current.isMarfou3() or current.isPast() or current.isStopWord():
			 # if  current.isMajrour():
				current.forcedCase();
				# add to the current word case a pointer to the previous word order.
				#p for previous
				# if the previous is None, that means that the previous is initiatl state
				# the current word is prefered, we add previous pointer to 0 position.
				current.addPrevious(syn_const.PrimateRelation);
			
			return (previous, current);
			
		elif not current:
			# if the current word is end of clause or end of line, (None)
			# and the previous is not followed by a word, 
			# the previous will have a next relation. 
			# إذا كانت الكلم الأولى بعدها لا كلمة، أي نهاية العبارة، نضع لها راطة لاحقة إلى لاشيء
			# تستعمل هذه في ضبط أواخر الجمل
			# مثلا
			# جاء ولد
			# تحولّ إلى ثنائيات
			# [None. جاء]، [جاء، ولد]، [ولد، None]

			# if the pounct is a break, the tanwin is prefered
			# the previous will have twnin
	
			if previous.isTanwin():
			# add a relation to previous
				previous.addNext(syn_const.TanwinRelation);
			return (previous, current);
		elif current.isPounct() or current.isStopWord() or  (current.hasProcletic() and not current.isDefined()):
			#if the word is pounctuation and it's transparent, the effect of previous factor will be kept
			#then we ignore this word in the next step, 
			#the variable 'previous' will not take the actual word.
			#if debug:print current.isBreak(), current.isPounct() 
			# if the pounct is a break, the tanwin is prefered
			# the previous will have twnin
	
			if current.isBreak() and previous.isTanwin():
				previous.addNext(syn_const.TanwinRelation);			
			return (previous, current);

		#the stop word is factors, others no, if the previous is not stop word return.
		if previous.isStopWord():
			if current.isNoun():# and previous.isNominalFactor():
				if (previous.isJar() or previous.isAddition()) and  current.isMajrour():
					weight =  syn_const.JarMajrourRelation				

				# اسم إنّ منصوب
				elif previous.isNaseb() and  current.isMansoub():
					current.setInnaNoun();
					weight =  syn_const.InnaNasebMansoubRelation

				elif previous.isInitial() and  current.isMarfou3():
					weight =  syn_const.PrimateRelation	

				# اسم كان وأخواتها
				elif previous.isKanaRafe3() and current.isMarfou3():
					current.setKanaNoun();
					weight =  syn_const.KanaRafe3Marfou3Relation						
				elif previous.isRafe3() and current.isMarfou3():
					weight =  syn_const.Rafe3Marfou3Relation
			#verb
			elif current.isVerb() and previous.isVerbalFactor():
				if previous.isJazem()  and  current.isMajzoum():
					weight =  syn_const.JazemMajzoumRelation
				elif previous.isVerbNaseb() and  current.isMansoub():
					weight =  syn_const.NasebMansoubRelation							
				elif previous.isVerbRafe3() and current.isMarfou3():
					weight =  syn_const.Rafe3Marfou3Relation
		else: # previous is not a stopword
			if current.isVerb():
				# الجارية فعل والسابق مبتدأ
				if previous.isNoun():
					if current.isMarfou3():
					# Todo treat the actual word
						weight =  syn_const.Rafe3Marfou3Relation
			
			if current.isNoun() or current.isAddition():
				# المضاف والمضاف إليه
				# إضافة لفظية
				# مثل لاعبو الفريق
				if current.isMajrour():
					if previous.isAdded():
						weight =  syn_const.JarMajrourRelation
					elif previous.isNoun() and not previous.isDefined() and  not previous.isAdded() and not previous.isTanwin() :
						weight =  syn_const.JarMajrourRelation
				# منعوت والنعت
				#  تحتاج إلى إعادة نظر
				# بالاعتماد على خصائص الاسم الممكن أن يكون صفة
				if previous.isNoun():
					# Todo treat the actual word
					if self.areCompatible(previous, current):
						if current.isAdj():
							weight =  syn_const.DescribedAdjectiveRelation
					#مبتدأ وخبر
					elif self.areNominalCompatible(previous, current):
						if current.isAdj():
							weight =  syn_const.PrimatePredicateRelation
				if previous.isVerb():
					if previous.is3rdperson():
						# Todo treat the actual word
						# الفعل والفاعل أو نائبه
						if current.isMarfou3():
							weight =  syn_const.VerbSubjectRelation
					# الفعل والمفعول به
					if current.isMansoub():
							weight =  syn_const.VerbObjectRelation
		if weight :
			# add to the previous a pointer to the next word order.
			previous.addNext(currentPosition, weight);

			# add to the current word case a pointer to the previous word order.
			current.addPrevious(previousPosition, weight);
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
		else: return False;

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
		if not ((previous.isNoun() or previous.isAddition()) and current.isNoun()):
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
		# مذكر ومذكر
		#مؤنث ومؤنث
		# جمع التكسير مؤنث
		if (current.isFeminin() and previous.isFeminin()) or (current.isMasculin() and previous.isMasculin()) or (previous.isBrokenPlural() and current.isFeminin()):
			compatible = True;
		else: return False;
		
		return compatible;


	def areNominalCompatible(self, previous, current):
		"""
		verify the gramatica relation between the two words, for nominal relational المبتدأ والخبر
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
		compatible = False;
		if (previous.isNoun() and current.isNoun()):
			# التعريف
			# المبتدأ معرفة والخبر نكرة
			if (not current.isDefined() and previous.isDefined()):
				compatible = True;
			else:
				return False;
			# الحركة
			# تقابل الحالة الإعرابية
			# مبتدأ مرفوع خبر مرفوع
			# مبتدأ منصوب خبر مرفوع# اسم كان
			# مبتدأ مرفوع خبر منصوب#  اسم إنّ
			if (previous.isInnaNoun() and previous.isMansoub() and current.isMarfou3())\
			or (previous.isKanaNoun() and previous.isMarfou3() and current.isMansoub())\
			or (not previous.isInnaNoun() and not previous.isKanaNoun() and previous.isMarfou3() and current.isMarfou3()):
				compatible = True;
			else:
				return False;
			# الكلمة الثانية  غير مسبوقة بسابقة غير التعريف
			# هذا التحقق جاء بعد التحقق من التعريف أو التنكير
			if not current.hasProcletic():
				compatible = True;
			else:
				return False;
			# التنوين
			if not previous.isTanwin():
				compatible = True;
			else:
				return False;
			# والتثنية والإفراد الجمع
			# التذكير والتأنيث
			# مذكر ومذكر
			#مؤنث ومؤنث
			# جمع التكسير مؤنث
			if (current.isFeminin() and previous.isFeminin()) or (current.isMasculin() and previous.isMasculin()) or (previous.isBrokenPlural() and current.isFeminin()):
				compatible = True;
			else: return False;
		#الأول اسم والثاني فعل
		elif (previous.isNoun() and current.isVerb()):
		
			# التعريف
			# المبتدأ معرفة والخبر نكرة
			if previous.isDefined():
				compatible = True;
			else:
				return False;
			# الحركة
			# تقابل الحالة الإعرابية
			# مبتدأ مرفوع خبر مرفوع
			# مبتدأ منصوب خبر مرفوع# اسم كان
			# مبتدأ مرفوع خبر منصوب#  اسم إنّ

			# الكلمة الثانية  غير مسبوقة بسابقة غير التعريف
			# هذا التحقق جاء بعد التحقق من التعريف أو التنكير
			if not current.hasProcletic():
				compatible = True;
			else:
				return False;
			# التنوين
			if not previous.isTanwin():
				compatible = True;
			else:
				return False;
			# والتثنية والإفراد الجمع
			# التذكير والتأنيث
			# مذكر ومذكر
			#مؤنث ومؤنث
			# جمع التكسير مؤنث
			# if (current.isFeminin() and previous.isFeminin()) or (current.isMasculin() and previous.isMasculin()) or (previous.isBrokenPlural() and current.isFeminin()):
				# compatible = True;
			# else: return False;		
			#الفعل مرفوع أو مبني
			if current.isPast() or (current.isPresent() and current.isMarfou3()):
				compatible=True;
			else:
				return False;
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

	def detectAcceptedGrammar(self, synNodeList):
		"""
		Detect Possible syntaxical nodes sequences
		@param synNodeList: list of synNode.
		@type synNodeList:  list of synNode.
		"""
		#for Test
		# display all cases
		#print synNodeList;
		grammarList=[];
		for sn in synNodeList:
			tmplist=[];
			taglist=[];
			if sn.hasVerb():
				taglist.append('V');
			if sn.hasNoun():
				taglist.append('N');
			if sn.hasStopword():
				taglist.append('S');
			if sn.hasPounct():
				taglist.append('.');
			if not grammarList:
				grammarList=taglist;
			else:
				for g in grammarList:
					for tag in taglist:
						tmplist.append(g+tag);
			if tmplist:
				grammarList=tmplist;
		#add 
		# tmplist= [];
		if debug:
			for g in grammarList:
				if not g.endswith('.'):
					g+='.';
				if g in syn_const.GrammarPhrase:
					print g, 'ok';
				else:
					print g, 'no';
			# tmplist.append(g);
		# grammarList=tmplist;
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
