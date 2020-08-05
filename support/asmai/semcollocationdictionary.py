#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        semantic collocations
# Purpose:     Arabic automatic vocalization.
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------

import re
import sqlite3 as sqlite
FILE_DB=u"data/collocations.sqlite"
import pyarabic.araby as araby
class semCollocationDictionary:
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
		for k in list(self.attribIndex.keys()):
			v=self.attribIndex[k];
			self.attribNumIndex[v]=k;
		self.tableName=tableName;
		try:
			self.dbConnect = sqlite.connect(FILE_DB)
			self.cursor = self.dbConnect.cursor()
		except:
			print "Fatal Error Can't find the database file", FILE_DB

			
	def __del__(self):
		"""
		Delete instance and close database connection
		
		"""
		if self.dbConnect:
			self.dbConnect.close();
			#print "___del__ collocation dictionary called";
	def getEntryById(self,id):
		""" Get dictionary entry by id from the dictionary
		@param id word identifier
		@type id: integer
		@param attribute the attribute name
		@type attribute: unicode
		@return: all attributes
		@rtype: dict
		"""
		# if the id exists and the attribute existe return the value, else return False
		# The keys in the dictinary are numeric, for comression reason,
		# then we use text keys in output, according to the self.attribNumIndex
		# eg.
		# entry ={0:"kataba", 1:"ktb"}
		# output entry ={'vocalized':'kataba', 'unvocalized':'ktb'}
		sql = u"select * FROM %s WHERE id=%d"%(self.tableName,id);
		try:
			self.cursor.execute(sql);
			if self.cursor:
				for row in self.cursor:
					entryDict={}
					for numKey in self.attribNumIndex:
						textKey = self.attribNumIndex[numKey]
						entryDict[textKey] = row[numKey]
					return entryDict;
		except:
			return False;
		return False;

	def getAttribById(self,id, attribute):
		""" Get attribute value by id from the dictionary
		@param id word identifier
		@type id: integer
		@param attribute the attribute name
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

		if self.attribIndex.has_key(attribute):
			attnum=self.attribIndex[attribute];
		else:
			return False;
		# if the id exists and the attribute existe return the value, else return False
		sql = u"select * FROM %s WHERE id=%d"%(self.tableName,id);
		try:
			self.cursor.execute(sql);
			entryDict={}		
			if self.cursor:
				for row in self.cursor:
						return  row[attnum]
		except:
			print "error in request getattribut by id";
			return False;					
		return False;

	def lookup(self,text):
		"""
		look up for all word forms in the dictionary
		@param text: the normalized word.
		@type text: unicode.
		@return: list of dictionary entries IDs.
		@rtype: list.
		"""
		idList=[];

		sql = u"select id FROM %s WHERE vocalized='%s'"%(self.tableName,text);
		try:
			self.cursor.execute(sql);
			if self.cursor:
				for row in self.cursor:
						idList.append(row[0]);
			# for collocation we must have only one reponse, if have a lot, we oignore it
			if len(idList)>1:
				return [];
			else:
				return idList;
		except:
			return [];

#Class test
if __name__ == '__main__':
	#ToDo: use the full dictionary of arramooz
	Collocation_DICTIONARY_INDEX={
	u'id':0,
	u'vocalized':1,
	u'unvocalized':2,
	u'rule':3,
	u'category':4,
	u'note':5,
	}
	#from   dictionaries.verb_dictionary  import *
	mydict=semCollocationDictionary('collocations', Collocation_DICTIONARY_INDEX);
	wordlist=[u"صلاة الفجر", u'كرة القدم',u"دولة قطر"]
	for word in wordlist:
		print "jjjjjjjj"
		idlist=mydict.lookup(word);
		print idlist;
		for id in idlist:
			print mydict.getAttribById(id, u'vocalized').encode('utf8');
			myentry= mydict.getEntryById(id);
			print repr(myentry);