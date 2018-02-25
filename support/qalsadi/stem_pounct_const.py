#!/usr/bin/python
# -*- coding=utf-8 -*-
"""
Constants for pounctuation stemming
"""
POUNCTUATION = {}

POUNCTUATION[u'.'] = {
    'word': u'.',
    'tags': u'نقطة:break',
}
POUNCTUATION[u'~'] = {
    'word': u'~',
    'tags': u'شفاف',
}

POUNCTUATION[u','] = {
    'word': u',',
    'tags': u'فاصلة:break',
}
POUNCTUATION[u'،'] = {
    'word': u'،',
    'tags': u'فاصلة:break',
}
#POUNCTUATION[u',']={'word':u',', 'tags':u'فاصلة:شفاف',}
#POUNCTUATION[u'،']={'word':u'،', 'tags':u'فاصلة:شفاف',}

POUNCTUATION[u'?'] = {
    'word': u'?',
    'tags': u'استفهام:break',
}
POUNCTUATION[u'؟'] = {
    'word': u'؟',
    'tags': u'استفهام:break',
}
POUNCTUATION[u'!'] = {
    'word': u'!',
    'tags': u'تعجب:break',
}

POUNCTUATION[u';'] = {
    'word': u';',
    'tags': u'نقطة فاصلة:break',
}
POUNCTUATION[u'-'] = {
    'word': u'-',
    'tags': u'مطة:break',
}

POUNCTUATION[u':'] = {
    'word': u':',
    'tags': u'نقطتان:break',
}

POUNCTUATION[u"'"] = {
    'word': u"'",
    'tags': u'تنصيص مفرد:شفاف',
}
POUNCTUATION[u" "] = {
    'word': u" ",
    'tags': u'فراغ:شفاف',
}

POUNCTUATION[u'"'] = {
    'word': u'"',
    'tags': u'تنصيص مزدوج:شفاف',
}

POUNCTUATION[u')'] = {
    'word': u')',
    'tags': u'قوس',
}
POUNCTUATION[u'('] = {
    'word': u'(',
    'tags': u'قوس',
}

POUNCTUATION[u'['] = {
    'word': u'[',
    'tags': u'عارضة',
}
POUNCTUATION[u']'] = {
    'word': u']',
    'tags': u'عارضة',
}

POUNCTUATION[u'{'] = {
    'word': u'{',
    'tags': u'حاضنة',
}
POUNCTUATION[u'}'] = {
    'word': u'}',
    'tags': u'حاضنة:break',
}
#treat newline as pounct for now
POUNCTUATION[u'\n'] = {
    'word': u'\n',
    'tags': u'سطر جديد:newline:break',
}
