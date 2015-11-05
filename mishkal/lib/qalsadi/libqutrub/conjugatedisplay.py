#!/usr/bin/python
# -*- coding=utf-8 -*-
#************************************************************************
# $Id: conjugateddisplay.py, v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2009, Arabtechies, Arabeyes Taha Zerrouki
#
#  The Class used to display information after conjugated
#   All print and views and display are redirected to this class
#
# -----------------
# Revision Details:    (Updated by Revision Control System)
# -----------------
#  $Date: 2009/06/02 01:10:00 $
#  $Author: Taha Zerrouki $
#  $Revision: 0.7 $
#  $Source: arabtechies.sourceforge.net
#
#***********************************************************************/
"""
The conjugation display class to manage different display format.
"""
#~ from libqutrub.verb_const import *
import libqutrub.verb_const as vconst
import pyarabic.araby as araby

# صف عرض التصريفات حسب الضمائر
# جدول عرض التصريفات حسب الأزمنة
# تعيينه متغيرا شاملا من أجل تقليل
 #~ بناء جدول عرض التصريفات في كل عرض.
ONE_TENSE_PRONOUN = {u"أنا":"" , u"أنت":"" , u"أنتِ":"" , u"هو":"" ,
 u"هي":"" , u"أنتما":"" , u"أنتما مؤ":"" , u"هما":"" , 
 u"هما مؤ":"" ,
  u"نحن":"" , u"أنتم":"" , u"أنتن":"" , u"هم":"" , u"هن":""}

# delete the global TableConj vvariable because  it causes problem
TAB_DISPLAY = {
vconst.PronounAna:u"1", 
vconst.PronounNahnu:u"2", 
vconst.PronounAnta:u"3", 
vconst.PronounAnti:u"4ِ", 
vconst.PronounAntuma:u"5", 
vconst.PronounAntuma_f:u"6", 
vconst.PronounAntum:u"7", 
vconst.PronounAntunna:u"8", 
vconst.PronounHuwa:u"9", 
vconst.PronounHya:u"10", 
vconst.PronounHuma:u"11", 
vconst.PronounHuma_f:u"12", 
vconst.PronounHum:u"13", 
vconst.PronounHunna:u"14", 


# const for Tense Name
vconst.TensePast:u"20", 
vconst.TenseFuture:u"21", 
vconst.TenseImperative:u"22", 
vconst.TenseConfirmedImperative:u"23", 
vconst.TenseJussiveFuture:u"24", 
vconst.TenseSubjunctiveFuture:u"25", 
vconst.TenseConfirmedFuture:u"26", 


vconst.TensePassivePast:u"27", 
vconst.TensePassiveFuture:u"28", 
vconst.TensePassiveJussiveFuture:u"29", 
vconst.TensePassiveSubjunctiveFuture:u"30", 
vconst.TensePassiveConfirmedFuture:u"31", 
}

class ConjugateDisplay:
    """
    conjugatedisplay class is used to display verb conjugation 
    in different ways and uses.
    """
    tab_conjug = {}
    pronouns = {}
    verb = u""
    mode = 'Text'
    future_form = u""
    text = {}
    transitive = False
    def __init__(self, verb):
        """
        Create the conjugedtdisplay instance for the verb.
        @param verb: given verb.
        @type verb unicode.
        """
# بناء جدول عرض التصريفات
        self.tab_conjug = {
    vconst.TensePast:ONE_TENSE_PRONOUN.copy(), 
    vconst.TensePassivePast:ONE_TENSE_PRONOUN.copy(), 
    vconst.TenseFuture:ONE_TENSE_PRONOUN.copy(), 
    vconst.TensePassiveFuture:ONE_TENSE_PRONOUN.copy(), 
    vconst.TenseJussiveFuture:ONE_TENSE_PRONOUN.copy(), 
    vconst.TensePassiveJussiveFuture:ONE_TENSE_PRONOUN.copy(), 
    vconst.TenseSubjunctiveFuture:ONE_TENSE_PRONOUN.copy(), 
    vconst.TensePassiveSubjunctiveFuture:ONE_TENSE_PRONOUN.copy(), 
    vconst.TenseImperative:ONE_TENSE_PRONOUN.copy(), 
    vconst.TenseConfirmedFuture:ONE_TENSE_PRONOUN.copy(), 
    vconst.TenseConfirmedImperative:ONE_TENSE_PRONOUN.copy()
    }
        self.verb = verb
        self.text = {}
        self.mode = 'Text'
        self.future_form = u""
        self.transitive = False
        self.bab = "0"
    def __del__(self):
        self.tab_conjug = {}
        self.verb = ""
        self.text = {}
        self.mode = 'Text'
        self.future_form = u""
        self.transitive = False
        self.bab = "0"
#####################################
#{ Attributes functions
#####################################
    def setmode(self, mode):
        """ 
        Set the display mode as:
            - 'Text':
            - 'HTML':
            - 'HTMLColoredDiacritics':
            - 'DICT':
            - 'CSV':
            - 'GUI':
            - 'TABLE':
            - 'XML':
            - 'TeX':
            - 'ROWS':
        @param mode: the given mode to display result
        @type mode: unicode
        """
        self.mode = mode
    def settransitive(self):
        """ 
        Set the transitivity value to True.
        """    
        self.transitive = True 
    def setbab(self, bab):
        """ 
        Set the bab sarf value to bab
        @param bab: the given sarf bab.
        @type bab: integer (1-6)
        """    
        self.bab = bab
#------------------------------------------------------------------
    def set_future_form(self, future_form):
        """ 
        Set the future form of the verb value to future_form.
        مثلا: صرب يصرب
        @param future_form: the future form.
        @type future_form: unicode
        """        
        self.future_form = future_form
    def get_verb_attributs(self):
        """
        Get attributes as text
        @return: Attributes as text.
        @rtype: unicode
        """    
        return self.text

    def add_attribut(self, title, value):
        """
        Add a new attribut to display, like the transitivity 
        the root and the future form.
        @param title: the title of the attribute to display.
        @type title: unicode
        @param value:the value if the attribute.
        @type value: unicode
        """    
        if title != '' :
            self.text[title] = value
    def get_conj(self, tense, pronoun):
        """
        Get the conjugated verb by tense and pronoun.
        @param tense: tense of the added conjuagtion.
        @type tense: unicode
        @param pronoun: pronoun of the added conjuagtion.
        @type pronoun: unicode
        @return : conjugated form of verb if exists.
        @rtype : unicode
        
        """
        if  self.tab_conjug.has_key(tense):
            if self.tab_conjug[tense].has_key(pronoun):
                return self.tab_conjug[tense][pronoun]
        return u""

    def add(self, tense, pronoun, verbconjugated):
        """
        Add a new conjugation to display.
        @param tense: tense of the added conjuagtion.
        @type tense: unicode
        @param pronoun: pronoun of the added conjuagtion.
        @type pronoun: unicode
        @param verbconjugated:aded conjuagtion.
        @type verbconjugated:unicode
        
        """
        if  not self.tab_conjug.has_key(tense):
            self.tab_conjug[tense] = {}
        self.tab_conjug[tense][pronoun] = verbconjugated
#####################################
#{ Display functions
#####################################
    def display(self, listtense = None):
        """
        Display The conjugation result for a list of tenses, 
        with a display mode given by the class attribute.
        Set the display mode as:
            - 'Text':
            - 'HTML':
            - 'HTMLColoredDiacritics':
            - 'DICT':
            - 'CSV':
            - 'GUI':
            - 'TABLE':
            - 'XML':
            - 'TeX':
            - 'ROWS':
        @param listtense: the given tenses list to display result
        @type listtense: list of unicode
        @return: the result in a specified dispaly mode.
        @rtype: according to display mode.
        """        
        return self.display(self.mode, listtense)
    def display(self, mode, listtense = None):
        """
        Display The conjugation result for a list of tenses, 
        with a display mode.
        Set the display mode as:
            - 'Text':
            - 'HTML':
            - 'HTMLColoredDiacritics':
            - 'DICT':
            - 'CSV':
            - 'GUI':
            - 'TABLE':
            - 'XML':
            - 'TeX':
            - 'ROWS':
        @param mode: the given mode to display result
        @type mode: unicode
        @param listtense: the given tenses list to display result
        @type listtense: list of unicode
        @return: the result in a specified dispaly mode.
        @rtype: according to display mode.
        """
        if not listtense:
            listtense = vconst.TABLE_TENSE
        if mode == 'Text':
            return self.display_text(listtense)
        elif mode == 'HTML':
            return self.display_html(listtense)
        elif mode == 'HTMLColoredDiacritics':
            return self.display_html_colored_diacritics(listtense)
        elif mode == 'DICT':
            return self.display_dict(listtense)
        elif mode == 'CSV':
            return self.display_csv(listtense)
        elif mode == 'GUI':
            return self.display_table(listtense)
        elif mode == 'TABLE':
            return self.display_table(listtense)
        elif mode == 'XML':
            return self.display_xml(listtense)
        elif mode.upper() == 'TeX'.upper():
            return self.display_tex(listtense)
        elif mode == 'ROWS'.upper():
            return self.display_rows(listtense)
        else:
            return self.display_text(listtense)

    def display_text(self, listtense):
        """
        Display The conjugation result for a list of tenses, as text.
        @param listtense: the given tenses list to display result
        @type listtense: list of unicode
        @return: the result as text.
        @rtype: uunicode.
        """    
        text = u""
        for title in self.text.keys():
            text += u"%s: %s\n"  % (title, self.text[title])
        text += u"\t"
        text += u"\t".join(listtense)
        for pronoun in vconst.PronounsTable:
            text += u"\n%s"  % (pronoun)
            for tense in listtense:
                if self.tab_conjug[tense].has_key(pronoun):
                    text += u"\t%s"  % (self.tab_conjug[tense][pronoun])
        return text


    def display_csv(self, listtense ):
        """
        Display The conjugation result for a list of tenses, 
        as comma separeted value text.
        every line contains:
        example:
            >>> اللزوم/التعدي: متعدي
            الفعل: مَنَحَ
            نوع الفعل: فعل ثلاثي
            الماضي المعلومالمضارع المعلومالمضارع المجزومالمضارع المنصو
            بالمضارع المؤكد الثقيلالأمرالأمر المؤكدالماضي المجهولالمضارع المجهولالمضارع المجهول المجزومالمضارع المجهول المنصوبالمضارع المؤكد الثقيل المجهول 
            أنامَنَحْتُأَمْنَحُأَمْنَحْأَمْنَحَأَمْنَحَنَّمُنِحْتُأُمْنَحُأُمْنَحْأُمْنَحَأُمْنَحَنَّ
            نحنمَنَحْنَانَمْنَحُنَمْنَحْنَمْنَحَنَمْنَحَنَّمُنِحْنَانُمْنَحُنُمْنَحْنُمْنَحَنُمْنَحَنَّ
            أنتمَنَحْتَتَمْنَحُتَمْنَحْتَمْنَحَتَمْنَحَنَّاِمْنَحْاِمْنَحَنَّمُنِحْتَتُمْنَحُتُمْنَحْتُمْنَحَتُمْنَحَنَّ


        @param listtense: the given tenses list to display result
        @type listtense: list of unicode
        @return: the result as text in row.
        @rtype: unicode.
        """        
        text = u""
        for title in self.text.keys():
            text += u"%s: %s\n"  % (title, self.text[title])
        text += u"".join(listtense)
        text += u"\n"
        for pronoun in vconst.PronounsTable:
            text += u"%s"  % (pronoun)
            for tense in listtense:
#                print (self.verb).encode("utf-8"), 
                if self.tab_conjug[tense].has_key(pronoun):
                    text += u"%s"  % (self.tab_conjug[tense][pronoun])
            text += u"\n"
        return text




    def display_rows(self, listtense ):
        """
        Display The conjugation result for a list of tenses, as text in rows.
        every row contains:
            - unvocalized conjugation, 
            - unvocalized conjugation, 
            - pronoun
            - tense, 
            - transitive, 
            - original verb
            - tasrif bab

        @param listtense: the given tenses list to display result
        @type listtense: list of unicode
        @return: the result as text in row.
        @rtype: unicode.
        """        
        text = u""

        transitive = "0"
        if self.transitive:
            transitive = '1'
        for pronoun in vconst.PronounsTable:
##            text += u"%s"  % (pronoun)
            for tense in listtense:
#                print (self.verb).encode("utf-8"), 
                if  self.tab_conjug[tense][pronoun] != "":
                    text += "\t".join([
                        araby.strip_harakat(self.tab_conjug[tense][pronoun]), 
                        self.tab_conjug[tense][pronoun], 
                        TAB_DISPLAY[pronoun], 
                        TAB_DISPLAY[tense], 
                        transitive, 
                        self.verb, 
                        self.bab, 
                        ])
                    text += u"\n"
        return text


    def display_html(self, listtense):
        """
        Display The conjugation result for a list of tenses, as HTML.
        @param listtense: the given tenses list to display result
        @type listtense: list of unicode
        # @return: the result as HTML.
        @rtype: unicode.
        """        
        indicative_tenses = []
        passive_tenses = []
        for tense in listtense:
            if tense in vconst.TableIndicativeTense:
                indicative_tenses.append(tense)
            else:
                passive_tenses.append(tense)
        text = u""
        text += u"<h3>%s : %s - %s</h3>\n"  % (self.verb, self.verb, 
        self.future_form)
#        text += u"<h3>%s - %s</h3>\n\n"  % (self.verb, self.future_form)
        # print spelcial attribut of the verb
        text += u"<ul>\n"
        for title in self.text.keys():
            text += u"<li><b>%s:</b> %s</li>\n"  % (title, self.text[title])
        text += u"</ul>\n\n"

        for  mode in("indicative", "passive"):
            if mode == "indicative":
                listtense_to_display = indicative_tenses

            else:
                listtense_to_display = passive_tenses
                text += "<br/>"
            if len(listtense_to_display) >0:
                text += u"""<table class = 'resultarea' border = 1
                 cellspacing = 0>\n"""
                text += u"<tr><th>&nbsp</th>"
                for tense in listtense_to_display:
                    text += u"<th>%s</th>"  % (tense)
                text += u"</tr>\n"
                for pronoun in vconst.PronounsTable:
                    text += u"<tr>"
                    text += u"<th>%s</th>"  % (pronoun)
                    for tense in listtense_to_display:
                        text += u"<td>&nbsp%s</td>"  % (
                        self.tab_conjug[tense][pronoun])
                    text += u"</tr>\n"
                text += u"</table>\n"
        return text

    def display_html_colored_diacritics(self, listtense):
        """
        Display The conjugation result for a list of tenses, 
        as HTML with colored vocalization.
        @param listtense: the given tenses list to display result
        @type listtense: list of unicode
        @return: the result as HTML.
        @rtype: unicode.
        """        
        text = self.display_html(listtense)
##        text = "<div style = 'color:red'>"+text+"</div>"
        text = self.highlight_diacritics_html(text)
        return text

    def highlight_diacritics_html(self, text):
        """
        Highlight dfiactitics in the HTML text.
        @param text: the given text
        @type text: unicode.
        @return: the result as HTML.
        @rtype: unicode.
        """        
        hight_text = u""
        lefttag = u"<span class = 'tashkeel'>"
        righttag = u"</span>"
        for i in range(len(text)):
            if text[i] in (araby.FATHA, araby.DAMMA, araby.KASRA, araby.SUKUN):
                if (i>0 and text[i-1] not in (araby.ALEF, 
                araby.ALEF_HAMZA_ABOVE, araby.WAW_HAMZA, araby.ALEF_MADDA,
                 araby.DAL, araby.THAL, araby.WAW, araby.REH, araby.ZAIN,
            araby.SHADDA)) and (i+1<len(text) and text[i+1] not in (" ", "<")):
                    hight_text += u"".join([lefttag, araby.TATWEEL, 
                    text[i], righttag])
                else :
##               hight_text += u"<span style = 'color:red'>%s</span>"%text[i]
                    hight_text += u"".join([lefttag, " ", text[i], righttag])
            else:
                hight_text += text[i]
        return hight_text

    def display_table(self, listtense):
        """Display The conjugation result for a list of tenses, as array.
        @param listtense: the given tenses list to display result
        @type listtense: list of unicode
        @return: the result as table, the table[0] contains pronouns.
        @rtype: dict with number indice.
        """    
        table = {}

        j = 0
        table[0] = {0:u"الضمائر"}
        for j in range(len(listtense)):
            table[0][j+1] = listtense[j]
        i = 1
        for pronoun in vconst.PronounsTable:
            table[i] = {}
            table[i][0] = pronoun
            j = 1
            for tense in listtense:
                table[i][j] = self.tab_conjug[tense][pronoun]
                j = j+1
            i = i+1
        return table

    def display_dict(self, listtense):
        """
        Display The conjugation result for a list of tenses, as python dict.
        @param listtense: the given tenses list to display result
        @type listtense: list of unicode
        @return: the result as python dict.
        @rtype: dict.
        """        
        table = {}
        for tense in listtense:
            table[tense] = self.tab_conjug[tense]
        #text = json.dumps(table, ensure_ascii = False)
        return table

    def display_xml(self, listtense):
        """
        Display The conjugation result for a list of tenses, as XML.
        @param listtense: the given tenses list to display result
        @type listtense: list of unicode
        @return: the result as XML.
        @rtype: unicode.
        """        
        text = u""
        text += u"<verb_conjugation>\n"
        text += u"\t<proprety name = 'verb' value = '%s'/>\n"  % (self.verb)
        for title in self.text.keys():
            text += u"\t<proprety name = '%s' value = '%s'/>\n"  % (title,
             self.text[title])
        for tense in listtense:
            text += u"\t<tense name = '%s'>\n"  % (tense)
            for pronoun in vconst.PronounsTable:
                if self.tab_conjug[tense][pronoun] != "":
                    text += u"""\t\t<conjugation pronoun = '%s' value = '%s'
                    />\n"""  % (pronoun, self.tab_conjug[tense][pronoun])
            text += u"\t</tense>\n"
        text += u"</verb_conjugation>"
        return text

    def display_tex(self, listtense):
        """
        Display The conjugation result for a list of tenses, as TeX.
        @param listtense: the given tenses list to display result
        @type listtense: list of unicode
        @return: the result as TeX format.
        @rtype: unicode.
        """        
        text = u""
        text += u"\\environment qutrub-layout\n"
        text += u"\\starttext\n"

        text += u"\\Title{%s}\n"  % (self.verb)

        text += u"\\startitemize\n"
        for title in self.text.keys():
            if title == u" الكتابة الداخلية للفعل ":
                text += u"\\item {\\bf %s} \\DeShape{%s}\n"  % (title,
                 self.text[title])
            else:
                text += u"\\item {\\bf %s} %s\n"  % (title, self.text[title])
        text += u"\\stopitemize\n"

        text += u"\\starttable[|lB|l|l|l|l|l|]\n"
        text += u"\\HL[3]\n\\NC"
        for tense in listtense:
            text += u"\\NC {\\bf %s}"  % (tense)
        text += u"\\SR\n\\HL\n"
        for pronoun in vconst.PronounsTable:
            text += u"\\NC %s"  % (pronoun)
            for tense in listtense:
                text += u"\\NC %s"  % (self.tab_conjug[tense][pronoun])
            text += u"\\AR\n"
        text += u"\\LR\\HL[3]\n"
        text += u"\\stoptable\n"

        text += u"\\stoptext"
        return text
