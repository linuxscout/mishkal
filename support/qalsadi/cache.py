#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        analex
# Purpose:     Arabic lexical analyser, provides feature to stem arabic 
#words as noun, verb, stopword
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
"""Cache Module for analex"""
if __name__ == "__main__":
    import sys
    sys.path.append('..')

from CodernityDB.database import Database
from CodernityDB.hash_index import HashIndex
from hashlib import md5
import pyarabic.arabrepr as arabrepr
arabicRepr = arabrepr.ArabicRepr()
import os
#DB_PATH = '/var/qalsadiCache'
DB_PATH = os.path.join(os.path.expanduser('~'), '.qalsadiCache')


class WithAIndex(HashIndex):
    """ hache with Index Class """
    def __init__(self, *args, **kwargs):
        """init"""
        kwargs['key_format'] = '32s'
        #~ kwargs['hash_lim'] = 4 * 1024
        super(WithAIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        """make a key value from ``data`` """
        a_val = data.get("a")
        if a_val:
            if not isinstance(a_val, unicode):
                a_val = unicode(a_val)
            return md5(a_val.encode('utf8')).hexdigest(), {}
        return None

    def make_key(self, key):
        """make a ``key`` """
        if not isinstance(key, unicode):
            key = unicode(key)
        return md5(key.encode('utf8')).hexdigest()


class Cache(object):
    """
        cache for word morphological analysis
    """

    def __init__(self, ):
        """
        Create Analex Cache
        """
        self.cache = {
            'checkedWords': {},
            'FreqWords': {
                'noun': {},
                'verb': {},
                'stopword': {}
            },
        }
        self.db = Database(DB_PATH)
        if not self.db.exists():
            self.db.create()
            x_ind = WithAIndex(self.db.path, 'a')
            self.db.add_index(x_ind)
        else:
            self.db.open()

    def __del__(self):
        """
        Delete instance and clear cache

        """
        self.cache = None
        self.db.close()

    def is_already_checked(self, word):
        """ return if ``word`` is already cached"""
        try:
            return bool(self.db.get('a', word))
        except:
            return False
        #~ except: return False;

    def get_checked(self, word):
        """ return checked ``word`` form cache"""
        xxx = self.db.get('a', word, with_doc=True)
        yyy = xxx.get('doc', False)
        if yyy:
            return yyy.get('d', [])
        else: return []

    def add_checked(self, word, data):
        """ add checked ``word`` form cache"""
        idata = {"a": word, 'd': data}
        self.db.insert(idata)

    def exists_cache_freq(self, word, wordtype):
        """ return if word exists in freq cache"""
        return word in self.cache['FreqWords']

    def get_freq(self, originalword, wordtype):
        """ return  ``word`` frequency form cache"""
        return self.cache['FreqWords'][wordtype].get(originalword, 0)

    def add_freq(self, original, wordtype, freq):
        """ add   ``original`` frequency ``freq`` to cache"""
        self.cache['FreqWords'][wordtype][original] = freq


def mainly():
    """main function"""
    print("test")


if __name__ == "__main__":
    mainly()
