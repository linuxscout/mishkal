#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        disambig_const.py# Purpose:     Arabic lexical analyser constants used for disambiguation before analysis## Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)## Created:     31-10-2011# Copyright:   (c) Taha Zerrouki 2011# Licence:     GPL#-------------------------------------------------------------------------------
# import  pyarabic.araby as arabyDISAMBIGUATATION_TABLE={ # إذا كانت الكلمة الحالية "أن" تكون "أنْ" حرف نصب إذا سبقت فعلا # وتكون أنّ، من أخوات إنّ إذا كان ما بعدها اسماu'أن':{'verb':{'tag':'t','vocalized':u'أَنْ'},		'noun':{'tag':'t','vocalized':u'أنَّ'},	}, # إذا كانت الكلمة الحالية "من" تكون "مَنْ" حرف استفهام  إذا سبقت فعلا # وتبقى ملتبسة إذا سبقت اسما.# u'أن':{'verb':{'tag':'t','vocalized':u'مَنْ'},		# 'noun':{'tag':'t','vocalized':u'من'},	# },# u'ثنا':{'abbr':u'ثَنَا',}	}

