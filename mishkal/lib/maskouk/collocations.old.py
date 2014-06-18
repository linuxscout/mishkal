#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        collocations
# Purpose:     Arabic automatic vocalization.
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
import collocationdictionary
#import collocationdictionary as colloDict
import collocation_const
import pyarabic.araby as araby
import itertools
class CollocationClass:
	"""
        Arabic Collocations Class
	"""

	def __init__(self, showDelimiter=False):
		self.min=2;
		self.max=5;
		# used to quote the collocations
		self.delimiter = u"'";
		# used to mention the unvocalized collocation
		# this feature is temporary to get the user feed back about unvocalized  collocations
		self.unknownDelimiter =u"~";
		self.showDelimiter = showDelimiter;
		Collocation_DICTIONARY_INDEX={
		u'id':0,
		u'vocalized':1,
		u'unvocalized':2,
		u'rule':3,
		u'category':4,
		u'note':5,
		}
		#cache of collocations to speedup the process
		self.colloCache={}
		# enable and disable Cache use
		self.CacheEnabled = True;
		#from   dictionaries.verb_dictionary  import *
		self.colloDict=collocationdictionary.collocationDictionary('collocations', Collocation_DICTIONARY_INDEX);
		for key in collocation_const.GENERAL_COLLOCATIONS.keys():
			self.colloCache[key]= collocation_const.GENERAL_COLLOCATIONS[key]['v'];
		pass;
	def setMin(self,min0):
		# to avoid errers, verify the min
		self.min=min(min0,self.min);
		self.max=max(min0,self.max);		
	def setMax(self,max0):
		# to avoid errers, verify the max
		self.min=min(max0,self.min);
		self.max=max(max0,self.max);
	def setDelimiter(self,delimiter):
		"""
		set the delimiter for collocations output
		@param delimiter : the given delimiter.
		@type delimiter : one unicode char.
		"""
		self.delimiter = delimiter;
	def getDelimiter(self):
		"""
		get the delimiter used for collocations output
		@return : return the actual delimiter.
		@rtype : one unicode char.
		"""
		return self.delimiter;
	def setUnknownDelimiter(self,delimiter):
		"""
		set the delimiter for unvocalized collocations output
		@param delimiter : the given delimiter.
		@type delimiter : one unicode char.
		"""
		self.unknownDelimiter = delimiter;
	def getUnknownDelimiter(self):
		"""
		get the  unknown delimiter used for collocations output
		@return : return the actual unknown delimiter.
		@rtype : one unicode char.
		"""
		return self.unknownDelimiter;

	def enableShowDelimiter(self):
		"""
		Enable the option to show collocation delimiters
		"""
		self.showDelimiter = True;

	def disableShowDelimiter(self):
		"""
		Enable the option to show collocation delimiters
		"""
		self.showDelimiter = False;

	def enableCache(self):
		"""
		Enable the option to enable cache
		"""
		self.CacheEnabled = True;

	def disableCache(self):
		"""
		disable the option to show collocation delimiters
		"""
		self.CacheEnabled = False;
	def getShowDelimiter(self):
		"""
		get the show delimimter state
		@return : return the actual state of collocation delimiter show.
		@rtype : Boolean.
		"""
		return self.showDelimiter;

	def isCollocated(self,wordlist):
		"""
		Return The vocalized text if the word list is collocated.
		@param wordlist: word of list, 2 or more words.
		@type wordlist: list of unicode.
		@return : The collocation as a key if exists. else False.
		@rtype: dict/None.
		"""
		# The fisrt case is the two words collocation

		# get two element from the list start
		key=u' '.join(wordlist);
		
		if len(wordlist)<2:
			return False;
		elif len(wordlist)>2:
			# the more than 2 words collocations are a small list 
			# mentioned in Gcollocation_const.GENRAL_COLLOCATIONS
			# key=u' '.join(wordlist);			
			if self.CacheEnabled and self.colloCache.has_key(key): 
				return key;
		elif  not collocation_const.token_pat.search(key) :
		# invalid words
			return False;	
		else:
			# get two element from the list start
			key=u' '.join(wordlist);
			# if the key existss in the cache.
			if self.CacheEnabled and self.colloCache.has_key(key): 
				return key;			
			
			#print key.encode('utf8');
			idlist=self.colloDict.lookup(key);
			# if the wordlist as key existes in collocation database, 
			# insert its vocalization in a collocation cache dict
			if len(idlist)>=1 :
				if self.CacheEnabled and not self.colloCache.has_key(key): 
					firstEntry=idlist[0];
					#print idlist;
					# self.colloCache[key]= self.colloDict.getAttribById(id,'vocalized')
					self.colloCache[key]= firstEntry['vocalized']					
				return key;
			else:
				#before return false we can strip samm prefix from the clause
				# for example : الحمد لله
				# is a collocation,, but بالحمد لله is not found
				if key[0] in (araby.FEH, araby.WAW, araby.BEH, araby.LAM, araby.KAF):
					firstLetter=key[0];
					newKey=key[1:];
					#print key.encode('utf8');
					#look up for the new key
					idlist=self.colloDict.lookup(newKey);
					# if the wordlist as key existes in collocation data base, 
					# insert its vocalization in a collocation cache dict
					if len(idlist)>=1 :
						if self.CacheEnabled and not self.colloCache.has_key(key): 
							# id=idlist[0];
							#print idlist;
							# vocalizedCollocation = self.colloDict.getAttribById(id,'vocalized')
							vocalizedCollocation = idlist[0]['vocalized']							
							# some fields in database are not vocalized
							if vocalizedCollocation!="":
								# save the variant of collocation also, by key
								self.colloCache[key] = firstLetter+ vocalizedCollocation
							else: 
								# if vocalized is empty, save a empty string in cache
								# if the returned string is empty the program suggest to vocalized the collocation
								self.colloCache[key] = vocalizedCollocation

							# save the found collocation in cache by newKey
								if not self.colloCache.has_key(newKey):
									self.colloCache[newKey] = vocalizedCollocation;
							
						# return the given key
						return key;

					else: return False;
				return False;		
		return False;

	def ngramfinder(self,min,liste):
		"""
		Lookup for ngram (min number of words), in the word list.
		return a list of single words and collocations.
		@param wordlist: word of list, 2 or more words.
		@type wordlist: list of unicode.
		@param min: minimum number of words in the collocation
		@type min: integer.		
		@return : list of words and collocations, else False.
		@rtype: list /None.
		"""	
		newlist=[];
		while len(liste)>=min:
			sublist=[];
			for i in range(min):
				current=liste.pop();
				# if araby.isArabicword(current):
				sublist.insert(0,current);
				# else:
					# sublist=[];
					# break;
			if sublist:
				print "bsublis", u' '.join(sublist).encode('utf8');
				result=self.isCollocated(sublist);
				if result:
					newlist.append(result);
				else:
					newlist.append(sublist.pop());
					liste.extend(sublist);
		# rest element
		liste.reverse()
		newlist.extend(liste);
		newlist.reverse();
		return newlist




	def lookup(self,wordlist):
		"""
		Lookup for all ngrams , in the word list.
		return a list of vocalized words collocations.
		@param wordlist: word of list, 2 or more words.
		@type wordlist: list of unicode.
		@return : dict of words attributes like dict {'vocalized':vocalizedword list,'category': categoryOfCollocation}. else False.
		@rtype: dict of dict /None.
		"""
		#lookup for collocation from max number to min number of words in the collocation
		i=self.max;
		collolist=wordlist;
		while i>=self.min: 
			collolist= self.ngramfinder(i,collolist);
			#print repr(collolist);
			i-=1;
		#Get the list of single words and collocations
		#collolist=self.ngrams(self.min, self.max, wordlist);
		##collodict={};
		newlist=[]
		#print repr(self.colloCache);
		for item in collolist:
			if self.colloCache.has_key(item):
				vocalized=self.colloCache[item];
				#lookup for collocations in dictionary
				# the dictionary conatins the vocalized collocation,
				# but it contains also a list of collocations non vocalized yet,
				# this 'vocalized value is empty, then we use this feature to collect the user feed back and correction
				if vocalized!=u"":
					# if the vocalization is vocalized, we don't mention it
					# newlist.append(u"'"+vocalized+u"'");
					if self.getShowDelimiter():
						newlist.append(u''.join([self.getDelimiter(),item, self.getDelimiter()]));
					else:
						newlist.append(vocalized);					
				else:
					# ig the collocation isn't vocalized, we delemeit it by ~, to collect corrections.
					if self.getShowDelimiter():
						newlist.append(u''.join([self.getUnknownDelimiter(),item, self.getUnknownDelimiter()]));				
					else:
						newlist.append(item);						
			else:
				newlist.append(item);
		return newlist;
	def isPossibleCollocation(self,list2,context="",lenght=2):
		"""
		Guess if the given list is a possible collocation
		This is used to collect unkown collocations, from user input
		return True oor false
		@param wordlist: word of list, 2 or more words.
		@type wordlist: list of unicode.
		@param lenght: minimum number of words in the collocation
		@type lenght: integer.		
		@return : the rule of found collocation, 100 default.
		@rtype: interger.
		"""		
		if len(list2)<lenght:
			return 0;
		else:
			itemV1=list2[0];
			itemV2=list2[1];
			item1=araby.stripTashkeel(itemV1);
			item2=araby.stripTashkeel(itemV2);		
			#if item1[-1:] in (u".",u"?",u",",u'[', u']',u'(',')'):
			#	return 0;
			if  not collocation_const.token_pat.search(item1) or not collocation_const.token_pat.search(item2) :
				return -1;
			#else: return 100;
			elif item1 in collocation_const.ADDITIONAL_WORDS :
				return 10;
			elif item1 in collocation_const.NAMED_PRIOR :
				return 15;			
			elif (item2 not in collocation_const.SPECIAL_DEFINED):
				if  item2.startswith(u'ال') and  item1.startswith(u'ال'):#re.search(ur'^(ال|بال|وبال|فال|وال|لل|كال|فكال|ولل|فلل|فبال)', item1):
					return 20;
				elif item1.endswith(u'ة') and item2.startswith(u'ال'):
					return 30;

				#حالة الكلمات التي تبدأ بلام الجر والتعريف 
				# لا داعي لها لأنها دائما مجرورة
				#if  item2.startswith(u'لل'):
				#	return 40;
				elif item1.endswith(u'ة') and item2.endswith(u'ة')  :
					return 40;
				#if item1.endswith(u'ي') and item2.endswith(u'ي'):
				#	return 60;

				elif  context!=u"" and context in collocation_const.tab_noun_context and item2.startswith(u'ال') :
					return 50;
				#return True;

				elif item1.endswith(u'ات') and item2.startswith(u'ال') :
					return 60;
			return 100;

		
#Class test
if __name__ == '__main__':
	collocationdictionary.FILE_DB=u"data/collocations.sqlite"
	collo=CollocationClass()
	wordlist=[u"قبل",u"صلاة",u"الفجر",u"كرة",u"القدم",u"في",u"دولة",u"قطر", u"الآن", u"أن"]
	words=u"""تغمده الله برحمته . أشهد أن لا إله إلا الله وحده لا شريك له . أشهد أن محمدا عبده ورسوله . صلى الله عليه وآله وصحبه وسلم . أشهد أن لا إله إلا الله . أشهد أن محمدا رسول الله . صلى الله عليه وسلم .
	"""
	words+=u"والحمد لله . الحمد لله . بالحمد لله . بسم الله الرحمن الرحيم . عبد الله . بعبد الله ."
	# words=u"بسم الله الرحمن الرحيم"
	wordlist=words.split(' ');
	collo.setDelimiter('#');
	collo.setUnknownDelimiter('@');	
	collo.enableShowDelimiter();
	# collo.disableCache();	
	
	for i in range(100):
		newlist=collo.lookup(wordlist);
		print u'\t'.join(newlist).encode('utf8')
