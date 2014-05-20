#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Arabic Stop Word Dictionary from Arramooz Al Waseet
# Purpose:     Morphological porpus Dictionary.
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     16-12-2013
# Copyright:   (c) Taha Zerrouki 2013
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
Arabic Stop Word Dictionary Class from Arramooz Al Waseet.
Used in multiporpus morpholigical treatment
"""
import re
import sys, os

import sqlite3 as sqlite
FILE_DB_FREQ=u"data/stopwords.sqlite"
import pyarabic.araby as araby
stopwords_DICTIONARY_INDEX={
u'id':0, # id
u'unvocalized':1, # the unvocalized word
u'procletic':2, 
u'tags':3, # word tags
u'vocalized':4,# the vocalized form
u'stem':5, # the stem word
u'type':6, # the word type
u'original':7, #the word original
u'encletic':8, # the word  encletic
}

class stopWordsDictionary:
	"""
		Arabic dictionary Class
		Used to allow abstract acces to lexicon of arabic language,
		can get indexed and hashed entries from the  basic lexicon
		add also, support to extract attributtes from entries
	"""

	def __init__(self, tableName, attribIndex, keyAttribute='unvocalized'):
		"""
		initialisation of dictionary from a data dictionary, create indexes to speed up the access.

		"""
		# load data from the brut dictionary into a new dictionary with numeric ids
		self.dictionary={};
		self.attribIndex=attribIndex;
		self.keyAttribute= keyAttribute;
		self.attribNumIndex={};
		# create the attribute num index
		# attribIndex: 		attribNumIndex
		# vocalized: 0		0: vocalized
		#unvocalized: 1		1: unvocalized
		#
		for k in self.attribIndex.keys():
			v=self.attribIndex[k];
			self.attribNumIndex[v]=k;
		self.tableName=tableName;
		# get the database path
		if hasattr(sys,'frozen'): # only when running in py2exe this exists
			base = sys.prefix
		else: # otherwise this is a regular python script
			base = os.path.dirname(os.path.realpath(__file__))
		file_path=os.path.join(base, FILE_DB_FREQ);
		
		if os.path.exists(file_path):
			try:
				self.dbConnect = sqlite.connect(file_path)
				self.dbConnect.row_factory = sqlite.Row 				
				self.cursor = self.dbConnect.cursor()
			except:
				print "Fatal Error Can't find the database file", file_path

		else:
			print u" ".join(["Inexistant File", file_path, " current dir ", os.curdir]).encode('utf8');
		#create index to speed up search
		indexField='unvocalized'
		self.createTableIndex(indexField);

		# if self.createTableIndex(indexField):
			# print 'Index created';
		# else:
			# print (' Cant create index', self.tableName, indexField);

	def __del__(self):
		"""
		Delete instance and close database connection
		
		"""
		if self.dbConnect:
			self.dbConnect.close();

			
			
	def createTableIndex(self, indexField):
		""" create the database index if not exists
		@param indexField: the given to be indexed field
		@type indexField: text;
		@return: void
		@rtype: void
		"""
		sql = u"create index if not exists myindex on %s (%s)"%(self.tableName, indexField);
		try:
			self.cursor.execute(sql);
			if self.cursor:
				return True;
				
		except:

			return False;

	def getEntryById(self,id):
		""" Get dictionary entry by id from the dictionary
		@param id: word identifier
		@type id: integer
		@return: all attributes
		@rtype: dict
		"""
		# if the id exists and the attribute existe return the value, else return False
		# The keys in the dictinary are numeric, for comression reason,
		# then we use text keys in output, according to the self.attribNumIndex
		# eg.
		# entry ={0:"kataba", 1:"ktb"}
		# output entry ={'vocalized':'kataba', 'unvocalized':'ktb'}
		sql = u"select * FROM %s WHERE id='%s'"%(self.tableName,id);
		try:
			self.cursor.execute(sql);
			if self.cursor:
				for row in self.cursor:
					entryDict={}
					for numKey in self.attribNumIndex:
						textKey = self.attribNumIndex[numKey]
						if row[numKey]:
							entryDict[textKey] = row[numKey]
						else: entryDict[textKey] = u'';
					return entryDict;
		except:
			return False;
		return False;

	def getAttribById(self,id, attribute):
		""" Get attribute value by id from the dictionary
		@param id : word identifier
		@type id: integer
		@param attribute:the attribute name
		@type attribute: unicode
		@return: The attribute
		value
		@rtype: mix.
		"""
		# if the given attribute existes on the attrib index
		#in order to redure the dictionary size we use numecric index to show the attributes
		# like
		#NOUN_DICTIONATY_INDEX={u'vocalized':0, u'unvocalized':1, u'wordtype':2, u'root':3, u'original':4, u'mankous':5, u'feminable':6, u'number':7, u'dualable':8, u'masculin_plural':9, u'feminin_plural':10, u'broken_plural':11, u'mamnou3_sarf':12, u'relative':13, u'w_suffix':14, u'hm_suffix':15, u'kal_prefix':16, u'ha_suffix':17, u'k_suffix':18, u'annex':19, u'definition':20, u'note':21, }
		#NOUN_DICTIONARY={
		#u'مفرد/تكسير':{0:u'مفرد/تكسير', 1:u'مفرد/تكسير', 2:u'اسم فاعل', 3:u'', 4:u'', 5:u'المنقوص', 6:u'التأنيث', 7:u'جمع تكسير', 8:u'التثنية', 9:u'"ج. مذ. س."', 10:u'"ج. مؤ. س."', 11:u'الجمع', 12:u'', 13:u'نسب', 14:u'ـو', 15:u'هم', 16:u'كال', 17:u'ها', 18:u'ك', 19:u'"إض. لف."', 20:u'', 21:u':لا جذر:لا مفرد:لا تشكيل:لا شرح', },
		#u'شَاذّ':{0:u'شَاذّ', 1:u'شاذ', 2:u'اسم فاعل', 3:u'', 4:u'', 5:u'', 6:u'Ta', 7:u'جمع تكسير', 8:u'DnT', 9:u'Pm', 10:u'Pf', 11:u'":شواذ"', 12:u'', 13:u'', 14:u'', 15:u'', 16:u'', 17:u'', 18:u'', 19:u'', 20:u'', 21:u':لا جذر:لا مفرد:لا شرح', },

		# if self.attribIndex.has_key(attribute):
			# attnum=self.attribIndex[attribute];
		# else:
			# return False;
		# if the id exists and the attribute existe return the value, else return False
		sql = u"select * FROM %s WHERE id='%s'"%(self.tableName,id);
		try:
			self.cursor.execute(sql);
			entryDict={}		
			if self.cursor:
				for row in self.cursor:
						# return  row[attnum]
						return  row[attribute]						
		except:
			return False;					
		return False;

	def lookup(self,text):
		"""
		look up for all word forms in the dictionary, according to word_type
			- 'verb': lookup for verb only.
			- 'noun': llok up for nouns.
			- 'unknown': the word is not alayzed, then search for unvocalized word.
			- '': look for voaclize word without type
		@param text:vocalized word.
		@type text: unicode.
		@return: list of dictionary entries IDs.
		@rtype: list.
		"""
		idList=[];
		sql = u"select * FROM %s WHERE unvocalized='%s'"%(self.tableName,text);
		try:
			self.cursor.execute(sql);
			if self.cursor: 
				# return self.curser.fetchall();
				for row in self.cursor:
						idList.append(row);
			return idList;
		except:
			return [];
	def isStopWord(self,text):
		"""
		return the word frequency from the in the dictionary
		@param text:vocalized word.
		@type text: unicode.
		@return: word freq.
		@rtype: integer.
		"""
		idList=[];
		#if araby.isHaraka(text[-1:]): text=text[:-1];
		idList=self.lookup(text);
		# if there are many take the first
		if idList:
			return True;
		else: 
			return False;

#Class test
if __name__ == '__main__':
	#ToDo: use the full dictionary of arramooz
	wordfreq_DICTIONARY_INDEX={
	u'id':0, # id
	u'vocalized':1, # the vocalized word
	u'unvocalized':2,# the unvocalized form
	u'word_type':3, # the word frequency
	u'freq':4, # the word class
	u'future_type':5, # the haraka for verb	
	#u'trans':5,  # translation
	}
	#from   dictionaries.verb_dictionary  import *
	mydict=stopWordsDictionary('stopwords', stopwords_DICTIONARY_INDEX);
	wordlist=[u"بعضهما", u'في',u"منً", u"أن", u'عندما']
	
	for word in wordlist:
		print "-------"
		print "word freq", mydict.isStopWord(word);
		idlist=mydict.lookup(word);
		print idlist;
		for id in idlist:
			print mydict.getAttribById(id, 'original').encode('utf8');
			myentry= mydict.getEntryById(id);
			print repr(myentry);