#!/usr/bin/python
# -*- coding=utf-8 -*-
#---
#************************************************************************
# $Id: verb_const.py, v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2009, Arabtechies, Arabeyes Taha Zerrouki
#
#  List of constants used in the arabic verb conjugation
#
# -----------------
# Revision Details:
# -----------------
#  $Date: 2009/06/02 01:10:00 $
#  $Author: Taha Zerrouki $
#  $Revision: 0.7 $
#  $Source: arabtechies.sourceforge.net
#
#***********************************************************************/
"""
Arabic Qutrub verb conjugation, verb_const file
"""
from pyarabic.araby import FATHA, DAMMA, KASRA, SHADDA, SUKUN, HAMZA, ALEF, \
 NOON, ALEF_WASLA, WAW, ALEF_HAMZA_ABOVE, ALEF_HAMZA_BELOW, ALEF_MADDA, \
 YEH_HAMZA, WAW_HAMZA, TATWEEL, SMALL_ALEF, SMALL_YEH, SMALL_WAW, YEH, \
 ALEF_MAKSURA

import re

PronounsTable = (u"أنا" , u"نحن" , u"أنت" , u"أنتِ" , u"أنتما" , 
 u"أنتما مؤ" , u"أنتم" , u"أنتن" , u"هو" , u"هي" , u"هما" ,
  u"هما مؤ" , u"هم" , u"هن")
PronounsTableNotPassiveForUntransitive = (u"أنا" , u"نحن" , u"أنت" ,
 u"أنتِ" , u"أنتما" , u"أنتما مؤ" , u"أنتم" , u"أنتن" , u"هما" ,
  u"هما مؤ" , u"هم" , u"هن")
PronounAna = u"أنا"
PronounNahnu = u"نحن"
PronounAnta = u"أنت"
PronounAnti = u"أنتِ"
PronounAntuma = u"أنتما"
PronounAntuma_f = u"أنتما مؤ"
PronounAntum = u"أنتم"
PronounAntunna = u"أنتن"
PronounHuwa = u"هو"
PronounHya = u"هي"
PronounHuma = u"هما"
PronounHuma_f = u"هما مؤ"
PronounHum = u"هم"
PronounHunna = u"هن"
PRONOUN_FEATURES = {
 u"أنا" : {'person':u'متكلم', 'gender':u'', 'number': u'مفرد'} 
, u"أنت" : {'person':u'مخاطب', 'gender':u'مذكر', 'number': u'مفرد'} 
, u"أنتِ" : {'person':u'مخاطب', 'gender':u'مؤنث', 'number': u'مفرد'} 
, u"هو" : {'person':u'غائب', 'gender':u'مذكر', 'number': u'مفرد'} 
, u"هي" : {'person':u'غائب', 'gender':u'مؤنث', 'number': u'مفرد'} 
, u"أنتما" : {'person':u'مخاطب', 'gender':u'مذكر', 'number': u'مثنى'} 
, u"أنتما مؤ" : {'person':u'مخاطب', 'gender':u'مؤنث', 'number': u'مثنى'} 
, u"هما" : {'person':u'غائب', 'gender':u'مذكر', 'number': u'مثنى'}
, u"هما مؤ" : {'person':u'غائب', 'gender':u'مؤنث', 'number': u'مثنى'} 
, u"نحن" : {'person':u'متكلم', 'gender':u'', 'number': u'جمع'}
, u"أنتم" : {'person':u'مخاطب', 'gender':u'مذكر', 'number': u'جمع'}
, u"أنتن" : {'person':u'مخاطب', 'gender':u'مؤنث', 'number': u'جمع'}
, u"هم" : {'person':u'غائب', 'gender':u'مذكر', 'number': u'جمع'}
, u"هن" : {'person':u'غائب', 'gender':u'مؤنث', 'number': u'جمع'}
}

ImperativePronouns = (u"أنت" , u"أنتِ" , u"أنتما" , u"أنتما مؤ" , u"أنتم" 
             , u"أنتن" )
# const for Tense Name
TensePast = u"الماضي المعلوم"
TenseFuture = u"المضارع المعلوم"
TenseImperative = u"الأمر"
TenseConfirmedImperative = u"الأمر المؤكد"
TenseJussiveFuture = u"المضارع المجزوم"
TenseSubjunctiveFuture = u"المضارع المنصوب"
TenseConfirmedFuture = u"المضارع المؤكد الثقيل"


TensePassivePast =  u"الماضي المجهول"
TensePassiveFuture = u"المضارع المجهول"
TensePassiveJussiveFuture = u"المضارع المجهول المجزوم"
TensePassiveSubjunctiveFuture = u"المضارع المجهول المنصوب"
TensePassiveConfirmedFuture = u"المضارع المؤكد الثقيل المجهول "


TABLE_TENSE = [TensePast, TenseFuture, TenseJussiveFuture, 
        TenseSubjunctiveFuture, TenseConfirmedFuture, TenseImperative, 
        TenseConfirmedImperative, 
        TensePassivePast, TensePassiveFuture, 
        TensePassiveJussiveFuture, TensePassiveSubjunctiveFuture,
         TensePassiveConfirmedFuture]
TableIndicativeTense = [TensePast, TenseFuture, TenseJussiveFuture, 
             TenseSubjunctiveFuture, TenseConfirmedFuture, TenseImperative, 
        TenseConfirmedImperative]
TablePassiveTense = [TensePassivePast, TensePassiveFuture, 
        TensePassiveJussiveFuture, TensePassiveSubjunctiveFuture,
        TensePassiveConfirmedFuture]

TENSE_FEATURES = {
TensePast : { 'tense':u'ماضي', 'voice':u'معلوم', 'mood':u'', 'confirmed':u'', },
TenseFuture : { 'tense':u'مضارع', 'voice':u'معلوم', 'mood':u'مرفوع', 'confirmed':u'', },
TenseImperative : { 'tense':u'أمر', 'voice':u'', 'mood':u'', 'confirmed':u'', },
TenseConfirmedImperative : { 'tense':u'أمر', 'voice':u'', 'mood':u'', 'confirmed':u'مؤكذ', },
TenseJussiveFuture : { 'tense':u'مضارع', 'voice':u'معلوم', 'mood':u'مجزوم', 'confirmed':u'', },
TenseSubjunctiveFuture : { 'tense':u'مضارع', 'voice':u'معلوم', 'mood':u'منصوب', 'confirmed':u'', },
TenseConfirmedFuture : { 'tense':u'مضارع', 'voice':u'معلوم', 'mood':u'', 'confirmed':u'مؤكد', },


TensePassivePast :  { 'tense':u'ماضي', 'voice':u'مجهول', 'mood':u'', 'confirmed':u'', },
TensePassiveFuture : { 'tense':u'مضارع', 'voice':u'مجهول', 'mood':u'مرفوع', 'confirmed':u'', },
TensePassiveJussiveFuture : { 'tense':u'مضارع', 'voice':u'مجهول', 'mood':u'مجزوم', 'confirmed':u'', },
TensePassiveSubjunctiveFuture : { 'tense':u'مضارع', 'voice':u'مجهول', 'mood':u'منصوب', 'confirmed':u'', }, 
TensePassiveConfirmedFuture : { 'tense':u'مضارع', 'voice':u'مجهول', 'mood':u'', 'confirmed':u'مؤكد', },
}

past = {
 u"أنا" : [u"", u"ْتُ"]
, u"أنت" : [u"", u"ْتَ"]
, u"أنتِ" : [u"", u"ْتِ"]
, u"هو" : [u"", u"َ"]
, u"هي" : [u"", u"َتْ"]
, u"أنتما" : [u"", u"ْتُما"]
, u"أنتما مؤ" : [u"", u"ْتُما"]
, u"هما" : [u"", u"َا"]
, u"هما مؤ" : [u"", u"َتَا"]
, u"نحن" : [u"", u"ْنَا"]
, u"أنتم" : [u"", u"ْتُم"]
, u"أنتن" : [u"", u"ْتُنَّ"]
##, u"هم" : [u"", u"ُوا"]
, u"هم" : [u"", DAMMA + WAW + ALEF_WASLA]
, u"هن" : [u"", u"ْنَ"]
}
future = {
u"أنا" : [u"أ", u"ُ"]
, u"أنت" : [u"ت", u"ُ"]
, u"أنتِ" : [u"ت", u"ِينَ"]
, u"أنتم" : [u"ت", u"ُونَ"]
, u"أنتما" : [u"ت", FATHA + ALEF + NOON + KASRA]
, u"أنتما مؤ" : [u"ت", FATHA + ALEF + NOON + KASRA]
, u"أنتن" : [u"ت", SUKUN + NOON + FATHA]
, u"نحن" : [u"ن", u"ُ"]
, u"هم" : [u"ي", u"ُونَ"]
, u"هما" : [u"ي", u"َانِ"]
, u"هما مؤ" : [u"ت", u"َانِ"]
, u"هن" : [u"ي", u"ْنَ"]
, u"هو" : [u"ي", u"ُ"]
, u"هي" : [u"ت", u"ُ"]
}
future_majzoom = {
u"أنا" : [u"أ", u"ْ"]
, u"أنت" : [u"ت", u"ْ"]
, u"أنتِ" : [u"ت", u"ِي"]
, u"أنتم" : [u"ت", DAMMA + WAW + ALEF_WASLA]
##, u"أنتم" : [u"ت", DAMMA+WAW+ALEF]
, u"أنتما" : [u"ت", u"َا"]
, u"أنتما مؤ" : [u"ت", u"َا"]
, u"أنتن" : [u"ت", u"ْنَ"]
, u"نحن" : [u"ن", u"ْ"]
##, u"هم" : [u"ي", DAMMA+WAW+ALEF]
, u"هم" : [u"ي", DAMMA+WAW+ALEF_WASLA]
, u"هما" : [u"ي", u"َا"]
, u"هما مؤ" : [u"ت", u"َا"]
, u"هن" : [u"ي", u"ْنَ"]
, u"هو" : [u"ي", u"ْ"]
, u"هي" : [u"ت", u"ْ"]
}
future_mansoub = {
u"أنا" : [u"أ", u"َ"]
, u"أنت" : [u"ت", u"َ"]
, u"أنتِ" : [u"ت", u"ِي"]
, u"أنتم" : [u"ت", DAMMA+WAW+ALEF_WASLA]
##, u"أنتم" : [u"ت", DAMMA+WAW+ALEF]
, u"أنتما" : [u"ت", u"َا"]
, u"أنتما مؤ" : [u"ت", u"َا"]
, u"أنتن" : [u"ت", u"ْنَ"]
, u"نحن" : [u"ن", u"َ"]
##, u"هم" : [u"ي", DAMMA+WAW+ALEF]
, u"هم" : [u"ي", DAMMA+WAW+ALEF_WASLA]
, u"هما" : [u"ي", u"َا"]
, u"هما مؤ" : [u"ت", u"َا"]
, u"هن" : [u"ي", u"ْنَ"]
, u"هو" : [u"ي", u"َ"]
, u"هي" : [u"ت", u"َ"]
}

future_confirmed = {
u"أنا" : [u"أ", FATHA+NOON+SHADDA+FATHA]
, u"أنت" : [u"ت", FATHA+NOON+SHADDA+FATHA]
, u"أنتِ" : [u"ت", KASRA+NOON+SHADDA+FATHA]
, u"أنتما" : [u"ت", FATHA+ALEF+NOON+SHADDA+KASRA]
, u"أنتما مؤ" : [u"ت", FATHA+ALEF+NOON+SHADDA+KASRA]
, u"أنتم" : [u"ت", DAMMA+NOON+SHADDA+FATHA]
, u"أنتن" : [u"ت", SUKUN+NOON+FATHA+ALEF+NOON+SHADDA+KASRA]
, u"نحن" : [u"ن", FATHA+NOON+SHADDA+FATHA]
, u"هم" : [u"ي", DAMMA+NOON+SHADDA+FATHA]
, u"هما" : [u"ي", FATHA+ALEF+NOON+SHADDA+KASRA]
, u"هما مؤ" : [u"ت", FATHA+ALEF+NOON+SHADDA+KASRA]
, u"هن" : [u"ي", SUKUN+NOON+FATHA+ALEF+NOON+SHADDA+KASRA]
, u"هو" : [u"ي", FATHA+NOON+SHADDA+FATHA]
, u"هي" : [u"ت", FATHA+NOON+SHADDA+FATHA]
}
imperative = {
u"أنت" : [u"", u"ْ"]
, u"أنتِ" : [u"", u"ِي"]
, u"أنتم" : [u"", DAMMA+WAW+ALEF_WASLA]
, u"أنتما" : [u"", u"َا"]
, u"أنتما مؤ" : [u"", u"َا"]
, u"أنتن" : [u"", u"ْنَ"]
}
imperative_confirmed = {
u"أنت" : [u"", FATHA+NOON+SHADDA+FATHA]
, u"أنتِ" : [u"", KASRA+NOON+SHADDA+FATHA]
, u"أنتم" : [u"", DAMMA+NOON+SHADDA+FATHA]
, u"أنتما" : [u"", FATHA+ALEF+NOON+SHADDA+KASRA]
, u"أنتما مؤ" : [u"", FATHA+ALEF+NOON+SHADDA+KASRA]
, u"أنتن" : [u"", SUKUN+NOON+FATHA+ALEF+NOON+SHADDA+KASRA]
}

TableTensePronoun = {}
TableTensePronoun[TensePast] = past
TableTensePronoun[TenseFuture] = future
TableTensePronoun[TenseImperative] = imperative
TableTensePronoun[TenseJussiveFuture] = future_majzoom
TableTensePronoun[TenseSubjunctiveFuture] = future_mansoub
TableTensePronoun[TenseConfirmedFuture] = future_confirmed
TableTensePronoun[TenseConfirmedImperative] = imperative_confirmed

TableTensePronoun[TensePassivePast] = past
TableTensePronoun[TensePassiveFuture] = future
TableTensePronoun[TensePassiveJussiveFuture] = future_majzoom
TableTensePronoun[TensePassiveSubjunctiveFuture] = future_mansoub
TableTensePronoun[TensePassiveConfirmedFuture] = future_confirmed


TAB_SARF = {
#باب تصريف الفعل، الصفر لكل الأفعال عدا الثلاثي
0: {"past":FATHA, "future":KASRA}, 
# فَعَل يَفْعُل

1: {"past":FATHA, "future":DAMMA}, 
# فَعَل يَفْعِل
2: {"past":FATHA, "future":KASRA}, 
# فَعَل يَفْعَل
3: {"past":FATHA, "future":FATHA}, 
# فَعِل يَفْعَل
4: {"past":KASRA, "future":FATHA}, 
# فَعِل يَفْعِل
5: {"past":KASRA, "future":KASRA}, 
# فَعُل يَفْعُل
6: {"past":DAMMA, "future":DAMMA}, 
}

NOT_DEF_HARAKA = TATWEEL
##NOT_DEF_HARAKA = FATHA

STRIP_HARAKA = u"i"
ALEF_HARAKA = SMALL_ALEF
ALEF4_HARAKA = u"y"
ALEF_YEH_HARAKA = u"#"
ALEF_WAW_HARAKA = u"*"

YEH_HARAKA = SMALL_YEH

ALTERNATIVE_YEH_HARAKA = u"t"
ALEF_YEH_ALTERNATIVE = u"x"
WAW_HARAKA = SMALL_WAW
ALEF_MAMDUDA = "9"
YEH_NAKISA = "5"

WRITTEN_HARAKA = {
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

# table of conversion if التقاء الساكنين
CONVERSION_TABLE = {
    ALEF_YEH_HARAKA:        KASRA, 
    ALEF_WAW_HARAKA:         DAMMA, 
    WAW_HARAKA:                DAMMA, 
    YEH_HARAKA :            KASRA, 
    ALTERNATIVE_YEH_HARAKA:    DAMMA, 
}
##WAW_MAKSURA = WAW

#HARAKAT = u"%s%s%s%s%s"%(SUKUN, FATHA, DAMMA, KASRA, SHADDA)
HARAKAT = (SUKUN, FATHA, DAMMA, KASRA)
HARAKAT2 = u"".join([ALEF_HARAKA, WAW_HARAKA, YEH_HARAKA, SUKUN, 
          FATHA, DAMMA, KASRA])
HAMZAT_PATTERN = re.compile(u"[%s%s%s%s%s]"%(ALEF_HAMZA_ABOVE, WAW_HAMZA, 
             YEH_HAMZA , HAMZA, ALEF_HAMZA_BELOW), re.UNICODE)
HAMZAT = (ALEF_HAMZA_ABOVE, WAW_HAMZA, YEH_HAMZA , HAMZA, ALEF_HAMZA_BELOW)


LAM_ALEF_PAT = re.compile(u'[\ufef7\ufef9\ufef5]', re.UNICODE)

#uniformate harkat
UNIFORMATE_MARKS_4 = FATHA+SUKUN+FATHA+FATHA
UNIFORMATE_MARKS_5TEH = FATHA+FATHA+SUKUN+FATHA+FATHA
UNIFORMATE_MARKS_5 = KASRA+SUKUN+FATHA+FATHA+FATHA
UNIFORMATE_MARKS_6 = KASRA+SUKUN+FATHA+SUKUN+FATHA+FATHA

BEGIN_WORD = u"^"
END_WORD = u"$"

LONG_HARAKAT = (ALEF_HARAKA, YEH_HARAKA, WAW_HARAKA, ALEF_YEH_HARAKA, 
                  ALEF_WAW_HARAKA)
_F = FATHA
_D = DAMMA
_K = KASRA
_S = SUKUN
_A = ALEF_HARAKA
_W = WAW_HARAKA
_Y = YEH_HARAKA

_AH = ALEF_HARAKA
_YH = YEH_HARAKA
_WH = WAW_HARAKA
_AYH = ALEF_YEH_HARAKA
_AWH = ALEF_WAW_HARAKA
_YHALT = ALTERNATIVE_YEH_HARAKA
#HAMZAT
_AHA = ALEF_HAMZA_ABOVE
_AHB = ALEF_HAMZA_BELOW
_AM = ALEF_MADDA
_YHA = YEH_HAMZA
_WHA = WAW_HAMZA
_HZ = HAMZA


INITIAL_TAHMEEZ_TABLE = {_S:_HZ, _F:_AHA, _D:_AHA, _K:_AHB, _AH:_AM , 
            _WH:_AHA, _YH:_AHB, _YHALT:_AHB}


MIDDLE_TAHMEEZ_TABLE = {
_S: {_S:_HZ, _F:_AHA, _D:_WHA, _K:_YHA, _AH:_AHA, _WH:_WHA, _YH:_YHA }, 
_F: {_S:_AHA, _F:_AHA, _D:_WHA, _K:_YHA, _AH:_AHA, _WH:_WHA, _YH:_YHA }, 
_D: {_S:_WHA, _F:_WHA, _D:_WHA, _K:_YHA, _AH:_WHA, _WH:_WHA, _YH:_YHA }, 
_K: {_S:_YHA, _F:_YHA, _D:_YHA, _K:_YHA, _AH:_YHA, _WH:_YHA, _YH:_YHA }, 
_AH: {_S:_HZ, _F:_HZ, _D:_WHA, _K:_YHA, _AH:_HZ, _WH:_WHA, _YH:_YHA }, 
_WH: {_S:_HZ, _F:_HZ, _D:_WHA, _K:_YHA, _AH:_HZ, _WH:_WHA, _YH:_YHA }, 
_YH: {_S:_YHA, _F:_YHA, _D:_YHA, _K:_YHA, _AH:_YHA, _WH:_YHA, _YH:_YHA }, 
}

FINAL_TAHMEEZ_TABLE = {
u"%s" % BEGIN_WORD :{_S:_HZ, _F:_AHA, _D:_AHA, _K:_AHB, _AH:_AM, _WH:_AHA, 
 _YH:_AHA}, 
_S: {_S:_HZ, _F:_AHA, _D:_WHA, _K:_YHA, _AH:_AHA, _WH:_WHA, _YH:_YHA }, 
_F: {_S:_AHA, _F:_AHA, _D:_AHA, _K:_AHB, _AH:_AHA, _WH:_WHA, _YH:_YHA }, 
_D: {_S:_WHA, _F:_WHA, _D:_WHA, _K:_YHA, _AH:_WHA, _WH:_WHA, _YH:_YHA }, 
_K: {_S:_YHA, _F:_YHA, _D:_YHA, _K:_YHA, _AH:_WHA, _WH:_WHA, _YH:_YHA }, 
_AH: {_S:_HZ, _F:_HZ, _D:_HZ, _K:_HZ, _AH:_HZ, _WH:_WHA, _YH:_YHA }, 
_WH: {_S:_HZ, _F:_HZ, _D:_HZ, _K:_HZ, _AH:_WHA, _WH:_WHA, _YH:_YHA}, 
_YH: {_S:_HZ, _F:_HZ, _D:_HZ, _K:_HZ, _AH:_WHA, _WH:_WHA, _YH:_YHA}
}

# جدول تحويل الألف الفتحة الطويلة إلى حركات أخرى حسب سياقها
HOMOGENIZE_ALEF_HARAKA_TABLE = {
_S:{_S:'*' , _F:ALEF_HARAKA, _D:WAW_HARAKA, _K:YEH_HARAKA }, 
_F:{_S:ALEF_HARAKA, _F:ALEF_HARAKA, _D:ALEF_HARAKA, _K:ALEF_HARAKA }, 
_D:{_S:WAW_HARAKA, _F:ALEF_HARAKA, _D:ALEF_HARAKA, _K:YEH_HARAKA }, 
_K:{_S:YEH_HARAKA, _F:ALEF_HARAKA, _D:YEH_HARAKA,  _K:ALEF_HARAKA}, 
}


# Table of irregular verbs
# irregular verbs have common forms
# جدول الأفعال عربية الشاذة،
# مثل الفعل رأى، أرى، أخذ أكل، سأل
#الأفعال المثال
# كل سطر يحتوي على جذوع تصريف الفعل
# في زمن معين
IRREGULAR_VERB_CONJUG = {}
CONJUG_BAB = u"باب التصريف"

#  في الحركات، الحركة الأولى هي لحركة حرف المضارعة
IRREGULAR_VERB_CONJUG[u"رءى"+FATHA+FATHA] = {
CONJUG_BAB:(FATHA, FATHA), 
TenseFuture:(u"رى", FATHA+FATHA+FATHA), 
TensePassiveFuture:(u"رى", DAMMA+FATHA+FATHA), 
TenseImperative:(u"رى", FATHA+FATHA), 
}
IRREGULAR_VERB_CONJUG[u"ءري"+FATHA+FATHA] = {
CONJUG_BAB:(FATHA, FATHA), 
TenseFuture:(u"ري", DAMMA+KASRA+FATHA), 
TensePassiveFuture:(u"ري", DAMMA+FATHA+FATHA), 
TenseImperative:(u"ءري", FATHA+KASRA+FATHA), 
}
#~ ان يتصرف من باب (عَلِمَ يَعْلَمُ)، 
#~ لا تحذف واوه؛ نحو: وَجِلَ، يَوْجَلُ، 
#~ عدا ثلاثة أفعال هي: (وذر), و(وسع)، و(وطأ)،
 #~ تحذف واوها؛ فنقول: وَذِرَ، يَذَرُ،
# ونقول: وَسِعَ، يَسَعُ، ونقول: وَطِئَ، يَطَأُ.
#إذا ك# الفعل وذر يذر
# KASRA FATHA
IRREGULAR_VERB_CONJUG[u"وذر"+KASRA+FATHA] = {
    CONJUG_BAB:(KASRA, FATHA), 
    TenseFuture:(u"ذر", FATHA+FATHA+DAMMA), 
    TensePassiveFuture:(u"ذر", DAMMA+FATHA+DAMMA), 
    TenseImperative:(u"ذر", FATHA+SUKUN), 
}
# الفعل وَسِعَ يسع
# KASRA FATHA
IRREGULAR_VERB_CONJUG[u"وسع"+KASRA+FATHA] = {
    CONJUG_BAB:(KASRA, FATHA), 
    TenseFuture:(u"سع", FATHA+FATHA+DAMMA), 
    TensePassiveFuture:(u"سع", DAMMA+FATHA+DAMMA), 
    TenseImperative:(u"سع", FATHA+SUKUN), 
}
# الفعل وطئ يطأ
# KASRA FATHA
IRREGULAR_VERB_CONJUG[u"وطء"+KASRA+FATHA] = {
    CONJUG_BAB:(KASRA, FATHA), 
    TenseFuture:(u"طء", FATHA+FATHA+DAMMA), 
    TensePassiveFuture:(u"وطء", DAMMA+SUKUN+FATHA+DAMMA), 
    TenseImperative:(u"طء", FATHA+SUKUN), 
}



# الأفعال التي يتغير أمرها بحذف الهمزة وجوبا، مثل أكل،  أخذ
# أما ما لا تحذف همزته وجوبا مثل سأل وأمر، فلا تعتبر شاذة

# الفعل أكَل يأكُل، كُل
#FATHA, DAMMA
IRREGULAR_VERB_CONJUG[u"ءكل"+FATHA+DAMMA] = {
    CONJUG_BAB:(FATHA, DAMMA), 
    TenseFuture:(u"ءكل", FATHA+SUKUN+DAMMA+DAMMA), 
    TensePassiveFuture:(u"ءكل", DAMMA+SUKUN+FATHA+FATHA), 
    TenseImperative:(u"كل", DAMMA+SUKUN), 
}
#الفعل أخَذَ يأخُذُ، خُذ
#FATHA, DAMMA
IRREGULAR_VERB_CONJUG[u"ءخذ"+FATHA+DAMMA] = {
    CONJUG_BAB:(FATHA, DAMMA), 
    TenseFuture:(u"ءخذ", FATHA+SUKUN+DAMMA+DAMMA), 
    TensePassiveFuture:(u"ءخذ", DAMMA+SUKUN+FATHA+FATHA), 
    TenseImperative:(u"خذ", DAMMA+SUKUN), 
}
#ج- إذا كان يتصرف من باب (مَنَعَ يَمْنَعُ)، 
#~ تحذف واوه, نحو: وَضَعَ، يَضَعُ، وَجَأَ يَجَأُ، وَدَعَ يَدَعُ، وَزَعَ يَزَعُ،
 #~ وَضَأَ يَضَأُ، وَطَأَ يَطَأُ، وَقَعَ يَقَعُ، وَلَغَ يَلَغُ، وَهَبَ يَهَبُ، 
#~ عدا خمسة أفعال هي:
 #~ (وَبَأ)، و(وَبَهَ)، و(وَجَعَ)، و(وَسَعَ)، و(وَهَلَ)، 
#~ فلا تحذف منها الواو؛ فنقول: يَوْبَأُ، يَوْبَهُ، يَوْجَعُ، يَوْسَعُ، يَوْهَلُ.
# الأفعال (وَبَأ)، و(وَبَهَ)، و(وَجَعَ)، و(وَسَعَ)، و(وَهَلَ)،#الفعل وبَأ يوبأ
#FATHA FATHA
IRREGULAR_VERB_CONJUG[u"وبء"+FATHA+FATHA] = {
    CONJUG_BAB:(FATHA, FATHA), 
    TenseFuture:(u"وبء", FATHA+SUKUN+FATHA+DAMMA), 
    TensePassiveFuture:(u"وبء", DAMMA+SUKUN+FATHA+DAMMA), 
    TenseImperative:(u"وبء", SUKUN+FATHA+SUKUN), 
}
# الفعل وبه يوبه
#FATHA FATHA
IRREGULAR_VERB_CONJUG[u"وبه"+FATHA+FATHA] = {
    CONJUG_BAB:(FATHA, FATHA), 
    TenseFuture:(u"وبه", FATHA+SUKUN+FATHA+DAMMA), 
    TensePassiveFuture:(u"وبه", DAMMA+SUKUN+FATHA+DAMMA), 
    TenseImperative:(u"وبه", SUKUN+FATHA+SUKUN), 
}
# الفعل وجع يوجع
#FATHA FATHA
IRREGULAR_VERB_CONJUG[u"وجع"+FATHA+FATHA] = {
    CONJUG_BAB:         (FATHA, FATHA), 
    TenseFuture:        (u"وجع", FATHA+SUKUN+FATHA+DAMMA), 
    TensePassiveFuture: (u"وجع", DAMMA+SUKUN+FATHA+DAMMA), 
    TenseImperative:    (u"وجع", SUKUN+FATHA+SUKUN), 
}
#الفعل وسع يوسع
#FATHA FATHA
IRREGULAR_VERB_CONJUG[u"وسع"+FATHA+FATHA] = {
    CONJUG_BAB:         (FATHA, FATHA), 
    TenseFuture:        (u"وسع", FATHA+SUKUN+FATHA+DAMMA), 
    TensePassiveFuture: (u"وسع", DAMMA+SUKUN+FATHA+DAMMA), 
    TenseImperative:    (u"وسع", SUKUN+FATHA+SUKUN), 
}

# الفعل وهل يوهل
#FATHA FATHA
IRREGULAR_VERB_CONJUG[u"وهل"+FATHA+FATHA] = {
    CONJUG_BAB:         (FATHA, FATHA), 
    TenseFuture:        (u"وهل", FATHA+SUKUN+FATHA+DAMMA), 
    TensePassiveFuture: (u"وهل", DAMMA+SUKUN+FATHA+DAMMA), 
    TenseImperative:    (u"وهل", SUKUN+FATHA+SUKUN), 
}



ALEF_MADDA_VERB_TABLE = {
u'آبل':[u'أءبل'], 
u'آبه':[u'أءبه'], 
u'آبى':[u'أءبى'], 
u'آتم':[u'أءتم'], 
u'آتن':[u'أءتن'], 
u'آتى':[u'أءتى'], 
#~ u'آتى':[u'أءتى'], 
u'آثر':[u'أءثر'], 
u'آثف':[u'أءثف'], 
u'آثم':[u'أءثم'], 
u'آثى':[u'ءاثى'], 
u'آجد':[u'أءجد'], 
u'آجر':[u'أءجر', u'ءاجر'], 
u'آجل':[u'أءجل'], 
u'آجم':[u'أءجم'], 
u'آحن':[u'ءاحن'], 
u'آخذ':[u'ءاخذ'], 
u'آخى':[u'أءخى', u'ءاخى'], 
u'آدب':[u'أءدب'], 
u'آدم':[u'أءدم'], 
u'آدى':[u'أءدى'], 
u'آذن':[u'أءذن'], 
u'آذى':[u'أءذى'], 
u'آرب':[u'أءرب', u'ءارب'], 
u'آرخ':[u'أءرخ'], 
u'آرس':[u'أءرس'], 
u'آرض':[u'أءرض'], 
u'آرط':[u'أءرط'], 
u'آرف':[u'ءارف'], 
u'آرق':[u'أءرق'], 
u'آرك':[u'أءرك'], 
u'آرم':[u'ءارم'], 
u'آرن':[u'أءرن', u'ءارن'], 
u'آرى':[u'أءرى'], 
u'آزر':[u'ءازر'], 
u'آزف':[u'أءزف'], 
u'آزل':[u'أءزل'], 
u'آزى':[u'أءزى', u'ءازى'], 
u'آسب':[u'أءسب'], 
u'آسد':[u'أءسد'], 
u'آسف':[u'أءسف'], 
u'آسن':[u'أءسن'], 
#~ u'آسى':[u'ءاسى'], 
u'آسى':[u'أءسى', u'ءاسى'], 
u'آشى':[u'أءشى'], 
u'آصد':[u'أءصد'], 
u'آصر':[u'ءاصر'], 
u'آصل':[u'أءصل'], 
u'آضّ':[u'ءاضّ'], 
u'آطم':[u'أءطم'], 
u'آفك':[u'أءفك'], 
u'آفى':[u'أءفى'], 
u'آقط':[u'أءقط'], 
u'آكد':[u'أءكد'], 
u'آكر':[u'ءاكر'], 
u'آكف':[u'أءكف'], 
u'آكل':[u'أءكل', u'ءاكل'], 
u'آلت':[u'أءلت'], 
u'آلس':[u'ءالس'], 
u'آلف':[u'أءلف', u'ءالف'], 
u'آلم':[u'أءلم'], 
u'آلى':[u'أءلى'], 
u'آمر':[u'أءمر', u'ءامر'], 
u'آمن':[u'أءمن'], 
u'آنث':[u'أءنث'], 
u'آنس':[u'أءنس', u'ءانس'], 
u'آنض':[u'أءنض'], 
u'آنف':[u'أءنف'], 
u'آنق':[u'أءنق'], 
u'آنى':[u'أءنى'], 
u'آهل':[u'أءهل'], 
u'آوب':[u'ءاوب'], 
u'آوى':[u'أءوى'], 
u'آيد':[u'ءايد'], 
u'آيس':[u'أءيس'], 
}

STANDARD_REPLACEMENT=[
    #-تحويل همزة القطع على الألف بعدها فتحة 
#وهمزة القطع على الألف بعدها سكون إلى ألف ممدودة
( u"".join([ALEF_HAMZA_ABOVE, FATHA, ALEF]), ALEF_MADDA)
, ( u"".join([ALEF_MADDA, FATHA]), ALEF_MADDA)
, ( u"".join([ALEF_MADDA, ALEF]), ALEF_MADDA)
, ( u"".join([ALEF_HAMZA_ABOVE, FATHA, ALEF_HAMZA_ABOVE, SUKUN]), ALEF_MADDA)
, ( u"".join([ALEF_HAMZA_ABOVE, FATHA, ALEF_HAMZA_ABOVE, FATHA]), ALEF_MADDA)
, ( u"".join([ALEF_HAMZA_ABOVE, DAMMA, WAW_HAMZA, SUKUN]), ALEF_HAMZA_ABOVE+DAMMA+WAW)
, ( u"".join([YEH, SHADDA, FATHA, ALEF_MAKSURA]), YEH+SHADDA+FATHA+ALEF)
# إدغام النون الساكنة
, ( u"".join([NOON, SUKUN, NOON]), NOON+SHADDA)
# إذا كان الحرف الأول ساكنا وبعده شدة، ثم أضيفت إليه الألف
, ( u"".join([SUKUN, SHADDA]), SHADDA)
##  معالجة ألف التفريق
, ( ALEF_WASLA, ALEF)
##  معالجة ألف التفريق
, ( ALEF_MAMDUDA, ALEF)

##  معالجة ألف  الوصل الزائدة عند إضافتها إلى أول الفعل المثال
##    word = word.replace( u"%s%s%s%s"%(ALEF, DAMMA, YEH, SUKUN), ALEF+DAMMA+WAW)




]
