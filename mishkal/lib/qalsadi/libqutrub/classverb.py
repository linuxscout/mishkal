#!/usr/bin/python
# -*- coding=utf-8 -*-

#************************************************************************
# $Id: classverb.py,v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2009, Arabtechies, Arabeyes Taha Zerrouki
#
#  The Main class to do the conjugation
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
Verb Class for conjugation
@author: Taha Zerrouki
@contact: taha dot zerrouki at gmail dot com
@copyright: Arabtechies, Arabeyes,  Taha Zerrouki
@license: GPL
@date:2009/06/02
@version: 0.9
"""
import copy
# from ar_ctype import *
import sys
import re
import string
import pyarabic.araby as araby
from ar_verb import *
from verb_const import *
from conjugatedisplay import *


class conjug_stem:
	"""
	A Class to represent a conjugated stem
	"""
	# بنية جذع تصريف الجذع
	#تتكون من الزمن، الحروف والحركات
	# تستعمل لتخزين جذوع التصريف
	tense=u"";
	""" the actual tense"""
	letters=u"";
	""" letters of the conjugated stem"""
	marks=u"";
	""" marks of the conjugated stem"""	
	def __init__(self,tense,letters,marks):
		""" 
		init method
		@param tense: the given tense;
		@type tense: unicode.
		@param letters: the word letters;
		@type letters: unicode.		
		@param marks: the word marks; 
		@type marks: unicode.		
		"""
		self.tense=tense;
		self.letters=letters;
		self.marks=marks;
# a global cache for verbs conjigation
cacheStandard={'standard':{},
					'sukun':{},
					'suffix':{}}
class verbclass:
	"""
	Verb Class: represent a verb, prepare it to be conjugated and store the conjugation result
	"""
	verb=u"";
	#" internl verb : is the normalized form of the verb"
	internal_verb=u"";
	word_letters=u"";
	word_marks=u"";
	unvocalized=u"";
	vlength=0;
	vtype=u"";
	future_type=u'';
	transitive=u"";
	hamza_zaida=False;
	#deprecated
	# teh_zaida=False;
	future_form=u"";
	conj_display=None;
	tab_conjug_stem=None;

#---------------------------------------------------------------------------
	def __init__(self,verb,transitive, future_type=FATHA):
		""" 
		init method
		@param verb: the given verb;
		@type verb: unicode.
		@param transitive: the verb is transitive or not;
		@type transitive: Boolean.		
		@param future_type: The mark of the third radical letter in the verb, used for triletiral verb only. Default value is Fatha; 
		@type future_type: unicode; one arabic letter (Fatha, Damma, Kasra).		
		"""	
		self.verb=verb;
		# this cache is used to avoid duplicated operatioon in standardisation, treat_sukun, and uniformate suffix
		self.cacheStandard=cacheStandard;#{'standard':{},
					#'sukun':{},
					#'suffix':{}}
		self.internal_verb=normalize(verb);
		self.future_type=future_type;
		(self.word_letters,self.word_marks)=uniformate_verb(verb);
        #Before last haraka in the past
		self.past_haraka=araby.secondlastChar(self.word_marks);
		self.word_marks=uniformate_alef_origin(self.word_marks,self.internal_verb,self.future_type);

		self.transitive=transitive;
		self.hamza_zaida=False;
		# self.teh_zaida=False;

##		self.conj_display.add_attribut(u"الكتابة الداخلية للفعل",self.word_letters+" - "+self.word_marks);
		self.tab_conjug_stem={};
		verb=self.verb;
##		root=self.root;
		tab_type=[u"",u"",u"",u"فعل ثلاثي",u"فعل رباعي",u"فعل خماسي",u"فعل سداسي",u"فعل سباعي",u"فعل ثماني",u"فعل تساعي"];
		verb=normalize(verb);

		self.unvocalized=araby.stripHarakat(verb);
		verb_nm=self.unvocalized;
		self.vlength=len(verb_nm);
		self.vtype=tab_type[self.vlength];

        # الهمزة زائدة
		self.hamza_zaida=self.is_hamza_zaida(verb_nm);

        # التاء الزائدة
		#deprecated
		#self.teh_zaida=self.is_teh_zaida(verb_nm);

        # معالجة حالة الأفعال الشاذة
        # إذا كان الفعل من الشواذ، استخرجنا جذوع التصريف من جدوله
        #وإلا ولّدنا جذوع تصريفه
        # في المضارع والأمر فقط
        # أما الماضي فليس فيه شذوذ
		self.prepare_past_stem();
		self.prepare_passive_past_stem();
		if self.is_irregular_verb():
		    self.prepare_irregular_future_and_imperative_stem();

		else:
		    self.prepare_future_and_imperative_stem();


		# display object
		self.conj_display=conjugatedisplay(self.verb);
		if self.transitive  :
		    self.conj_display.add_attribut(u"اللزوم/التعدي",u"متعدي");
		else :
		    self.conj_display.add_attribut(u"اللزوم/التعدي",u"لازم");
		self.conj_display.add_attribut(u"الفعل",self.verb);
		self.conj_display.add_attribut(u"نوع الفعل",self.vtype);#+str(self.vlength));
		self.future_form=self.conjugate_tense_pronoun(TenseFuture,PronounHuwa);
		self.conj_display.set_future_form(self.future_form);
		if self.transitive : self.conj_display.settransitive();
		self.conj_display.setbab(self.future_type);


	def __del__(self):
		"""
		Delete instance 
		
		"""
		self.conj_display=None;
		self.tab_conjug_stem=None;


#####################################
#{ Attributes functions
#####################################
	def set_display(self, mode='Text'):
		""" 
		Set the display mode as:
			- 'Text':
			- 'HTML':
			- 'HTMLColoredDiacritics':
			- 'DICT':
			- 'CSV':
			- 'GUI':
			- 'TABLE':
			- 'XML':
			- 'TeX':
			- 'ROWS':
		@param mode: the given mode to display result;
		"""		
		self.conj_display.setmode(mode)
#-------------------------------------------------------------------------------------
	def get_conj_display(self):
		"""
		Get The conjugation display class with result.
		@return: an object with result.
		@rtype: conjugatedisplay class;
		"""
		return copy.copy(self.conj_display)
#####################################
#{ Extract information from verb functions
#####################################
		#deprecated
	# def is_teh_zaida(self, verb_normalized_unvocalized):
		# """
		# Determine if the verb starts with Teh and the Teh is not original like تفاعل, 
		# Tafa3ala. The verb starting by adde teh change the first vowel of teh, the  future mark will be fatha, else kasra, e.g: yatafa3'a'lu (teh added), yafta3'i'lu ( non added teh);
		# @param verb_normalized_unvocalized: the unvovalized form f the verb.
		# @type verb_normalized_unvocalized: unicde;
		# @return: return True if the start Teh is not original
		# @rtype: boolean; 
		# """
		# # How to deterine that Teh is Added:
		# # rule : Teh is added, if the verb is 5 letters lenght and starts by Teh
		# #الناء الأولى زائدة في الفعل الخماسي مطلقا
		# # لا يمكن أن يكون الفعل الخماسي مبدوءا بتاء أصلية،
	 
		# return ( len(verb_normalized_unvocalized)==5 and verb_normalized_unvocalized.startswith(TEH))


	def is_hamza_zaida(self, verb_normalized_unvocalized):
		"""
		Function to determine if the first HAMZA in the verb is not original
		ترجع إذا كانت الهمزة الأولى في الفعل غير أصليةDetermine if the verb starts with Hamza and the Teh is not original like أضرب
		@param verb_normalized_unvocalized: the unvovalized form f the verb.
		@type verb_normalized_unvocalized: unicde;
		@return: return True if the start Teh is not original
		@rtype: boolean; 
		"""
	# if the lenght of verb is exactely 4 letters and starts by hamza
	# and it is in the AF3Al wazn and not FA33al or FAA3la
	# ألوزن المعني هو أفعل
	# الأوزان غير المعنية هي فاعل وفعّل
	# الأوزان المشتقة هي أفعّ من أفعل
	# الخلاصة أن يكون الفعل رباعيا، حرفه الأول همزة
	# ولا يكون حرفه الثاني ألف، لمنع الوزن فاعل
	# ولا يكون حرفه الثالث شدة، لمنع الوزن فعّل
		verb=verb_normalized_unvocalized;
		if len(verb)!=4 or  not verb.startswith(HAMZA) :return False;
		elif len(verb)==4 and verb.startswith(HAMZA) and verb[1]!=ALEF and verb[2]!=SHADDA:
				return True;
		else : return False;

	def homogenize_harakat(self,original_harakat,applied_harakat):
		""" 
		Treat Harakat to be homogenized with letters in conjugation.
		إذا كان طول الحركات ألأصلية للفعل أقل من طول حركات الماضي المبني للمجهول
		هذا يعني وجود حركة طويلة
		نقوم بتحويل الحركة الطويلة إلى ما يوافقها

		@param original_harakat: given original harakatof the verb.
		@type original_harakat: unicode.
		@param applied_harakat: given harakat to be applied to  verb.
		@type applied_harakat: unicode.	
		@return: nesw harakat to be applied to the verb.
		@rtype: unicode.
		"""	
		marks=original_harakat;
		new_marks=applied_harakat;
#  إذا كان طول الحركات ألأصلية للفعل أقل من طول حركات الماضي المبني للمجهول
# هذا يعني وجود حركة طويلة
# نقوم بتحويل الحركة الطويلة إلى ما يوافقها
		if len(marks)<len(new_marks):
			alef_haraka_pos=marks.find(ALEF_HARAKA);
			if alef_haraka_pos<0:
				alef_haraka_pos=marks.find(ALEF_WAW_HARAKA);
			if alef_haraka_pos<0:
				alef_haraka_pos=marks.find(ALEF_YEH_HARAKA);
			if alef_haraka_pos>=0 and alef_haraka_pos+1<len(new_marks):
				first=new_marks[alef_haraka_pos];
				second=new_marks[alef_haraka_pos+1];
				changed_haraka=tab_homogenize_alef_haraka[first][second];
				new_marks=new_marks[:alef_haraka_pos]+changed_haraka+new_marks[alef_haraka_pos+2:]
		return new_marks;		
#####################################
#{ Preparing  conjugation stems for every tense functions
#####################################

	def prepare_future_and_imperative_stem(self):
		"""
		Prepare the conjugation stems for future tenses (future, jussive, subjective) and imperative tense. Those stems will be concatenated with conjugation affixes. This function store results in self.tab_conjug_stem. This function prepare conjugation stems for the following tenses:
			- TenseFuture :  تصريف الفعل المضارع 
			- TenseJussiveFuture : تصريف الفعل المضارع المجزوم 
			- TenseSubjunctiveFuture : تصريف الفعل المضارع المنصوب 
			- TenseConfirmedFuture: المضارع المؤكد الثقيل
			- TensePassiveFuture :تصريف الفعل المضارع المبني للمجهول
			- TensePassiveJussiveFuture: تصريف الفعل المضارع المجزوم المني للمجهول
			- TensePassiveSubjunctiveFuture:تصريف الفعل المضارع المنصوب 
			- TensePassiveConfirmedFuture:المضارع المؤكد الثقيل المنبي للمجهول
			- TenseImperative:الفعل الامر
			- TenseConfirmedImperative: الفعل الامر المؤكد.
		"""
		letters=self.word_letters;
		marks=self.word_marks;
		future_letters=letters;
		# حالة الفعل الثلاثي
		if self.vlength==3:
			first_future_mark=FATHA;
			first_passive_future_mark=DAMMA;
			future_marks=SUKUN+self.future_type+FATHA;
			passive_future_marks=SUKUN+FATHA+FATHA;
		# معالجة الفعل المثال الواوي
		#ToDO

		# الفعل الرباعي
		elif self.vlength==4:
			first_future_mark=DAMMA;
			first_passive_future_mark=DAMMA;
			future_marks=FATHA+SUKUN+KASRA+DAMMA;
			passive_future_marks=FATHA+SUKUN+FATHA+DAMMA;
		# الفعل الخماسي
		elif self.vlength==5:
			first_future_mark=FATHA;
			first_passive_future_mark=DAMMA;
			if letters.startswith(TEH):
				future_marks=FATHA+FATHA+SUKUN+FATHA+DAMMA;
				passive_future_marks=FATHA+FATHA+SUKUN+FATHA+DAMMA;
			else :
				future_marks=FATHA+SUKUN+FATHA+KASRA+DAMMA;
				passive_future_marks=FATHA+SUKUN+FATHA+FATHA+DAMMA;
		#الفعل السداسي
		elif self.vlength==6:
			first_future_mark=FATHA;
			first_passive_future_mark=DAMMA;
			future_marks=FATHA+SUKUN+FATHA+SUKUN+KASRA+DAMMA;
			passive_future_marks=FATHA+SUKUN+FATHA+SUKUN+FATHA+DAMMA;
		# معالجة الألفات في الفعل والحركات الطويلة
		#  إذا كان طول الحركات ألأصلية للفعل أقل من طول حركات الماضي المبني للمجهول
		# هذا يعني وجود حركة طويلة
		# نقوم بتحويل الحركة الطويلة إلى ما يوافقها
		if len(marks)<len(future_marks):
			future_marks=self.homogenize_harakat(marks,future_marks)
			passive_future_marks=self.homogenize_harakat(marks,passive_future_marks)
		imp_marks=future_marks;
		imp_letters=future_letters;
        # حالة الأفعال التي تبدأ بألف وصل
		if letters.startswith(ALEF) or self.hamza_zaida:
			future_letters=letters[1:];
			future_marks=future_marks[1:]
			passive_future_marks=passive_future_marks[1:];
			passive_letters=letters[1:];
        # حالة الفعل المثال
		elif self.vlength==3 and self.word_letters.startswith(WAW) and (self.future_type==KASRA or  (self.future_type==FATHA and self.word_marks==FATHA+FATHA+FATHA and not self.word_letters.endswith(SHADDA))):
			future_letters=letters[1:];
			future_marks=future_marks[1:]
##			passive_future_marks=passive_future_marks[1:]
			passive_letters=letters;
		else:
			future_letters=letters;
			passive_letters=letters;
		new_marks=first_future_mark+future_marks;
		passive_marks=first_passive_future_mark+passive_future_marks;

        # حالة الأفعال التي تبدأ بألف وصل
		if imp_letters.startswith(ALEF):
			imp_letters=letters[1:];
			imp_marks=imp_marks[1:]
		elif self.vlength==3 and self.word_letters.startswith(WAW) and (self.future_type==KASRA or (self.future_type==FATHA and self.word_marks==FATHA+FATHA+FATHA)):
			imp_letters=letters[1:];
			imp_marks=imp_marks[1:]
		else:
			imp_letters=letters;

		# معالجة الفعل الناقص عند تصريفه في المجهول
		# تستبدل واو التاقص الذي حركة عين ماضيه فتحة بياء
##		passive_letters=future_letters;
		if self.vlength==3 and passive_letters.endswith(ALEF_MAMDUDA):
			passive_letters=passive_letters[:-1]+ALEF_MAKSURA;
		#  القعل الأمر يأخذ نفس حركات الفعل المضارع دون حركة حرف المضارعة
##		imp_marks=future_marks;
		### معلجة إضافة حرف ألف الوصل في الأفعال المسبوقة بالسكون
##		new_marks=first_future_mark+future_marks;
##		passive_marks=first_passive_future_mark+passive_future_marks;
		self.tab_conjug_stem[TenseFuture]=conjug_stem(TenseFuture,future_letters,new_marks);
		# تصريف الفعل المضارع المنصوب والمجزوم
		self.tab_conjug_stem[TenseJussiveFuture]=conjug_stem(TenseJussiveFuture,future_letters,new_marks);
		self.tab_conjug_stem[TenseSubjunctiveFuture]=conjug_stem(TenseSubjunctiveFuture,future_letters,new_marks);
		# المضارع المؤكد الثقيل
		self.tab_conjug_stem[TenseConfirmedFuture]=conjug_stem(TenseConfirmedFuture,future_letters,new_marks);

        # المبني للمجهول
  		self.tab_conjug_stem[TensePassiveFuture]=conjug_stem(TensePassiveFuture,passive_letters,passive_marks);
		# تصريف الفعل المضارع المنصوب والمجزوم المني للمجهول
		self.tab_conjug_stem[TensePassiveJussiveFuture]=conjug_stem(TensePassiveJussiveFuture,passive_letters,passive_marks);
		self.tab_conjug_stem[TensePassiveSubjunctiveFuture]=conjug_stem(TensePassiveSubjunctiveFuture,passive_letters,passive_marks);
		# المضارع المؤكد الثقيل المنبي للمجهول
		self.tab_conjug_stem[TensePassiveConfirmedFuture]=conjug_stem(TensePassiveConfirmedFuture,passive_letters,passive_marks);

		# الفعل الامر
		self.tab_conjug_stem[TenseImperative]=conjug_stem(TenseImperative,imp_letters,imp_marks);
		# الفعل الامر المؤكد
		self.tab_conjug_stem[TenseConfirmedImperative]=conjug_stem(TenseConfirmedImperative,imp_letters,imp_marks);

#	--------------------------------------------------------------------------
	def prepare_past_stem(self):
		"""
		Prepare the conjugation stems for past tense.
		Those stems will be concatenated with conjugation affixes.
		This function store results in self.tab_conjug_stem. This function prepare conjugation stems for the following tenses:
			- TensePast: الفعل الماضي.
		"""	
		self.past_stem=self.internal_verb;
		self.tab_conjug_stem[TensePast]=conjug_stem(TensePast,self.word_letters,self.word_marks);


	def prepare_passive_past_stem(self):
		"""
		Prepare the conjugation stems for past tense.
		Those stems will be concatenated with conjugation affixes.
		This function store results in self.tab_conjug_stem. This function prepare conjugation stems for the following tenses:
			- TensePast: الفعل الماضي
		"""		
##		verb=self.internal_verb;
		letters=self.word_letters;
		marks=self.word_marks;

		if len(letters)==3 and letters.endswith(ALEF_MAMDUDA) and marks[1]==FATHA:
			letters=letters[:-1]+ALEF_MAKSURA;
		if self.vlength==3:
			passive_marks=DAMMA+KASRA+FATHA;
		elif self.vlength==4:
			passive_marks=DAMMA+SUKUN+KASRA+FATHA;
		elif self.vlength==5:
			if letters.startswith(TEH):
				passive_marks=DAMMA+DAMMA+SUKUN+KASRA+FATHA;
			else :
				passive_marks=DAMMA+SUKUN+DAMMA+KASRA+FATHA;
		elif self.vlength==6:
			passive_marks=DAMMA+SUKUN+DAMMA+SUKUN+KASRA+FATHA;
#  إذا كان طول الحركات ألأصلية للفعل أقل من طول حركات الماضي المبني للمجهول
# هذا يعني وجود حركة طويلة
# نقوم بتحويل الحركة الطويلة إلى ما يوافقها
		if len(marks)<len(passive_marks):
			passive_marks=self.homogenize_harakat(marks,passive_marks)

# -	حالة الفعل الأجوف الذي حركة مضارعه فتحة أو كسرة،
#-	فيصبح في الماضي عند التقاء الساكنين كسرة، لذا يجب تعديل ذلك في الماضي المجهول، بجعلها تتحول إلى ضمة عند التقاء الساكنين.
		if len(passive_marks)==2 and passive_marks[0]==YEH_HARAKA and  self.future_type in(FATHA,KASRA):
			passive_marks=ALTERNATIVE_YEH_HARAKA+FATHA;
		self.tab_conjug_stem[TensePassivePast]=conjug_stem(TensePassivePast,letters,passive_marks);

	def conjugate_tense_pronoun(self,tense,pronoun):
		"""
		Conjugate a verb in a given tense with a pronoun.
		@param tense: given tense;
		@type tense: unicode name of the tense;
		@param pronoun: given pronoun;
		@type pronoun: unicode name of the pronoun;
		@return: conjugated verb;
		@rtype: unicode;		
		"""
        #prefix
		pre_val=TableTensePronoun[tense][pronoun][0];
        #suffix
		suf_val=TableTensePronoun[tense][pronoun][1];
		stem_l=self.tab_conjug_stem[tense].letters;
		stem_m=self.tab_conjug_stem[tense].marks;
#deprecated
##		return self.join(stem_l,stem_m,prefix,suffix);
        # _m : marks
        #_l :letters
		if pre_val!=u"":
			pre_val_l=pre_val;
			pre_val_m=stem_m[0];
			stem_m=stem_m[1:];
		else:
			pre_val_l=u"";
			pre_val_m=u"";

        # the suffix already start by a HARAKA,
        # we add Taweel to ensure valid word in the uniformate function
		suf_val=TATWEEL+suf_val;
        #uniformate suffix
		# the case is used to avoid duplicated staddization
		if self.cacheStandard['suffix'].has_key( suf_val): 
			(suf_val_l,suf_val_m)=self.cacheStandard['suffix'][suf_val]
		else:
			(suf_val_l,suf_val_m)=uniformate_suffix(suf_val);
			self.cacheStandard['suffix'][suf_val]=(suf_val_l,suf_val_m)
        # add affix to the stem
		conj_l=pre_val_l+stem_l+suf_val_l;
		#The end of the stem marks takes the begining of the suffix marks
		conj_m=pre_val_m+stem_m[:-1]+suf_val_m;
        # the begining of suffix letters is Tatweel, it will be striped
		conj_l=pre_val_l+stem_l+suf_val_l[1:];

        # Treat sukun
		# the case is used to avoid duplicated staddization
		keyCache=u'-'.join([conj_l, conj_m]);
		if self.cacheStandard['sukun'].has_key(keyCache):
			conj_m=self.cacheStandard['sukun'][keyCache];
		else:
			conj_m = treat_sukun2(conj_l,conj_m,self.future_type);
			self.cacheStandard['sukun'][keyCache] =conj_m;
        # standard orthographic form
		# the case is used to avoid duplicated staddization
		keyCache=u'-'.join([conj_l, conj_m]);
		if self.cacheStandard['standard'].has_key(keyCache):
			conj=self.cacheStandard['standard'][keyCache];
		else:	
			conj = standard2(conj_l,conj_m);
			self.cacheStandard['standard'][keyCache]=conj;
		return conj;


#--------------------------------------------------------------------------------
# التصريف في الأزمنة المختلفة،
# عند وضع قائمة خاصة بالأزمنة المختارة،
# تلقائيا كافة الأزمنة
#--------------------------------------------------------------------------------
	def conjugate_all_tenses(self,listtense=TableTense):
		"""
		Conjugate a verb  with a list of tenses.
		@param listtense: given tense;
		@type listtense: list of unicode;
		@return: conjugated verb ;
		@rtype: the type is given according to the display mode;		
		"""	
		for tense in listtense:
			if tense==TensePast:
					conj_ana=self.conjugate_tense_pronoun(tense,PronounAna);
					self.conj_display.add(tense,PronounAna,conj_ana);
					conj_ana_without_last_mark=conj_ana[:-1];
					self.conj_display.add(tense,PronounAnta,conj_ana_without_last_mark+FATHA);
					self.conj_display.add(tense,PronounAnti,conj_ana_without_last_mark+KASRA);
					self.conj_display.add(tense,PronounAntuma,conj_ana+MEEM+FATHA+ALEF);
					self.conj_display.add(tense,PronounAntuma_f,conj_ana+MEEM+FATHA+ALEF);
					self.conj_display.add(tense,PronounAntum,conj_ana+MEEM);
					self.conj_display.add(tense,PronounAntunna,conj_ana+NOON+SHADDA+FATHA)
					self.conj_display.add(tense,PronounAna,conj_ana);

					conj_nahnu=self.conjugate_tense_pronoun(tense,PronounNahnu);
					self.conj_display.add(tense,PronounNahnu,conj_nahnu);

					conj_hunna=self.conjugate_tense_pronoun(tense,PronounHunna);
					self.conj_display.add(tense,PronounHunna,conj_hunna);

					conj_huma=self.conjugate_tense_pronoun(tense,PronounHuma);
					self.conj_display.add(tense,PronounHuma,conj_huma);

					conj_hum=self.conjugate_tense_pronoun(tense,PronounHum);
					self.conj_display.add(tense,PronounHum,conj_hum);

					conj_hunna=self.conjugate_tense_pronoun(tense,PronounHunna);
					self.conj_display.add(tense,PronounHunna,conj_hunna);

					conj_huwa=self.conjugate_tense_pronoun(tense,PronounHuwa);
					self.conj_display.add(tense,PronounHuwa,conj_huwa);
					conj_hya=self.conjugate_tense_pronoun(tense,PronounHya);
					self.conj_display.add(tense,PronounHya,conj_hya);
					self.conj_display.add(tense,PronounHuma_f,conj_hya[:-1]+FATHA+ALEF);
			elif tense ==TensePassivePast:
					conj_ana=self.conjugate_tense_pronoun(tense,PronounAna);
					self.conj_display.add(tense,PronounAna,conj_ana);
					conj_ana_without_last_mark=conj_ana[:-1];
					self.conj_display.add(tense,PronounAnta,conj_ana_without_last_mark+FATHA);
					self.conj_display.add(tense,PronounAnti,conj_ana_without_last_mark+KASRA);
					self.conj_display.add(tense,PronounAntuma,conj_ana+MEEM+FATHA+ALEF);
					self.conj_display.add(tense,PronounAntuma_f,conj_ana+MEEM+FATHA+ALEF);
					self.conj_display.add(tense,PronounAntum,conj_ana+MEEM);
					self.conj_display.add(tense,PronounAntunna,conj_ana+NOON+SHADDA+FATHA)
					self.conj_display.add(tense,PronounAna,conj_ana);

					conj_nahnu=self.conjugate_tense_pronoun(tense,PronounNahnu);
					self.conj_display.add(tense,PronounNahnu,conj_nahnu);

					conj_hunna=self.conjugate_tense_pronoun(tense,PronounHunna);
					self.conj_display.add(tense,PronounHunna,conj_hunna);

					conj_hunna=self.conjugate_tense_pronoun(tense,PronounHunna);
					self.conj_display.add(tense,PronounHunna,conj_hunna);

					conj_huwa=self.conjugate_tense_pronoun(tense,PronounHuwa);
					self.conj_display.add(tense,PronounHuwa,conj_huwa);
# حالة الفعل مهموز الآخر
					if conj_huwa.endswith(YEH+HAMZA+FATHA) :
					   self.conj_display.add(tense,PronounHya,conj_huwa[:-2]+YEH_HAMZA+FATHA+TEH+SUKUN);
					   self.conj_display.add(tense,PronounHuma_f,conj_huwa[:-2]+YEH_HAMZA+FATHA+TEH+FATHA+ALEF);
##					   conj_huma=self.conjugate_tense_pronoun(tense,PronounHuma);
					   self.conj_display.add(tense,PronounHuma,conj_huwa[:-2]+YEH_HAMZA+FATHA+ALEF);

##					   conj_hum=self.conjugate_tense_pronoun(tense,PronounHum);
					   self.conj_display.add(tense,PronounHum,conj_huwa[:-2]+YEH_HAMZA+DAMMA+WAW+ALEF);

					else :
					   self.conj_display.add(tense,PronounHya,conj_huwa+TEH+SUKUN);
					   self.conj_display.add(tense,PronounHuma_f,conj_huwa+TEH+FATHA+ALEF);
					   self.conj_display.add(tense,PronounHuma,conj_huwa+ALEF);
					   if conj_huwa.endswith(KASRA+YEH+FATHA):
					       self.conj_display.add(tense,PronounHum,conj_huwa[:-3]+DAMMA+WAW+ALEF);
					   else:
					       self.conj_display.add(tense,PronounHum,conj_huwa[:-1]+DAMMA+WAW+ALEF);
			elif tense in (TenseFuture,TensePassiveFuture,TenseJussiveFuture,TenseSubjunctiveFuture,TenseConfirmedFuture,TensePassiveJussiveFuture,TensePassiveSubjunctiveFuture,TensePassiveConfirmedFuture):
					conj_ana=self.conjugate_tense_pronoun(tense,PronounAna);
					self.conj_display.add(tense,PronounAna,conj_ana);

					conj_anta=self.conjugate_tense_pronoun(tense,PronounAnta);
					self.conj_display.add(tense,PronounAnta,conj_anta);
					conj_anta_without_future_letter=conj_anta[1:];
##					self.conj_display.add(tense,PronounAnta,TEH+conj_ana_without_future_letter);
					self.conj_display.add(tense,PronounNahnu,NOON+conj_anta_without_future_letter);
					self.conj_display.add(tense,PronounHuwa,YEH+conj_anta_without_future_letter);
					self.conj_display.add(tense,PronounHya,TEH+conj_anta_without_future_letter);

					conj_anti=self.conjugate_tense_pronoun(tense,PronounAnti);
					self.conj_display.add(tense,PronounAnti,conj_anti);

					conj_antuma=self.conjugate_tense_pronoun(tense,PronounAntuma);
					self.conj_display.add(tense,PronounAntuma,conj_antuma);
					self.conj_display.add(tense,PronounAntuma_f,conj_antuma);
					self.conj_display.add(tense,PronounHuma_f,conj_antuma);
					self.conj_display.add(tense,PronounHuma,YEH+conj_antuma[1:]);

					conj_antum=self.conjugate_tense_pronoun(tense,PronounAntum);
					self.conj_display.add(tense,PronounAntum,conj_antum);
					self.conj_display.add(tense,PronounHum,YEH+conj_antum[1:]);

					conj_antunna=self.conjugate_tense_pronoun(tense,PronounAntunna);
					self.conj_display.add(tense,PronounAntunna,conj_antunna);
					self.conj_display.add(tense,PronounHunna,YEH+conj_antunna[1:]);
			elif tense ==TenseImperative or  tense ==TenseConfirmedImperative:
				for pron in  ImperativePronouns:
					conj=self.conjugate_tense_pronoun(tense,pron);
					self.conj_display.add(tense,pron,conj);
		if not self.transitive:
			for tense in TablePassiveTense:
				for pron in PronounsTableNotPassiveForUntransitive:
					self.conj_display.add(tense,pron,u"");
# if the result is not diplyed directely on the screen, we return it
		result=self.conj_display.display(self.conj_display.mode,listtense);
		if result: return result;






#--------------------------------------------------------------------------------
	def conjugateTenseForPronoun(self,tense, pronoun):
		"""
		Conjugate a verb  for a pronoun in specific tense, 
		we use an homoginized conjugation 
		@param tense: given tense;
		@type tense: unicode;
		@param pronoun: given pronoun;
		@type pronoun: unicode;
		@return: conjugated verb ;
		@rtype: unicode;		
		"""
		# the idea is to generate some conjugation from others
		#  in particalar cases, we can generate conjugation  from others pronouns.
		#  for each tense we have two pronouns lists: 
		#	- direct conjugated pronouns.
		#	- indirect conjugated pronouns.

		if tense==TensePast:
			# direct concongated pronouns
			if pronoun in (PronounAna,  PronounNahnu, PronounHunna, PronounHuma ,PronounHum, PronounHunna, PronounHuwa, PronounHya):
				conj = self.conjugate_tense_pronoun( tense, pronoun);
				self.conj_display.add(tense, pronoun, conj);
			# indirect conjugation
			# from Aana Pronoun
			elif pronoun in (PronounAnta, PronounAnta, PronounAnti, PronounAntuma, PronounAntuma_f, PronounAntum, PronounAntunna):
				# test if the verb is conjugated 
				conj_ana = self.conj_display.getConj(tense, pronoun);
				if conj_ana == u"":
					conj_ana = self.conjugate_tense_pronoun(tense, PronounAna);
				conj_ana_without_last_mark=conj_ana[:-1];
				if pronoun == PronounAnta:
					self.conj_display.add(tense, PronounAnta ,conj_ana_without_last_mark+FATHA);
				elif pronoun == PronounAnti:
					self.conj_display.add(tense, PronounAnti ,conj_ana_without_last_mark+KASRA);
				elif pronoun == PronounAntuma :
					self.conj_display.add(tense, PronounAntuma ,conj_ana+MEEM+FATHA+ALEF);
				elif pronoun == PronounAntuma_f:
					self.conj_display.add(tense, PronounAntuma_f ,conj_ana+MEEM+FATHA+ALEF);
				elif pronoun == PronounAntum:
					self.conj_display.add(tense, PronounAntum ,conj_ana+MEEM);
				elif pronoun == PronounAntunna:
					self.conj_display.add(tense, PronounAntunna ,conj_ana+NOON+SHADDA+FATHA)

			# indirect conjugation
			# from  Hya Pronoun
			elif pronoun ==  PronounHuma_f:
				# test if the verb is conjugated 
				conj_hya = self.conj_display.getConj(tense, PronounHya);
				if conj_hya == u"":
					conj_hya = self.conjugate_tense_pronoun(tense, PronounHya);
				self.conj_display.add(tense, PronounHuma_f,conj_hya[:-1]+FATHA+ALEF);
		elif tense ==TensePassivePast:
				# direct conjugation
				if pronoun in (PronounAna, PronounNahnu, PronounHunna,  PronounHunna, PronounHuwa):
					conj = self.conjugate_tense_pronoun(tense, pronoun);
					self.conj_display.add(tense, pronoun, conj);
				# indirect conjugation
				# Ana pronoun like conjugation
				elif pronoun in (PronounAnta, PronounAnti, PronounAntuma, PronounAntuma_f, PronounAntum, PronounAntunna):
					conj_ana = self.conj_display.getConj(tense, PronounAna);
					if conj_ana == u"":
						conj_ana = self.conjugate_tense_pronoun(tense, PronounAna);
						self.conj_display.add(tense, PronounAna, conj_ana);	
					conj_ana_without_last_mark=conj_ana[:-1];
					if pronoun == PronounAnta:
						self.conj_display.add(tense, PronounAnta, conj_ana_without_last_mark+FATHA);
					elif pronoun == PronounAnti:
						self.conj_display.add(tense, PronounAnti, conj_ana_without_last_mark+KASRA);
					elif pronoun == PronounAntuma:
						self.conj_display.add(tense, PronounAntuma, conj_ana+MEEM+FATHA+ALEF);
					elif pronoun == PronounAntuma_f:
						self.conj_display.add(tense, PronounAntuma_f, conj_ana+MEEM+FATHA+ALEF);
					elif pronoun == PronounAntum:
						self.conj_display.add(tense, PronounAntum, conj_ana+MEEM);
					elif pronoun == PronounAntunna:
						self.conj_display.add(tense, PronounAntunna, conj_ana+NOON+SHADDA+FATHA)
				# indirect conjugation
				# Ana pronoun like conjugation
				elif pronoun in ( PronounHya, PronounHuma_f, PronounHuma, PronounHum):
					conj_huwa= self.conj_display.getConj(tense, PronounHuwa);
					if conj_huwa == u"":
						conj_huwa = self.conjugate_tense_pronoun(tense, PronounHuwa);
						self.conj_display.add(tense, PronounHuwa, conj_huwa);
# حالة الفعل مهموز الآخر
					if conj_huwa.endswith(YEH+HAMZA+FATHA) :
					   self.conj_display.add(tense,PronounHya,conj_huwa[:-2]+YEH_HAMZA+FATHA+TEH+SUKUN);
					   self.conj_display.add(tense,PronounHuma_f,conj_huwa[:-2]+YEH_HAMZA+FATHA+TEH+FATHA+ALEF);
	##					   conj_huma=self.conjugate_tense_pronoun(tense,PronounHuma);
					   self.conj_display.add(tense,PronounHuma,conj_huwa[:-2]+YEH_HAMZA+FATHA+ALEF);

	##					   conj_hum=self.conjugate_tense_pronoun(tense,PronounHum);
					   self.conj_display.add(tense,PronounHum,conj_huwa[:-2]+YEH_HAMZA+DAMMA+WAW+ALEF);

					else :
					   self.conj_display.add(tense,PronounHya, conj_huwa+TEH+SUKUN);
					   self.conj_display.add(tense,PronounHuma_f, conj_huwa+TEH+FATHA+ALEF);
					   self.conj_display.add(tense,PronounHuma,conj_huwa+ALEF);
					   if conj_huwa.endswith(KASRA+YEH+FATHA):
					       self.conj_display.add(tense,PronounHum,conj_huwa[:-3]+DAMMA+WAW+ALEF);
					   else:
					       self.conj_display.add(tense,PronounHum,conj_huwa[:-1]+DAMMA+WAW+ALEF);
		elif tense in (TenseFuture,TensePassiveFuture,TenseJussiveFuture,TenseSubjunctiveFuture,TenseConfirmedFuture,TensePassiveJussiveFuture,TensePassiveSubjunctiveFuture,TensePassiveConfirmedFuture):

			# direct pronouns conjugations
			if pronoun in (PronounAna, PronounAnta,  PronounAnti, PronounAntuma, PronounAntum, PronounAntunna):
				conj=self.conjugate_tense_pronoun(tense, pronoun);
				self.conj_display.add(tense, pronoun, conj);
			# indirect pronouns
			# Anta pronouns conjugation like
			elif pronoun in (PronounNahnu, PronounHuwa, PronounHya):
				conj_anta = self.conj_display.getConj(tense, PronounAnta)
				if conj_anta == u"":
					conj_anta = self.conjugate_tense_pronoun(tense,PronounAnta);
					self.conj_display.add(tense,PronounAnta,conj_anta);

				conj_anta_without_future_letter=conj_anta[1:];
				if pronoun == PronounNahnu:
##					self.conj_display.add(tense,PronounAnta,TEH+conj_ana_without_future_letter);
					self.conj_display.add(tense,PronounNahnu,NOON+conj_anta_without_future_letter);
				elif pronoun == PronounHuwa:
					self.conj_display.add(tense,PronounHuwa,YEH+conj_anta_without_future_letter);
				elif pronoun == PronounHya:
					self.conj_display.add(tense,PronounHya,TEH+conj_anta_without_future_letter);

			# indirect pronouns
			# Antuma pronouns conjugation like
			elif pronoun in (PronounAntuma, PronounAntuma_f, PronounHuma, PronounHuma_f ):
				conj_antuma = self.conj_display.getConj(tense, PronounAntuma)
				if conj_antuma == u"":
					conj_antuma=self.conjugate_tense_pronoun(tense,PronounAntuma);
					self.conj_display.add(tense,PronounAntuma,conj_antuma);
				if pronoun == PronounAntuma_f:
					self.conj_display.add(tense,PronounAntuma_f,conj_antuma);
				if pronoun == PronounHuma_f:
					self.conj_display.add(tense,PronounHuma_f,conj_antuma);
				if pronoun == PronounHuma:
					self.conj_display.add(tense,PronounHuma,YEH+conj_antuma[1:]);


			# indirect pronouns
			# Antum pronouns conjugation like
			elif pronoun == PronounHum:
				conj_antum = self.conj_display.getConj(tense, PronounAntum)
				if conj_antum == u"":
					conj_antum=self.conjugate_tense_pronoun(tense,PronounAntum);
					self.conj_display.add(tense,PronounAntum,conj_antum);
				self.conj_display.add(tense,PronounHum,YEH+conj_antum[1:]);


			# indirect pronouns
			# Antum pronouns conjugation like
			elif pronoun == PronounHunna:
				conj_antunna = self.conj_display.getConj(tense, PronounAntunna)
				if conj_antunna == u"":
					conj_antunna=self.conjugate_tense_pronoun(tense, PronounAntunna);
					self.conj_display.add(tense, PronounAntunna, conj_antunna);
				self.conj_display.add(tense,PronounHunna,YEH+conj_antunna[1:]);
		elif tense == TenseImperative or  tense == TenseConfirmedImperative:
			conj=self.conjugate_tense_pronoun(tense, pronoun);
			self.conj_display.add(tense, pronoun, conj);
		# the cnjugated form is stored in cnj_display
		return self.conj_display.getConj(tense, pronoun);
#####################################
#{ Irregular verbs functions
#####################################		
#--------------------------------------------------------

#
#--------------------------------------------------------
	def is_irregular_verb(self):
		"""
		Return True if the verb is irregular, founded in the irregular verb table
		إرجاع إّذا كان الفعل ضاذا.
		الأفعال العربية الخاصة هي
		رأى، أكل أمر سأل،
		ج- إذا كان يتصرف من باب (مَنَعَ يَمْنَعُ)، تحذف واوه, نحو: وَضَعَ، يَضَعُ، وَجَأَ يَجَأُ، وَدَعَ يَدَعُ، وَزَعَ يَزَعُ، وَضَأَ يَضَأُ، وَطَأَ يَطَأُ، وَقَعَ يَقَعُ، وَلَغَ يَلَغُ، وَهَبَ يَهَبُ، عدا خمسة أفعال هي: (وَبَأ)، و(وَبَهَ)، و(وَجَعَ)، و(وَسَعَ)، و(وَهَلَ)، فلا تحذف منها الواو؛ فنقول: يَوْبَأُ، يَوْبَهُ، يَوْجَعُ، يَوْسَعُ، يَوْهَلُ.  الأفعال (وَبَأ)، و(وَبَهَ)، و(وَجَعَ)، و(وَسَعَ)، و(وَهَلَ)، الفعل وبَأ يوبأ
		
		@return:True if irregular;
		@rtype: Boolean;
		"""		
		if len(self.word_letters)!=3: return False;
		else:
			# the key is composed from the letters and past and future marks, to identify irregular verb
			key=self.word_letters+self.past_haraka+self.future_type
			if IrregularVerbsConjug.has_key(key ):
				return True;
	##	            if self.past_haraka== IrregularVerbsConjug[self.word_letters][ConjugBab][0] and self.future_type== IrregularVerbsConjug[self.word_letters][ConjugBab][1]:
	##	                return True;
		return False;

	def get_irregular_future_stem(self):
		"""
		Get the future stem for irregular verb.
		@return: the future conjuagtion stem;
		@rtype: unicode;		
		"""		
	  # the key is composed from the letters and past and future marks, to identify irregular verb
		key=self.word_letters+self.past_haraka+self.future_type
		if  IrregularVerbsConjug.has_key(key):
			return IrregularVerbsConjug[key][TenseFuture];
		else:
			self.word_letters
#--------------------------------------------------------
	def get_irregular_passivefuture_stem(self):
		"""
		Get the passive future stem for irregular verb.
		@return: the passive future conjuagtion stem;
		@rtype: unicode;		
		"""		
      # the key is composed from the letters and past and future marks, to identify irregular verb
		key=self.word_letters+self.past_haraka+self.future_type
		if IrregularVerbsConjug.has_key(key):
			return IrregularVerbsConjug[key][TensePassiveFuture];
		else:
			self.word_letters
#--------------------------------------------------------
	def get_irregular_imperative_stem(self):
		"""
		Get the imperative stem for irregular verb.
		@return: the passive imperative conjuagtion stem;
		@rtype: unicode;		
		"""		
      # the key is composed from the letters and past and future marks, to identify irregular verb
		key=self.word_letters+self.past_haraka+self.future_type
		if  IrregularVerbsConjug.has_key(key):
			return IrregularVerbsConjug[key][TenseImperative];
		else:
			self.word_letters

#--------------------------------------------------------
# prepare the irregular conjug for future and imperative
# تحضير جذوع التصريف في المضارع والأمر للأفعال الضاذة
#
#--------------------------------------------------------
	def prepare_irregular_future_and_imperative_stem(self):
		"""
		Prepare the conjugation stems for future tenses (future, jussive, subjective) and imperative tense.
		Those stems will be concatenated with conjugation affixes.
		"""			
		##	   if self.word_letters in IrregularVerbsConjug.keys():
		if self.is_irregular_verb():
			(l,m)=self.get_irregular_future_stem();
			#IrregularVerbsConjug[self.word_letters][TenseFuture];
			#تمت إضافة حركة حرف المضارعة إلى الجذع المستعمل في الفعل الشاذ
			self.tab_conjug_stem[TenseFuture]=conjug_stem(TenseFuture,l,m);
			self.tab_conjug_stem[TenseJussiveFuture]=conjug_stem(TenseJussiveFuture,l,m);
			self.tab_conjug_stem[TenseSubjunctiveFuture]=conjug_stem(TenseSubjunctiveFuture,l,m);
			self.tab_conjug_stem[TenseConfirmedFuture]=conjug_stem(TenseConfirmedFuture,l,m);


			(l1,m1)=self.get_irregular_passivefuture_stem();
			#تمت إضافة حركة حرف المضارعة إلى الجذع المستعمل في الفعل الشاذ
			self.tab_conjug_stem[TensePassiveFuture]=conjug_stem(TensePassiveFuture,l1,m1);
			self.tab_conjug_stem[TensePassiveJussiveFuture]=conjug_stem(TensePassiveJussiveFuture,l1,m1);
			self.tab_conjug_stem[TensePassiveSubjunctiveFuture]=conjug_stem(TensePassiveSubjunctiveFuture,l1,m1);
			self.tab_conjug_stem[TensePassiveConfirmedFuture]=conjug_stem(TensePassiveConfirmedFuture,l1,m1);


			(l2,m2)=self.get_irregular_imperative_stem();
			self.tab_conjug_stem[TenseImperative]=conjug_stem(TenseImperative,l2,m2);
			self.tab_conjug_stem[TenseConfirmedImperative]=conjug_stem(TenseConfirmedImperative,l2,m2);
		##	       print l.encode("utf"),m.encode("utf");
		return False;

#-----------------------------------------------------
	def getConj(self,tense, pronoun):
		"""
		Get the conjugated verb by tense and pronoun.
		@param tense: tense of the added conjuagtion.
		@type tense: unicode;
		@param pronoun: pronoun of the added conjuagtion.
		@type pronoun: unicode;
		@return : conjugated form of verb if exists.
		@rtype : unicode;
		
		"""
		return self.conj_display.getConj(tense, pronoun);

