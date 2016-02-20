#!/usr/bin/python
# -*- coding=utf-8 -*-
#------------------------------------------------------------------------
# Name:        aranasyn.syn_const
# Purpose:     Arabic syntaxic analyser.
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#------------------------------------------------------------------------
"""
Syntaxic Analysis
"""
if __name__ == "__main__":
    import sys
    sys.path.append('../lib')
    sys.path.append('../')
import pyarabic.araby as araby
import aranasyn.syn_const 
#~ import qalsadi.stemmedword as stemmedword
import aranasyn.synnode
import aranasyn.stemmedsynword as stemmedsynword
import naftawayh.wordtag as wordtag
from operator import and_
from operator import xor

class SyntaxAnalyzer:
    """
        Arabic Syntax analyzer
    """
    def __init__(self):
        self.wordtagger = wordtag.WordTagger()
        pass
    def analyze(self, detailed_stemming_dict):
        """
        Syntaxic analysis of stemming results.
        morphological Result is a list of stemmedword objects
         The syntaxic result have the same structure, 
         but we add a field named 'syntax' to every word steming dictioionary
        @param detailed_stemming_dict: detailed stemming dict.
        @type detailed_stemming_dict:list of list of stemmedword objects
        @return: detailed syntaxic result with syntaxic tags.
        @rtype: list of list of stemmedsynword
        """
        # create stemmed word instances
        stemmedsynwordlistlist = []
        synnode_list = []
        # convert objects from stemmedWord to stemmedSynWord 
        # in order to add syntaxic proprities
        for stemming_list in detailed_stemming_dict:
            tmplist = [stemmedsynword.StemmedSynWord(
            stemming_list[order], order) for order in range(len(stemming_list))]
            if not tmplist:
                tmplist = [stemmedsynword.StemmedSynWord(stemming_list[0]),]
            stemmedsynwordlistlist.append(tmplist)
            #create the synode object from tmplist
            synnode_list.append(aranasyn.synnode.SynNode(tmplist))
        stemmedsynwordlistlist = self.study_syntax_by_synode(
        stemmedsynwordlistlist, synnode_list)
        return stemmedsynwordlistlist, synnode_list


    def study_syntax_by_synode(self, stemmedsynwordlistlist, synnode_list):
        """
        Analyzing the texts words cases by one syntax node,

        """
        #split the synodelist into small lists (chunks) 
        #~according to break points
        #Break points are word with syntaxique procletics 
        #~like WAW conjinctions, and Prepositions
        # treat chunks and choose relationship according to word type
        # verb + noun = > verb + subject or verb + objects
        # noun + noun = > noun adjective, or mubtad' wa Khabar
        # factor + noun,
        # factor + verb

        # ignore if the current word is transparent
        ignore = False
        #~counter = 0
        previous_index = 0
        pre_node = None
        previous_index = False        
        # study the relations between words stemmings
        for current_index in  range(len(stemmedsynwordlistlist)):
            #index used to handle stmd position
            stmword_case_position = 0
            current_node = synnode_list[current_index]
            if current_index - 1 >=0 :
                pre_node = synnode_list[current_index-1]
              # guess the word type by word tag
                tag = self.wordtagger.one_word_tagging(current_node.get_word(), pre_node.get_word())
                current_node.set_guessed_type_tag(tag)
            else:
                pre_node =None
            if current_index + 1 < len(stemmedsynwordlistlist) : 
                next_node = synnode_list[current_index+1]
            else:
                next_node = None            
            for stmword in stemmedsynwordlistlist[current_index]:
                if  current_index == 0:  # the initial case
                    # the initial case
                    #~counter += 1
                    stmword = self.bigram_analyze(None, stmword )[1]
                else:
                    previous_case_position = 0 
                    for previous in stemmedsynwordlistlist[previous_index]:
                        #~counter += 1
                        previous, stmword = self.bigram_analyze(previous, stmword, previous_case_position, stmword_case_position, pre_node, next_node)
                        previous_case_position += 1 


                # if the current word is transparent, ignore it 
                # and fix the previous index to the previous word.
                if stmword.is_transparent():
                    ignore = True
                else: ignore = False
                stmword_case_position += 1
            # if the current word ha sall its cases as transparent
                #~words = u"""تغمده الله برحمته .            
            #~# الكلمة الشفافة مثل اسم الإشارة 
            #~تنقل تأثير الكلمة السابقة لها للكلمة اللاحقة لها# م
                        #~
            # مثل رأيت هذا الرجل
            # if not the word is not transprent, change the previous index.
            # else: change the ignore state and save the previous index as it.
            if not ignore:
                previous_index = current_index
            else:
                # previous index is mantained.
                ignore = False
        return stemmedsynwordlistlist

    def bigram_analyze2(self, previous, current, previous_position = 0, 
            current_position = 0, pre_node = None, next_node = None):
        for cond in aranasyn.syn_const.conditions:
            precondlist = cond['previous'] 
            curcondlist = cond['current']
            precriteria = False 
            curcriteria = False 
            # join all tests
            if previous :
                # Browse all condition, if one is false, break with false
                # else all conditions are true,                 
                for k,v in precondlist:
                    if getattr(previous, k)() != v:
                        break
                else:
                    precriteria = True 
            if precriteria and current:  
                # Browse all condition, if one is false, break with false
                # else all conditions are true, 
                for k,v in curcondlist:
                    if getattr(current, k)() != v:
                        break
                else:
                    curcriteria = True
            if precriteria and curcriteria:
                weight = cond.get("rule", 0)
                break;
    #~ def bigram_analyze2(self, previous, current, previous_position = 0, 
            #~ current_position = 0, pre_node = None, next_node = None):
        #~ for cond in aranasyn.syn_const.conditions:
            #~ precondlist = cond['previous'] 
            #~ curcondlist = cond['current']
            #~ precriteria = False 
            #~ curcriteria = False 
            #~ # join all tests
            #~ if previous :
                #~ # Browse all condition, if one is false, break with false
                #~ # else all conditions are true,                 
                #~ precriteria =reduce( and_,[getattr(previous, k)() == v for k,v in precondlist])
            #~ if precriteria and current: 
                #~ curcriteria =reduce( and_,[getattr(current, k)() == v for k,v in curcondlist])
            #~ if precriteria and curcriteria:
                #~ weight = cond.get("rule", 0)
                #~ break;          
    def is_number_relation(self, previous, current):
        """
        Return the weight if the previous and current have number relation
        """
        weight = 0
        if current.is_noun():
            try:
                # get intger part only
                number = int(float(previous.get_word()))
            except ValueError:
                number = 0
            if number  % 100 in range(3,10) or number % 100 == 0:
                if current.is_majrour():
                    weight = aranasyn.syn_const.JarMajrourRelation
            elif  number % 100 in range(11,99) or number % 100 == 0:
                if current.is_mansoub():
                    weight = aranasyn.syn_const.NasebMansoubRelation 
        return weight
        
    def is_verb_object_relation(self, previous, current):
        """
        Return the weight if the previous and current have verb object relation
        """
        return current.is_noun() and current.is_mansoub()  and not previous.has_encletic() and previous.is_transitive()

    def is_jonction_relation(self, previous, current): 
        if current.is_break() and current.is_noun()  and previous.is_noun() \
         and (current.has_procletic() and current.has_jonction() and not current.has_jar()): 
            # jonction 
            if (current.is_majrour() and previous.is_majrour()) \
            or (current.is_mansoub() and previous.is_mansoub()) \
            or (current.is_marfou3()and previous.is_marfou3()):
                return True
        else:
            return False

    def bigram_analyze(self, previous, current, previous_position = 0, 
            current_position = 0, pre_node = None, next_node = None):
        """
        Syntaxic analysis of stemming results, two words.
        the positions are use to join related cases.
        @param previous : the first item in bigram.
        @type previous  : stemmedSynWord
        @param current  : the second item in bigram.
        @type current   : stemmedSynWord
        @param currentSynode    : the current synode in The phrase.
        @type  currentSynode    : synnode object
        @param previous : the first item position in the word case list.
        @type previous  : stemmedSynWord
        @param current  : the second item position in the word case list.
        @type current   : stemmedSynWord
        @return: the updated previous and current stemmedSynWord.
        @rtype: (previous, current)
        """
        # Todo treat the actual word according to the previous word
        # treat the initial case when previous = None
        # to save the forced case to link previous and current word.
        # the word can be forced before this treatement,
        # the this variable is used to indicate if the word is 
        #forced during the actual process.
        
        #~ self.bigram_analyze2( previous, current)
        weight = 0
       

        if not previous or previous.is_initial():
            if current.is_marfou3() or current.is_past() or current.is_stopword():
             # if  current.is_majrour():
                current.forced_case()
                # add to the current word case a pointer
                #to the previous word order.
                #p for previous
                # if the previous is None, that means 
                #that the previous is initiatl state
                # the current word is prefered, we add previous
                # pointer to 0 position.
                current.add_previous(previous_position, aranasyn.syn_const.PrimateRelation)

            return (previous, current)

        elif not current:
            # if the current word is end of clause or end of line, (None)
            # and the previous is not followed by a word,
            # the previous will have a next relation.
                #~words = u"""تغمده الله برحمته .
             #~أشهد أن لا إله إلا الله وحده لا           
             #~# إذا كانت الكلم الأولى بعدها لا كلمة،
             #~أي نهاية العبارة، نضع لها راطة لاحقة إلى لاشيء
            # تستعمل هذه في ضبط أواخر الجمل
            # مثلا
            # جاء ولد
            # تحولّ إلى ثنائيات
            # [None. جاء]، [جاء، ولد]، [ولد، None]

            # if the pounct is a break, the tanwin is prefered
            # the previous will have twnin

            if previous.is_tanwin():
            # add a relation to previous
                previous.add_next(current_position, aranasyn.syn_const.TanwinRelation)
            return (previous, current)


        # جملة مقول القول
        if current.is_pounct() and previous.is_verb() and previous.get_original() == u"قالَ":
            #if the current is pounctuation and the previous is a speach verb, 
            previous.add_next(current_position, aranasyn.syn_const.VerbObjectRelation)
            return (previous, current)            

        elif self.is_jonction_relation(previous, current): 
            previous.add_next( current_position, aranasyn.syn_const.JonctionRelation)
            current.add_previous(previous_position, aranasyn.syn_const.JonctionRelation)                
            return (previous, current)

        elif current.is_pounct() or current.is_stopword() or \
        (current.has_procletic()) :# and not current.is_defined()):
            # if the pounct is a break, the tanwin is prefered
            # the previous will have twnin

            if current.is_break() and previous.is_tanwin():
                previous.add_next(current_position, aranasyn.syn_const.TanwinRelation)
                return (previous, current)
        #العدد والمعدود، التمييز
        # quantity case
        #the previous is a number, 
        if previous.is_number():
            weight = self.is_number_relation(previous, current)

        #the stop word is factors, others no, 
        # if the previous is not stop word return.
        if previous.is_stopword() and not current.is_break():
            if current.is_noun():# and previous.is_nominalFactor():
                if (previous.is_jar() or previous.is_addition()) and \
                current.is_majrour():
                    print current.get_vocalized().encode('utf8'), current.get_tags().encode('utf8'),current.get_order(),current.is_majrour()
                    weight = aranasyn.syn_const.JarMajrourRelation

                # اسم إنّ منصوب
                elif previous.is_naseb() and  current.is_mansoub():
                    current.set_inna_noun()
                    weight = aranasyn.syn_const.InnaNasebMansoubRelation
                    # خبر إنّ لمبتدإ ضمير متصل
                elif previous.has_encletic() and previous.is_naseb() and current.is_marfou3():
                    #~ current.set_inna_noun()
                    weight = aranasyn.syn_const.InnaRafe3Marfou3Relation

                elif previous.is_initial() and  current.is_marfou3():
                    weight = aranasyn.syn_const.PrimateRelation

                # اسم كان وأخواتها
                elif previous.is_kana_rafe3() and current.is_marfou3():
                    current.set_kana_noun()
                    weight = aranasyn.syn_const.KanaRafe3Marfou3Relation
                elif previous.is_rafe3() and current.is_marfou3():
                    weight = aranasyn.syn_const.Rafe3Marfou3Relation
            # pronoun verb
            elif current.is_verb() and self.compatible_subject_verb(previous, current):
                # تطابق الضمير مع الضمير المسند إليه
                weight = aranasyn.syn_const.SubjectVerbRelation
            #verb
            elif current.is_verb() and previous.is_verbal_factor():
                if current.is_present():
                    if previous.is_jazem() and current.is_majzoum():
                        #حالة خاصة لا الناهية تنهى عن الأفعال
                        # المسندة للضمير المخاطب فقط
                        if previous.get_unvoriginal() == u'لا':
                            if current.has_imperative_pronoun():
                               weight = aranasyn.syn_const.JazemMajzoumRelation 
                        else:
                            weight = aranasyn.syn_const.JazemMajzoumRelation
                    elif previous.is_verb_naseb() and  current.is_mansoub():
                        weight = aranasyn.syn_const.NasebMansoubRelation
                    elif previous.is_verb_rafe3() and current.is_marfou3():
                        #حالة لا النافية 
                        # المسندة لغير الضمائر المخاطبة
                        if previous.get_unvoriginal() == u'لا':
                            if not current.has_imperative_pronoun():
                               weight = aranasyn.syn_const.Rafe3Marfou3Relation
                        else:
                            weight = aranasyn.syn_const.Rafe3Marfou3Relation
                elif previous.is_condition_factor():
                    weight = aranasyn.syn_const.ConditionVerbRelation
                elif previous.is_verb_jobless_factor():
                    #~ print "x"
                    weight = aranasyn.syn_const.JoblessFactorVerbRelation

        else : # previous is not a stopword
            if current.is_verb() and not current.is_break():
                # الجارية فعل والسابق مبتدأ
                if previous.is_noun() and previous.is_defined():
                    if current.is_marfou3():
                    # Todo treat the actual word
                        weight = aranasyn.syn_const.Rafe3Marfou3Relation 
            if not current.is_break() and (current.is_noun() or current.is_addition()):
                # المضاف والمضاف إليه
                # إضافة لفظية
                # مثل لاعبو الفريق
                #~if current.is_majrour() or current.is_stopword():
                if current.is_majrour() :
                    if previous.is_added():
                        weight = aranasyn.syn_const.JarMajrourRelation
                    elif previous.is_noun() and not previous.is_defined() \
                           and not previous.is_added() and \
                           not previous.is_tanwin() and not current.is_adj():
                        weight = aranasyn.syn_const.JarMajrourRelation 
                # منعوت والنعت
                #  تحتاج إلى إعادة نظر
                # بالاعتماد على خصائص الاسم الممكن أن يكون صفة
                if previous.is_noun():
                    # Todo treat the actual word
                    #~print u" ".join([previous.get_word(), current.get_word(), str(current.is_adj()), str(self.are_compatible(previous, current))])
                    if self.are_compatible(previous, current):
                        if current.is_adj() and (current.is_defined() or current.is_tanwin()):
                            weight = aranasyn.syn_const.DescribedAdjectiveRelation
                    #مبتدأ وخبر
                    elif self.are_nominal_compatible(previous, current):
                        if current.is_adj():
                            weight = aranasyn.syn_const.PrimatePredicateRelation
                if previous.is_verb() and not current.is_break():
                    if previous.is3rdperson():
                        # Todo treat the actual word
                        # الفعل والفاعل أو نائبه
                        
                        if current.is_marfou3()  :
                            if not previous.is_passive():
		                        if ((current.is_feminin() and previous.is3rdperson_feminin())
		                           or (not current.is_feminin() and previous.is3rdperson_masculin())):
		                            #weight = aranasyn.syn_const.VerbSubjectRelation
		                            weight = aranasyn.syn_const.VerbSubjectRelation
                            else:
		                        if ((current.is_feminin() and previous.is3rdperson_feminin())
		                           or (not current.is_feminin() and previous.is3rdperson_masculin())):
		                            weight = aranasyn.syn_const.VerbPassiveSubjectRelation
                                

            # الفعل والمفعول به
            if self.is_verb_object_relation(previous, current):
                weight = aranasyn.syn_const.VerbObjectRelation
                       
            # فعل متعدي بحرف
            #ToDo:
            if previous.is_transitive() and current.is_stopword():
                weight = aranasyn.syn_const.VerbObjectRelation
     
        if weight :
            # add to the previous a pointer to the next word order.
            previous.add_next(current_position, weight)

            # add to the current word case a pointer 
            #to the previous word order.
            current.add_previous(previous_position, weight)
        return previous, current

    def is_related(self, previous, current):
        """
        verify the syntaxic path from the previous to current stemmed word.
        If the current word is related with the previous word, return True.
        The previous word can contain a pointer to the next word. t
        he current can have a pointer to the previous if they ara realated
        @param previous: the previous stemmed word, 
        choosen by the tashkeel process.
        @type previous:stemmedSynWord class 
        @param current: the current stemmed word.
        @type current:stemmedSynWord class 
        @return: return if the two words are related syntaxicly.
        @rtype: boolean
        """
        if (previous and current) and previous.get_order() in\
        current.get_previous() and current.get_order() in previous.get_next():
            return True
        else: return False

    def are_compatible(self, previous, current):
        """
        verify the gramatica relation between the two words.
        دراسة الترابط النخوي بين الكلمتين، اي توافقهما في الجمع والنوع، والحركة
        If the current word is related with the previous word, return True.
        The previous word can contain a pointer to the next word. 
        the current can have a pointer to the previous if they ara realated
        @param previous: the previous stemmed word, choosen by the tashkeel process.
        @type previous:stemmedSynWord class 
        @param current: the current stemmed word.
        @type current:stemmedSynWord class 
        @return: return if the two words are related syntaxicly.
        @rtype: boolean
        """
        #الكلمتان اسمان
        #if (not ((previous.is_noun() or previous.is_addition()) and 
        #current.is_noun())):
        if (not ((previous.is_noun() or previous.is_addition()) and 
        current.is_noun())):
            return False
        compatible = False
        # التعريف
        # إمّا معرفان معا، أو نكرتان معا
        #if ((current.is_defined() and previous.is_defined()) 
        #     or  (not current.is_defined() and not previous.is_defined())):
        if not xor(current.is_defined() , previous.is_defined()):
            compatible = True
        else:
            return False
		# العدد
        # والتثنية والإفراد الجمع
        # إمّا مفردان معا، أو جمعان معا أو مثنيان معا
        if ((current.is_plural() and previous.is_plural()) 
             or  (current.is_dual() and previous.is_dual())
			or (current.is_single() and previous.is_single())):
            compatible = True
        else:
            return False
        # الحركة
        # تساوي الحالة الإعرابية
        if (current.is_majrour() and previous.is_majrour()) \
            or (current.is_mansoub() and previous.is_mansoub()) \
            or (current.is_marfou3()and previous.is_marfou3()):
            compatible = True
        else:
            return False

        # الكلمة الثانية  غير مسبوقة بسابقة غير التعريف
        # هذا التحقق جاء بعد التحقق من التعريف أو التنكير
        if not current.has_procletic() or current.get_procletic() in (u"ال",
         u"فال" , u"وال", u"و", u"ف"):
            compatible = True
        else:
            return False
        # التنوين
        if not xor(current.is_tanwin() , previous.is_tanwin()):
            compatible = True
        else:
            return False

        # التذكير والتأنيث
        # مذكر ومذكر
        #مؤنث ومؤنث
        # جمع التكسير مؤنث
        if (current.is_feminin() and previous.is_feminin()) \
           or (current.is_masculin() and previous.is_masculin()) : # \
           #~or (previous.is_broken_plural() and current.is_feminin()
            compatible = True
        #~else: return False
        #ToDo: fix feminin and masculin cases
        return compatible


    def are_nominal_compatible(self, previous, current):
        """
        verify the gramatica relation between the two words, 
        for nominal relational المبتدأ والخبر
        دراسة الترابط النخوي بين الكلمتين، اي توافقهما في الجمع والنوع، والحركة
        If the current word is related with the previous word, return True.
        The previous word can contain a pointer to the next word. 
        the current can have a pointer to the previous if they ara realated
        @param previous: the previous stemmed word, 
        choosen by the tashkeel process.
        @type previous:stemmedSynWord class 
        @param current: the current stemmed word.
        @type current:stemmedSynWord class 
        @return: return if the two words are related syntaxicly.
        @rtype: boolean
        """
        #الكلمتان اسمان
        compatible = False
        if (previous.is_noun() and current.is_noun()):
            # التعريف
            # المبتدأ معرفة والخبر نكرة
            if (not current.is_defined() and previous.is_defined()):
                compatible = True
            else:
                return False
            # الحركة
            # تقابل الحالة الإعرابية
            # مبتدأ مرفوع خبر مرفوع
            # مبتدأ منصوب خبر مرفوع# اسم كان
            # مبتدأ مرفوع خبر منصوب#  اسم إنّ
            if (previous.is_inna_noun() and previous.is_mansoub() \
            and current.is_marfou3()) or (previous.is_kana_noun() \
             and previous.is_marfou3() and current.is_mansoub())\
            or (not previous.is_inna_noun() and not previous.is_kana_noun() \
            and previous.is_marfou3() and current.is_marfou3()):
                compatible = True
            else:
                return False
            # الكلمة الثانية  غير مسبوقة بسابقة غير التعريف
            # هذا التحقق جاء بعد التحقق من التعريف أو التنكير
            if not current.has_procletic():
                compatible = True
            else:
                return False
            # التنوين
            if not previous.is_tanwin():
                compatible = True
            else:
                return False
            # والتثنية والإفراد الجمع
		# العدد
        # والتثنية والإفراد الجمع
        # إمّا مفردان معا، أو جمعان معا أو مثنيان معا
            if ((current.is_plural() and previous.is_plural()) 
		         or  (current.is_dual() and previous.is_dual())
				or (current.is_single() and previous.is_single())):
                compatible = True
            else:
                return False
            # التذكير والتأنيث
            # مذكر ومذكر
            #مؤنث ومؤنث
            # جمع التكسير مؤنث
            if (current.is_feminin() and previous.is_feminin()) \
             or (current.is_masculin() and previous.is_masculin()) \
             or (previous.is_broken_plural() and current.is_feminin()):
                compatible = True
            else: return False
        #الأول اسم والثاني فعل
        elif (previous.is_noun() and current.is_verb()):

            # التعريف
            # المبتدأ معرفة والخبر نكرة
            if previous.is_defined():
                compatible = True
            else:
                return False
            # الحركة
            # تقابل الحالة الإعرابية
            # مبتدأ مرفوع خبر مرفوع
            # مبتدأ منصوب خبر مرفوع# اسم كان
            # مبتدأ مرفوع خبر منصوب#  اسم إنّ

            # الكلمة الثانية  غير مسبوقة بسابقة غير التعريف
            # هذا التحقق جاء بعد التحقق من التعريف أو التنكير
            if not current.has_procletic():
                compatible = True
            else:
                return False
            # التنوين
            if not previous.is_tanwin():
                compatible = True
            else:
                return False
            # والتثنية والإفراد الجمع
            # التذكير والتأنيث
            # مذكر ومذكر
            #مؤنث ومؤنث
            # جمع التكسير مؤنث
            # else: return False
            #الفعل مرفوع أو مبني
            if current.is_past() or (current.is_present() and\
             current.is_marfou3()):
                compatible = True
            else:
                return False
        return compatible




    def compatible_subject_verb(self, previous, current):
        """
        verify the gramatical relation between the two words, 
        for subject and verb 
        دراسة الترابط بين الفاعل والفعل، حين يسبق الفاعل الفعل
        If the current word is related with the previous word, return True.
        The previous word can contain a pointer to the next word. 
        the current can have a pointer to the previous if they ara realated
        @param previous: the previous stemmed word, 
        choosen by the tashkeel process.
        @type previous:stemmedSynWord class 
        @param current: the current stemmed word.
        @type current:stemmedSynWord class 
        @return: return if the two words are related syntaxicly.
        @rtype: boolean
        """
        compatible = False
        if previous.is_stopword():
            if (previous.is_pronoun() and current.is_verb()):
                # الضمير مطابق لضمير الفعل
                if previous.is_pronoun():
                    expected_pronouns = aranasyn.syn_const.TABLE_PRONOUN.get(current.get_pronoun(), [])
                    #~ print u"\t".join([previous.get_vocalized(),expected_pronoun]).encode('utf8')
                    if previous.get_original() in expected_pronouns:
                        compatible = True
            #الضمير المتصل مطابق لضمير الفعل
            #Todo fix is_added function
            if True or previous.is_added():
                expected_pronouns = aranasyn.syn_const.TABLE_PRONOUN.get(current.get_pronoun(), [])
                #~ print "is_added",previous.is_added(),  u"\t".join([previous.get_vocalized(), previous.get_encletic(),u", ".join(expected_pronouns)]).encode('utf8')
                if previous.get_encletic() in expected_pronouns:
                    compatible = True                    
        return compatible




    def exclode_cases(self, word_result):
        """
        exclode imcompatible cases
        @param word_result: The steming dict of the previous word.
        @type word_result: list of dict
        @return: the filtred word result dictionary with related tags.
        @rtype: list of dict
        """
    # حالة تحديد نمط الكلمة من السياق
        new_word_result = []
        for stemming_dict in word_result:
            if "#" in stemming_dict.get_syntax():
                new_word_result.append(stemming_dict)
        if len(new_word_result)>0:
            return new_word_result
        else:
            return word_result
        return word_result

    def detect_accepted_gammar(self, synnode_list):
        """
        Detect Possible syntaxical nodes sequences
        @param synnode_list: list of synNode.
        @type synnode_list:  list of synNode.
        """
        #for Test
        # display all cases
        #print synnode_list
        grammar_list = []
        for snd in synnode_list:
            tmplist = []
            taglist = []
            if snd.hasVerb():
                taglist.append('V')
            if snd.hasNoun():
                taglist.append('N')
            if snd.hasStopword():
                taglist.append('S')
            if snd.has_pounct():
                taglist.append('.')
            if not grammar_list:
                grammar_list = taglist
            else:
                for grm in grammar_list:
                    for tag in taglist:
                        tmplist.append(grm+tag)
            if tmplist:
                grammar_list = tmplist
        return True              
    def decode(self, stemmed_synwordlistlist):
        """
        Decode objects result from analysis. helps to display result.
        @param stemmed_synwordlistlist: list of  list of StemmedSynWord.
        @type word_result: list of  list of StemmedSynWord
        @return: the list of list of dict to display.
        @rtype: list of  list of dict
        """
        new_result = []
        for rlist in stemmed_synwordlistlist:
            tmplist = []
            for item in rlist:
                tmplist.append(item.get_dict())
            new_result.append(tmplist)
        return  new_result
    def display (self, stemmed_synwordlistlist):
        """
        display objects result from analysis
        @param stemmed_synwordlistlist: list of  list of StemmedSynWord.
        @type word_result: list of  list of StemmedSynWord
        """
        text = u"["
        for rlist in stemmed_synwordlistlist:
            text += u'\n\t['
            for item in rlist:
                text += u'\n\t\t{'
                stmword = item.__dict__
                for key in stmword.keys():
                    text += u"\n\t\tu'%s' = u'%s'," % (key, stmword[key])
                text += u'\n\t\t}'
            text += u'\n\t]'
        text += u'\n]'
        return text
def mainly():
    """
    main test
    """
    # #test syn
    text = u"سمع"
    import qalsadi.analex
    result = []
    analyzer = qalsadi.analex.Analex()
    anasynt = SyntaxAnalyzer()
    result = analyzer.check_text(text)
    result = anasynt.analyze(result)
    # the result contains objects
    print repr(result)
    #~ text2display = anasynt.display(result)
    #~ print text2display.encode('utf8')
if __name__ == "__main__":
    mainly()

