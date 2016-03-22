#!/usr/bin/python
# -*- coding = utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        sem_const
# Purpose:     Arabic semantic analyzer Asmai
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     29-11-2012
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------

#semantic table
# this is a simulation for a database only
# temporary
Subject=u'Subject'
Predicate=u'Predicate'
Added = u'Added'
Adj =u'Adj'
#~ Subject=u'فاعلية'
#~ Predicate=u'مفعولية'
#~ Added = u'مضاف إليه'
#~ Adj =u'نعت'
#~ SemanticTable={
 #~ u'طَلَع شَمْس':Subject,
 #~ u'عَبَد الله':Predicate,
#~ u'شَرَحَ دَرْسٌ':Predicate,
#~ u'شَرَحَ كِتَابٌ':Predicate,
#~ u'شَرَحَ شّيْخٌ':Subject,
#~ u'شَرَّحَ طَبِيبٌ':Subject,
#~ u'شَبَّ نَارٌ':Subject,
#~ u'عَالَجَ مَرِيضٌ':Predicate,
#~ u'رَسُولٌ اللهُ':Added,
#~ u'نَسَبٌ كَرِيمٌ':Adj,
#~ u'أَكَلَ فَاكِهَةٌ':Predicate,
#~ u'حَرَثَ أَرْضٌ':Predicate,
#~ u'اِنْكَسَرَ زُجاجٌ':Subject,
#~ u'غَرَّدَ عَصْفُورٌ':Subject,
#~ }

# This table contains extracted data about verbs and their derivations
# for example the verb "use" استعمل has three dérivations:
# subjective adjective نعت اسم فاعل  => مستعمِل user
# objective adjective نعت اسم مفعول => مستعمَل used
# addition nominal المصدر => استعمال use
# This table is used temporaly in order to simulate database to be created after tests.
# this Data alow us to select approiate vocalized form
# هذا الجدول مؤقت لمحاكاة قاعدة بيانات دلالية ستنشأ بعد الفحوص
# في الجدول علاقات دلالية تتيح اختيار الكلمة المناسبة في السياق حسب العلاقة الدلاليةد
# مثال
#~ استعمل القلم => علاقة مفعولية 
#~ نستنتج منها القلم مستعمل مفعول
#~ يستعمل القلم => علاقة فعل ونائب فاعل
#~ 
#~ SEM_RELATION_TABLE ={
#~ u'اِسْتَعْمَلَ':{
#~ u"قَلَمٌ":Subject,
#~ u"قَلَمٌ":Predicate,
#~ },
#~ u'شَرَّحَ':{
#~ u"طَبِيبٌ":Subject,
#~ u"جَسَدٌ":Predicate,
#~ u"طَبِيبٌ":Predicate,
#~ },
#~ u'نَشَّطَ': {
#~ u"دَوَاءٌ":Subject,
#~ u"دَواءٌ":Predicate,
#~ u"دَوَاءٌ":Predicate,
#~ },
#~ 
#~ }
#~ 
#~ SEM_DERIVATION_TABLE = {
#~ u'اِسْتَعْمَلَ': {"trans":True, 'subj':u'مُسْتَعْمِلٌ', 'obj':u'مُسْتَعْمَلٌ', "add":u"اِسْتِعْمَالٌ"},
#~ u'شَرَّحَ': {"trans":True, 'subj':u'مُشَرِّحٌ', 'obj':u'مُشَرَّحٌ', "add":u"تَشْرِيحٌ"},
#~ u'نَشَّطَ': {"trans":True, 'subj':u'مُنَشِّطٌ', 'obj':u'مُنَشَّطٌ', "add":u"تَنْشِيطٌ"},
#~ }
