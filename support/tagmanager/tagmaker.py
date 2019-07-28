#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tag_const.py
#  
#  Copyright 2018 zerrouki <zerrouki@majd4>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    division,
    )
if __name__ == "__main__":
    import tag_const 
    import tagconfig
else:
    from . import tag_const 
    from . import tagconfig

import pandas as pd

    
class tagMaker:
    """
    Manage tags, create, code, decode a tag
    """

    def __init__(self,):
        # read config fist
        #~ self.load_config()
        if not tag_const.TAGSDICT:
            configueur = tagconfig.tagConfig()
            configueur.load_config()
        # prepare the tag maker
        self.reset()
        
    def reset(self,):
        """ reset the taglist to mane a new"""
        # init taglist
        self.taglist = []
        for i in range(len(tag_const.TAG_PARTS_SIZES)):
            self.taglist.append(['-']*tag_const.TAG_PARTS_SIZES[i])

    def __str__(self,):
        """ prepare list to be printed"""
        # join sub lists without separater, 
        # the join parts by separator
        return  tag_const.TAG_PARTS_SEP.join([u"".join(x) for x in self.taglist])
    @staticmethod
    def repr(obj):
        """
        """
        if type(obj) is dict:
            return  repr(obj).replace("},","},\n").decode('unicode-escape') 
        else:
            return  repr(obj).decode('unicode-escape')             
 
    def add(self, tag):
        """ add a new tag to the taglist
        @param tag: a tag 
        @ptype tag: unicode
        """
        debug = False
        # if tag names are differents, it can contain many tags
        taglist =[]
        if not tag in tag_const.TAGSDICT:
            taglist = tag_const.TAGSMAP.get(tag,[])
            if debug: print("***",u";;".join(taglist).encode('utf8'))
        else:
            taglist =[tag,]
        # if the tag exist in tagsdict configuration
        # choose value and add it to a position
        for tg in taglist:
            if tg in tag_const.TAGSDICT:
                if debug: print("***//",tg.encode('utf8'))
                part = tag_const.TAGSDICT[tg]['part'] -1
                pos = tag_const.TAGSDICT[tg]['pos']-1
                code = tag_const.TAGSDICT[tg]['code']
                self.taglist[part][pos] = code


    def encode(self, taglist = []):
        """
        Decode a string tag to get all tags
        """
        if not taglist:
            return u""
        for tag in taglist:
            self.add(tag)
        return self.__str__()
        
    def decode(self, tagstring = False):
        """
        Decode a string tag to get all tags
        """
        if not tagstring:
            tagsting = self.__str__()
        parts = tagsting.split(tag_const.TAG_PARTS_SEP)
        
        tags = []
        # read codes
        for ip, part in enumerate(parts):
            for i in range(len(part)):
                code = part[i]
                key = u":".join([str(ip+1), str(i+1), code])
                #~ print key
                tag = tag_const.INVERSE_TAGSDICT.get(key,{}).get('ar_value',"")
                attr = tag_const.INVERSE_TAGSDICT.get(key,{}).get('ar_attr',"")
                if tag:
                    tags.append((attr, tag))
                
        return tags
        
    def inflect_noun(self, tagstring):
        """
        get inflectionfor a noun
        """
        if not tagstring:
            tagsting = self.__str__()
        inflct = []
        if self.has_tag(u"اسم", tagstring):
             # inflect = Syntaxtic classe
             # مفعول به منصوب وعلامة نصبه الفتحة
             #نعت منصوب وعلامةنصبه الياء لأنه مثنى
             #مبتدأ مرفوع وعلامة رفعه الواو لأنه جمع مذكر سالم
            # case
            case = self.get_inflect(u'إعراب', tagstring)
            if case:
                case_part = u"اسم %s"%case
                inflct.append(case_part)
                # Jar
                if self.has_tag(u"مجرور", tagstring):
                    jar = self.get_inflect(u'جر', tagstring)
                    if jar:
                        jar_part = jar
                        inflct.append(jar_part)
                # inflect Mark
                mark =self.get_inflect(u'علامة', tagstring)
                mark_value =self.get_value(u'علامة', tagstring)
                if mark:
                    #علامة الإعراب
                    # وعلامة رفعه الضمة
                    mark_part =""
                    # علة علامة الإعراب
                    # وعلامة رفعه الألف لأنه مثنى
                    cause_part =""
                    if case == u"مبني":
                        mark_part = u"على %s"%mark
                    else:
                        # استخراج الحالة
                        #~ مرفوع => رفعه
                        #~ منصوب => نصبه
                        #~ مجرور => جره
                        case_mark = ""
                        if case == u"مرفوع":
                            case_mark = u"رفعه"
                        elif case == u"منصوب":
                            case_mark = u"نصبه"
                        elif case == u"مجرور":
                            case_mark = u"جرّه"
                        
                        mark_part = u"وعلامة %s %s"%(case_mark, mark)
                        
                        # mark cause
                        
                        if self.has_tag(u"مثنى", tagstring):
                            cause_part = u"لأنه مثنى"
                        elif self.has_tag(u'مؤنث', tagstring) and self.has_tag(u"جمع", tagstring):
                            cause_part = u"لأنه جمع مؤنث سالم"                            
                        elif self.has_tag(u'مذكر', tagstring) and self.has_tag(u"جمع", tagstring):
                            cause_part = u"لأنه جمع مذكر سالم"                           
                        elif self.has_tag(u'مجرور', tagstring) and self.has_tag(u"ممنوع من الصرف", tagstring):
                            cause_part = u"لأنه ممنوع من الصرف"                           
                    inflct.append(mark_part)
                    inflct.append(cause_part)
                #attached pronoun
                add_p = self.get_inflect(u'ضمير متصل', tagstring)
                if add_p:
                    add_part = u"وهو مضاف، %s في محل جر مضاف إليه"%add_p
                    inflct.append(add_part)
            else: # no case
                word_type = self.get_value(u'نوع الكلمة', tagstring)
                if word_type:
                    inflct.append(word_type)  
        return u" ".join(inflct)
    def inflect_verb(self, tagstring):
        """
        get inflectionfor a noun
        """
        if not tagstring:
            tagsting = self.__str__()
        inflct = []
        if self.has_tag(u"فعل", tagstring):
             # inflect = Syntaxtic classe
             # مفعول به منصوب وعلامة نصبه الفتحة
             #نعت منصوب وعلامةنصبه الياء لأنه مثنى
             #مبتدأ مرفوع وعلامة رفعه الواو لأنه جمع مذكر سالم
            # case
            case = self.get_inflect(u'إعراب', tagstring)
            #~ print((u"###%s####"%case).encode('utf8'), tagstring)
            if case:
                case_part = u"فعل %s"%case
                inflct.append(case_part)

                # inflect Mark
                mark =self.get_inflect(u'علامة', tagstring)
                mark_value =self.get_value(u'علامة', tagstring)
                if mark:
                    #علامة الإعراب
                    # وعلامة رفعه الضمة
                    mark_part =""
                    # علة علامة الإعراب
                    # وعلامة رفعه الألف لأنه مثنى
                    cause_part =""
                    if case == u"مبني":
                        mark_part = u"على %s"%mark
                    else:
                        # استخراج الحالة
                        #~ مرفوع => رفعه
                        #~ منصوب => نصبه
                        #~ مجرور => جره
                        case_mark = ""
                        if case == u"مرفوع":
                            case_mark = u"رفعه"
                        elif case == u"منصوب":
                            case_mark = u"نصبه"
                        elif case == u"مجزوم":
                            case_mark = u"جزمه"
                        
                        mark_part = u"وعلامة %s %s"%(case_mark, mark)
                        
                        # mark cause
                        
                        condition_5verbs = (self.has_tag(u"مثنى", tagstring)
                        or (self.has_tag(u'مذكر', tagstring) and self.has_tag(u"جمع", tagstring))
                        or (self.has_tag(u'مؤنث', tagstring) and self.has_tag(u"مخاطب", tagstring) and self.has_tag(u"مفرد", tagstring))
                        )
                        if condition_5verbs:
                            cause_part = u"لأنه من الأفعال الخمسة"                            
                    inflct.append(mark_part)
                    inflct.append(cause_part)
                #attached pronoun
                add_p = self.get_inflect(u'ضمير متصل', tagstring)
                #~ print((u"H###%s####"%add_p).encode('utf8'))
                if add_p:
                    add_part = u"%s في محل نصب مفعول به"%add_p
                    inflct.append(add_part)
            else: # no case
                word_type = self.get_value(u'نوع الكلمة', tagstring)
                if word_type:
                    inflct.append(word_type)  
        return u" ".join(inflct)
    def inflect_tool(self, tagstring = False):
        """
        """
        return u""
    def inflect(self, tagstring = False):
        """
        Display inlfection in traditional way
        عرض إعراب الكلمة حسب التقاليد
        """
        if not tagstring:
            tagsting = self.__str__()
        inflct = []
        if self.has_tag(u"اسم", tagstring):
            return self.inflect_noun(tagstring)
        elif self.has_tag(u"فعل", tagstring):
            return self.inflect_verb(tagstring)
        elif self.has_tag(u"أداة", tagstring):
            return self.inflect_tool(tagstring)
        else:
            word_type = self.get_value(u'نوع الكلمة', tagstring)
            if word_type:
                inflct.append(word_type)            
        return u" ".join(inflct)

    def has_tag(self, tag, tagstring = False):
        """
        Decode a string tag to get all tags
        """
        if not tagstring:
            tagsting = self.__str__()
        parts = tagsting.split(tag_const.TAG_PARTS_SEP)
        if tag not in tag_const.TAGSDICT:
            return False
        else:
            part = tag_const.TAGSDICT[tag]['part']
            pos = tag_const.TAGSDICT[tag]['pos']
            code = tag_const.TAGSDICT[tag]['code']
            if parts[part-1][pos-1] == code:
                return True
            else:
                return False
        return False

    def exists_attr(self, attr, tagstring = False):
        """
        test if attribute is enabled, for example, جر is ok, if tag code is B, K, L, is not if code is '-'
        """
        deco = self.decode_attr(attr, tagstring)
        return bool(deco) 

    def get_value(self, attr, tagstring=False):
        """
        Return the value of attribute
        """
        deco = self.decode_attr(attr, tagstring)
        if deco: 
            return deco.get('ar_value','')
        return ''

    def get_inflect(self, attr, tagstring=False):
        """
        Return the inflect text of attribute
        """
        deco = self.decode_attr(attr, tagstring)
        if deco: 
            return deco.get('inflect','')
        return ''
            
            
    def decode_attr(self, attr, tagstring = False):
        """
        Decode an attribute
        """
        if not tagstring:
            tagsting = self.__str__()
        parts = tagsting.split(tag_const.TAG_PARTS_SEP)
        if attr not in tag_const.ATTR_TAGSDICT:
            return {}
        else:
            part = tag_const.ATTR_TAGSDICT[attr]['part']
            pos = tag_const.ATTR_TAGSDICT[attr]['pos']
            code = parts[part-1][pos-1]
            if code == '-':
                return {}
            else:
                key = u":".join([str(part), str(pos), code])
                return tag_const.INVERSE_TAGSDICT.get(key,{})
        return {}
        
if __name__ == "__main__":
    #~ configeur = tagconfig.tagConfig()
    #~ configeur.load_config()
    tag_maker = tagMaker()
    #~ tagstr = str(tag_maker)
    #~ print("----")
    #~ for tag in tag_const.TAGSDICT:
        #~ tagstr = str(tag_maker)
        #~ tag_maker.add(tag)
        #~ tagstr_new = str(tag_maker)
        #~ if tagstr == tagstr_new:
            #~ print(u" ".join(["error:old\t",  tagstr, tag, "\n     new:\t",  tagstr_new]).encode('utf8'))
        #~ else:
            #~ print(u" ".join([tag, tagstr_new]).encode('utf8')) 
        #~ decode_tags = tag_maker.decode()
        #~ df = pd.DataFrame(decode_tags)
        #~ print(df)
        #~ tag_maker.add(u"اسم")
        #~ print("******Inflect", tag_maker.inflect().encode('utf8'))
        #~ tag_maker.add(u"فعل")
        #~ print("***Verb***Inflect", tag_maker.inflect().encode('utf8'))
    tag_maker.reset()
    
    taglists = [[u'اسم', u'هاء', u'مجرور',],
                u'تعريف::مرفوع:متحرك:ينون:::'.split(":"),
                u'المضارع المعلوم:هو:::n:'.split(":"),
                u':مضاف:مجرور:متحرك:ينون:::'.split(':'),
                ]
    for taglist in taglists:
        tag_maker.reset()
        tag_maker.encode(taglist)
        print(u"+".join(taglist).encode('utf8'))
        print(str(tag_maker).encode('utf8'))
        print(tag_maker.repr(tag_maker.decode()).encode('utf8'))
    
    
