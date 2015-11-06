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


from CodernityDB.database import Database
from CodernityDB.hash_index import HashIndex
from hashlib import md5
import pyarabic.arabrepr as arabrepr
arabicRepr = arabrepr.ArabicRepr()


class WithAIndex(HashIndex):

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        #~ kwargs['hash_lim'] = 4 * 1024
        super(WithAIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        a_val = data.get("a")
        if a_val:
            if not isinstance(a_val,unicode):
                a_val = unicode(a_val)
            return md5(a_val.encode('utf8')).hexdigest(), {}
        return None

    def make_key(self, key):
        if not isinstance(key, unicode):
            key = unicode(key)
        return md5(key.encode('utf8')).hexdigest()

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
		self.db = Database('~/tmp/qalsadiCache')
		if not self.db.exists():
			self.db.create();
			x_ind = WithAIndex(self.db.path, 'a')
			self.db.add_index(x_ind)        
		else:
			self.db.open();

	def __del__(self):
		"""
		Delete instance and clear cache
		
		"""
		self.cache=None;
		self.db.close();

	def isAlreadyChecked(self, word):
		try:
			return bool(self.db.get('a', word))
		except: return False
		#~ except: return False;

	def getChecked(self, word):
		x = self.db.get('a', word, with_doc=True)
		y= x.get('doc',False);
		if y: return y.get('d',[])
		else: return []
	
	def addChecked(self, word, data):
		idata = {"a":word,'d':data}
		self.db.insert(idata)

	
	def existsCacheFreq(self, word, wordtype):
		return word in self.cache['FreqWords'];
	
	def getFreq(self, originalword, wordtype):
		return self.cache['FreqWords'][wordtype].get(originalword,0);
	
	def addFreq(self, original, wordtype, freq):
		self.cache['FreqWords'][wordtype][original] = freq;
		
def mainly():
	print "test";		
	
if __name__=="__main__":
	mainly();
