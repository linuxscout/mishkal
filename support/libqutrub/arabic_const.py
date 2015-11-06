#!/usr/bin/python
# -*- coding=utf-8 -*-
#---
# $Id: arabic_const.py,v 1.6 2003/04/22 17:18:22 elzubeir Exp $
#
# ------------
# Description:
# ------------
#
# Arabic codes
#
# (C) Copyright 2003, Arabeyes, Mohammed Elzubeir
# -----------------
# Revision Details:    (Updated by Revision Control System)
# -----------------
#  $Date: 2003/04/22 17:18:22 $
#  $Author: elzubeir $
#  $Revision: 1.6 $
#  $Source: /home/arabeyes/cvs/projects/duali/pyduali/pyduali/arabic.py,v $
#
#  This program is written under the BSD License.
#---

COMMA            = u'\u060C'
SEMICOLON        = u'\u061B'
QUESTION         = u'\u061F'
HAMZA            = u'\u0621'
ALEF_MADDA       = u'\u0622'
ALEF_HAMZA_ABOVE = u'\u0623'
WAW_HAMZA        = u'\u0624'
ALEF_HAMZA_BELOW = u'\u0625'
YEH_HAMZA        = u'\u0626'
ALEF             = u'\u0627'
BEH              = u'\u0628'
TEH_MARBUTA      = u'\u0629'
TEH              = u'\u062a'
THEH             = u'\u062b'
JEEM             = u'\u062c'
HAH              = u'\u062d'
KHAH             = u'\u062e'
DAL              = u'\u062f'
THAL             = u'\u0630'
REH              = u'\u0631'
ZAIN             = u'\u0632'
SEEN             = u'\u0633'
SHEEN            = u'\u0634'
SAD              = u'\u0635'
DAD              = u'\u0636'
TAH              = u'\u0637'
ZAH              = u'\u0638'
AIN              = u'\u0639'
GHAIN            = u'\u063a'
TATWEEL          = u'\u0640'
FEH              = u'\u0641'
QAF              = u'\u0642'
KAF              = u'\u0643'
LAM              = u'\u0644'
MEEM             = u'\u0645'
NOON             = u'\u0646'
HEH              = u'\u0647'
WAW              = u'\u0648'
ALEF_MAKSURA     = u'\u0649'
YEH              = u'\u064a'
MADDA_ABOVE      = u'\u0653'
HAMZA_ABOVE      = u'\u0654'
HAMZA_BELOW      = u'\u0655'
ZERO             = u'\u0660'
ONE              = u'\u0661'
TWO              = u'\u0662'
THREE            = u'\u0663'
FOUR             = u'\u0664'
FIVE             = u'\u0665'
SIX              = u'\u0666'
SEVEN            = u'\u0667'
EIGHT            = u'\u0668'
NINE             = u'\u0669'
PERCENT          = u'\u066a'
DECIMAL          = u'\u066b'
THOUSANDS        = u'\u066c'
STAR             = u'\u066d'
MINI_ALEF        = u'\u0670'
ALEF_WASLA       = u'\u0671'
FULL_STOP        = u'\u06d4'
BYTE_ORDER_MARK  = u'\ufeff'

# Diacritics
FATHATAN         = u'\u064b'
DAMMATAN         = u'\u064c'
KASRATAN         = u'\u064d'
FATHA            = u'\u064e'
DAMMA            = u'\u064f'
KASRA            = u'\u0650'
SHADDA           = u'\u0651'
SUKUN            = u'\u0652'

SMALL_ALEF=u"\u0670"
SMALL_WAW=u"\u06E5"
SMALL_YEH=u"\u06E6"

#---------------------------------------------------------------------------
# Arabic ligatures
#---------------------------------------------------------------------------

LAM_ALEF=u'\ufefb'
LAM_ALEF_HAMZA_ABOVE=u'\ufef7'
LAM_ALEF_HAMZA_BELOW=u'\ufef9'
LAM_ALEF_MADDA_ABOVE=u'\ufef5'
simple_LAM_ALEF=LAM+ALEF
simple_LAM_ALEF_HAMZA_ABOVE=LAM+ALEF_HAMZA_ABOVE
simple_LAM_ALEF_HAMZA_BELOW=LAM+ALEF_HAMZA_BELOW
simple_LAM_ALEF_MADDA_ABOVE=LAM+HAMZA+FATHA+ALEF


