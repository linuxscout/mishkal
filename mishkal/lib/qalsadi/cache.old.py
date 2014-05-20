#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        analex
# Purpose:     Arabic lexical analyser, provides feature to stem arabic words as noun, verb, stopword 
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
if __name__=="__main__":
	import sys
	sys.path.append('..');


class cache :
	"""
		cache for word morphological analysis
	"""
	def __init__(self,):
		"""
		Create Analex Cache
		"""
		self.cache={'checkedWords':{},
			    'FreqWords':{'noun':{}, 'verb':{},'stopword':{}},
			};

	def __del__(self):
		"""
		Delete instance and clear cache
		
		"""
		self.cache=None;
	def isAlreadyChecked(self, word):
		return word in self.cache['checkedWords'];
		
	def getChecked(self, word):
		return self.cache['checkedWords'][word];
	
	def addChecked(self, word, data):
		self.cache['checkedWords'][word] = data;
	
	def existsCacheFreq(self, word, wordtype):
		return word in self.cache['FreqWords'];
	
	def getFreq(self, originalword, wordtype):
		return self.cache['FreqWords'][wordtype].get(originalword,0);
	
	def addFreq(self, original, wordtype, freq):
		self.cache['FreqWords'][wordtype][original]=freq;
		
def mainly():
	print "test";		
	
if __name__=="__main__":
	mainly();
