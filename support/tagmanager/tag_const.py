#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tag_const.py
#  
#  Copyright 2018 zerrouki <zerrouki@majd4>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    division,
    )

# stucture

TAGS_CONFIG=u"""#Part;Pos;Attribute;خاصية;code;Value;قيمة;inflection;
# Word Type نوع الكلمة
1;1;word_type;نوع الكلمة;N;Noun;اسم;اسم;
1;1;word_type;نوع الكلمة;V;Verb;فعل;فعل;
1;1;word_type;نوع الكلمة;T;Tool;أداة;حرف;
1;1;word_type;نوع الكلمة;P;Punctuation;ترقيم;علامة ترقيم;
1;1;word_type;نوع الكلمة;S;Symbol;رمز;رمز;
1;1;word_type;نوع الكلمة;D;Numeric;عدد;عدد;
1;1;word_type;نوع الكلمة;-;Undef;لاشيء;;
## Sub Class صنف فرعي
1;2;subclass;صنف;M;Masdar;مصدر;;
## transitive
1;3;transitive;تعدي;0;intransitive;لازم;;
1;3;transitive;تعدي;1;transitive;متعدي;;
1;3;transitive;تعدي;2;double transitive;متعدي لمفعولين;;
1;3;transitive;تعدي;4;commun;مشترك;;
1;3;transitive;-;تعدي;undef;لاشيء;;

# Conjugation
## Gender الجنس
2;1;gender;جنس;M;masculine;مذكر;مذكر
2;1;gender;جنس;F;Feminine;مؤنث;مؤنث;
2;1;gender;جنس;-;none;لاشيء;;
## Number العدد
2;2;number;عدد;1;single;مفرد;مفرد;
2;2;number;عدد;2;dual;مثنى;مثنى;
2;2;number;عدد;3;plural;جمع;جمع;
2;2;number;عدد;4;plural;جمع تكسير;جمع تكسير;
2;2;number;عدد;-;none;لاشيء;;
## Inlfection case الحالة الإعرابية
2;3;case;إعراب;U;marfou3;مرفوع;مرفوع;
2;3;case;إعراب;0;manjzoum; مجزوم;مجزوم;
2;3;case;إعراب;I;majrour;مجرور;مجرور;
2;3;case;إعراب;A;mansoub;منصوب;منصوب;
2;3;case;إعراب;B;mabni;مبني;مبني;
2;3;case;إعراب;-;undef;لاشيء;;
## Inflection marks
2;4;mark;علامة;u;damma;الضمة;الضمة;
2;4;mark;علامة;a;fatha;الفتحة;الفتحة;
2;4;mark;علامة;i;kasra;الكسرة;الكسرة;
2;4;mark;علامة;0;sukun;السكون;السكون;
2;4;mark;علامة;A;alef;الألف;الألف;
2;4;mark;علامة;W;waw;الواو;الواو;
2;4;mark;علامة;Y;yeh;الياء;الياء;
2;4;mark;علامة;N;noon;ثبوت النون;ثبوت النون;
2;4;mark;علامة;-;undef;لاشيء;;


# Procletics and prefixes
## Conjuction
3;1;conjonction;عطف;W;WAW;الواو;;
3;1;conjonction;عطف;F;FEH;الفاء;;
3;1;conjonction;عطف;-;undef;لاشيء;;
## preposition
3;2;preposition;جر;B;Beh;باء;بالباء;
3;2;preposition;جر;K;Kaf;كاف;بالكاف;
3;2;preposition;جر;L;Lam;لام;باللام;
3;2;preposition;جر;-;undef;لاشيء;;
## Definition
3;3;definite;تعريف;L;definited;معرفة;;
3;3;definite;تعريف;-;indefinite;نكرة;;


## Enclitics
3;4;encletic;ضمير متصل;H;Heh;ضمير متصل;والضمير المتصل مبني;
3;4;encletic;ضمير متصل;-;undef;لاشيء;;

# Special Verb
## Istiqbal
4;1;istqbal;استقبال;s;istqbal;استقبال;استقبال;
4;1;istqbal;استقبال;-;undef;لاشيء;;
## Voice البناء
4;2;voice;بناء;a;acive voice;معلوم;مبني للمعلوم;
4;2;voice;بناء;p;acive voice;مجهول;مبني للمجهول;
4;2;voice;بناء;-;undef;لاشيء;;
## tense الزمن
4;3;tense;زمن;p;past;ماض;ماضي;
4;3;tense;زمن;f;present;مضارع;مضارع;
4;3;tense;زمن;i;imperative;أمر;أمر;
4;3;tense;زمن;-;undef;لاشيء;;
## person الشخص
4;4;person;شخص;I;1st person;متكلم;;
4;4;person;شخص;Y;2nd person;مخاطب;;
4;4;person;شخص;H;3rd person;غائب;;
4;4;person;شخص;-;undef;لاشيء;;
"""

TAG_PARTS_SEP = ';'
TAG_PARTS_SIZES = [3,4,4,4]
TAGSDICT ={}
INVERSE_TAGSDICT = {}
ATTR_TAGSDICT = {}
# Map for different tags
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
TAGSMAP = {
#pronouns FEATURES
 u"أنا" : [u'متكلم',   u'مفرد'] 
, u"أنت" : [u'مخاطب', u'مذكر',  u'مفرد'] 
, u"أنتِ" : [u'مخاطب', u'مؤنث',  u'مفرد'] 
, u"هو" : [u'غائب', u'مذكر',  u'مفرد'] 
, u"هي" : [u'غائب', u'مؤنث',  u'مفرد'] 
, u"أنتما" : [u'مخاطب', u'مذكر',  u'مثنى'] 
, u"أنتما مؤ" : [u'مخاطب', u'مؤنث',  u'مثنى'] 
, u"هما" : [u'غائب', u'مذكر',  u'مثنى']
, u"هما مؤ" : [u'غائب', u'مؤنث',  u'مثنى'] 
, u"نحن" : [u'متكلم',   u'جمع']
, u"أنتم" : [u'مخاطب', u'مذكر',  u'جمع']
, u"أنتن" : [u'مخاطب', u'مؤنث',  u'جمع']
, u"هم" : [u'غائب', u'مذكر',  u'جمع']
, u"هن" : [u'غائب', u'مؤنث',  u'جمع'],
#TENSE_FEATURES = [
TensePast : [ u'ماضي', u'معلوم',  ],
TenseFuture : [ u'مضارع', u'معلوم', u'مرفوع',  ],
TenseImperative : [ u'أمر', ],
TenseConfirmedImperative : [ u'أمر',  u'مؤكذ', ],
TenseJussiveFuture : [ u'مضارع', u'معلوم', u'مجزوم',  ],
TenseSubjunctiveFuture : [ u'مضارع', u'معلوم', u'منصوب',  ],
TenseConfirmedFuture : [ u'مضارع', u'معلوم',  u'مؤكد', ],


TensePassivePast :  [ u'ماضي', u'مجهول', ],
TensePassiveFuture : [ u'مضارع', u'مجهول', u'مرفوع',  ],
TensePassiveJussiveFuture : [ u'مضارع', u'مجهول', u'مجزوم',  ],
TensePassiveSubjunctiveFuture : [ u'مضارع', u'مجهول', u'منصوب',  ], 
TensePassiveConfirmedFuture : [ u'مضارع', u'مجهول',  u'مؤكد', ],

"Verb": [u'فعل'],
"Noun": [u'اسم'],
u"مفعول به": [u'ضمير متصل'],
u"تعريف": [u'معرفة'],
u"n": [u'لازم'],
u"y": [u'متعدي'],
u"مضاف": [u'ضمير متصل'],

}

# you must call tag_config class to load tags indexes 
if __name__ == "__main__":
    print("""Test ir from tag_config to load configuration
    Call it from tagmaker
    """)
