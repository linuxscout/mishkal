#!/usr/bin/python
# -*- coding=utf-8 -*-

#------------------------------------------------------------------------
# Name:        dconst.py
# Purpose:     Arabic lexical analyser constants used for disambiguation
# before analysis
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-----------------------------------------------------------------------
"""
A class to remove ambiguation in text analysis
"""
if __name__ == "__main__":
    import sys
    sys.path.append('../')
    sys.path.append('../support')

import qalsadi.disambig_const as dconst
import naftawayh.wordtag


class Disambiguator:
    """
    A class to remove ambiguation in text analysis
    """

    def __init__(self, ):
        self.tagger = naftawayh.wordtag.WordTagger()

    def disambiguate_words(self, word_list, tag_list):
        """
        Disambiguate some word according to tag guessing to reduce cases.
        return word list with dismbiguate.
        @param word_list: the given word lists.
        @type word_list: unicode list.
        @param tag_list: the given tag lists, produced by naftawayh
        @type tag_list: unicode list.
        @return: a new word list
        @rtype: unicode list
        """
        # print u" ".join(word_list).encode('utf8');
        # print u" ".join(tag_list).encode('utf8');

        if not word_list or len(word_list) != len(tag_list):
            #print "error"
            return word_list
        else:
            newwordlist = []
            wordtaglist = zip(word_list, tag_list)
            # print wordtaglist
            for i, wordtag in enumerate(wordtaglist):
                currentword = wordtag[0]
                # if the current exists in disambig table,
                if self.is_ambiguous(currentword):
                    if i - 1 >= 0:
                        previousword = wordtaglist[i - 1][0]
                    else:
                        previousword = ""
                    # disambiguate the word according the previous  word
                    tmpword = self.get_disambiguated_by_prev_word(
                        currentword, previousword)
                    if tmpword != currentword:
                        currentword = tmpword
                    elif i + 1 < len(wordtaglist):
                        #print "*5"
                        nexttag = wordtaglist[i + 1][1]
                        #~ nextword = wordtaglist[i + 1][0]
                        # if the next is similar to the expected tag,
                        # return vocalized word form
                        # test if expected tag is verb and
                        if self.tagger.is_verb_tag(nexttag) and \
                        self.is_disambiguated_by_next_verb(currentword):
                            currentword = \
                            self.get_disambiguated_by_next_verb(currentword)
                        elif (self.tagger.is_noun_tag(nexttag) and
                              self.is_disambiguated_by_next_noun(currentword)):
                            currentword = self.get_disambiguated_by_next_noun(
                                currentword)
                newwordlist.append(currentword)
            return newwordlist
    @staticmethod
    def is_ambiguous(word):
        """ test if the word is an ambiguous case
        @param word: input word.
        @type word: unicode.
        @return : if word is ambiguous
        @rtype: True/False.
        """
        return word in dconst.DISAMBIGUATATION_TABLE

    @staticmethod
    def get_disambiguated_by_next_noun(word):
        """ get The disambiguated form of the word by the next word is noun.
        The disambiguated form can be fully or partially vocalized.
        @param word: input word.
        @type word: unicode.
        @return : if word is ambiguous
        @rtype: True/False.
        """
        return dconst.DISAMBIGUATATION_TABLE.get(word, {}).get('noun', \
         {}).get('vocalized', word)

    @staticmethod
    def get_disambiguated_by_prev_word(word, previous):
        """ get The disambiguated form of the word by the previous.
        The disambiguated form can be fully or partially vocalized.
        @param word: input word.
        @type word: unicode.
        @param previous: input previous word.
        @type previous: unicode.
        @return : if word is ambiguous
        @rtype: True/False.
        """
        return dconst.DISAMBIGUATATION_TABLE.get(word, {}).get('previous', \
         {}).get(previous, word)

    @staticmethod
    def get_disambiguated_by_next_word(word, w_next):
        """ get The disambiguated form of the word by the next.
        The disambiguated form can be fully or partially vocalized.
        @param word: input word.
        @type word: unicode.
        @param next: input next word.
        @type next: unicode.
        @return : if word is ambiguous
        @rtype: True/False.
        """
        return dconst.DISAMBIGUATATION_TABLE.get(word, {}).get('next', \
         {}).get(w_next, word)
    @staticmethod
    def get_disambiguated_by_next_verb(word):
        """ get The disambiguated form of the word by the next word is a verb.
        The disambiguated form can be fully or partially vocalized.
        @param word: input word.
        @type word: unicode.
        @return : if word is ambiguous
        @rtype: True/False.
        """
        return dconst.DISAMBIGUATATION_TABLE.get(word, {}).get('verb', \
        {}).get('vocalized', word)
    @staticmethod
    def is_disambiguated_by_next_noun(word):
        """ test if the word can be disambiguated if the next word is a noun
        @param word: input word.
        @type word: unicode.
        @return : if word has an disambiguated.
        @rtype: True/False.
        """
        return dconst.DISAMBIGUATATION_TABLE.get(word, {}).has_key('noun')
    @staticmethod
    def is_disambiguated_by_next_verb(word):
        """ test if the word can be disambiguated if the next word is a verb
        @param word: input word.
        @type word: unicode.
        @return : if word has an disambiguated.
        @rtype: True/False.
        """
        return dconst.DISAMBIGUATATION_TABLE.get(word, {}).has_key('verb')


def mainly():
    """
    MAin test
    """
    text = u"   السلام أن العبادي كان أعلن فتح المنطقة أن السلام مفيد أن يركبوا"
    # tokenize the text
    wordlist = text.split(' ')
    # create the disambiguator instance
    disamb = Disambiguator()
    # tag the word list
    taglist = disamb.tagger.word_tagging(wordlist)
    print("\t".join(taglist))
    newwordlist = disamb.disambiguate_words(wordlist, taglist)
    print(u" ".join(newwordlist).encode('utf8'))


if __name__ == "__main__":
    mainly()
