#!/usr/bin/python
# -*- coding=UTF-8 -*-
#------------------------------------------------------------------------
# Name:        adaat
# Purpose:    interface between library and the web interface for Adawat 
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-----------------------------------------------------------------------
"""
Adaat, arabic tools interface
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import sys
import os
import re
import random
from collections import Counter

sys.path.append(os.path.join(os.path.dirname(__file__), '../support/'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../mishkal'))


import pyarabic.araby  as araby # arabic words general functions
import pyarabic.number
import pyarabic.named
import pyarabic.unshape

import tashaphyne.stemming 
try:
    import generate
except ImportError:
    from . import generate

import qalsadi.analex 
import asmai.anasem 
import aranasyn.anasyn as arasyn      
import naftawayh.wordtag
import tashkeel.tashkeel as ArabicVocalizer
import maskouk.collocations as colloc 
try:
    import randtext
except ImportError:
    from . import randtext
    

def DoAction(text, action, options = {}):
    """
    do action by name
    """
    if action == "DoNothing":
        return text
    elif action == "TashkeelText":
        lastmark = options.get('lastmark', "0")
        return tashkeel_text(text, lastmark)
    elif action == "Tashkeel2":
        lastmark = options.get('lastmark', "0")    
        return tashkeel2(text, lastmark)
    elif action == "SpellCheck":
        # lastmark= options.get('lastmark', "0")    
        return spellcheck(text)
    elif action == "CompareTashkeel":
        return compare_tashkeel(text)
    elif action == "ReduceTashkeel":
        return reduced_tashkeel_text(text)
    if action == "Contibute":
        return text
    elif action == "StripHarakat":
        return araby.strip_tashkeel(text)
    elif action == "CsvToData":
        return csv_to_python_table(text)
    elif action == "Romanize":
        return romanize(text)
    elif action == "NumberToLetters":
        return number2letters(text)
    elif action == "LightStemmer":
        lastmark = options.get('lastmark', "0")
        return full_stemmer(text, lastmark)
    elif action == "Tokenize":
        return token_text(text)
    elif action == "Poetry":
        return justify_poetry(text)
    elif action == "Unshape":
        return pyarabic.unshape.unshaping_text(text)
    elif action == "Affixate":
        return affixate(text)
    elif action == "Normalize":
        return normalize(text)
    elif action == "Wordtag":
        return wordtag(text)
    elif action == "Inverse":
        return inverse(text)
    elif action == "Itemize":
        return itemize(text)
    elif action == "Tabulize":
        return tabulize(text)
    elif action == "Tabbing":
        return tabbing(text)
    elif action == "Language":
        return segment_language(text)
    elif action == "RandomText":
        return random_text()
    elif action == "showCollocations":
        return show_collocations(text)
    elif action == "extractEnteties":
        return extract_enteties(text)
    elif action == "extractNamed":
        return extractNamed(text)
    elif action == "chunk":
        return chunksplit(text)
    elif action == "bigrams":
        return bigrams(text)
    elif action == "extractNumbered":
        return extractNumbered(text)       
    else:

        return text


def csv_to_python_table(text):
    """
    Convert CSV text to python syntax Array
    return Text
    """
    lines = text.splitlines()
    if u'' in lines:
        lines.remove(u'')
    resulttext = ""

    if len(lines)>1:
        tablename = lines[0]
        if tablename == "":
            tablename = "#Table"
        else :
            tablename = tablename.split()[0]
        # if there only two lines, the array is a list
        if len(lines) == 2:
            fieldsnames = lines[1].split("\t")
            for i in range(len(fieldsnames)):
                fieldsnames[i] = "'%s'" % fieldsnames[i].strip()
            resulttext += tablename + "=("+", ".join(fieldsnames)+u")\n"
        else:
            resulttext += tablename+u"={}\n"
            fieldsnames = lines[1].split("\t")
            for i in range(len(fieldsnames)):
                fieldsnames[i] = fieldsnames[i].strip()
                resulttext += tablename+u"['%s']={}\n" % fieldsnames[i]

            if len(lines) == 3:
                for line in lines[1:]:
                    line = line.strip()
                    fields = line.split("\t")
                    for i in range(len(fields)):
                        fields[i] = fields[i].strip()
            ##            fields[i]=re.sub('\\', ''', fields[i])
                        fields[i] = re.sub("'", "\\'", fields[i])
                        fields[i] = re.sub("\"", "\\\"", fields[i])
                    resulttext += tablename+u"[u'%s']={}\n" % fields[0]
                    for i in range(0, len(fields)):
                        if i < len(fieldsnames):
                            fieldname = fieldsnames[i]
                        else:
                            fieldname = u"Field#%d" % i
                            fieldsnames.append(fieldname)
                            resulttext += tablename+u"[u'%s']={}\n" % fieldname

                        resulttext += tablename+u"[u'%s']=u'%s'" % (fieldname, 
                          fields[i])+"\n"

            else:
                for line in lines[1:]:
                    line = line.strip()
                    fields = line.split("\t")
                    for i in range(len(fields)):
                        fields[i] = fields[i].strip()
            ##            fields[i] = re.sub('\\', ''', fields[i])
                        fields[i] = re.sub("'", "\\'", fields[i])
                        fields[i] = re.sub("\"", "\\\"", fields[i])

                    for i in range(1, len(fields)):
                        if i < len(fieldsnames):
                            fieldname = fieldsnames[i]
                        else:
                            fieldname = u"Field#%d" % i
                            fieldsnames.append(fieldname)
                            resulttext += tablename+u"[u'%s']={}\n" % fieldname

                        resulttext += tablename + u"[u'%s'][u'%s']='%s'" % (
                        fieldname, fields[0], fields[i]) +"\n"

    return resulttext


def romanize(text, code = "ISO"):
    """
    Convert Arabic into Latin using a code representaton
    """
    textcoded = u""
    if ArabicRomanizationTable.has_key(code):
        for k in text:
            if ArabicRomanizationTable[code].has_key(k):
                print("1")
                if explicated:
                    textcoded += "("+k+")"
                    print("2")
                textcoded += ArabicRomanizationTable[code][k]
                print("3")
            else:
                textcoded += "*"
    else:
        textcoded = text
        print("4")
    return textcoded

def number2letters(text):
    """
    Convert number to text
    """
    text = text.strip()
    ar = pyarabic.number.ArNumbers()
    return ar.int2str(text)


def light_stemmer(text):
    """
    LightStemming unsing Tashaphyne
    """
    result = []
    als = tashaphyne.stemming.ArabicLightStemmer()
    word_list = als.tokenize(text)
    for word in word_list:
        #~listseg =  als.segment(word)
        als.segment(word)
        affix_list = als.get_affix_list()
        for affix in affix_list:
            result.append({'word':word, 'prefix':affix['prefix'], 
            'stem':affix['stem'], 'suffix':affix['suffix'], 
            'root':affix['root'], 'type':'-'}
                          )
    return result


def full_stemmer(text, lastmark):
    """
    morphological analysis
    """
  
    result = []
    debug = False
    limit = 100
    cpath = os.path.join(os.path.dirname(__file__), '../tmp/')
    analyzer = qalsadi.analex.Analex(cache_path=cpath)
    if lastmark == "0" or not lastmark:
        analyzer.disable_syntax_lastmark()

    anasynt = arasyn.SyntaxAnalyzer()
    anasem = asmai.anasem.SemanticAnalyzer()    
    analyzer.set_debug(debug)
    analyzer.set_limit(limit)
    analyzer.disable_allow_cache_use()    
    mode = 'all'
    result = analyzer.check_text(text)
    #~result, synodelist = anasynt.analyze(result)
    result, __ = anasynt.analyze(result)
    result = anasem.analyze(result)            
    # the result contains objets
    return anasynt.decode(result)


def token_text(text):
    """
    tokenize a text into words
    """
    tasha = tashaphyne.stemming.ArabicLightStemmer()
    return araby.tokenize(text)
    return tasha.tokenize(text)
##    if u'' in listword:listword.remove(u'')
##     listword

def normalize(text):
    """
    normalize a text
    """
    tasha = tashaphyne.stemming.ArabicLightStemmer()
    return tasha.normalize(text)
    
def justify_poetry(text):
    """
    justify a poetry 
    """
    lines = text.splitlines()
    if u'' in lines:
        lines.remove(u"")
    rows = []
    for line in lines:
        partlist = line.strip().split("\t")
        if u'' in partlist:
            partlist.remove(u"")
        if len(partlist) == 2:
            rows.append(partlist)
    return rows


def affixate(text):
    """
    generate all affixed froms from a word
    """
    word_list = token_text(text)
    if len(word_list) == 0:
        return u''
    else:
        for word in word_list:
            list_gen_words = generate.generate(word)
        return list_gen_words



def wordtag(text):
    """
    word tagginginto noun, verb, tool
    """
    tagger = naftawayh.wordtag.WordTagger()
    word_list = token_text(text)

    if len(word_list) == 0:
        return []
    else:
        list_result = []
        second_previous =""
        previous = u""
        #~previous_tag  =  ""        
        for word in word_list:
            word_nm = araby.strip_tashkeel(word)
            tag = ''
            if tagger.is_stopword(word):
                tag = 't'
            else:
                if tagger.is_noun(word):
                    tag += 'n'
                if tagger.is_verb(word):
                    tag += 'v'
                if tag in ("", "nv"):
                    tag = tagger.context_analyse(previous, word)+"1"
                    if tag in ("", "nv1", "vn1"):
                        tag = tagger.context_analyse(u" ".join([second_previous, previous]), word)+"2"                    
            list_result.append({'word':word, 'tag': tag})
            second_previous = previous
            previous = word_nm
            #~previous_tag  =  tag
        return list_result


def inverse(text):
    """
    inverse a text
    """
    word_list = token_text(text)

    if len(word_list) == 0:
        return []
    else:
        list_result = []
        inter_list = []
        for word in word_list:
            inter_list.append(word[::-1])
        inter_list.sort()
        for word in inter_list:
##            result_list.append()
            list_result.append(word[::-1])
        return list_result


def itemize(text):
    """
     Convert lines into Latex list
    return Text
    """
    lines = text.splitlines()
    if u'' in lines:
        lines.remove(u'')
    resulttext = ""

    if len(lines)>1:
        resulttext = u"\\begin{itemize}\n"
        for line in lines:
            resulttext += u'\\item '+line.strip()+u"\n"
        resulttext += u"\\end{itemize}\n"
    return resulttext


def tabulize(text):
    """
    Convert lines into Latex tabular
    return Text
    """
    lines = text.splitlines()
    if u'' in lines:
        lines.remove(u'')
    resulttext = ""

    if len(lines)>1:
        length = len(lines[0].split("\t"))
        param = "|c"*length+"|"
        resulttext = u"\\begin{table}\n \\begin{tabular}{"+param+u"}\n"
        for line in lines:
            resulttext += u'\\hline '+" & ".join(line.split("\t")) + "\\"*2+"\n"
        resulttext += u"""\hline\n
\\end{tabular}\n
\\label{mytab:table}\n
\\caption{mytab:table}\n
\\end{table}\n"""
    return resulttext

def tabbing(text):
    """
    Convert lines into Latex tabular
    return Text
    """
    lines = text.splitlines()
    if u'' in lines:
        lines.remove(u'')
    resulttext = ""

    if len(lines) > 1:
        length = len(lines[0].split("\t"))
        #~param = "|c"*length+"|"
        resulttext = u"\\begin{tabbing}\n"
        resulttext += "\hspace{4cm}\="*length+"\kill\n"
        for line in lines:
            resulttext += " \\> ".join(line.split("\t"))+"\\"*2+"\n"
        resulttext += u"""\end{tabbing}\n
                    """
    return resulttext


def segment_language(text):
    """
    Detect language
    """
    resultlist = []
    if re.search(u"[\u0600-\u06ff]", text[0]):
        arabic = True
    else:
        arabic = False
    actual_text = u""
    for  k in text:
        if re.search(u"[\u0600-\u06ff]", k):
            if arabic:
                actual_text += k
            else:
                resultlist.append(('latin', actual_text))
                arabic = True
                actual_text = k
        elif re.search(u"[\s\d\?, :\!\(\)]", k):
            actual_text += k
        else:
            if arabic:
                i = len(actual_text)
                temp_text = u""
                while not re.search(u"[\u0600-\u06ff]", actual_text[i:i+1]):
                    i -= 1
                temp_text = actual_text[i+1:]
                actual_text = actual_text[:i+1]
                resultlist.append(('arabic', actual_text))
                arabic = False
                actual_text = temp_text+k
            else:
                actual_text += k
    if arabic:
        resultlist.append(('arabic', actual_text))
    else:
        resultlist.append(('latin', actual_text))
    return resultlist


def tashkeel_text(text, lastmark=True):
    """
    Tashkeel text without suggestions
    """
    cpath = os.path.join(os.path.dirname(__file__), '../tmp/')
    vocalizer = ArabicVocalizer.TashkeelClass(mycache_path=cpath)
    #~ print "lastMark", lastmark
    if lastmark == "0":
        vocalizer.disable_last_mark()
    vocalized_text = vocalizer.tashkeel(text)
    return vocalized_text
def reduced_tashkeel_text(text):
    """
    Reduce Harakat and vocalization from a vocalized text.
    @param text: a given vocalized text.
    @type text: unicode.
    @return : reduced text vocalization
    @rtype: unicode
    """
    return araby.reduce_tashkeel(text)

def show_collocations(text):
    """
    Show collocations found in the text.
    The collocations is looked up from a data base extracted from a corpus.
    @param text: a given vocalized text.
    @type text: unicode.
    @return : the text have collocations quoted
    @rtype: unicode
    """
    """import tashkeel.tashkeel as ArabicVocalizer    
    vocalizer = ArabicVocalizer.TashkeelClass()
    vocalized_text = vocalizer.stat_tashkeel(text)
    return vocalized_text
    """
    coll = colloc.CollocationClass(True)
    text = coll.lookup4long_collocations(text)
    wordlist = araby.tokenize(text)
    vocalized_list, taglist = coll.lookup(wordlist)
    #return u" ".join(zip(vocalized_list,taglist))
    text_output = u""
    opened = False
    for word, tag in zip(vocalized_list,taglist):
        if tag in ( "CB", "CI"):
            if not opened:
                text_output += "<mark class='coll'>"
                opened = True   
            text_output += word + " "
        else:
            if opened:
                text_output += "</mark>"
                opened = False
            text_output += word + " "
    return text_output
def extractNamed(text):
    """
    Extract Named Enteties in the text.
    @param text: a given text.
    @type text: unicode.
    @return : the text have Named enteties quoted
    @rtype: unicode
    >>> extractNamed(u"قال خالد بن رافع  حدثني أحمد بن عنبر عن خاله")
    ("خالد بن رافع"، "أحمد بن عنبر ")
    """
    wordlist = araby.tokenize(text)
    taglist = pyarabic.named.detect_named(wordlist)

    text_output = ""
    opened = False
    for word, tag in zip(wordlist, taglist):
        if tag in ("named", 'NI','NB'):
            if not opened:
                text_output += "<mark class='named'>"
                opened = True   
            text_output += word + " "
        else:
            if opened:
                text_output += "</mark>"
                opened = False
            text_output += word + " "
    return text_output


def extract_enteties(text):
    """
    Extract enteties as numbers, named enteties, collocations.
    @param text: a given text.
    @type text: unicode.
    @return : the text have enteties phrases quoted
    @rtype: unicode
    """

    coll = colloc.CollocationClass(True)
    wordlist = araby.tokenize(text)
    taglist_nb = pyarabic.number.detect_numbers(wordlist)
    voclist_nb = pyarabic.number.pre_tashkeel_number(wordlist)
    taglist_nmd = pyarabic.named.detect_named(wordlist)
    voclist_nmd = pyarabic.named.pretashkeel_named(wordlist)
    voclist_coll, taglist_coll = coll.lookup(wordlist)
    # return phrases
    text_output = []
    opened = False
    for word, tagnb, vocnb, tagnmd, vocnmd, tagcol, voccol in zip(wordlist, taglist_nb,voclist_nb, taglist_nmd, voclist_nmd, taglist_coll, voclist_coll):
        if tagnb == 'DB':
            if opened:
                text_output.append("</mark>")
            text_output.extend(["<mark class='number'>",vocnb] )
            opened = True                  
        elif tagnmd == 'NB':
            if opened:
                text_output.append("</mark>")
            text_output.extend(["<mark class='named'>",vocnmd] )
            opened = True  
        elif tagcol =='CB':
            if opened:
                text_output.append("</mark>")
            text_output.extend(["<mark class='coll'>",voccol] )
            opened = True 
        elif tagnmd == "NI":
            text_output.append(vocnmd) 
        elif tagnb == "DI":
            text_output.append(vocnb) 
        elif tagcol == "CI":
            text_output.append(voccol) 
        else:
            if opened:
                 text_output.append("</mark>") 
                 opened = False
            text_output.append(word)
    if opened:
        text_output.append("</mark>")  
    return u" ".join(text_output)


def extract_enteties2(text):
    """
    Extract enteties as numbers, named enteties, collocations.
    @param text: a given text.
    @type text: unicode.
    @return : the text have enteties phrases quoted
    @rtype: unicode
    """
    coll = colloc.CollocationClass(True)
    wordlist = araby.tokenize(text)
    taglist_nb = pyarabic.number.detect_numbers(wordlist)
    taglist_nmd = pyarabic.named.detect_named(wordlist)
    vocalized_list, taglist_coll = coll.lookup(wordlist)
    # return phrases
    text_output = ""
    opened = False
    for word, voc, tagnb, tagnmd, tagcol in zip(wordlist,vocalized_list, taglist_nb, taglist_nmd, taglist_coll):
        if tagnb in ('DI','DB'):
            if not opened:
                text_output += "<mark class='number'>"
                opened = True   
            text_output += word + " "
        elif tagnmd in ('NI','NB'):
            if not opened:
                text_output += "<mark class='named'>"
                opened = True   
            text_output += word + " "
        elif tagcol in ('CI','CB'):
            if not opened:
                text_output += "<mark class='coll'>"
                opened = True   
            text_output += voc + " "           
        else:
            if opened:
                text_output += "</mark>"
                opened = False
            text_output += word + " "
    return text_output
   

def extractNumbered(text):
    """
    Extract number phrases in the text.
    @param text: a given text.
    @type text: unicode.
    @return : the text have number phrases quoted
    @rtype: unicode
    >>> extractNumber(u"وجدت خمسمئة وثلاثة وعشرين دينارا")
    وجدت خمسمئة وثلاثة وعشرين دينارا ")
    """
    wordlist = araby.tokenize(text)
    taglist = pyarabic.number.detect_numbers(wordlist)
    # return phrases
    text_output = ""
    opened = False
    for word, tag in zip(wordlist, taglist):
        if tag in ("named", 'DI','DB'):
            if not opened:
                text_output += "<mark class='number'>"
                opened = True   
            text_output += word + " "
        else:
            if opened:
                text_output += "</mark>"
                opened = False
            text_output += word + " "
    return text_output
    
def tashkeel2(text, lastmark):
    """
    Tashkeel text with suggestions
    """
    #~ import tashkeel.tashkeel as ArabicVocalizer
    cpath = os.path.join(os.path.dirname(__file__), '../tmp/')
    vocalizer = ArabicVocalizer.TashkeelClass(mycache_path = cpath)
    #~ vocalizer.disable_cache()
    if lastmark == "0" or not lastmark:
        vocalizer.disable_last_mark()    
    vocalized_dict = vocalizer.tashkeel_ouput_html_suggest(text)
    return vocalized_dict
    
def spellcheck(text):
    """
    Spellcheck a text
    """
    import spellcheck.spellcheck as ArabicSpellchecker
    cpath = os.path.join(os.path.dirname(__file__), '../tmp/')
    vocalizer = ArabicSpellchecker.SpellcheckClass(cpath)
    #print (u"lastMark %s"%lastmark).encode('utf8')
    vocalized_dict = vocalizer.spellcheckOuputHtmlSuggest(text)
    return vocalized_dict

def compare_tashkeel(text):
    """
    Compare tashkeel between vocalized text and automatic vocalized text
    """
    #~ import tashkeel.tashkeel as ArabicVocalizer
    # the entred text is vocalized correctly
    correct_text = text.strip()
    text = araby.strip_tashkeel(text.strip())
    cpath = os.path.join(os.path.dirname(__file__), '../tmp/')
    vocalizer = ArabicVocalizer.TashkeelClass(mycache_path=cpath)
    #~vocalized_text = vocalizer.tashkeel(text)
    #~ vocalizer.disable_cache()

    vocalized_dict = vocalizer.tashkeel_ouput_html_suggest(text)
    
    # compare voalized text with a correct text
    text1 = correct_text
    #~text2 = vocalized_text
    displayed_html = u""
    
    #stemmer=tashaphyne.stemming.ArabicLightStemmer()
    #~texts = vocalizer.analyzer.split_into_phrases(text1)
    texts = [text1, ]
    list1 =[]
    for txt in texts:
        list1 += vocalizer.analyzer.tokenize(txt)
    list2 = vocalized_dict
    print(u"\t".join(list1).encode('utf8'))
    correct = 0
    incorrect = 0
    total = len(list1)
    if len(list1)!= len(list2):
        print("lists haven't the same length", len(list1), len(list2))
        for i in range(min(len(list1), len(list2))):
            print((u"'%s'\t'%s'"%(list1[i], list2[i].get('chosen',''))).encode("utf8"))
        sys.exit()
    else:
        for i in range(total):
            wo1 = list1[i]
            wo1_strip = wo1            
            wo2 = list2[i]['chosen']
            wo2_strip = list2[i]['semi']  # words without inflection mark
            inflect = list2[i]['inflect']
            link = list2[i]['link']
            rule = list2[i]['rule']
            style = "diff"
            #~if araby.is_vocalized(wo2) and araby.vocalizedlike(wo1, wo2):
            if araby.vocalizedlike(wo1, wo2):
                if wo2 == "\n":
                    wo2 = "<br/>"
                #~displayed_html += u" " + wo2
                displayed_html += u" <span id='diff'  class='%s' original='%s' inflect='%s' link='%s' rule='%s'>%s</span>" % ( style, wo1, inflect, link, str(rule), wo2)

                correct += 1
            else:
                incorrect += 1
                # green for last mark difference
                wo1_strip = wo1
                #~wo2_strip = araby.strip_lastharaka(wo2)
                if araby.vocalizedlike(wo1_strip, wo2_strip):
                    style = 'diff-mark'
                else:
                    # if the last marks are equal
                    wm1 = wo1[-1:]
                    wm2 = wo2[-1:]
                    if (araby.is_haraka(wm1) and araby.is_haraka(wm2) and wm1 == wm2) \
                    or (bool(araby.is_haraka(wm1)) ^  bool(araby.is_haraka(wm2))):
                        style = "diff-word"
                    else:
                        style = 'diff-all'
                displayed_html += u" <span id='diff'  class='%s' original='%s' inflect='%s' link='%s' rule='%s'>%s</span>" % ( style, wo1, inflect, link, str(rule), wo2)
    per_correct = round(correct*100.00/total, 2)
    per_incorrect = round(incorrect*100.00/total, 2)
    result = [displayed_html, "correct:%0.2f%%, incorrect:%0.2f%%"%(per_correct, per_incorrect)]
    return result#correct*100/total

def assistanttashkeel(text):
    """
    get tashkeel with suggestions
    """
    #~ import tashkeel.tashkeel as ArabicVocalizer
    cpath = os.path.join(os.path.dirname(__file__), '../tmp/')
    vocalizer = ArabicVocalizer.TashkeelClass(mycache_path=cpath)
    vocalized_text = vocalizer.assistanttashkeel(text)
    return vocalized_text
def random_text():
    """
    get random text for tests
    """    

    
    return random.choice(randtext.textlist)
def chunksplit(text):
    """
    split text into chunks
    """
    # lexical analyzer
    cpath = os.path.join(os.path.dirname(__file__), '../tmp/')
    morphanalyzer = qalsadi.analex.Analex(cache_path=cpath)
    # syntaxic analyzer
    anasynt = aranasyn.anasyn.SyntaxAnalyzer(cache_path=cpath);    
    #~ line =  araby.strip_tashkeel(line);
    #morpholigical analysis of text
    detailled_stem =  morphanalyzer.check_text(text);
    #syntaxical analysis of text
    detailled_syntax, synnodeList =  anasynt.analyze(detailled_stem);
    # print detailled_syntax;
    syno_tags = u" ‫"
    chunklist =[]
    achunk = []
    for synnode in synnodeList:
        if synnode.get_break_type() in ("break", "mostBreak"):
            if synnode.is_break_end():
                achunk.append(synnode.get_word())
                chunklist.append(u" ".join(achunk))
                achunk = []
               #~ print synnode.get_word().encode('utf8');
               #~ print syno_tags.encode('utf8')
                syno_tags = ""
            else:
                chunklist.append(u" ".join(achunk))
                achunk = []
                achunk.append(synnode.get_word())               
               #~ print "break";
               #~ print syno_tags.encode('utf8')
                syno_tags = u" ‫"
               #~ print synnode.get_word().encode('utf8'),                        
        else:
            achunk.append(synnode.get_word())
    if achunk:
        chunklist.append(u" ".join(achunk))
            #print synnode.get_word().encode('utf8'),
        #syno_tags += " '%s[%s]'"%(synnode.get_word_type(), synnode.get_guessed_type_tag())
    return chunklist
def bigrams(text):
    """
    split text into bigrams
    """
    # tokenize texts
    words = araby.tokenize(text)
    bigramslist = []
    for i in range(len(words)-1):
        bigramslist.append(u" ".join([words[i], words[i+1]]))
    counts = Counter(bigramslist)
    bl =[]
    for item in sorted(counts):
        bl.append(u' '.join([item, str(counts[item])]))
    #~ return bigramslist
    return bl
