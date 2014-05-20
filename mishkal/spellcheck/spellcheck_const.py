#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        spellcheck
# Purpose:     Arabic spellchecking.
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
import pyarabic.araby as araby

Alphabet = u'Ø°Ø¶ØµØ«Ù‚ÙØºØ¹Ù‡Ø®Ø­Ø¬Ø¯Ø·ÙƒÙ…Ù†ØªØ§Ù„Ø¨ÙŠØ³Ø´Ø¸Ø²ÙˆØ©Ù‰Ø±Ø¤Ø¡Ø¦Ø£Ø¥Ø¢'
TabReplacment=[
#common spelling error
(araby.ALEF_MAKSURA, araby.YEH),
(araby.TEH_MARBUTA	, araby.HEH),

(araby.ALEF			, araby.ALEF_HAMZA_ABOVE),
(araby.ALEF			, araby.ALEF_HAMZA_BELOW),
(araby.HAMZA			, araby.ALEF_HAMZA_BELOW),
(araby.WAW_HAMZA			, araby.YEH_HAMZA),
(araby.YEH_HAMZA			, araby.WAW_HAMZA),



# o	ÅÛİÇá ÒÑ ÇáÅÒÇÍÉ shift
# ?	Ûíä åãÒÉ ÊÍÊ ÇáÃáİ
# ?	Ã Ç
# o	ÇáãÊÔÇßáÇÊ : ÍÑæİ áåÇ äİÓ ÇáÔßá ÈäŞØ ãÎÊáİÉ
# ?	È Ê ä Ë í
# ?	Ì Í Î
# ?	Ï Ğ
# ?	Ñ Ò
# ?	Ô Ó
# ?	Õ Ö
# ?	Ø Ù
# ?	Ú Û
# ?	İ Ş
# ?	É å 
# o	ÇáãÊÔÇÈåÇÊ ÑÓãÇ
# ?	Ç Ã Â Å 
# o	ÇáåãÒÇÊ 
# ?	Ã Á Ä Æ Å ìÁ Â
# o	ÇáãÊÔÇÈåÇÊ áİÙÇ
# ?	ãÕÑí:
# •	Ò Ğ
# •	Ë Ó
# •	Ş Ã
# ?	ÎáíÌí
# •	Ì í
# ?	ÚÇã
# •	Õ Ó 
# •	Ë Ê
# •	Ù Ö
#common pronciation error
(araby.DAD			, araby.ZAH),
(araby.ZAH			, araby.DAD),
(araby.THAL, 	araby.ZAIN),
(araby.ZAIN,	araby.THAL),
(araby.SEEN,	araby.THEH),
(araby.THEH,	araby.SEEN),
(araby.QAF,	araby.ALEF_HAMZA_ABOVE),
(araby.QAF,	araby.ALEF_HAMZA_BELOW),
(araby.JEEM,	araby.YEH),
(araby.YEH,	araby.JEEM),
(araby.SAD,	araby.SEEN),
(araby.SEEN,	araby.SAD),
(araby.THEH,	araby.TEH),

# o	ÇáÃÎØÇÁ ÇáÅãáÇÆí
# ?	Ê É
# ?	Ç ì
(araby.TEH,			araby.TEH_MARBUTA),
(araby.TEH_MARBUTA,	araby.TEH),
(araby.ALEF_MAKSURA, araby.ALEF),




]