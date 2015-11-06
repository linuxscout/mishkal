#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
__license__ = 'MIT'
__copyright__ = '2009, John Schember '
__docformat__ = 'restructuredtext en'
 
import re
import sys

import pyarabic.araby as araby 
#import enchant
import os
from PyQt4.Qt import QAction
from PyQt4.Qt import QApplication
from PyQt4.Qt import QEvent
from PyQt4.Qt import QMenu
from PyQt4.Qt import QMouseEvent
from PyQt4.Qt import QPlainTextEdit
from PyQt4.Qt import QSyntaxHighlighter
from PyQt4.Qt import QTextCharFormat
from PyQt4.Qt import QTextCursor
from PyQt4.Qt import QTextOption
from PyQt4.Qt import Qt
from PyQt4.QtCore import pyqtSignal

import customdictionary



class myspeller:
    def __init__(self):
        self.dict={};
        self.custom_dict = customdictionary.CustomizedDictionary();
    def check(self, word):
        key = araby.strip_tashkeel(word);
        if self.dict.has_key(key):
            return True;
        else:
            return False;
    def add(self, word, suggestList):
        if word!=u"" and  suggestList!=[] and  type(suggestList).__name__=='list': 
            #ToDo: adding different suggestion into one list;
            # NB: this is time eater because if the word is frequent.
            # if self.dict.has_key(word):
                # # if the dict has previous suggestions for the word,
                # # add new suggestions and remove duplicata;
                # suggestList+=self.dict[word];
                # suggestList=set(suggestList);
                # self.dict[word]=suggestList;
            #else:
            self.dict[araby.strip_tashkeel(word)]=suggestList;
    def suggest(self, word):
        key=araby.strip_tashkeel(word)
        if self.dict.has_key(key):
            return self.dict[key];
        return [];
    def __del__():
        del (self.custom_dict)
class SpellTextEdit(QPlainTextEdit):
 
    def __init__(self, *args):
        QPlainTextEdit.__init__(self, *args)
        # Default options to RightToleft
        options=QTextOption();
        options = self.document().defaultTextOption();
        options.setAlignment(Qt.AlignRight);
        options.setTextDirection(Qt.RightToLeft);
        self.document().setDefaultTextOption(options)
        # Default dictionary based on the current locale.
        self.dict = myspeller()
        # self.highlighter = Highlighter(self.document())
        # self.highlighter.setDict(self.dict)
        self.pretxt=''
 
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # Rewrite the mouse event to a left button event so the cursor is
            # moved to the location of the pointer.
            event = QMouseEvent(QEvent.MouseButtonPress, event.pos(),
                Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        QPlainTextEdit.mousePressEvent(self, event)
 
    def contextMenuEvent(self, event):
        popup_menu = self.createStandardContextMenu()
        #~popup_menu = QMenu()
        #~self.setContextMenuPolicy()
        RightToLeft = 1;
        # Select the word under the cursor.
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        self.setTextCursor(cursor)
 
        # Check if the selected word is misspelled and offer spelling
        # suggestions if it is.
        if self.textCursor().hasSelection():
            

            
            #~text = (unicode(self.textCursor().selectedText()))
            #this is a workaround for QT bug when double click selects Arabic punctuation marks
            # plus the word in the text editor see https://bugreports.qt-project.org/browse/QTBUG-42397
            originaltext = unicode(self.textCursor().selectedText())
            
            arabicmarks = [u'؟',u'،',u'؛',u'“',u'”',u'‘',u'’']
            holder = originaltext[-1]
            if holder in arabicmarks:
                self.pretxt = holder
            else:
                self.pretxt=''
            text = originaltext.strip(u'؟،؛“”‘’')   

            # the word is aleady analyzed         
            if self.dict.check(text):
                spell_menu = QMenu(u'المزيد...')
                spell_menu.setLayoutDirection(RightToLeft)
                suggests = self.dict.suggest(text)
                for word in suggests[:10]:
                    action = SpellAction(word, spell_menu)
                    action.correct.connect(self.correctWord)
                    #~spell_menu.addAction(action)
                    popup_menu.addAction(action)

                    
                #~spell_menu.setStyleSheet("QMenu {font: 32px;  margin: 2px;}")
                popup_menu.setStyleSheet("QMenu {font: 24px;}")
                # Only add the spelling suggests to the menu if there are
                # suggestions.
                
                #~if len(spell_menu.actions()) != 0:
                    #~popup_menu.insertSeparator(popup_menu.actions()[0])
                    #~popup_menu.insertMenu(popup_menu.actions()[0], spell_menu)
                if len (suggests)>10:
                    for word in suggests[10:]:
                        action = SpellAction(word, spell_menu)
                        action.correct.connect(self.correctWord)
                        #~spell_menu.addAction(action)
                        spell_menu.addAction(action)                    
                    spell_menu.setStyleSheet("QMenu {font: 24px;}")
                    
                    popup_menu.addSeparator()
                    popup_menu.addMenu(spell_menu)
                
                if len(suggests) == 1 and not araby.is_vocalized(suggests[0]):
                    addtodict_action = popup_menu.addAction(u'أضف للقاموس')
                    #~addtodict_action.triggered.connect( lambda x = x = originaltext: self.add_to_dict(x))
                    addtodict_action.triggered.connect( lambda : self.add_to_dict(originaltext))
                    # if the word hs no suggestions
                    # we lookup for customized vocalization
                    suggests = self.dict.custom_dict.lookup(word)
                    for word in suggests:
                        action = SpellAction(word, spell_menu)
                        action.correct.connect(self.correctWord)
                        #~spell_menu.addAction(action)
                        popup_menu.addAction(action)                    
                    
                    
            else:
                # redo taskeel for this word
                #~pass;
                # if the word hs no suggestions
                # we lookup for customized vocalization
                suggests = self.dict.custom_dict.lookup(text)
                for word in suggests:
                    action = SpellAction(word, spell_menu)
                    action.correct.connect(self.correctWord)
                    #~spell_menu.addAction(action)
                    popup_menu.addAction(action)
        popup_menu.exec_(event.globalPos())
    def add_to_dict(self, text):
        """
        Add non vocalized words with user vocalization into a dictionary to be used as feed back
        """
        print "Added word", text.encode('utf8')
        self.dict.custom_dict.add(text)
    
    def correctWord(self, word):
        '''
        Replaces the selected text with word.
        '''
        cursor = self.textCursor()
        cursor.beginEditBlock()
 
        cursor.removeSelectedText()
        cursor.insertText(word + self.pretxt)
 
        cursor.endEditBlock()
 
 
 
class SpellAction(QAction):
 
    '''
    A special QAction that returns the text in a signal.
    '''
 
    correct = pyqtSignal(unicode)
 
    def __init__(self, *args):
        QAction.__init__(self, *args)
 
        self.triggered.connect(lambda x: self.correct.emit(
            unicode(self.text())))

            
 
def main(args=sys.argv):
    app = QApplication(args)
 
    spellEdit = SpellTextEdit()
    spellEdit.show()
 
    return app.exec_()
 
if __name__ == '__main__':
    sys.exit(main())
