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
Subject=u'فاعلية'
Predicate=u'مفعولية'
Added = u'مضاف إليه'
Adj =u'نعت'
SemanticTable={
 u'طَلَع شَمْس':Subject,
 u'عَبَد الله':Predicate,
u'شَرَحَ دَرْسٌ':Predicate,
u'شَرَحَ كِتَابٌ':Predicate,
u'شَرَحَ شّيْخٌ':Subject,
u'شَرَّحَ طَبِيبٌ':Subject,
u'شَبَّ نَارٌ':Subject,
u'عَالَجَ مَرِيضٌ':Predicate,
u'رَسُولٌ اللهُ':Added,
u'نَسَبٌ كَرِيمٌ':Adj,
u'أَكَلَ فَاكِهَةٌ':Predicate,
u'حَرَثَ أَرْضٌ':Predicate,
u'اِنْكَسَرَ زُجاجٌ':Subject,
u'غَرَّدَ عَصْفُورٌ':Subject,
 }

