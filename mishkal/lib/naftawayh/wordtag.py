#!/usr/bin/python
# -*- coding=utf-8 -*-
"""
Arabic Word Type Guessing:
This class can identify the type of word (noun, verb, prepostion).
"""
import re
import string
if __name__ == "__main__":
	import sys
	sys.path.append('../');
	sys.path.append('lib');	
import tashaphyne
import stopwords
#
#from arabic_const import *
#from ar_ctype import *
import pyarabic.araby as araby
import  affix_const
import wordtag_const

class WordTagger():
    """
    Arabic Word type Guessing
    """
    def __init__(self,):
        self.word=u"";
        self.verbstemmer=tashaphyne.ArabicLightStemmer();
        # prepare the verb stemmer
    	verb_prefix=u"أسفلونيتا"
    	verb_infix=u"اتويدط"
    	verb_suffix=u"امتةكنهوي"
    	verb_max_prefix=4
    	verb_max_suffix=6
        self.verbstemmer.set_max_prefix_length(verb_max_prefix);
        self.verbstemmer.set_max_suffix_length(verb_max_suffix);
        self.verbstemmer.set_prefix_letters(verb_prefix);
        self.verbstemmer.set_suffix_letters(verb_suffix);
        self.verbstemmer.set_prefix_list(affix_const.VERBAL_PREFIX_LIST);
        self.verbstemmer.infix_letters=verb_infix;
        # prepare the noun stemmer
        self.nounstemmer=tashaphyne.ArabicLightStemmer();
        noun_prefix=u"مأسفلونيتاكب"
    	noun_infix=u"اتويدط"
    	noun_suffix=u"امتةكنهوي"
    	noun_max_prefix=4
    	noun_max_suffix=6

        self.nounstemmer.set_max_prefix_length(noun_max_prefix);
        self.nounstemmer.set_max_suffix_length(noun_max_suffix);
        self.nounstemmer.set_prefix_letters(noun_prefix);
        self.nounstemmer.set_suffix_letters(noun_suffix);
        self.nounstemmer.set_prefix_list(affix_const.NOMINAL_PREFIXES_LIST);
        self.nounstemmer.infix_letters=noun_infix;
        self.Cache={}; # a cache to speed up the tagging process
		
		# prepare verb pattern
	def __del__(self):
		"""
		Delete instance and clear cache
		
		"""
        self.Cache={}
    def is_noun(self,word):
        """
        Return True if the word is a possible noun form

        @param word: word.
        @type word: unicode.
        @return: is a noun or not
        @rtype: Boolean
        """
        if word in wordtag_const.FixedNouns: return True;		
        if self.is_possible_noun(word)>0:
            return True;
        else:
            return False;

    def is_verb(self,word):
        """
        Return True if the word is a possible verb form

        @param word: word.
        @type word: unicode.
        @return: is a noun or not
        @rtype: Boolean
        """
        if word in wordtag_const.FixedNouns: return False;
        if self.is_possible_verb(word)>0:
            return True;
        else:
            return False;
    def isStopWordTag(self, guessedTag):
        """
        decode guessed Tag, to tell if the word is stopword, not noun or verb
        @param guessedTag: the given word tag.  't': tool, 'v': verb, 'n' :noun, 'nv' or 'vn' unidentifed.
        @type guessedTag: unicode .
        @return: if is stopword or not.
        @rtype: boolean 
        """
        return  guessedTag=='t';
    def isVerbTag(self, guessedTag):
        """
        decode guessed Tag, to tell if the word is verb, not noun
        @param guessedTag: the given word tag.  't': tool, 'v': verb, 'n' :noun, 'nv' or 'vn' unidentifed.
        @type guessedTag: unicode .
        @return: if is verb or not.
        @rtype: boolean 
        """
        return  guessedTag=='v';

        
    def isNounTag(self, guessedTag):
        """
        decode guessed Tag, to tell if the word is noun , not a verb
        @param guessedTag: the given word tag.  't': tool, 'v': verb, 'n' :noun, 'nv' or 'vn' unidentifed.
        @type guessedTag: unicode .
        @return: if is noun or not.
        @rtype: boolean 
        """
        return guessedTag=='n';

    def hasVerbTag(self, guessedTag):
        """
        decode guessed Tag, to tell if the word has a verb tag or not
        @param guessedTag: the given word tag.  't': tool, 'v': verb, 'n' :noun, 'nv' or 'vn' unidentifed.
        @type guessedTag: unicode .
        @return: if is verb or not.
        @rtype: boolean 
        """
        return ('v' in  guessedTag or guessedTag=='');

        
    def hasNounTag(self, guessedTag):
        """
        decode guessed Tag, to tell if the word has a noun tag or not
        @param guessedTag: the given word tag.  't': tool, 'v': verb, 'n' :noun, 'nv' or 'vn' unidentifed.
        @type guessedTag: unicode .
        @return: if is noun or not.
        @rtype: boolean 
        """
        return ('n' in  guessedTag or guessedTag=='');

    def is_possible_noun(self,word):
        """
        Return True if the word is a possible noun form
        This function return True, if the word is valid, else, return False

        @param word: word.
        @type word: unicode.
        @return: error code : indicate the id of the rules aplied. Negative, if not a verb
        @rtype: integer
        """

    	self.verbstemmer.lightStem(word);
    	starword=self.verbstemmer.get_starword();
    	#print starword.encode('utf8')
    	word_nm=self.verbstemmer.get_unvocalized();
    	guessed_word=self.guess_stem(word_nm)
    	

    # HAMZA BELOW araby.ALEF
    	if wordtag_const.verbPattern[100].search(word):
             return 100;
    # case of more than 5 original letters, a verb can't have more then 4 letters root.
    # أية كلمة بها أكثر من 5 حروف أصلية ليست فعلا لانّ الافعال جذورها لا تتعدى أربعة
    	if starword.count('*')>4: 
    	    return 210
    	elif wordtag_const.verbPattern[121].search(word):
             return 121;
    # the word ends with wa  a is  araby.WAW  araby.ALEF , is a verb
    	if wordtag_const.verbPattern[160].search(starword) :
    	    return -160;

    # the word is started by  araby.NOON , before REH or araby.LAM, or  araby.NOON , is a verb and not a noun
    	if wordtag_const.verbPattern[10].match(word_nm):

    		return -10;
    # the word is started by  araby.YEH,
    # before some letters is a verb and not a noun
    	if wordtag_const.verbPattern[20].match(word_nm):

    		return -20;

	# ro do verify this case,
	# هذه الحالة تتناقض مع حالة الاستفعال في الأسماء
	#يمكن حلها بضبط عدد النجوم إلى ثلاثة
    #the word is like inf3l pattern
    	#print starword.encode('utf8');
    	if starword.count('*')==3 and wordtag_const.verbPattern[30].search(starword):

    		return -30;
    # the word is like ift3l pattern
    	if starword.count('*')==3 and wordtag_const.verbPattern[40].search(starword):

    		return -40;
    # the word is like isf3l pattern
    	if starword.count('*')<=3 and wordtag_const.verbPattern[50].search(word_nm):

    		return -50;
    # the word contains y|t|A)st*
    # يست، أست، نست، تست
    	if starword.count('*')<=3 and wordtag_const.verbPattern[60].search(starword) :

    		return -60;
    # the word contains ist***
    # استفعل
    	if wordtag_const.verbPattern[70].search(starword) :

    		return -70;

    # the word contains ***t when **+t+* t is  araby.TEH 
    # if  araby.TEH  is followed by  araby.MEEM , araby.ALEF,  araby.NOON 
    # تم، تما، تن، تا، تني
    # حالة تنا غير مدرجة
    	if wordtag_const.verbPattern[80].search(starword) :

    		return -80;

    #To reDo
    ### case of ***w  w is  araby.WAW , this case is a verb,
    ### the case of ***w* is a noun
    ##	if wordtag_const.verbPattern[].search(u"\*\*\*%s[^\*%s]"%( araby.WAW , araby.NOON ),starword):
    ##		if starword.count("*")==3:
    ##
    ##		  return -90;
    ##		else:
    ##		  if wordtag_const.verbPattern[].search(u"\*\*\*\*%s%s"%( araby.WAW ,araby.ALEF),starword):
    ##		    return -100;

    # case of future verb with  araby.WAW   araby.NOON ,
    	if wordtag_const.verbPattern[110].search(starword):
    	    return -110;
    # case of future verb with araby.ALEF  araby.NOON ,
    	if wordtag_const.verbPattern[115].search(starword):
    	    return -115;

    # case of yt,tt,nt and 3 stars is a verb like yt*** or yt*a**
    # at is an ambiguous case with hamza of interogation.
    	if wordtag_const.verbPattern[120].search(starword):
    	    return -120;
    # case of yn,tn,nn and 3 stars is a verb like yn*** or yn*a* or ynt**

    	if wordtag_const.verbPattern[130].search(starword):

    	    return -130;
    # case of y***, y
    # exception ; case of y**w*
    	if wordtag_const.verbPattern[140].search(starword):

    	    return -140;
# To do
# لا تعمل مع كلمة البرنامج
##    # the word contains a****  a is araby.ALEF is a verb
##    	if wordtag_const.verbPattern[].search(ur"^([^\*])*%s(\*\*\*\*)"%(araby.ALEF),starword) :
##
##    	    return -150;

    # the word has suffix TM ( araby.TEH   araby.MEEM )  and two original letters at list, is a verb
    	if wordtag_const.verbPattern[170].search(starword) and starword.count("*")>=2 :
    	    return -170;
    # the word ends with an added  araby.TEH 
    	if wordtag_const.verbPattern[180].search(guessed_word):
    	    return -180;
    # the word starts with  an added  araby.YEH
    	if wordtag_const.verbPattern[190].search(guessed_word):
    	    return -190;
    # the word starts with   araby.TEH  and ends with  araby.TEH  not araby.ALEF  araby.TEH .
    	if wordtag_const.verbPattern[200].search(starword) :
    	    return -200;
    	return 100;
    #---------------------------------------
    def is_possible_verb(self,word):
        """
        Return True if the word is a possible verb form
        This function return True, if the word is valid, else, return False
        A word is not valid verb if :
          - minimal lenght : 3
          - starts with araby.ALEF_MAKSURA,  araby.WAW_HAMZA, araby.YEH_HAMZA,
            HARAKAT
          - contains :  araby.TEH_MARBUTA
          - contains  araby.ALEF_MAKSURA at the began or middle.
          - contains : double haraka : a warning
          - contains : araby.ALEF_HAMZA_BELOW
          - contains: tanween
        @param word: word.
        @type word: unicode.
        @return: error code : indicate the id of the rules aplied. Negative, if not a verb
        @rtype: integer
        """

    	self.nounstemmer.lightStem(word);
    	starword=self.nounstemmer.get_starword();
    	word_nm=self.nounstemmer.get_unvocalized();
    # ~	#print 'v',starword.encode('utf8')
    ##	word_nm=araby.stripTashkeel_keepshadda(word);
        # affixed starword, is a which we srip affix and not derived,
        # for example  araby.MEEM  is not an affix, but is a deiveitional letter
        # تنزع السوابق الالتصاقية مثل بال، ولا تنزع السوابق الاشتقاقية مثل مست

##    	affixed_noun_prefix=u"أفلواكب"
##    	affixed_noun_infix=u"اتوي"
##    	affixed_noun_suffix=u"امتةكنهوي"
##    	affixed_noun_max_prefix=4
##    	affixed_noun_max_suffix=6
##    	affixed_starword,affixed_left,affixed_right=self.nounstemmer.transformToStars(word);

    # case of more than 5 original letters, a verb can't have more then 4 letters root.
    # أية كلمة بها أكثر من 5 حروف أصلية ليست فعلا لانّ الافعال جذورها لا تتعدى أربعة
    	if starword.count('*')>4: 
    	    return -2010
    	if wordtag_const.nounPattern[1000].search(word):
             return -1000;

    # HAMZA BELOW araby.ALEF
    	elif wordtag_const.nounPattern[1010].search(word):
             return -1010;

    	elif wordtag_const.nounPattern[1020].search(word):
             return -1020;

    # the word is like ift3al pattern
    	elif wordtag_const.nounPattern[1030].match(word_nm):
    	   return -1030;
    # the word is like inf3al pattern
    	elif wordtag_const.nounPattern[1040].match(word_nm):
    	   return -1040;

    # the word is like isf3al pattern
    	elif wordtag_const.nounPattern[1050].match(word_nm):
    	   return -1050;

    # the word is finished by HAMZA preceded by araby.ALEF
    #and more than 2 originals letters
    	elif wordtag_const.nounPattern[1060].match(word_nm):
    	   return -1060;

    # the word contains three araby.ALEF,
    # the kast araby.ALEF musn't be at end
    	if wordtag_const.nounPattern[1070].match(word_nm):
    	   return -1070;

    # the word is started by beh, before BEH,FEH, araby.MEEM 
    #is a noun and not a verb
    	if wordtag_const.nounPattern[1080].match(word_nm):
    	   return -1080;

    # the word is started by  araby.MEEM , before BEH,FEH, araby.MEEM 
    #is a noun and not a verb
    	if wordtag_const.nounPattern[1090].match(word_nm):
    	   return -1090;

    # the word is started  by araby.ALEF araby.LAM
    # and the  original letters are more than two,
    	if wordtag_const.nounPattern[1120].match(word_nm) or wordtag_const.nounPattern[1121].match(word_nm):
    	   min=word_nm.find(araby.ALEF+araby.LAM);
    	   if min<0: min=word_nm.find(araby.LAM+araby.LAM);
    	   min+=2;
    	   if min<len(word_nm):
    	       suffixes=u"امتةكنهوي"
    	       infixes=u"اتوي";
    	       word_nm2=word_nm[min:]
    	       word_nm2=re.sub(u"[^%s]"%suffixes, '*',word_nm2)
    #the  araby.MEEM  is suffixes if is preceded by araby.HEH or araby.KAF
    	       word_nm2=re.sub(u"(?<!(%s|%s|%s))%s"%(araby.KAF,araby.HEH, araby.TEH , araby.MEEM ), '*',word_nm2)
    	       max=word_nm2.rfind('*');
    	       if max>=0:
    	           word_nm2=word_nm2[:max+1]
    	           word_nm2=re.sub(ur"[^%s]"%infixes, '*',word_nm2)
    	       if word_nm2.count('*')>=3:
    	           return -1120;
    	       if word_nm2.find(u'*%s*'%araby.ALEF)>=0:
    	           return -1130;
    # case of  araby.MEEM  has three original letters in folloing
    	# print starword.encode('utf8');
    	if wordtag_const.nounPattern[1140].search(starword) and starword.count('*')>=3:
    	   return -1140;

    # case of  araby.MEEM  folowed by t,  araby.NOON , st, has two original letters in folloing
    	if wordtag_const.nounPattern[1145].search(starword) and starword.count('*')>=2:
    	   return -1145;


    # the word is finished by araby.ALEF  araby.TEH 
    # and the  original letters are more than two,
    	if wordtag_const.nounPattern[1150].search(starword) and starword.count('*')>=3:
    	           return -1150;

    # the word contains **Y* when y is  araby.YEH
    	if wordtag_const.nounPattern[1160].search(starword) :
    	    return -1160;

    # the word contains al*Y* when araby.ALEF-araby.LAM+*+ araby.YEH+*is  araby.YEH
    	if wordtag_const.nounPattern[1170].search(starword) :
    	    return -1170;

    # the word contains al*w* when araby.ALEF-araby.LAM+*+ araby.WAW +*  w is  araby.WAW 
    	if wordtag_const.nounPattern[1180].search(starword) :
    	    return -1180;

    # the word contains ***w* when ***+ araby.WAW +* w is  araby.WAW 
    	if wordtag_const.nounPattern[1190].search(starword) :
    	    return -1190;

    # the word contains **a* when **+a+* a is araby.ALEF
    	if wordtag_const.nounPattern[1200].search(starword) :
    	    return -1200;

    # the word contains t**y* when **+t+* a is araby.ALEF
    	if wordtag_const.nounPattern[1210].search(starword) :
    	    return -1210;

    # case of word ends  with araby.ALEF  araby.NOON , if it hasnt  araby.YEH or  araby.TEH  on prefix
    	if wordtag_const.nounPattern[1220].search(starword) and wordtag_const.nounPattern[1221].search(starword) and starword.count("*")>=2:
    	    return -1220;

    # case of word ends  with  araby.WAW   araby.NOON , if it hasnt  araby.YEH or  araby.TEH  on prefix
    	if wordtag_const.nounPattern[1230].search(starword) and wordtag_const.nounPattern[1231].search(starword) and starword.count("*")>=2:
    	    return -1230;

    # case of word ends  with  araby.YEH  araby.NOON , if it hasnt  araby.YEH or  araby.TEH  on prefix
    	if wordtag_const.nounPattern[1232].search(starword) and wordtag_const.nounPattern[1233].search(starword) and starword.count("*")>=2:
    	    return -1230;

    # the word is finished by  araby.WAW - araby.NOON , araby.ALEF- araby.NOON ,  araby.YEH- araby.NOON , and not started by araby.ALEF_HAMZA_ABOVE or  araby.YEH or  araby.TEH  or  araby.NOON ,
    # and the stem length is more than 2 letters
    # and not have verb prefixes  araby.WAW , FEH, araby.LAM, araby.SEEN 

    #ToDo 2 avoid فكان وفزين cases
    	if wordtag_const.nounPattern[1100].match(word_nm):
    	   if not wordtag_const.nounPattern[1101].match(word_nm):
    	       return -1100;
    	return 200; 

    def guess_stem(self,word):
        """
        Detetect affixed letters based or phonetic root composition.
        In Arabic language, there are some letters which can't be adjacent in a root.
        This function return True, if the word is valid, else, return False

        @param word: the word.
        @type word: unicode.
        @return: word with a '-' to indicate the stemming position.
        @rtype: unicode
        """
    # certain roots are forbiden in arabic
    #exprimed in letters sequences
    # but this sequence can be used for affixation
    #then we can guess that this letters are affixed
    #
    #treat one prefixe letter
    # we strip harkat and shadda
        word=araby.stripTashkeel(word);
        # prefixes_letters=( araby.TEH , araby.MEEM , araby.LAM, araby.WAW , araby.BEH, araby.KAF, araby.FEH, araby.HAMZA, araby.YEH, araby.NOON )
        # prefixes_forbiden={
        # araby.ALEF_HAMZA_ABOVE:( araby.ALEF_HAMZA_ABOVE, araby.ZAH, araby.AIN, araby.GHAIN), 
        # araby.BEH:( araby.BEH, araby.FEH, araby.MEEM ), 
        # araby.TEH :( araby.THEH, araby.DAL, araby.THAL, araby.ZAIN, araby.SHEEN, araby.SAD, araby.DAD, araby.TAH, araby.ZAH),
        # araby.FEH:( araby.BEH, araby.FEH, araby.MEEM ), 
        # araby.KAF:( araby.JEEM, araby.DAD, araby.TAH, araby.ZAH, araby.QAF, araby.KAF), 
        # araby.LAM:( araby.REH, araby.SHEEN, araby.LAM, araby.NOON ), 
        # araby.MEEM :( araby.BEH, araby.FEH, araby.MEEM ), 
        # araby.NOON :( araby.REH, araby.LAM, araby.NOON ), 
        # araby.WAW :( araby.WAW , araby.YEH), 
        # araby.YEH:( araby.THEH, araby.JEEM, araby.HAH, araby.KHAH, araby.THAL, araby.ZAIN, araby.SHEEN, araby.SAD, araby.DAD, araby.TAH, araby.ZAH, araby.GHAIN, araby.KAF, araby.HEH, araby.YEH),}

        word_guess=word;
        if len(word)>=2:
            c1=word[0];
            c2=word[1];
            if c1 in wordtag_const.prefixes_letters and ( c2 in wordtag_const.prefixes_forbiden.get(c1,'')):
                word_guess=u"%s-%s"%(c1,word[1:])
                if len(word_guess)>=4:
                    c1=word_guess[2];
                    c2=word_guess[3];
                    if c1 in wordtag_const.prefixes_letters and ( c2 in wordtag_const.prefixes_forbiden[c1]):
                        word_guess=u"%s-%s"%(c1,word_guess[2:])




    # # treat two suffixe letters
        # bisuffixes_letters=(araby.KAF+araby.MEEM ,araby.KAF+araby.NOON ,araby.HEH+araby.MEEM ,araby.HEH+araby.NOON )

        # bisuffixes_forbiden={
        # araby.HEH+araby.MEEM :(araby.ALEF_HAMZA_ABOVE, araby.HAMZA, araby.WAW_HAMZA, araby.YEH_HAMZA, araby.BEH, araby.THEH, araby.HAH, araby.KHAH, araby.SAD, araby.DAD, araby.TAH, araby.ZAH, araby.AIN, araby.GHAIN, araby.HEH, araby.YEH), 
        # araby.KAF+araby.MEEM :(araby.ALEF_HAMZA_ABOVE, araby.HAMZA, araby.WAW_HAMZA, araby.YEH_HAMZA, araby.BEH, araby.THEH, araby.JEEM, araby.KHAH, araby.ZAIN, araby.SEEN , araby.SHEEN, araby.DAD, araby.TAH, araby.ZAH, araby.GHAIN, araby.FEH, araby.QAF, araby.KAF, araby.LAM, araby.NOON , araby.HEH, araby.YEH), 
        # araby.HEH+araby.NOON :(araby.ALEF_HAMZA_ABOVE, araby.HAMZA, araby.WAW_HAMZA, araby.YEH_HAMZA, araby.BEH, araby.THEH, araby.JEEM, araby.HAH, araby.KHAH, araby.SAD, araby.DAD, araby.TAH, araby.ZAH, araby.AIN, araby.GHAIN, araby.HEH, araby.YEH), 
        # araby.KAF+araby.NOON :(araby.ALEF_HAMZA_ABOVE, araby.HAMZA, araby.WAW_HAMZA, araby.YEH_HAMZA, araby.BEH, araby.THEH, araby.JEEM, araby.HAH, araby.KHAH, araby.THAL, araby.SHEEN, araby.DAD, araby.TAH, araby.ZAH, araby.AIN, araby.GHAIN, araby.QAF, araby.KAF, araby.NOON , araby.HEH, araby.YEH), 

            # }
    ##    word_guess=word;
        word=word_guess;
        if len(word)>=3:
            bc_last=word[-2:];
            bc_blast=word[-3:-2]
            if bc_last in wordtag_const.bisuffixes_letters:
                if bc_blast in wordtag_const.bisuffixes_forbiden[bc_last]:
                    word_guess=u"%s-%s"%(word[:-2],bc_last)

    # # treat one suffixe letters
        # suffixes_letters=(araby.KAF,araby.TEH ,araby.HEH)

        # suffixes_forbiden={
        # araby.TEH :(araby.THEH, araby.JEEM, araby.DAL, araby.THAL, araby.ZAIN, araby.SHEEN, araby.TAH, araby.ZAH), 
        # araby.KAF:(araby.THEH, araby.JEEM, araby.KHAH, araby.THAL, araby.TAH, araby.ZAH, araby.GHAIN, araby.QAF),
        # araby.HEH:(araby.TEH , araby.HAH, araby.KHAH, araby.DAL, araby.REH, araby.SEEN , araby.SHEEN, araby.SAD, araby.ZAH, araby.AIN, araby.GHAIN), 
            # }
        word=word_guess;
        c_last=word[-1:];
        c_blast=word[-2:-1]
        if c_last in wordtag_const.suffixes_letters:
            if c_blast in wordtag_const.suffixes_forbiden[c_last]:
                word_guess=u"%s-%s"%(word[:-1],c_last)


        return word_guess;


    def is_valid_stem(self,stem):
        """
        Return True if the stem is valid.
        A stem can't be started by SHADDA,  araby.WAW_HAMZA,  araby.YEH_HAMZA.
        @param stem: the stem.
        @type stem: unicode.
        @return: is valid a tsem.
        @rtype: Boolean
        """

    	if stem[0] in ( araby.WAW_HAMZA, araby.YEH_HAMZA,SHADDA):
    		return False;
    	stem_guessed=guess_stem(stem);
    	if re.search("-",stem_guessed):
    		return False;
    	return True;


    def context_analyse(self,word_one, word_two, tag_one='vn', tag_two='vn'):
        """
        Detect the word type according to the previous word.
        @param word_one: the previous word.
        @type word_one: unicode.
        @param word_two: the word to detect.
        @type word_two: unicode.
        @param tag_one: the previous word tag.
        @type tag_one: unicode ('t','n','v', 'vn').
        @param tag_two: the current word.
        @type tag_two: unicode.

        @return: a code of word type ('v': verb, 'vn': verb& noun, 'n': noun)
        @rtype: unicode
        """
        # tab_verb_context? tab_noun_context declared in wordtag_const
        if word_one in wordtag_const.tab_verb_context: return "v";
        elif word_one in wordtag_const.tab_noun_context: return "n";
        elif word_two in wordtag_const.tab_noun_context or word_two in wordtag_const.tab_noun_context:
            return "t";
		# if the previous word is a verb, the second word must'nt be a verb, with out jonction
		# إذا كانت الكلمة الاولى فعلا، ينبغي أن تكون الثانية ليست فعلا
		# غلا أن تكون معطوفة أو مسبقوة بلام
		# مثل يأكل ليشبع، يأكل ويشرب،
		# يمكن أن يتوالى فعلان في حالة 
		# أفعال الشروع والمقاربة.
		# بعد التجارب تبيّن أنّ هذه الحالة غير ممكنة في حالات مثل 
		# من زرع حصد، ومن يجتهد ينجح
		#في انتظار إيجاد طريقة أفضل تبنى على تحليل أكثر للسياق
        # elif tag_one==u"v" and tag_two=='vn' and word_two[0] not in ( araby.WAW , araby.LAM, FEH):
        	# return 'n';
        return "vn";



    def is_stopword(self,word):
        """
        Return True if the word is a stopword, according a predefined list.
        @param word: the previous word.
        @type word: unicode.

        @return: is the word a stop word
        @rtype: Boolean
        """
	return  stopwords.STOPWORDS.has_key(word);
        #if word in STOPWORDS.keys():
        #    return True;
        #else:
        #    return False;
        
    def wordTagging(self, word_list):
        """
        Guess word classification, into verb, noun, stopwords.
        return al list of guessed tags
        @param word_list: the given word lists.
        @type word_list: unicode list.
        @return: a tag list : 't': tool, 'v': verb, 'n' :noun, 'nv' or 'vn' unidentifed.
        @rtype: unicode list 
        """
        if len(word_list)==0:
            return [];
        else:
            list_result=[];
            previous=u"";
            previous_tag = "";
            for word in word_list:
                tag='';
                if self.Cache.has_key(word):
                    tag=self.Cache.get(word,'');
                else:
                    if self.is_stopword(word):tag='t';
                    else:
                        if self.is_noun(word):tag+='n';
                        if self.is_verb(word):tag+='v';
                    # add the found tag to Cache.
                    self.Cache[word]=tag;
                # if the tagging give an ambigous tag, we can do an contextual analysis
				# the contextual tag is not saved in Cache, because it can be ambigous.
				# for example  
				# في ضرب : is a noun
				# قد ضرب : is a verb
                if tag in ("","nv"):
                    tag=self.context_analyse(previous, word, previous_tag)+"1";
                list_result.append(tag);
                previous=word;
                previous_tag = tag;
            return list_result;
if __name__ == "__main__":
    tagger=WordTagger();
    word_list=(
	u"باستحقاقه",
	u"ومعرفته",
 u"تأسست",
u"وتأسست",
 u"التجاوزات",
 u"تجاوزات",
 u'التعريف',
 )

    if len(word_list)==0:
        print 'emplty wordlist'
    else:
        list_result=[];
        previous=u"";
        previous_tag = "";		
        for word in word_list:
            tag='';
            if tagger.is_stopword(word):tag='t';
            else:
                print word.encode('utf8'), tagger.is_possible_noun(word);			
                if tagger.is_noun(word):tag+='n';
                print word.encode('utf8'),tagger.is_possible_verb(word);
                if tagger.is_verb(word):tag+='v';
                if tag in ("","nv"):
                    tag=tagger.context_analyse(previous, word, previous_tag)+"1";
            list_result.append({'word':word,'tag': tag});
            previous=word;
            previous_tag = tag;
        for item  in list_result:
            print ("%s\t%s"%(item['word'],item['tag'])).encode('utf8');
