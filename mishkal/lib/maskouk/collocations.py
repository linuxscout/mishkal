#!/usr/bin/python
# -*- coding=utf-8 -*-
#-----------------------------------------------------------------------
# Name:        collocations
# Purpose:     Arabic automatic vocalization.
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-----------------------------------------------------------------------
"""
    Arabic _collocations Class
"""
import maskouk.collocationdictionary as collocationdictionary
import maskouk.collocation_const as cconst
import pyarabic.araby as araby
import re
class CollocationClass:
    """
        Arabic _collocations Class
    """

    def __init__(self, show_delimiter = False):
        self.mini = 2
        self.maxi = 5
        # used to quote the collocations
        self.delimiter = u"'"
        # used to mention the unvocalized collocation
        # this feature is temporary to get the user feed back about 
        #unvocalized  collocations
        self.unknown_delimiter  = u"~"
        self.show_delimiter = show_delimiter
        COLLOCATION_DICTIONARY_INDEX = {
        u'id':0, 
        u'vocalized':1, 
        u'unvocalized':2, 
        u'rule':3, 
        u'category':4, 
        u'note':5, 
        }
        #cache of collocations to speedup the process
        self.collo_cache = {}
        # enable and disable _cache use
        self.cache_enabled = True
        #from   dictionaries.verb_dictionary  import *
        self.collo_dict = collocationdictionary.collocationDictionary(
        'collocations', COLLOCATION_DICTIONARY_INDEX)
        for key in cconst.GENERAL_COLLOCATIONS.keys():
            self.collo_cache[key] = \
             cconst.GENERAL_COLLOCATIONS[key]['v']


    def set_min(self, min0):
        """
        set minimum
        """
        # to avoid errers, verify the min
        self.mini = min(min0, self.mini)
        self.maxi = max(min0, self.maxi)        
    def set_max(self, max0):
        """
        set maximum
        """
        # to avoid errers, verify the max
        self.mini = min(max0, self.mini)
        self.maxi = max(max0, self.maxi)
    def set_delimiter(self, delimiter):
        """
        set the delimiter for collocations output
        @param delimiter : the given delimiter.
        @type delimiter : one unicode char.
        """
        self.delimiter = delimiter
    def get_delimiter(self):
        """
        get the delimiter used for collocations output
        @return : return the actual delimiter.
        @rtype : one unicode char.
        """
        return self.delimiter
    def set_unknown_delimiter(self, delimiter):
        """
        set the delimiter for unvocalized collocations output
        @param delimiter : the given delimiter.
        @type delimiter : one unicode char.
        """
        self.unknown_delimiter = delimiter
    def get_unknown_delimiter(self):
        """
        get the  unknown delimiter used for collocations output
        @return : return the actual unknown delimiter.
        @rtype : one unicode char.
        """
        return self.unknown_delimiter

    def enable_show_delimiter(self):
        """
        Enable the option to show collocation delimiters
        """
        self.show_delimiter = True

    def disable_show_delimiter(self):
        """
        Enable the option to show collocation delimiters
        """
        self.show_delimiter = False

    def enable_cache(self):
        """
        Enable the option to enable cache
        """
        self.cache_enabled = True

    def disable_cache(self):
        """
        disable the option to show collocation delimiters
        """
        self.cache_enabled = False
    def get_show_delimiter(self):
        """
        get the show delimimter state
        @return : return the actual state of collocation delimiter show.
        @rtype : Boolean.
        """
        return self.show_delimiter

    def is_collocated(self, wordlist):
        """
        Return The vocalized text if the word list is collocated.
        @param wordlist: word of list, 2 or more words.
        @type wordlist: list of unicode.
        @return : The collocation as a key if exists. else False.
        @rtype: dict/None.
        """
        # The fisrt case is the two words collocation

        # get two element from the list start
        key = u' '.join(wordlist)
        
        if len(wordlist)<2:
            return False
        elif len(wordlist)>2:
            # the more than 2 words collocations are a small list 
            # mentioned in Gcconst.GENRAL_COLLOCATIONS
            # key = u' '.join(wordlist)            
            if self.cache_enabled and self.collo_cache.has_key(key): 
                return key
        elif  not cconst.token_pat.search(key) :
        # invalid words
            return False    
        else:
            # get two element from the list start
            key = u' '.join(wordlist)
            # if the key existss in the cache.
            if self.cache_enabled and self.collo_cache.has_key(key): 
                return key            
            
            #print key.encode('utf8')
            idlist = self.collo_dict.lookup(key)
            # if the wordlist as key existes in collocation database, 
            # insert its vocalization in a collocation cache dict
            if len(idlist) >= 1 :
                if self.cache_enabled and not self.collo_cache.has_key(key): 
                    first_entry = idlist[0]
                    self.collo_cache[key] =  first_entry['vocalized'] 
                return key
            else:
                #before return false we can strip samm prefix from the clause
                # for example : الحمد لله
                # is a collocation, , but بالحمد لله is not found
                if key[0] in (araby.FEH, araby.WAW, araby.BEH, araby.LAM,
                 araby.KAF):
                    first_letter = key[0]
                    new_key = key[1:]
                    #print key.encode('utf8')
                    #look up for the new key
                    idlist = self.collo_dict.lookup(new_key)
                    # if the wordlist as key existes in collocation data base, 
                    # insert its vocalization in a collocation cache dict
                    if len(idlist) >= 1 :
                        if self.cache_enabled and not \
                        self.collo_cache.has_key(key):
                            vocalized_collocation = idlist[0]['vocalized']
                            # some fields in database are not vocalized
                            if vocalized_collocation != "":
                                # save the variant of collocation also, by key
                                self.collo_cache[key] = first_letter + \
                                vocalized_collocation
                            else: 
                                # if vocalized is empty, save a empty 
                                #string in cache
                                # if the returned string is empty the program 
                                #suggest to vocalized the collocation
                                self.collo_cache[key] = vocalized_collocation

                            # save the found collocation in cache by new_key
                                if not self.collo_cache.has_key(new_key):
                                    self.collo_cache[new_key] = \
                                    vocalized_collocation
                            
                        # return the given key
                        return key

                    else: return False
                return False        
        return False

    def ngramfinder(self, mini, liste):
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
        newlist = []
        while len(liste) >= mini:
            sublist = []
            for i in range(mini):
                current = liste.pop()
                # if araby.isArabicword(current):
                sublist.insert(0, current)
                # else:
                    # sublist = []
                    # break
            if sublist:
                result = self.is_collocated(sublist)
                if result:
                    newlist.append(result)
                else:
                    newlist.append(sublist.pop())
                    liste.extend(sublist)
        # rest element
        liste.reverse()
        newlist.extend(liste)
        newlist.reverse()
        return newlist

    def lookup4long_collocations(self, inputtext):
        """
        Lookup for long collocations in a text.
        return a  vocalized words collocations.
        @param inputtext: given text
        @type inputtext:  unicode.
        @return : text.
        @rtype: unicode.
        """
        for k in cconst.GENERAL_COLLOCATIONS.keys():
            inputtext = re.sub( k, cconst.GENERAL_COLLOCATIONS[k].get('v', 
            ''), inputtext )
        return inputtext

    def lookup(self, wordlist):
        """
        Lookup for all ngrams , in the word list.
        return a list of vocalized words collocations.
        @param wordlist: word of list, 2 or more words.
        @type wordlist: list of unicode.
        @return : dict of words attributes like dict {'vocalized':
        vocalizedword list, 'category': categoryOf_collocation}. else False.
        @rtype: dict of dict /None.
        """
        #lookup for collocation from max number to min number of 
        # words in the collocation
        i = self.maxi
        collolist = wordlist
        while i >= self.mini: 
            collolist =  self.ngramfinder(i, collolist)
            #print repr(collolist)
            i -= 1
        #Get the list of single words and collocations
        #collolist = self.ngrams(self.min, self.max, wordlist)
        ##collodict = {}
        newlist = []
        #print repr(self.collo_cache)
        for item in collolist:
            if self.collo_cache.has_key(item):
                vocalized = self.collo_cache[item]
                #lookup for collocations in dictionary
                # the dictionary conatins the vocalized collocation, 
                # but it contains also a list of collocations 
                # non vocalized yet, 
                # this 'vocalized value is empty, then we use this 
                # feature to collect the user feed back and correction
                if vocalized != u"":
                    # if the vocalization is vocalized, we don't mention it
                    # newlist.append(u"'"+vocalized+u"'")
                    if self.get_show_delimiter():
                        newlist.append(u''.join([self.get_delimiter(), 
                        item, self.get_delimiter()]))
                    else:
                        newlist.append(vocalized)                    
                else:
                    # ig the collocation isn't vocalized, we delemeit 
                    #it by ~, to collect corrections.
                    if self.get_show_delimiter():
                        newlist.append(u''.join([self.get_unknown_delimiter(), 
                        item, self.get_unknown_delimiter()]))                
                    else:
                        newlist.append(item)                        
            else:
                newlist.append(item)
        return newlist
    def is_possible_collocation(self, list2, context = "", lenght = 2):
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
            return 0
        else:
            item_v1 = list2[0]
            item_v2 = list2[1]
            item1 = araby.strip_tashkeel(item_v1)
            item2 = araby.strip_tashkeel(item_v2)        
            #if item1[-1:] in (u".", u"?", u", ", u'[', u']', u'(', ')'):
            #    return 0
            if  not cconst.token_pat.search(item1) or not \
            cconst.token_pat.search(item2) :
                return -1
            #else: return 100
            elif item1 in cconst.ADDITIONAL_WORDS :
                return 10
            elif item1 in cconst.NAMED_PRIOR :
                return 15            
            elif (item2 not in cconst.SPECIAL_DEFINED):
                if  item2.startswith(u'ال') and  item1.startswith(u'ال'):
                    return 20
                elif item1.endswith(u'ة') and item2.startswith(u'ال'):
                    return 30

                #حالة الكلمات التي تبدأ بلام الجر والتعريف 
                # لا داعي لها لأنها دائما مجرورة
                #if  item2.startswith(u'لل'):
                #    return 40
                elif item1.endswith(u'ة') and item2.endswith(u'ة')  :
                    return 40
                #if item1.endswith(u'ي') and item2.endswith(u'ي'):
                #    return 60

                elif  context != u"" and context in cconst.tab_noun_context \
                and item2.startswith(u'ال') :
                    return 50
                #return True

                elif item1.endswith(u'ات') and item2.startswith(u'ال') :
                    return 60
            return 100

def mainly():
    """
    main test """
    collocationdictionary.FILE_DB = u"data/collocations.sqlite"
    collo = _collocationClass()
    wordlist = [u"قبل", u"صلاة", u"الفجر", u"كرة", u"القدم",
     u"في", u"دولة", u"قطر", u"الآن", u"أن"]
    words = u"""تغمده الله برحمته . أشهد أن لا إله إلا الله وحده لا
     شريك له . أشهد أن محمدا عبده ورسوله .
 صلى الله عليه وآله وصحبه وسلم . أشهد أن لا إله إلا الله .
 أشهد أن محمدا رسول الله . صلى الله عليه وسلم
      .
    """
    words += u"""والحمد لله . الحمد لله . بالحمد لله .
 بسم الله الرحمن الرحيم . عبد الله . بعبد الله ."""
    words += u"بسم الله الرحمن الرحيم"
    words += u"  taha zerrouki "
    wordlist = words.split(' ')
    collo.set_delimiter('#')
    collo.set_unknown_delimiter('@')    
    collo.enable_show_delimiter()
    # collo.disable_cache()    
    #~import re
    for i in range(1):
        newlist = collo.lookup(wordlist)
        print i, u'\t'.join(newlist).encode('utf8')
    inputtext = words
    for k in cconst.GENERAL_COLLOCATIONS.keys():
        print k.encode('utf8'), \
        cconst.GENERAL_COLLOCATIONS[k].get('v', '').encode('utf8')
        if k in inputtext:
            print  'ok'
        inputtext = re.sub( k, cconst.GENERAL_COLLOCATIONS[k].get('v', ''),
         inputtext )

    #~ txt  = collo.lookup4long_collocations(words)
    print "long collo, ", inputtext.encode('utf8')    
    
    
#Class test
if __name__ == '__main__':
    mainly()
