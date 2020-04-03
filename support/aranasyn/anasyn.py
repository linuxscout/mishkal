#!/usr/bin/python
# -*- coding=utf-8 -*-
#------------------------------------------------------------------------
# Name:        sconst
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

from operator import xor

import pyarabic.araby as araby
import naftawayh.wordtag as wordtag
from pyarabic.arabrepr import arepr 

import aranasyn.syn_const  as sconst
import aranasyn.synnode
import aranasyn.stemmedsynword as stemmedsynword
import aranasyn.cache as cache


class SyntaxAnalyzer:
    """
        Arabic Syntax analyzer
    """
    def __init__(self, cache_path=False):
        self.wordtagger = wordtag.WordTagger()
        ## Cache for relations betwwen words
        # I will use it for traning for extracting relations between original words
        self.syntax_train_enabled = False
        #~ self.syntax_train_enabled = True
        #file to use as cache in NoSQL format
        self.cache = cache.cache(cache_path)
        # structure will be:
        # { "original-word":{
        # "nextoriginalword":{relation1:frequncy, relation2:frequency2},},
        
        pass
    def __del__(self):
        #~ print "SynatxAnalyzer is dying"
        # print or log relations into a file or a file
        if self.syntax_train_enabled:
            self.cache.update()
            self.cache.display_all()
        pass
    
    def add_cache_relation(self, previous, current, relation):
        """
        Add relation between previous and current with realtion code
        """
        pre_original = previous.get_original()
        cur_original = current.get_original()
        self.cache.add_relation(pre_original, cur_original, relation)
        
        
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
            tmplist = [stemmedsynword.StemmedSynWord(stemming_list[order], order) 
                        for order in range(len(stemming_list))]
            # if there is just one, we select it
            if not tmplist:
                tmplist = [stemmedsynword.StemmedSynWord(stemming_list[0]),]
            stemmedsynwordlistlist.append(tmplist)
            #create the synode object from tmplist
            synnode_list.append(aranasyn.synnode.SynNode(tmplist))
        stemmedsynwordlistlist, synnode_list = self.study_syntax_by_synode(stemmedsynwordlistlist, synnode_list)
        return stemmedsynwordlistlist, synnode_list

    def study_syntax_by_synode(self, stemmedsynwordlistlist, synnode_list):
        """
        Analyzing the texts words cases by one syntax node,

        """
        #split the synodelist into small lists (chunks) 
        #~according to break points
        # Break points are word with syntaxique procletics 
        #~like WAW conjonctions, and Prepositions
        # treat chunks and choose relationship according to word type
        # verb + noun = > verb + subject or verb + objects
        # noun + noun = > noun adjective, or mubtad' wa Khabar
        # factor + noun,
        # factor + verb

        pre_node = None
        previous_index = False        
        # study the relations between words stemmings
        for current_index, (stemmedsynwordlist, current_node)  in  enumerate(list(zip(stemmedsynwordlistlist,synnode_list))):
            #index used to handle stmd position
            if current_index + 1 < len(synnode_list) : 
                next_node = synnode_list[current_index+1]
            else:
                next_node = None            
            for current_case_index, stmword in enumerate(stemmedsynwordlist):
                if  not current_index :  # the initial case
                    # the initial case
                    stmword = self.bigram_analyze(None, stmword )[1]
                else:
                    for previous_case_index, previous in enumerate(stemmedsynwordlistlist[previous_index]):
                        previous, stmword = self.bigram_analyze(previous, stmword, previous_case_index, current_case_index, pre_node, next_node)

            # خاصية الشفافية يجب أن تعالج في مستوى آخر وليس في مستوى حالات الكلمة
            previous_index = current_index
            pre_node       = current_node

        return stemmedsynwordlistlist, synnode_list





    def is_number_relation(self, previous, current):
        """
        Return the weight if the previous and current have number relation
        """
        weight = 0
        if current.is_noun() and current.is_tanwin():
            try:
                # get intger part only
                number = int(float(previous.get_word()))
            except ValueError:
                number = 0
            if number  % 100 in list(range(3,10)) or number % 100 == 0:
                if current.is_majrour():
                    weight = sconst.JarMajrourRelation
            elif  number % 100 in list(range(11,99)) or number % 100 == 0:
                if current.is_mansoub():
                    weight = sconst.NasebMansoubRelation 
        return weight
        
    def is_verb_object_relation(self, previous, current):
        """
        Return the weight if the previous and current have verb object relation
        """
        return (current.is_noun() and current.is_mansoub()  
           and not previous.has_encletic() and previous.is_transitive())

    def is_jonction_relation(self, previous, current): 
        #العطف بين اسمين
        #لا يعطف على حرف
        if previous.is_stopword():
            return False
        if current.is_break() and current.is_noun()  and previous.is_noun() \
         and (current.has_procletic() and current.has_jonction() and not current.has_jar()): 
            # jonction 
            if current.eq_case(previous):
                return True
        elif current.is_break() and current.is_verb()  and previous.is_verb() \
         and (current.has_procletic() and current.has_jonction() and not current.has_jar()): 
            # jonction 
            # تساوي الأزمنة والضمائر
            # 
            if ((current.get_tense() == previous.get_tense())
                and (current.get_pronoun() == previous.get_pronoun())):
                # الفعل المضارع يتساوى في الحالة الإعرابية
                if not current.is_present():
                    if current.eq_case(previous):
                        return True
                    else: 
                        return False
                # الفعل غير المضارع يكفي تساوي الأزمنة والضمائر
                else:
                    return True
            else: #عدم تساوي الأزمنة والضمائر
                return False                
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
        

        weight = 0
        #~ print "anasyn 8", current.get_vocalized(), "verb",current.is_verb(), "break", current.is_break()
        # the initial case
        if not previous or previous.is_initial():
            return self.treat_initial(previous, current, previous_position, current_position)
        # the final case
        elif not current:
            return self.treat_final(previous, current, previous_position, current_position)
        # jonction relations
        elif self.is_jonction_relation(previous, current): 
            previous.add_next( current_position, sconst.JonctionRelation)
            current.add_previous(previous_position, sconst.JonctionRelation)
            return (previous, current)
        if current.is_break():
            # حالة التنوين في آخر الجملة
            if previous.is_tanwin():
                previous.add_next(current_position, sconst.TanwinRelation)
                return (previous, current)
                # فعل متعدي بحرف
            #ToDo:
            if previous.is_verb() and (current.is_stopword() or current.has_jar()) :
                if  (current.has_jar() or current.is_indirect_transitive_stopword()) and previous.is_indirect_transitive() :
                    # Todo Has jar if it's كاف التشبيه
                    weight = sconst.VerbParticulRelation
              # جملة مقول القول    
            if current.is_pounct():
                #print "anasyn", 381, "Kala", previous.get_original().encode('utf8')
                if previous.get_original() == u"قَالَ":
                    #if the current is pounctuation and the previous is a speach verb, 
                    previous.add_next(current_position, sconst.VerbObjectRelation)
                    return (previous, current)                    
            
        else: # current is not a break
            #~ print "anasyn 10"       
            if previous.is_noun():
                #~ print "anasyn 11"
                weight = self.treat_previous_noun(previous, current)    
            elif previous.is_verb():
                #~ print "anasyn 12"                
                weight = self.treat_previous_verb(previous, current)
            #~ print "anasyn 13"                
            # a stopword can also be a verb or a noun            
            if not weight and previous.is_stopword():
            #~ if previous.is_stopword():
                #~ print "anasyn 14", weight, previous.get_word()
                weight = self.treat_previous_stopword(previous, current)
                #~ print "anasyn 15", weight
            #العدد والمعدود، التمييز
            # quantity case
            #the previous is a number, 
            if previous.is_number():
                weight = self.is_number_relation(previous, current)
    
        if weight :
            # add to the previous a pointer to the next word order.
            previous.add_next(current_position, weight)

            # add to the current word case a pointer 
            #to the previous word order.
            current.add_previous(previous_position, weight)
            
            if self.syntax_train_enabled:
                self.add_cache_relation(previous, current, weight)
        return previous, current


    def treat_initial(self, previous, current, previous_position, current_position):
        """
        Treat Initial case, where the current case is the first in the list
        @param previous: the previous case
        @type previous: stemmedSynWord
        @param next: the current case
        @type current: stemmedSynWord
        @return: (previous, current) after treatment
        @rtype: tuple of stemmedSynWord
        """
        if current.is_marfou3() or current.is_past() or current.is_stopword():
            # if the previous is None, that means 
            #that the previous is initiatl state
            # the current word is prefered, we add previous
            # pointer to 0 position.
            current.add_previous(previous_position, sconst.PrimateRelation)
        return (previous, current)


    def treat_final(self, previous, current,previous_position, current_position):
        """
        Treat final cases, where the current case is the end of line
        @param previous: the previous case
        @type previous: stemmedSynWord
        @param next: the current case
        @type current: stemmedSynWord
        @return: (previous, current) after treatment
        @rtype: tuple of stemmedSynWord
        """
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
            previous.add_next(current_position, sconst.TanwinRelation)
        return (previous, current)

    def treat_previous_noun(self, previous, current):
        """
        Treat noun cases, where the previous is a noun
        @param previous: the previous case
        @type previous: stemmedSynWord
        @param next: the current case
        @type current: stemmedSynWord
        @return: (previous, current) after treatment
        @rtype: tuple of stemmedSynWord
        """
        weight = 0
        #~ print "anasyn 6", previous.get_vocalized(), previous.is_noun(), previous.is_pronoun()
        #~ print "anasyn 7", current.get_vocalized(), previous.is_verb()
        if current.is_break() or not previous.is_noun():
            return 0

              # المضاف والمضاف إليه
            # إضافة لفظية
            # مثل لاعبو الفريق
        if current.is_noun():
            #~ if current.is_majrour() :
                #~ if previous.is_addition():
                    #~ weight = sconst.AdditionRelation
                #~ elif ((previous.is_additional())
                      #~ and (not (current.is_adj() and not current.is_defined()) 
                        #~ or  current.is_defined() )
                    #~ ):
                    #~ weight = sconst.AdditionRelation
            if previous.need_addition() and current.is_additionable():
                weight = sconst.AdditionRelation
            # منعوت والنعت
            #  تحتاج إلى إعادة نظر
            # بالاعتماد على خصائص الاسم الممكن أن يكون صفة
            if self.are_compatible(previous, current):
                #~ print "adj-1", (u"\t".join([current.get_word(), previous.get_word()])).encode('utf8')
                if current.is_adj() :#and (current.is_defined() or current.is_tanwin()):
                    weight = sconst.DescribedAdjectiveRelation
            #مبتدأ وخبر
            elif self.are_nominal_compatible(previous, current):
                if current.is_adj():
                    # مبتدأ مرفوع خبر مرفوع 
                    if  previous.is_marfou3() and current.is_marfou3():
                        weight = sconst.PrimatePredicateRelation  
                     # مبتدأ منصوب خبر مرفوع# اسم كان
                    elif (previous.is_mansoub() and current.is_marfou3()):
                        weight = sconst.PrimateMansoubPredicateRelation                        

                    elif (previous.is_marfou3() and current.is_mansoub()):
                        weight = sconst.PrimatePredicateMansoubRelation                         
            #~ else:
                #~ print "adj-2", (u"\t".join([current.get_word(), previous.get_word()])).encode('utf8')
        elif current.is_verb():
            # الجارية فعل والسابق مبتدأ
            if self.compatible_subject_verb(previous, current):
                # Todo treat the actual word
                weight = sconst.Rafe3Marfou3Relation 
        if not weight and current.is_confirmation():
            weight = sconst.ConfirmationRelation
        #~ print "anasyn", weight
        return weight                

    def treat_previous_verb(self, previous, current):
        """
        Treat verb cases, where the previous is a noun
        @param previous: the previous case
        @type previous: stemmedSynWord
        @param next: the current case
        @type current: stemmedSynWord
        @return: (previous, current) after treatment
        @rtype: tuple of stemmedSynWord
        """
        weight = 0
        if current.is_break() or not previous.is_verb():
            return 0                       


        if current.is_noun():
            #~ if current.is_marfou3() or current.is_mabni():
            if current.is_marfou3():
                if previous.is3rdperson() and previous.is_single():
                    # Todo treat the actual word
                    # الفعل والفاعل أو نائبه
                    if not previous.is_passive():
                        if True or ((current.is_feminin() and previous.is3rdperson_feminin())
                           or (not current.is_feminin() and previous.is3rdperson_masculin())):
                            # if the verb is a factor
                            if previous.is_kana_rafe3():
                                weight = sconst.KanaRafe3Marfou3Relation
                            # كاد وأخواتها
                            
                            else:
                                weight = sconst.VerbSubjectRelation
                           
                    else: # passive verb
                        if ((current.is_feminin() and previous.is3rdperson_feminin())
                           or (not current.is_feminin() and previous.is3rdperson_masculin())):
                            weight = sconst.VerbPassiveSubjectRelation
    # الفعل والمفعول به     
            #~ print "12",current.is_mansoub(), current.is_majrour(), current.is_marfou3()
            if current.is_mansoub() or current.is_mabni():
            #elif current.is_mansoub():
                #~ #print "1-2"
                if not previous.is_passive():
                    if not previous.has_encletic() and previous.is_transitive():
                        weight = sconst.VerbObjectRelation

        return weight                            

    def treat_previous_stopword(self, previous, current):
        """
        Treat stopword cases, where the previous is a stopword
        @param previous: the previous case
        @type previous: stemmedSynWord
        @param next: the current case
        @type current: stemmedSynWord
        @return: (previous, current) after treatment
        @rtype: tuple of stemmedSynWord
        """
        weight = 0
        if current.is_break() or not previous.is_stopword():
            return 0
        # جار ومجرور
        #مضاف ومضاف إليه
        if current.is_noun():
            if previous.is_jar():
                #~ if (current.is_majrour() or current.is_mabni() ):
                if current.is_majrour():
                    weight = sconst.JarMajrourRelation

            # اسم إنّ منصوب
            elif previous.is_naseb():
                #~ if (current.is_mansoub() or current.is_mabni() ):
                if current.is_mansoub():
                    weight = sconst.InnaNasebMansoubRelation

            elif previous.is_initial() and  current.is_marfou3():
                weight = sconst.PrimateRelation

            # اسم كان وأخواتها
            elif previous.is_kana_rafe3() and current.is_marfou3():
                weight = sconst.KanaRafe3Marfou3Relation
            elif previous.is_rafe3():
                #~ if (current.is_marfou3() or current.is_mabni() ):
                if current.is_marfou3() :
                    weight = sconst.Rafe3Marfou3Relation
                #~ # خبر إنّ لمبتدإ ضمير متصل
                #~ elif current.is_marfou3():
                    #~ if previous.has_encletic():
                        #~ weight = sconst.InnaRafe3Marfou3Relation 
            if previous.is_substituted():
                   
                if (previous.is_mansoub() and current.is_mansoub()):
                    weight = sconst.SubstitutionMansoubRelation                         
                elif (previous.is_marfou3() and current.is_marfou3()):
                    weight = sconst.SubstitutionMarfou3Relation                         
                elif (previous.is_majrour() and current.is_majrour()):
                    weight = sconst.SubstitutionMajrourRelation                     

        # pronoun verb
        elif current.is_verb():
            if self.compatible_subject_verb(previous, current):
            # تطابق الضمير مع الضمير المسند إليه
                weight = sconst.SubjectVerbRelation
        #verb
            #if previous.is_verbal_factor():
            if current.is_present():
                if previous.is_jazem() and current.is_majzoum():
#حالة خاصة لا الناهية تنهى عن الأفعال
# المسندة للضمير المخاطب فقط
                    if previous.get_unvoriginal() == u'لا':
                        if current.has_imperative_pronoun():
                           weight = sconst.JazemMajzoumRelation 
                    else:
                        weight = sconst.JazemMajzoumRelation
                elif previous.is_verb_naseb() and  current.is_mansoub():
                    weight = sconst.NasebMansoubRelation
                elif previous.is_verb_rafe3() and current.is_marfou3():
                    #حالة لا النافية 
                    # المسندة لغير الضمائر المخاطبة
                    if previous.get_unvoriginal() == u'لا':
                        if not current.has_imperative_pronoun():
                           weight = sconst.Rafe3Marfou3Relation
                    else:
                        weight = sconst.Rafe3Marfou3Relation
            if previous.is_condition_factor():
                weight = sconst.ConditionVerbRelation
            if previous.is_verb_jobless_factor():
                weight = sconst.JoblessFactorVerbRelation
        if previous.is_jonction():
            weight = sconst.JonctionRelation
        #~ print "anasyn", previous.get_vocalized(), current.is_mansoub(), current.get_vocalized(), weight, current.get_tags()
        return weight

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
        #~ return True
        #الكلمتان اسمان
        if (not ((previous.is_noun() or previous.is_addition()) and 
        current.is_noun())):
            return False
        compatible = False
        # التعريف
        # إمّا معرفان معا، أو نكرتان معا
        #~ if not xor(current.is_defined() , previous.is_defined()):
            #~ compatible = True
        #~ else:
            #~ return False
        #~ # التنوين
        #~ if not xor(current.is_tanwin() , previous.is_tanwin()):
            #~ compatible = True
        #~ else:
            #~ return False
        if current.eq_defined(previous):
            compatible = True
        else:
            return False

        # التذكير والتأنيث
        # مذكر ومذكر
        #مؤنث ومؤنث
        # جمع التكسير مؤنث
        if current.eq_gender(previous):
        #~ if ((current.is_feminin() and previous.is_feminin()) 
           #~ or (current.is_masculin() and previous.is_masculin())
        #~ ):
            compatible = True
            # تحتاج إلى استكمال بعد أن يتم تحديد نوع كل اسم في القاموس
        #~ else: return False

        # العدد
        # والتثنية والإفراد الجمع
        # إمّا مفردان معا، أو جمعان معا أو مثنيان معا
        #~ if ((current.is_plural() and previous.is_plural()) 
             #~ or  (current.is_dual() and previous.is_dual())
            #~ or (current.is_single() and previous.is_single())
            #~ or (current.is_single() and current.is_feminin() and
             #~ previous.is_plural() and previous.is_feminin())
#~ ):
        if current.eq_number(previous) or (current.is_single() and current.is_feminin() and
             previous.is_plural() and previous.is_feminin()):
            compatible = True
        else:
            return False
        # الحركة
        # تساوي الحالة الإعرابية
        #~ if (current.is_majrour() and previous.is_majrour()) \
            #~ or (current.is_mansoub() and previous.is_mansoub()) \
            #~ or (current.is_marfou3()and previous.is_marfou3()):
        if current.eq_case(previous):            
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
        #ToDo: fix feminin and masculin cases
        #~ if not xor (current.is_feminin(), previous.is_feminin()):
            #~ compatible = True
        #~ else:
            #~ return False
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
        if not previous.is_noun():
            return False
        #الكلمتان اسمان

        compatible = False
        if current.is_noun():
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
            #~ if (previous.is_inna_noun() and previous.is_mansoub() \
            #~ and current.is_marfou3()) or (previous.is_kana_noun() \
             #~ and previous.is_marfou3() and current.is_mansoub())\
            #~ or (not previous.is_inna_noun() and not previous.is_kana_noun() \
            #~ and previous.is_marfou3() and current.is_marfou3()):
                #~ compatible = True
                        # مبتدأ مرفوع خبر منصوب#  اسم إنّ
            if ((previous.is_mansoub() and current.is_marfou3())
                         # مبتدأ منصوب خبر مرفوع# اسم كان
             or (previous.is_marfou3() and current.is_mansoub())
            # مبتدأ مرفوع خبر مرفوع
            or (previous.is_marfou3() and current.is_marfou3())):
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
            #~ if ((current.is_plural() and previous.is_plural()) 
                 #~ or  (current.is_dual() and previous.is_dual())
                #~ or (current.is_single() and previous.is_single())):
            if current.eq_number(previous):
                compatible = True
            else:
                return False
            # التذكير والتأنيث
            # مذكر ومذكر
            #مؤنث ومؤنث
            # جمع التكسير مؤنث: عولجت هذه المسألة في الدالة Is_feminin
            #~ if  ((current.is_feminin() and previous.is_feminin()) 
             #~ or (current.is_masculin() and previous.is_masculin())
                #~ ):
            if current.eq_gender(previous):                    
                compatible = True
            else: return False
        #الأول اسم والثاني فعل
        elif current.is_verb():

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
            #~ if ((current.is_plural() and previous.is_plural()) 
                 #~ or  (current.is_dual() and previous.is_dual())
                #~ or (current.is_single() and previous.is_single())):
            if current.eq_number(previous):
                compatible = True
            else:
                return False
# الضمير
            #~ if  ((current.is_speaker_person() and previous.is_speaker_person()) 
             #~ or (current.is_present_person() and previous.is_present_person())
             #~ or (current.is_absent_person() and previous.is_absent_person())
                #~ ):
            if current.eq_person(previous):
                compatible = True
            else: return False
            # التذكير والتأنيث
            # مذكر ومذكر
            #مؤنث ومؤنث
            #~ if  ((current.is_feminin() and previous.is_feminin()) 
             #~ or (current.is_masculin() and previous.is_masculin())
                #~ ):
            if current.eq_gender(previous):
                compatible = True
                
            else: return False
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
        # لا يلتصق المبتدأ مع فعل مجزوم أو منصوب
        # في المضارع
        #~ print 'anasyn', previous.get_vocalized(), previous.is_pronoun(), previous.is_stopword()
        if current.is_majzoum() or current.is_mansoub():
            return False
        if previous.is_stopword():
            #~ print "anasyn.py", previous.get_word(), previous.is_pronoun()
            if (previous.is_pronoun() and current.is_verb()):
                # الضمير مطابق لضمير الفعل
                if previous.is_pronoun():
                    expected_pronouns = sconst.TABLE_PRONOUN.get(current.get_pronoun(), [])
                    #~ print "anasyn.py", "anasyn 4", u"\t".join([previous.get_vocalized(),u', '.join(expected_pronouns)]).encode('utf8')
                    if previous.get_original() in expected_pronouns:
                        compatible = True
            #~ print 'anasyn 3', compatible
            #الضمير المتصل مطابق لضمير الفعل
            #Todo fix is_added function
            #~ if True or previous.is_added():
            if previous.is_added():
                expected_pronouns = sconst.TABLE_PRONOUN.get(current.get_pronoun(), [])
                #~ print "is_added",previous.is_added(),  u"\t".join([previous.get_vocalized(), previous.get_encletic(),u", ".join(expected_pronouns)]).encode('utf8')
                if previous.get_encletic() in expected_pronouns:
                    compatible = True
            #~ print 'anasyn 2', compatible
                    
            
        else:
            # المبتدأ معه فعل يتطلب أن يكون إما معرفة أو منونا
            if (previous.is_defined() or previous.is_tanwin()  or previous.has_encletic()):
                compatible = True
            else:
                return False
            # والتثنية والإفراد الجمع
            #~ if ((current.is_plural() and previous.is_plural()) 
                 #~ or  (current.is_dual() and previous.is_dual())
                #~ or (current.is_single() and previous.is_single())):
            if current.eq_number(previous):
                compatible = True
            else:
                return False
# الضمير
            #~ if  ((current.is_speaker_person() and previous.is_speaker_person()) 
             #~ or (current.is_present_person() and previous.is_present_person())
             #~ or (current.is_absent_person() and previous.is_absent_person())
                #~ ):
            if current.eq_person(previous):
                compatible = True
            else: return False
            # التذكير والتأنيث
            # مذكر ومذكر
            #مؤنث ومؤنث
            #~ if  ((current.is_feminin() and previous.is_feminin()) 
             #~ or (current.is_masculin() and previous.is_masculin())
                #~ ):
            if current.eq_gender(previous):
                compatible = True
            else: return False
            # جمع التكسير مؤنث
            # else: return False
            #الفعل مرفوع أو مبني
            if current.is_past() or (current.is_present() and\
             current.is_marfou3()):
                compatible = True
            else:
                return False
        #~ print "anasyn", compatible
        return compatible


    def are_compatible_relations(self, previous, current):
        """
        verify the gramatica relation between three words are compatible.
           دراسة الترابط النحوي بين ثلاث كلمات بواسطة علاقتها، اي توافق العلاقتين، لا سيما في التبعية والبدل.
        If the current relation can be compatible with the previous relation
        @param previous: the relation choosen by the tashkeel process.
        @type previous:int 
        @param current: the current relation.
        @type current: int 
        @return: return if the two relations are compatible syntaxicly.
        @rtype: boolean
        """
        # substitutions
        if current == sconst.SubstitutionMajrourRelation :
            if u"جر" in sconst.RELATIONS_TAGS.get(previous,""):
                return True;
            else :
                return False
        if current == sconst.SubstitutionMansoubRelation :
            if u"نصب" in sconst.RELATIONS_TAGS.get(previous,""):
                return True;
            else :
                return False
        if current == sconst.SubstitutionMarfou3Relation :
            if u"رفع" in sconst.RELATIONS_TAGS.get(previous,""):
                return True;
            else :
                return False
        # relation of "subject verb" with "verb subject"
        #علاقة مبتدأ فعل مع علاقة فعل وفاعل
        if current == sconst.VerbSubjectRelation and previous == sconst.SubjectVerbRelation :
            return False;
        # relation of "subject verb" with "verb subject"
        #علاقةالاسم الموصول من مع بقية  العلاقة فعل وفاعل
        elif current == sconst.VerbSubjectRelation and previous == sconst.ConditionVerbRelation :
            return False;
            
            
        #  Premate is mansoub by INNA, Predicate is marfou3
       #مبتدأ مرفوع وخبر منصوب
        if current == sconst.PrimateMansoubPredicateRelation and not previous == sconst.InnaNasebMansoubRelation :
            return False;
        #  Premate is Mrfou3 by Kana, Predicate is mansoub
        #مبتدأ مرفوع، خبر منصوب
        elif current == sconst.PrimatePredicateMansoubRelation and not previous == sconst.KanaRafe3Marfou3Relation :
            return False; 
         # منع حالات رفع المبتدا والخبر إن كانمسبوقا بناسخ   
        #  Premate is mansoub by INNA, Predicate is marfou3
       #مبتدأ مرفوع وخبر منصوب
        if current == sconst.PrimatePredicateRelation:
            if previous == sconst.InnaNasebMansoubRelation :
                return False;
        #  Premate is Mrfou3 by Kana, Predicate is mansoub
        #مبتدأ مرفوع، خبر منصوب
            elif previous == sconst.KanaRafe3Marfou3Relation :
                return False; 
                       
        return True

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
    def enable_allow_cache_use(self):
        """
        Allow the anasyntax to use Cache to reduce calcul.
        """
        self.syntax_train_enabled = True

    def disable_allow_cache_use(self):
        """
        Not allow the anasyntax to use Cache to reduce calcul.
        """
        self.syntax_train_enabled = False
        
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
                for key in sorted(stmword.keys()):
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
    text = u"إلى البيت"
    import qalsadi.analex
    result = []
    analyzer = qalsadi.analex.Analex()
    anasynt = SyntaxAnalyzer()
    result = analyzer.check_text(text)
    result, synodelist  = anasynt.analyze(result)
    # the result contains objects
    text2display = anasynt.display(result)
    try:
        print(str(text2display))
    except UnicodeEncodeError:
        print(text2display.encode('utf8'))
        
if __name__ == "__main__":
    mainly()

