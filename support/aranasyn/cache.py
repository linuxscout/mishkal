#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        anasyn
# Purpose:     Arabic syntax analyser, 
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     13-12-2017
# Copyright:   (c) Taha Zerrouki 2017
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
Cache system for extrcat features for words relations.
"""
if __name__=="__main__":
    import sys
    sys.path.append('../');
    sys.path.append('../../support/');


from CodernityDB.database import Database
from CodernityDB.hash_index import HashIndex
from hashlib import md5
from pyarabic.arabrepr import arepr


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
        # use this dictionary as a local cache,
        # The global db will be updated on destructing object
        self.cache={};
        self.db = Database('~/tmp/thaalibCache')
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

    def update(self):
        """update data base """
        for word in self.cache:
            self.add_checked(word, self.cache[word])        

    def is_already_checked(self, word):
        try:
            return bool(self.db.get('a', word))
        except:
            return False
        #~ except: return False;

    def get_checked(self, word):
        x = self.db.get('a', word, with_doc=True)
        y = x.get('doc',False);
        if y: 
            return y.get('d',[])
        else: return []
    
    def add_checked(self, word, data):
        idata = {"a":word,'d':data}
        try:
            saved = self.db.get('a', word, with_doc=True)
        except:
            saved = False
        if saved:
            saved['doc']['d'] = data
            doc  = saved['doc']
            doc['update'] = True
            self.db.update(doc)
        else:
            self.db.insert(idata)

    
    def exists_cache_word(self, word):
        return word in self.cache;
    
    def get_relation_freq(self, word_prev, word_cur, relation):
        
        return self.cache.get(word_prev, {}).get(word_cur, {}).get(relation, 0);
    
    def is_related(self, word_prev, word_cur):
        
        return self.cache.get(word_prev, {}).get(word_cur, {});

    def add_relation(self, word_prev, word_cur, relation):
        
        #~ relation ='r'+str(relation)

        if word_prev not in self.cache:
            # test first that is in db cache
            if self.is_already_checked(word_prev):
                stored_data = self.get_checked(word_prev)
                self.cache[word_prev] = stored_data
            else: # create an new entry
                self.cache[word_prev] = {word_cur:{relation:1, }, }

        # word_prev exists
        # add word_cur to previous dict
        elif word_cur not in self.cache[word_prev]:
            self.cache[word_prev][word_cur] = {relation:1,}
                
        elif relation not in self.cache[word_prev][word_cur]:
            self.cache[word_prev][word_cur][relation] = 1
        else:
            self.cache[word_prev][word_cur][relation] += 1

    def display_all(self):
        """ display all contents of data base """
        print "aranasyn.cache: dislay all records in Thaalib Database """
        for curr in self.db.all('a', with_doc=True):
            print curr['doc']['a'], arepr(curr['doc']['d'])
        
def mainly():
    mycache = cache()
    #mycache.display_all()      
    
if __name__=="__main__":
    mainly();
