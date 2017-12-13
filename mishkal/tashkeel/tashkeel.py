#!/usr/bin/python 
# -*- coding=utf-8 -*-
#---------------------------------------------------------------------
# Name:        tashkeel 
# Purpose:     Arabic automatic vocalization. # 
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com) 
# Created:     31-10-2011 
#  Copyright:   (c) Taha Zerrouki 2011 # Licence:     GPL 
#---------------------------------------------------------------------
"""
    Arabic Tashkeel Class
"""
import sys
sys.path.append('../lib')
sys.path.append('../')
import re
import pyarabic.araby as araby
import tashkeel_const
import qalsadi.analex
import aranasyn.anasyn 
import aranasyn.syn_const 
import asmai.anasem 
import maskouk.collocations as coll
import pyarabic.number
import pyarabic.named
import unknown_tashkeel
from operator import and_
from itertools import izip, count

# This global constant is used todefine where the vocazlizer don't vocalized uncertain words' ends
UNCERTAIN_TASHKEEL = False
# to debug program
debug = False
#~ debug = True
class TashkeelClass:
    """
        Arabic Tashkeel Class
    """
    def __init__(self):
        # to display internal messages for debugging
        #~debug = False
        # limit of words to vocalize, default value is 1000 words.
        self.limit = 1000
        
        #  set the option value to enable the Last mark on voaclize 
        # words in output
        # default value is True, can be disabled for debuging porpus
        self.enabled_last_mark = True
        
        # set the option to do statistical vocalization based 
        # on collocations
        # default value is True, can be disabled for debuging porpus
        #self.enabled_stat_tashkeel = False    
        self.enabled_stat_tashkeel = True   
            
        # set the option to show the collocations marks
        # default value is False, can be enabled for debuging porpus
        self.enabled_show_collocation_mark = False
        
        # set the option to use scoring teashkeel chosing.
        self.select_by_score_enabled = False
        # set the option to do syntaxic Analysis
        # default value is True, can be disabled for debuging porpus
        self.enabled_syntaxic_analysis = True

        # set the option to do allow ajusting voaclization result, 
        # for التقاء الساكنين
        # default value is True, can be disabled for debuging porpus
        self.enabled_ajust_vocalization = True        

        # set the option to do Semantic Analysis
        # default value is True, can be disabled for debuging porpus        
        self.enabled_semantic_analysis = True
        #~ self.enabled_semantic_analysis = False

        # enable the last mark (Harakat Al-I3rab) 
        self.allow_syntax_last_mark = True 

        # lexical analyzer
        self.analyzer = qalsadi.analex.Analex()
        self.analyzer.disable_allow_cache_use()
        #~ self.analyzer.enable_allow_cache_use()

        # syntaxic analyzer
        self.anasynt = aranasyn.anasyn.SyntaxAnalyzer()
        # semantic analyzer
        self.anasem = asmai.anasem.SemanticAnalyzer()        
        #set the lexical analzer debugging
        self.analyzer.set_debug(debug)
        #set the lexical analzer  word limit
        self.analyzer.set_limit(self.limit)
        #collocations dictionary for statistical tashkeel
        self.collo = coll.CollocationClass(self.enabled_show_collocation_mark)
        
        # unknown vocalizer for unrecognized words
        self.unknown_vocalizer = unknown_tashkeel.UnknownTashkeel()

    
    def set_limit(self, limit):
        """
        set the limit length of words to vocalize
        """
        self.limit = limit
        #set the lexical analzer  wrd limit
        self.analyzer.set_limit(self.limit)

    def enable_stat_tashkeel(self):
        """
        Enable the stat tasheel option.
        """
        self.enabled_stat_tashkeel = True
    def disable_stat_tashkeel(self):
        """
        disable the stat tasheel option.
        """
        self.enabled_stat_tashkeel = False

    def disable_cache(self):
        """
        disable the morphological use of cache.
        """
        self.analyzer.disable_allow_cache_use()

    def get_enabled_stat_tashkeel(self):
        """
        return the  the stat tasheel option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabled_stat_tashkeel
    def enable_show_collocation_mark(self):
        """
        Enable the show the collocation mark option.
        """
        self.enabled_show_collocation_mark = True
        self.collo.enable_show_delimiter()
    def disable_show_collocation_mark(self):
        """
        disable the show the collocation mark option.
        """
        self.enabled_show_collocation_mark = False
        self.collo.disable_show_delimiter()
    def get_show_collocation_mark(self):
        """
        return the  the show the collocation mark option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabled_show_collocation_mark
    def enable_last_mark(self):
        """
        Enable the last mark option.
        """
        self.enabled_last_mark = True
    def disable_last_mark(self):
        """
        disable the last mark vocalization  option.
        """
        self.enabled_last_mark = False
    def get_enabled_last_mark(self):
        """
        return the  the last mark vocalization option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabled_last_mark
    def enable_syntaxic_analysis(self):
        """
        Enable the syntaxic analysis option.
        """
        self.enabled_syntaxic_analysis = True
    def disable_syntaxic_analysis(self):
        """
        disable the syntaxic analysis option.
        """
        self.enabled_syntaxic_analysis = False
    def get_enabled_syntaxic_analysis(self):
        """
        return the  the syntaxic analysis option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabled_syntaxic_analysis
    def enable_semantic_analysis(self):
        """
        Enable the Semantic analysis option.
        """
        self.enabled_semantic_analysis = True
    def disable_semantic_analysis(self):
        """
        disable the Semantic analysis option.
        """
        self.enabled_semantic_analysis = False
    def get_enabled_semantic_analysis(self):
        """
        return the  the Semantic analysis option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabled_semantic_analysis
    def enable_ajust_vocalization(self):
        """
        Enable the Ajust Vocalization option.
        """
        self.enabled_ajust_vocalization = True
    def disable_ajust_vocalization(self):
        """
        disable the Ajust Vocalization option.
        """
        self.enabled_ajust_vocalization = False
    def get_enabled_ajust_vocalization(self):
        """
        return the  the Ajust Vocalization option value.
        @return: True if enabled, false else.
        @rtype: boolean.
        """
        return self.enabled_ajust_vocalization

    def full_stemmer(self, text):
        """
        Do the lexical, syntaxic  and semantic analysis of the text.
        @param text: input text.
        @type text: unicode.
        @return: syntaxic and lexical tags.
        rtype: list of list of stemmedSynWord class.
        """
        result = []
        result = self.analyzer.check_text(text)
        if self.get_enabled_syntaxic_analysis():
            result, synodelist = self.anasynt.analyze(result)
            # in this stpe we can't do semantic analysis without 
            # syntaxic analysis
            # we think it's can be done, 
            # To do: do semantic analysis without syntaxic one
            if self.get_enabled_semantic_analysis():
                result = self.anasem.analyze(result)    
        return result, synodelist

    def tashkeel(self, inputtext, suggestion = False, format_display = 'text'):
        """
        Vocalize the text and give suggestion to improve tashkeel by user.
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: dict of dict or text.
        """
        inputtext = self.pre_tashkeel(inputtext)
        #print "PreTashkeel", inputtext.encode('utf8')
        # The statistical tashkeel must return a text.
        #comment this after tests
        if self.get_enabled_stat_tashkeel():
            inputtext = self.stat_tashkeel(inputtext)
            #print "statTashkeel", inputtext.encode('utf8')
        #split texts into phrases to treat one phrase in time
        #~texts = self.analyzer.split_into_phrases(inputtext)
        texts = [inputtext, ]
        #~print u" \n".join(texts).encode('utf8')
        vocalized_text = u""
        previous = None
        output_suggest_list = []
        _chosen_list = []    
        suggests_list = []    
        for text in texts:
            #morpholigical analysis of text
            detailled_syntax, synodelist = self.full_stemmer(text)
            previous = None
            next_node = None
            pre_node = None
            previous_index = False
            previous_case_index = False
            previous_chosen_relation = False
            # reduce cases
            for current_index, word_cases_list, current_synode  in izip(count(),detailled_syntax, synodelist):
                #~ word_cases_list = detailled_syntax[current_index]
                if current_index - 1 >= 0 :
                    pre_node = synodelist[current_index-1]
                else:
                    pre_node =None
                if current_index + 1 < len(detailled_syntax) : 
                    next_node = synodelist[current_index+1]
                else:
                    next_node = None
                
                if previous_index  and previous_case_index:
                    previous = detailled_syntax[previous_index][previous_case_index]
                # reduce cases 
                self.__reduce_cases(word_cases_list, current_synode,  
                previous, pre_node, next_node)

            # choose tashkeel
            
            for current_index, word_cases_list, current_synode  in izip(count(),detailled_syntax, synodelist):
                #~ word_cases_list = detailled_syntax[current_index]
                if current_index - 1 >= 0 :
                    pre_node = synodelist[current_index-1]
                else:
                    pre_node =None
                if current_index + 1 < len(detailled_syntax) : 
                    next_node = synodelist[current_index+1]
                else:
                    next_node = None
                
                if previous_index  and previous_case_index:
                    previous = detailled_syntax[previous_index][previous_case_index]
                # choose a tashkeel 
                current_chosen_case_index = self.__choose_tashkeel(word_cases_list, current_synode,  
                previous, pre_node, next_node, previous_chosen_relation)
                # the new previous relation
                if previous:
                    current_chosen_relation = previous.get_next_relation(current_chosen_case_index)
                else:
                    current_chosen_relation = False
                    
                #~ print "relations", previous_chosen_relation, current_chosen_relation
                previous_chosen_relation = current_chosen_relation 
                #~ current_chosen_relation = previous.get_next_relation(current_chosen_case_index)
                
                #~print current_chosen_case_index, len(detailled_syntax[current_index]), current_index
                # ajust tanwin case
                # if previous and previous.canhave_tanwin() and not 
                # self.anasynt.is_related(previous, current_chosen):
                    # vocalized_text += "1"
                    # _chosen_list[len(_chosen_list)-1].ajust_tanwin() 
                # o ajust relation between words
                # if the actual word is transparent don't change the previous
                # add this to Sytaxic Analyser
                current_chosen = word_cases_list[current_chosen_case_index]
                #~ if not current_chosen.is_transparent():
                    #~ previous_index = current_index 
                    #~ previous_case_index = current_chosen_case_index 
                    #~ previous = current_chosen
                #~ if not current_chosen.is_transparent():
                previous_index = current_index 
                previous_case_index = current_chosen_case_index 
                previous = current_chosen
                _chosen_list.append(current_chosen)

                # create a suggest list
                #~ suggest = [item.get_vocalized() for item in word_cases_list]
                suggest = current_synode.get_vocalizeds()
                #~for item in word_cases_list:
                    #~# ITEM IS A stemmedSynWord instance
                    #~voc = item.get_vocalized()
                    #~suggest.append(voc)
                    # if item.canhave_tanwin():
                        # # يمكن لهذا أن يولد صيغا جديدة بها تنوي
                        # # في بعض الحالات قد لا يكون شيئا جديدا 
 # # نقارنه مع الكلمة السابقة منوّنة
# ومن ثمّ نقرر إضافتها أولا
                        # item.ajust_tanwin()
                        # vocTnwn = item.get_vocalized()
                        # if vocTnwn! = voc:
                            # suggest.append(vocTnwn)
                #~ suggest = list(set(suggest))
                #~ suggest.sort()
                suggests_list.append(suggest)
        output_suggest_list = []
        #create texts from chosen cases
        privous_order = -1
        previous = -1
        for i, current_chosen in enumerate(_chosen_list):
            voc_word = _chosen_list[i].get_vocalized()
            if not voc_word:
                voc_word = _chosen_list[i].get_word()
            #print "uuu", _chosen_list[i].get_semivocalized().encode('utf8')
            #print _chosen_list[i]
            #print "**", voc_word.encode('utf8')
            semivocalized = _chosen_list[i].get_semivocalized()
            #word without inflection mark
            inflect = u":".join([_chosen_list[i].get_type() , _chosen_list[i].get_tags_to_display()] ) 
            if previous >= 0:
                relation = _chosen_list[i].get_previous_relation(_chosen_list[previous].get_order())
            else: 
                relation = 0
            #get the title of relation
            relation = aranasyn.syn_const.DISPLAY_RELATION.get(relation, "")  
            #get the rule number
            selection_rule = _chosen_list[i].get_rule()  
            #ToDo
            # Add uncertain cases
            # if the selection is not sure, we take semivocalized only
            if  UNCERTAIN_TASHKEEL and selection_rule > 30:
                voc_word =   semivocalized                    
            # omit the last haraka if the option LastMark is False
            if not self.get_enabled_last_mark():
                vocalized_text = u" ".join([vocalized_text, self.display(voc_word, format_display)])
            else:
                #semivocalized 
                vocalized_text = u" ".join([vocalized_text, self.display(semivocalized, format_display)])
            output_suggest_list.append({'chosen':voc_word, 'semi':semivocalized, 
            'suggest':u";".join(suggests_list[i]), 'inflect':inflect, "link":relation, 'rule':selection_rule})
            # save the current chosen as a previous
            previous = i

        # correct the resulted text to ajust some case of consonant neighbor
        #معالجة حالات التقاء الساكنين
        if self.get_enabled_ajust_vocalization():
            vocalized_text = self._ajust_vocalized_result(vocalized_text)
        if suggestion:
            output_suggest_list = self.ajust_vocalized_suggestion(output_suggest_list)
            return output_suggest_list
        else:
            return vocalized_text

    def tashkeel_ouput_html_suggest(self, text):
        """
        Vocalize the text and give suggestion to improve tashkeel by user.
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: dict of dict.
        """
        return self.tashkeel(text, suggestion = True, format_display = "html")
    def tashkeel_output_text(self, text):
        """
        Vocalize the text witthout suggestion
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: text.
        """
        return self.tashkeel(text, suggestion = False, format_display = "text")
    def _ajust_vocalized_result(self, text):
        """
        Ajust the resulted text after vocalization to correct some case 
        like 'meeting of two queiscents = ألتقاء الساكنين'
        @param text: vocalized text
        @type text: unicode
        @return: ajusted text.
        @rtype: unicode
        """
        # min = > mina
        text = re.sub(ur'\sمِنْ\s+ا', u' مِنَ ا', text)
        # man = > mani
        text = re.sub(ur'\sمَنْ\s+ا', u' مَنِ ا', text)
        #An = > ani
        text = re.sub(ur'\sعَنْ\s+ا', u' عَنِ ا', text)
        #sukun + alef = > kasra +alef
        text = re.sub(ur'\s%s\s+ا'%araby.SUKUN, u' %s ا' % araby.SUKUN, text)
        #ajust pounctuation
        text = re.sub(ur" ([.?!, :)”—]($| ))", ur"\1", text)
        #binu = > bin 
        # temporary, to be analysed by syntaxical analyzer
        text = re.sub(ur'\sبْنُ\s', u' بْن ', text)        
        # # # اختصارات مثل حدثنا إلى ثنا وه تكثر في كتب التراث
        # text = re.sub(ur'\seثِنَا\s', u' ثَنَا ', text)        
        return text

    def ajust_vocalized_suggestion(self, _suggest_list):
        """
        Ajust the resulted text after vocalization to correct some case 
        like 'meeting of two queiscents = ألتقاء الساكنين'
        @param text: _suggest_list
        @type text: list of dict of unicode
        @return: _suggest_list.
        @rtype: list of dict of unicode
        """
        for i in range(len(_suggest_list)-1):
            if _suggest_list[i]['chosen'] in (u'مَنْ', u'مِنْ', u'عَنْ'):
                if i+1 < len(_suggest_list) and \
                _suggest_list[i+1].has_key('chosen') \
                and _suggest_list[i+1]['chosen'].startswith(araby.ALEF):
                    if _suggest_list[i]['chosen'] == u'مِنْ':
                        _suggest_list[i]['chosen'] = u'مِنَ'
                    elif _suggest_list[i]['chosen'] == u'عَنْ':
                        _suggest_list[i]['chosen'] = u'عَنِ'
                    elif _suggest_list[i]['chosen'] == u'مَنْ':
                        _suggest_list[i]['chosen'] = u'مَنِ'
            # if _suggest_list[i]['chosen'] == u'بْنُ':
                # _suggest_list[i]['chosen'] = u'بْن'
        return _suggest_list

    def display(self, word, format_display = "text"):
        """
        format the vocalized word to be displayed on web interface.
        @param word: input vocalized word.
        @type word: unicode.
        @return: html code.
        rtype: unicode.
        """
        format_display = format_display.lower()
        if format_display == "html":
            return u"<span id='vocalized' class='vocalized'>%s</span>" % word
        elif format_display == 'text':
            return word
        else:
            return word

    def assistanttashkeel(self, text):
        """
        Vocalize the text.
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: unicode.
        """    
        detailled_syntax = self.full_stemmer(text)
        vocalized_text = u""

        for word_analyze_list in detailled_syntax:
            # o ajust relation between words 
            #previous = word_stemming_dict
            for item in word_analyze_list:
                voc = item.get_vocalized()
                #~vocalized_text = u"".join([vocalized_text, voc])
                vocalized_text = u" ".join([vocalized_text, voc])
        return vocalized_text

    def pre_tashkeel(self, text):
        """
        Vocalize the text by evident cases and by detecting numbers clauses
        @param text: input text.
        @type text: unicode.
        @return: statisticlly vocalized text.
        rtype: unicode.
        """
        # get the word list
        # اختصارات مثل حدثنا إلى ثنا وه تكثر في كتب التراث
        for abr in tashkeel_const.CorrectedTashkeel.keys():
            text = re.sub(ur"\s%s\s"%abr, ur" %s " % \
            tashkeel_const.CorrectedTashkeel[abr], text)
        wordlist = self.analyzer.tokenize(text)
        prevocalized_list = pyarabic.number.pre_tashkeel_number(wordlist)
        #prevocalized_list = wordlist
        #Todo ajust prevocalization of named enteties
        #if len(prevocalized_list) != len(wordlist):
        #    print "nb", u"+".join(prevocalized_list)
        #prevocalized_list = pyarabic.named.pretashkeel_named(prevocalized_list)
        #print "nmd", u"@".join(prevocalized_list)
        return u" ".join(prevocalized_list)


    def stat_tashkeel(self, text):
        """
        Vocalize the text by statistical method according to the collocation dictionary
        @param text: input text.
        @type text: unicode.
        @return: statisticlly vocalized text.
        rtype: unicode.
        """
        text = self.collo.lookup4long_collocations(text)

        # get the word list
        wordlist = self.analyzer.tokenize(text)
        # use a list as a stack, 
        # give two element from the end.
        # test the tow elements if they are collocated, 
        # if collocated return the vocalized text
        # if else, delete the last element, and return the other to the list.
        newlist, taglist = self.collo.lookup(wordlist)
        #todo: return a text from the statistical tashkeel
        return  u" ".join(newlist)


    # new version of choose tashkeel 
    # first we use indexes instead of stemmedsynword object
    #~ def __choose_tashkeel_algo2(self, caselist, previous_chosen_case = None,
    def __choose_tashkeel(self, caselist, current_synode, previous_chosen_case = None,
     pre_node = None, next_node = None, previous_chosen_relation = False):
        """
        Choose a tashkeel for the current word, according to the previous one.
        A new algorithm
        @param : list of steming result of the word.
        @type caselist: list of stemmedSynword
        @param : the choosen previous word stemming.
        @type previous_chosen_case:stemmedSynwordhg 
        @return: the choosen stemming of the current word.
        @rtype:stemmedSynword.
        """
        
        chosen = None
        chosen_index = False
        rule = 0
        previous = previous_chosen_case
        if previous:
              pre_relation = 0 ; #_chosen_list[i].get_previous_relation(_chosen_list[previous].get_order());
        else:
            pre_relation = 0    
        if next_node:
            next_chosen_indexes = next_node.get_chosen_indexes()
        else:
            next_chosen_indexes = None            
        #~ debug = True
        # How to choose a vocalized case
        # and lets other methods to choose by semantic and syntaxic
        # choose a case is a stop, word and has next relation
        # browse the list by indexes
        #~ indxlist = range(len(caselist))
        # get the chosen indexes from the current synode
        # which allow to handle previous and nexts and make other analysis
        indxlist = current_synode.get_chosen_indexes()
        
        # get all the indexes in the current cases list
        tmplist = []
        if len(indxlist) == 1 : 
            if caselist[0].is_unknown():
                caselist[0].set_vocalized(self.unknown_vocalizer.lookup(caselist[0].get_word()))
                rule = 102
            else:
                rule = 101
        
        if not rule:
            # order indexes list by word frequency
            indxlist = sorted(indxlist, key=lambda x:caselist[x].get_freq())
        # initial cases
        if not rule and (not previous or previous.is_initial()):
            tmplist = filter(lambda x: (caselist[x].is_stopword() or
                     (caselist[x].is_marfou3() and not caselist[x].is_passive())
                     or caselist[x].is_past() ), indxlist)
            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, rule)
            # and lets other methode to choices by semantic and syntaxic
            # select all cases with semantic relations
        if not rule and self.get_enabled_semantic_analysis():            
            tmplist = filter(lambda x: self.anasem.is_related(previous, caselist[x]) or caselist[x].has_sem_next(next_chosen_indexes), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, rule)

            # two semantic relations
            tmplist = filter(lambda x: self.anasem.is_related(previous, caselist[x]) and caselist[x].has_sem_next(next_chosen_indexes), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 4)
            

            # one semantic relations from previous
            tmplist = filter(lambda x: self.anasem.is_related(previous, caselist[x]) and caselist[x].has_next(next_chosen_indexes), indxlist)
            
            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 5)


            # one semantic relations from next
            tmplist = filter(lambda x: self.anasynt.is_related(previous, caselist[x]) and caselist[x].has_sem_next(next_chosen_indexes), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 6)

            # select stopword
        if not rule:
            tmplist = filter(lambda x:  caselist[x].is_stopword(), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 3)

            # syntaxic
            # select stopword

        if not rule:           
            tmplist = filter(lambda x:  caselist[x].is_stopword() and (self.anasynt.is_related(previous, caselist[x])
                                     and caselist[x].has_next(next_chosen_indexes)) , indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 41)

        if not rule:           
            tmplist = filter(lambda x:  caselist[x].is_stopword() and caselist[x].has_next(next_chosen_indexes) , indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 10)

        #~ if not rule:           
            #~ tmplist = filter(lambda x:  caselist[x].is_stopword()  and self.anasynt.is_related(previous, caselist[x]) , indxlist)
            #~ # if indexes list is empty, the current indexes list is reloaded, and no change
            #~ if tmplist:
                #~ indxlist = tmplist  
                #~ if len(indxlist) == 1 : rule = 42
            #~ if debug: print 10,rule, u", ".join([caselist[x].get_vocalized() for x in indxlist]).encode('utf8')

            # get all the indexes in the current cases list
        if not rule and self.get_enabled_syntaxic_analysis():
            # select all cases with syntaxic relations
            tmplist = filter(lambda x: (self.anasynt.is_related(previous, caselist[x]) and caselist[x].has_next(next_chosen_indexes)), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 11)
      
        if not rule and  self.get_enabled_syntaxic_analysis():
            tmplist = filter(lambda x: (self.anasynt.is_related(previous, caselist[x])), indxlist)
           

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 12)
        #
        if not rule and  self.get_enabled_syntaxic_analysis():
            tmplist = filter(lambda x: (self.anasynt.is_related(previous, caselist[x]) and self.anasynt.are_compatible_relations(previous_chosen_relation, previous.get_next_relation(x)) ), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 13)
        # select only compatible relations with previous relations
        # reduces cases if the previous chosen relation is not compatible with actual relations
        
        # like قال هذا الرجل، 
        #قال هذا 
        #~ give us a verb subject,
         #~ then the relation between
         #~ هذا الرجل 
        #~ must be raf3 substitution

        if not rule and  self.get_enabled_syntaxic_analysis():
            tmplist = filter(lambda x: (self.anasynt.is_related(previous, caselist[x]) and self.anasynt.are_compatible_relations(previous_chosen_relation, previous.get_next_relation(x)) ), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 13)

            # Default cases selection 
            # get all the indexes in the current cases list
        if not rule and self.get_enabled_syntaxic_analysis():
            # select all cases with syntaxic relations
            tmplist = filter(lambda x: caselist[x].has_next(next_chosen_indexes), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 14)
        # Get relations of non mansoub with a has_previous
        # Previlege relations of Raf3 or Jar than the Nasb if there are many relations
        if not rule and self.get_enabled_syntaxic_analysis():
            # select all cases with syntaxic relations
            tmplist = filter(lambda x: (self.anasynt.is_related(previous, caselist[x]) and caselist[x].is_noun() and not caselist[x].is_mansoub()), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 17)        
        if not rule:
            # select all cases with tanwin
            if (next_node and next_node.is_break()) or not next_node:
                tmplist = filter(lambda x: caselist[x].is_tanwin() or not caselist[x].is_noun() , indxlist)

                indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 15)

            #select default

        if not rule:
            # select cases with the max frequency
            # first get max freq
            maxfreq = 0
            maxfreq = max([caselist[x].get_freq() for x in indxlist])
            tmplist = filter(lambda x: caselist[x].get_freq() == maxfreq, indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 31)
        #~ conditions = [
        #~ { "rule":30, "cond":[("is_stopword",True), ],} ,
        #~ { "rule":32, "cond":[("is_noun",True),  ("is_mansoub",True),],} ,
        #~ { "rule":33, "cond":[("is_verb",True), ("is_passive",False),],} ,
        #~ { "rule":34, "cond":[("is_verb",True), ("is_marfou3",True),],} ,
        #~ { "rule":34, "cond":[("is_verb",True), ("is_past",True),],} ,
        #~ { "rule":35, "cond":[("is_verb",True), ("is3rdperson",True),],} ,
        #~ { "rule":36, "cond":[("is_verb",True), ("is1stperson",True),],} ,
        #~ ]
        #~ if not rule:            
            #~ for cond in conditions:
                #~ tmplist = [] 
                #~ condlist = cond['cond']             
                #~ for x in indxlist:
                    #~ # join all tests
                    #~ criteria = [getattr(caselist[x], k)() == v  for k, v in condlist] 
                    #print criteria
                    #~ if reduce(and_, criteria):
                        #~ tmplist.append(x)
                #if debug: print rule,rule, u", ".join([caselist[x].get_vocalized() for x in indxlist]).encode('utf8')
                #~ if tmplist:
                    #~ indxlist = tmplist               
                    #~ if len(indxlist) == 1 :
                        #~ rule = cond.get('rule',0)
                        #~ break
        if not rule:                
            # exode Dual cases
            # use to avoid dual cases like من الفلاحَين instead of من الفلاحِين
            tmplist = filter(lambda x: ( caselist[x].is_noun() and  not caselist[x].is_dual()), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 32)

        if not rule:                
            # select mansoub noun
            tmplist = filter(lambda x: ( caselist[x].is_noun() and  caselist[x].is_mansoub()), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 33)

        #~ if not rule:                
            #~ # select plural noun
            #~ tmplist = filter(lambda x: ( caselist[x].is_noun() and  caselist[x].is_plural()), indxlist)

            #~             indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, rule)

        if not rule:                
            # select active voice
            tmplist = filter(lambda x: ( caselist[x].is_verb() and not caselist[x].is_passive()), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 35)

        if not rule:                        
            # select present marfou3 or past
            tmplist = filter(lambda x: ( caselist[x].is_verb() and (caselist[x].is_marfou3() or caselist[x].is_past())), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 36)
        if not rule:            
            # select 3rd person
            tmplist = filter(lambda x: ( caselist[x].is_verb() and caselist[x].is3rdperson()), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 37)

        if not rule:            
            # select 1st person
            tmplist = filter(lambda x: ( caselist[x].is_verb() and caselist[x].is1stperson()), indxlist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 38)
                                        
        # select the first case if there one or many
        chosen_index =  indxlist[0]
        chosen = caselist[chosen_index]
        if not rule: rule = 100
        if debug: print 100,rule, u", ".join([caselist[x].get_vocalized() for x in indxlist]).encode('utf8')
         
        
        # set the selection rule to dispaly how tahskeel is selected
        chosen.set_rule(rule)
        return chosen.get_order() 
            

    # new version of choose tashkeel 
    # first we use indexes instead of stemmedsynword object
    #~ def __choose_tashkeel_algo2(self, caselist, previous_chosen_case = None,
    def __reduce_cases(self, caselist, current_synode, previous_chosen_case = None,
     pre_node = None, next_node = None):
        """
        reduce  possible cases for the current word, according to the previous one and nexts.
        A new algorithm
        @param : list of steming result of the word.
        @type caselist: list of stemmedSynword
        @param : the choosen previous word stemming.
        @type previous_chosen_case:stemmedSynwordhg 
        @return: the choosen stemming of the current word.
        @rtype:stemmedSynword.
        """
        
        rule = 0
        debug = False
        if next_node:
            next_chosen_indexes = next_node.get_chosen_indexes()
        else:
            next_chosen_indexes = None            
        #~ debug = True
        # How to choose a vocalized case
        # and lets other methode to choices by semantic and syntaxic
        # choose a case is a stop, word and has next relation
        # browse the list by indexes
        #~ indxlist = range(len(caselist))
        # get the chosen indexes from the current synode
        # which allow to handle previous and nexts and make other analysis
        indxlist = current_synode.get_chosen_indexes()
        # get all the indexes in the current cases list
        tmplist = []
        rule = 0
        # syntaxic
        # choose all tanwin cases before breaks
        if not next_node or (next_node and next_node.is_break()):
            #~ tmplist = filter(lambda x:  (caselist[x].is_tanwin() and caselist[x].has_next(next_chosen_indexes)) or not caselist[x].is_noun()  , indxlist)
            #~ tmplist = filter(lambda x:  caselist[x].is_tanwin() or caselist[x].is_defined() or not caselist[x].is_noun()  , indxlist)
            #~ tmplist = filter(lambda x:  not(caselist[x].is_tanwin() and not caselist[x].is_defined())  , indxlist)
            # if indexes list is empty, the current indexes list is reloaded, and no change
            if tmplist:
                indxlist = tmplist
        #~ if not rule and self.get_enabled_semantic_analysis():            
            #~ tmplist = filter(lambda x: caselist[x].has_sem_next(next_chosen_indexes) or caselist[x].has_sem_previous(), indxlist)
            #~ # if indexes list is empty, the current indexes list is reloaded, and no change
            #~ if tmplist:
                #~ indxlist = tmplist
#~ 
            #~ # if there are many semantic relations or non one, we use frequency to choose the
            #~ # most frequent word to be selected
                #~ if len(indxlist) == 1 : rule = 2
            #~ if debug: print 2,rule, u", ".join([caselist[x].get_vocalized() for x in indxlist]).encode('utf8')

        # select stopword
        if next_node:
            
            tmplist = filter(lambda x:  caselist[x].is_stopword() and (caselist[x].has_next(next_chosen_indexes) 
                        ), indxlist)
            #~ tmplist = filter(lambda x:  caselist[x].is_stopword() and (caselist[x].has_next(next_chosen_indexes) 
                        #~ or caselist[x].has_previous()), indxlist)
            # if indexes list is empty, the current indexes list is reloaded, and no change
            if tmplist:
                indxlist = tmplist  
                if len(indxlist) == 1 : rule = 3
            if debug: print 3,rule, u", ".join([caselist[x].get_vocalized() for x in indxlist]).encode('utf8')
 
            # get all the indexes in the current cases list
        #~ if not rule and self.get_enabled_syntaxic_analysis():
            #~ # select all cases with syntaxic relations
            #~ tmplist = filter(lambda x: caselist[x].has_next(next_chosen_indexes) or caselist[x].has_previous(), indxlist)
            #~ # if indexes list is empty, the current indexes list is reloaded, and no change
            #~ if tmplist:
                #~ indxlist = tmplist
                #~ if len(indxlist) == 1 : rule = 13
            #~ if debug: print 13,rule, u", ".join([caselist[x].get_vocalized() for x in indxlist]).encode('utf8')
                    #~ 
        # reduce the list of cases
        current_synode.set_chosen_indexes(indxlist)

def _get_indexlist_and_rule(tmplist, indexlist, caselist, rule):
    """
    Just a macro to avoid repetetion
    if tmplist is not empty, change indexlist,
    if the indexlist has one element, the rule is applyed
    """
    debug = False
    #~ debug = True
    #~ if tmplist is not empty, change indexlist,

    if tmplist:
       indexlist = tmplist

    #~ if the indexlist has one element, the rule is applied
    applied_rule = rule if len(indexlist) == 1 else 0
    # if debug, display the 
    if debug: 
        print "choose tashkeel", rule,applied_rule, u", ".join([caselist[x].get_vocalized() for x in indexlist]).encode('utf8')
    return indexlist, applied_rule


def mainly():
    """
    main test
    """
    print "test"        
    vocalizer = TashkeelClass()
    # text = u"""تجف أرض السلام بالسلام الكبير.    مشى على كتاب السلام.
    # جاء الولد السمين من قاعة القسم الممتلئ"""
    text = u"يعبد الله تطلع الشمس"
    voc = vocalizer.tashkeel(text)
    print voc.encode('utf8')
if __name__ == "__main__":
    mainly()

