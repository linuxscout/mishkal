#!/usr/bin/python
# -*- coding=utf-8 -*-
#************************************************************************
# $Id: ar_verb.py,v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2009, Arabtechies, Arabeyes Taha Zerrouki
#
#  Elementary function to manipulate arabic texte
#
# -----------------
# Revision Details:    (Updated by Revision Control System)
# -----------------
#  $Date: 2009/06/02 01:10:00 $
#  $Author: Taha Zerrouki $
#  $Revision: 0.7 $
#  $Source: arabtechies.sourceforge.net
#
#***********************************************************************/
"""
Basic routines to treat verbs
ar_verb
"""
import re
# import string
# import sys
# import os
# import types
from arabic_const import *
from verb_const import *
from ar_ctype import *
import pyarabic.araby as araby

from alefmaddaverbtable import *

#used to
VALID_INFINITIVE_VERB6_pat=re.compile(u"^است...|ا..ن..|ا..و..|ا..ا.ّ|ا....ّ|ا.ّ.ّ.|ا.ّا..$",re.UNICODE)

VALID_INFINITIVE_VERB4_pat=re.compile(u"^([%s%s][^%s]{2}.|[^%s%s]%s[^%s%s].|[^%s%s]{2}%s[^%s]|[^%s%s]{4})$"%(ALEF_HAMZA_ABOVE,HAMZA,SHADDA,ALEF,SHADDA,ALEF,ALEF,SHADDA,ALEF,SHADDA,SHADDA,SHADDA,ALEF,SHADDA),re.UNICODE)

VALID_INFINITIVE_VERB5_pat=re.compile( u"|".join([
                                    u"^ا...ّ$",
            # حالة اتخذ أو اذّكر أو اطّلع
            u"^%s[%s%s%s]%s..$"%(ALEF,TEH,THAL,TAH,SHADDA),
            # حالة اتخذ أو اذّكر أو اطّلع
           u"^ا[تذط]ّ[^اّ][^اّ]$",
            # انفعل
            u"^ان...$",
            #افتعل
            u"^(ازد|اصط|اضط)..$"
            u"^ا[^صضطظد]ت..$",
            u"^ا...ّ$",
            # حالة اتخذ أو اذّكر أو اطّلع
             u"^ا.ّ..$",
             u"^ا...ى$",
             ]) ,re.UNICODE);
#####################################
#{ verb attributes conversion functions
#####################################

def get_bab_sarf_harakat(number):
	"""
	Get the   the past and future marks by the bab sarf number
		- Bab: past  future
		- 1  : FATHA DAMMA
		- 2  : FATHA KASRA
		- 3  : FATHA FATHA
		- 4  : KASRA FATHA
		- 5  : DAMMA DAMMA
		- 6  : KASRA KASRA
	@param number: Bab sarf number (1-6).
	@type number: integer(1-6)
	@return:  a tuple of (past_mark, future_mark);
	@rtype: tuple;
	"""
	if number<1 or number>6:
		return None;
	elif number==1:
		return (FATHA,DAMMA);
	elif number==2:
		return (FATHA,KASRA);
	elif number==3:
		return (FATHA,FATHA);
	elif number==4:
		return (KASRA,FATHA);
	elif number==5:
		return (DAMMA,DAMMA);
	elif number==6:
		return (KASRA,KASRA);

def get_bab_sarf_number(past_haraka,future_haraka):
	"""
	Get the bab sarf number by the past and future marks
		- Bab: past  future
		- 1  : FATHA DAMMA
		- 2  : FATHA KASRA
		- 3  : FATHA FATHA
		- 4  : KASRA FATHA
		- 5  : DAMMA DAMMA
		- 6  : KASRA KASRA
	@param past_haraka: past haraka of the verb.
	@type past_haraka: unicode;
	@param future_haraka: future haraka of the verb.
	@type future_haraka: unicode;
	@return: Bab sarf number (1-6);
	@rtype: integer;
	"""
	if past_haraka==FATHA and future_haraka==DAMMA:
		return 1;
	elif past_haraka==FATHA and future_haraka==KASRA:
		return 2;
	elif past_haraka==FATHA and future_haraka==FATHA:
		return 3;
	elif past_haraka==KASRA and future_haraka==FATHA:
		return 4;
	elif past_haraka==DAMMA and future_haraka==DAMMA:
		return 5;
	elif past_haraka==KASRA and future_haraka==KASRA:
		return 6;
	else:
		return 0;

def write_harakat_in_full(harakat):
	"""
	Write the harakat name in full  in arabic
	@param harakat: list of harakat chars.
	@type  harakat: unicode  string;
	@return: harakat in full;
	@rtype: unicode;
	"""
	full=u"";
	tab_harakat={
	FATHA:u"فتحة",
	DAMMA:u"ضمة",
	KASRA:u"كسرة",
	SUKUN:u"سكون",
	ALEF_HARAKA:u"ألف",
	WAW_HARAKA:u"واو",
	YEH_HARAKA:u"ياء",
	ALEF_YEH_HARAKA:u"ى",
	ALEF_WAW_HARAKA:u"و",
	ALEF_YEH_ALTERNATIVE:u"ئ",
	}
	for c in harakat:
		if tab_harakat.has_key(c):
			full+=u'-'+tab_harakat[c];
		else:
			full+=u"*";
	return full;

def get_past_harakat_by_babsarf(vtype):
	"""
	Get the past harakat for the trileteral verb by bab sarf
		- Bab: past  future
		- 1  : FATHA DAMMA
		- 2  : FATHA KASRA
		- 3  : FATHA FATHA
		- 4  : KASRA FATHA
		- 5  : DAMMA DAMMA
		- 6  : KASRA KASRA
	@param vtype: the bab sarf codification.
	@type vtype: unicode a string of number;
	@return: harakat;
	@rtype: unicode;
	"""
	marks=KASRA+KASRA+KASRA;
	if vtype in ('1','2','3'):
	   marks=FATHA+FATHA+FATHA
	elif vtype in ('4','6'):
	   marks=FATHA+KASRA+FATHA
	elif vtype=='5':
	   marks=FATHA+DAMMA+FATHA
	return marks;
def get_future_harakat_by_babsarf(vtype):
	"""
	Get the future harakat for the trileteral verb by bab sarf
		- Bab: past  future
		- 1  : FATHA DAMMA
		- 2  : FATHA KASRA
		- 3  : FATHA FATHA
		- 4  : KASRA FATHA
		- 5  : DAMMA DAMMA
		- 6  : KASRA KASRA
	@param vtype: the bab sarf codification.
	@type vtype: unicode a string of number;
	@return: harakat;
	@rtype: unicode;
	"""
	#ToDo Review
	marks=KASRA+KASRA+KASRA;
	if vtype in ('1','2','3'):
	   marks=FATHA+FATHA+FATHA
	elif vtype in ('4','6'):
	   marks=FATHA+KASRA+FATHA
	elif vtype=='5':
	   marks=FATHA+DAMMA+FATHA
	return marks;

def get_future_haraka_by_babsarf(vtype):
	"""
	Get the future_type value from  different codifications. used also in comand line
	in différent context the future_type is codified as:
	values
	or values used as Conjugation mode ( Bab Tasrif باب التصريف)
		- Bab: past  future
		- 1  : FATHA DAMMA
		- 2  : FATHA KASRA
		- 3  : FATHA FATHA
		- 4  : KASRA FATHA
		- 5  : DAMMA DAMMA
		- 6  : KASRA KASRA
	@param vtype: the bab sarf codification.
	@type vtype: unicode a string of number;
	@return: haraka;
	@rtype: unicode char;
	"""

	if vtype=='1': return DAMMA;
	elif vtype in ('2','6'): return KASRA;
	elif vtype in ('3','4'): return FATHA;
	elif vtype in ('1','5'): return DAMMA;
	else: return "";


def get_haraka_by_name(haraka_name):
	"""
	Convert an arabic named harakat to a real haraka
	values
		- Fahta:(فتحة)
		- DAMMA:(ضمة)
		- KASRA:(كسرة)
	@param haraka_name: the arabic name of haraka.
	@type haraka_name: unicode;
	@return: the arabic name of haraka .
	@rtype: unicode char;
	"""
	if haraka_name in(FATHA,DAMMA,KASRA, SUKUN):
         return haraka_name;
	if haraka_name==u"فتحة"  : return FATHA;
	elif haraka_name==u"ضمة":return DAMMA;
	elif haraka_name==u"كسرة":return KASRA;
	elif haraka_name==u"سكون": return SUKUN;
	else: return False;


def get_future_type_by_name(haraka_name):
	"""
	Get the future_type value by haraka arabic name.
	values
		- FATHA:(فتحة)
		- DAMMA:(ضمة)
		- KASRA:(كسرة)
	@param haraka_name: the arabic name of haraka.
	@type haraka_name: unicode;
	@return: haraka;
	@rtype: unicode char;
	"""
	haraka=get_haraka_by_name(haraka_name);
	if haraka: return haraka;
	else: return FATHA;


def get_future_type_entree(future_type):
	"""
	Get the future_type value from  different codifications. used also in comand line
	in différent context the future_type is codified as:
	values
		- Fahta:(fatha,فتحة,ف,f)
		- DAMMA:(damma,ضمة,ض,d)
		- KASRA:(kasra,كسرة,ك,k)
	or values used as Conjugation mode ( Bab Tasrif باب التصريف)
		- Bab: past  future
		- 1  : FATHA DAMMA
		- 2  : FATHA KASRA
		- 3  : FATHA FATHA
		- 4  : KASRA FATHA
		- 5  : DAMMA DAMMA
		- 6  : KASRA KASRA
	@param future_type: the future_type codification.
	@type future_type: unicode;
	@return: extract the future type mark;
	@rtype: unicode char;
	"""
	future_type=u""+future_type.lower();
	if future_type in (u'fatha',u'فتحة',u'ف',u'f',u'3',u'4'):
		return FATHA;
	if future_type in (u'damma',u'ضمة', u'ض',u'd',u'1',u'5'):
		return DAMMA;
	if future_type in (u'kasra',u'كسرة',u'ك',u'k',u'2',u'6'):
		return KASRA;
	else: return FATHA;

def get_transitive_entree(transitive):
	"""
	Get the transitive value from  different codifications.
	in différent context the transitivity is codified as:
		- "t", "transitive",
		- u"متعدي",u"م",u"مشترك",u"ك";
		- True;
	@param transitive: the transitive codification.
	@type transitive: unicode;
	@return: True if is transitive;
	@rtype: boolean;
	"""
	if transitive in (u"متعدي",u"م",u"مشترك",u"ك","t","transitive",True):
	    transitive=True;
	else :
	    transitive=False;
	return transitive;

#####################################
#{validation functions
#####################################
def is_valid_infinitive_verb(word, IsVocalized=True):
	"""
	Determine if the given word is a valid infinitive form of an arabic verb.
	A word is not valid  infinitive if
		- lenght < 3 letters.
		- starts with : ALEF_MAKSURA, WAW_HAMZA,YEH_HAMZA,	HARAKAT
		- contains TEH_MARBUTA,Tanwin
		- contains non arabic letters.
		- contains ALEF_MAKSURA not in the end.
		- contains double haraka : a warning
	@param word: given word.
	@type word: unicode.
	@param IsVocalized: if the given word is vocalized.
	@type IsVocalized:Boolean, default(True).
	@return: True if the word is a valid infinitive form of verb.
	@rtype: Boolean.
	"""
	# test if the word is an arabic valid word,
	if not  araby.isArabicword(word):
		return False;
	if IsVocalized :word_nm = araby.stripHarakat(word);
	else:
		word_nm=word;
	# the alef_madda is  considered as 2 letters

	word_nm=word_nm.replace(ALEF_MADDA,HAMZA+ALEF);
	length=len(word_nm)

	# lenght with shadda must be between 3 and 6
	if length<3  or length>=7: return False;
	# a 3 length verb can't start by Alef or Shadda, and the second letter can't be shadda
	elif length==3 and (word_nm[0]==ALEF or word_nm[0]==SHADDA or word_nm[1]==SHADDA):
		return False;

	# a 5 length verb must start by ALEF or TEH
	elif length==5 and word_nm[0] not in (TEH,ALEF):
		return False;
	# a 6 length verb must start by ALEF
	elif length==6 and word_nm[0]!=ALEF:
		return False;

	# contains some invalide letters in verb
	elif re.search(u"[%s%s%s%s%s]"%(ALEF_HAMZA_BELOW, TEH_MARBUTA,DAMMATAN,KASRATAN,FATHATAN),word):
		return False;
	# contains some SHADDA sequence letters in verb
	# Like shadda shadda, shadda on alef, start  by shadda, shadda on alef_ maksura,
	# ALEF folowed by (ALEF, ALEF_MAKSURA)
	# ALEF Folowed by a letter and ALEF
	# end with ALEF folowed by (YEH, ALEF_MAKSURA)
	# first letter is alef and ALLw alef and two letters aand shadda
	elif re.search(u"([%s%s%s]%s|^%s|^%s..%s|^.%s|%s.%s|%s%s|%s[%s%s]$)"%(ALEF,ALEF_MAKSURA,SHADDA,SHADDA,SHADDA,ALEF,SHADDA,SHADDA,ALEF,ALEF,ALEF,ALEF,ALEF,ALEF_MAKSURA,YEH),word_nm):
		return False;


	# Invalid root form some letters :
	# initial YEH folowed by ((THEH,JEEM,HAH,KHAH,THAL,ZAIN,SHEEN,SAD,DAD,TAH,ZAH,GHAIN,KAF,HEH,YEH))
	elif re.search(u"^%s[%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s]"%(YEH,THEH,JEEM,HAH,KHAH,THAL,ZAIN,SHEEN,SAD,DAD,TAH,ZAH,GHAIN,KAF,HEH,YEH),word_nm):
		return False;


	   # TEH After (DAL,THAL,TAH,ZAH,DAD)
	elif re.search(u"[%s%s%s%s%s]%s"%(DAL,THAL,DAD,TAH,ZAH,TEH),word_nm):
		return False;
	# Contains invalid root sequence in arabic, near in phonetic
	# like BEH and FEH, LAM And REH
	elif re.search(u"%s%s|%s%s|%s%s|%s%s|%s%s|%s%s|%s%s"%(LAM,REH,REH,LAM,FEH,BEH,BEH,FEH,NOON,LAM,HEH,HAH,HAH,HEH),word_nm):
		return False;


	# in non 5 letters verbs :initial TEH followed by   (THEH,DAL,THAL,ZAIN,SHEEN,SAD,DAD,TAH,ZAH)
	elif length!=5 and word_nm.startswith(TEH) and word_nm[1] in (TEH,THEH,DAL,THAL,ZAIN,SHEEN,SAD,DAD,TAH,ZAH):
		return False;
	# if word start by the same letter doubled
	elif word_nm[0]==word_nm[1] and word[0]!=TEH: return False;

	#verify the wazn of the verb
	elif length==3:
		if re.match("^[^%s][^%s].$"%(ALEF,SHADDA),word_nm):
			return True;
	# الأوزان المقبولة هي فعل، فعّ،
	# الأوزان غير المقبولة
	# اعل، فّل
		else: return False;
	elif length==4:
	#1- أفعل، 2- فاعل، 3 فعّل 4 فعلل
		if re.match("^([%s%s][^%s]{2}.|[^%s%s]%s[^%s%s].|[^%s%s]{2}%s[^%s]|[^%s%s]{4})$"%(ALEF_HAMZA_ABOVE,HAMZA,SHADDA,ALEF,SHADDA,ALEF,ALEF,SHADDA,ALEF,SHADDA,SHADDA,SHADDA,ALEF,SHADDA),word_nm):

			return True;
	# الأوزان المقبولة هي فعل، فعّ،
	# الأوزان غير المقبولة
	#     افعل: يجب تثبيت همزة القطع
	#فّعل، فعلّ: الشدة لها موضع خاص
	# فعال، فعلا: للألف موضع خاص
		else: return False;
	elif length==5:

		if  word_nm.startswith(ALEF):
			if re.match(u"^ا...ّ$",word_nm):
				return True;
			# حالة اتخذ أو اذّكر أو اطّلع
			if re.match(u"^%s[%s%s%s]%s..$"%(ALEF,TEH,THAL,TAH,SHADDA),word_nm):
				return True;

			# انفعل
			elif re.match(u"^ان...$",word_nm):
				return True;
			#افتعل
			elif re.match(u"^(ازد|اصط|اضط)..$",word_nm):
				return True;
			elif re.match(u"^ا[^صضطظد]ت..$",word_nm):
				return True;
			elif re.match(u"^ا...ّ$",word_nm):
				return True;
			# حالة اتخذ أو اذّكر أو اطّلع
			elif re.match(u"^ا.ّ..$",word_nm):
				return True;
			elif re.match(u"^ا...ى$",word_nm):
				return True;
			else: return False;
		elif word_nm.startswith(TEH):
			return True;
		else:
			return False;

	# الأوزان المقبولة هي فعل، فعّ،
	# الأوزان غير المقبولة
	#للشدة موضع خاص: تفعّل، افتعّ
	# للألف مواضع خاصة،
	elif length==6:
		if not (word_nm.startswith(ALEF) or word_nm.startswith(TEH)):
			return False;
		if VALID_INFINITIVE_VERB6_pat.match(word_nm):
			return True;
	# الأوزان المقبولة هي فعل، فعّ،
	# الأوزان غير المقبولة
	#للشدة موضع خاص: تفعّل، افتعّ
	# للألف مواضع خاصة،
		else: return False;
	return True;


def suggest_verb(verb):
	"""
	Generate a list of valid infinitive verb for an invalid infinitive form.
	@param verb: given verb, of invalid infinitive form.
	@type verb: unicode.
	@return: a list of suggested infinitive verb forms
	@rtype: list of unicode.
	"""
	# the verb is invalid
	list_suggest=[];
	# first strip harakat, shadda is not striped
	verb=araby.stripHarakat(verb);
	# second strip all inacceptable letters in an infinivive form
	verb=re.sub(u"[%s%s%s%s]"%( TEH_MARBUTA,DAMMATAN,KASRATAN,FATHATAN),'',verb)
	# test the resulted verb if it's valid, if ok, add it to the suggestion list.
	if is_valid_infinitive_verb(verb):
		list_suggest.append(verb);
		return list_suggest;
	# if the verb starts by ALEF_HAMZA_BELOW like إستعمل, replace if by an ALEF, because it's a common error.
	# if the result is valid add it to the suggestions list
	elif verb.startswith(ALEF_HAMZA_BELOW):
		verb=re.sub(ALEF_HAMZA_BELOW,ALEF,verb);
		if is_valid_infinitive_verb(verb):
			list_suggest.append(verb);
			return list_suggest;
	# if the verb starts by ALEF like اضرب, replace if by an ALEF_HAMZA_ABOVE, because it's a common error.
	# if the result is valid add it to the suggestions list
	elif verb.startswith(ALEF):
		verb_one=re.sub(ALEF,ALEF_HAMZA_ABOVE+FATHA,verb,1);
		if is_valid_infinitive_verb(verb_one):
			list_suggest.append(verb_one);
			return list_suggest;
	# if the verb is 2 letters length, suggest to add the third letter as : Shadda, Alef, Alef Maksura, Yeh at the end
	# if the result is valid add it to the suggestions list
	elif len(verb)==2:
		verb=re.sub(ALEF,ALEF_HAMZA_ABOVE,verb,1);
		#suggest to add the third letter as : Shadda at the end
		verb_one=verb+SHADDA;
		if is_valid_infinitive_verb(verb_one):
			list_suggest.append(verb_one);
		#suggest to add the third letter as : Alef Maksura
		verb_one=verb+ALEF_MAKSURA;
		if is_valid_infinitive_verb(verb_one):
			list_suggest.append(verb_one);
		#suggest to add the third letter as :Alef at the end
		verb_one=verb+ALEF;
		if is_valid_infinitive_verb(verb_one):
			list_suggest.append(verb_one);
		#suggest to add the third letter as :Alef in middle
		verb_one=verb[0]+ALEF+verb[1];
		if is_valid_infinitive_verb(verb_one):
			list_suggest.append(verb_one);
		return list_suggest;
	elif len(verb)>=6:
	# if the verb is more than 6 letters length, suggest to replace the over added letters by Alef
	# if the result is valid add it to the suggestions list
		for i in range(len(verb)-6):
			verb_one=ALEF+verb[i:i+5];
			if is_valid_infinitive_verb(verb_one):
				list_suggest.append(verb_one);
	elif len(verb)==5:
	# if the verb is 5 letters length, suggest
	# if the result is valid add it to the suggestions list
		# ToDo: review this part
		for i in range(len(verb)-5):
			verb_one=ALEF+verb[i:i+4];
			if is_valid_infinitive_verb(verb_one):
				list_suggest.append(verb_one);
	elif len(verb)==4:

	# if the verb is 5 letters length, suggest to replace the over added letters by Alef
	# if the result is valid add it to the suggestions list
	# فعال=> فاعل
	#فّعل=> فعّل
		if verb[2]==ALEF or verb[1]==SHADDA:
			verb_one=verb[0]+verb[2]+verb[1]+verb[3]
			if is_valid_infinitive_verb(verb_one):
				list_suggest.append(verb_one);
		if verb.endswith(SHADDA):
	# if the verb is 4 letters length, suggest to correct the alef and shadda position
	# if the result is valid add it to the suggestions list
	#فعلّ=> فعّل
			verb_one=verb[0]+verb[1]+verb[3]+verb[2]
			if is_valid_infinitive_verb(verb_one):
				list_suggest.append(verb_one);
		return list_suggest;
	else:
	# else sugest to conjugate another verb
		list_suggest.append(u"كتب");
		return list_suggest;
	return list_suggest;

#####################################
#{verb pretreatment functions
#####################################
def  normalize_alef_madda(word):
	"""
	Convert Alef madda into two letters.
    @param word: given word.
    @type word: unicode.
    @return: converted word.
    @rtype: unicode.
	"""
	if word.startswith(ALEF_MADDA):
		word_nm=araby.stripHarakat(word);
		if len(word_nm)==2:
			return word_nm.replace(ALEF_MADDA, HAMZA+ALEF);
		elif len(word_nm)==3:
			if AlefMaddaVerbTable.has_key(word_nm):
				#return the first one only
				#mylist=AlefMaddaVerbTable[word_nm];
				return AlefMaddaVerbTable[word_nm][0];
			else:
				return  word_nm.replace(ALEF_MADDA, HAMZA+ALEF);
		else:
			return word_nm.replace(ALEF_MADDA, HAMZA+ALEF)
	else:
		return word_nm;

# def normalize_hamza(word):

	# """
	# Standardize the Hamzat into one form of hamza
	# replace Madda by hamza and alef.
    # @param word: given word.
    # @type word: unicode.
    # @return: converted word.
    # @rtype: unicode.
	# """
	# HAMZAT= u"إأءئؤ";
# #TODO:
# ## مشكلة في تحويل ألف المدة الأولى، فهي تنقلب إما إلى همزة بعدها أللف في مثل فاعل،
# ## وذلك في حال الفعل المضعف مهموز الأول
# ## أو همزتين متتاليتين على وزن أفعل
# ## تستبدل الألف الممدودة في ,ل الكلمة بهمزة قطع بعدها همزة أخرى
	# if word.startswith(ALEF_MADDA):
	   # if len(word)>=3 and (word[1] not in HARAKAT) and (word[2]==SHADDA or len(word)==3):
			# word=HAMZA+ALEF+word[1:];
	   # else:
			# word=HAMZA+HAMZA+word[1:];
	# # convert all Hamza from into one form
	# word=word.replace(ALEF_MADDA,HAMZA+HAMZA);
	# word=HAMZAT_pat.sub(HAMZA,word);

	# return word;







def normalize(word,type="affix"):
	"""
	Normalize the word, by unifoming hamzat, Alef madda,  shadda, and lamalefs.
    @param word: given word.
    @type word: unicode.
    @param type: if the word is an affix
    @type type: unicode.
    @return: converted word.
    @rtype: unicode.
	"""

# تحويل الكلمة إلى شكلها النظري.
# الشكل اللإملائي للكلمة هو طريقة كتابتها حسب قواعد الإملاء
# الشكل النظري هو الشكل المتخيل للكلمة دون تطبيق قواعد اللغة
# ويخص عادة الأشكال المتعددة للهمزة، و التي تكتب همزة على السطر
# أمثلة
# إملائي		نظري
#إِمْلَائِي		ءِمْلَاءِي
#سَاَلَ		سَءَلَ
# الهدف : تحويل الكلمة إلى شكل نظري، ومن ثم إمكانية تصريفها بعيدا عن قواعد الإملاء،
#وبعد التصريف يتم تطبيق قواعد الإملاء من جديد.
#الفرضية: الكلمات المدخلة مشكولة شكلا تاما.
#الطريقة:
# 1-تحويل جميع أنواع الهمزات إلى همزة على السطر
# 1-فك الإدغام
	i=0;
#   strip tatweel
# the tatweel is used to uniformate the affix when the Haraka is used separetely
	if type!="affix": word=araby.stripTatweel(word);
## تستبدل الألف الممدودة في ,ل الكلمة بهمزة قطع بعدها همزة أخرى
	if word.startswith(ALEF_MADDA):
		word=normalize_alef_madda(word);

	# ignore harakat at the begin of the word
	len_word=len(word)
	while i<len_word and word[i] in HARAKAT:
		i+=1;
	word=word[i:]
	# convert all Hamza from into one form
	word=araby.normalizeHamza(word);
    #Convert All LAM ALEF Ligature into separate letters
	word=word.replace(LAM_ALEF,simple_LAM_ALEF);
	word=word.replace(LAM_ALEF_HAMZA_ABOVE,simple_LAM_ALEF_HAMZA_ABOVE);
	word=word.replace(LAM_ALEF_MADDA_ABOVE,simple_LAM_ALEF_MADDA_ABOVE);
    # deprecated
	# invalid letter
	#	word=word.replace(LAM_ALEF_HAMZA_BELOW,simple_LAM_ALEF_HAMZA_BELOW);

	# convert Shadda to sukun shadda
	#word=word.replace( SHADDA,SUKUN+SHADDA);

	# deprecated we don't need harakat here
	# while i <len(word):
# ## حالة غياب الفتحة قبل الألف
		# if word[i] not in(SUKUN,FATHA,KASRA,DAMMA,ALEF) and i+1<len(word) and word[i+1]==ALEF:
		  # word=replace_pos(word,word[i]+FATHA,i);
		# elif word[i]==ALEF_MADDA:
			# word=word.replace(ALEF_MADDA,HAMZA+FATHA+ALEF);
		# i+=1;
	return word;



def uniformate_alef_origin(marks,word_nm,future_type=KASRA):
	"""
	Convert toi its origin according to the future type haraka
    @param marks: given marks.
    @type marks: unicode.
    @param word_nm: given word unvocalized.
    @type word_nm: unicode.
    @param future_type: The future mark of the triletiral verb.
    @type future_type: unicode char, default KASRA.
    @return: converted marks.
    @rtype: unicode.
	"""
	if len(marks)!=2:return marks;
# الحرف ماقبل الأخير علة
	elif marks[len(marks)-2]==ALEF_HARAKA:
		if future_type==KASRA:
			marks=marks[:-2]+ALEF_YEH_HARAKA+marks[-1:]
		elif future_type==DAMMA:
			marks=marks[:-2]+ALEF_WAW_HARAKA+marks[-1:]
# الحرف الأخير علة
	if len(word_nm)==3 and word_nm[-1:]==ALEF:
		word_nm=word_nm[:-1]+ALEF_MAMDUDA
	elif len(word_nm)>3 and word_nm[-1:]==ALEF:
		word_nm=word_nm[:-1]+YEH#ALEF_MAKSURA
	elif word_nm[-1:]==ALEF_MAKSURA:
		word_nm=word_nm[:-1]+ALEF_MAKSURA
	return marks;

#--------------------------------------
# Predecated function
#--------------------------------------
def normalize_affix(word):
	"""
	Replace shadda by SUKUN +SHADDA
    @param word: given word.
    @type word: unicode.
    @return: converted word.
    @rtype: unicode.
	"""
    # convert SHadda to sukun shadda
	word=word.replace(SHADDA,SUKUN+SHADDA);

	return word;
#--------------------------------------

#--------------------------------------
def uniformate_suffix(word):
	""" separate the harakat and the letters of the given word, it return two strings ( the word without harakat and the harakat).
    If the weaked letters are reprsented as long harakat and striped from the word.
    """
    ## type : affix : uniformate affixes
##	word=normalize_affix(word);
	word=word.replace(SHADDA,SUKUN+SHADDA);
	HARAKAT=(FATHA,DAMMA,KASRA,SUKUN);
	shakl=u"";
	word_nm=u""
	i=0;
	len_word=len(word);
#	print "len word",len(word);
	while i <len_word:
		if word[i] not in HARAKAT:
			word_nm+=word[i];
			if i+1 < len(word) and word[i+1] in HARAKAT:
				if word[i+1]==FATHA :
					if i+2<len(word) and word[i+2]==ALEF and i+3<len(word) :
						shakl+=ALEF_HARAKA;
#						shakl+=ALEF;
						i+=3;
					else :
						shakl+=FATHA;
						i+=2;
				elif word[i+1]==DAMMA and i+2<len(word) and word[i+2]==WAW:
					if i+3>=len(word) or word[i+3] not in HARAKAT:
						shakl+=WAW_HARAKA;
						i+=3;
					else :
						shakl+=DAMMA;
						i+=2;
				elif word[i+1]==KASRA and i+2<len(word) and word[i+2]==YEH:
					if i+3>=len(word) or word[i+3] not in HARAKAT:
						shakl+=YEH_HARAKA;
						i+=3;
					else :
						shakl+=KASRA;
						i+=2;
				else :
					shakl+=word[i+1];
					i+=2;

			elif  i+1 < len(word) and word[i+1] in HARAKAT :
				shakl+=word[i+1];
			else:
				shakl+=NOT_DEF_HARAKA;
				i+=1;
		else: i+=1;
	if len(word_nm)==len(shakl):
		return (word_nm,shakl)
	else: return (u"",u"");


def uniformate_verb(word):
	"""
	Separate the harakat and the letters of the given word, it return two strings ( the word without harakat and the harakat).
	If the weaked letters are reprsented as long harakat and striped from the word.
	@param word: given word.
	@type word: unicode.
	@return: (letters, harakat).
	@rtype: tuple of unicode.
	"""

	if word=="": return ("","");
    #normalize ALEF MADDA
    #TODO : HAMZA HAMZA or HAMZA ALEF
	if word.startswith(ALEF_MADDA):
	   word=word.replace(ALEF_MADDA,HAMZA+HAMZA);
	else:
	   word=word.replace(ALEF_MADDA,HAMZA+ALEF);

	word_nm=araby.stripHarakat(word);
	length=len(word_nm);
	if len(word_nm)!=3:
        # تستعمل الهمزات لتخمين حركات الفعل الثلاثي
        # normalize hamza here, because we use it to detect harakat on the trilateral verb.
	   word_nm=HAMZAT_pat.sub(HAMZA,word_nm);
    # length of word after normalization

    # اهمزات تستعمل لكشف تشكيل الفعل، يتم توحيدها لاحقا
	if length==3:
		if word_nm[1]in (ALEF,ALEF_HAMZA_ABOVE) or word_nm[2] in(ALEF_MAKSURA, ALEF_HAMZA_ABOVE,ALEF):
			marks=FATHA+FATHA+FATHA;
		elif word[1]== YEH_HAMZA or word[2] in (YEH,YEH_HAMZA):
			marks=FATHA+KASRA+FATHA;
		else:
            # TODO
            # let the verb haraka
			i=0;
		## ignore harakat at the began of the word
			while word[i] in HARAKAT:
				i+=1;
		# الحرف الأول
			if word[i] not in HARAKAT:i+=1;
        # الحركة الأولى
			while word[i] in HARAKAT:
				i+=1;
		# الحرف الثاني
			if word[i] not in HARAKAT:i+=1;
        #الحركة الثانية
			if word[i] not in HARAKAT:
			#وجدنا مشاكل في تصريف الفعل المضاعف في الماضي
			# نجعل الحركة الثانية فتحة مؤقتا
			#ToDo: review this case
				secondharaka=FATHA;
			else:
				secondharaka=word[i];
			marks=FATHA+secondharaka+FATHA;
        # تستعمل الهمزات لتخمين حركات الفعل الثلاثي
        # normalize hamza here, because we use it to detect harakat on the trilateral verb.
		word_nm=HAMZAT_pat.sub(HAMZA,word_nm);

	elif length==4:
		marks=UNIFORMATE_MARKS_4#FATHA+SUKUN+FATHA+FATHA;
	elif length==5:
		if word_nm.startswith(TEH):
			marks=UNIFORMATE_MARKS_5TEH#FATHA+FATHA+SUKUN+FATHA+FATHA;
		else :
			marks=UNIFORMATE_MARKS_5#KASRA+SUKUN+FATHA+FATHA+FATHA;
	elif length==6:
		marks=UNIFORMATE_MARKS_6;
	else:
	    marks=FATHA*len(word_nm);

	i=1;
# first added automaticlly
	new_word=word_nm[0];
	new_harakat=marks[0];
# between the first and the last
	while i<length-1:
		if word_nm[i]==ALEF:
			new_harakat=new_harakat[:-1]+ALEF_HARAKA;
		else:
			new_harakat+=marks[i];
			new_word+=word_nm[i];
		i+=1;
# the last letter
##  حالة الفعل عيا، أعيا، عيّا والتي يتحول إلى ياء بدلا عن واو
	if word_nm[i]==ALEF:
	    if len(word_nm)==3 and word_nm[1]!=YEH:
	       new_word+=ALEF_MAMDUDA;
	    else:
	       new_word+=YEH;
	else:
	    new_word+=word_nm[i];
	new_harakat+=marks[i];
##	new_word+=word_nm[i];
	return (new_word,new_harakat);


#####################################
#{verb conjugation output treatment functions
#####################################
def standard_harakat(word):
	"""
	Treat Harakat on the word before output.
	معالجة الحركات قبل الإخراج،
	@param word: given vocalized word.
	@type word: unicode.
	@return: <vocalized word with ajusted harakat.
	@rtype: unicode.
	"""
	k=1;
	new_word=word[0];
	len_word=len(word);
	while k<len_word:
	## الحروف من دون العلة لا تؤخذ بيعين الاعتبار، كما لا تؤخذ إذا كانت في أول الكلمة
	   if word[k] not in (ALEF,YEH,WAW,ALEF_MAKSURA):
			new_word+=word[k];
	   else:
	##إذا كان الحرف علة ولم يكن في أول الكلمة
	##إذا كان ما قبله ليس حركة، ومابعده ليس حركة، أو انتهت الكلمة
		if word[k-1] not in HARAKAT and (k+1>=len_word or word[k+1] not in HARAKAT) :
			if word[k]==ALEF:
				new_word+=FATHA+ALEF;
			elif word[k]==WAW :
				new_word+=DAMMA+WAW;
			elif word[k]==YEH:
				new_word+=KASRA+YEH;
			else:new_word+=word[k];
		else:new_word+=word[k];
	   k+=1;
	return new_word;


def geminating(word_nm,harakat):
	""" treat geminating cases
	المدخلات هي من كلمة غير مشكولة يقابلها حركاتها
	والحرف المضعف يمثل بشدة
	وإذا كانت الحالة تستوجب الفك، استبدلت الشدة بالحرف المضعف،
	أمّا إذا كانت لا تستوجب الفك، فتُعدّل حركة الحرف المضعف الأول إلى حركة ملغاة، تحذف في دالة الرسم الإملائي فيما بعد

	@param word_nm: given unvocalized word.
	@type word_nm: unicode.
	@param harakat: given harakat.
	@type harakat: unicode.
	@return: (letters, harakat).
	@rtype: tuple of unicode.
	"""

	new_word=u"";
	new_harakat=u"";
	i=0;
	length=len(word_nm)
	##    has_shadda=False;
	##    has_shadda=False;
	if word_nm.find(SHADDA)<0:
		return (word_nm,harakat)
	##has_shadda and
	while i <length:
	# نعالج الحالات التي فيها الحرف الحالي متبوع بحرف شدة،
	# ندرس الحالات التي يجب فيها فك الإدغام
		if (i>0 and i+1<length and word_nm[i+1]==SHADDA and harakat[i] in (SUKUN,FATHA,KASRA,DAMMA)):
			# treat ungeminating case

	#    إذا كان الحرف المضعف الأول غير ساكن والحرف المضعّف الثاني (ممثلا بشدة)ساكنا، يفك الإدغام.
			if  harakat[i]!=SUKUN and harakat[i+1]==SUKUN:
				#ungeminating
				new_word+=word_nm[i];
				word_nm=replace_pos(word_nm,word_nm[i],i+1)
				new_harakat+=harakat[i];
				i+=1;

			elif  harakat[i]==SUKUN and harakat[i+1]==SUKUN:
				#no geminating
				new_word+=word_nm[i];
				word_nm=replace_pos(word_nm,word_nm[i],i+1)
				new_harakat+=FATHA;
				i+=1;
			else:

	# عندما يكون الحرف السابق ساكنا فإنه يستعيع
	#يض عن حركته بحركة الحرف الأول
				if i-1>=0 and new_harakat[i-1]==SUKUN:
					new_word+=word_nm[i]+SHADDA;
					if harakat[i]!=SUKUN:
						new_harakat=new_harakat[:-1]+harakat[i]+NOT_DEF_HARAKA+harakat[i+1];
					else:
						new_harakat=new_harakat[:-1]+FATHA+NOT_DEF_HARAKA+harakat[i+1];
	## يتم الإدغام إذا كان الحرف السابق ذو حركة طويلة
				elif i-1>=0 and new_harakat[i-1]in (ALEF_HARAKA,WAW_HARAKA,YEH_HARAKA):
					new_word+=word_nm[i]+SHADDA;
					new_harakat+=NOT_DEF_HARAKA+harakat[i+1];

				elif harakat[i]==SUKUN:
					new_word+=word_nm[i]+SHADDA;
					new_harakat+=NOT_DEF_HARAKA+harakat[i+1];
				else:
	## مؤقت حتى يتم حل المشكلة
					new_word+=word_nm[i]+SHADDA;
					new_harakat+=NOT_DEF_HARAKA+harakat[i+1];
	##TODO
	## منع الإدغام في بعض الحالات التي لا يمكن فيها الإدغام
	##مثل حالة سكتتا ، أي الحرفات متحركان وما قبلهاما متحرك
	## تم حل هذه المشكلة من خلال خوارزمية التجانس بين التصريفات
				i+=2;
		elif i>0 and i+1<length and word_nm[i+1]==word_nm[i] and harakat[i] ==SUKUN and harakat[i+1] in (FATHA, DAMMA, KASRA):
			# treat geminating case
			new_word+=word_nm[i]+SHADDA;
			new_harakat+=NOT_DEF_HARAKA+harakat[i+1];
			i+=2;
		else :
			new_word+=word_nm[i];
			new_harakat+=harakat[i];
			i+=1;
	return (new_word,new_harakat);


written_haraka={
ALEF_HARAKA:FATHA+ALEF,
ALEF_WAW_HARAKA:FATHA+ALEF,
ALEF_YEH_HARAKA:FATHA+ALEF,
WAW_HARAKA:DAMMA+WAW,
YEH_HARAKA:KASRA+YEH,
ALTERNATIVE_YEH_HARAKA:KASRA+YEH,
NOT_DEF_HARAKA:'',
FATHA: FATHA,
DAMMA:DAMMA,
KASRA:KASRA,
SUKUN:SUKUN,
SHADDA:SHADDA
}

#--------------------------------------
def standard2(word_nm, harakat):
	""" join the harakat and the letters to the give word in the standard script,
	it return one strings ( the word with harakat and the harakat).

	@param word_nm: given unvocalized word.
	@type word_nm: unicode.
	@param harakat: given harakat.
	@type harakat: unicode.
	@return: vocalized word.
	@rtype: unicode.
	"""
	if len(word_nm)!=len(harakat):
	##        print word_nm.encode("utf"), len(word_nm),write_harakat_in_full(harakat).encode("utf"), len(harakat);
		return u"";
	else:
		word=u"";
		i=0;
		word_nm,harakat=geminating(word_nm,harakat);
		if len(word_nm)!=len(harakat):
			return u"";
	## حالة عدم الابتداء بسكون
	##إذا كان الحرف الثاني مضموما  تكون الحركة الأولى مضمومة، وإلا تكون مكسورة
		if len(harakat)!=0 and harakat.startswith(SUKUN):
			word_nm=ALEF+word_nm
			if len(harakat)>=2 and harakat[1]in (DAMMA, WAW_HARAKA):
				harakat=DAMMA+harakat
			else:
				harakat=KASRA+harakat

	##        word_nm=tahmeez2(word_nm,harakat);
		if len(word_nm)!=len(harakat):
			return u"";
		word_before=word_nm;
		harakat_before=harakat;
		word_nm,harakat=homogenize(word_nm,harakat);
		if len(word_nm)!=len(harakat):
			print "len word: ",len(word_nm),  word_nm.encode('utf8'); 
			print "len harakat: ", len(harakat),repr(harakat);
			print repr(harakat_before), word_before.encode('utf8')
			return u"";
		word_nm=tahmeez2(word_nm,harakat);

		len_word_nm=len(word_nm);
		while i <len_word_nm:
			# للعمل :
	# هذه حالة الألف التي أصلها ياء
	# وقد استغنينا عنها بأن جعلنا الحرف الناقص من الفعل الناقص حرفا تاما
			if written_haraka.has_key(harakat[i]):
				word+=word_nm[i]+written_haraka[harakat[i]];
			else:
				word+=word_nm[i]+harakat[i];
			i+=1;

	#-	تحويل همزة القطع على الألف بعدها فتحة وهمزة القطع على الألف بعدها سكون إلى ألف ممدودة

	word=word.replace( u"%s%s%s"%(ALEF_HAMZA_ABOVE,FATHA,ALEF),ALEF_MADDA);
	word=word.replace( u"%s%s"%(ALEF_MADDA,FATHA),ALEF_MADDA);
	word=word.replace( u"%s%s"%(ALEF_MADDA,ALEF),ALEF_MADDA);
	word=word.replace( u"%s%s%s%s"%(ALEF_HAMZA_ABOVE,FATHA,ALEF_HAMZA_ABOVE,SUKUN),ALEF_MADDA);
	word=word.replace( u"%s%s%s%s"%(ALEF_HAMZA_ABOVE,FATHA,ALEF_HAMZA_ABOVE,FATHA),ALEF_MADDA);
	word=word.replace( u"%s%s%s%s"%(ALEF_HAMZA_ABOVE,DAMMA,WAW_HAMZA,SUKUN),ALEF_HAMZA_ABOVE+DAMMA+WAW);
	word=word.replace( u"%s%s%s%s"%(YEH,SHADDA,FATHA,ALEF_MAKSURA),YEH+SHADDA+FATHA+ALEF);
# إدغام النون الساكنة
	word=word.replace( u"%s%s%s"%(NOON,SUKUN,NOON),NOON+SHADDA);
# إذا كان الحرف الأول ساكنا وبعده شدة، ثم أضيفت إليه الألف
	word=word.replace( u"%s%s"%(SUKUN,SHADDA),SHADDA);
##  معالجة ألف التفريق
	word=word.replace( ALEF_WASLA,ALEF);
##  معالجة ألف التفريق
	word=word.replace( ALEF_MAMDUDA,ALEF);

##  معالجة ألف  الوصل الزائدة عند إضافتها إلى أول الفعل المثال
##	word=word.replace( u"%s%s%s%s"%(ALEF,DAMMA,YEH,SUKUN),ALEF+DAMMA+WAW);


	return word;


def tahmeez2(word_nm,harakat):
	""" Transform hamza on the standard script. in entry the word without harakat and the harakat seperately
	return the word with non uniform hamza.

	إعلال و إبدال الهمزة.
	@param word_nm: given unvocalized word.
	@type word_nm: unicode.
	@param harakat: given harakat.
	@type harakat: unicode.
	@return: (letters, harakat) after treatment.
	@rtype: tuple of unicode.
	"""

	# the harakat length != letters length
	if len(word_nm)!=len(harakat):
		return u"";
	# if no hamza, no tahmeez
	elif  word_nm.find(HAMZA)<0:
		return word_nm;
	else:
		ha2=u"";
		#eliminate some altenative of HARAKAT to standard.
		for h in harakat:
	##    	   if h==NOT_DEF_HARAKA:
	##    	       h=FATHA;
	##    	   elif h==ALEF_YEH_HARAKA or h==ALEF_WAW_HARAKA:
		   if h==ALEF_YEH_HARAKA or h==ALEF_WAW_HARAKA:
			   h=ALEF_HARAKA;
		   ha2+=h;
		harakat=ha2;
		word=u"";
		HAMZAT= u"إأءئؤ";
		for i in range(len(word_nm)):
			if word_nm[i] !=HAMZA and word_nm[i] !=ALEF_HAMZA_ABOVE:
				 word+=word_nm[i];
			else:
				if i==0:
					actual=harakat[i];
					swap= tab_tahmeez_initial[actual];
				else:
					before=harakat[i-1];
					actual=harakat[i];

					if i+1<len(word_nm):
	# if the hamza have shadda, it will take the harakat of shadda.
						if actual==NOT_DEF_HARAKA or actual==SUKUN:
							if word_nm[i+1]==SHADDA and harakat[i+1]!=SUKUN:
								actual=harakat[i+1];
						if before==NOT_DEF_HARAKA: before=FATHA;
						if actual==NOT_DEF_HARAKA: actual=FATHA;

						if  tab_tahmeez_middle.has_key(before) and  tab_tahmeez_middle[before].has_key(actual) :
							swap= tab_tahmeez_middle[before][actual];
						else :
	##	                	print (u"Middle : word %s in letter %s between '%s' and '%s'"%(word_nm,word_nm[i],before,actual)).encode("utf8");
							swap=word_nm[i];
					else :
						if before==NOT_DEF_HARAKA: before=FATHA;
						if actual==NOT_DEF_HARAKA: actual=FATHA;

						if  tab_tahmeez_final.has_key(before) and  tab_tahmeez_final[before].has_key(actual) :
							swap= tab_tahmeez_final[before][actual];
						else :
							swap=word_nm[i];
				word+=swap;
	return word;


# def treat_sukun2(word_nm, harakat, swaped_haraka=KASRA):
	# """ Treat the rencontre of sukun. in entry the word without harakat and the harakat seperately, and the probably haraka
	# return the new sequence of harakat

	# @param word_nm: given unvocalized word.
	# @type word_nm: unicode.
	# @param harakat: given harakat.
	# @type harakat: unicode.
	# @param  swaped_haraka: the swap haraka. الحركة المطبقة في الإعلال
	# @type swaped_haraka: unicode char, default KASRA.
	# @return: (letters, harakat).
	# @rtype: tuple of unicode.
	# """
	# len_word=len(word_nm);
	# len_harakat=len(harakat);
	# if len_word!=len_harakat:
		# return harakat;
	# else:
		# new_harakat=u"";
		# for i in range(len_word):
			# if harakat[i]==ALEF_HARAKA and i+1<len_harakat and harakat[i+1]==SUKUN:
	# #  other conditions
	# # إذا كان حرف الألف ثانيا مثل خاف يقلب كسرة،أما إذا كان ثالثا أو رابعا فيصبح فتحة، مثل خاف لا تخف
	# # حالة الألف بعدها حرف مشدد
				# if i+2<len_word and word_nm[i+2]==SHADDA:
					# new_harakat+=ALEF_HARAKA;
				# elif i==0 :
					# new_harakat+=KASRA;
				# else:
					# new_harakat+=FATHA;
			# elif harakat[i]==ALEF_YEH_HARAKA and i+1<len_harakat and harakat[i+1]==SUKUN:
	# #  other conditions
				# new_harakat+=KASRA;
			# elif harakat[i]==ALEF_WAW_HARAKA and i+1<len_harakat and harakat[i+1]==SUKUN:
	# #  other conditions
				# new_harakat+=DAMMA;
			# elif harakat[i]==WAW_HARAKA and i+1<len_harakat and harakat[i+1]==SUKUN:
				# #  other conditions
				# new_harakat+=DAMMA;
			# elif harakat[i]==YEH_HARAKA and i+1<len_harakat and harakat[i+1]==SUKUN:
				# #  other conditions
				# new_harakat+=KASRA;
			# elif harakat[i]==ALTERNATIVE_YEH_HARAKA and i+1<len_harakat and harakat[i+1]==SUKUN:
				# #  other conditions
				# new_harakat+=DAMMA;
			# else :
				# new_harakat+=harakat[i];
	# return new_harakat;
def treat_sukun2(word_nm, harakat, swaped_haraka=KASRA):
	""" Treat the rencontre of sukun. in entry the word without harakat and the harakat seperately, and the probably haraka
	return the new sequence of harakat

	@param word_nm: given unvocalized word.
	@type word_nm: unicode.
	@param harakat: given harakat.
	@type harakat: unicode.
	@param  swaped_haraka: the swap haraka. الحركة المطبقة في الإعلال
	@type swaped_haraka: unicode char, default KASRA.
	@return: (letters, harakat).
	@rtype: tuple of unicode.
	"""
	len_word=len(word_nm);
	len_harakat=len(harakat);
	# table of conversion if التقاء الساكنين
	conversionTable={
		ALEF_YEH_HARAKA:		KASRA,
		ALEF_WAW_HARAKA: 		DAMMA,
		WAW_HARAKA:				DAMMA,
		YEH_HARAKA :			KASRA,
		ALTERNATIVE_YEH_HARAKA:	DAMMA,
	}
	if len_word!=len_harakat:
		return harakat;
	else:
		new_harakat=u"";
		for i in range(len_word):
			if i+1<len_harakat and harakat[i+1]==SUKUN:
				if harakat[i]==ALEF_HARAKA:
					#  other conditions
					# إذا كان حرف الألف ثانيا مثل خاف يقلب كسرة،أما إذا كان ثالثا أو رابعا فيصبح فتحة، مثل خاف لا تخف
					# حالة الألف بعدها حرف مشدد
					if i+2<len_word and word_nm[i+2]==SHADDA:	new_harakat+=ALEF_HARAKA;
					elif i==0 :									new_harakat+=KASRA;
					else:										new_harakat+=FATHA;
				# if the actual haraka is in table use table conversion
				elif conversionTable.has_key(harakat[i]):
					new_harakat+=conversionTable[harakat[i]];
				else :
					new_harakat+=harakat[i];
			else :
				new_harakat+=harakat[i];
	return new_harakat;



def homogenize(word_nm,harakat):
	""" لإreat the jonction of WAW, YEH.
	معالجة التحولات التي تطرا على الياء أو الوا في وسط الكلمة أو في اخرها
	@param word_nm: given unvocalized word.
	@type word_nm: unicode.
	@param harakat: given harakat.
	@type harakat: unicode.
	@return: (letters, harakat)after treatment.
	@rtype: tuple of unicode.
	"""
	# inequal length between letters and harakat
	if len(word_nm)!=len(harakat):
		print "Homogenize:inequal length", len(word), len(harakat);
		return (word_nm, harakat);
	# word without weak letters doesn't need treatment
	elif not re.search(ur'[%s%s%s%s]'%(ALEF_MAKSURA,ALEF_MAMDUDA,YEH,WAW),word_nm):
		return (word_nm, harakat);
	# treatment
	else:
		new_harakat=harakat[0];
		new_word=word_nm[0];
		# نبدأ من الحرف الثاني لأن الحرف الأول لا يعالج
		i=1;
		## دراسة حالات الياء والواو قبل النهاية
		len_word_nm=len(word_nm);
		while i<len_word_nm-1:
			actualLetter=word_nm[i];			# Actual letter
			actualHaraka=harakat[i];			# Actual haraka
			if i-1>=0 :
				previousLetter=word_nm[i-1];	# previous letter
				previousHaraka=harakat[i-1];	# previous letter
			else:
				previousLetter='';
				previousHaraka='';
			if i+1<len_word_nm:
				nextLetter=word_nm[i+1];		# next letter
				nextHaraka=harakat[i+1];		# next haraka
			else:
				nextLetter='';
				nextHaraka='';
			# إذا كان الحرف التالي مضعف
			if i+2<len_word_nm and word_nm[i+2]==SHADDA:
				shadda_in_next=True;
			else:
				shadda_in_next=False;

			if  actualLetter==ALEF_MAKSURA or actualLetter==YEH:
			#إذا كانت الياء ساكنة أو مكسورة (كسرا قصيرا أو طويلا)، وكان ما قبلها مكسورا، يأخذ ماقبلها كسرة طويلة
			#مثال :
			# بِ +يْ => بِي
			#بِ +يِ  => بِي
			#بِ +يي => بِي

				if actualLetter==ALEF_MAKSURA and nextHaraka==SUKUN:
					new_harakat+=""
				elif  (actualHaraka in(SUKUN,KASRA,YEH_HARAKA)) and previousHaraka==KASRA and not shadda_in_next:
					new_harakat=new_harakat[:-1]+YEH_HARAKA
				elif  (actualHaraka in(KASRA)) and previousHaraka==KASRA and  shadda_in_next:
					new_harakat+=''
				# حالة هو تيسّر في المضارع المبني للمجهول
				elif  actualLetter==YEH and previousHaraka==DAMMA and actualHaraka ==DAMMA  and  shadda_in_next:
					#pass;
					new_harakat+=DAMMA;
					new_word+=YEH;
				# # مثل تؤدّينّ
				# elif  previousHaraka in (KASRA, FATHA) and actualHaraka ==DAMMA  and  shadda_in_next:
					# new_harakat+=FATHA;
					# new_word+=YEH;
				# ToDO review
				#سقّى، يُسقُّون
				elif  actualHaraka ==DAMMA  and  shadda_in_next:
					new_harakat=new_harakat[:-1]+DAMMA
				#تحويل الياء إلى واو ساكنة
				#2 - إذا كانت الياء مضمومة (ضما قصيرا أو طويلا)، وكان ما قبلها مفتوحا، تتحول الياء إلى واو ساكنة.
				#مثال :
				# بَ +يُ => بَِوْ
				#بَ +يو  => بَوْ

				elif (actualHaraka in (DAMMA, WAW_HARAKA))and  previousHaraka==FATHA and not shadda_in_next:
					new_harakat+=SUKUN
					new_word+=WAW;
				elif (actualHaraka in (DAMMA, WAW_HARAKA))and  previousHaraka==FATHA and shadda_in_next:
					new_harakat+=actualHaraka
					new_word+=WAW;
				#إذا كانت ساكنة، وماقبلها مضموما، ولم يكن ما بعدها ياء، أخذ ما قبلها ضمة طويلة.
				#مثال :
				# بُ +يُت =>بُوت

				#               elif  (harakat[i] in(SUKUN)) and i-1>=0 and harakat[i-1]==DAMMA and (i+1<len(word_nm) and word_nm[i+1]!=YEH)and ((i+1>=len(word_nm)or(i+1<len(word_nm) and (harakat[i+1] not in (SUKUN,NOT_DEF_HARAKA))))):

				elif  (actualHaraka ==SUKUN) and previousHaraka==DAMMA  and nextLetter!=YEH and not shadda_in_next:
					new_harakat=new_harakat[:-1]+WAW_HARAKA

				elif (actualHaraka ==YEH_HARAKA)and previousHaraka==FATHA:
					new_harakat+=SUKUN
					new_word+=YEH;
				elif  (actualHaraka ==WAW_HARAKA) and  previousHaraka==KASRA :
					new_harakat=new_harakat[:-1]+WAW_HARAKA

				else :
					new_harakat+=actualHaraka;
					new_word+=YEH;

			elif   actualLetter==ALEF_MAMDUDA or actualLetter==WAW:
				if actualLetter==ALEF_MAMDUDA and nextHaraka==SUKUN:
					new_harakat+=""
				elif actualLetter==ALEF_MAMDUDA and (actualHaraka in(SUKUN,DAMMA,WAW_HARAKA))and (previousHaraka==DAMMA) and not shadda_in_next:
					new_harakat=new_harakat[:-1]+WAW_HARAKA
				elif actualLetter==WAW and (actualHaraka in(SUKUN,DAMMA))and (previousHaraka==DAMMA) and not shadda_in_next:
					new_harakat=new_harakat[:-1]+WAW_HARAKA
				#تحويل الواو المضمومة  أو الطويلة إلى واو ساكنة
				elif  (actualHaraka in (DAMMA, WAW_HARAKA))and previousHaraka==FATHA :
					new_harakat+=SUKUN
					new_word+=WAW;
				# حالة وجع ايجع
				elif (actualHaraka ==(SUKUN))and (previousHaraka==KASRA)and not shadda_in_next:
					new_harakat=new_harakat[:-1]+YEH_HARAKA
				elif  (actualHaraka==KASRA)and shadda_in_next:
					new_harakat=new_harakat[:-1]+KASRA
				elif  actualLetter==ALEF_MAMDUDA and (actualHaraka==DAMMA)and shadda_in_next:
					new_harakat=new_harakat[:-1]+DAMMA
				elif  actualLetter==ALEF_MAMDUDA and (actualHaraka==YEH_HARAKA) and  not shadda_in_next:
					new_harakat=new_harakat[:-1]+YEH_HARAKA
				elif  actualLetter==WAW and (actualHaraka==DAMMA)and shadda_in_next:
					new_harakat+=DAMMA
					new_word+=WAW;
				else :
					new_harakat+=actualHaraka;
					new_word+=WAW;
			else:
				new_harakat+=actualHaraka;
				new_word+=actualLetter;
			i+=1;
	# end of while
	# we have to treat the last letter
	## دراسة حالة الحرف الأخير
		# Actual letter
		lastLetter=word_nm[i];
		# Actual haraka
		lastHaraka=harakat[i];
		if i-1>=0 :
			# previous letter
			previousLetter=word_nm[i-1];
			# previous haraka
			previousHaraka=harakat[i-1];
		else:
			previousLetter='';
			previousHaraka='';
		if  lastLetter==ALEF_MAKSURA or lastLetter==YEH :
			if  (lastHaraka in(KASRA,DAMMA))  and previousHaraka==KASRA:
				new_harakat=new_harakat[:-1]+YEH_HARAKA
			elif  (lastHaraka in(YEH_HARAKA)) and previousHaraka==KASRA :
				new_harakat=new_harakat[:-1]+YEH_HARAKA
			#حذف حركة الحرف الأخير إذا كان ساكنا
			elif (lastHaraka==SUKUN):
			## pass;
				new_harakat+='';
				new_word+='';
			elif  previousLetter==YEH and (lastHaraka in(KASRA,DAMMA,FATHA)) and previousHaraka==FATHA:
				new_harakat+=NOT_DEF_HARAKA
				new_word+=ALEF;
			elif  previousLetter!=YEH and (lastHaraka in(KASRA,DAMMA,FATHA)) and previousHaraka==FATHA:
				new_harakat+=NOT_DEF_HARAKA
				new_word+=ALEF_MAKSURA;
			elif  (lastHaraka in(WAW_HARAKA)) and previousHaraka==KASRA:
				new_harakat=new_harakat[:-1]+WAW_HARAKA
			#حالة تصريف الفعل الناقص في المضارع المجزوم مع أنت للمؤنث
			elif  (lastHaraka==YEH_HARAKA) and  previousHaraka==FATHA:
				new_harakat+=SUKUN
				new_word+=YEH;
			else :
				new_harakat+=lastHaraka;
				new_word+=YEH;

		elif lastLetter==ALEF_MAMDUDA :
			if (lastHaraka in(DAMMA,KASRA,WAW_HARAKA))and previousHaraka==DAMMA :
				new_harakat=new_harakat[:-1]+WAW_HARAKA
			##            if (lastHaraka in())and previousHaraka==DAMMA:
			##                new_harakat=new_harakat[:-1]+WAW_HARAKA
			elif (lastHaraka in(ALEF_HARAKA))and previousHaraka==DAMMA:
			##                pass;
				new_harakat=new_harakat[:-1]+YEH_HARAKA
			elif  (lastHaraka==YEH_HARAKA):
				new_harakat=new_harakat[:-1]+YEH_HARAKA
				new_word+='';
			elif (lastHaraka==SUKUN) and previousHaraka==KASRA :
				pass;

			elif (lastHaraka==SUKUN):
				new_harakat+='';
				new_word+='';
			elif (lastHaraka==FATHA)and previousHaraka==FATHA:
				new_harakat+=NOT_DEF_HARAKA;
				new_word+=ALEF_MAMDUDA;
			else :
				new_harakat+=lastHaraka;
				new_word+=WAW;
				#new_word+=ALEF_MAMDUDA;
		else:
			new_harakat+=harakat[i];
			new_word+=word_nm[i];
		return (new_word, new_harakat);


# def homogenize(word_nm,harakat):
	# """ لإreat the jonction of WAW, YEH.
	# معالجة التحولات التي تطرا على الياء أو الوا في وسط الكلمة أو في اخرها
	# @param word_nm: given unvocalized word.
	# @type word_nm: unicode.
	# @param harakat: given harakat.
	# @type harakat: unicode.
	# @return: (letters, harakat)after treatment.
	# @rtype: tuple of unicode.
	# """
	# if len(word_nm)!=len(harakat):
		# return (word_nm, harakat);
	# elif not re.search(ur'[%s%s%s%s]'%(ALEF_MAKSURA,ALEF_MAMDUDA,YEH,WAW),word_nm):
		# return (word_nm, harakat);
	# else:
		# new_harakat=harakat[0];
		# new_word=word_nm[0];
	# # نبدأ من الحرف الثاني لأن الحرف الأول لا يعالج
		# i=1;
	# ## دراسة حالات الياء والواو قبل النهاية
		# len_word_nm=len(word_nm);
		# while i<len_word_nm-1:
			# # Actual letter
			# actualLetter=word_nm[i];
			# # Actual haraka
			# actualHaraka=harakat[i];
			# if i-1>=0 :
				# # previous letter
				# previousLetter=word_nm[i-1];
				# # previous haraka
				# previousHaraka=harakat[i-1];
			# else:
				# previousLetter='';
				# previousHaraka='';
			# if i+1<len_word_nm:
				# # next letter
				# nextLetter=word_nm[i+1];
				# # next haraka
				# nextHaraka=harakat[i+1];
			# else:
				# nextLetter='';
				# nextHaraka='';
	# # إذا كان الحرف التالي مضعف
			# if i+2<len_word_nm and word_nm[i+2]==SHADDA:
				# shadda_in_next=True;
			# else:
				# shadda_in_next=False;


			# if  actualLetter==ALEF_MAKSURA or actualLetter==YEH :
	# #إذا كانت الياء ساكنة أو مكسورة (كسرا قصيرا أو طويلا)، وكان ما قبلها مكسورا، يأخذ ماقبلها كسرة طويلة
	# #مثال :
	# # بِ +يْ => بِي
	# #بِ +يِ  => بِي
	# #بِ +يي => بِي

				# if actualLetter==ALEF_MAKSURA and nextHaraka==SUKUN:
					# new_harakat+=""
				# elif  (actualHaraka in(SUKUN,KASRA,YEH_HARAKA)) and previousHaraka==KASRA and not shadda_in_next:
					# new_harakat=new_harakat[:-1]+YEH_HARAKA
				# elif  (actualHaraka in(KASRA)) and previousHaraka==KASRA and  shadda_in_next:
					# new_harakat+=''
				# elif  (actualHaraka in(DAMMA)) and  shadda_in_next:
					# new_harakat=new_harakat[:-1]+DAMMA
	# #تحويل الياء إلى واو ساكنة
	# #2 - إذا كانت الياء مضمومة (ضما قصيرا أو طويلا)، وكان ما قبلها مفتوحا، تتحول الياء إلى واو ساكنة.
	# #مثال :
	# # بَ +يُ => بَِوْ
	# #بَ +يو  => بَوْ

				# elif (actualHaraka in (DAMMA, WAW_HARAKA))and  previousHaraka==FATHA and not shadda_in_next:
					# new_harakat+=SUKUN
					# new_word+=WAW;
				# elif (actualHaraka in (DAMMA, WAW_HARAKA))and  previousHaraka==FATHA and shadda_in_next:
					# new_harakat+=actualHaraka
					# new_word+=WAW;
	# #إذا كانت ساكنة، وماقبلها مضموما، ولم يكن ما بعدها ياء، أخذ ما قبلها ضمة طويلة.
	# #مثال :
	# # بُ +يُت =>بُوت

	# #               elif  (harakat[i] in(SUKUN)) and i-1>=0 and harakat[i-1]==DAMMA and (i+1<len(word_nm) and word_nm[i+1]!=YEH)and ((i+1>=len(word_nm)or(i+1<len(word_nm) and (harakat[i+1] not in (SUKUN,NOT_DEF_HARAKA))))):

				# elif  (actualHaraka ==SUKUN) and previousHaraka==DAMMA  and nextLetter!=YEH and not shadda_in_next:
					# new_harakat=new_harakat[:-1]+WAW_HARAKA

				# elif (actualHaraka ==YEH_HARAKA)and previousHaraka==FATHA:
					# new_harakat+=SUKUN
					# new_word+=YEH;
				# elif  (actualHaraka ==WAW_HARAKA) and  previousHaraka==KASRA :
					# new_harakat=new_harakat[:-1]+WAW_HARAKA

				# else :
					# new_harakat+=actualHaraka;
					# new_word+=YEH;

			# elif   actualLetter==ALEF_MAMDUDA or actualLetter==WAW:
				# if actualLetter==ALEF_MAMDUDA and nextHaraka==SUKUN:
					# new_harakat+=""
				# elif actualLetter==ALEF_MAMDUDA and (actualHaraka in(SUKUN,DAMMA,WAW_HARAKA))and (previousHaraka==DAMMA) and not shadda_in_next:
					# new_harakat=new_harakat[:-1]+WAW_HARAKA
				# elif actualLetter==WAW and (actualHaraka in(SUKUN,DAMMA))and (previousHaraka==DAMMA) and not shadda_in_next:
					# new_harakat=new_harakat[:-1]+WAW_HARAKA
	# ##تحويل الواو المضمومة  أو الطويلة إلى واو ساكنة
				# elif  (actualHaraka in (DAMMA, WAW_HARAKA))and previousHaraka==FATHA :
					# new_harakat+=SUKUN
					# new_word+=WAW;

	# # حالة وجع ايجع
				# elif (actualHaraka ==(SUKUN))and (previousHaraka==KASRA)and not shadda_in_next:
					# new_harakat=new_harakat[:-1]+YEH_HARAKA
				# elif  (actualHaraka==KASRA)and shadda_in_next:
					# new_harakat=new_harakat[:-1]+KASRA
				# elif  actualLetter==ALEF_MAMDUDA and (actualHaraka==DAMMA)and shadda_in_next:
					# new_harakat=new_harakat[:-1]+DAMMA
				# elif  actualLetter==ALEF_MAMDUDA and (actualHaraka==YEH_HARAKA) and  not shadda_in_next:
					# new_harakat=new_harakat[:-1]+YEH_HARAKA
				# elif  actualLetter==WAW and (actualHaraka==DAMMA)and shadda_in_next:
					# new_harakat+=DAMMA
					# new_word+=WAW;
				# else :
					# new_harakat+=actualHaraka;
					# new_word+=WAW;
			# else:
				# new_harakat+=actualHaraka;
				# new_word+=actualLetter;
			# i+=1;
	# # end of while
	# # we have to treat the last letter
	# ## دراسة حالة الحرف الأخير
		# # Actual letter
		# lastLetter=word_nm[i];
		# # Actual haraka
		# lastHaraka=harakat[i];
		# if i-1>=0 :
			# # previous letter
			# previousLetter=word_nm[i-1];
			# # previous haraka
			# previousHaraka=harakat[i-1];
		# else:
			# previousLetter='';
			# previousHaraka='';
		# if  lastLetter==ALEF_MAKSURA or lastLetter==YEH :
			# if  (lastHaraka in(KASRA,DAMMA))  and previousHaraka==KASRA:
				# new_harakat=new_harakat[:-1]+YEH_HARAKA
			# elif  (lastHaraka in(YEH_HARAKA)) and previousHaraka==KASRA :
				# new_harakat=new_harakat[:-1]+YEH_HARAKA
	# #حذف حركة الحرف الأخير إذا كان ساكنا
			# elif (lastHaraka==SUKUN):
	# ##                pass;
				# new_harakat+='';
				# new_word+='';
			# elif  previousLetter==YEH and (lastHaraka in(KASRA,DAMMA,FATHA)) and previousHaraka==FATHA:
				# new_harakat+=NOT_DEF_HARAKA
				# new_word+=ALEF;
			# elif  previousLetter!=YEH and (lastHaraka in(KASRA,DAMMA,FATHA)) and previousHaraka==FATHA:
				# new_harakat+=NOT_DEF_HARAKA
				# new_word+=ALEF_MAKSURA;
			# elif  (lastHaraka in(WAW_HARAKA)) and previousHaraka==KASRA:
				# new_harakat=new_harakat[:-1]+WAW_HARAKA
	# #حالة تصريف الفعل الناقص في المضارع المجزوم مع أنت للمؤنث
			# elif  (lastHaraka==YEH_HARAKA) and  previousHaraka==FATHA:
				# new_harakat+=SUKUN
				# new_word+=YEH;
			# else :
				# new_harakat+=lastHaraka;
				# new_word+=YEH;

		# elif lastLetter==ALEF_MAMDUDA :
			# if (lastHaraka in(DAMMA,KASRA,WAW_HARAKA))and previousHaraka==DAMMA :
				# new_harakat=new_harakat[:-1]+WAW_HARAKA
	# ##            if (lastHaraka in())and previousHaraka==DAMMA:
	# ##                new_harakat=new_harakat[:-1]+WAW_HARAKA
			# elif (lastHaraka in(ALEF_HARAKA))and previousHaraka==DAMMA:
	# ##                pass;
				# new_harakat=new_harakat[:-1]+YEH_HARAKA
			# elif  (lastHaraka==YEH_HARAKA):
				# new_harakat=new_harakat[:-1]+YEH_HARAKA
				# new_word+='';
			# elif (lastHaraka==SUKUN) and previousHaraka==KASRA :
				# pass;

			# elif (lastHaraka==SUKUN):
				# new_harakat+='';
				# new_word+='';
			# elif (lastHaraka==FATHA)and previousHaraka==FATHA:
				# new_harakat+=NOT_DEF_HARAKA;
				# new_word+=ALEF_MAMDUDA;
			# else :
				# new_harakat+=lastHaraka;
				# new_word+=WAW;
				# #new_word+=ALEF_MAMDUDA;
		# else:
			# new_harakat+=harakat[i];
			# new_word+=word_nm[i];
		# return (new_word, new_harakat);



def is_triliteral_verb(verb):
	""" Test if the verb is  triliteral,
	used in selectionof verbs from the triliteral verb dictionnary
	@param verb: given verb.
	@type verb: unicode.
	@return: True if the verb is triliteral.
	@rtype: Boolean.
	"""
	verb_nm=araby.stripHarakat(verb);
	verb_nm=verb_nm.replace(ALEF_MADDA,HAMZA+ALEF);
	if len(verb_nm)==3:
		return True;
	else : return False;



def find_triliteral_verb(db_base_path, triliteralverb, givenharaka):
	"""
	Find the triliteral verb in the dictionary,
	return a list of possible verb forms
	@param db_base_path: the database path
	@type db_base_path: path string.
	@param triliteralverb: given verb.
	@type triliteralverb: unicode.
	@param givenharaka: given haraka of tuture type of the verb.
	@type givenharaka: unicode.
	@return: list of triliteral verbs.
	@rtype: list of unicode.
	"""
	liste=[];
	try:
#     db_path=os.path.join(_base_directory(req),"data/verbdict.db")
		db_path=os.path.join(db_base_path,"data/verbdict.db")
		conn = sqlite.connect(db_path)
		c = conn.cursor()
		verb_nm=araby.stripHarakat(triliteralverb)
		t=(verb_nm,)
		c.execute('select verb_vocalised,haraka,transitive from verbdict where verb_unvocalised=?',t)
		for row in c:
			verb_vocalised=row[0];
			haraka=row[1]
			transitive=row[2]
            # Return the transitivity option
            #MEEM is transitive
            # KAF is commun ( transitive and intransitive)
            # LAM is intransitive
			if transitive in (KAF,MEEM): transitive=True;
			else:transitive=False;
# if the given verb is the list, it will be inserted in the top of the list, to be treated in prior
			if triliteralverb==verb_vocalised and givenharaka==haraka:
				liste.insert(0,{"verb":verb_vocalised,"haraka":haraka,"transitive":transitive})
# else the verb is appended in the liste
			else:
				liste.append({"verb":verb_vocalised,"haraka":haraka,"transitive":transitive})
		c.close();
		return liste;
	except:
		return None;



from triverbtable import *
TriVerbTable_INDEX={};

def create_index_triverbtable():
	""" Create index from the verb dictionary
	to accelerate the search in the dictionary for verbs
	@return: create the TriVerbTable_INDEX;
	@rtype: None;
	"""
	# the key is the vocverb + the bab number
	for key in TriVerbTable.keys():
		vocverb=TriVerbTable[key]['verb'];
		unvverb=araby.stripHarakat(vocverb);
		normverb=araby.normalizeHamza(unvverb);
		if TriVerbTable_INDEX.has_key(normverb):
			TriVerbTable_INDEX[normverb].append(key);
		else:
			TriVerbTable_INDEX[normverb]=[key,];



def find_alltriverb(triverb, givenharaka=FATHA,VocalisedEntree=False):
	"""
	Find the triliteral verb in the dictionary (TriVerbTable)
	return a list of possible verb forms
	each item contains:
		- 'root':
		- 'haraka:
		- 'bab':
		- 'transitive':
	@param triverb: given verb.
	@type triverb: unicode.
	@param givenharaka: given haraka of tuture type of the verb, default(FATHA).
	@type givenharaka: unicode.
	@param VocalisedEntree: True if the given verb is vocalized, default False.
	@type VocalisedEntree: Boolean.
	@return: list of triliteral verbs.
	@rtype: list of dicts.
	"""
	liste=[];

	if VocalisedEntree: verb_nm=araby.stripHarakat(triverb);
	else:
		verb_nm=triverb;

	normalized=araby.normalizeHamza(verb_nm);
	if TriVerbTable_INDEX.has_key(normalized):
		for verb_voc_id in TriVerbTable_INDEX[normalized]:
			if triverb==TriVerbTable[verb_voc_id]['verb'] and givenharaka==TriVerbTable[verb_voc_id]['haraka']:
				liste.insert(0,TriVerbTable[verb_voc_id])
#			if VocalisedEntree:
				#if verb_voc_id[:-1]==triverb:
				#	liste.append(TriVerbTable[verb_voc_id]);
			else:
				liste.append(TriVerbTable[verb_voc_id]);
	else:
		print "triverb has no verb";
	return liste;


