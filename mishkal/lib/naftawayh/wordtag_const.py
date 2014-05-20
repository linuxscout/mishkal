#!/usr/bin/python
# -*- coding=utf-8 -*-
import re
import pyarabic.araby as araby
"""
Arabic Word Type Guessing constants:

"""
FixedNouns=(
u'الله',
u'لله',
u'بالله',
u'والله',
u'موسى',
u'مريم',
u'يونس',
u'يوسف',
u'يثرب',
u'يوسف',
u'يوسف',
)

tab_noun_context=(
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
	   # لا تكون محددة لأنها قد تسبق الاسم حرف جر، أو تسبق الفعل للاستفهام
		# u"من",
        u"بدون",
        u"خلال",
        u"أثناء",
        )
tab_verb_context=(
        u"قد",
        u"فقد",
        u"وقد",
        u"لن",
        u"لم",
        )

#------------------------
# Prefixes used as forbiden bigrams
#------------------------
prefixes_letters=( araby.TEH , araby.MEEM , araby.LAM, araby.WAW , araby.BEH, araby.KAF, araby.FEH, araby.HAMZA, araby.YEH, araby.NOON )
prefixes_forbiden={
araby.ALEF_HAMZA_ABOVE:( araby.ALEF_HAMZA_ABOVE, araby.ZAH, araby.AIN, araby.GHAIN), 
araby.BEH:( araby.BEH, araby.FEH, araby.MEEM ), 
araby.TEH :( araby.THEH, araby.DAL, araby.THAL, araby.ZAIN, araby.SHEEN, araby.SAD, araby.DAD, araby.TAH, araby.ZAH),
araby.FEH:( araby.BEH, araby.FEH, araby.MEEM ), 
araby.KAF:( araby.JEEM, araby.DAD, araby.TAH, araby.ZAH, araby.QAF, araby.KAF), 
araby.LAM:( araby.REH, araby.SHEEN, araby.LAM, araby.NOON ), 
araby.MEEM :( araby.BEH, araby.FEH, araby.MEEM ), 
araby.NOON :( araby.REH, araby.LAM, araby.NOON ), 
araby.WAW :( araby.WAW , araby.YEH), 
araby.YEH:( araby.THEH, araby.JEEM, araby.HAH, araby.KHAH, araby.THAL, araby.ZAIN, araby.SHEEN, araby.SAD, araby.DAD, araby.TAH, araby.ZAH, araby.GHAIN, araby.KAF, araby.HEH, araby.YEH),}

# treat two suffixe letters
bisuffixes_letters=(araby.KAF+araby.MEEM ,araby.KAF+araby.NOON ,araby.HEH+araby.MEEM ,araby.HEH+araby.NOON )

bisuffixes_forbiden={
araby.HEH+araby.MEEM :(araby.ALEF_HAMZA_ABOVE, araby.HAMZA, araby.WAW_HAMZA, araby.YEH_HAMZA, araby.BEH, araby.THEH, araby.HAH, araby.KHAH, araby.SAD, araby.DAD, araby.TAH, araby.ZAH, araby.AIN, araby.GHAIN, araby.HEH, araby.YEH), 
araby.KAF+araby.MEEM :(araby.ALEF_HAMZA_ABOVE, araby.HAMZA, araby.WAW_HAMZA, araby.YEH_HAMZA, araby.BEH, araby.THEH, araby.JEEM, araby.KHAH, araby.ZAIN, araby.SEEN , araby.SHEEN, araby.DAD, araby.TAH, araby.ZAH, araby.GHAIN, araby.FEH, araby.QAF, araby.KAF, araby.LAM, araby.NOON , araby.HEH, araby.YEH), 
araby.HEH+araby.NOON :(araby.ALEF_HAMZA_ABOVE, araby.HAMZA, araby.WAW_HAMZA, araby.YEH_HAMZA, araby.BEH, araby.THEH, araby.JEEM, araby.HAH, araby.KHAH, araby.SAD, araby.DAD, araby.TAH, araby.ZAH, araby.AIN, araby.GHAIN, araby.HEH, araby.YEH), 
araby.KAF+araby.NOON :(araby.ALEF_HAMZA_ABOVE, araby.HAMZA, araby.WAW_HAMZA, araby.YEH_HAMZA, araby.BEH, araby.THEH, araby.JEEM, araby.HAH, araby.KHAH, araby.THAL, araby.SHEEN, araby.DAD, araby.TAH, araby.ZAH, araby.AIN, araby.GHAIN, araby.QAF, araby.KAF, araby.NOON , araby.HEH, araby.YEH), 

}

# treat one suffixe letters
suffixes_letters=(araby.KAF,araby.TEH ,araby.HEH)

suffixes_forbiden={
araby.TEH :(araby.THEH, araby.JEEM, araby.DAL, araby.THAL, araby.ZAIN, araby.SHEEN, araby.TAH, araby.ZAH), 
araby.KAF:(araby.THEH, araby.JEEM, araby.KHAH, araby.THAL, araby.TAH, araby.ZAH, araby.GHAIN, araby.QAF),
araby.HEH:(araby.TEH , araby.HAH, araby.KHAH, araby.DAL, araby.REH, araby.SEEN , araby.SHEEN, araby.SAD, araby.ZAH, araby.AIN, araby.GHAIN), 
	}
#--------------------------------
# Prepare the verbs patterns
#---------------------------------
verbPattern={};
# HAMZA BELOW araby.ALEF
verbPattern[100]= re.compile(ur"[%s%s%s%s%s]"%(araby.ALEF_HAMZA_BELOW, araby.TEH_MARBUTA, araby.FATHATAN, araby.DAMMATAN, araby.KASRATAN),re.UNICODE)
verbPattern[121] =re.compile(ur"[%s](.)+"% araby.ALEF_MAKSURA, re.UNICODE)
# the word ends with wa  a is  araby.WAW  araby.ALEF , is a verb
verbPattern[160] = re.compile(ur"([^%s%s%s]..)%s%s$"%( araby.ALEF_HAMZA_ABOVE,  araby.WAW ,  araby.FEH,  araby.WAW ,  araby.ALEF), re.UNICODE) 
# the word is started by  araby.NOON , before REH or araby.LAM, or  araby.NOON , is a verb and not a noun
verbPattern[10] =re.compile(ur"^%s[%s%s%s]"%( araby.NOON , araby.REH, araby.LAM, araby.NOON ),re.UNICODE)
# the word is started by  araby.YEH,
# before some letters is a verb and not a noun
verbPattern[20] = re.compile(ur"^%s[%s%s%s%s%s%s%s%s%s%s%s%s%s]"%( araby.YEH, araby.THAL, araby.JEEM, araby.HAH, araby.KHAH, araby.ZAIN, araby.SHEEN, araby.SAD, araby.DAD, araby.TAH, araby.ZAH, araby.GHAIN, araby.KAF, araby.YEH), re.UNICODE)

# ro do verify this case,
# هذه الحالة تتناقض مع حالة الاستفعال في الأسماء
#يمكن حلها بضبط عدد النجوم إلى ثلاثة
#the word is like inf3l pattern
#print starword.encode('utf8');
verbPattern[30] = re.compile(ur"[%s%s%s%s%s]\*%s\*\*"%(araby.ALEF, araby.YEH, araby.NOON , araby.TEH ,araby.ALEF_HAMZA_ABOVE, araby.TEH ), re.UNICODE)
# the word is like ift3l pattern
verbPattern[40] = re.compile(ur"[%s%s%s%s%s]%s\*\*\*"%(araby.ALEF, araby.YEH, araby.NOON , araby.TEH ,araby.ALEF_HAMZA_ABOVE, araby.NOON ), re.UNICODE)
# the word is like isf3l pattern
verbPattern[50] = re.compile(ur"[%s%s%s%s%s]%s%s([^%s%s%s]{2})([^%s%s%s%s])"%(araby.ALEF, araby.YEH, araby.NOON , araby.TEH ,araby.ALEF_HAMZA_ABOVE, araby.SEEN , araby.TEH ,araby.ALEF, araby.YEH, araby.WAW ,araby.ALEF,araby.HEH,araby.KAF, araby.NOON ),re.UNICODE)
# the word contains y|t|A)st*
# يست، أست، نست، تست
verbPattern[60] = re.compile(ur"(%s|%s|%s|%s)%s%s\*"%(araby.ALEF_HAMZA_ABOVE, araby.YEH, araby.TEH , araby.NOON , araby.SEEN , araby.TEH ), re.UNICODE) 
# the word contains ist***
# استفعل
verbPattern[70]= re.compile(ur"%s%s%s\*\*\*"%(araby.ALEF, araby.SEEN , araby.TEH ), re.UNICODE) 

# the word contains ***t when **+t+* t is  araby.TEH 
# if  araby.TEH  is followed by  araby.MEEM , araby.ALEF,  araby.NOON 
# تم، تما، تن، تا، تني
# حالة تنا غير مدرجة
verbPattern[80] = re.compile(ur"\*\*\*%s(%s|%s|%s[^%s])"%( araby.TEH , araby.MEEM ,araby.ALEF, araby.NOON ,araby.ALEF), re.UNICODE) 
#To reDo
### case of ***w  w is  araby.WAW , this case is a verb,
### the case of ***w* is a noun
##	if re.compile(u"\*\*\*%s[^\*%s]"%( araby.WAW , araby.NOON ), re.UNICODE):
##		if starword.count("*")==3:
##
##		  return -90;
##		else:
##		  if re.compile(u"\*\*\*\*%s%s"%( araby.WAW ,araby.ALEF), re.UNICODE):
##		    return -100;

# case of future verb with  araby.WAW   araby.NOON ,
verbPattern[110] = re.compile(u"^([^\*%s])*[%s%s](.)*\*\*\*%s%s"%( araby.MEEM , araby.YEH, araby.TEH , araby.WAW , araby.NOON ), re.UNICODE)
# case of future verb with araby.ALEF  araby.NOON ,
verbPattern[115] = re.compile(u"^([^\*%s])*[%s%s](.)*\*\*\*%s%s"%( araby.MEEM , araby.YEH, araby.TEH ,araby.ALEF, araby.NOON ), re.UNICODE)

# case of yt,tt,nt and 3 stars is a verb like yt*** or yt*a**
# at is an ambiguous case with hamza of interogation.
verbPattern[120] = re.compile(u"^([^\*])*[%s%s%s]%s(\*\*\*|\*%s\*\*)"%( araby.YEH, araby.TEH , araby.NOON ,  araby.TEH ,araby.ALEF), re.UNICODE)
# case of yn,tn,nn and 3 stars is a verb like yn*** or yn*a* or ynt**

verbPattern[130] =re.compile(u"^([^\*])*[%s%s%s]%s(\*\*\*|\*%s\*|%s\*\*)"%( araby.YEH, araby.TEH , araby.NOON , araby.NOON ,araby.ALEF, araby.TEH ), re.UNICODE)

# case of y***, y
# exception ; case of y**w*
verbPattern[140]= re.compile(u"^([^\*])*%s(\*\*\*|\*%s\*\*)"%( araby.YEH,araby.ALEF), re.UNICODE)
# To do
# لا تعمل مع كلمة البرنامج
##    # the word contains a****  a is araby.ALEF is a verb
##    	if re.compile(ur"^([^\*])*%s(\*\*\*\*)"%(araby.ALEF), re.UNICODE) :
##
##    	    return -150;

# the word has suffix TM ( araby.TEH   araby.MEEM )  and two original letters at list, is a verb
verbPattern[170] = re.compile(u"%s%s([^\*])*$"%( araby.TEH , araby.MEEM ), re.UNICODE) 

# the word ends with an added  araby.TEH 
verbPattern[180] = re.compile(u"-%s$"%( araby.TEH ),re.UNICODE)

# the word starts with  an added  araby.YEH
verbPattern[190] =re.compile(u"^%s-"%( araby.YEH),re.UNICODE)
# the word starts with   araby.TEH  and ends with  araby.TEH  not araby.ALEF  araby.TEH .
verbPattern[200] = re.compile(u"^(.)*%s(.){2,}[^%s]%s$"%( araby.TEH ,araby.ALEF,  araby.TEH ), re.UNICODE)


#--------------------------------
# Prepare the verbs patterns
#---------------------------------
nounPattern={};

nounPattern[1000]=re.compile(ur"^[%s%s%s%s%s%s]"%( araby.WAW_HAMZA, araby.YEH_HAMZA, araby.FATHA,araby.DAMMA,araby.SUKUN,araby.KASRA),re.UNICODE)

# HAMZA BELOW araby.ALEF
nounPattern[1010]=re.compile(ur"[%s%s%s%s%s]"%(araby.ALEF_HAMZA_BELOW, araby.TEH_MARBUTA,araby.FATHATAN,araby.DAMMATAN,araby.KASRATAN),re.UNICODE)

nounPattern[1020]=re.compile(ur"[%s](.)+"%araby.ALEF_MAKSURA,re.UNICODE)

# the word is like ift3al pattern
nounPattern[1030]=re.compile(ur"%s([^%s%s%s%s%s]%s|[%s%s%s]%s|[%s]%s)(.)%s([^%s%s%s])"%(araby.ALEF,araby.LAM, araby.SEEN ,araby.SAD,araby.DAD,araby.ZAH, araby.TEH ,araby.SAD,araby.DAD,araby.ZAH,araby.TAH,araby.ZAIN,araby.DAL,araby.ALEF,araby.HEH,araby.KAF, araby.NOON ), re.UNICODE)

# the word is like inf3al pattern
nounPattern[1040]=re.compile(ur"%s%s(..)%s([^%s%s%s])"%(araby.ALEF, araby.NOON ,araby.ALEF,araby.HEH,araby.KAF, araby.NOON ), re.UNICODE)

# the word is like isf3al pattern
nounPattern[1050]=re.compile(ur"%s%s%s(..)%s([^%s%s%s])"%(araby.ALEF, araby.SEEN , araby.TEH ,araby.ALEF,araby.HEH,araby.KAF, araby.NOON ), re.UNICODE)

# the word is finished by HAMZA preceded by araby.ALEF
#and more than 2 originals letters
nounPattern[1060]=re.compile(ur"[^%s%s%s%s%s%s%s%s]{2,}%s%s(.)*"%( araby.YEH, araby.FEH,araby.LAM, araby.NOON ,araby.ALEF_HAMZA_ABOVE, araby.TEH , araby.WAW ,araby.ALEF,araby.ALEF, araby.HAMZA), re.UNICODE)

# the word contains three araby.ALEF,
# the kast araby.ALEF musn't be at end
nounPattern[1070]=re.compile(ur"^(.)*([%s](.)+){3}$"%(araby.ALEF), re.UNICODE)

# the word is started by beh, before BEH,FEH, araby.MEEM 
#is a noun and not a verb
nounPattern[1080]=re.compile(ur"^%s[%s%s%s]"%(araby.BEH,araby.BEH,araby.FEH, araby.MEEM ), re.UNICODE)

# the word is started by  araby.MEEM , before BEH,FEH, araby.MEEM 
#is a noun and not a verb
nounPattern[1090]=re.compile(ur"^%s[%s%s%s]"%( araby.MEEM ,araby.BEH,araby.FEH, araby.MEEM ), re.UNICODE)

# the word is started  by araby.ALEF araby.LAM
# and the  original letters are more than two,
nounPattern[1120]=re.compile(ur"^[%s|%s]?[%s|%s]?%s%s(.){3,8}"%( araby.FEH, araby.WAW ,araby.KAF,araby.BEH,araby.ALEF,araby.LAM), re.UNICODE)
nounPattern[1121]=re.compile(ur"^[%s|%s]?%s%s(.){3,8}"%(araby.FEH, araby.WAW ,araby.LAM,araby.LAM), re.UNICODE)


# case of  araby.MEEM  has three original letters in folloing
# print starword.encode('utf8');
nounPattern[1140]=re.compile(u"^([^\*])*%s"%( araby.MEEM ),re.UNICODE) 

# case of  araby.MEEM  folowed by t,  araby.NOON , st, has two original letters in folloing
nounPattern[1145]=re.compile(u"^([^\*])*%s(%s|%s|%s%s)"%( araby.MEEM , araby.TEH , araby.NOON , araby.SEEN , araby.TEH ),re.UNICODE)

# the word is finished by araby.ALEF  araby.TEH 
# and the  original letters are more than two,
nounPattern[1150]=re.compile(u"%s%s([^\*])*$"%(araby.ALEF, araby.TEH ),re.UNICODE) 

# the word contains **Y* when y is  araby.YEH
nounPattern[1160]=re.compile(ur"\*\*%s\*"%( araby.YEH),re.UNICODE) 

# the word contains al*Y* when araby.ALEF-araby.LAM+*+ araby.YEH+*is  araby.YEH
nounPattern[1170]=re.compile(ur"%s%s\*%s\*"%(araby.ALEF,araby.LAM, araby.YEH),re.UNICODE) 

# the word contains al*w* when araby.ALEF-araby.LAM+*+ araby.WAW +*  w is  araby.WAW 
nounPattern[1180]=re.compile(ur"%s%s\*%s\*"%(araby.ALEF,araby.LAM, araby.WAW ),re.UNICODE) 

# the word contains ***w* when ***+ araby.WAW +* w is  araby.WAW 
nounPattern[1190]=re.compile(ur"[^%s]\*\*%s\*"%(u"تاينلفأو", araby.WAW ),re.UNICODE) 

# the word contains **a* when **+a+* a is araby.ALEF
nounPattern[1200]=re.compile(ur"\*[\*%s]%s\*"%(u"وي",araby.ALEF),re.UNICODE) 

# the word contains t**y* when **+t+* a is araby.ALEF
nounPattern[1210]=re.compile(ur"%s\*\*%s\*"%( araby.TEH , araby.YEH),re.UNICODE) 

# case of word ends  with araby.ALEF  araby.NOON , nounPattern[]=it hasnt  araby.YEH or  araby.TEH  on prefix
nounPattern[1220]=re.compile(u"^([^\*%s%s])*\*"%( araby.YEH, araby.TEH ),re.UNICODE) 
nounPattern[1221]=re.compile(u"%s%s([^\*%s%s])*$"%(araby.ALEF, araby.NOON ,araby.ALEF, araby.YEH),re.UNICODE)

# case of word ends  with  araby.WAW   araby.NOON , nounPattern[]=it hasnt  araby.YEH or  araby.TEH  on prefix
nounPattern[1230]=re.compile(u"^([^\*%s%s%s%s])*\*"%( araby.YEH, araby.TEH ,araby.ALEF_HAMZA_ABOVE,araby.ALEF),re.UNICODE) 
nounPattern[1231]=re.compile(u"%s%s([^\*%s%s])*$"%( araby.WAW , araby.NOON ,araby.ALEF, araby.YEH),re.UNICODE) 

# case of word ends  with  araby.YEH  araby.NOON , nounPattern[]=it hasnt  araby.YEH or  araby.TEH  on prefix
nounPattern[1232]=re.compile(u"^([^\*%s%s%s%s])*\*"%( araby.YEH, araby.TEH ,araby.ALEF_HAMZA_ABOVE,araby.ALEF),re.UNICODE)
nounPattern[1233]=re.compile(u"%s%s([^\*%s%s])*$"%( araby.YEH, araby.NOON ,araby.ALEF, araby.YEH),re.UNICODE) 

# the word is finished by  araby.WAW - araby.NOON , araby.ALEF- araby.NOON ,  araby.YEH- araby.NOON , and not started by araby.ALEF_HAMZA_ABOVE or  araby.YEH or  araby.TEH  or  araby.NOON ,
# and the stem length is more than 2 letters
# and not have verb prefixes  araby.WAW , FEH, araby.LAM, araby.SEEN 

#ToDo 2 avoid فكان وفزين cases
nounPattern[1100]=re.compile(ur"^[%s|%s]?[%s|%s]?((.){2,7})(%s|%s|%s)%s$"%(araby.FEH, araby.WAW , araby.SEEN ,araby.LAM, araby.WAW , araby.YEH,araby.ALEF, araby.NOON ), re.UNICODE)
nounPattern[1101]=re.compile(ur"^[%s|%s]?[%s|%s]?[%s%s%s%s%s%s]"%(araby.FEH, araby.WAW , araby.SEEN ,araby.LAM, araby.YEH, araby.TEH ,araby.ALEF_HAMZA_ABOVE,araby.ALEF_MADDA, araby.NOON ,araby.ALEF), re.UNICODE)

