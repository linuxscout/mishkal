#!/usr/bin/python
# -*- coding=utf-8 -*-
#---
#************************************************************************
# $Id: verb_const.py,v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
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
from pyarabic.araby import *
# from arabic_const import *
import re;
#tab_pronoun	= (u"أنا" ,u"أنت" ,u"أنتِ" ,u"هو" ,u"هي" ,u"أنتما" ,u"أنتما مؤ" ,u"هما" ,u"هما مؤ" ,u"نحن" ,u"أنتم" ,u"أنتن" ,u"هم" ,u"هن");
PronounsTable	= (u"أنا" ,u"نحن" ,u"أنت" ,u"أنتِ" ,u"أنتما" ,u"أنتما مؤ" ,u"أنتم" ,u"أنتن" ,u"هو" ,u"هي" ,u"هما" ,u"هما مؤ" ,u"هم" ,u"هن");
PronounsTableNotPassiveForUntransitive	= (u"أنا" ,u"نحن" ,u"أنت" ,u"أنتِ" ,u"أنتما" ,u"أنتما مؤ" ,u"أنتم" ,u"أنتن" ,u"هما" ,u"هما مؤ" ,u"هم" ,u"هن");
PronounAna	= u"أنا";
PronounNahnu	= u"نحن";
PronounAnta	= u"أنت";
PronounAnti	= u"أنتِ";
PronounAntuma	= u"أنتما";
PronounAntuma_f	= u"أنتما مؤ";
PronounAntum	= u"أنتم";
PronounAntunna	= u"أنتن";
PronounHuwa	= u"هو";
PronounHya	= u"هي";
PronounHuma	= u"هما";
PronounHuma_f	= u"هما مؤ";
PronounHum	= u"هم";
PronounHunna	= u"هن";


ImperativePronouns	= (u"أنت" ,u"أنتِ" ,u"أنتما" ,u"أنتما مؤ" ,u"أنتم" ,u"أنتن" );
# const for Tense Name
TensePast	= u"الماضي المعلوم";
TenseFuture	= u"المضارع المعلوم"
TenseImperative	= u"الأمر"
TenseConfirmedImperative	= u"الأمر المؤكد"
TenseJussiveFuture	= u"المضارع المجزوم"
TenseSubjunctiveFuture	= u"المضارع المنصوب"
TenseConfirmedFuture	= u"المضارع المؤكد الثقيل"


TensePassivePast	=  u"الماضي المجهول";
TensePassiveFuture	= u"المضارع المجهول"
TensePassiveJussiveFuture	= u"المضارع المجهول المجزوم"
TensePassiveSubjunctiveFuture	= u"المضارع المجهول المنصوب"
TensePassiveConfirmedFuture	= u"المضارع المؤكد الثقيل المجهول "
TableTense	= [TensePast,TenseFuture,TenseJussiveFuture,TenseSubjunctiveFuture,TenseConfirmedFuture,TenseImperative,
        TenseConfirmedImperative,
		TensePassivePast,TensePassiveFuture,
        TensePassiveJussiveFuture,TensePassiveSubjunctiveFuture,TensePassiveConfirmedFuture];
TableIndicativeTense	= [TensePast,TenseFuture,TenseJussiveFuture,TenseSubjunctiveFuture,TenseConfirmedFuture,TenseImperative,
        TenseConfirmedImperative];
TablePassiveTense	= [TensePassivePast,TensePassiveFuture,
        TensePassiveJussiveFuture,TensePassiveSubjunctiveFuture,TensePassiveConfirmedFuture];

past	= {}
past[u"أنا"]	= [u"",u"ْتُ"];
past[u"أنت"]	= [u"",u"ْتَ"];
past[u"أنتِ"]	= [u"",u"ْتِ"];
past[u"هو"]	= [u"",u"َ"];
past[u"هي"]	= [u"",u"َتْ"];
past[u"أنتما"]	= [u"",u"ْتُما"];
past[u"أنتما مؤ"]	= [u"",u"ْتُما"];
past[u"هما"]	= [u"",u"َا"];
past[u"هما مؤ"]	= [u"",u"َتَا"];
past[u"نحن"]	= [u"",u"ْنَا"];
past[u"أنتم"]	= [u"",u"ْتُم"];
past[u"أنتن"]	= [u"",u"ْتُنَّ"];
##past[u"هم"]	= [u"",u"ُوا"];
past[u"هم"]	= [u"",DAMMA+WAW+ALEF_WASLA];
past[u"هن"]	= [u"",u"ْنَ"];
future	= {}
future[u"أنا"]	= [u"أ",u"ُ"];
future[u"أنت"]	= [u"ت",u"ُ"];
future[u"أنتِ"]	= [u"ت",u"ِينَ"];
future[u"أنتم"]	= [u"ت",u"ُونَ"];
future[u"أنتما"]	= [u"ت",FATHA+ALEF+NOON+KASRA];
future[u"أنتما مؤ"]	= [u"ت",FATHA+ALEF+NOON+KASRA];
future[u"أنتن"]	= [u"ت",SUKUN+NOON+FATHA];
future[u"نحن"]	= [u"ن",u"ُ"];
future[u"هم"]	= [u"ي",u"ُونَ"];
future[u"هما"]	= [u"ي",u"َانِ"];
future[u"هما مؤ"]	= [u"ت", u"َانِ"];
future[u"هن"]	= [u"ي",u"ْنَ"];
future[u"هو"]	= [u"ي",u"ُ"];
future[u"هي"]	= [u"ت",u"ُ"];
future_majzoom	= {}
future_majzoom[u"أنا"]	= [u"أ",u"ْ"];
future_majzoom[u"أنت"]	= [u"ت",u"ْ"];
future_majzoom[u"أنتِ"]	= [u"ت",u"ِي"];
future_majzoom[u"أنتم"]	= [u"ت",DAMMA+WAW+ALEF_WASLA];
##future_majzoom[u"أنتم"]	= [u"ت",DAMMA+WAW+ALEF];
future_majzoom[u"أنتما"]	= [u"ت",u"َا"];
future_majzoom[u"أنتما مؤ"]	= [u"ت",u"َا"];
future_majzoom[u"أنتن"]	= [u"ت",u"ْنَ"];
future_majzoom[u"نحن"]	= [u"ن",u"ْ"];
##future_majzoom[u"هم"]	= [u"ي",DAMMA+WAW+ALEF];
future_majzoom[u"هم"]	= [u"ي",DAMMA+WAW+ALEF_WASLA];
future_majzoom[u"هما"]	= [u"ي",u"َا"];
future_majzoom[u"هما مؤ"]	= [u"ت", u"َا"];
future_majzoom[u"هن"]	= [u"ي",u"ْنَ"];
future_majzoom[u"هو"]	= [u"ي",u"ْ"];
future_majzoom[u"هي"]	= [u"ت",u"ْ"];
future_mansoub	= {}
future_mansoub[u"أنا"]	= [u"أ",u"َ"];
future_mansoub[u"أنت"]	= [u"ت",u"َ"];
future_mansoub[u"أنتِ"]	= [u"ت",u"ِي"];
future_mansoub[u"أنتم"]	= [u"ت",DAMMA+WAW+ALEF_WASLA];
##future_mansoub[u"أنتم"]	= [u"ت",DAMMA+WAW+ALEF];
future_mansoub[u"أنتما"]	= [u"ت",u"َا"];
future_mansoub[u"أنتما مؤ"]	= [u"ت",u"َا"];
future_mansoub[u"أنتن"]	= [u"ت",u"ْنَ"];
future_mansoub[u"نحن"]	= [u"ن",u"َ"];
##future_mansoub[u"هم"]	= [u"ي",DAMMA+WAW+ALEF];
future_mansoub[u"هم"]	= [u"ي",DAMMA+WAW+ALEF_WASLA];
future_mansoub[u"هما"]	= [u"ي",u"َا"];
future_mansoub[u"هما مؤ"]	= [u"ت", u"َا"];
future_mansoub[u"هن"]	= [u"ي",u"ْنَ"];
future_mansoub[u"هو"]	= [u"ي",u"َ"];
future_mansoub[u"هي"]	= [u"ت",u"َ"];

future_confirmed	= {}
future_confirmed[u"أنا"]	= [u"أ",FATHA+NOON+SHADDA+FATHA];
future_confirmed[u"أنت"]	= [u"ت",FATHA+NOON+SHADDA+FATHA];
future_confirmed[u"أنتِ"]	= [u"ت",KASRA+NOON+SHADDA+FATHA];
future_confirmed[u"أنتما"]	= [u"ت",FATHA+ALEF+NOON+SHADDA+KASRA];
future_confirmed[u"أنتما مؤ"]	= [u"ت",FATHA+ALEF+NOON+SHADDA+KASRA];
future_confirmed[u"أنتم"]	= [u"ت",DAMMA+NOON+SHADDA+FATHA];
future_confirmed[u"أنتن"]	= [u"ت",SUKUN+NOON+FATHA+ALEF+NOON+SHADDA+KASRA];
future_confirmed[u"نحن"]	= [u"ن",FATHA+NOON+SHADDA+FATHA];
future_confirmed[u"هم"]	= [u"ي",DAMMA+NOON+SHADDA+FATHA];
future_confirmed[u"هما"]	= [u"ي",FATHA+ALEF+NOON+SHADDA+KASRA];
future_confirmed[u"هما مؤ"]	= [u"ت", FATHA+ALEF+NOON+SHADDA+KASRA];
future_confirmed[u"هن"]	= [u"ي",SUKUN+NOON+FATHA+ALEF+NOON+SHADDA+KASRA];
future_confirmed[u"هو"]	= [u"ي",FATHA+NOON+SHADDA+FATHA];
future_confirmed[u"هي"]	= [u"ت",FATHA+NOON+SHADDA+FATHA];

imperative	= {}
imperative[u"أنت"]	= [u"",u"ْ"];
imperative[u"أنتِ"]	= [u"",u"ِي"];
imperative[u"أنتم"]	= [u"",DAMMA+WAW+ALEF_WASLA];
imperative[u"أنتما"]	= [u"",u"َا"];
imperative[u"أنتما مؤ"]	= [u"",u"َا"];
imperative[u"أنتن"]	= [u"",u"ْنَ"];

imperative_confirmed	= {}
imperative_confirmed[u"أنت"]	= [u"",FATHA+NOON+SHADDA+FATHA];
imperative_confirmed[u"أنتِ"]	= [u"",KASRA+NOON+SHADDA+FATHA];
imperative_confirmed[u"أنتم"]	= [u"",DAMMA+NOON+SHADDA+FATHA];
imperative_confirmed[u"أنتما"]	= [u"",FATHA+ALEF+NOON+SHADDA+KASRA];
imperative_confirmed[u"أنتما مؤ"]	= [u"",FATHA+ALEF+NOON+SHADDA+KASRA];
imperative_confirmed[u"أنتن"]	= [u"",SUKUN+NOON+FATHA+ALEF+NOON+SHADDA+KASRA];


TableTensePronoun	= {}
TableTensePronoun[TensePast]	= past;
TableTensePronoun[TenseFuture]	= future;
TableTensePronoun[TenseImperative]	= imperative;
TableTensePronoun[TenseJussiveFuture]	= future_majzoom;
TableTensePronoun[TenseSubjunctiveFuture]	= future_mansoub;
TableTensePronoun[TenseConfirmedFuture]	= future_confirmed;
TableTensePronoun[TenseConfirmedImperative]	= imperative_confirmed;

TableTensePronoun[TensePassivePast]	= past;
TableTensePronoun[TensePassiveFuture]	= future;
TableTensePronoun[TensePassiveJussiveFuture]	= future_majzoom;
TableTensePronoun[TensePassiveSubjunctiveFuture]	= future_mansoub;
TableTensePronoun[TensePassiveConfirmedFuture]	= future_confirmed;


tab_sarf	= {};
#باب تصريف الفعل، الصفر لكل الأفعال عدا الثلاثي
tab_sarf[0]	= {"past":FATHA,"future":KASRA}
# فَعَل يَفْعُل

tab_sarf[1]	= {"past":FATHA,"future":DAMMA}
# فَعَل يَفْعِل
tab_sarf[2]	= {"past":FATHA,"future":KASRA}
# فَعَل يَفْعَل
tab_sarf[3]	= {"past":FATHA,"future":FATHA}
# فَعِل يَفْعَل
tab_sarf[4]	= {"past":KASRA,"future":FATHA}
# فَعِل يَفْعِل
tab_sarf[5]	= {"past":KASRA,"future":KASRA}
# فَعُل يَفْعُل
tab_sarf[6]	= {"past":DAMMA,"future":DAMMA}


NOT_DEF_HARAKA	= TATWEEL;
##NOT_DEF_HARAKA	= FATHA;

STRIP_HARAKA	= u"i";
ALEF_HARAKA	= SMALL_ALEF;
ALEF4_HARAKA	= u"y";
ALEF_YEH_HARAKA	= u"#";
ALEF_WAW_HARAKA	= u"*";

YEH_HARAKA	= SMALL_YEH;

ALTERNATIVE_YEH_HARAKA	= u"t"
ALEF_YEH_ALTERNATIVE	= u"x"
WAW_HARAKA	= SMALL_WAW;
ALEF_MAMDUDA	= "9";
YEH_NAKISA	= "5";
##WAW_MAKSURA	= WAW

#HARAKAT	= u"%s%s%s%s%s"%(SUKUN,FATHA,DAMMA,KASRA,SHADDA);
HARAKAT	= (SUKUN,FATHA,DAMMA,KASRA);
HARAKAT2	= u"%s%s%s%s%s%s%s"%(ALEF_HARAKA,WAW_HARAKA,YEH_HARAKA,SUKUN,FATHA,DAMMA,KASRA);
HAMZAT_pat	= re.compile(u"[%s%s%s%s%s]"%(ALEF_HAMZA_ABOVE, WAW_HAMZA, YEH_HAMZA , HAMZA, ALEF_HAMZA_BELOW),re.UNICODE);
HAMZAT	= (ALEF_HAMZA_ABOVE, WAW_HAMZA, YEH_HAMZA , HAMZA, ALEF_HAMZA_BELOW);


LAM_ALEF_pat	= re.compile(u'[\ufef7\ufef9\ufef5]',re.UNICODE);

#uniformate harkat
UNIFORMATE_MARKS_4	= FATHA+SUKUN+FATHA+FATHA;
UNIFORMATE_MARKS_5TEH	= FATHA+FATHA+SUKUN+FATHA+FATHA;
UNIFORMATE_MARKS_5	= KASRA+SUKUN+FATHA+FATHA+FATHA;
UNIFORMATE_MARKS_6	= KASRA+SUKUN+FATHA+SUKUN+FATHA+FATHA;

BEGIN_WORD	= u"^";
END_WORD	= u"$";

LONG_HARAKAT	= (ALEF_HARAKA,YEH_HARAKA,WAW_HARAKA,ALEF_YEH_HARAKA,ALEF_WAW_HARAKA);
_F	= FATHA;
_D	= DAMMA;
_K	= KASRA;
_S	= SUKUN;
_A	= ALEF_HARAKA;
_W	= WAW_HARAKA;
_Y	= YEH_HARAKA

_AH	= ALEF_HARAKA;
_YH	= YEH_HARAKA
_WH	= WAW_HARAKA
_AYH	= ALEF_YEH_HARAKA
_AWH	= ALEF_WAW_HARAKA
_YHALT	= ALTERNATIVE_YEH_HARAKA
##tab_change_haraka	= {};
##tab_change_haraka[_S]	= {_S:_S,_F:_F,_D:_D,_K:_K,_AH:_AH,_WH:_WH,_YH:_YH}
##tab_change_haraka[_F]	= {_S:_S,_F:_F,_D:_D,_K:_K,_AH:_AH,_WH:_WH,_YH:_YH}
##tab_change_haraka[_D]	= {_S:_S,_F:_F,_D:_D,_K:_K,_AH:_AH,_WH:_WH,_YH:_YH}
##tab_change_haraka[_K]	= {_S:_S,_F:_F,_D:_D,_K:_K,_AH:_AH,_WH:_WH,_YH:_YH}
##tab_change_haraka[_AH]	= {_S:_F,_F:_AH,_D:_WH,_K:_YH,_AH:u"",_YH:u"",_WH:u"",_YH:u""}
##tab_change_haraka[_WH]	= {_S:_D,_F:_AH,_D:_WH,_K:_YH,_AH:u"",_WH:u"",_YH:u""}
##tab_change_haraka[_YH]	= {_S:_K,_F:_AH,_D:_WH,_K:_YH,_AH:u"",_WH:u"",_YH:u""}
##tab_change_haraka[_AWH]	= {_S: (u"%s%s"%(_F,_S),_W),_F:(u"%s%s"%(_F,_F),_W),_D:_WH,_K:_YH,_AH:(u"%s%s"%(_F,_AH),_W),_WH:_WH,_YH:_YH}
##tab_change_haraka[_AYH]	= {_S:(u"%s%s"%(_F,_S),_Y),_F:(u"%s%s"%(_F,_F),_Y),_D:_YH,_K:_YH,_AH:(u"%s%s"%(_F,_AH),_Y),_WH:_WH,_YH:_YH}
#HAMZAT
_AHA	= ALEF_HAMZA_ABOVE
_AHB	= ALEF_HAMZA_BELOW
_AM	= ALEF_MADDA;
_YHA	= YEH_HAMZA
_WHA	= WAW_HAMZA
_HZ	= HAMZA


tab_tahmeez_initial	= {_S:_HZ,_F:_AHA,_D:_AHA, _K:_AHB,_AH:_AM ,_WH:_AHA, _YH:_AHB,_YHALT:_AHB};


tab_tahmeez_middle	= {};
tab_tahmeez_middle[_S]	= {_S:_HZ,_F:_AHA,_D:_WHA, _K:_YHA,_AH:_AHA,_WH:_WHA, _YH:_YHA };
tab_tahmeez_middle[_F]	= {_S:_AHA,_F:_AHA,_D:_WHA, _K:_YHA,_AH:_AHA,_WH:_WHA, _YH:_YHA };
tab_tahmeez_middle[_D]	= {_S:_WHA,_F:_WHA,_D:_WHA, _K:_YHA,_AH:_WHA,_WH:_WHA, _YH:_YHA };
tab_tahmeez_middle[_K]	= {_S:_YHA,_F:_YHA,_D:_YHA, _K:_YHA,_AH:_YHA,_WH:_YHA, _YH:_YHA };
tab_tahmeez_middle[_AH]	= {_S:_HZ,_F:_HZ,_D:_WHA, _K:_YHA,_AH:_HZ,_WH:_WHA, _YH:_YHA };
tab_tahmeez_middle[_WH]	= {_S:_HZ,_F:_HZ,_D:_WHA, _K:_YHA,_AH:_HZ,_WH:_WHA, _YH:_YHA };
tab_tahmeez_middle[_YH]	= {_S:_YHA,_F:_YHA,_D:_YHA, _K:_YHA,_AH:_YHA,_WH:_YHA, _YH:_YHA };


tab_tahmeez_final	= {};
tab_tahmeez_final[u"%s"%BEGIN_WORD]	= {_S:_HZ,_F:_AHA,_D:_AHA, _K:_AHB,_AH:_AM ,_WH:_AHA, _YH:_AHA};
tab_tahmeez_final[_S]	= {_S:_HZ,_F:_AHA,_D:_WHA, _K:_YHA,_AH:_AHA,_WH:_WHA, _YH:_YHA };
tab_tahmeez_final[_F]	= {_S:_AHA,_F:_AHA,_D:_AHA, _K:_AHB,_AH:_AHA,_WH:_WHA, _YH:_YHA };
tab_tahmeez_final[_D]	= {_S:_WHA,_F:_WHA,_D:_WHA, _K:_YHA,_AH:_WHA,_WH:_WHA, _YH:_YHA };
tab_tahmeez_final[_K]	= {_S:_YHA,_F:_YHA,_D:_YHA, _K:_YHA,_AH:_WHA,_WH:_WHA, _YH:_YHA };
tab_tahmeez_final[_AH]	= {_S:_HZ,_F:_HZ,_D:_HZ, _K:_HZ,_AH:_HZ,_WH:_WHA, _YH:_YHA };
tab_tahmeez_final[_WH]	= {_S:_HZ,_F:_HZ,_D:_HZ, _K:_HZ,_AH:_WHA,_WH:_WHA, _YH:_YHA};
tab_tahmeez_final[_YH]	= {_S:_HZ,_F:_HZ,_D:_HZ, _K:_HZ,_AH:_WHA,_WH:_WHA, _YH:_YHA};


# جدول تحويل الألف الفتحة الطويلة إلى حركات أخرى حسب سياقها
tab_homogenize_alef_haraka	= {};
tab_homogenize_alef_haraka[_S]	= {_S:'*'        ,_F:ALEF_HARAKA,_D:WAW_HARAKA , _K:YEH_HARAKA };
tab_homogenize_alef_haraka[_F]	= {_S:ALEF_HARAKA,_F:ALEF_HARAKA,_D:ALEF_HARAKA, _K:ALEF_HARAKA };
tab_homogenize_alef_haraka[_D]	= {_S:WAW_HARAKA, _F:ALEF_HARAKA,_D:ALEF_HARAKA, _K:YEH_HARAKA };
tab_homogenize_alef_haraka[_K]	= {_S:YEH_HARAKA, _F:ALEF_HARAKA,_D:YEH_HARAKA, _K:ALEF_HARAKA};



# Table of irregular verbs
# irregular verbs have common forms
# جدول الأفعال عربية الشاذة،
# مثل الفعل رأى، أرى، أخذ أكل، سأل
#الأفعال المثال
# كل سطر يحتوي على جذوع تصريف الفعل
# في زمن معين
IrregularVerbsConjug	= {};
ConjugBab	= u"باب التصريف";
##IrregularVerbsConjug[u""]	= {
##TensePast:u"",
##TensePassivePast:u"",
##TenseFuture:u"",
##TensePassiveFuture:u"",
##TenseImperative:u""
##}
#  في الحركات، الحركة الأولى هي لحركة حرف المضارعة
IrregularVerbsConjug[u"رءى"+FATHA+FATHA]	= {
ConjugBab:(FATHA,FATHA),
TenseFuture:(u"رى",FATHA+FATHA+FATHA),
TensePassiveFuture:(u"رى",DAMMA+FATHA+FATHA),
TenseImperative:(u"رى",FATHA+FATHA),
}
IrregularVerbsConjug[u"ءري"+FATHA+FATHA]	= {
ConjugBab:(FATHA,FATHA),
TenseFuture:(u"ري",DAMMA+KASRA+FATHA),
TensePassiveFuture:(u"ري",DAMMA+FATHA+FATHA),
TenseImperative:(u"ءري",FATHA+KASRA+FATHA),
}
#إذا كان يتصرف من باب (عَلِمَ يَعْلَمُ)، لا تحذف واوه؛ نحو: وَجِلَ، يَوْجَلُ، عدا ثلاثة أفعال هي: (وذر), و(وسع)، و(وطأ)، تحذف واوها؛ فنقول: وَذِرَ، يَذَرُ، ونقول: وَسِعَ، يَسَعُ، ونقول: وَطِئَ، يَطَأُ.
# الفعل وذر يذر
# KASRA FATHA
IrregularVerbsConjug[u"وذر"+KASRA+FATHA]	= {
ConjugBab:(KASRA,FATHA),
TenseFuture:(u"ذر",FATHA+FATHA+DAMMA),
TensePassiveFuture:(u"ذر",DAMMA+FATHA+DAMMA),
TenseImperative:(u"ذر",FATHA+SUKUN),
}
# الفعل وَسِعَ يسع
# KASRA FATHA
IrregularVerbsConjug[u"وسع"+KASRA+FATHA]	= {
ConjugBab:(KASRA,FATHA),
TenseFuture:(u"سع",FATHA+FATHA+DAMMA),
TensePassiveFuture:(u"سع",DAMMA+FATHA+DAMMA),
TenseImperative:(u"سع",FATHA+SUKUN),
}
# الفعل وطئ يطأ
# KASRA FATHA
IrregularVerbsConjug[u"وطء"+KASRA+FATHA]	= {
ConjugBab:(KASRA,FATHA),
TenseFuture:(u"طء",FATHA+FATHA+DAMMA),
TensePassiveFuture:(u"وطء",DAMMA+SUKUN+FATHA+DAMMA),
TenseImperative:(u"طء",FATHA+SUKUN),
}



# الأفعال التي يتغير أمرها بحذف الهمزة وجوبا، مثل أكل،  أخذ
# أما ما لا تحذف همزته وجوبا مثل سأل وأمر، فلا تعتبر شاذة

# الفعل أكَل يأكُل، كُل
#FATHA,DAMMA
IrregularVerbsConjug[u"ءكل"+FATHA+DAMMA]	= {
ConjugBab:(FATHA,DAMMA),
TenseFuture:(u"ءكل",FATHA+SUKUN+DAMMA+DAMMA),
TensePassiveFuture:(u"ءكل",DAMMA+SUKUN+FATHA+FATHA),
TenseImperative:(u"كل",DAMMA+SUKUN),
}
#الفعل أخَذَ يأخُذُ، خُذ
#FATHA,DAMMA
IrregularVerbsConjug[u"ءخذ"+FATHA+DAMMA]	= {
ConjugBab:(FATHA,DAMMA),
TenseFuture:(u"ءخذ",FATHA+SUKUN+DAMMA+DAMMA),
TensePassiveFuture:(u"ءخذ",DAMMA+SUKUN+FATHA+FATHA),
TenseImperative:(u"خذ",DAMMA+SUKUN),
}
#ج- إذا كان يتصرف من باب (مَنَعَ يَمْنَعُ)، تحذف واوه, نحو: وَضَعَ، يَضَعُ، وَجَأَ يَجَأُ، وَدَعَ يَدَعُ، وَزَعَ يَزَعُ، وَضَأَ يَضَأُ، وَطَأَ يَطَأُ، وَقَعَ يَقَعُ، وَلَغَ يَلَغُ، وَهَبَ يَهَبُ، عدا خمسة أفعال هي: (وَبَأ)، و(وَبَهَ)، و(وَجَعَ)، و(وَسَعَ)، و(وَهَلَ)، فلا تحذف منها الواو؛ فنقول: يَوْبَأُ، يَوْبَهُ، يَوْجَعُ، يَوْسَعُ، يَوْهَلُ.
# الأفعال (وَبَأ)، و(وَبَهَ)، و(وَجَعَ)، و(وَسَعَ)، و(وَهَلَ)،
#الفعل وبَأ يوبأ
#FATHA FATHA
IrregularVerbsConjug[u"وبء"+FATHA+FATHA]	= {
ConjugBab:(FATHA,FATHA),
TenseFuture:(u"وبء",FATHA+SUKUN+FATHA+DAMMA),
TensePassiveFuture:(u"وبء",DAMMA+SUKUN+FATHA+DAMMA),
TenseImperative:(u"وبء",SUKUN+FATHA+SUKUN),
}
# الفعل وبه يوبه
#FATHA FATHA
IrregularVerbsConjug[u"وبه"+FATHA+FATHA]	= {
ConjugBab:(FATHA,FATHA),
TenseFuture:(u"وبه",FATHA+SUKUN+FATHA+DAMMA),
TensePassiveFuture:(u"وبه",DAMMA+SUKUN+FATHA+DAMMA),
TenseImperative:(u"وبه",SUKUN+FATHA+SUKUN),
}
# الفعل وجع يوجع
#FATHA FATHA
IrregularVerbsConjug[u"وجع"+FATHA+FATHA]	= {
	ConjugBab:			(FATHA,FATHA),
	TenseFuture:		(u"وجع",FATHA+SUKUN+FATHA+DAMMA),
	TensePassiveFuture:	(u"وجع",DAMMA+SUKUN+FATHA+DAMMA),
	TenseImperative:	(u"وجع",SUKUN+FATHA+SUKUN),
}
#الفعل وسع يوسع
#FATHA FATHA
IrregularVerbsConjug[u"وسع"+FATHA+FATHA]	= {
	ConjugBab:			(FATHA,FATHA),
	TenseFuture:		(u"وسع",FATHA+SUKUN+FATHA+DAMMA),
	TensePassiveFuture:	(u"وسع",DAMMA+SUKUN+FATHA+DAMMA),
	TenseImperative:	(u"وسع",SUKUN+FATHA+SUKUN),
}

# الفعل وهل يوهل
#FATHA FATHA
IrregularVerbsConjug[u"وهل"+FATHA+FATHA]	= {
	ConjugBab:			(FATHA,FATHA),
	TenseFuture:		(u"وهل",FATHA+SUKUN+FATHA+DAMMA),
	TensePassiveFuture:	(u"وهل",DAMMA+SUKUN+FATHA+DAMMA),
	TenseImperative:	(u"وهل",SUKUN+FATHA+SUKUN),
}



AlefMaddaVerbTable	= {
u'آبل':[u'أءبل'],
u'آبه':[u'أءبه'],
u'آبى':[u'أءبى'],
u'آتم':[u'أءتم'],
u'آتن':[u'أءتن'],
u'آتى':[u'أءتى'],
u'آتى':[u'أءتى'],
u'آثر':[u'أءثر'],
u'آثف':[u'أءثف'],
u'آثم':[u'أءثم'],
u'آثى':[u'ءاثى'],
u'آجد':[u'أءجد'],
u'آجر':[u'أءجر',u'ءاجر'],
u'آجل':[u'أءجل'],
u'آجم':[u'أءجم'],
u'آحن':[u'ءاحن'],
u'آخذ':[u'ءاخذ'],
u'آخى':[u'أءخى',u'ءاخى'],
u'آدب':[u'أءدب'],
u'آدم':[u'أءدم'],
u'آدى':[u'أءدى'],
u'آذن':[u'أءذن'],
u'آذى':[u'أءذى'],
u'آرب':[u'أءرب',u'ءارب'],
u'آرخ':[u'أءرخ'],
u'آرس':[u'أءرس'],
u'آرض':[u'أءرض'],
u'آرط':[u'أءرط'],
u'آرف':[u'ءارف'],
u'آرق':[u'أءرق'],
u'آرك':[u'أءرك'],
u'آرم':[u'ءارم'],
u'آرن':[u'أءرن',u'ءارن'],
u'آرى':[u'أءرى'],
u'آزر':[u'ءازر'],
u'آزف':[u'أءزف'],
u'آزل':[u'أءزل'],
u'آزى':[u'أءزى',u'ءازى'],
u'آسب':[u'أءسب'],
u'آسد':[u'أءسد'],
u'آسف':[u'أءسف'],
u'آسن':[u'أءسن'],
u'آسى':[u'ءاسى'],
u'آسى':[u'أءسى',u'ءاسى'],
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
u'آكل':[u'أءكل',u'ءاكل'],
u'آلت':[u'أءلت'],
u'آلس':[u'ءالس'],
u'آلف':[u'أءلف',u'ءالف'],
u'آلم':[u'أءلم'],
u'آلى':[u'أءلى'],
u'آمر':[u'أءمر',u'ءامر'],
u'آمن':[u'أءمن'],
u'آنث':[u'أءنث'],
u'آنس':[u'أءنس',u'ءانس'],
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
