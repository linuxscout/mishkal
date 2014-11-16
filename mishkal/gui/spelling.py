#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
__license__ = 'MIT'
__copyright__ = '2009, John Schember '
__docformat__ = 'restructuredtext en'
 
import re
import sys
import pyarabic.araby as araby 
#import enchant
 
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
class myspeller:
	def __init__(self):
		self.dict={};
	def check(self, word):
		key=araby.strip_tashkeel(word);
		if self.dict.has_key(key):
			return False;
		else:
			return True;
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
            orginaltext = unicode(self.textCursor().selectedText())
            arabicmarks = [u'؟',u'،',u'؛',u'“',u'”',u'‘',u'’']
            holder = orginaltext[-1]
            if holder in arabicmarks:
                self.pretxt = holder
            else:
                self.pretxt=''
            text = orginaltext.strip(u'؟،؛“”‘’')            
            if not self.dict.check(text):
                spell_menu = QMenu(u'اقتراحات التشكيل')
                spell_menu.setLayoutDirection(RightToLeft)
                for word in self.dict.suggest(text):
                    action = SpellAction(word, spell_menu)
                    action.correct.connect(self.correctWord)
                    spell_menu.addAction(action)
                spell_menu.setStyleSheet("QMenu {font: 24px;  margin: 2px;}")						
                # Only add the spelling suggests to the menu if there are
                # suggestions.
                if len(spell_menu.actions()) != 0:
                    popup_menu.insertSeparator(popup_menu.actions()[0])
                    popup_menu.insertMenu(popup_menu.actions()[0], spell_menu)
 
        popup_menu.exec_(event.globalPos())
 
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
