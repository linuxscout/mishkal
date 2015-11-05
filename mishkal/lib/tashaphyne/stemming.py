# -*- coding: UTF-8 -*-
"""
Arabic Light Stemmer: a class which provides a configurable stemmer 
and segmentor for arabic text.

Features:
 == == == == = 
    - Arabic word Light Stemming.
    - Root Extraction.
    - Word Segmentation
    - Word normalization
    - Default Arabic Affixes list.
    - An customizable Light stemmer: possibility of change 
    stemmer options and data.
    - Data independent stemmer
Licence:
 == == == ==  
    Author 2010, Taha Zerrouki <taha_zerrouki at gmail dot com>
    Released under terms of Gnu Public License.
    The Latest version of the license can be found on
    "www.gnu.org/copyleft/gpl.html"

"""

import  re, sys
sys.path.append('tashaphyne/lib/')
import pyarabic.araby as araby

import tashaphyne.normalize as normalize
import tashaphyne.stem_const as stem_const


class ArabicLightStemmer:
    """
    ArabicLightStemmer: a class which proved a configurable stemmer
     and segmentor for arabic text.
    """
    def __init__(self):
        #load affix information
        # pass
        self.prefix_letters = stem_const.DEFAULT_PREFIX_LETTERS
        self.suffix_letters = stem_const.DEFAULT_SUFFIX_LETTERS
        self.infix_letters = stem_const.DEFAULT_INFIX_LETTERS
        self.max_prefix_length = stem_const.DEFAULT_MAX_PREFIX
        self.max_suffix_length = stem_const.DEFAULT_MAX_SUFFIX
        self.min_stem_length = stem_const.DEFAULT_MIN_STEM
        self.joker = stem_const.DEFAULT_JOKER
        self.prefix_list = stem_const.DEFAULT_PREFIX_LIST
        self.suffix_list = stem_const.DEFAULT_SUFFIX_LIST
        self.word = u""
        self.unvocalized = u""
        self.normalized = u""
        self.starword = u""
        self.root = u""
        self.left = 0
        self.right = 0
        self.segment_list = []
        #token pattern
        # letters and harakat
        self.token_pat = re.compile(ur"[^\w\u064b-\u0652']+", re.UNICODE)
        self.prefixes_tree = self._create_prefix_tree(self.prefix_list)
        self.suffixes_tree = self._create_suffix_tree(self.suffix_list)        
    ######################################################################
    #{ Attribut Functions
    ######################################################################
    def get_prefix_letters(self, ):
        """ return the prefixation letters.
        This constant take DEFAULT_PREFIX_LETTERS by default.
        @return: return a letters.
        @rtype: unicode.
        """
        return self.prefix_letters

    def set_prefix_letters(self, new_prefix_letters):
        """ set the prefixation letters.
        This constant take DEFAULT_PREFIX_LETTERS by default.
        @param new_prefix_letters: letters to be striped from a word,
         e.g.new_prefix_letters = u"وف":.
        @type new_prefix_letters: unicode.
        """
        self.prefix_letters = new_prefix_letters

    def get_suffix_letters(self, ):
        """ return the suffixation letters.
        This constant take DEFAULT_SUFFIX_LETTERS by default.
        @return: return a letters.
        @rtype: unicode.
        """
        return self.suffix_letters

    def set_suffix_letters(self, new_suffix_letters):
        """ set the suffixation letters.
        This constant take DEFAULT_SUFFIX_LETTERS by default.
        @param new_suffix_letters: letters to be striped from the end of a word,
         e.g.new_suffix_letters = u"ةون":.
        @type new_suffix_letters: unicode.
        """
        self.suffix_letters = new_suffix_letters

    def get_infix_letters(self, ):
        """ get the inffixation letters.
        This constant take DEFAULT_INFIX_LETTERS by default.
        @return: infixes letters.
        @rtype: unicode.
        """
        return self.infix_letters

    def set_infix_letters(self, new_infix_letters):
        """ set the inffixation letters.
        This constant take DEFAULT_INFIX_LETTERS by default.
        @param new_infix_letters: letters to be striped from the middle
         of a word, e.g.new_infix_letters = u"أوي":.
        @type new_infix_letters: unicode.
        """
        self.infix_letters = new_infix_letters


    def get_joker(self, ):
        """ get the joker letter.
        This constant take DEFAULT_JOKER by default.
        @return: joker letter.
        @rtype: unicode.
        """
        return self.joker

    def set_joker(self, new_joker):
        """ set the joker letter.
        This constant take DEFAULT_JOKER by default.
        @param new_joker: joker letter.
        @type new_joker: unicode.
        """
        if len(new_joker)>1:
            new_joker = new_joker[0]
        self.joker = new_joker

    def get_max_prefix_length(self, ):
        """ return the constant of max length of the prefix used by the stemmer.
        This constant take DEFAULT_MAX_PREFIX_LENGTH by default.
        @return: return a number.
        @rtype: integer.
        """
        return self.max_prefix_length

    def set_max_prefix_length(self, new_max_prefix_length):
        """ Set the constant of max length of the prefix used by the stemmer.
        This constant take DEFAULT_MAX_PREFIX_LENGTH by default.
        @param new_max_prefix_length: the new max prefix length constant.
        @type new_max_prefix_length: integer.
        """
        self.max_prefix_length = new_max_prefix_length

    def get_max_suffix_length(self, ):
        """ return the constant of max length of the suffix used by the stemmer.
        This constant take DEFAULT_MAX_SUFFIX_LENGTH by default.
        @return: return a number.
        @rtype: integer.
        """
        return self.max_suffix_length

    def set_max_suffix_length(self, new_max_suffix_length):
        """ Set the constant of max length of the suffix used by the stemmer.
        This constant take DEFAULT_MAX_SUFFIX_LENGTH by default.
        @param new_max_suffix_length: the new max suffix length constant.
        @type new_max_suffix_length: integer.
        """
        self.max_suffix_length = new_max_suffix_length

    def get_min_stem_length(self, ):
        """ return the constant of min length of the stem used by the stemmer.
        This constant take DEFAULT_MIN_STEM_LENGTH by default.
        @return: return a number.
        @rtype: integer.
        """
        return self.min_stem_length

    def set_min_stem_length(self, new_min_stem_length):
        """ Set the constant of min length of the stem used by the stemmer.
        This constant take DEFAULT_MIN_STEM_LENGTH by default.
        @param new_min_stem_length: the min stem length constant.
        @type new_min_stem_length: integer.
        """
        self.min_stem_length = new_min_stem_length

    def get_prefix_list(self, ):
        """ return the prefixes list used by the stemmer.
        This constant take DEFAULT_PREFIX_LIST by default.
        @return: prefixes list.
        @rtype: set().
        """
        return self.prefix_list
    def set_prefix_list(self, new_prefix_list):
        """ Set  prefixes list used by the stemmer.
        This constant take DEFAULT_PREFIX_LIST by default.
        @param new_prefix_list: a set of prefixes.
        @type new_prefix_list: set of unicode string.
        """
        self.prefix_list = new_prefix_list
        self._create_prefix_tree(self.prefix_list)

    def get_suffix_list(self, ):
        """ return the suffixes list used by the stemmer.
        This constant take DEFAULT_SUFFIX_LIST by default.
        @return: suffixes list.
        @rtype: set().
        """
        return self.suffix_list

    def set_suffix_list(self, new_suffix_list):
        """ Set  suffixes list used by the stemmer.
        This constant take DEFAULT_SUFFIX_LIST by default.
        @param new_suffix_list: a set of suffixes.
        @type new_suffix_list: set of unicode string.
        """
        self.suffix_list = new_suffix_list
        self._create_suffix_tree(self.suffix_list)        


    def set_word(self, new_word):
        """ Set the word to treat by the stemmer.
        @param new_word: the new word.
        @type new_word: unicode.
        """
        self.word = new_word

    def get_word(self):
        """ return the last word treated by the stemmer.
        @return: word.
        @rtype: unicode.
        """
        return self.word
    #########################################################
    #{ Calculated Attribut Functions
    #########################################################

    def get_starword(self):
        """ return the starlike word treated by the stemmer.
        All non affix letters are converted to a joker.
        The joker take by default DEFAULT_JOKER = "*".
        Exmaple:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'أفتصربونني'
            >>> stem = ArListem.lightStem(word)
            >>> print ArListem.get_starword()
            أفت***ونني

        @return: word.
        @rtype: unicode.
        """
        return self.starword

    def get_root(self, prefix_index = -1, suffix_index = -1):
        """ return the root of the treated word by the stemmer.
        All non affix letters are converted to a joker.
        All letters in the joker places are part of root.
        The joker take by default DEFAULT_JOKER = "*".
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'أفتصربونني'
            >>> stem = ArListem.lightStem(word)
            >>> print ArListem.get_starword()
            أفت***ونني
            >>> print ArListem.get_root()
            ضرب

        @param prefix_index: indicate the left stemming position
            if = -1: not cosidered, and take the default word prefix lentgh.
        @type prefix_index:integer.
        @param suffix_index:indicate the right stemming position.
            if = -1: not cosidered, and take the default word suffix position.
        @type suffix_index: integer.
        @return: root.
        @rtype: unicode.
        """
        if prefix_index >= 0 or suffix_index >= 0:
            self.extract_root(prefix_index, suffix_index)
        return self.root

    def get_normalized(self):
        """ return the normalized form of the treated word by the stemmer.
        Some letters are converted into normal form like Hamzat.
        Example:
            >>> word = u"استؤجرُ"
            >>> ArListem = ArabicLightStemmer()
            >>> stem = ArListem.lightStem(word)
            >>> print ArListem.get_normalized()
            استءجر

        @return: normalized word.
        @rtype: unicode.
        """
        return self.normalized

    def get_unvocalized(self):
        """ return the unvocalized form of the treated word by the stemmer.
        Harakat are striped.
        Example:
            >>> word = u"الْعَرَبِيّةُ"
            >>> ArListem = ArabicLightStemmer()
            >>> stem = ArListem.lightStem(word)
            >>> print ArListem.get_unvocalized()
            العربية

        @return: unvocalized word.
        @rtype: unicode.
        """
        return self.unvocalized

    def get_left(self):
        """ return the the left position of stemming 
        (prefixe end position )in the word treated word by the stemmer.
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'أفتصربونني'
            >>> stem = ArListem.lightStem(word)
            >>> print ArListem.get_starword()
            أفت***ونني
            >>> print ArListem.get_left()
            3

        @return: the left position of stemming.
        @rtype: integer.
        """
        return self.left

    def get_right(self):
        """ return the the right position of stemming 
        (suffixe start position )in the word treated word by the stemmer.
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'أفتصربونني'
            >>> stem = ArListem.lightStem(word)
            >>> print ArListem.get_starword()
            أفت***ونني
            >>> print ArListem.get_right()
            6

        @return: the right position of stemming.
        @rtype: integer.
        """

        return self.right

    def get_stem(self, prefix_index = -1, suffix_index = -1):
        """ return the stem of the treated word by the stemmer.
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'أفتكاتبانني'
            >>> stem = ArListem.lightStem(word)
            >>> print ArListem.get_stem()
            كاتب

        @param prefix_index: indicate the left stemming position
            if = -1: not cosidered, and take the default word prefix lentgh.
        @type prefix_index:integer.
        @param suffix_index:indicate the right stemming position.
            if = -1: not cosidered, and take the default word suffix position.
        @type suffix_index: integer.
        @return: stem.
        @rtype: unicode.
        """
        if prefix_index < 0:
            left = self.left
        else:
            left = prefix_index
        if suffix_index < 0:
            right = self.right
        else:
            right = suffix_index
        return self.unvocalized[left:right]

    def get_starstem(self, prefix_index = -1, suffix_index = -1):
        """ return the star form stem of the treated word by the stemmer.
        All non affix letters are converted to a joker.
        The joker take by default DEFAULT_JOKER = "*".
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'أفتكاتبانني'
            >>> stem = ArListem.lightStem(word)
            >>> print ArListem.get_stem()
            كاتب
            >>> print ArListem.get_starstem()
            *ات*

        @param prefix_index: indicate the left stemming position
            if = -1: not cosidered, and take the default word prefix lentgh.
        @type prefix_index:integer.
        @param suffix_index:indicate the right stemming position.
            if = -1: not cosidered, and take the default word suffix position.
        @type suffix_index: integer.
        @return: stared form of stem.
        @rtype: unicode.
        """
        if prefix_index < 0 and suffix_index < 0:
            return self.starword[self.left:self.right]
        else:
            left = self.left
            right = self.right
            if prefix_index >= 0:
                left = prefix_index
            if suffix_index >= 0:
                right = suffix_index
            if self.infix_letters != "": 
                newstarstem = re.sub(u"[^%s]"%self.infix_letters, \
                   self.joker, self.starword[left:right])
            else:
                newstarstem = self.joker*len(self.starword[left:right])
                
            return newstarstem

    # def get_prefix(self):
        # return self.unvocalized[:self.left]

    def get_prefix(self, prefix_index = -1):
        """ return the prefix of the treated word by the stemmer.
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'أفتكاتبانني'
            >>> stem = ArListem.lightStem(word)
            >>> print ArListem.get_prefix()
            أفت

        @param prefix_index: indicate the left stemming position
            if = -1: not cosidered, and take the default word prefix lentgh.
        @type prefix_index:integer.
        @return:  prefixe.
        @rtype: unicode.
        """
        if prefix_index < 0:
            return self.unvocalized[:self.left]
        else:
            return self.unvocalized[:prefix_index]


    def get_suffix(self, suffix_index = -1):
        """ return the suffix of the treated word by the stemmer.
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'أفتكاتبانني'
            >>> stem = ArListem.lightStem(word)
            >>> print ArListem.get_suffix()
            انني

        @param suffix_index:indicate the right stemming position.
            if = -1: not cosidered, and take the default word suffix position.
        @type suffix_index: integer.
        @return:  suffixe.
        @rtype: unicode.
        """
        if suffix_index < 0:
            return self.unvocalized[self.right:]
        else:
            return self.unvocalized[suffix_index:]

    def get_affix(self, prefix_index = -1, suffix_index = -1):
        """ return the affix of the treated word by the stemmer.
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'أفتكاتبانني'
            >>> stem = ArListem.lightStem(word)
            >>> print ArListem.get_affix()
            أفت-انني

        @param prefix_index: indicate the left stemming position
            if = -1: not cosidered, and take the default word prefix lentgh.
        @type prefix_index:integer.
        @param suffix_index:indicate the right stemming position.
            if = -1: not cosidered, and take the default word suffix position.
        @type suffix_index: in4teger.
        @return:  suffixe.
        @rtype: unicode.
        """
        return u"-".join([self.get_prefix(prefix_index), \
        self.get_suffix(suffix_index)])

    def get_affix_tuple(self, prefix_index = -1, suffix_index = 0):
        """ return the affix tuple of the treated word by the stemmer.
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'أفتضاربانني'
            >>> stem = ArListem.lightStem(word)
            >>> print ArListem.get_affix_tuple()
            {'prefix': u'أفت', 'root': u'ضرب', 'suffix': u'انني', 'stem': u'ضارب'}

        @param prefix_index: indicate the left stemming position
            if = -1: not cosidered, and take the default word prefix lentgh.
        @type prefix_index:integer.
        @param suffix_index:indicate the right stemming position.
            if = -1: not cosidered, and take the default word suffix position.
        @type suffix_index: integer.
        @return: affix tuple.
        @rtype: dict.
        """
        return {
        'prefix':self.get_prefix(prefix_index), 
        'suffix':self.get_suffix(suffix_index), 
        'stem':self.get_stem(prefix_index, suffix_index), 
        'root':self.get_root(prefix_index, suffix_index), }
    #########################################################
    #{ Stemming Functions
    #########################################################
    def light_stem(self, word):
        u"""
        Stemming function, stem an arabic word, and return a stem.
        This function store in the instance the stemming positions (left, right), then it's possible to get other calculted attributs like : stem, prefixe, suffixe, root.
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'أفتضاربانني'
            >>> stem = ArListem.light_stem(word)
            >>> print ArListem.get_stem()
            ضارب
            >>> print ArListem.get_starstem()
            *ا**
            >>> print ArListem.get_left()
            3
            >>> print ArListem.get_right()
            6
            >>> print ArListem.get_root()
            ضرب

        @param word: the input word.
        @type word: unicode.
        @return: stem.
        @rtype: unicode.
        """
        if word ==  u'':
            return u''
        #~ starword, left, right = self.transform2stars(word)
        self.transform2stars(word)

        #consititute the root
        self.extract_root()
        return self.get_stem()

    def transform2stars(self, word):
        """
        Transform all non affixation letters into a star.
        the star is a joker(by default '*'). 
        which indicates that the correspandent letter is an original.
        this function is used by the stmmer to identify original letters.
         and return a stared form and stemming positions (left, right)
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'أفتضاربانني'
            >>> starword, left, right = ArListem.transformToStrars(word)
            (أفت*ا**انني, 3, 6)

        @param word: the input word.
        @type word: unicode
        @return: (starword, left, right):
            - starword : all original letters converted into a star
            - left : the greater possible left stemming position.
            - right : the greater possible right stemming position.
        @rtype: tuple.
        """
        self.word = word
        word = araby.strip_tashkeel(word)
        # word, harakat = araby.separate(word)
        self.unvocalized = word
        word = re.sub("[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
        word = re.sub("[^%s%s]"%(self.prefix_letters, self.suffix_letters), \
         self.joker, word)
        #~ ln = len(word)
        left = word.find(self.joker)
        right = word.rfind(self.joker)
        if left >= 0:
            left = min(left, self.max_prefix_length-1)
            right = max(right+1, len(word)-self.max_suffix_length)
            prefix = word[:left]
            stem = word[left:right]
            suffix = word[right:]
            prefix = re.sub("[^%s]"%self.prefix_letters, self.joker, prefix)
            # avoid null infixes
            if(self.infix_letters != u""):
                stem = re.sub("[^%s]"%self.infix_letters, self.joker, stem)
            suffix = re.sub("[^%s]"%self.suffix_letters, self.joker, suffix)
            word = prefix+stem+suffix

        left = word.find(self.joker)
        right = word.rfind(self.joker)
        # prefix_list = self.PREFIX_LIST
        # suffix_list = self.SUFFIX_LIST

        if left < 0:
            left = min(self.max_prefix_length, len(word)-2)
        if left >= 0:
            prefix = word[:left]
            while prefix != "" and prefix not in self.prefix_list:
                prefix = prefix[:-1]
            if right < 0:
                right = max(len(prefix), len(word)-self.max_suffix_length)
            suffix = word[right:]

            while suffix != "" and suffix not in self.suffix_list:
                suffix = suffix[1:]
            left = len(prefix)
            right = len(word)-len(suffix)
            stem = word[left:right]
            # convert stem into  stars.
            # a stem must starts with alef, or end with alef.
            # any other infixes letter isnt infixe at the border of the stem.
            #substitute all non infixes letters
            if self.infix_letters != "":
                stem = re.sub("[^%s]"%self.infix_letters, self.joker, stem)

            # substitube teh in infixes the teh mst be in the first 
            # or second place, all others, are converted
            #
            # stem = stem[:2]+re.sub(TEH, self.joker, stem[2:])
            word = prefix+stem+suffix
        # store result
        self.left = left
        self.right = right
        self.starword = word
        self.extract_root()
        # return starword, left, right position of stem
        return (word, left, right)

    def extract_root(self, prefix_index = -1, suffix_index = -1):
        """ return the root of the treated word by the stemmer.
        All non affix letters are converted to a joker.
        All letters in the joker places are part of root.
        The joker take by default DEFAULT_JOKER = "*".
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'أفتصربونني'
            >>> stem = ArListem.lightStem(word)
            >>> print ArListem.get_starword()
            أفت***ونني
            >>> print ArListem.get_root()
            ضرب

        @param prefix_index: indicate the left stemming position
            if = -1: not cosidered, and take the default word prefix lentgh.
        @type prefix_index:integer.
        @param suffix_index:indicate the right stemming position.
            if = -1: not cosidered, and take the default word suffix position.
        @type suffix_index: integer.
        @return: root.
        @rtype: unicode.
        """
    
        starstem = self.get_starstem(prefix_index, suffix_index)
        stem = self.get_stem(prefix_index, suffix_index)
        root = u""
        if len(starstem) ==  len(stem):
            for i in range(len(stem)):
                if starstem[i] ==  self.joker:
                    root +=  stem[i]
        else:
            root = stem
        self.root = root
        return root


    def _create_prefix_tree(self, prefixes):
        """
        Create a prefixes tree from given prefixes list
        @param prefixes: list of prefixes
        @type prefixes: list of unicode
        @return : prefixes tree
        @rtype: Tree stucture
        """
        prefixestree = {}
        for prefix in prefixes:
            # print prefix.encode('utf8')
            branch = prefixestree
            for char in prefix:
                if not branch.has_key(char):
                    branch[char] = {}
                branch = branch[char]
            # branch['#'] = '#' # the hash # as an end postion
            if branch.has_key('#'):
                branch['#'][prefix] = "#"
            else:
                branch['#'] = {prefix:"#", }
        self.prefixes_tree = prefixestree
        return self.prefixes_tree
    def _create_suffix_tree(self, suffixes):
        """
        Create a suffixes tree from given suffixes list
        @param suffixes: list of suffixes
        @type suffixes: list of unicode
        @return : suffixes tree
        @rtype: Tree stucture
        """        
        suffixestree = {}
        for suffix in suffixes:
            # print (u"'%s'"%suffix).encode('utf8')
            branch = suffixestree
            #reverse a string
            for char in suffix[::-1]:
                if not branch.has_key(char):
                    branch[char] = {}
                branch = branch[char]
            # branch['#'] = '#' # the hash # as an end postion
            if branch.has_key('#'):
                branch['#'][suffix] = "#"
            else:
                branch['#'] = {suffix:"#", }
        self.suffixes_tree = suffixestree
        return self.suffixes_tree

    def lookup_prefixes(self, word):
        """
        lookup for prefixes in the word
        @param word: the given word
        @type word: unicode
        @return : list of prefixes starts positions
        @rtype: list of int
        """        
        branch = self.prefixes_tree
        lefts = [0, ]
        i = 0
        while i < len(word) and branch.has_key(word[i]):
            if branch.has_key('#'):
                # if branch['#'].has_key(word[:i]):
                lefts.append(i)
            if branch.has_key(word[i]):
                branch = branch[word[i]]
            else:
                # i +=  1
                break
            i +=  1
        if i < len(word) and branch.has_key('#') :
            lefts.append(i)
        return lefts    


    def lookup_suffixes(self, word):
        """
        lookup for suffixes in the word
        @param word: the given word
        @type word: unicode
        @return : list of suffixes starts positions
        @rtype: list of int
        """
        branch = self.suffixes_tree
        suffix = ''
        # rights = [len(word)-1, ]
        rights = []        
        i = len(word)-1
        while i >= 0 and branch.has_key(word[i]):
            suffix = word[i]+suffix
            if branch.has_key('#'):
                # if branch['#'].has_key(word[i:]):
                    # rights.append(i)
                rights.append(i+1)
            if branch.has_key(word[i]):
                branch = branch[word[i]]
            else:
                # i -=  1
                break
            i -= 1
        if i >= 0 and branch.has_key('#') :#and branch['#'].has_key(word[i+1:]):
            rights.append(i+1)
        return rights
    #########################################################
    #{ Segmentation Functions
    #########################################################

    def segment(self, word):
        """ generate  a list of  all posibble segmentation positions
         (lef, right)  of the treated word by the stemmer.
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'فتضربين'
            >>> print ArListem.segment(word)
            set(([(1, 5), (2, 5), (0, 7)])

        @return: List of segmentation
        @rtype: set of tuple of integer.
        """
        self.word = word
        self.unvocalized = araby.strip_tashkeel(word)
        # word, harakat = araby.separate(word)
        word = re.sub("[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
        
        # get all lefts position of prefixes
        lefts = self.lookup_prefixes(word)
        # get all rights position of suffixes
        rights = self.lookup_suffixes(word)
        if lefts:
            self.left = max(lefts)
        else:
            self.left = -1
        if rights:
            self.right = min(rights)
        else:
            self.right = -1
        #~ ln = len(word)
        self.segment_list = set([(0, len(word))])
        # print lefts, rights
        for i in lefts:
            for j in rights:
                if j >= i+2:
                    self.segment_list.add((i, j))               
        return self.segment_list


    # #########################################################
    # #{ Segmentation Functions
    # #########################################################
    def get_segment_list(self):
        """ return   a list of segmentation positions (left, right) 
         of the treated word by the stemmer.
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'فتضربين'
            >>> ArListem.segment(word)
            >>> print ArListem.get_segment_list()
            set(([(1, 5), (2, 5), (0, 7)])

        @return: List of segmentation
        @rtype: set of tuple of integer.
        """
        return self.segment_list


    def get_affix_list(self, ):
        u""" return   a list of affix tuple of the treated word by the stemmer.
        Example:
            >>> ArListem = ArabicLightStemmer()
            >>> word = u'فتضربين'
            >>> ArListem.segment(word)
            >>> print ArListem.get_affix_list()
            [{'prefix': u'ف', 'root': u'ضرب', 'suffix': u'\u064aن', 'stem': u'تضرب'}, 
            {'prefix': u'فت', 'root': u'ضرب', 'suffix': u'\u064aن', 'stem': u'ضرب'}, 
            {'prefix': u'', 'root': u'فضربن', 'suffix': u'', 'stem': u'فتضرب\u064aن'}]

        @return: List of Affixes tuple
        @rtype: list of dict.
        """
        affix_list = []
        for  item in self.segment_list:
            affix_list.append(self.get_affix_tuple(item[0], item[1]))
        return affix_list


    ###############################################################
    #{ General Functions
    ###############################################################

    def normalize(self, word = u""):
        """
        Normalize a word.
        Convert some leters forms into unified form.
        @param word: the input word, if word is empty, 
        the word member of the class is normalized.
        @type word: unicode.
        @return: normalized word.
        @rtype: unicode.
        """

        if word ==  u'' and self.word ==  u"":
            return u""
        elif word != u'':
            self.word = word
        else:
            word = self.word
        self.normalized = normalize.normalize_searchtext(word)
        return self.normalized

    def tokenize(self, text = u""):
        """
        Tokenize text into words
        @param text the input text.
        @type text: unicode.
        @return: list of words.
        @rtype: list.
        """
        if not text :
            return []
        else:
            mylist = self.token_pat.split(text)
            if u'' in mylist:
                mylist.remove(u'')
            return mylist
