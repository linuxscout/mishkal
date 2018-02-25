#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        analex_const
# Purpose:     Arabic lexical analyser constants, provides feature for stemming arabic word
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
"""Constants for analex"""
PARTIAL_VOCALIZED_TAG = u'مدخل مشكول'
#fields names and abbriviations

ANALEX_FIELDS_WORD = {
    'word': 'w',
    'affix': 'a',
    'procletic': 'pp',
    'encletic': 'ss',
    'prefix': 'p',
    'suffix': 's',
    'stem': 'st',
    'original': 'o',
    'vocalized': 'v',
    'semivocalized': 'sv',
    'tags': 'tg',
    'type': 't',
    'freq': 'f',
    'originaltags': 'ot',
    'syntax': 'sy',
}
