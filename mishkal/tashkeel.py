#!/usr/bin/python
# -*- coding=utf-8 -*-
# ---------------------------------------------------------------------
# Name:        tashkeel
# Purpose:     Arabic automatic vocalization. #
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011 # Licence:     GPL
# ---------------------------------------------------------------------
"""
    Arabic Tashkeel Class
"""
import sys
import re
import logging
from operator import and_

import pyarabic.araby as araby
import qalsadi.analex
import sylajone.anasyn
import sylajone.syn_const
import asmai.anasem
import maskouk.collocations as coll
import pyarabic.number
import pyarabic.named

izip=zip
from itertools import count
import mysam.tagmaker
from . import unknown_tashkeel
from . import tashkeel_const
#~ import unknown_tashkeel
#~ import tashkeel_const

sys.path.append('../lib')
sys.path.append('../')

# This global constant is used todefine where the vocazlizer don't vocalized uncertain words' ends
UNCERTAIN_TASHKEEL = False
# to debug program
debug = False
# ~ debug = True


class TashkeelClass:
    """
        Arabic Tashkeel Class
    """
    def __init__(self, mycache_path=False):
        # configure logging       
        logging.basicConfig(level=logging.ERROR)
        self.logger = logging.getLogger(__name__)

        # limit of words to vocalize, default value is 1000 words.
        self.limit = 1000

        #  set the option value to enable the Last mark on vocalize
        # words in output
        # default value is True, can be disabled for debugging purposes
        self.enabled_last_mark = True

        # set the option to do statistical vocalization based
        # on collocations
        # default value is True, can be disabled for debugging purposes
        # self.enabled_stat_tashkeel = False
        self.enabled_stat_tashkeel = True

        # set the option to display logger on stdout
        # default value is False, can be enabled for debugging purposes
        self.enabled_verbose = False

        # set the option to show the collocations marks
        # default value is False, can be enabled for debugging purposes
        self.enabled_show_collocation_mark = False

        # set the option to use scoring teashkeel chosing.
        self.select_by_score_enabled = False

        # set the option to do syntaxic Analysis
        # default value is True, can be disabled for debugging purposes
        self.enabled_syntaxic_analysis = True

        # set the option to do allow adjusting vocalization result,
        # for التقاء الساكنين
        # default value is True, can be disabled for debugging purposes
        self.enabled_ajust_vocalization = True

        # set the option to do Semantic Analysis
        # default value is True, can be disabled for debugging purposes
        self.enabled_semantic_analysis = True
        # ~ self.enabled_semantic_analysis = False

        # enable the last mark (Harakat Al-I3rab)
        self.allow_syntax_last_mark = True

        # lexical analyzer

        self.analyzer = qalsadi.analex.Analex(cache_path=mycache_path)
        #~ self.logger.info("Cache Path cache %s"%self.analyzer.cache.DB_PATH)
        #~ self.logger.info("Cache Path cache %s"%self.analyzer.cache.db.path)
        self.analyzer.disable_allow_cache_use()
        #~ self.analyzer.enable_allow_cache_use()

        # syntaxic analyzer
        self.anasynt = sylajone.anasyn.SyntaxAnalyzer(cache_path = mycache_path)
        self.anasynt.disable_allow_cache_use()
        
        # to disable the training when do Tashkeel
        self.syntax_train_enabled = False

        # semantic analyzer
        self.anasem = asmai.anasem.SemanticAnalyzer(cache_path = mycache_path)
        #self.anasem.disable_allow_cache_use()
        
        self.analyzer.set_debug(debug)
        # set the lexical analzer  word limit
        self.analyzer.set_limit(self.limit)

        # collocations dictionary for statistical tashkeel
        self.collo = coll.CollocationClass(self.enabled_show_collocation_mark)

        # unknown vocalizer for unrecognized words
        self.unknown_vocalizer = unknown_tashkeel.UnknownTashkeel()



    def set_limit(self, limit):
        """
        set the limit length of words to vocalize
        """
        self.limit = limit
        # set the lexical analzer  wrd limit
        self.analyzer.set_limit(self.limit)

    def enable_stat_tashkeel(self):
        """
        Enable the stat tasheel option.
        """
        self.enabled_stat_tashkeel = True

    def enable_syn_train(self):
        """
        Enable the syntaxique relation extraction from a vocalized text
        """
        self.anasynt.syntax_train_enabled = True

        # in this case we should use fully_vocalized_input text
        self.analyzer.enable_fully_vocalized_input()

    def disable_stat_tashkeel(self):
        """
        disable the stat tasheel option.
        """
        self.enabled_stat_tashkeel = False

    def enable_verbose(self):
        """
        enable logger
        """
        self.enabled_verbose = True

    def disable_cache(self):
        """
        disable the morphological use of cache.
        """
        self.analyzer.disable_allow_cache_use()
        self.anasynt.disable_allow_cache_use()

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

        #~ print "tashkeel6", len(result), len(araby.tokenize(text)), text.encode('utf8')
        for syndl in  result:
            self.logger.debug("Syn len before syntax: %s",repr(len(syndl)))            
        if self.get_enabled_syntaxic_analysis():
            result, synodelist = self.anasynt.analyze(result)
            #for synd in synodelist:
                #self.logger.debug(u"33 %s", repr(synd))
            # in this stpe we can't do semantic analysis without 
            # syntaxic analysis
            # we think it's can be done,
            # To do: do semantic analysis without syntaxic one
            for syndl in  result:
                self.logger.debug("Syn len: %s",repr(len(syndl)))            
                
                for synd in syndl:
                    self.logger.debug("Syn sem next before: %s",repr(synd.get_sem_next()))
                    self.logger.debug("Syn next before: %s",repr(synd.get_next()))            
            if self.get_enabled_semantic_analysis():
                result = self.anasem.analyze(result)

            for syndl in  result:
                for synd in syndl:
                    self.logger.debug("Syn sem next: %s",repr(synd.get_sem_next()))
                    self.logger.debug("Syn next: %s",repr(synd.get_next()))                 
        return result, synodelist

    def tashkeel(self, inputtext, suggestion=False, format_display='text'):
        """
        Vocalize the text and give suggestion to improve tashkeel by user.
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: dict of dict or text.
        """
        # ~ print "tashkeel 10", inputtext.encode('utf8')
        inputtext = self.pre_tashkeel(inputtext)
        # print "PreTashkeel", inputtext.encode('utf8')
        # The statistical tashkeel must return a text.
        # comment this after tests
        # ~ print "tashkeel 9", inputtext.encode('utf8')
        if self.get_enabled_stat_tashkeel():
            inputtext = self.stat_tashkeel(inputtext)
            self.logger.debug("stat tashkeel %s", inputtext)
        # split texts into phrases to treat one phrase in time
        # ~texts = self.analyzer.split_into_phrases(inputtext)
        texts = [inputtext, ]
        vocalized_text = u""
        previous = None
        output_suggest_list = []
        _chosen_list = []
        suggests_list = []
        for text in texts:
            # morpholigical analysis of text
            detailled_syntax, synodelist = self.full_stemmer(text)
            #self.logger.debug("List of synodes List **********")
            #for syno in synodelist:
                #self.logger.debug("Synode : %s",repr(syno))

                                     
            previous = None
            next_node = None
            pre_node = None
            previous_index = False
            previous_case_index = False
            previous_chosen_relation = False
            # reduce cases
     
            self.logger.debug("List of synodes **********")
            for current_index, word_cases_list, current_synode  in list(izip(count(),detailled_syntax, synodelist)):
                #~ word_cases_list = detailled_syntax[current_index]
                if current_index - 1 >= 0 :
                    pre_node = synodelist[current_index-1]
                else:
                    pre_node = None
                if current_index + 1 < len(detailled_syntax) : 
                    next_node = synodelist[current_index+1]
                else:
                    next_node = None

                if previous_index and previous_case_index:
                    previous = detailled_syntax[previous_index][previous_case_index]
                # reduce cases
                self.__reduce_cases(
                    word_cases_list, current_synode,
                    previous, pre_node, next_node
                )

            # choose tashkeel

            for current_index, word_cases_list, current_synode  in list(izip(count(),detailled_syntax, synodelist)):
                #~ word_cases_list = detailled_syntax[current_index]
                if current_index - 1 >= 0 :
                    pre_node = synodelist[current_index-1]

                else:
                    pre_node = None
                if current_index + 1 < len(detailled_syntax):
                    next_node = synodelist[current_index + 1]
                else:
                    next_node = None

                if previous_index and previous_case_index:
                    previous = detailled_syntax[previous_index][previous_case_index]
                # choose a tashkeel
                current_chosen_case_index = self.__choose_tashkeel(
                    word_cases_list, current_synode, previous,
                    pre_node, next_node, previous_chosen_relation
                )
                # the new previous relation
                if previous:
                    current_chosen_relation = previous.get_next_relation(current_chosen_case_index)
                else:
                    current_chosen_relation = False

                # ~ print "relations", previous_chosen_relation, current_chosen_relation
                previous_chosen_relation = current_chosen_relation
                # ~ current_chosen_relation = previous.get_next_relation(current_chosen_case_index)

                current_chosen = word_cases_list[current_chosen_case_index]

                previous_index = current_index
                previous_case_index = current_chosen_case_index
                previous = current_chosen
                _chosen_list.append(current_chosen)

                # create a suggest list
                # ~ suggest = [item.get_vocalized() for item in word_cases_list]
                suggest = current_synode.get_vocalizeds()
                suggests_list.append(suggest)
        output_suggest_list = []
        # create texts from chosen cases
        privous_order = -1
        previous = -1
        for i, current_chosen in enumerate(_chosen_list):
            voc_word = _chosen_list[i].get_vocalized()
            if not voc_word:
                voc_word = _chosen_list[i].get_word()
            semivocalized = _chosen_list[i].get_semivocalized()
            # word without inflection mark
            inflect = u":".join([_chosen_list[i].get_type(), _chosen_list[i].get_tags_to_display()])
            # Create a special tag
            mytagmaker = mysam.tagmaker.tagMaker()
            mytagmaker.encode(_chosen_list[i].get_tags().split(':'))
            mytagmaker.encode(_chosen_list[i].get_type().split(':'))
            #~ print(_chosen_list[i].get_tags().split(':'))
            if self.enabled_verbose:
                self.logger.info("TaharZe Tags to display '%s' and tagmaker =='%s'", _chosen_list[i].get_tags(), str(mytagmaker))

            inflect = u"[%s]{%s}" % (str(mytagmaker), mytagmaker.inflect()) + "<br/>" + inflect
            if previous >= 0:
                relation = _chosen_list[i].get_previous_relation(_chosen_list[previous].get_order())
            else:
                relation = 0
            # get the title of relation
            relation = sylajone.syn_const.DISPLAY_RELATION.get(relation, "")
            # get the rule number
            selection_rule = _chosen_list[i].get_rule()
            # ToDo
            # Add uncertain cases
            # if the selection is not sure, we take semivocalized only
            if UNCERTAIN_TASHKEEL and selection_rule > 30:
                voc_word = semivocalized
            # omit the last haraka if the option LastMark is False
            if not self.get_enabled_last_mark():
                vocalized_text = u" ".join([vocalized_text, self.display(semivocalized, format_display)])
            else:
                # semivocalized
                vocalized_text = u" ".join([vocalized_text, self.display(voc_word, format_display)])
            output_suggest_list.append({
                'chosen': voc_word,
                'semi': semivocalized,
                'suggest': u";".join(suggests_list[i]),
                'inflect': inflect,
                "link": relation,
                'rule': selection_rule
            })
            # save the current chosen as a previous
            previous = i

        # correct the resulted text to ajust some case of consonant neighbor
        # معالجة حالات التقاء الساكنين
        # ~ print "tashkeel 2", vocalized_text.encode('utf8')
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
        return self.tashkeel(text, suggestion=True, format_display="html")

    def tashkeel_output_text(self, text):
        """
        Vocalize the text witthout suggestion
        @param text: input text.
        @type text: unicode.
        @return: vocalized text.
        rtype: text.
        """
        return self.tashkeel(text, suggestion=False, format_display="text")

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
        text = re.sub(u'\sمِنْ\s+ا', u' مِنَ ا', text)
        # man = > mani

        text = re.sub(u'\sمَنْ\s+ا', u' مَنِ ا', text)
        #An = > ani
        text = re.sub(u'\sعَنْ\s+ا', u' عَنِ ا', text)
        #sukun + alef = > kasra +alef
        text = re.sub(u'\s%s\s+ا'%araby.SUKUN, u' %s ا' % araby.KASRA, text)
        #~ text = re.sub(ur'\s%s\s+ا'%araby.SUKUN, u' %s ا' % araby.SUKUN, text)
        #ajust pounctuation
        text = re.sub(u" ([.?!, :)”—]($| ))", u"\1", text)
        #binu = > bin 
        # temporary, to be analysed by syntaxical analyzer
        text = re.sub(u'\sبْنُ\s', u' بْن ', text)        
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
            if i+1 < len(_suggest_list) and  "chosen" in _suggest_list[i+1] \
            and _suggest_list[i+1]['chosen'].startswith(araby.ALEF):

                if _suggest_list[i]['chosen'] in (u'مَنْ', u'مِنْ', u'عَنْ'):
                        if _suggest_list[i]['chosen'] == u'مِنْ':
                            _suggest_list[i]['chosen'] = u'مِنَ'
                        elif _suggest_list[i]['chosen'] == u'عَنْ':
                            _suggest_list[i]['chosen'] = u'عَنِ'
                        elif _suggest_list[i]['chosen'] == u'مَنْ':
                            _suggest_list[i]['chosen'] = u'مَنِ'

                elif _suggest_list[i]['chosen'].endswith(araby.SUKUN):
                    _suggest_list[i]['chosen'] = _suggest_list[i]['chosen'][:-1] + araby.KASRA
            # if _suggest_list[i]['chosen'] == u'بْنُ':
                # _suggest_list[i]['chosen'] = u'بْن'
        return _suggest_list

    def display(self, word, format_display="text"):
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
            # previous = word_stemming_dict
            for item in word_analyze_list:
                voc = item.get_vocalized()
                # ~vocalized_text = u"".join([vocalized_text, voc])
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
        for abr in list(tashkeel_const.CorrectedTashkeel.keys()):
            text = re.sub(u"\s%s\s"%abr, u" %s " % \
            tashkeel_const.CorrectedTashkeel[abr], text)
        wordlist = self.analyzer.tokenize(text)

        prevocalized_list = pyarabic.number.pre_tashkeel_number(wordlist)
        self.logger.debug("pre_tashkeel numbers %s", u" ".join(prevocalized_list))

        # Todo ajust prevocalization of named enteties
        if len(prevocalized_list) != len(wordlist):
            self.logger.debug("nb %s", u"+".join(prevocalized_list))

        prevocalized_list = pyarabic.named.pretashkeel_named(prevocalized_list)
        self.logger.debug("nmd %s", u" ".join(prevocalized_list))
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
        # todo: return a text from the statistical tashkeel
        return u" ".join(newlist)


    # new version of choose tashkeel
    # first we use indexes instead of stemmedsynword object
    # ~ def __choose_tashkeel_algo2(self, caselist, previous_chosen_case = None,
    def __choose_tashkeel(
        self, caselist, current_synode, previous_chosen_case=None,
        pre_node=None, next_node=None, previous_chosen_relation=False
    ):
        """
        Choose a tashkeel for the current word, according to the previous one.
        A new algorithm
        @param caselist: list of steming result of the word.
        @type caselist: list of stemmedSynword
        @param: the choosen previous word stemming.
        @type previous_chosen_case:stemmedSynwordhg
        @return: the choosen stemming of the current word.
        @rtype:stemmedSynword.
        """
        chosen = None
        chosen_index = False
        rule = 0
        previous = previous_chosen_case
        if previous:
            pre_relation = 0
        else:
            pre_relation = 0
        if next_node:
            next_chosen_indexes = next_node.get_chosen_indexes()
        else:
            next_chosen_indexes = None
        # ~ debug = True
        # How to choose a vocalized case
        # and lets other methods to choose by semantic and syntaxic
        # choose a case is a stop, word and has next relation
        # browse the list by indexes
        # ~ indxlist = range(len(caselist))
        # get the chosen indexes from the current synode
        # which allow to handle previous and nexts and make other analysis
        indxlist = current_synode.get_chosen_indexes()
        # get all the indexes in the current cases list
        tmplist = []
        if len(indxlist) == 1:
            if caselist[0].is_unknown():
                caselist[0].set_vocalized(self.unknown_vocalizer.lookup(caselist[0].get_word()))
                rule = 102
            else:
                rule = 101

        if not rule:
            # order indexes list by word frequency
            indxlist = sorted(indxlist, key=lambda x: caselist[x].get_freq())
        # initial cases
        if not rule and (not previous or previous.is_initial()):
            # choose the initial case
            indxlist, rule = self.__choose_initial(indxlist, caselist,  next_chosen_indexes, next_node)
            self.logger.debug("2:%s", repr(indxlist))

            # and lets other methode to choices by semantic and syntaxic
        if not rule:
            self.logger.debug("2-1:%s", repr(indxlist))
            indxlist, rule = self.__choose_cases(indxlist, caselist, previous, next_chosen_indexes, next_node, previous_chosen_relation)
            self.logger.debug("3: %s", repr(indxlist))
        #~ return 0        
        #select default
        if not rule:
            indxlist, rule = self.__choose_default(indxlist, caselist)
            self.logger.debug("4: %s",  repr(indxlist))

        # select the first case if there one or many
        chosen_index = indxlist[0]
        chosen = caselist[chosen_index]
        if not rule: rule = 100
        if debug: 
            self.logger.debug("100: %d %s", rule, u", ".join([caselist[x].get_vocalized() for x in indxlist]))
         
        
        # set the selection rule to dispaly how tahskeel is selected
        chosen.set_rule(rule)
        return chosen.get_order()

    def __choose_initial(self, indxlist, caselist, next_chosen_indexes, next_node):
        """
        Select the initial case to start a sentence
        @param caselist: list of steming result of the word.
        @type caselist: list of stemmedSynword
        @param indxlist: list of index.
        @type indxlist: list of integer
        @return: indexlist and rule.
        @rtype:( list of integer, integer/False) .
        """
        rule = False
        # select more words with relations
        if not rule and self.get_enabled_semantic_analysis():
            # one semantic relations from next
            self.logger.debug("10 %s", repr(indxlist))
            #~ tmplist = list(filter(lambda x: caselist[x].has_sem_next(next_chosen_indexes), indxlist))
            tmplist = [x for x in indxlist if caselist[x].has_sem_next(next_chosen_indexes)]
            indxlist, rule = _get_indexlist_and_rule(list(tmplist), indxlist, caselist, 6)
            self.logger.debug("11 %s", repr(tmplist))
            self.logger.debug("11 %s", repr(indxlist))

        if not rule and self.get_enabled_syntaxic_analysis():
            # select all cases with syntaxic relations
            self.logger.debug("12a %s next_chosen", repr(next_chosen_indexes))
            for x in indxlist:
                self.logger.debug("12b [%d] : %s nexts",x, caselist[x].get_next())
                self.logger.debug("12b [%d] : %s nexts",x, repr(caselist[x].next))
            self.logger.debug("12e %s indxlist", repr(indxlist))               
            #tmplist = list(filter(lambda x: caselist[x].has_next(next_chosen_indexes), indxlist))
            tmplist = [x for x in indxlist if caselist[x].has_next(next_chosen_indexes)]

            self.logger.debug("12c %s indxlist", repr(tmplist))
            
            
            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 14)
            self.logger.debug("12 %s indxlist", repr(indxlist))

        # choose default for initial

        tmplist = list(filter(lambda x: (caselist[x].is_stopword() or
                 (caselist[x].is_marfou3() and not caselist[x].is_passive())
                 or caselist[x].is_past() ), indxlist))
        self.logger.debug("13 %s", repr(indxlist))
        indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 200)
        
        return  indxlist, rule


    def __choose_cases(self, indxlist, caselist, previous, next_chosen_indexes, next_node, previous_chosen_relation):
        """
        Select the case  in the middle, when it is possible
        @param caselist: list of steming result of the word.
        @type caselist: list of stemmedSynword
        @param indxlist: list of index.
        @type indxlist: list of integer
        @return: indexlist and rule.
        @rtype:( list of integer, integer/False) .
        """
        rule = 0
            # select all cases with semantic relations
        if not rule and self.get_enabled_semantic_analysis(): 
            self.logger.debug("14-a %s", repr(indxlist))


            tmplist = list(filter(lambda x: self.anasem.is_related(previous, caselist[x]) or caselist[x].has_sem_next(next_chosen_indexes), indxlist))

            #tmplist = list(tmplist)
            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, rule)
            self.logger.debug("14-b %s", repr(indxlist))
            # two semantic relations
            tmplist = list(filter(lambda x: self.anasem.is_related(previous, caselist[x]) and caselist[x].has_sem_next(next_chosen_indexes), indxlist))
            #tmplist = list(tmplist)
            self.logger.debug("14-c %s", repr(indxlist))
            
            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 4)


            # one semantic relations from previous
            tmplist = list(filter(lambda x: self.anasem.is_related(previous, caselist[x]) and caselist[x].has_next(next_chosen_indexes), indxlist))
            #tmplist = list(tmplist)
            self.logger.debug("15 %s", repr(indxlist))            

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 5)


            # one semantic relations from next
            tmplist = list(filter(lambda x: self.anasynt.is_related(previous, caselist[x]) and caselist[x].has_sem_next(next_chosen_indexes), indxlist))
            #tmplist = list(tmplist)
            self.logger.debug("16 %s", repr(indxlist))            
            
            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 6)

            # select stopword
        if not rule:
            tmplist = list(filter(lambda x:  caselist[x].is_stopword(), indxlist))
            #tmplist = list(tmplist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 3)
            self.logger.debug("16 %s", repr(indxlist))            

            # syntaxic
            # select stopword

        if not rule:           
            tmplist = list(filter(lambda x:  caselist[x].is_stopword() and (self.anasynt.is_related(previous, caselist[x])
                                     and caselist[x].has_next(next_chosen_indexes)) , indxlist))
            #tmplist = list(tmplist)
            self.logger.debug("17 %s", repr(indxlist))            
            
            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 41)

        if not rule:           
            tmplist = list(filter(lambda x:  caselist[x].is_stopword() and caselist[x].has_next(next_chosen_indexes) , indxlist))
            #tmplist = list(tmplist)
            self.logger.debug("18 %s", repr(indxlist))            
            

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 10)

        # ~ if not rule:
            # ~ tmplist = filter(lambda x:  caselist[x].is_stopword()  and self.anasynt.is_related(previous, caselist[x]) , indxlist)
            # ~ # if indexes list is empty, the current indexes list is reloaded, and no change
            # ~ if tmplist:
                # ~ indxlist = tmplist
                # ~ if len(indxlist) == 1: rule = 42
            # ~ if debug: print 10,rule, u", ".join([caselist[x].get_vocalized() for x in indxlist]).encode('utf8')

            # get all the indexes in the current cases list
        if not rule and self.get_enabled_syntaxic_analysis():
            # select all cases with syntaxic relations
            tmplist = list(filter(lambda x: (self.anasynt.is_related(previous, caselist[x]) and caselist[x].has_next(next_chosen_indexes)), indxlist))
            #tmplist = list(tmplist)
            self.logger.debug("19 %s", repr(indxlist))            
            
            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 11)
        if not rule and  self.get_enabled_syntaxic_analysis():
            tmplist = list(filter(lambda x: (self.anasynt.is_related(previous, caselist[x])), indxlist))
           
            #tmplist = list(tmplist)
            self.logger.debug("20 %s", repr(indxlist))            
            
            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 12)
        #
        if not rule and  self.get_enabled_syntaxic_analysis():
            tmplist = list(filter(lambda x: (self.anasynt.is_related(previous, caselist[x]) and self.anasynt.are_compatible_relations(previous_chosen_relation, previous.get_next_relation(x)) ), indxlist))
            #tmplist = list(tmplist)
            self.logger.debug("21 %s", repr(indxlist))            
            
            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 13)
        # select only compatible relations with previous relations
        # reduces cases if the previous chosen relation is not compatible with actual relations


        # like قال هذا الرجل،
        # قال هذا
        # ~ give us a verb subject,
        # ~ then the relation between
        # ~ هذا الرجل
        # ~ must be raf3 substitution

        if not rule and  self.get_enabled_syntaxic_analysis():
            tmplist = list(filter(lambda x: (self.anasynt.is_related(previous, caselist[x]) and self.anasynt.are_compatible_relations(previous_chosen_relation, previous.get_next_relation(x)) ), indxlist))
            #tmplist = list(tmplist)

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 13)
            self.logger.debug("22 %s", repr(indxlist))            

            # Default cases selection
            # get all the indexes in the current cases list
        if not rule and self.get_enabled_syntaxic_analysis():
            # select all cases with syntaxic relations
            tmplist = list(filter(lambda x: caselist[x].has_next(next_chosen_indexes), indxlist))
            #tmplist = list(tmplist)
            self.logger.debug("23 %s", repr(indxlist))            
            
            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 14)
        # Get relations of non mansoub with a has_previous
        # Previlege relations of Raf3 or Jar than the Nasb if there are many relations
        if not rule and self.get_enabled_syntaxic_analysis():
            # select all cases with syntaxic relations
            tmplist = list(filter(lambda x: (self.anasynt.is_related(previous, caselist[x]) and caselist[x].is_noun() and not caselist[x].is_mansoub()), indxlist))
            #tmplist = list(tmplist)
            self.logger.debug("24 %s", repr(indxlist))            
            
            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 17)        
        if not rule:
            # select all cases with tanwin
            if (next_node and next_node.is_break()) or not next_node:
                tmplist = list(filter(lambda x: caselist[x].is_tanwin() or not caselist[x].is_noun() , indxlist))
                #tmplist = list(tmplist)
                self.logger.debug("25 %s", repr(indxlist))            
                

                indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 15)

        return indxlist, rule

    def __choose_default(self, indxlist, caselist):
        """
        Select default cases when all others methods fail
        @param caselist: list of steming result of the word.
        @type caselist: list of stemmedSynword
        @param indxlist: list of index.
        @type indxlist: list of integer
        @return: indexlist and rule.
        @rtype:( list of integer, integer/False) .
        """
        # select cases with the max frequency
        # first get max freq
        maxfreq = 0
            
        maxfreq = max([caselist[x].get_freq() for x in indxlist])
        tmplist = list(filter(lambda x: caselist[x].get_freq() == maxfreq, indxlist))
        #tmplist = list(tmplist)                 
        indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 31)

        if not rule:
            # exode Dual cases
            # use to avoid dual cases like من الفلاحَين instead of من الفلاحِين
            tmplist = list(filter(lambda x: ( caselist[x].is_noun() and  not caselist[x].is_dual()), indxlist))
            #tmplist = list(tmplist)                 

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 32)

        if not rule:
            # select mansoub noun
            tmplist = list(filter(lambda x: ( caselist[x].is_noun() and  caselist[x].is_mansoub()), indxlist))
            #tmplist = list(tmplist)                 

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 33)

        # ~ if not rule:
            # ~ # select plural noun
            # ~ tmplist = filter(lambda x: ( caselist[x].is_noun() and  caselist[x].is_plural()), indxlist)

            # ~             indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, rule)

        if not rule:
            # select active voice
            tmplist = list(filter(lambda x: ( caselist[x].is_verb() and not caselist[x].is_passive()), indxlist))
            #tmplist = list(tmplist)  

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 35)

        if not rule:
            # select present marfou3 or past
            tmplist = list(filter(lambda x: ( caselist[x].is_verb() and (caselist[x].is_marfou3() or caselist[x].is_past())), indxlist))

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 36)
        if not rule:
            # select 3rd person
            tmplist = list(filter(lambda x: ( caselist[x].is_verb() and caselist[x].is3rdperson()), indxlist))

            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 37)

        if not rule:
            # select 1st person
            tmplist = list(filter(lambda x: ( caselist[x].is_verb() and caselist[x].is1stperson()), indxlist))
            #tmplist = list(tmplist) 
            indxlist, rule = _get_indexlist_and_rule(tmplist, indxlist, caselist, 38)

        return indxlist, rule
    # new version of choose tashkeel
    # first we use indexes instead of stemmedsynword object
    # ~ def __choose_tashkeel_algo2(self, caselist, previous_chosen_case = None,

    def __reduce_cases(
        self, caselist, current_synode, previous_chosen_case=None,
        pre_node=None, next_node=None
    ):
        """
        reduce  possible cases for the current word, according to the previous one and nexts.
        A new algorithm
        @param: list of steming result of the word.
        @type caselist: list of stemmedSynword
        @param: the choosen previous word stemming.
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
        # ~ debug = True
        # How to choose a vocalized case
        # and lets other methode to choices by semantic and syntaxic
        # choose a case is a stop, word and has next relation
        # browse the list by indexes
        # ~ indxlist = range(len(caselist))
        # get the chosen indexes from the current synode
        # which allow to handle previous and nexts and make other analysis
        indxlist = current_synode.get_chosen_indexes()
        # get all the indexes in the current cases list
        tmplist = []
        rule = 0
        # syntaxic
        # choose all tanwin cases before breaks
        if not next_node or (next_node and next_node.is_break()):
            # ~ tmplist = filter(lambda x:  (caselist[x].is_tanwin() and caselist[x].has_next(next_chosen_indexes)) or not caselist[x].is_noun()  , indxlist)
            # ~ tmplist = filter(lambda x:  caselist[x].is_tanwin() or caselist[x].is_defined() or not caselist[x].is_noun()  , indxlist)
            # ~ tmplist = filter(lambda x:  not(caselist[x].is_tanwin() and not caselist[x].is_defined())  , indxlist)
            # if indexes list is empty, the current indexes list is reloaded, and no change
            if tmplist:
                indxlist = tmplist
        # ~ if not rule and self.get_enabled_semantic_analysis():
            # ~ tmplist = filter(lambda x: caselist[x].has_sem_next(next_chosen_indexes) or caselist[x].has_sem_previous(), indxlist)
            # ~ # if indexes list is empty, the current indexes list is reloaded, and no change
            # ~ if tmplist:
                # ~ indxlist = tmplist
# ~
            # ~ # if there are many semantic relations or non one, we use frequency to choose the
            # ~ # most frequent word to be selected
                # ~ if len(indxlist) == 1: rule = 2
            # ~ if debug: print 2,rule, u", ".join([caselist[x].get_vocalized() for x in indxlist]).encode('utf8')

        # select stopword
        if next_node:
           
            tmplist = list(filter(lambda x:  caselist[x].is_stopword() and (caselist[x].has_next(next_chosen_indexes) 
                        ), indxlist))

            # if indexes list is empty, the current indexes list is reloaded, and no change
            if tmplist:
                indxlist = tmplist
                if len(indxlist) == 1 : rule = 3
            if debug: print(3,rule, u", ".join([caselist[x].get_vocalized() for x in indxlist]).encode('utf8'))
 

        # reduce the list of cases
        current_synode.set_chosen_indexes(indxlist)


def _get_indexlist_and_rule(tmplist, indexlist, caselist, rule):
    """
    Just a macro to avoid repetetion
    if tmplist is not empty, change indexlist,
    if the indexlist has one element, the rule is applyed
    """
    debug = False
    if tmplist:
        indexlist = tmplist

    # ~ if the indexlist has one element, the rule is applied
    applied_rule = rule if len(indexlist) == 1 else 0
    # if debug, display the 
    if debug: 
        print("choose tashkeel", rule,applied_rule, u", ".join([caselist[x].get_vocalized() for x in indexlist]).encode('utf8'))
    return indexlist, applied_rule


def mainly():
    """
    main test
    """
    print("test")
    vocalizer = TashkeelClass()
    # text = u"""تجف أرض السلام بالسلام الكبير.    مشى على كتاب السلام.
    # جاء الولد السمين من قاعة القسم الممتلئ"""
    text = u"يعبد الله تطلع الشمس"
    voc = vocalizer.tashkeel(text)
    print(voc.encode('utf8'))
if __name__ == "__main__":
    mainly()
