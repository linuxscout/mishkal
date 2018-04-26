#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        syn_const
# Purpose:     Arabic syntaxic analyser constants.
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#------------------------------------------------------------------------------
import libqutrub.verb_const as vconst
#-------------------
NOMINAL_FACTOR_LIST =set([
        u"في",
        u"بأن",
        u"بين",
        u"ففي",
        u"وفي",
        u"عن",
        u"إلى",
        u"على",
        u"بعض",
        u"تجاه",
        u"تلقاء",
        u"جميع",
        u"حسب",
        u"سبحان",
        u"سوى",
        u"شبه",
        u"غير",
        u"كل",
        u"لعمر",
        u"مثل",
        u"مع",
        u"معاذ",
        u"نحو",
        u"خلف",
        u"أمام",
        u"فوق",
        u"تحت",
        u"يمين",
        u"شمال",
        u"دون",
        u"من",
        u"بدون",
        u"خلال",
        u"أثناء",
        #vovalized factor
        u'أَنِّ',
        u'إِنَّ',
]);
KanaSisters_LIST=set([
# yahia alhadj
u'كان',
u'يكون',
u'كانت',
u'صار',
u'صارت',
u'يصير',
u'أمسى',
u'يمسي',
u'أمست',
u'تمسي',
u'ليس',
u'ليست',
u'ظلّ',
u'ظلّت',
u'أضحى',
u'أضحت',
u'يضحي',
u'تضحي',
u'أصبح',
u'أصبحت',
u'يصبح',
u'تصبح',
u'بات',
u'باتت',
u'يبيت',
u'تبيت',

u'مازال',
u'لازال',
u'لايزال',
u'لازالت',
u'مايزال',
u'مازالت',
u'ماتزال',
u'مابرح',
u'مايبرح',
u'مابرحت',
u'ماانفك',
u'ماانفكّت',
u'ماينفك',
u'لاينفك',
u'مادام',
u'مادامت',

]);
#-------------------
RAFE3_LIST=set([
u'أنه',
u'أنك',
u'أنها',
u'بأنها',
u'بأنه',
u'وأنها',
u'فأنها',
u'فأنه',
u'كأنه',
u'كأنها',

# yahia alhadj
u'كان',
u'يكون',
u'كانت',
u'صار',
u'صارت',
u'يصير',
u'أمسى',
u'ليس',
u'ليست',
u'ظلّ',
u'ظلّت',
u'أضحى',
u'أضحت',
u'يضحي',
u'أصبح',
u'أصبحت',
u'يصبح',
u'بات',
u'باتت',
u'يبيت',
u'مازال',
u'لازال',
u'لايزال',
u'لازالت',
u'مايزال',
u'مازالت',
u'ماتزال',
u'مابرح',
u'مايبرح',
u'مابرحت',
u'ماانفك',
u'ماانفكّت',
u'ماينفك',
u'لاينفك',
u'مادام',
u'مادامت',
u'نعم',
u'بئس',
u'حبذا',

#إضافي
u'هل',
#u'من',
u'ما',
u'متى',
u'أين',
u'ماذا',
u'كيف',
u'أيان',
#اسماء الإشارة بعد فاء الإستئناف
u'فهذا',
u'فذلك',
u'فتلك',
u'فهؤلاء',
u'فأولئك',
u'فذلكم',
u'فهذه',
#ضمائر الرفع المنفصلة
u'هو',
u'هما',
u'هم',
u'هي',
u'هما',
u'هن',
u'أنت',
u'أنتما',
u'أنتم',
u'أنت',
u'أنتما',
u'أنتن',
u'أنا',
u'نحن',
u'إذ', 

#--------------
u'ثنا',
u'أَمّا',
u'وأما',
u'وَأَمَّا',
]);

JAR_LIST=set([
u'من', 
u'عن', 
u'إلى',
u'على',
u'في',
u'رب',
u'منذ',
u'مذ',
u'عدا',
u'خلا',
u'حاشا',

u'عند',
u'أمام',
u'وراء',
u'خلف',
u'مع',
u'قبل',
u'بعد',
u'تحت',
u'أي',
u'كلّ',
u'بعض',
u'غير',
u'سوى',
u'ليل',
u'شمال',
u'جنوب',
u'يمين',
u'شرق',
u'غرب',
u'شطر',
u'أسفل',
u'أعلى',
u'جنب',
u'جانب',
u'تلقاء',
u'قدام',

u'أعلى',
u'شهر',
u'سنة',
u'غروب',
u'شروق',
u'دون',
u'شهور',

u'يوم',
u'حين',
u'ساعة',
u'زمان',
u'أزمان',
u'أيام',
u'أوقات',
u'وقت',
u'لحظة',

u'خلال',
u"بدون",

u"أثناء",
u"ذات",
u"ذو",
U"ذي",
u"ذوو",
u"ذوات",
u"ذوي",
u"بن",
u"ابن",
u"بنت",
u'بين',
# صيغ واضحة الإضافة

u'أبو',
u'أبي',
u'وأبو',
u'وأبي',
u'وأبا',
u'أبا',

u'أخو',
u'بواسطة',

u'فَوْقَ',
u'مِنْ',

u'إِلَى',
u'رُبَّ',
u'عَلَى',
u'عَنْ',
u'فِي',
u'مِنْ',
u'عَمَّا',
u'حَتَّى',
u'مُنْذُ',
u'مُذْ',
u'فَإِلَى',
u'فَرُبَّ',
u'فَعَلَى',
u'فَعَنْ',
u'فَفِي',
u'فَمِنْ',
u'فَعَمَّا',
u'فَحَتَّى',
u'فَمُنْذُ',
u'فَمُذْ',
u'وَإِلَى',
u'وَرُبَّ',
u'وَعَلَى',
u'وَعَنْ',
u'وَفِي',
u'وَمِنْ',
u'وَعَمَّا',
u'وَحَتَّى',
u'وَمُنْذُ',
u'وَمُذْ',

u'بِلَا',
u'بلا',
#
u'مِنْ',
u'عَنْ',
u'إِلَى',
u'عَلَى',
u'فِي',
u'رُبَّ',
u'مُنْذُ',
u'مُذْ',
u'عَدَا',
u'خَلَا',
u'حَاشَا',
u'عِنْدَ',
u'أَمَامَ',
u'وَراءَ',
u'خَلْفَ',
u'مَعَ',
u'قَبْلَ',
u'بَعْدَ',
u'تَحْتَ',
u'أَيُّ',
u'كلّ',
u'بَعْضُ',
u'غَيْرَ',
u'سِوَى',
u'لَيْلَ',
u'شَمَالَ',
u'جَنُوبَ',
u'يَمِينَ',
u'شَرِقَ',
u'غَرِبَ',

u'شَطَرَ',
u'أَسْفَلَ',
u'أَعَلَى',
u'جَنَبَ',
u'جَانِبَ',
u'تِلْقَاءَ',
u'قدامُ',
u'أَعَلَى',
u'شَهَرَ',
u'سَنَةُ',
u'غُرُوبُ',
u'شُرُوقُ',
u'دُونَ',
u'شهور',
u'يَوْمَ',
u'حِينَ',
u'سَاعَةُ',
u'زَمانُ',
#~u'أَزَمانُ',
#~u'أيَّامُ',
u'أَوََقَاتَ',
u'وَقْتَ',
u'لَحْظَةُ',
u'خِلَالَ',
u"بِدونِ",
u"أَثَناءَ",
u"ذَاتُ",
u"ذُو",
u"ذِي",
u"ذُوُو",
u"ذُوَاتُ",
u"ذَوِيَ",
u"بْنُ",
u"اِبْنُ",
#~u"بُنْتِ",
u'بَيْنَ',
# صِيغَ وَاضِحَةُ الْإضافَةِ 
u'أَبُو',
u'أَخُو',
u'بِوَاسِطَةِ',
]);

JAZEM_LIST=set([
u'لم',
u'لما',
u'مهما',
u'حيثما',
u'أينما',
u'كيفما',
u'لا', # لا الناهية
u'ولا',
u'فلا',
u'إن', 
u'إِنْ',
u'لَمْ',
u'لَمَّا',
u'مَهْمَا',
u'حَيْثُمَا',
u'أَيْنَمَا',
u'كَيْفَمَا',
u'لَا',
u'وَلَا',
u'فَلَا',
]);

VERB_NASEB_LIST=set([
u'أن',
u'كي',
u'لن',
u'حتى',
u'إذن',
u'لئلا', 
#vocalized factor
u'أَنْ',
u'كَيْ',
u'لَنْ',
u'حَتَّى',
u'إِذَنْ',
u'لِئَلَا',
]);

VERB_RAFE3_LIST=set([
#لا النافية
u'لا',
u'ولا',
u'فلا',
u'لَا',
u'وَلَا',
u'فَلَا',


u'هل',
u'من',
u'ما',
u'متى',
u'أين',
u'ماذا',
u'كيف',
u'أيان',
u'يوم',
u'حين',
u'ساعة',
u'زمان',
u'أزمان',
u'أيام',
u'أوقات',
u'وقت',
u'لحظة',

#vocalized
u'هَلْ',
u'مَنْ',
u'مَا',
u'مَتَى',
u'أَيْنَ',
u'مَاذَا',
u'كَيْفَ',
u'ّأَيَّانَ',
u'يَوْمُ',
u'حِينَ',
u'سَاعَةُ',
u'زَمانُ',
u'أَزَمانُ',
u'أيَّامُ',
u'أَوََقَاتَ',
u'وَقَّتَ',
u'لَحْظَةُ',
]);

NOUN_NASEB_LIST=set([
#~u'أن',
#~u'إن',
#~u'فإن',
#~u'لأن',
#~u'كأن',
#~u'لكن',
#~u'ليت',
#~u'لعل',
#vocalized factor
u'أَنَّ',
u'فَإَنَّ',
u'أَنَّ',
u'إِنَّ',
u'فَإِنَّ',
u'لِأَنَّ',
u'كَأَنِّ',
u'لَكِنَّ',
u'لَيْتَ',
u'لَعَلَّ',
]);


VERBAL_FACTOR_LIST=set([
        u"قد",
        u"فقد",
        u"وقد",
        u"لن",
        u"لم",
        #vovalized factor
        u'أَنْ',
        u'إِنْ',
        
]);





NominalPhrase=[
    "NN.",
    "NNN.",
    "NNNN.",
    "NSN.",
    "NNSN.",
    "NSNN.",
    "NSNNN.",
    "NSNSN.",
    "NSSN.",
    "NSSNN.",
    "NV.",
    "NVN.",
    "NVNN.",
    "NNV.",
    "NNVV.",
    "NVV.",
    "NVNV.",
    "NVSN.",
    "NVSNV.",
    "NVSNVN.",
    "SNV.",
    "SNVN.",
    "SNSV.",
    "SNN.",
    "SNNN.",
    "SNNNN.",
    "SSNN.",
    "SNSSN.",
    "SNSN.",
    "SNSNV.",
    "SSNNN.",
    "SSNSNSN.",
    "SSNSSN.",
    "SSSNN.",
    "SSSNSN.",
    "SSNV.",
    "SSNSV.",
];


VerbalPhrase=[
    "V.",
    "VN.",
    "VSN.",
    "VSSV.",
    "VNSSV.",
    "VSNN.",
    "VSNV.",
    "VNV.",
    "VNVN.",
    "VNVNN.",
    "VNVSN.",
    "VNVNNN.",
    "VNVNNNN.",
    "VNVNNNNN.",
    "VNN.",
    "VNNV.",
    "VNNVV.",
    "VNNN.",
    "VNNNV.",
    "VNNNSN.",
    "VNNNN.",
    "VNNNNN.",
    "VNNNNNN.",
    "VNNNNNV.",
    "VV.",
    "VVN.",
    "VVNN.",
    "VVNNN.",
    "VVNNNN.",
    "SV.",
    "SVNSVNN.",
    "SVSN.",
    "SVNSN.",
    "SVV.",
    "SVNV.",
    "SVNVN.",
    "SVSNV.",
    "SSSVV.",
    "SSVNV.",
    "SSVNVN.",
    "SSVSNV.",
    #added 
    "SVN.",
    "VNSN.", #added 
    
    ]
GrammarPhrase = VerbalPhrase+NominalPhrase;
PRONOUN_LIST = (
u"أنا" ,
u"نحن" , 
u"أنت" ,
u"أنتِ", 
u"أنتما",
u"أنتم" ,
u"أنتن" ,
u"هو" , 
u"هي" ,
u"هما" ,
u"هم" , 
u"هن",
)
CONDITION_FACTORS =(
u'لَمَّا',
u'مَهْمَا',
u'حَيْثُمَا',
u'أَيْنَمَا',
u'كَيْفَمَا',
u'إِذَا',
u'مَنْ',
u'إِنْ',
)




DIRECT_JAR_LIST=set([
u'من', 
u'عن', 
u'إلى',
u'على',
u'في',
u'رب',
u'منذ',
u'مذ',
u'عدا',
u'خلا',
u'حاشا',

u'عند',
u'أمام',
u'وراء',
u'خلف',
u'مع',
u'قبل',
u'بعد',
u'تحت',
u'أي',
u'كلّ',
u'بعض',
u'غير',
u'سوى',
u'ليل',
u'شمال',
u'جنوب',
u'يمين',
u'شرق',
u'غرب',
u'شطر',
u'أسفل',
u'أعلى',
u'جنب',
u'جانب',
u'تلقاء',
u'قدام',

u'أعلى',
u'شهر',
u'سنة',
u'غروب',
u'شروق',
u'دون',
u'شهور',

u'يوم',
u'حين',
u'ساعة',
u'زمان',
u'أزمان',
u'أيام',
u'أوقات',
u'وقت',
u'لحظة',

u'خلال',
u"بدون",

u"أثناء",
u"ذات",
u"ذو",
u"ذوو",
u"ذوات",
u"ذوي",
u"بن",
u"ابن",
u"بنت",
u'بين',
# صيغ واضحة الإضافة

u'أبو',
u'أخو',
u'بواسطة',

u'فَوْقَ',
u'مِنْ',

]);
DIRECT_JAZEM_LIST=set([
u'لم',
u'لما',
u'مهما',
u'حيثما',
u'أينما',
u'كيفما',

]);
DIRECT_VERB_NASEB_LIST=set([
u'أن',
u'كي',
u'لن',
u'حتى',
u'إذن',
#vocalized factor
u'أَنْ',
]);
DIRECT_VERB_RAFE3_LIST=set([

u'هل',
u'من',
u'ما',
u'متى',
u'أين',
u'ماذا',
u'كيف',
u'أيان',
u'يوم',
u'حين',
u'ساعة',
u'زمان',
u'أزمان',
u'أيام',
u'أوقات',
u'وقت',
u'لحظة',

]);

DIRECT_NOUN_NASEB_LIST=set([
u'أن',
u'إن',
u'فإن',
u'لأن',
u'كأن',
u'لكن',
u'ليت',
u'لعل',
#vocalized factor
u'أَنَّ',
u'فَإَنَّ',
u'أَنَّ',
u'إِنَّ',
u'فَإِنَّ',
u'لِأَنِّ',
u'كَأَنِّ',
u'لَكِنَّ',
u'لَيْتَ',
u'لَعَلَّ',
]);

DIRECT_VERBAL_FACTOR_LIST=set([
        u"قد",
        u"فقد",
        u"وقد",
        u"لن",
        u"لم",
        #vovalized factor
        u'أَنْ',
        u'إِنْ',
]);

DIRECT_NOMINAl_FACTOR_LIST=set([
        u"في",
        u"بأن",
        u"بين",
        u"ففي",
        u"وفي",
        u"عن",
        u"إلى",
        u"على",
        u"بعض",
        u"تجاه",
        u"تلقاء",
        u"جميع",
        u"حسب",
        u"سبحان",
        u"سوى",
        u"شبه",
        u"غير",
        u"كل",
        u"لعمر",
        u"مثل",
        u"مع",
        u"معاذ",
        u"نحو",
        u"خلف",
        u"أمام",
        u"فوق",
        u"تحت",
        u"يمين",
        u"شمال",
        u"دون",
        u"من",
        u"بدون",
        u"خلال",
        u"أثناء",
        #vovalized factor
        u'أَنِّ',
        u'إِنَّ',       
]);



DIRECT_RAFE3_LIST=set([
u'أنه',
u'أنك',
u'أنها',
u'بأنها',
u'بأنه',
u'وأنها',
u'فأنها',
u'فأنه',
u'كأنه',
u'كأنها',

# yahia alhadj
u'كان',
u'يكون',
u'كانت',
u'صار',
u'صارت',
u'يصير',
u'أمسى',
u'ليس',
u'ليست',
u'ظلّ',
u'ظلّت',
u'أضحى',
u'أضحت',
u'يضحي',
u'أصبح',
u'أصبحت',
u'يصبح',
u'بات',
u'باتت',
u'يبيت',
u'مازال',
u'لازال',
u'لايزال',
u'لازالت',
u'مايزال',
u'مازالت',
u'ماتزال',
u'مابرح',
u'مايبرح',
u'مابرحت',
u'ماانفك',
u'ماانفكّت',
u'ماينفك',
u'لاينفك',
u'مادام',
u'مادامت',
u'نعم',
u'بئس',
u'حبذا',

#إضافي
u'هل',
#u'من',
u'ما',
u'متى',
u'أين',
u'ماذا',
u'كيف',
u'أيان',
#اسماء الإشارة بعد فاء الإستئناف
u'فهذا',
u'فذلك',
u'فتلك',
u'فهؤلاء',
u'فأولئك',
u'فذلكم',
u'فهذه',
#ضمائر الرفع المنفصلة
u'هو',
u'هما',
u'هم',
u'هي',
u'هما',
u'هن',
u'أنت',
u'أنتما',
u'أنتم',
u'أنت',
u'أنتما',
u'أنتن',
u'أنا',
u'نحن',
u'إذ', 
]);

FACTORS_LIST={

u'حيثما': {u'حيثما': ['DVN', 'VJ'], u'حَيْثُمَا': ['CF', 'VJ']} ,
u'وأنها': {u'وأنها': ['NR', 'DNR']} ,
u'جنوب': {u'جنوب': ['DNJ', 'NJ'], u'جَنُوبَ': ['NJ']} ,
u'ومنذ': {u'وَمُنْذُ': ['NJ']} ,
u'فحتى': {u'فَحَتَّى': ['NJ']} ,
u'تحت': {u'تحت': ['DNJ', 'NJ', 'DNF'], u'تَحْتَ': ['NJ']} ,
u'لعل': {u'لعل': ['DNN'], u'لَعَلَّ': ['NN', 'DNN']} ,
u'بنت': {u'بنت': ['DNJ', 'NJ']} ,
u'لازالت': {u'لازالت': ['NR', 'DNR', 'KS']} ,
u'زمان': {u'زمان': ['DNJ', 'NJ', 'VR', 'DVR'], u'زَمانُ': ['NJ', 'VR']} ,
u'إذ': {u'إذ': ['NR', 'DNR']} ,
u'غير': {u'غير': ['DNJ', 'NJ', 'DNF'], u'غَيْرَ': ['NJ']} ,
u'حاشا': {u'حاشا': ['DNJ', 'NJ'], u'حَاشَا': ['NJ']} ,
u'ليس': {u'ليس': ['NR', 'DNR', 'KS']} ,
u'شرق': {u'شرق': ['DNJ', 'NJ'], u'شَرِقَ': ['NJ']} ,
u'مابرحت': {u'مابرحت': ['NR', 'DNR', 'KS']} ,
u'لكن': {u'لكن': ['DNN'], u'لَكِنَّ': ['NN', 'DNN']} ,
u'سبحان': {u'سبحان': ['DNF']} ,
u'مابرح': {u'مابرح': ['NR', 'DNR', 'KS']} ,
u'كأنها': {u'كأنها': ['NR', 'DNR']} ,
u'يضحي': {u'يضحي': ['NR', 'DNR', 'KS']} ,
u'غرب': {u'غرب': ['DNJ', 'NJ'], u'غَرِبَ': ['NJ']} ,
u'فهذه': {u'فهذه': ['NR', 'DNR']} ,
u'إذا': {u'إِذَا': ['CF']} ,
u'لازال': {u'لازال': ['NR', 'DNR', 'KS']} ,
u'بن': {u'بن': ['DNJ', 'NJ'], u'بْنُ': ['NJ']} ,
u'قبل': {u'قبل': ['DNJ', 'NJ'], u'قَبْلَ': ['NJ']} ,
u'وفي': {u'وفي': ['DNF'], u'وَفِي': ['NJ']} ,
u'ماتزال': {u'ماتزال': ['NR', 'DNR', 'KS']} ,
u'مايبرح': {u'مايبرح': ['NR', 'DNR', 'KS']} ,
u'إلى': {u'إلى': ['DNJ', 'NJ', 'DNF'], u'إِلَى': ['NJ']} ,
u'فذلك': {u'فذلك': ['NR', 'DNR']} ,
u'هن': {u'هن': ['NR', 'DNR']} ,
u'هم': {u'هم': ['NR', 'DNR']} ,
u'هل': {u'هل': ['NR', 'VR', 'DVR', 'DNR'], u'هَلْ': ['VR']} ,
u'وإلى': {u'وَإِلَى': ['NJ']} ,
u'شهر': {u'شهر': ['DNJ', 'NJ'], u'شَهَرَ': ['NJ']} ,
u'فهذا': {u'فهذا': ['NR', 'DNR']} ,
u'شبه': {u'شبه': ['DNF']} ,
u'لاينفك': {u'لاينفك': ['NR', 'DNR', 'KS']} ,
u'هي': {u'هي': ['NR', 'DNR']} ,
u'هو': {u'هو': ['NR', 'DNR']} ,
u'فوق': {u'فوق': ['DNF'], u'فَوْقَ': ['DNJ', 'NJ']} ,
u'وقد': {u'وقد': ['VF', 'DVF']} ,
u'مايزال': {u'مايزال': ['NR', 'DNR', 'KS']} ,
u'صارت': {u'صارت': ['NR', 'DNR', 'KS']} ,
u'معاذ': {u'معاذ': ['DNF']} ,
u'وقت': {u'وقت': ['DNJ', 'NJ', 'VR', 'DVR'], u'وَقَّتَ': ['VR'], u'وَقْتَ': ['NJ']} ,
u'مازال': {u'مازال': ['NR', 'DNR', 'KS']} ,
u'إن': {u'إن': ['DNN', 'VJ'], u'إِنَّ': ['NN', 'DNN', 'DNF'], u'إِنْ': ['CF', 'VJ', 'VF', 'DVF']} ,
u'فإلى': {u'فَإِلَى': ['NJ']} ,
u'تصبح': {u'تصبح': ['KS']} ,
u'غروب': {u'غروب': ['DNJ', 'NJ'], u'غُرُوبُ': ['NJ']} ,
u'نحو': {u'نحو': ['DNF']} ,
u'حسب': {u'حسب': ['DNF']} ,
u'نحن': {u'نحن': ['NR', 'DNR']} ,
u'فتلك': {u'فتلك': ['NR', 'DNR']} ,
u'لحظة': {u'لحظة': ['DNJ', 'NJ', 'VR', 'DVR'], u'لَحْظَةُ': ['NJ', 'VR']} ,
u'قد': {u'قد': ['VF', 'DVF']} ,
u'شمال': {u'شمال': ['DNJ', 'NJ', 'DNF'], u'شَمَالَ': ['NJ']} ,
u'فمنذ': {u'فَمُنْذُ': ['NJ']} ,
u'باتت': {u'باتت': ['NR', 'DNR', 'KS']} ,
u'ليست': {u'ليست': ['NR', 'DNR', 'KS']} ,
u'أعلى': {u'أعلى': ['DNJ', 'NJ'], u'أَعَلَى': ['NJ']} ,
u'يصبح': {u'يصبح': ['NR', 'DNR', 'KS']} ,
u'يمين': {u'يمين': ['DNJ', 'NJ', 'DNF'], u'يَمِينَ': ['NJ']} ,
u'فمن': {u'فَمِنْ': ['NJ']} ,
u'فهؤلاء': {u'فهؤلاء': ['NR', 'DNR']} ,
u'فعما': {u'فَعَمَّا': ['NJ']} ,
u'أنت': {u'أنت': ['NR', 'DNR']} ,
u'بدون': {u'بدون': ['DNJ', 'NJ', 'DNF'], u'بِدونِ': ['NJ']} ,
u'وعن': {u'وَعَنْ': ['NJ']} ,
u'منذ': {u'منذ': ['DNJ', 'NJ'], u'مُنْذُ': ['NJ']} ,
u'أنا': {u'أنا': ['NR', 'DNR']} ,
u'ما': {u'ما': ['NR', 'VR', 'DVR', 'DNR'], u'مَا': ['VR']} ,
u'مثل': {u'مثل': ['DNF']} ,
u'فعلى': {u'فَعَلَى': ['NJ']} ,
u'مع': {u'مع': ['DNJ', 'NJ', 'DNF'], u'مَعَ': ['NJ']} ,
u'ماانفك': {u'ماانفك': ['NR', 'DNR', 'KS']} ,
u'لعمر': {u'لعمر': ['DNF']} ,
u'مذ': {u'مذ': ['DNJ', 'NJ'], u'مُذْ': ['NJ']} ,
u'شهور': {u'شهور': ['DNJ', 'NJ']} ,
u'ذوي': {u'ذوي': ['DNJ', 'NJ'], u'ذَوِيَ': ['NJ']} ,
u'كيف': {u'كيف': ['NR', 'VR', 'DVR', 'DNR'], u'كَيْفَ': ['VR']} ,
u'بأنه': {u'بأنه': ['NR', 'DNR']} ,
u'ولا': {u'ولا': ['VR', 'VJ'], u'وَلَا': ['VR', 'VJ']} ,
u'أنه': {u'أنه': ['NR', 'DNR']} ,
u'كانت': {u'كانت': ['NR', 'DNR', 'KS']} ,
u'من': {u'من': ['DNJ', 'NJ', 'DNF', 'VR', 'DVR'], u'مَنْ': ['CF', 'VR'], u'مِنْ': ['DNJ', 'NJ']} ,
u'أنك': {u'أنك': ['NR', 'DNR']} ,
u'حتى': {u'حتى': ['DVN', 'VN'], u'حَتَّى': ['NJ', 'VN']} ,
u'ورب': {u'وَرُبَّ': ['NJ']} ,
u'أبا': {u'أبا': ['NJ']} ,
u'حبذا': {u'حبذا': ['NR', 'DNR']} ,
u'تمسي': {u'تمسي': ['KS']} ,
u'ذي': {u'ذي': ['NJ'], u'ذِي': ['NJ']} ,
u'ذو': {u'ذو': ['DNJ', 'NJ'], u'ذُو': ['NJ']} ,
u'أي': {u'أي': ['DNJ', 'NJ'], u'أَيُّ': ['NJ']} ,
u'بأنها': {u'بأنها': ['NR', 'DNR']} ,
u'مادام': {u'مادام': ['NR', 'DNR', 'KS']} ,
u'تضحي': {u'تضحي': ['KS']} ,
u'عدا': {u'عدا': ['DNJ', 'NJ'], u'عَدَا': ['NJ']} ,
u'بأن': {u'بأن': ['DNF']} ,
u'عند': {u'عند': ['DNJ', 'NJ'], u'عِنْدَ': ['NJ']} ,
u'أن': {u'أن': ['DNN', 'DVN', 'VN'], u'أَنَّ': ['NN', 'DNN'], u'أَنِّ': ['DNF'], u'أَنْ': ['DVN', 'VF', 'DVF', 'VN']} ,
u'بواسطة': {u'بواسطة': ['DNJ', 'NJ'], u'بِوَاسِطَةِ': ['NJ']} ,
u'أمام': {u'أمام': ['DNJ', 'NJ', 'DNF'], u'أَمَامَ': ['NJ']} ,
u'فأولئك': {u'فأولئك': ['NR', 'DNR']} ,
u'بات': {u'بات': ['NR', 'DNR', 'KS']} ,
u'هما': {u'هما': ['NR', 'DNR']} ,
u'أنها': {u'أنها': ['NR', 'DNR']} ,
u'وأما': {u'وأما': ['NR'], u'وَأَمَّا': ['NR']} ,
u'على': {u'على': ['DNJ', 'NJ', 'DNF'], u'عَلَى': ['NJ']} ,
u'إذن': {u'إذن': ['DVN', 'VN'], u'إِذَنْ': ['VN']} ,
u'عن': {u'عن': ['DNJ', 'NJ', 'DNF'], u'عَنْ': ['NJ']} ,
u'أخو': {u'أخو': ['DNJ', 'NJ'], u'أَخُو': ['NJ']} ,
u'يكون': {u'يكون': ['NR', 'DNR', 'KS']} ,
u'مازالت': {u'مازالت': ['NR', 'DNR', 'KS']} ,
u'حين': {u'حين': ['DNJ', 'NJ', 'VR', 'DVR'], u'حِينَ': ['NJ', 'VR']} ,
u'أوقات': {u'أوقات': ['DNJ', 'NJ', 'VR', 'DVR'], u'أَوََقَاتَ': ['NJ', 'VR']} ,
u'ومذ': {u'وَمُذْ': ['NJ']} ,
u'فلا': {u'فلا': ['VR', 'VJ'], u'فَلَا': ['VR', 'VJ']} ,
u'أيان': {u'أيان': ['NR', 'VR', 'DVR', 'DNR'], u'ّأَيَّانَ': ['VR']} ,
u'أيام': {u'أيام': ['DNJ', 'NJ', 'VR', 'DVR'], u'أيَّامُ': ['VR']} ,
u'أين': {u'أين': ['NR', 'VR', 'DVR', 'DNR'], u'أَيْنَ': ['VR']} ,
u'عما': {u'عَمَّا': ['NJ']} ,
u'بعد': {u'بعد': ['DNJ', 'NJ'], u'بَعْدَ': ['NJ']} ,
u'فأنه': {u'فأنه': ['NR', 'DNR']} ,
u'بعض': {u'بعض': ['DNJ', 'NJ', 'DNF'], u'بَعْضُ': ['NJ']} ,
u'أينما': {u'أينما': ['DVN', 'VJ'], u'أَيْنَمَا': ['CF', 'VJ']} ,
u'أبي': {u'أبي': ['NJ']} ,
u'أضحت': {u'أضحت': ['NR', 'DNR', 'KS']} ,
u'كي': {u'كي': ['DVN', 'VN'], u'كَيْ': ['VN']} ,
u'أمست': {u'أمست': ['KS']} ,
u'مادامت': {u'مادامت': ['NR', 'DNR', 'KS']} ,
u'نعم': {u'نعم': ['NR', 'DNR']} ,
u'فإن': {u'فإن': ['DNN'], u'فَإَنَّ': ['NN', 'DNN'], u'فَإِنَّ': ['NN', 'DNN']} ,
u'تلقاء': {u'تلقاء': ['DNJ', 'NJ', 'DNF'], u'تِلْقَاءَ': ['NJ']} ,
u'خلا': {u'خلا': ['DNJ', 'NJ'], u'خَلَا': ['NJ']} ,
u'كان': {u'كان': ['NR', 'DNR', 'KS']} ,
u'وعما': {u'وَعَمَّا': ['NJ']} ,
u'ومن': {u'وَمِنْ': ['NJ']} ,
u'بين': {u'بين': ['DNJ', 'NJ', 'DNF'], u'بَيْنَ': ['NJ']} ,
u'قدام': {u'قدام': ['DNJ', 'NJ'], u'قدامُ': ['NJ']} ,
u'لايزال': {u'لايزال': ['NR', 'DNR', 'KS']} ,
u'صار': {u'صار': ['NR', 'DNR', 'KS']} ,
u'ففي': {u'ففي': ['DNF'], u'فَفِي': ['NJ']} ,
u'أضحى': {u'أضحى': ['NR', 'DNR', 'KS']} ,
u'وأبو': {u'وأبو': ['NJ']} ,
u'ليت': {u'ليت': ['DNN'], u'لَيْتَ': ['NN', 'DNN']} ,
u'متى': {u'متى': ['NR', 'VR', 'DVR', 'DNR'], u'مَتَى': ['VR']} ,
u'خلال': {u'خلال': ['DNJ', 'NJ', 'DNF'], u'خِلَالَ': ['NJ']} ,
u'كأنه': {u'كأنه': ['NR', 'DNR']} ,
u'أزمان': {u'أزمان': ['DNJ', 'NJ', 'VR', 'DVR'], u'أَزَمانُ': ['VR']} ,
u'ثنا': {u'ثنا': ['NR']} ,
u'كلّ': {u'كلّ': ['DNJ', 'NJ']} ,
u'رب': {u'رب': ['DNJ', 'NJ'], u'رُبَّ': ['NJ']} ,
u'ماذا': {u'ماذا': ['NR', 'VR', 'DVR', 'DNR'], u'مَاذَا': ['VR']} ,
u'يوم': {u'يوم': ['DNJ', 'NJ', 'VR', 'DVR'], u'يَوْمَ': ['NJ'], u'يَوْمُ': ['VR']} ,
u'ماينفك': {u'ماينفك': ['NR', 'DNR', 'KS']} ,
u'ذوو': {u'ذوو': ['DNJ', 'NJ'], u'ذُوُو': ['NJ']} ,
u'أبو': {u'أبو': ['DNJ', 'NJ'], u'أَبُو': ['NJ']} ,
u'دون': {u'دون': ['DNJ', 'NJ', 'DNF'], u'دُونَ': ['NJ']} ,
u'لم': {u'لم': ['DVN', 'VJ', 'VF', 'DVF'], u'لَمْ': ['VJ']} ,
u'جنب': {u'جنب': ['DNJ', 'NJ'], u'جَنَبَ': ['NJ']} ,
u'بلا': {u'بلا': ['NJ'], u'بِلَا': ['NJ']} ,
u'وحتى': {u'وَحَتَّى': ['NJ']} ,
u'يصير': {u'يصير': ['NR', 'DNR', 'KS']} ,
u'ظلّ': {u'ظلّ': ['NR', 'DNR', 'KS']} ,
u'وأبي': {u'وأبي': ['NJ']} ,
u'جانب': {u'جانب': ['DNJ', 'NJ'], u'جَانِبَ': ['NJ']} ,
u'ساعة': {u'ساعة': ['DNJ', 'NJ', 'VR', 'DVR'], u'سَاعَةُ': ['NJ', 'VR']} ,
u'جميع': {u'جميع': ['DNF']} ,
u'يمسي': {u'يمسي': ['KS']} ,
u'شروق': {u'شروق': ['DNJ', 'NJ'], u'شُرُوقُ': ['NJ']} ,
u'أسفل': {u'أسفل': ['DNJ', 'NJ'], u'أَسْفَلَ': ['NJ']} ,
u'فقد': {u'فقد': ['VF', 'DVF']} ,
u'وراء': {u'وراء': ['DNJ', 'NJ'], u'وَراءَ': ['NJ']} ,
u'مهما': {u'مهما': ['DVN', 'VJ'], u'مَهْمَا': ['CF', 'VJ']} ,
u'كيفما': {u'كيفما': ['DVN', 'VJ'], u'كَيْفَمَا': ['CF', 'VJ']} ,
u'سنة': {u'سنة': ['DNJ', 'NJ'], u'سَنَةُ': ['NJ']} ,
u'سوى': {u'سوى': ['DNJ', 'NJ', 'DNF'], u'سِوَى': ['NJ']} ,
u'ماانفكّت': {u'ماانفكّت': ['NR', 'DNR', 'KS']} ,
u'كأن': {u'كأن': ['DNN'], u'كَأَنِّ': ['NN', 'DNN']} ,
u'فذلكم': {u'فذلكم': ['NR', 'DNR']} ,
u'فرب': {u'فَرُبَّ': ['NJ']} ,
u'وأبا': {u'وأبا': ['NJ']} ,
u'لن': {u'لن': ['DVN', 'VF', 'DVF', 'VN'], u'لَنْ': ['VN']} ,
u'لأن': {u'لأن': ['DNN'], u'لِأَنَّ': ['NN'], u'لِأَنِّ': ['DNN']} ,
u'في': {u'في': ['DNJ', 'NJ', 'DNF'], u'فِي': ['NJ']} ,
u'ذات': {u'ذات': ['DNJ', 'NJ'], u'ذَاتُ': ['NJ']} ,
u'لئلا': {u'لئلا': ['VN'], u'لِئَلَا': ['VN']} ,
u'خلف': {u'خلف': ['DNJ', 'NJ', 'DNF'], u'خَلْفَ': ['NJ']} ,
u'ظلّت': {u'ظلّت': ['NR', 'DNR', 'KS']} ,
u'يبيت': {u'يبيت': ['NR', 'DNR', 'KS']} ,
u'فمذ': {u'فَمُذْ': ['NJ']} ,
u'كل': {u'كل': ['DNF']} ,
u'أصبح': {u'أصبح': ['NR', 'DNR', 'KS']} ,
u'أما': {u'أَمّا': ['NR']} ,
u'ذوات': {u'ذوات': ['DNJ', 'NJ'], u'ذُوَاتُ': ['NJ']} ,
u'أصبحت': {u'أصبحت': ['NR', 'DNR', 'KS']} ,
u'أثناء': {u'أثناء': ['DNJ', 'NJ', 'DNF'], u'أَثَناءَ': ['NJ']} ,
u'أمسى': {u'أمسى': ['NR', 'DNR', 'KS']} ,
u'لا': {u'لا': ['VR', 'VJ'], u'لَا': ['VR', 'VJ']} ,
u'فعن': {u'فَعَنْ': ['NJ']} ,
u'ابن': {u'ابن': ['DNJ', 'NJ'], u'اِبْنُ': ['NJ']} ,
u'فأنها': {u'فأنها': ['NR', 'DNR']} ,
u'تجاه': {u'تجاه': ['DNF']} ,
u'أنتما': {u'أنتما': ['NR', 'DNR']} ,
u'شطر': {u'شطر': ['DNJ', 'NJ'], u'شَطَرَ': ['NJ']} ,
u'أنتم': {u'أنتم': ['NR', 'DNR']} ,
u'تبيت': {u'تبيت': ['KS']} ,
u'أنتن': {u'أنتن': ['NR', 'DNR']} ,
u'وعلى': {u'وَعَلَى': ['NJ']} ,
u'لما': {u'لما': ['DVN', 'VJ'], u'لَمَّا': ['CF', 'VJ']} ,
u'بئس': {u'بئس': ['NR', 'DNR']} ,
u'ليل': {u'ليل': ['DNJ', 'NJ'], u'لَيْلَ': ['NJ']} ,
}
TABLE_PRONOUN = {
vconst.PronounAna : [u"أَنَا", u"نِي"],#u"أنا",
vconst.PronounNahnu : [u"نَحْنُ", u"نَا"], 
vconst.PronounAnta : [u"أَنْتَ", u"كَ" ], #u"أنت",
vconst.PronounAnti :  [u"أَنْتِ",  u"كِ"], # u"أنتِ",
vconst.PronounAntuma : [u"اََنْتُمَا", u"كُمَا"], #u"أنتما",
vconst.PronounAntuma_f :[ u"أَنْتُمَا", u"كُمَا"], #  u"أنتما مؤ",
vconst.PronounAntum : [u"ْأَنْتُم",   u"كُمْ"], #u"أنتم", 
vconst.PronounAntunna :[ u"أَنْتُنَّ",  u"كُنَّ"], #u"أنتن", 
vconst.PronounHuwa : [u"هُوَ",   u"هُ", u"الَّذِي",  u'الَّذِي', u'مَنْ', u'هَذَا',u'ذِهِ',  u'ذَلِكَ', u'ذَلِكُمْ', u'ذَلَكُمَا', u'ذَلِكُنَّ', u'ذَانِكَ', u'ذَا', u'ذَاكَ', ], #u"هو",
vconst.PronounHya : [u"َهِي",     u"هَا" , u'الَّتِي',  u'مَنْ', u'هَذِهِ', u'هَذِي', u'هَاتِهِ', u'هَاتِي', u'تِلْكَ', u'تِلْكُمْ', u'تِلْكُمَا'
],  #u"هي",  
vconst.PronounHuma :[ u"هُمَا",   u"هُمَا" , u'الْلَذَانِ', u'الْلَذَيْنِ', u'مَنْ', u'مَا', u'هَذَانِ', u'هَذَيْنِ', u'ذَانِ'],  #u"هما",
vconst.PronounHuma_f :[ u"هُمَا", u"هُمَا" , u'الْلَتَانِ', u'الْلَتَيَّا', u'الْلَتَيْنِ', u'مَنْ', u'مَا', u'هَاتَانِ', u'هَاتَيْنِ', u'تَانِ', u'تَانِكَ'],#u"هما مؤ",
vconst.PronounHum : [u"ْهُم",      u"هُمْ" , u'الَّذِينَ', u'الْأَلَاءُ', u'الْأُلَى', u'مَنْ', u'مَا', u'هَؤُلَاءِ', u'أُولَئِكَ', u'أُولَئِكُمْ', u'أُولَاءِ', u'أُولَالِكَ'], #u"هم",
vconst.PronounHunna :[ u"َّهُن",    u"هُنَّ", u'الْلَائِي', u'الْلَاتِي', u'الْلَوَاتِي',  u'مَنْ', u'مَا' ], #u"هن",
}










#constants of syntaxic relations
# RAF3  رفعrelation starts with 10
VerbSubjectRelation = 10; #علاقة فعل وفاعل
SubjectVerbRelation = 11; # علاقة فاعل وفعل
VerbPassiveSubjectRelation = 12 # علاقة فعل ونائب فاعل

PrimateRelation = 13; # علاقة مبتدأ، ببداية الجملة
Rafe3Marfou3Relation = 14; # علاقة رافع  ومرفوع
KanaRafe3Marfou3Relation = 15; # علاقة رافع  ومرفوع
InnaRafe3Marfou3Relation = 16 #علاقة خبر إنّ مرفوع
KanaNasebMansoubRelation = 17 #   خبر كان منصوب
PrimateMansoubPredicateRelation  = 18   #مبتدأ منصوب وخبر مرفوع


# Nasb نصب relation starts with 20
VerbObjectRelation  = 20; # علاقة فعل ومفعول به
InnaNasebMansoubRelation = 21; # علاقة ناصب ومنصوب
NasebMansoubRelation =22; # علاقة ناصب ومنصوب
PrimatePredicateMansoubRelation = 23  #مبتدأ مرفوع وخبر منصوب

# Jar/ Jazm جر relation starts with 30
AdditionRelation = 30; #علاقة مضاف مضاف إليه
JarMajrourRelation = 31; # علاقة جار ومجرور
JazemMajzoumRelation = 32; # علاقة جازم ومجزوم

# Related (تبعية) relation starts with 40
DescribedAdjectiveRelation = 40; # علاقة منعوت ونعت
JonctionRelation = 41 ; # علاقة المعطوف والمعطوف عليه
SubstitutionMansoubRelation = 42 # بدل منه وبدل منصوب 
SubstitutionMajrourRelation = 43 #بدل منه وبدل مجرور 
SubstitutionMarfou3Relation = 44 #بدل منه وبدل مرفوع
ConfirmationRelation =45 #"24 توكيد"

#Jobless relations علاقة عاطلة starts with 50
JoblessFactorVerbRelation = 50 # أدوات عاطلة للفعل مثل قد

# Divers relations متنوعة starts with 60
VerbParticulRelation = 60; # علاقة فعل متعدي بحرف
PrimatePredicateRelation  = 61; # علاقة مبتدأ وخبر
TanwinRelation = 62; #علاقة تنوين، للكلمة النكرة بفاصل بعدها
ConditionVerbRelation = 63 #علاقة اسم شرط مع فعل




RELATIONS_TAGS={
#Raf
VerbSubjectRelation: [u"رفع",u""], 
SubjectVerbRelation: [u"رفع",u""], 
VerbPassiveSubjectRelation: [u"رفع",u""], 

PrimateRelation: [u"رفع",u""], 
Rafe3Marfou3Relation: [u"رفع",u""], 
KanaRafe3Marfou3Relation: [u"رفع",u""], 
InnaRafe3Marfou3Relation: [u"رفع",u""], 
KanaNasebMansoubRelation: [u"رفع",u""], 
PrimateMansoubPredicateRelation : [u"رفع",u""], 

# Nasb
VerbObjectRelation: [u"نصب",u""], 
InnaNasebMansoubRelation: [u"نصب",u""], 
NasebMansoubRelation: [u"نصب",u""], 
PrimatePredicateMansoubRelation : [u"نصب",u""],

# jAR jAZM
AdditionRelation: [u"جر",u""], 
JarMajrourRelation: [u"جر",u""], 
JazemMajzoumRelation: [u"جزم",u""], 

# related
DescribedAdjectiveRelation: [u"تابع",u""], 
JonctionRelation: [u"عطف",u""], 
SubstitutionMansoubRelation: [u'تابع', u"بدل",u"منصوب"], 
SubstitutionMajrourRelation: [u'تابع', u"بدل",u"مجرور"], 
SubstitutionMarfou3Relation: [u"تابع",u"بدل", u"مرفوع"], 
ConfirmationRelation: [u"تابع",u""], 

#Jobless
JoblessFactorVerbRelation: [u"عاطل",u""], 

#
VerbParticulRelation: [u"",u""], 
PrimatePredicateRelation: [u"",u""], 
TanwinRelation: [u"",u""], 
ConditionVerbRelation: [u"",u""], 
  
}



#used to display text on relations
DISPLAY_RELATION={
# RAF3  رفعrelation starts with 10
VerbSubjectRelation : u" 10علاقة فعل وفاعل", 
SubjectVerbRelation : u" 11 علاقة فاعل وفعل", 
VerbPassiveSubjectRelation : u" 12 # علاقة فعل ونائب فاعل", 

PrimateRelation : u" 13 علاقة مبتدأ، ببداية الجملة", 
Rafe3Marfou3Relation : u" 14 علاقة رافع  ومرفوع", 
KanaRafe3Marfou3Relation : u" 15 علاقة رافع  ومرفوع", 
InnaRafe3Marfou3Relation : u" 16 #علاقة خبر إنّ مرفوع", 
KanaNasebMansoubRelation : u" 17 #   خبر كان منصوب", 
PrimateMansoubPredicateRelation :u"18   #مبتدأ منصوب  وخبر مرفوع",

# Nasb نصب relation starts with 20 
VerbObjectRelation  : u" 20 علاقة فعل ومفعول به", 
InnaNasebMansoubRelation : u" 21 علاقة ناصب ومنصوب", 
NasebMansoubRelation : u" 22 علاقة ناصب ومنصوب", 
PrimatePredicateMansoubRelation : u"23  #مبتدأ مرفوع وخبر منصوب", 

# Jar/ Jazm جر relation starts with 30
AdditionRelation : u" 30علاقة مضاف مضاف إليه", 
JarMajrourRelation : u" 31 علاقة جار ومجرور", 
JazemMajzoumRelation : u" 32 علاقة جازم ومجزوم", 

# Related (تبعية) relation starts with 40
DescribedAdjectiveRelation : u" 40 علاقة منعوت ونعت", 
JonctionRelation : u" 41  علاقة المعطوف والمعطوف عليه", 
SubstitutionMansoubRelation : u" 42 بدل منه وبدل منصوب", 
SubstitutionMajrourRelation : u" 43 بدل منه وبدل مجرور", 
SubstitutionMarfou3Relation : u" 44 بدل منه وبدل مرفوع", 
ConfirmationRelation : u"45 توكيد",

#Jobless relations علاقة عاطلة starts with 50
JoblessFactorVerbRelation : u" 50 # أدوات عاطلة للفعل مثل قد", 

# Divers relations متنوعة starts with 60
VerbParticulRelation : u" 60 علاقة فعل متعدي بحرف", 
PrimatePredicateRelation  : u" 61 علاقة مبتدأ وخبر", 
TanwinRelation : u" 62علاقة تنوين، للكلمة النكرة بفاصل بعدها", 
ConditionVerbRelation : u" 63 #علاقة اسم شرط مع فعل", 


}









        
conditions = [
{ "rule":VerbObjectRelation,
     "previous":[ ("is_verb",True), ("get_original",u"قالَ"), ],
    "current":[("is_pounct",True), ]
},
{ "rule":JonctionRelation,
     "previous":[ ("is_noun",True), ("get_original",u"قالَ"), ("is_majrour",True), ],
    "current":[("is_noun",True), ("has_procletic",True),("has_jonction",True), ("has_jar",False), ("is_majrour",True),]
},

{ "rule":JonctionRelation,
     "previous":[ ("is_noun",True), ("get_original",u"قالَ"), ("is_majrour",True), ],
    "current":[("is_noun",True), ("has_procletic",True),("has_jonction",True), ("has_jar",False), ("is_majrour",True),]
},
{ "rule":JonctionRelation,
     "previous":[ ("is_noun",True), ("get_original",u"قالَ"), ("is_mansoub",True), ],
    "current":[("is_noun",True), ("has_procletic",True),("has_jonction",True), ("has_jar",False), ("is_mansoub",True),]
},

{ "rule":JonctionRelation,
     "previous":[ ("is_noun",True), ("get_original",u"قالَ"), ("is_marfou3",True), ],
    "current":[("is_noun",True), ("has_procletic",True),("has_jonction",True), ("has_jar",False), ("is_marfou3",True),]
},

{ "rule":TanwinRelation,
     "previous":[ ("is_tanwin",True), ],
     "current":[ ("is_break",True),]
},
{ "rule":JarMajrourRelation,
     "previous":[ ("is_stopword",True), ("is_jar",True),],
     "current":[ ("is_noun",True), ("is_break",False), ("is_majrour",True),]
},
{ "rule":InnaNasebMansoubRelation,
     "previous":[ ("is_stopword",True), ("is_naseb",True),],
     "current":[ ("is_noun",True), ("is_break",False), ("is_mansoub",True),]
},
            # خبر إنّ لمبتدإ ضمير متصل
{ "rule":InnaRafe3Marfou3Relation,
     "previous":[ ("is_stopword",True), ("is_naseb",True), ("has_encletic",True)],
     "current":[ ("is_noun",True), ("is_break",False), ("is_marfou3",True),]
},
{ "rule":PrimateRelation,
     "previous":[ ("is_stopword",True), ("is_initial",True),],
     "current":[ ("is_noun",True), ("is_break",False), ("is_marfou3",True),]
},
        # اسم كان وأخواتها
{ "rule":KanaRafe3Marfou3Relation,
     "previous":[ ("is_stopword",True), ("is_kana_rafe3",True),],
     "current":[ ("is_noun",True), ("is_break",False), ("is_marfou3",True),]
},
        # رافع ومرفوع   
{ "rule":Rafe3Marfou3Relation,
     "previous":[ ("is_stopword",True), ("is_rafe3",True),],
     "current":[ ("is_noun",True), ("is_break",False), ("is_marfou3",True),]
},
        #جازم ومجزوم
{ "rule":JazemMajzoumRelation,
  "previous":[("is_stopword",True), ("is_verbal_factor",True), ("is_jazem",True),],
  "current":[("is_verb",True), ("is_break",False), ("is_majzoum",True), ("is_present",True)]
},

        ##حالة خاصة لا الناهية تنهى عن الأفعال
                # المسندة للضمير المخاطب فقط
{ "rule":JazemMajzoumRelation,
  "previous":[("is_stopword",True), ("is_verbal_factor",True), ("is_jazem",True), ("get_unvoriginal",u'لا')],
  "current":[("is_verb",True), ("is_break",False), ("is_majzoum",True), ("is_present",True),
("has_imperative_pronoun", True)]
},
    # ناصب ومنصوب الفعل
{ "rule":NasebMansoubRelation,
  "previous":[("is_stopword",True), ("is_verbal_factor",True), ("is_verb_naseb",True),],
  "current":[("is_verb",True), ("is_break",False), ("is_mansoub",True), ("is_present",True)]
},


    # رافع ومرفوع الفعل
{ "rule":Rafe3Marfou3Relation,
  "previous":[("is_stopword",True), ("is_verbal_factor",True), ("is_verb_rafe3",True),],
  "current":[("is_verb",True), ("is_break",False), ("is_present",True), ("is_marfou3",True)]
},


    # رافع ومرفوع الفعل
                #حالة لا النافية 
                # المسندة لغير الضمائر المخاطبة
{ "rule":Rafe3Marfou3Relation,
  "previous":[("is_stopword",True), ("is_verbal_factor",True), ("is_verb_rafe3",True), ("get_unvoriginal",u'لا')],
  "current":[("is_verb",True), ("is_break",False), ("is_present",True), ("is_marfou3",True),("has_imperative_pronoun", False)]
},

        # الجارية فعل والسابق مبتدأ
{ "rule":Rafe3Marfou3Relation,
  "previous":[("is_noun",True), ("is_defined",True),],
  "current":[("is_verb",True), ("is_break",False), ("is_present",True), ("is_marfou3",True),]
},
# المضاف والمضاف إليه
        # إضافة لفظية
        # مثل لاعبو الفريق
{ "rule":JarMajrourRelation,
  "previous":[("is_added",True), ],
  "current":[("is_noun",True), ("is_break",False), ("is_majrour",True), ]
},
{ "rule":JarMajrourRelation,
  "previous":[("is_noun",True), ("is_defined",False), ("is_added",False), ("is_tanwin",False),],
  "current":[("is_noun",True), ("is_break",False), ("is_majrour",True), ]
},


{ "rule":JarMajrourRelation,
  "previous":[("is_noun",True), ("is_defined",False), ("is_added",False), ("is_tanwin",False),],
  "current":[("is_addition",True), ("is_break",False), ("is_majrour",True), ]
},

      # الفعل والفاعل 
{ "rule":VerbSubjectRelation,
  "previous":[("is_verb",True), ("is3rdperson",True), ("is_passive",False), ],
  "current":[("is_noun",True), ("is_break",False), ("is_marfou3",True), ]
},
# الفعل و نائب الفاعل
{ "rule":VerbPassiveSubjectRelation,
  "previous":[("is_verb",True), ("is3rdperson",True), ("is_passive",True), ],
  "current":[("is_noun",True), ("is_break",False), ("is_marfou3",True), ]
},

# الفعل والمفعول به
{ "rule":VerbObjectRelation,
  "previous":[("is_verb",True), ("is_passive",False), ("is_transitive", True), ("has_encletic", False) ],
  "current":[("is_noun",True), ("is_break",False), ("is_mansoub",True), ]
},
]
           
