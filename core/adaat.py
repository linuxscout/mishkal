#!/usr/bin/python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        adaat
# Purpose:    interface between library and the web interface for Adawat 
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------

import re
import random
import pyarabic.araby  as araby # arabic words general functions
# import pyarabic.unshape # unshape arabic lettres
# import pyarabic.number # convert numbers into arabic words
# import pyarabic.named as named
# import tashkeel.tashkeel as ArabicVocalizer

# GlobalVocalizer=tashkeel.TashkeelClass();
# aranasyn.anasyn as arasyn
import tashaphyne

#from core.ar_stopwords import *
#import core.wordtag 


def DoAction(text,action, options={}):
    if action=="DoNothing":
        return text;
    elif action=="TashkeelText":
        lastmark= options.get('lastmark', "0");
        return tashkeelText(text, lastmark);
    elif action=="Tashkeel2":
        lastmark= options.get('lastmark', "0");	
        return tashkeel2(text, lastmark);
    elif action=="SpellCheck":
        # lastmark= options.get('lastmark', "0");	
        return spellcheck(text);
    elif action=="CompareTashkeel":
        return Comparetashkeel(text);
    elif action=="ReduceTashkeel":
        return reducedTashkeelText(text);
    if action=="Contibute":
        return text;
    elif action=="StripHarakat":
        return araby.stripTashkeel(text);
    elif action=="CsvToData":
        return csv_to_python_table(text);
    elif action=="Romanize":
        return romanize(text);
    elif action=="NumberToLetters":
        return numberToLetters(text);
    elif action=="LightStemmer":
        lastmark= options.get('lastmark', "0");
        return fullStemmer(text,lastmark);
    elif action=="Tokenize":
        return token_text(text);
    elif action=="Poetry":
        return justify_poetry(text);
    elif action=="Unshape":
        import pyarabic.unshape
        return pyarabic.unshape.unshaping_text(text);
    elif action=="Affixate":
        return affixate(text);
    elif action=="Normalize":
        return normalize(text);
    elif action=="Wordtag":
        return wordtag(text);
    elif action=="Inverse":
        return inverse(text);
    elif action=="Itemize":
        return itemize(text);
    elif action=="Tabulize":
        return tabulize(text);
    elif action=="Tabbing":
        return tabbing(text);
    elif action=="Language":
        return segmentLanguage(text);
    elif action=="RandomText":
        return randomText();
    elif action=="showCollocations":
        return showCollocations(text);
    elif action=="extractNamed":
        return extractNamed(text);
    elif action=="extractNumbered":
        return extractNumbered(text);		
    else:

        return text;

#----------------------------
# Convert CSV text to python syntax Array
# return Text
#----------------------------
def csv_to_python_table(text):
    lines=text.splitlines()
    if u'' in lines: lines.remove(u'');
    resultText=""

    if len(lines)>1:
        tablename=lines[0];
        if tablename=="":
            tablename="#Table";
        else :
            tablename=tablename.split()[0];
        # if there only two lines, the array is a list
        if len(lines)==2:
            fieldsnames=lines[1].split("\t");
            for i in range(len(fieldsnames)):
                fieldsnames[i]="'%s'"%fieldsnames[i].strip();
            resultText+=tablename+"=("+",".join(fieldsnames)+u")\n";
        else:
            resultText+=tablename+u"={};\n";
            fieldsnames=lines[1].split("\t");
            for i in range(len(fieldsnames)):
                fieldsnames[i]=fieldsnames[i].strip();
                resultText+=tablename+u"['%s']={}\n"%fieldsnames[i];

            if len(lines)==3:
                for line in lines[1:]:
                    line=line.strip();
                    fields=line.split("\t")
                    for i in range(len(fields)):
                        fields[i]=fields[i].strip();
            ##            fields[i]=re.sub('\\',''',fields[i])
                        fields[i]=re.sub("'","\\'",fields[i])
                        fields[i]=re.sub("\"","\\\"",fields[i])
                    resultText+=tablename+u"[u'%s']={}\n"%fields[0];
                    for i in range(0,len(fields)):
                        if i< len(fieldsnames):
                            fieldname=fieldsnames[i];
                        else:
                            fieldname=u"Field#%d"%i;
                            fieldsnames.append(fieldname);
                            resultText+=tablename+u"[u'%s']={}\n"%fieldname;

                        resultText+= tablename+u"[u'%s']=u'%s'"%(fieldname,fields[i])+";\n"

            else:
                for line in lines[1:]:
                    line=line.strip();
                    fields=line.split("\t")
                    for i in range(len(fields)):
                        fields[i]=fields[i].strip();
            ##            fields[i]=re.sub('\\',''',fields[i])
                        fields[i]=re.sub("'","\\'",fields[i])
                        fields[i]=re.sub("\"","\\\"",fields[i])

                    for i in range(1,len(fields)):
                        if i< len(fieldsnames):
                            fieldname=fieldsnames[i];
                        else:
                            fieldname=u"Field#%d"%i;
                            fieldsnames.append(fieldname);
                            resultText+=tablename+u"[u'%s']={}\n"%fieldname;

                        resultText+= tablename+u"[u'%s'][u'%s']='%s'"%(fieldname,fields[0],fields[i])+";\n"

    return resultText

#-----------------------------------------
# Convert Arabic into Latin using a code representaton
#-----------------------------------------

def romanize(text,code="ISO"):
	textcoded=u"";
	if ArabicRomanizationTable.has_key(code):
		for c in text:
			if ArabicRomanizationTable[code].has_key(c):
				print "1";
				if explicated:
					textcoded+="("+c+")"
					print "2"
				textcoded+=ArabicRomanizationTable[code][c]
				print "3"
			else:
				textcoded+="*"
	else:
		textcoded=text;
		print "4"
	return textcoded;

def numberToLetters(text):
##    number=int(text);
    text=text.strip();
    import pyarabic.number
    ar=pyarabic.number.ArNumbers();
    return ar.int2str(text);

#---------------------------------
#
#LightStemming unsing Tashaphyne
#--------------------------------

def lightStemmer(text):
    result=[];
    als=tashaphyne.ArabicLightStemmer();
    word_list=als.tokenize(text)
    for word in word_list:
        listseg= als.segment(word);
##        print word.encode("utf8"),listseg
        affix_list=als.get_affix_list();
        for affix in affix_list:
            result.append({'word':word,'prefix':affix['prefix'],'stem':affix['stem'],
                           'suffix':affix['suffix'],'root':affix['root'],'type':'-'}
                          );

    return result;


def fullStemmer(text, lastmark):
	import qalsadi.analex 
	import asmai.anasem 
	import aranasyn.anasyn as arasyn	
	result=[];
	debug=False;
	limit=100
	analyzer=qalsadi.analex.analex()
	if lastmark=="0" or not lastmark:
		analyzer.disableAllowSyntaxLastMark();

	anasynt=arasyn.SyntaxAnalyzer();
	anasem=asmai.anasem.SemanticAnalyzer();	
	analyzer.set_debug(debug);
	analyzer.set_limit(limit);
	mode='all';
	if mode=='verb':
		result=analyzer.check_text_as_verbs(text);
	elif mode=='noun':
		result=analyzer.check_text_as_nouns(text);
	else:
		result=analyzer.check_text(text);
		result, synodelist=anasynt.analyze(result);
		result=anasem.analyze(result);			
		# the result contains objets
	return anasynt.decode(result);


def token_text(text):
    tasha=tashaphyne.ArabicLightStemmer();
    return tasha.tokenize(text);
##    if u'' in listword:listword.remove(u'');
##     listword;

def normalize(text):
    tasha=tashaphyne.ArabicLightStemmer();
    return tasha.normalize(text);
def justify_poetry(text):
    lines=text.splitlines();
    if u'' in lines: lines.remove(u"")
    rows=[];
    for line in lines:
        partlist=line.strip().split("\t");
        if u'' in partlist: partlist.remove(u"");
        if len(partlist)==2:
            rows.append(partlist);
    return rows;


def affixate(text):
    word_list=token_text(text);
    import generate
    if len(word_list)==0:
        return u'';
    else:
        for word in word_list:
            list_gen_words=generate.generate(word);
        return list_gen_words;



def wordtag(text):
    import naftawayh
    tagger=naftawayh.wordtag.WordTagger();
    word_list=token_text(text);

    if len(word_list)==0:
        return [];
    else:
        list_result=[];
        previous=u"";
        previous_tag = "";		
        for word in word_list:
            tag='';
            if tagger.is_stopword(word):tag='t';
            else:
                if tagger.is_noun(word):tag+='n';
                if tagger.is_verb(word):tag+='v';
                if tag in ("","nv"):
                    tag=tagger.context_analyse(previous, word, previous_tag)+"1";
            list_result.append({'word':word,'tag': tag});
            previous=word;
            previous_tag = tag;
        return list_result;


def inverse(text):
    word_list=token_text(text);

    if len(word_list)==0:
        return [];
    else:
        list_result=[];
        inter_list=[];
        for word in word_list:
            inter_list.append(word[::-1]);
        inter_list.sort();
        for word in inter_list:
##            result_list.append();
            list_result.append(word[::-1]);
        return list_result;


#----------------------------
# Convert lines into Latex list
# return Text
#----------------------------
def itemize(text):
    lines=text.splitlines()
    if u'' in lines: lines.remove(u'');
    resultText=""

    if len(lines)>1:
        resultText=u"\\begin{itemize}\n"
        for line in lines:
            resultText+=u'\\item '+line.strip()+u"\n";
        resultText+=u"\\end{itemize}\n"
    return resultText


#----------------------------
# Convert lines into Latex tabular
# return Text
#----------------------------
def tabulize(text):
    lines=text.splitlines()
    if u'' in lines: lines.remove(u'');
    resultText=""

    if len(lines)>1:
        length=len(lines[0].split("\t"));
        param="|c"*length+"|";
        resultText=u"\\begin{table}\n \\begin{tabular}{"+param+u"}\n";
        for line in lines:
            resultText+=u'\\hline '+" & ".join(line.split("\t"))+"\\"*2+"\n";
        resultText+=u"""\hline\n
                    \\label{mytab:table}\n
                    \\caption{mytab:table}\n
                    \\end{tabular}\n
                     \\end{table}\n
                    """
    return resultText

#----------------------------
# Convert lines into Latex tabular
# return Text
#----------------------------
def tabbing(text):
    lines=text.splitlines()
    if u'' in lines: lines.remove(u'');
    resultText=""

    if len(lines)>1:
        length=len(lines[0].split("\t"));
        param="|c"*length+"|";
        resultText=u"\\begin{tabbing}\n"
        resultText+="\hspace{4cm}\="*length+"\kill\n";
        for line in lines:
            resultText+=" \\> ".join(line.split("\t"))+"\\"*2+"\n";
        resultText+=u"""\end{tabbing}\n
                    """
    return resultText




def segmentLanguage(text):
    resultlist=[];
    if re.search(u"[\u0600-\u06ff]",text[0]):
        arabic=True;
    else:
        arabic=False;
    actual_text=u"";
    for  c in text:
        if re.search(u"[\u0600-\u06ff]",c):
            if arabic:
                actual_text+=c;
            else:
                resultlist.append(('latin',actual_text));
                arabic=True;
                actual_text=c;
        elif re.search(u"[\s\d\?,;:\!\(\)]",c):
                actual_text+=c;
        else:
            if arabic:
                i=len(actual_text);
                temp_text=u"";
                while not re.search(u"[\u0600-\u06ff]",actual_text[i:i+1]):
                    i-=1;
                temp_text=actual_text[i+1:];
                actual_text=actual_text[:i+1];
                resultlist.append(('arabic',actual_text));
                arabic=False;
                actual_text=temp_text+c;
            else:
                actual_text+=c;
    if arabic:
        resultlist.append(('arabic',actual_text));
    else:
        resultlist.append(('latin',actual_text));
    return resultlist;


def tashkeelText(text, lastmark=True):
	import tashkeel.tashkeel as ArabicVocalizer
	vocalizer=ArabicVocalizer.TashkeelClass();
	print "lastMark", lastmark
	if lastmark=="0":
		vocalizer.disableLastMark();
	vocalized_text=vocalizer.tashkeel(text);
	return vocalized_text;
def reducedTashkeelText(text):
	"""
	Reduce Harakat and vocalization from a vocalized text.
	@param text: a given vocalized text.
	@type text: unicode.
	@return : reduced text vocalization
	@rtype: unicode
	"""
	return araby.reduceTashkeel(text);
def showCollocations(text):
	"""
	Show collocations found in the text.
	The collocations is looked up from a data base extracted from a corpus.
	@param text: a given vocalized text.
	@type text: unicode.
	@return : the text have collocations quoted
	@rtype: unicode
	"""
	import tashkeel.tashkeel as ArabicVocalizer	
	vocalizer=ArabicVocalizer.TashkeelClass();
	vocalized_text=vocalizer.statTashkeel(text);
	return vocalized_text;

def extractNamed(text):
	"""
	Extract Named Enteties in the text.
	@param text: a given text.
	@type text: unicode.
	@return : the text have Named enteties quoted
	@rtype: unicode
	>>> extractNamed(u"قال خالد بن رافع  حدثني أحمد بن عنبر عن خاله");
	("خالد بن رافع"، "أحمد بن عنبر ")
	"""
	import pyarabic.named as named
	phrases=[];
	wordlist = araby.tokenize(text);
	positions= named.detectNamedPosition(wordlist);
	previousPos=0; # to keep the previous pos in the list
	for pos in positions:
		if len(pos)>=2:
			if pos[0]<=len(wordlist) and pos[1]<=len(wordlist):
				phrases.append((u' '.join(wordlist[previousPos:pos[0]]),''))
				phrases.append((u' '.join(wordlist[pos[0]: pos[1]+1]),'named'))
			previousPos=pos[1]+1
	#add the last part of the wordlist;
	phrases.append((u' '.join(wordlist[previousPos:]),''))
	# return phrases;
	newText="";
	for tuple in phrases:
		if tuple[1]=='named':
			newText+=" <span class='named'>%s</span> "%tuple[0];
		else:
			newText+=tuple[0];
	return newText;#u"<br>".join(phrases);

def extractNumbered(text):
	"""
	Extract number phrases in the text.
	@param text: a given text.
	@type text: unicode.
	@return : the text have number phrases quoted
	@rtype: unicode
	>>> extractNumber(u"وجدت خمسمئة وثلاثة وعشرين دينارا");
	وجدت خمسمئة وثلاثة وعشرين دينارا ")
	"""
	import pyarabic.number
	phrases=[];
	wordlist = araby.tokenize(text);
	positions= pyarabic.number.detectNumberPhrasesPosition(wordlist);
	previousPos=0; # to keep the previous pos in the list
	for pos in positions:
		if len(pos)>=2:
			if pos[0]<=len(wordlist) and pos[1]<=len(wordlist):
				phrases.append((u' '.join(wordlist[previousPos:pos[0]]),''))
				phrases.append((u' '.join(wordlist[pos[0]: pos[1]+1]),'named'))
			previousPos=pos[1]+1
	#add the last part of the wordlist;
	phrases.append((u' '.join(wordlist[previousPos:]),''))
	# return phrases;
	newText="";
	for tuple in phrases:
		if tuple[1]=='named':
			newText+=" <span class='named'>%s</span> "%tuple[0];
		else:
			newText+=tuple[0];
	return newText;#u"<br>".join(phrases);
	
def tashkeel2(text, lastmark):
	import tashkeel.tashkeel as ArabicVocalizer
	vocalizer=ArabicVocalizer.TashkeelClass();
	#print (u"lastMark %s"%lastmark).encode('utf8');
	if lastmark=="0" or not lastmark:
		vocalizer.disableLastMark();	
	vocalized_dict=vocalizer.tashkeelOuputHtmlSuggest(text);
	#print vocalized_dict
	return vocalized_dict;
	
def spellcheck(text, lastmark=None):
	import spellcheck.spellcheck as ArabicSpellchecker
	vocalizer=ArabicSpellchecker.SpellcheckClass();
	#print (u"lastMark %s"%lastmark).encode('utf8');
	vocalized_dict=vocalizer.spellcheckOuputHtmlSuggest(text);
	return vocalized_dict;

def Comparetashkeel(text):
	import tashkeel.tashkeel as ArabicVocalizer
	# the entred text is vocalized correctly
	correct_text=text;
	text=araby.stripTashkeel(text);
	vocalizer=ArabicVocalizer.TashkeelClass();
	vocalized_text=vocalizer.tashkeel(text);
	
	# compare voalized text with a correct text
	text1=correct_text;
	text2=vocalized_text;
	# remove collocations symboles
	text2=text2.replace("'","");
	text2=text2.replace("~","");
	
	#stemmer=tashaphyne.stemming.ArabicLightStemmer()
	list1=vocalizer.analyzer.tokenize(text1);
	list2=vocalizer.analyzer.tokenize(text2);
	print u":".join(list1).encode('utf8');
	print u":".join(list2).encode('utf8');
	correct=0;
	incorrect=0;
	total=len(list1);
	if len(list1)!=len(list2):
		print "lists haven't the same length";
	else:
		for i in range(total):
			if araby.vocalizedlike(list1[i],list2[i]):
				correct+=1;
			else:
				incorrect+=1;
	
	result=[vocalized_text,"correct:%0.2f%%"%round(correct*100.00/total,2),"incorrect:%0.2f%%"%round(incorrect*100.00/total,2),total]
	return result#correct*100/total;

def assistanttashkeel(text):
	import tashkeel.tashkeel as ArabicVocalizer
	vocalizer=ArabicVocalizer.TashkeelClass();
	vocalized_text=vocalizer.assistanttashkeel(text);
	return vocalized_text;
def randomText():
	import randtext
	
	return random.choice(randtext.textlist);
