#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        stem_verb_const
# Purpose:     Arabic lexical analyser constants, provides feature for stemming arabic word as verb
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
Arabic lexical analyser constants, provides feature for stemming arabic word as verb
"""
import re
import pyarabic.araby as ar
import libqutrub.verb_const as qutrubVerbConst
VERB_STAMP_PAT = re.compile(ur"[%s%s%s%s%s%s]" % (ar.ALEF, ar.YEH, ar.WAW, ar.ALEF_MAKSURA,
                         ar.HAMZA, ar.SHADDA), re.UNICODE)
# Compound affixes
COMP_PREFIX_LETTERS = u"أسلفو"
COMP_SUFFIX_LETTERS = u"ينهكماو"
COMP_INFIX_LETTERS = u""
COMP_MAX_PREFIX = 3
COMP_MAX_SUFFIX = 6
COMP_MIN_STEM = 2
COMP_JOKER = u"*"
"""COMP_PREFIX_LIST=set([
    "",
    ar.ALEF_HAMZA_ABOVE,
    ar.ALEF_HAMZA_ABOVE+ ar.FEH,
    ar.ALEF_HAMZA_ABOVE+ ar.FEH+ ar.LAM,
    ar.ALEF_HAMZA_ABOVE+ ar.FEH+ ar.SEEN,
    ar.ALEF_HAMZA_ABOVE+ ar.WAW,
    ar.ALEF_HAMZA_ABOVE+ ar.WAW+ ar.SEEN,
    ar.ALEF_HAMZA_ABOVE+ ar.WAW+ ar.LAM,
    ar.ALEF_HAMZA_ABOVE+ ar.LAM,
    ar.ALEF_HAMZA_ABOVE+ ar.SEEN,
    ar.FEH,
    ar.FEH+ ar.LAM,
    ar.FEH+ ar.SEEN,
    ar.WAW,
    ar.WAW+ ar.LAM,
    ar.WAW+ ar.SEEN,
    ar.LAM,
    ar.SEEN,
    ]);
COMP_SUFFIX_LIST=set(["",
    ar.YEH,
    ar.NOON+ ar.YEH,
    ar.NOON+ ar.ALEF,
    ar.KAF,
    ar.KAF+ ar.MEEM+ ar.ALEF,
    ar.KAF+ ar.MEEM,
    ar.KAF+ ar.NOON,
    ar.HEH,
    ar.HEH+ ar.ALEF,
    ar.HEH+ ar.MEEM+ ar.ALEF,
    ar.HEH+ ar.MEEM,
    ar.HEH+ ar.NOON,
# To double MAf3ool suffix
    u'يي',
    u'يني',
    u'ينا',
    u'يك',
    u'يكما',
    u'يكم',
    u'يكن',
    u'يه',
    u'يها',
    u'يهما',
    u'يهم',
    u'يهن',
    u'نيي',
    u'نيني',
    u'نينا',
    u'نيك',
    u'نيكما',
    u'نيكم',
    u'نيكن',
    u'نيه',
    u'نيها',
    u'نيهما',
    u'نيهم',
    u'نيهن',
    u'ناي',
    u'ناني',
    u'نانا',
    u'ناك',
    u'ناكما',
    u'ناكم',
    u'ناكن',
    u'ناه',
    u'ناها',
    u'ناهما',
    u'ناهم',
    u'ناهن',
    u'كي',
    u'كني',
    u'كنا',
    u'كك',
    u'ككما',
    u'ككم',
    u'ككن',
    u'كه',
    u'كها',
    u'كهما',
    u'كهم',
    u'كهن',
    u'كماي',
    u'كماني',
    u'كمانا',
    u'كماك',
    u'كماكما',
    u'كماكم',
    u'كماكن',
    u'كماه',
    u'كماها',
    u'كماهما',
    u'كماهم',
    u'كماهن',
    u'كموي',
    u'كموني',
    u'كمونا',
    u'كموك',
    u'كموكما',
    u'كموكم',
    u'كموكن',
    u'كموه',
    u'كموها',
    u'كموهما',
    u'كموهم',
    u'كموهن',
    u'كني',
    u'كنني',
    u'كننا',
    u'كنك',
    u'كنكما',
    u'كنكم',
    u'كنكن',
    u'كنه',
    u'كنها',
    u'كنهما',
    u'كنهم',
    u'كنهن',
    u'هي',
    u'هني',
    u'هنا',
    u'هك',
    u'هكما',
    u'هكم',
    u'هكن',
    u'هه',
    u'هها',
    u'ههما',
    u'ههم',
    u'ههن',
    u'هاي',
    u'هاني',
    u'هانا',
    u'هاك',
    u'هاكما',
    u'هاكم',
    u'هاكن',
    u'هاه',
    u'هاها',
    u'هاهما',
    u'هاهم',
    u'هاهن',
    u'هماي',
    u'هماني',
    u'همانا',
    u'هماك',
    u'هماكما',
    u'هماكم',
    u'هماكن',
    u'هماه',
    u'هماها',
    u'هماهما',
    u'هماهم',
    u'هماهن',
    u'هموي',
    u'هموني',
    u'همونا',
    u'هموك',
    u'هموكما',
    u'هموكم',
    u'هموكن',
    u'هموه',
    u'هموها',
    u'هموهما',
    u'هموهم',
    u'هموهن',
    u'هني',
    u'هنني',
    u'هننا',
    u'هنك',
    u'هنكما',
    u'هنكم',
    u'هنكن',
    u'هنه',
    u'هنها',
    u'هنهما',
    u'هنهم',
    u'هنهن',
    ]);
"""
COMP_PREFIX_LIST_TAGS = {
    u"": {
        'tags': (u"", ),
        "vocalized": (u"", )
    },
    u'أ': {
        'tags': (u'استفهام', ),
        "vocalized": (u"أَ", )
    },
    u'أس': {
        'tags': (u'استفهام', u'استقبال'),
        "vocalized": (u"أَسَ", )
    },
    u'و': {
        'tags': (u"عطف", ),
        "vocalized": (u"وَ", )
    },
    u'وس': {
        'tags': (u"عطف", u'استقبال'),
        "vocalized": (u"وَسَ", )
    },
    u'أو': {
        'tags': (u'استفهام', ),
        "vocalized": (u"أَوََ", )
    },
    u'أوس': {
        'tags': (u'استفهام', u'استقبال'),
        "vocalized": (u"أَوََسَ", )
    },
    u'أول': {
        'tags': (u'استفهام', u'عطف', u'لام'),
        "vocalized": (u"أَوَلََ", )
    },
    u'س': {
        'tags': (u'استقبال', ),
        "vocalized": (u"سَ", )
    },
    u'ف': {
        'tags': (u'عطف', ),
        "vocalized": (u"فَ", )
    },
    u'فس': {
        'tags': (u'عطف', u'استقبال'),
        "vocalized": (u"فَسَ", )
    },
    u'أف': {
        'tags': (
            u'استفهام',
            u'عطف',
        ),
        "vocalized": (u"أَفَ", )
    },
    u'أفس': {
        'tags': (
            u'استفهام',
            u'عطف',
            u'استقبال',
        ),
        "vocalized": (u"أَفَسَ", )
    },
    u'ل': {
        'tags': (u'جر', ),
        "vocalized": (u"لِ", )
    },
    u'ول': {
        'tags': (u'عطف', u'لام'),
        "vocalized": (u"وَلََ", )
    },
    u'فل': {
        'tags': (u'عطف', u'لام'),
        "vocalized": (u"فَلَ", )
    },
}
COMP_PREFIX_LIST = COMP_PREFIX_LIST_TAGS.keys()
COMP_SUFFIX_LIST_TAGS = {
    "": {
        'tags': (u"", ),
        "vocalized": (u"", )
    },
    u'ني': {
        'tags': (u"مفعول به", ),
        "vocalized": (u"نِي", ),
    },
    u'ي': {
        'tags': (u"مفعول به", ),
        "vocalized": (u"ي", ),
    },
    u'ك': {
        'tags': (u"مفعول به", ),
        "vocalized": (u"كَ", ),
    },
    u'ه': {
        'tags': (u"مفعول به", ),
        "vocalized": (u"هُ", ),
    },
    u'كم': {
        'tags': (u"مفعول به", ),
        "vocalized": (u"كُمْ", ),
    },
    u'كن': {
        'tags': (u"مفعول به", ),
        "vocalized": (u"كُنَّ", ),
    },
    u'ها': {
        'tags': (u"مفعول به", ),
        "vocalized": (u"هَا", ),
    },
    u'هم': {
        'tags': (u"مفعول به", ),
        "vocalized": (u"هُمْ", ),
    },
    u'هن': {
        'tags': (u"مفعول به", ),
        "vocalized": (u"هُنَّ", ),
    },
    u'نا': {
        'tags': (u"مفعول به", ),
        "vocalized": (u"نَا", ),
    },
    u'كما': {
        'tags': (u"مفعول به", ),
        "vocalized": (u"كُمَا", ),
    },
    u'هما': {
        'tags': (u"مفعول به", ),
        "vocalized": (u"هُمَا", ),
    },
}
COMP_SUFFIX_LIST = COMP_SUFFIX_LIST_TAGS.keys()

CONJ_PREFIX_LETTERS = u"تأنياء"
CONJ_SUFFIX_LETTERS = u"متواني"
CONJ_INFIX_LETTERS = u""
CONJ_MAX_PREFIX = 1
CONJ_MAX_SUFFIX = 3
CONJ_MIN_STEM = 2
CONJ_JOKER = u"*"
CONJ_PREFIX_LIST = ("", ar.ALEF, ar.YEH, ar.TEH, ar.NOON,
                    ar.ALEF_HAMZA_ABOVE, ar.HAMZA)
CONJ_SUFFIX_LIST = (
    "",
    ar.TEH,
    ar.TEH + ar.ALEF,
    ar.TEH + ar.MEEM,
    ar.TEH + ar.MEEM + ar.WAW,
    ar.TEH + ar.MEEM + ar.ALEF,
    ar.TEH + ar.NOON,
    ar.ALEF,
    ar.NOON,
    ar.NOON + ar.ALEF,
    ar.ALEF + ar.NOON,
    ar.WAW + ar.ALEF,
    ar.WAW + ar.NOON,
    ar.WAW,
    ar.YEH,
    ar.YEH + ar.NOON,
)
SUFFIX_LIST_STRIPOUS = set([
    u"",
    ar.TEH,
    ar.TEH + ar.ALEF,
    ar.WAW + ar.ALEF,
    ar.WAW + ar.NOON,
    ar.WAW,
    ar.YEH,
    ar.YEH + ar.NOON,
])
SUFFIX_LIST_SAKEN = set([
    u"",
    ar.TEH,
    # حالة خاصة مع الفعل الناقص
    ar.TEH + ar.ALEF,
    ar.TEH + ar.MEEM,
    #TEH+MEEM+WAW,
    ar.TEH + ar.MEEM + ar.ALEF,
    ar.TEH + ar.NOON,
    ar.NOON,
    ar.NOON + ar.ALEF,
])
SUFFIX_LIST_VOWELED = set([
    u"",
    ar.ALEF,
    ar.ALEF + ar.NOON,
    ar.NOON,
    ar.TEH,
    ar.TEH + ar.NOON,
    ar.TEH + ar.MEEM,
])
PREFIX_LIST_STRIPOUS = (ar.YEH, ar.TEH, ar.NOON,
                        ar.ALEF_HAMZA_ABOVE, ar.HAMZA)
VERBAL_CONJUGATION_AFFIX = set([
    u'-',
    u'-ا',
    u'-ت',
    u'-تا',
    u'-تم',
    u'-تما',
    u'-تنّ',
    u'-تن',
    u'-ن',
    u'-نا',
    u'-وا',
    u'أ-',
    u'أ-نّ',
    u'ا-',
    u'ا-ا',
    u'ا-انّ',
    u'ا-ن',
    u'ا-نانّ',
    u'ا-نّ',
    u'ا-وا',
    u'ا-ي',
    u'ت-',
    u'ت-ا',
    u'ت-ان',
    u'ت-انّ',
    u'ت-ن',
    u'ت-نانّ',
    u'ت-نّ',
    u'ت-وا',
    u'ت-ون',
    u'ت-ي',
    u'ت-ين',
    u'ن-',
    u'ن-نّ',
    u'ي-',
    u'ي-ا',
    u'ي-ان',
    u'ي-انّ',
    u'ي-ن',
    u'ي-نانّ',
    u'ي-نّ',
    u'ي-وا',
    u'ي-ون',
    # تمو
    ##u"-تمو",
    ##u'ي-و',
    ##u'ت-و',
    ##u'ا-و',
    ##u'-و',
    u'-ي',
    # added confirmed
    u'-تن',
    u'أ-ن',
    u'ا-ان',
    u'ا-نان',
    u'ا-ن',
    u'ت-ان',
    u'ت-نان',
    u'ت-ن',
    u'ن-ن',
    u'ي-ان',
    u'ي-نان',
    u'ي-ن',
    u'ء-ن',
    u'ء-',
])
TABLE_DOUBLE_TRANSITIVE_SUFFIX = {
    u'يك': {
        'first': u'ي',
        'second': u'ي'
    },
    u'يكما': {
        'first': u'ي',
        'second': u'ي'
    },
    u'يكم': {
        'first': u'ي',
        'second': u'ي'
    },
    u'يكن': {
        'first': u'ي',
        'second': u'ي'
    },
    u'يه': {
        'first': u'ي',
        'second': u'ي'
    },
    u'يها': {
        'first': u'ي',
        'second': u'ي'
    },
    u'يهما': {
        'first': u'ي',
        'second': u'ي'
    },
    u'يهم': {
        'first': u'ي',
        'second': u'ي'
    },
    u'يهن': {
        'first': u'ي',
        'second': u'ي'
    },
    u'نيي': {
        'first': u'ني',
        'second': u'ني'
    },
    u'نيني': {
        'first': u'ني',
        'second': u'ني'
    },
    u'نينا': {
        'first': u'ني',
        'second': u'ني'
    },
    u'نيك': {
        'first': u'ني',
        'second': u'ني'
    },
    u'نيكما': {
        'first': u'ني',
        'second': u'ني'
    },
    u'نيكم': {
        'first': u'ني',
        'second': u'ني'
    },
    u'نيكن': {
        'first': u'ني',
        'second': u'ني'
    },
    u'نيه': {
        'first': u'ني',
        'second': u'ني'
    },
    u'نيها': {
        'first': u'ني',
        'second': u'ني'
    },
    u'نيهما': {
        'first': u'ني',
        'second': u'ني'
    },
    u'نيهم': {
        'first': u'ني',
        'second': u'ني'
    },
    u'نيهن': {
        'first': u'ني',
        'second': u'ني'
    },
    u'ناي': {
        'first': u'نا',
        'second': u'نا'
    },
    u'ناني': {
        'first': u'نا',
        'second': u'نا'
    },
    u'نانا': {
        'first': u'نا',
        'second': u'نا'
    },
    u'ناك': {
        'first': u'نا',
        'second': u'نا'
    },
    u'ناكما': {
        'first': u'نا',
        'second': u'نا'
    },
    u'ناكم': {
        'first': u'نا',
        'second': u'نا'
    },
    u'ناكن': {
        'first': u'نا',
        'second': u'نا'
    },
    u'ناه': {
        'first': u'نا',
        'second': u'نا'
    },
    u'ناها': {
        'first': u'نا',
        'second': u'نا'
    },
    u'ناهما': {
        'first': u'نا',
        'second': u'نا'
    },
    u'ناهم': {
        'first': u'نا',
        'second': u'نا'
    },
    u'ناهن': {
        'first': u'نا',
        'second': u'نا'
    },
    u'كي': {
        'first': u'ك',
        'second': u'ك'
    },
    u'كنا': {
        'first': u'ك',
        'second': u'ك'
    },
    ##u'كك':{'first':u'ك','second':u'ك'},
    ##u'ككما':{'first':u'ك','second':u'ك'},
    ##u'ككم':{'first':u'ك','second':u'ك'},
    ##u'ككن':{'first':u'ك','second':u'ك'},
    u'كه': {
        'first': u'ك',
        'second': u'ك'
    },
    u'كها': {
        'first': u'ك',
        'second': u'ك'
    },
    u'كهما': {
        'first': u'ك',
        'second': u'ك'
    },
    u'كهم': {
        'first': u'ك',
        'second': u'ك'
    },
    u'كهن': {
        'first': u'ك',
        'second': u'ك'
    },
    u'كماي': {
        'first': u'كما',
        'second': u'كما'
    },
    u'كماني': {
        'first': u'كما',
        'second': u'كما'
    },
    u'كمانا': {
        'first': u'كما',
        'second': u'كما'
    },
    ##u'كماك':{'first':u'كما','second':u'كما'},
    ##u'كماكما':{'first':u'كما','second':u'كما'},
    ##u'كماكم':{'first':u'كما','second':u'كما'},
    ##u'كماكن':{'first':u'كما','second':u'كما'},
    u'كماه': {
        'first': u'كما',
        'second': u'كما'
    },
    u'كماها': {
        'first': u'كما',
        'second': u'كما'
    },
    u'كماهما': {
        'first': u'كما',
        'second': u'كما'
    },
    u'كماهم': {
        'first': u'كما',
        'second': u'كما'
    },
    u'كماهن': {
        'first': u'كما',
        'second': u'كما'
    },
    u'كموي': {
        'first': u'كم',
        'second': u'كم'
    },
    u'كموني': {
        'first': u'كم',
        'second': u'كم'
    },
    u'كمونا': {
        'first': u'كم',
        'second': u'كم'
    },
    u'كموك': {
        'first': u'كم',
        'second': u'كم'
    },
    u'كموكما': {
        'first': u'كم',
        'second': u'كم'
    },
    u'كموكم': {
        'first': u'كم',
        'second': u'كم'
    },
    u'كموكن': {
        'first': u'كم',
        'second': u'كم'
    },
    u'كموه': {
        'first': u'كم',
        'second': u'كم'
    },
    u'كموها': {
        'first': u'كم',
        'second': u'كم'
    },
    u'كموهما': {
        'first': u'كم',
        'second': u'كم'
    },
    u'كموهم': {
        'first': u'كم',
        'second': u'كم'
    },
    u'كموهن': {
        'first': u'كم',
        'second': u'كم'
    },
    u'كني': {
        'first': u'كن',
        'second': u'كن'
    },
    u'كنني': {
        'first': u'كن',
        'second': u'كن'
    },
    u'كننا': {
        'first': u'كن',
        'second': u'كن'
    },
    u'كنك': {
        'first': u'كن',
        'second': u'كن'
    },
    u'كنكما': {
        'first': u'كن',
        'second': u'كن'
    },
    u'كنكم': {
        'first': u'كن',
        'second': u'كن'
    },
    u'كنكن': {
        'first': u'كن',
        'second': u'كن'
    },
    u'كنه': {
        'first': u'كن',
        'second': u'كن'
    },
    u'كنها': {
        'first': u'كن',
        'second': u'كن'
    },
    u'كنهما': {
        'first': u'كن',
        'second': u'كن'
    },
    u'كنهم': {
        'first': u'كن',
        'second': u'كن'
    },
    u'كنهن': {
        'first': u'كن',
        'second': u'كن'
    },
    u'هي': {
        'first': u'ه',
        'second': u'ه'
    },
    u'هنا': {
        'first': u'ه',
        'second': u'ه'
    },
    u'هك': {
        'first': u'ه',
        'second': u'ه'
    },
    u'هكما': {
        'first': u'ه',
        'second': u'ه'
    },
    u'هكم': {
        'first': u'ه',
        'second': u'ه'
    },
    u'هكن': {
        'first': u'ه',
        'second': u'ه'
    },
    u'هه': {
        'first': u'ه',
        'second': u'ه'
    },
    u'هها': {
        'first': u'ه',
        'second': u'ه'
    },
    u'ههما': {
        'first': u'ه',
        'second': u'ه'
    },
    u'ههم': {
        'first': u'ه',
        'second': u'ه'
    },
    u'ههن': {
        'first': u'ه',
        'second': u'ه'
    },
    u'هاي': {
        'first': u'ها',
        'second': u'ها'
    },
    u'هاني': {
        'first': u'ها',
        'second': u'ها'
    },
    u'هانا': {
        'first': u'ها',
        'second': u'ها'
    },
    u'هاك': {
        'first': u'ها',
        'second': u'ها'
    },
    u'هاكما': {
        'first': u'ها',
        'second': u'ها'
    },
    u'هاكم': {
        'first': u'ها',
        'second': u'ها'
    },
    u'هاكن': {
        'first': u'ها',
        'second': u'ها'
    },
    u'هاه': {
        'first': u'ها',
        'second': u'ها'
    },
    u'هاها': {
        'first': u'ها',
        'second': u'ها'
    },
    u'هاهما': {
        'first': u'ها',
        'second': u'ها'
    },
    u'هاهم': {
        'first': u'ها',
        'second': u'ها'
    },
    u'هاهن': {
        'first': u'ها',
        'second': u'ها'
    },
    u'هماي': {
        'first': u'هما',
        'second': u'هما'
    },
    u'هماني': {
        'first': u'هما',
        'second': u'هما'
    },
    u'همانا': {
        'first': u'هما',
        'second': u'هما'
    },
    u'هماك': {
        'first': u'هما',
        'second': u'هما'
    },
    u'هماكما': {
        'first': u'هما',
        'second': u'هما'
    },
    u'هماكم': {
        'first': u'هما',
        'second': u'هما'
    },
    u'هماكن': {
        'first': u'هما',
        'second': u'هما'
    },
    u'هماه': {
        'first': u'هما',
        'second': u'هما'
    },
    u'هماها': {
        'first': u'هما',
        'second': u'هما'
    },
    u'هماهما': {
        'first': u'هما',
        'second': u'هما'
    },
    u'هماهم': {
        'first': u'هما',
        'second': u'هما'
    },
    u'هماهن': {
        'first': u'هما',
        'second': u'هما'
    },
    u'هموي': {
        'first': u'هم',
        'second': u'هم'
    },
    u'هموني': {
        'first': u'هم',
        'second': u'هم'
    },
    u'همونا': {
        'first': u'هم',
        'second': u'هم'
    },
    u'هموك': {
        'first': u'هم',
        'second': u'هم'
    },
    u'هموكما': {
        'first': u'هم',
        'second': u'هم'
    },
    u'هموكم': {
        'first': u'هم',
        'second': u'هم'
    },
    u'هموكن': {
        'first': u'هم',
        'second': u'هم'
    },
    u'هموه': {
        'first': u'هم',
        'second': u'هم'
    },
    u'هموها': {
        'first': u'هم',
        'second': u'هم'
    },
    u'هموهما': {
        'first': u'هم',
        'second': u'هم'
    },
    u'هموهم': {
        'first': u'هم',
        'second': u'هم'
    },
    u'هموهن': {
        'first': u'هم',
        'second': u'هم'
    },
    u'هني': {
        'first': u'هن',
        'second': u'هن'
    },
    u'هنني': {
        'first': u'هن',
        'second': u'هن'
    },
    u'هننا': {
        'first': u'هن',
        'second': u'هن'
    },
    u'هنك': {
        'first': u'هن',
        'second': u'هن'
    },
    u'هنكما': {
        'first': u'هن',
        'second': u'هن'
    },
    u'هنكم': {
        'first': u'هن',
        'second': u'هن'
    },
    u'هنكن': {
        'first': u'هن',
        'second': u'هن'
    },
    u'هنه': {
        'first': u'هن',
        'second': u'هن'
    },
    u'هنها': {
        'first': u'هن',
        'second': u'هن'
    },
    u'هنهما': {
        'first': u'هن',
        'second': u'هن'
    },
    u'هنهم': {
        'first': u'هن',
        'second': u'هن'
    },
    u'هنهن': {
        'first': u'هن',
        'second': u'هن'
    },
}
# created on fly at the program start, from the Table_affix
TABLE_AFFIX_INDEX = {
    '': {
        'pronouns':
        qutrubVerbConst.PronounsTable,
        'tenses': [
            qutrubVerbConst.TenseJussiveFuture,
            qutrubVerbConst.TensePassiveConfirmedFuture,
            qutrubVerbConst.TensePassiveFuture,
            qutrubVerbConst.TensePassiveJussiveFuture,
            qutrubVerbConst.TensePassivePast,
            qutrubVerbConst.TensePassiveSubjunctiveFuture,
            qutrubVerbConst.TensePast,
            qutrubVerbConst.TenseSubjunctiveFuture,
            qutrubVerbConst.TenseConfirmedFuture,
            qutrubVerbConst.TenseConfirmedImperative,
            qutrubVerbConst.TenseFuture,
            qutrubVerbConst.TenseImperative,
        ]
    },
}
TABLE_AFFIX = {
    u'ت-ون': [
        (u'المضارع المجهول', u'أنتم'),
        (u'المضارع المعلوم', u'أنتم'),
    ],
    u'-ن': [
        (u'الماضي المجهول', u'هن'),
        (u'الأمر المؤكد', u'أنتِ'),
        (u'الأمر المؤكد', u'أنت'),
        (u'الأمر المؤكد', u'أنتم'),
        (u'الماضي المعلوم', u'هن'),
        (u'الأمر', u'أنتن'),
    ],
    u'أ-': [
        (u'المضارع المنصوب', u'أنا'),
        (u'المضارع المجهول المجزوم', u'أنا'),
        (u'المضارع المجهول', u'أنا'),
        (u'المضارع المعلوم', u'أنا'),
        (u'المضارع المجزوم', u'أنا'),
        (u'المضارع المجهول المنصوب', u'أنا'),
    ],
    u'ت-نان': [
        (u'المضارع المؤكد الثقيل', u'أنتن'),
        (u'المضارع المؤكد الثقيل المجهول ', u'أنتن'),
    ],
    u'-ي': [
        (u'الأمر', u'أنتِ'),
    ],
    u'ت-ان': [
        (u'المضارع المؤكد الثقيل', u'أنتما مؤ'),
        (u'المضارع المؤكد الثقيل', u'أنتما'),
        (u'المضارع المؤكد الثقيل', u'هما مؤ'),
        (u'المضارع المجهول', u'أنتما مؤ'),
        (u'المضارع المجهول', u'أنتما'),
        (u'المضارع المجهول', u'هما مؤ'),
        (u'المضارع المعلوم', u'أنتما مؤ'),
        (u'المضارع المعلوم', u'أنتما'),
        (u'المضارع المعلوم', u'هما مؤ'),
        (u'المضارع المؤكد الثقيل المجهول ', u'أنتما مؤ'),
        (u'المضارع المؤكد الثقيل المجهول ', u'أنتما'),
        (u'المضارع المؤكد الثقيل المجهول ', u'هما مؤ'),
    ],
    u'ت-ا': [
        (u'المضارع المنصوب', u'أنتما مؤ'),
        (u'المضارع المنصوب', u'أنتما'),
        (u'المضارع المنصوب', u'هما مؤ'),
        (u'المضارع المجهول المجزوم', u'أنتما مؤ'),
        (u'المضارع المجهول المجزوم', u'أنتما'),
        (u'المضارع المجهول المجزوم', u'هما مؤ'),
        (u'المضارع المجزوم', u'أنتما مؤ'),
        (u'المضارع المجزوم', u'أنتما'),
        (u'المضارع المجزوم', u'هما مؤ'),
        (u'المضارع المجهول المنصوب', u'أنتما مؤ'),
        (u'المضارع المجهول المنصوب', u'أنتما'),
        (u'المضارع المجهول المنصوب', u'هما مؤ'),
    ],
    u'-وا': [
        (u'الماضي المجهول', u'هم'),
        (u'الماضي المعلوم', u'هم'),
        (u'الأمر', u'أنتم'),
    ],
    u'-تا': [
        (u'الماضي المجهول', u'هما مؤ'),
        (u'الماضي المعلوم', u'هما مؤ'),
    ],
    u'ي-ون': [
        (u'المضارع المجهول', u'هم'),
        (u'المضارع المعلوم', u'هم'),
    ],
    u'-': [
        (u'الماضي المجهول', u'هو'),
        (u'الماضي المعلوم', u'هو'),
        (u'الأمر', u'أنت'),
    ],
    u'ي-نان': [
        (u'المضارع المؤكد الثقيل', u'هن'),
        (u'المضارع المؤكد الثقيل المجهول ', u'هن'),
    ],
    u'ي-ا': [
        (u'المضارع المنصوب', u'هما'),
        (u'المضارع المجهول المجزوم', u'هما'),
        (u'المضارع المجزوم', u'هما'),
        (u'المضارع المجهول المنصوب', u'هما'),
    ],
    u'-تم': [
        (u'الماضي المجهول', u'أنتم'),
        (u'الماضي المعلوم', u'أنتم'),
    ],
    u'-تن': [
        (u'الماضي المجهول', u'أنتن'),
        (u'الماضي المعلوم', u'أنتن'),
    ],
    u'ي-ان': [
        (u'المضارع المؤكد الثقيل', u'هما'),
        (u'المضارع المجهول', u'هما'),
        (u'المضارع المعلوم', u'هما'),
        (u'المضارع المؤكد الثقيل المجهول ', u'هما'),
    ],
    u'ي-وا': [
        (u'المضارع المنصوب', u'هم'),
        (u'المضارع المجهول المجزوم', u'هم'),
        (u'المضارع المجزوم', u'هم'),
        (u'المضارع المجهول المنصوب', u'هم'),
    ],
    u'أ-ن': [
        (u'المضارع المؤكد الثقيل', u'أنا'),
        (u'المضارع المؤكد الثقيل المجهول ', u'أنا'),
    ],
    u'ت-': [
        (u'المضارع المنصوب', u'أنت'),
        (u'المضارع المنصوب', u'هي'),
        (u'المضارع المجهول المجزوم', u'أنت'),
        (u'المضارع المجهول المجزوم', u'هي'),
        (u'المضارع المجهول', u'أنت'),
        (u'المضارع المجهول', u'هي'),
        (u'المضارع المعلوم', u'أنت'),
        (u'المضارع المعلوم', u'هي'),
        (u'المضارع المجزوم', u'أنت'),
        (u'المضارع المجزوم', u'هي'),
        (u'المضارع المجهول المنصوب', u'أنت'),
        (u'المضارع المجهول المنصوب', u'هي'),
    ],
    u'ت-ين': [
        (u'المضارع المجهول', u'أنتِ'),
        (u'المضارع المعلوم', u'أنتِ'),
    ],
    u'ي-ن': [
        (u'المضارع المنصوب', u'هن'),
        (u'المضارع المؤكد الثقيل', u'هم'),
        (u'المضارع المؤكد الثقيل', u'هو'),
        (u'المضارع المجهول المجزوم', u'هن'),
        (u'المضارع المجهول', u'هن'),
        (u'المضارع المعلوم', u'هن'),
        (u'المضارع المجزوم', u'هن'),
        (u'المضارع المجهول المنصوب', u'هن'),
        (u'المضارع المؤكد الثقيل المجهول ', u'هم'),
        (u'المضارع المؤكد الثقيل المجهول ', u'هو'),
    ],
    u'-تما': [
        (u'الماضي المجهول', u'أنتما مؤ'),
        (u'الماضي المجهول', u'أنتما'),
        (u'الماضي المعلوم', u'أنتما مؤ'),
        (u'الماضي المعلوم', u'أنتما'),
    ],
    u'-ا': [
        (u'الماضي المجهول', u'هما'),
        (u'الماضي المعلوم', u'هما'),
        (u'الأمر', u'أنتما مؤ'),
        (u'الأمر', u'أنتما'),
    ],
    u'-ان': [
        (u'الأمر المؤكد', u'أنتما مؤ'),
        (u'الأمر المؤكد', u'أنتما'),
    ],
    u'ت-وا': [
        (u'المضارع المنصوب', u'أنتم'),
        (u'المضارع المجهول المجزوم', u'أنتم'),
        (u'المضارع المجزوم', u'أنتم'),
        (u'المضارع المجهول المنصوب', u'أنتم'),
    ],
    u'-نا': [
        (u'الماضي المجهول', u'نحن'),
        (u'الماضي المعلوم', u'نحن'),
    ],
    u'-نان': [
        (u'الأمر المؤكد', u'أنتن'),
    ],
    u'-ت': [
        (u'الماضي المجهول', u'أنتِ'),
        (u'الماضي المجهول', u'أنت'),
        (u'الماضي المجهول', u'أنا'),
        (u'الماضي المجهول', u'هي'),
        (u'الماضي المعلوم', u'أنتِ'),
        (u'الماضي المعلوم', u'أنت'),
        (u'الماضي المعلوم', u'أنا'),
        (u'الماضي المعلوم', u'هي'),
    ],
    u'ت-ي': [
        (u'المضارع المنصوب', u'أنتِ'),
        (u'المضارع المجهول المجزوم', u'أنتِ'),
        (u'المضارع المجزوم', u'أنتِ'),
        (u'المضارع المجهول المنصوب', u'أنتِ'),
    ],
    u'ي-': [
        (u'المضارع المنصوب', u'هو'),
        (u'المضارع المجهول المجزوم', u'هو'),
        (u'المضارع المجهول', u'هو'),
        (u'المضارع المعلوم', u'هو'),
        (u'المضارع المجزوم', u'هو'),
        (u'المضارع المجهول المنصوب', u'هو'),
    ],
    u'ن-ن': [
        (u'المضارع المؤكد الثقيل', u'نحن'),
        (u'المضارع المؤكد الثقيل المجهول ', u'نحن'),
    ],
    u'ت-ن': [
        (u'المضارع المنصوب', u'أنتن'),
        (u'المضارع المؤكد الثقيل', u'أنتِ'),
        (u'المضارع المؤكد الثقيل', u'أنت'),
        (u'المضارع المؤكد الثقيل', u'أنتم'),
        (u'المضارع المؤكد الثقيل', u'هي'),
        (u'المضارع المجهول المجزوم', u'أنتن'),
        (u'المضارع المجهول', u'أنتن'),
        (u'المضارع المعلوم', u'أنتن'),
        (u'المضارع المجزوم', u'أنتن'),
        (u'المضارع المجهول المنصوب', u'أنتن'),
        (u'المضارع المؤكد الثقيل المجهول ', u'أنتِ'),
        (u'المضارع المؤكد الثقيل المجهول ', u'أنت'),
        (u'المضارع المؤكد الثقيل المجهول ', u'أنتم'),
        (u'المضارع المؤكد الثقيل المجهول ', u'هي'),
    ],
    u'ن-': [
        (u'المضارع المنصوب', u'نحن'),
        (u'المضارع المجهول المجزوم', u'نحن'),
        (u'المضارع المجهول', u'نحن'),
        (u'المضارع المعلوم', u'نحن'),
        (u'المضارع المجزوم', u'نحن'),
        (u'المضارع المجهول المنصوب', u'نحن'),
    ],
}
EXTERNAL_PREFIX_TABLE = {}
# [ أ الإستفهام]
EXTERNAL_PREFIX_TABLE[u'أ'] = set([
    qutrubVerbConst.TenseConfirmedFuture,
    # qutrubVerbConst.TenseConfirmedImperative,
    qutrubVerbConst.TenseFuture,
    # qutrubVerbConst.TenseImperative,
    # qutrubVerbConst.TenseJussiveFuture,
    qutrubVerbConst.TensePassiveConfirmedFuture,
    qutrubVerbConst.TensePassiveFuture,
    # qutrubVerbConst.TensePassiveJussiveFuture,
    qutrubVerbConst.TensePassivePast,
    # qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TensePast,
    qutrubVerbConst.TenseSubjunctiveFuture,
])
# [و العطف]
EXTERNAL_PREFIX_TABLE[u'و'] = set([
    qutrubVerbConst.TenseConfirmedFuture,
    qutrubVerbConst.TenseConfirmedImperative,
    qutrubVerbConst.TenseFuture,
    qutrubVerbConst.TenseImperative,
    qutrubVerbConst.TenseJussiveFuture,
    qutrubVerbConst.TensePassiveConfirmedFuture,
    qutrubVerbConst.TensePassiveFuture,
    qutrubVerbConst.TensePassiveJussiveFuture,
    qutrubVerbConst.TensePassivePast,
    qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TensePast,
    qutrubVerbConst.TenseSubjunctiveFuture,
])
# [ أ الإستفهام][و العطف]
EXTERNAL_PREFIX_TABLE[u'أو'] = set([
    qutrubVerbConst.TenseConfirmedFuture,
    # qutrubVerbConst.TenseConfirmedImperative,
    qutrubVerbConst.TenseFuture,
    # qutrubVerbConst.TenseImperative,
    # qutrubVerbConst.TenseJussiveFuture,
    qutrubVerbConst.TensePassiveConfirmedFuture,
    # qutrubVerbConst.TensePassiveFuture,
    # qutrubVerbConst.TensePassiveJussiveFuture,
    qutrubVerbConst.TensePassivePast,
    # qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TensePast,
    # qutrubVerbConst.TenseSubjunctiveFuture,
])
# [ف العطف]
EXTERNAL_PREFIX_TABLE[u'ف'] = set([
    qutrubVerbConst.TenseConfirmedFuture,
    qutrubVerbConst.TenseConfirmedImperative,
    qutrubVerbConst.TenseFuture,
    qutrubVerbConst.TenseImperative,
    qutrubVerbConst.TenseJussiveFuture,
    qutrubVerbConst.TensePassiveConfirmedFuture,
    qutrubVerbConst.TensePassiveFuture,
    qutrubVerbConst.TensePassiveJussiveFuture,
    qutrubVerbConst.TensePassivePast,
    qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TensePast,
    qutrubVerbConst.TenseSubjunctiveFuture,
])
# [ف السببيّة]
#Added to Feh AlAtf
EXTERNAL_PREFIX_TABLE[u'ف'] |= set([
    qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TenseSubjunctiveFuture,
])
# [ أ الإستفهام][ف العطف]
EXTERNAL_PREFIX_TABLE[u'أف'] = set([
    qutrubVerbConst.TenseConfirmedFuture,
    # qutrubVerbConst.TenseConfirmedImperative,
    qutrubVerbConst.TenseFuture,
    # qutrubVerbConst.TenseImperative,
    # qutrubVerbConst.TenseJussiveFuture,
    qutrubVerbConst.TensePassiveConfirmedFuture,
    # qutrubVerbConst.TensePassiveFuture,
    # qutrubVerbConst.TensePassiveJussiveFuture,
    qutrubVerbConst.TensePassivePast,
    # qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TensePast,
    # qutrubVerbConst.TenseSubjunctiveFuture,
])
# [ل التوكيد]
EXTERNAL_PREFIX_TABLE[u'ل'] = set([
    qutrubVerbConst.TenseConfirmedFuture,
    # qutrubVerbConst.TenseConfirmedImperative,
    qutrubVerbConst.TenseFuture,
    # qutrubVerbConst.TenseImperative,
    # qutrubVerbConst.TenseJussiveFuture,
    qutrubVerbConst.TensePassiveConfirmedFuture,
    # qutrubVerbConst.TensePassiveFuture,
    # qutrubVerbConst.TensePassiveJussiveFuture,
    qutrubVerbConst.TensePassivePast,
    # qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TensePast,
    # qutrubVerbConst.TenseSubjunctiveFuture,
])
# [و العطف][ل التوكيد]
EXTERNAL_PREFIX_TABLE[u'ول'] = set([
    qutrubVerbConst.TenseConfirmedFuture,
    # qutrubVerbConst.TenseConfirmedImperative,
    qutrubVerbConst.TenseFuture,
    # qutrubVerbConst.TenseImperative,
    # qutrubVerbConst.TenseJussiveFuture,
    qutrubVerbConst.TensePassiveConfirmedFuture,
    # qutrubVerbConst.TensePassiveFuture,
    # qutrubVerbConst.TensePassiveJussiveFuture,
    qutrubVerbConst.TensePassivePast,
    # qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TensePast,
    # qutrubVerbConst.TenseSubjunctiveFuture,
])
# [ف العطف][ل التوكيد]
EXTERNAL_PREFIX_TABLE[u'فل'] = set([
    qutrubVerbConst.TenseConfirmedFuture,
    # qutrubVerbConst.TenseConfirmedImperative,
    qutrubVerbConst.TenseFuture,
    # qutrubVerbConst.TenseImperative,
    # qutrubVerbConst.TenseJussiveFuture,
    qutrubVerbConst.TensePassiveConfirmedFuture,
    # qutrubVerbConst.TensePassiveFuture,
    # qutrubVerbConst.TensePassiveJussiveFuture,
    qutrubVerbConst.TensePassivePast,
    # qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TensePast,
    # qutrubVerbConst.TenseSubjunctiveFuture,
])
# [ل التعليل]
# added to لام التوكيد
EXTERNAL_PREFIX_TABLE[u'ل'] |= set([
    qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TenseSubjunctiveFuture,
])
# [ أ الإستفهام][ل التعليل]
EXTERNAL_PREFIX_TABLE[u'أل'] = set([
    qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TenseSubjunctiveFuture,
])
# [و العطف][ل التعليل]
# added to لام التوكيد
EXTERNAL_PREFIX_TABLE[u'ول'] |= set([
    qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TenseSubjunctiveFuture,
])
# [ف العطف][ل التعليل]
# added to لام التوكيد
EXTERNAL_PREFIX_TABLE[u'فل'] |= set([
    qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TenseSubjunctiveFuture,
])
# [ أ الإستفهام][و العطف][ل التعليل]
EXTERNAL_PREFIX_TABLE[u'أول'] = set([
    qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TenseSubjunctiveFuture,
])
# [ أ الإستفهام][ف العطف][ل التعليل]
EXTERNAL_PREFIX_TABLE[u'أفل'] = set([
    qutrubVerbConst.TensePassiveSubjunctiveFuture,
    qutrubVerbConst.TenseSubjunctiveFuture,
])
# [ل الأمر]
#added to Lam Tawkid
EXTERNAL_PREFIX_TABLE[u'ل'] |= set([
    qutrubVerbConst.TenseJussiveFuture,
    qutrubVerbConst.TensePassiveJussiveFuture,
])
# [و العطف][ل الأمر]
#added to Lam Tawkid
EXTERNAL_PREFIX_TABLE[u'ول'] |= set([
    qutrubVerbConst.TenseJussiveFuture,
    qutrubVerbConst.TensePassiveJussiveFuture,
])
# [ف العطف][ل الأمر]
#added to Lam Tawkid
EXTERNAL_PREFIX_TABLE[u'فل'] |= set([
    qutrubVerbConst.TenseJussiveFuture,
    qutrubVerbConst.TensePassiveJussiveFuture,
])
# [س سوف]
EXTERNAL_PREFIX_TABLE[u'س'] = set([
    qutrubVerbConst.TenseFuture,
    qutrubVerbConst.TensePassiveFuture,
])
# [ أ الإستفهام][س سوف]
EXTERNAL_PREFIX_TABLE[u'أس'] = set([
    qutrubVerbConst.TenseFuture,
    qutrubVerbConst.TensePassiveFuture,
])
# [و العطف][س سوف]
EXTERNAL_PREFIX_TABLE[u'وس'] = set([
    qutrubVerbConst.TenseFuture,
    qutrubVerbConst.TensePassiveFuture,
])
# [ف العطف][س سوف]
EXTERNAL_PREFIX_TABLE[u'فس'] = set([
    qutrubVerbConst.TenseFuture,
    qutrubVerbConst.TensePassiveFuture,
])
# [ أ الإستفهام][و العطف][س سوف]
EXTERNAL_PREFIX_TABLE[u'أوس'] = set([
    qutrubVerbConst.TenseFuture,
    qutrubVerbConst.TensePassiveFuture,
])
# [ أ الإستفهام][ف العطف][س سوف]
EXTERNAL_PREFIX_TABLE[u'أفس'] = set([
    qutrubVerbConst.TenseFuture,
    qutrubVerbConst.TensePassiveFuture,
])
EXTERNAL_SUFFIX_TABLE = {}
# تصلح فقط مع الأفعال الخمسة
#ToDo
# التحقق من يالء مع ا\لأفعال  الخمسة فقط
EXTERNAL_SUFFIX_TABLE[u'ي'] = (
    # qutrubVerbConst.PronounAna, #u"أنا";
    # qutrubVerbConst.PronounNahnu,#u"نحن";
    # qutrubVerbConst.PronounAnta,   #u"أنت";
    qutrubVerbConst.PronounAnti,  #u"أنتِ";
    qutrubVerbConst.PronounAntuma,  #u"أنتما";
    qutrubVerbConst.PronounAntuma_f,  #u"أنتما مؤ";
    qutrubVerbConst.PronounAntum,  #u"أنتم";
    # qutrubVerbConst.PronounAntunna,   #u"أنتن";
    # qutrubVerbConst.PronounHuwa,   #u"هو";
    # qutrubVerbConst.PronounHya,   #u"هي";
    # qutrubVerbConst.PronounHuma,   #u"هما";
    # qutrubVerbConst.PronounHuma_f,   #u"هما مؤ";
    # qutrubVerbConst.PronounHum,   #u"هم";
    # qutrubVerbConst.PronounHunna,   #u"هن";
)
EXTERNAL_SUFFIX_TABLE[u'ني'] = (
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAna,  #u"أنا";
    # qutrubVerbConst.PronounNahnu,#u"نحن";
    qutrubVerbConst.PronounAnta,  #u"أنت";
    qutrubVerbConst.PronounAnti,  #u"أنتِ";
    qutrubVerbConst.PronounAntuma,  #u"أنتما";
    qutrubVerbConst.PronounAntuma_f,  #u"أنتما مؤ";
    qutrubVerbConst.PronounAntum,  #u"أنتم";
    qutrubVerbConst.PronounAntunna,  #u"أنتن";
    qutrubVerbConst.PronounHuwa,  #u"هو";
    qutrubVerbConst.PronounHya,  #u"هي";
    qutrubVerbConst.PronounHuma,  #u"هما";
    qutrubVerbConst.PronounHuma_f,  #u"هما مؤ";
    qutrubVerbConst.PronounHum,  #u"هم";
    qutrubVerbConst.PronounHunna,  #u"هن";
)
EXTERNAL_SUFFIX_TABLE[u'نا'] = (
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAna,  #u"أنا";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounNahnu,  #u"نحن";
    qutrubVerbConst.PronounAnta,  #u"أنت";
    qutrubVerbConst.PronounAnti,  #u"أنتِ";
    qutrubVerbConst.PronounAntuma,  #u"أنتما";
    qutrubVerbConst.PronounAntuma_f,  #u"أنتما مؤ";
    qutrubVerbConst.PronounAntum,  #u"أنتم";
    qutrubVerbConst.PronounAntunna,  #u"أنتن";
    qutrubVerbConst.PronounHuwa,  #u"هو";
    qutrubVerbConst.PronounHya,  #u"هي";
    qutrubVerbConst.PronounHuma,  #u"هما";
    qutrubVerbConst.PronounHuma_f,  #u"هما مؤ";
    qutrubVerbConst.PronounHum,  #u"هم";
    qutrubVerbConst.PronounHunna,  #u"هن";
)
# للمذكر: يحذف صمير المؤنث
# للمؤنث يحذف صمير المذكر
EXTERNAL_SUFFIX_TABLE[u'ك'] = (
    qutrubVerbConst.PronounAna,  #u"أنا";
    qutrubVerbConst.PronounNahnu,  #u"نحن";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAnta,  #u"أنت";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAnti,  #u"أنتِ";
    # qutrubVerbConst.PronounAntuma,   #u"أنتما";
    # qutrubVerbConst.PronounAntuma_f,   #u"أنتما مؤ";
    # qutrubVerbConst.PronounAntum,   #u"أنتم";
    # qutrubVerbConst.PronounAntunna,   #u"أنتن";
    qutrubVerbConst.PronounHuwa,  #u"هو";
    qutrubVerbConst.PronounHya,  #u"هي";
    qutrubVerbConst.PronounHuma,  #u"هما";
    qutrubVerbConst.PronounHuma_f,  #u"هما مؤ";
    qutrubVerbConst.PronounHum,  #u"هم";
    qutrubVerbConst.PronounHunna,  #u"هن";
)
EXTERNAL_SUFFIX_TABLE[u'كما'] = (
    qutrubVerbConst.PronounAna,  #u"أنا";
    qutrubVerbConst.PronounNahnu,  #u"نحن";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAnta,  #u"أنت";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAnti,  #u"أنتِ";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAntuma,  #u"أنتما";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAntuma_f,  #u"أنتما مؤ";
    # qutrubVerbConst.PronounAntum,   #u"أنتم";
    # qutrubVerbConst.PronounAntunna,   #u"أنتن";
    qutrubVerbConst.PronounHuwa,  #u"هو";
    qutrubVerbConst.PronounHya,  #u"هي";
    qutrubVerbConst.PronounHuma,  #u"هما";
    qutrubVerbConst.PronounHuma_f,  #u"هما مؤ";
    qutrubVerbConst.PronounHum,  #u"هم";
    qutrubVerbConst.PronounHunna,  #u"هن";
)
EXTERNAL_SUFFIX_TABLE[u'كم'] = (
    qutrubVerbConst.PronounAna,  #u"أنا";
    qutrubVerbConst.PronounNahnu,  #u"نحن";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAnta,  #u"أنت";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAnti,  #u"أنتِ";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAntuma,  #u"أنتما";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAntuma_f,  #u"أنتما مؤ";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAntum,  #u"أنتم";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAntunna,  #u"أنتن";
    qutrubVerbConst.PronounHuwa,  #u"هو";
    qutrubVerbConst.PronounHya,  #u"هي";
    qutrubVerbConst.PronounHuma,  #u"هما";
    qutrubVerbConst.PronounHuma_f,  #u"هما مؤ";
    qutrubVerbConst.PronounHum,  #u"هم";
    qutrubVerbConst.PronounHunna,  #u"هن";
)
EXTERNAL_SUFFIX_TABLE[u'كن'] = (
    qutrubVerbConst.PronounAna,  #u"أنا";
    qutrubVerbConst.PronounNahnu,  #u"نحن";
    # qutrubVerbConst.PronounAnta,   #u"أنت";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAnti,  #u"أنتِ";
    qutrubVerbConst.PronounAntuma,  #u"أنتما";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAntuma_f,  #u"أنتما مؤ";
    # qutrubVerbConst.PronounAntum,   #u"أنتم";
    # أفعال القلوب المتعدية لمفعول به عاقل
    qutrubVerbConst.PronounAntunna,  #u"أنتن";
    qutrubVerbConst.PronounHuwa,  #u"هو";
    qutrubVerbConst.PronounHya,  #u"هي";
    qutrubVerbConst.PronounHuma,  #u"هما";
    qutrubVerbConst.PronounHuma_f,  #u"هما مؤ";
    qutrubVerbConst.PronounHum,  #u"هم";
    qutrubVerbConst.PronounHunna,  #u"هن";
)
# This cases take all Pronoun
EXTERNAL_SUFFIX_TABLE[u'ه'] = qutrubVerbConst.PronounsTable
EXTERNAL_SUFFIX_TABLE[u'ها'] = qutrubVerbConst.PronounsTable
EXTERNAL_SUFFIX_TABLE[u'هما'] = qutrubVerbConst.PronounsTable
EXTERNAL_SUFFIX_TABLE[u'هم'] = qutrubVerbConst.PronounsTable
EXTERNAL_SUFFIX_TABLE[u'هنّ'] = qutrubVerbConst.PronounsTable
EXTERNAL_SUFFIX_TABLE[u'هن'] = qutrubVerbConst.PronounsTable
