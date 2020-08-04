# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'qutrubgui.ui'
#
# Created: Mon Sep 28 14:46:07 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import random

#~ import PyQt4.QtCore
#~ import PyQt4.QtGui

#~ try:
    #~ from PyQt4.QtCore import QString
#~ except ImportError:
    #~ QString = str
    #~ unicode=str    
#~ import time

import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
import PyQt5.QtPrintSupport
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox

try:
    from PyQt5.QtCore import QString
except ImportError:
    QString = str
    unicode=str    
import time

import core.adaat
from .setting import *
from .spelling import *

#cONSTANT
myAPPLICATION_NAME=u"مشكال: تشكيل النصوص العربية"
PWD = os.path.dirname(__file__)


class WorkThread(QtCore.QThread):
    def __init__(self, parent=None, target=None, args=()):
        """
        This class is meant for heavy lifing that has to happen in a separate
        thread, to keep the UI responding.  It will take a callable `target'
        and execute it in a separate thread with the given `args'.  Please
        note that a reference to the thread object will be pre-pendend to the
        arguments list passed to th callable, to allow acces to the methods
        provided by this class to modify the progress bar used to show the
        user the progress of the work executed in the thread.
        """
        QtCore.QThread.__init__(self, parent)
        self.target = target
        self.args = (self,) + args

    def run(self):
        """
        This method is run in a separate thread by Qt.  Don't call this method
        explicitly: it is called implicitly after calling the `start()'
        method.  Executes the given target with the given arguments, prepended
        with a reference to this thread instance.
        """
        if self.target:
            self.target(*self.args)


    
class Ui_MainWindow(PyQt5.QtWidgets.QWidget):
    font_base=None;
    font_result=None;
    result={}


    def setupUi(self, MainWindow):
        #add a speller or tashkeel
        self.dict = myspeller();
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        self.MainWindow=MainWindow;
        self.font_base=None;
        self.font_result=QtGui.QFont(DefaultFont.family(),DefaultFont.pointSize(),DefaultFont.bold());
        self.result={}
        self.language="arabic"
        self.SuggestedVerbList=[];
#-----------------------------------------------
        self.font_base = QtGui.QFont()
        self.font_base.setFamily("KacstOne")
        self.font_base.setPointSize(12)
        self.font_base.setBold(True)



        RightToLeft=1;
        MainWindow.setLayoutDirection(RightToLeft)
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(789, 593)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
##        self.Label = PyQt5.QtWidgets.QLabel(self.centralwidget)
##        self.Label.setObjectName("Label")
##        self.gridLayout_3.addWidget(self.Label, 1, 1, 1, 1)
##        self.Label_2 = PyQt5.QtWidgets.QLabel(self.centralwidget)
##        self.Label_2.setObjectName("Label_2")
##        self.gridLayout_3.addWidget(self.Label_2, 2, 1, 1, 1)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_6 = PyQt5.QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        #self.TSearch = PyQt5.QtWidgets.QLineEdit(self.centralwidget)
        #self.TSearch.setEnabled(True)
        #self.TSearch.setMaximumSize(QtCore.QSize(500, 40))

        #self.TSearch.setFont(self.font_result)
        #self.TSearch.setObjectName("TSearch")
        #self.gridLayout_5.addWidget(self.TSearch, 0, 0, 1, 1)
        self.CBLexique = PyQt5.QtWidgets.QComboBox(self.centralwidget)
        self.CBLexique.hide();      
        self.CBLexique.setObjectName("CBLexique")

# add lexique
        self.tab_lexique=load_lexique();
        for i in range(len(self.tab_lexique)):
            name=self.tab_lexique[i]["name"]
##            print name;
            self.CBLexique.addItem(QString())
            self.CBLexique.setItemText(i,self.tab_lexique[i]["title"])
##        self.CBLexique.addItem(QtCore.QString())
##        self.CBLexique.addItem(QtCore.QString())

        self.gridLayout_5.addWidget(self.CBLexique, 0, 5, 1, 1)

#Explication option
        self.BLastMarkVocalization= PyQt5.QtWidgets.QCheckBox(self.centralwidget)
        self.BLastMarkVocalization.setObjectName("BLastMarkVocalization")
        self.BLastMarkVocalization.setText(u"تشكيل أواخر الكلمات")
        self.BLastMarkVocalization.setCheckState(Qt.Checked);
        self.gridLayout_5.addWidget(self.BLastMarkVocalization, 0, 2, 1, 1)

#Explication option
        self.BReducedVocalization= PyQt5.QtWidgets.QCheckBox(self.centralwidget)
        self.BReducedVocalization.setObjectName("BReducedVocalization")
        self.BReducedVocalization.setText(u"تشكيل مُختزَل")

        self.gridLayout_5.addWidget(self.BReducedVocalization, 1, 2, 1, 1)

# langige choice"

        self.CBLanguage= PyQt5.QtWidgets.QComboBox(self.centralwidget)
        self.CBLanguage.setObjectName("CBLanguage")
        self.CBLanguage.addItem(QString())
        self.CBLanguage.addItem(QString())
        self.CBLanguage.addItem(QString())
        self.CBLanguage.hide();
##        self.gridLayout_5.addWidget(self.CBLanguage, 0, 2, 1, 1)



        self.BVocalize = PyQt5.QtWidgets.QPushButton(self.centralwidget)

        self.BVocalize.setFont(self.font_base)
        self.BVocalize.setObjectName("BVocalize")
        self.gridLayout_5.addWidget(self.BVocalize, 0, 1, 1, 1)


        #Add remove tashkeel Button
        self.BRemoveTashkeel = PyQt5.QtWidgets.QPushButton(self.centralwidget)

        self.BRemoveTashkeel.setFont(self.font_base)
        self.BRemoveTashkeel.setObjectName("BRemoveTashkeel")
        self.gridLayout_5.addWidget(self.BRemoveTashkeel, 0, 3, 1, 1)

        #Add random text tashkeel Button
        self.BRandomText = PyQt5.QtWidgets.QPushButton(self.centralwidget)

        self.BRandomText.setFont(self.font_base)
        self.BRandomText.setObjectName("BRandomText")
        self.gridLayout_5.addWidget(self.BRandomText, 0, 4, 1, 1)

        self.horizontalLayout_6.addLayout(self.gridLayout_5)
        self.gridLayout_4.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.TabVoice = PyQt5.QtWidgets.QTabWidget(self.centralwidget)
        self.TabVoice.setFont(self.font_base)
        self.TabVoice.setObjectName("TabVoice")
        self.TabResult = QWidget()
        self.TabResult.setObjectName("TabResult")
        self.gridLayout_2 = QGridLayout(self.TabResult)
        self.gridLayout_2.setObjectName("gridLayout_2")




# Vocalized Result
        self.TabResultVocalized = QWidget()
        self.TabResultVocalized.setObjectName("TabResultVocalized")
        #self.ResultVocalized = PyQt5.QtWidgets.QTextEdit(self.centralwidget)
        self.ResultVocalized = SpellTextEdit(self.centralwidget)
        self.ResultVocalized.setObjectName("ResultVocalized")
        self.ResultVocalized.setPlainText("text")
        self.ResultVocalized.setFont(self.font_result)
        self.ResultVocalized.setLayoutDirection(RightToLeft)

        self.gridLayout_2Codepoint = QGridLayout(self.TabResultVocalized)
        self.gridLayout_2Codepoint.setObjectName("gridLayout_2Codepoint")
        self.gridLayout_2Codepoint.addWidget(self.ResultVocalized, 0, 0, 1, 1)
        self.TabVoice.addTab(self.TabResultVocalized, "")
        #add a contextual menu to suggest tashkeel
        #self.ResultVocalized.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #QtCore.QObject.connect(self.ResultVocalized, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.contextMenuEvent)



        self.gridLayout.addWidget(self.TabVoice, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = PyQt5.QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = PyQt5.QtWidgets.QMenuBar(MainWindow)
        self.menubar.setLayoutDirection(RightToLeft)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 789, 21))
        self.menubar.setObjectName("menubar")
        self.menu = PyQt5.QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
##        self.menu_6 = PyQt5.QtWidgets.QMenu(self.menu)
##        self.menu_6.setObjectName("menu_6")
        self.menu_2 = PyQt5.QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = PyQt5.QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = PyQt5.QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = PyQt5.QtWidgets.QMenu(self.menubar)
        self.menu_5.setObjectName("menu_5")
        self.menu_insert = PyQt5.QtWidgets.QMenu(self.menubar)
        self.menu_insert.setObjectName("menu_insert")       
        self.menu_tashkeel = PyQt5.QtWidgets.QMenu(self.menubar)
        self.menu_tashkeel.setObjectName("menu_tashkeel")   
        self.menu_convert = PyQt5.QtWidgets.QMenu(self.menubar)
        self.menu_convert.setObjectName("menu_convert")         
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = PyQt5.QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        # open file action
        # import or Open dialog
        self.AImport = PyQt5.QtWidgets.QAction(MainWindow)
        self.AImport.setObjectName("AImport")

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(PWD, 'ar/images/open.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AImport.setIcon(icon)
        # export text 
        self.AExport = PyQt5.QtWidgets.QAction(MainWindow)
        self.AExport.setObjectName("AExport")
        self.AExit = PyQt5.QtWidgets.QAction(MainWindow)
        self.AExit.setObjectName("AExit")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(PWD, 'ar/images/save.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AExport.setIcon(icon)
        self.AFont = PyQt5.QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(PWD, 'ar/images/font.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AFont.setIcon(icon)
        self.AFont.setObjectName("AFont")
        self.AZoomIn = PyQt5.QtWidgets.QAction(MainWindow)
        self.AZoomIn.setObjectName("AZoomin")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(PWD, 'ar/images/zoomin.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AZoomIn.setIcon(icon)
        self.AZoomOut = PyQt5.QtWidgets.QAction(MainWindow)
        self.AZoomOut.setObjectName("AZoomOut")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(PWD, 'ar/images/zoomout.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AZoomOut.setIcon(icon)     
        self.AAbout = PyQt5.QtWidgets.QAction(MainWindow)
        self.AAbout.setObjectName("AAbout")
        self.AManual = PyQt5.QtWidgets.QAction(MainWindow)
        self.AManual.setObjectName("AManual")
        self.ACopy = PyQt5.QtWidgets.QAction(MainWindow)
        self.ACopy.setObjectName("ACopy")
        icon.addPixmap(QtGui.QPixmap(os.path.join(PWD, 'ar/images/copy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ACopy.setIcon(icon)
        self.AWhoisqutrub = PyQt5.QtWidgets.QAction(MainWindow)
        self.AWhoisqutrub.setObjectName("AWhoisqutrub")
        self.ASetting = PyQt5.QtWidgets.QAction(MainWindow)
        self.ASetting.setObjectName("ASetting")
        self.APrint = PyQt5.QtWidgets.QAction(MainWindow)
        self.APrint.setObjectName("APrint")
        icon.addPixmap(QtGui.QPixmap(os.path.join(PWD, 'ar/images/print.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.APrint.setIcon(icon)
        self.menu.addAction(self.AImport)
        self.menu.addAction(self.AExport)
        self.menu.addSeparator()
        self.menu.addAction(self.APrint)
        self.menu.addAction(self.AExit)
        self.menu_2.addAction(self.AFont)
        self.menu_2.addAction(self.AZoomIn)
        self.menu_2.addAction(self.AZoomOut)
        self.menu_3.addAction(self.AAbout)
        self.menu_3.addAction(self.AManual)
        self.menu_3.addAction(self.AWhoisqutrub)
        self.menu_4.addAction(self.ACopy)
        self.menu_5.addAction(self.ASetting)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_insert.menuAction())
        self.menubar.addAction(self.menu_tashkeel.menuAction())
        self.menubar.addAction(self.menu_convert.menuAction())      
        self.menubar.addAction(self.menu_5.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.toolBar.addAction(self.AFont)
        self.toolBar.addAction(self.ACopy)

    # Menu Right to Left
        self.menu.setLayoutDirection(RightToLeft);
        self.menu_2.setLayoutDirection(RightToLeft);
        self.menu_3.setLayoutDirection(RightToLeft);
        self.menu_4.setLayoutDirection(RightToLeft);
        self.menu_5.setLayoutDirection(RightToLeft);
        self.menu_insert.setLayoutDirection(RightToLeft);
        self.menu_tashkeel.setLayoutDirection(RightToLeft);
        self.menu_convert.setLayoutDirection(RightToLeft);

#tool bar
        self.toolBar.addAction(self.AFont)
        self.toolBar.addAction(self.ACopy)
        self.toolBar.addAction(self.AImport)        
        self.toolBar.addAction(self.AExport)
        self.toolBar.addAction(self.APrint)

        
#ToDo 2
##        self.toolBar.addAction(self.APrintPreview)
        self.toolBar.addAction(self.AZoomIn)
        self.toolBar.addAction(self.AZoomOut)


        #Actions

        #-----------------------------
        # create a table of symboles to insert
        TablesInsertActions=[];        
        SymboleToInsert={
        araby.FATHA:{'image':'fatha', u'action':'insert', u'label':u'فتحة', 'class':'insert'},
        araby.DAMMA:{'image':'damma', u'action':'insert', u'label':u'ضمة', 'class':'insert'},
        araby.KASRA:{'image':'kasra', u'action':'insert', u'label':u'كسرة', 'class':'insert'},
        araby.SUKUN:{'image':'sukun', u'action':'insert', u'label':u'سكون', 'class':'insert'},
        araby.SHADDA:{'image':'shadda', u'action':'insert', u'label':u'شدّة', 'class':'insert'},
        araby.FATHATAN:{'image':'fathatan', u'action':'insert', u'label':u'فتحتان', 'class':'insert'},
        araby.DAMMATAN:{'image':'dammatan', u'action':'insert', u'label':u'ضمتان', 'class':'insert'},
        araby.KASRATAN:{'image':'kasratan', u'action':'insert', u'label':u'كسرتان', 'class':'insert'},
        araby.TATWEEL:{'image':"tatweel", u'action':'insert', u'label':u'تطويل', 'class':'insert'},
        araby.ALEF_WASLA:{'image':'alef_wasla', u'action':'insert', u'label':u'ألف وصل', 'class':'insert'},
        u'\u200D':{'image':'zwj', u'action':'insert', u'label':u'ربط الحرف', 'class':'insert'}, # Zero Wisth Joiner
        u'\u200C': {'image':'zwnj', u'action':'insert', u'label':u'فصل الحروف', 'class':'insert'},# Zero Wisth NOn Joiner
        u'\u06AF': {'image':'gaf', u'action':'insert', u'label':u'جيم مصرية', 'class':'insert'},#Gaf
        u'\u067E': {'image':'peh', u'action':'insert', u'label':u'الباء المثلثة', 'class':'insert'},#Peh
        u'\u0670': {'image':'smallalef', u'action':'insert', u'label':'ألف صغيرة', 'class':'insert'},# supscript Alef
        }    
        # =imagesName.keys()
        i=0;
        for actualSymbol in SymboleToInsert:
            TablesInsertActions.append(PyQt5.QtWidgets.QAction(MainWindow))
            TablesInsertActions[i].setObjectName("AInsert"+str(i))
            label= SymboleToInsert[actualSymbol].get('label', 'missedlabel');
            TablesInsertActions[i].setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", label, None))

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join(PWD, "ar/images/%s.png"%SymboleToInsert[actualSymbol].get('image', 'missedimage'))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            TablesInsertActions[i].setIcon(icon)
            #--------Insert
            self.toolBar.addAction(TablesInsertActions[i])
            #~ print("actual symbole", actualSymbol)
            #~ QtCore.QObject.connect(TablesInsertActions[i], QtCore.SIGNAL("triggered()"), lambda text=actualSymbol: self.insert(text))
            #~ TablesInsertActions[i].triggered.connect(lambda text=actualSymbol: self.insert(text))
            TablesInsertActions[i].triggered.connect(lambda checked, text=actualSymbol: self.insert(text))

            self.menu_insert.addAction(TablesInsertActions[i])
            i+=1;
        #-----------------------------
        # create a table of actions to do
        TableActions={
        # u'Wordtag':{'image':'Wordtag', u'action':'Wordtag', u'label':'تصنيف الكلمات', 'class':'convert'},
        # u'Unshape':{'image':'Unshape', u'action':'Unshape', u'label':'قلب الحروف', 'class':'convert'},
        # u'Tokenize':{'image':'Tokenize', u'action':'Tokenize', u'label':'تفريق', 'class':'convert'},
        # u'TashkeelText':{'image':'TashkeelText', u'action':'TashkeelText', u'label':'TashkeelText', 'class':''},
        # u'Tashkeel2':{'image':'Tashkeel2', u'action':'Tashkeel2', u'label':'تشكيل', 'class':'tashkeel'},
        # u'autoCorrect':{'image':'autocorrect', u'action':'autoCorrect', u'label':'تصحيح تلقائي', 'class':'convert'},

        # u'Tabulize':{'image':'Tabulize', u'action':'Tabulize', u'label':'Tabulize', 'class':'format'},
        # u'Tabbing':{'image':'Tabbing', u'action':'Tabbing', u'label':'Tabbing', 'class':'format'},
        # u'SwapKeybEnAr':{'image':'SwapKeybEnAr', u'action':'SwapKeybEnAr', u'label':'تصحيح لوحة المفاتيح', 'class':'convert'},
        u'StripHarakat':{'image':'StripHarakat', u'action':'StripHarakat', u'label':'حذف الحركات', 'class':'tashkeel'},
        # u'Romanize':{'image':'Romanize', u'action':'Romanize', u'label':'رومنة', 'class':'convert'},
        # u'Arabize':{'image':'Arabize', u'action':'Arabize', u'label':'تعريب', 'class':'convert'},        
        # u'ReduceTashkeel':{'image':'ReduceTashkeel', u'action':'ReduceTashkeel', u'label':'ReduceTashkeel', 'class':''},
        # u'Poetry':{'image':'Poetry', u'action':'Poetry', u'label':'ضبط قصيدة عمودية', 'class':'format'},
#        QtCore.QObject.connect(self.AExit, QtCore.SIGNAL("triggered()"), MainWindow.close)
        u'RandomText':{'image':'NumberToLetters', u'action':'RandomText', u'label':'نص عشوائي', 'class':'tashkeel'},
        u'NumberToLetters':{'image':'NumberToLetters', u'action':'NumberToLetters', u'label':'تحويل الأعداد إلى كلمات', 'class':'convert'},
        u'Normalize':{'image':'Normalize', u'action':'Normalize', u'label':'تنميط', 'class':'convert'},
        # u'LightStemmer':{'image':'LightStemmer', u'action':'LightStemmer', u'label':'تحليل', 'class':''},
        # u'Language':{'image':'Language', u'action':'Language', u'label':'كشف اللغة', 'class':'convert'},
        # u'Itemize':{'image':'Itemize', u'action':'Itemize', u'label':'Itemize', 'class':'format'},
        # u'Inverse':{'image':'Inverse', u'action':'Inverse', u'label':'ترتيب حسب آخر حرف', 'class':'convert'},
        # u'DoNothing':{'image':'DoNothing', u'action':'DoNothing', u'label':'DoNothing', 'class':''},
        # u'CsvToData':{'image':'CsvToData', u'action':'CsvToData', u'label':'CsvToData', 'class':'convert'},
        # u'Contibute':{'image':'Contibute', u'action':'Contibute', u'label':'Contibute', 'class':''},
        # u'CompareTashkeel':{'image':'CompareTashkeel', u'action':'CompareTashkeel', u'label':'CompareTashkeel', 'class':''},
        # u'Affixate':{'image':'Affixate', u'action':'Affixate', u'label':'توليد الكلمات', 'class':'convert'},
        # u'lettersFrequency':{'image':'lettersFrequency', u'action':'lettersFrequency', u'label':'تعداد الحروف', 'class':'convert'},
        # u'removeDots':{'image':'removeDots', u'action':'removeDots', u'label':'حذف نقاط الحروف', 'class':'convert'},
        # u'timToUtf8':{'image':'timToUtf8', u'action':'timToUtf8', u'label':'تحويل ترميز بلكولتر', 'class':'convert'},
        
        }
        TablesTreatActions=[]
        i=0;
        for key in  TableActions.keys():
            TablesTreatActions.append(PyQt5.QtWidgets.QAction(MainWindow))
            TablesTreatActions[i].setObjectName("A"+key)
            name=TableActions[key]['label'];
            TablesTreatActions[i].setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", name, None))#))#, ))
            imagename=TableActions[key]['image'];
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join(PWD, "ar/images%s.png"%imagename)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            TablesTreatActions[i].setIcon(icon)
            #--------Treat
            action=key;
            #~ QtCore.QObject.connect(TablesTreatActions[i], QtCore.SIGNAL("triggered()"), lambda text=action: self.display_resultActions(text))
            TablesTreatActions[i].triggered.connect(lambda cheched, text=action: self.display_resultActions(text))

            if TableActions[key]['class']=='convert':
                self.menu_convert.addAction(TablesTreatActions[i])
            elif TableActions[key]['class']=='insert':
                self.menu_insert.addAction(TablesTreatActions[i])
            elif TableActions[key]['class']=='tashkeel':
                self.menu_tashkeel.addAction(TablesTreatActions[i])
            else:
                self.menu.addAction(TablesTreatActions[i])                    
            i+=1;        

        self.retranslateUi(MainWindow)
        self.TabVoice.setCurrentIndex(0)

        self.ResultVocalized.setPlainText(u"تشكيل النصوص العربية");

        #~ QtCore.QObject.connect(self.BVocalize, QtCore.SIGNAL("clicked()"), self.doHeavyLifting);#self.display_result)
        #~ QtCore.QObject.connect(self.BRemoveTashkeel, QtCore.SIGNAL("clicked()"), self.display_resultRemove)
        #~ QtCore.QObject.connect(self.BRandomText, QtCore.SIGNAL("clicked()"), self.randomText)

        #~ # QtCore.QObject.connect(self.ARandomText, QtCore.SIGNAL("triggered()"), self.randomText)

        #~ # QtCore.QObject.connect(self.CBLanguage, QtCore.SIGNAL("activated(int)"), self.change_language)
        #~ #QtCore.QObject.connect(self.CBLexique, QtCore.SIGNAL("activated(int)"), self.display_result)

        #~ QtCore.QObject.connect(self.AExit, QtCore.SIGNAL("triggered()"), MainWindow.close)
        #~ QtCore.QObject.connect(self.APrint, QtCore.SIGNAL("triggered()"), self.print_result)

        #~ ##QtCore.QObject.connect(self.APrintPreview, QtCore.SIGNAL("triggered()"), self.print_preview)
        #~ QtCore.QObject.connect(self.AFont, QtCore.SIGNAL("triggered()"), self.change_font)
        #~ QtCore.QObject.connect(self.AAbout, QtCore.SIGNAL("triggered()"), self.about)
        #~ QtCore.QObject.connect(self.AWhoisqutrub, QtCore.SIGNAL("triggered()"), self.whoisqutrub)
        #~ QtCore.QObject.connect(self.AManual, QtCore.SIGNAL("triggered()"), self.manual)
        #~ QtCore.QObject.connect(self.AImport, QtCore.SIGNAL("triggered()"), self.open_file)

        #~ QtCore.QObject.connect(self.AExport, QtCore.SIGNAL("triggered()"), self.save_result)
        #~ QtCore.QObject.connect(self.AZoomIn, QtCore.SIGNAL("triggered()"), self.zoomin)
        #~ QtCore.QObject.connect(self.AZoomOut, QtCore.SIGNAL("triggered()"), self.zoomout)

        
        #~ QtCore.QObject.connect(self.ASetting, QtCore.SIGNAL("triggered()"), self.set_setting)
        #~ #QtCore.QObject.connect(self.APagesetup, QtCore.SIGNAL("triggered()"), self.page_setup)
        #~ QtCore.QObject.connect(self.ACopy, QtCore.SIGNAL("triggered()"), self.set_copy)
        self.BVocalize.clicked.connect(self.doHeavyLifting);#self.display_result)
        self.BRemoveTashkeel.clicked.connect(self.display_resultRemove)
        self.BRandomText.clicked.connect(self.randomText)

        self.AExit.triggered.connect(MainWindow.close)
        self.APrint.triggered.connect(self.print_result)

        self.AFont.triggered.connect(self.change_font)
        self.AAbout.triggered.connect(self.about)
        self.AWhoisqutrub.triggered.connect(self.whoisqutrub)
        self.AManual.triggered.connect(self.manual)
        self.AImport.triggered.connect(self.open_file)

        self.AExport.triggered.connect(self.save_result)
        self.AZoomIn.triggered.connect(self.zoomin)
        self.AZoomOut.triggered.connect(self.zoomout)

        self.ASetting.triggered.connect(self.set_setting)

        self.ACopy.triggered.connect(self.set_copy)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #---------
# Menu Right to Left
        self.menu.setLayoutDirection(RightToLeft);
        self.menu_2.setLayoutDirection(RightToLeft);
        self.menu_3.setLayoutDirection(RightToLeft);
        self.menu_4.setLayoutDirection(RightToLeft);
        self.menu_5.setLayoutDirection(RightToLeft);

# disable unallowed actions
        self.AExport.setEnabled(False)
        # self.AFont.setEnabled(False)
        # self.ACopy.setEnabled(False)
        self.APrint.setEnabled(False)
        # #self.APrintPreview.setEnabled(False)
        # # self.APagesetup.setEnabled(False)
        # self.AZoomIn.setEnabled(False)
        # self.AZoomOut.setEnabled(False)


        self.result={};
        self.TabVoice.show();
        #~ QtCore.QObject.connect(self.AExit, QtCore.SIGNAL("toggled(bool)"), MainWindow.close)
        self.AExit.toggled.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.readSettings();
        self.applySettings();
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(PWD, "ar/images/appicon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MainWindow.setWindowIcon(icon)
#create a Progressbar
        self.singleProgress = PyQt5.QtWidgets.QProgressBar(self.centralwidget)
        try:
            self.singleProgress.setProperty("value", QtCore.QVariant(0))
        except TypeError:
            self.singleProgress.setProperty("value", 0)

        self.singleProgress.setObjectName("singleProgress")
        #self.gridLayout.addWidget(self.singleProgress, 0 ,2, 3, 0)
        #self.singleProgress.hide();
        self.mytimer = QtCore.QTimer()
        # # constant timer
        #~ QtCore.QObject.connect(self.mytimer, QtCore.SIGNAL("timeout()"), self.singleUpdate)
        self.mytimer.timeout.connect(self.singleUpdate)

#end create a Progressbar

        self.progressDialog=QDialog(self.centralwidget)
        self.progressDialog.setObjectName("ProgressDialog")
        self.progressDialog.setWindowTitle(u'يُشَكِّلُ...')
        self.gridLayoutPD = QGridLayout(self.progressDialog)
        self.gridLayoutPD.setObjectName("gridLayout")
        self.gridLayoutPD.addWidget(self.singleProgress, 0, 0, 1, 1)
        self.progressDialog.setLayoutDirection(RightToLeft);
        #self.progressDialog.show();

# add a thread to handle slow tashkeel
        self.thread = None

    def doHeavyLifting(self):
        """
        UI callback, starts the thread with the proper arguments.
        """
        if self.thread: # Sanity check.
            return

        self.singleProgress.setValue(1)
        self.progressDialog.show();
        self.mytimer.start(1000);
        PyQt5.QtWidgets.QApplication.setOverrideCursor(
        QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.thread = WorkThread(target=self.display_result)
        #~ QtCore.QObject.connect(self.thread, QtCore.SIGNAL("mainThread"),
                     #~ self.mainThread)

        #~ self.thread.mainThread.connect(self.mainThread)
        #~ QtCore.QObject.connect(self.thread, QtCore.SIGNAL("finished()"), self.threadDone)
        self.thread.finished.connect(self.threadDone)

        self.thread.start()

    def mainThread(self, code):
        """
        Callback for calls from the thread that need to be executed in the
        main thread.
        """
        exec(code)


    def threadDone(self):
        """
        Callback for thread end.
        """

        del self.thread
        self.thread = None
        self.mytimer.stop();
        self.singleProgress.setValue(100)
        #Display result in tab
        self.display_result_in_tab()
        self.progressDialog.hide();
        #self.display_result_in_tab()
        PyQt5.QtWidgets.QApplication.restoreOverrideCursor()
        RightToLeft=1;
        msgBox=PyQt5.QtWidgets.QMessageBox(self.centralwidget);
        msgBox.setWindowTitle(PyQt5.QtWidgets.QApplication.translate("MainWindow", "مشكال", None))#, ));
        msgBox.setText(u"انتهى التشكيل");
        msgBox.setLayoutDirection(RightToLeft);
        msgBox.setStandardButtons(PyQt5.QtWidgets.QMessageBox.Ok);
        msgBox.setDefaultButton(PyQt5.QtWidgets.QMessageBox.Ok);
        msgBox.exec_(); 


    def convert_text(self,text, partialVocalization=False, lastMarkTashkeel=False):
        action="Tashkeel2";
        options={'lastmark':lastMarkTashkeel,}
        vocalizedTextDict = core.adaat.DoAction(text,action,options);
        vocalizedText = u"";
        for itemD in vocalizedTextDict:
            if  'chosen' in itemD:

                #~vocalizedText+=" "+itemD['chosen'];
                if itemD['chosen'][0] in u"-[\]{}()*+?.,،:\^$|#\s\n،":
                    vocalizedText += ""+itemD['chosen'];
                else:
                    # if the word is recognized
                    if araby.is_vocalized(itemD['chosen']):
                        vocalizedText += " "+ itemD['chosen'];
                    else: #unrecognized word
                        #get suggestions from customized dictionary
                        custom_suggest = self.dict.custom_dict.lookup(itemD['chosen'])
                        if len(custom_suggest)>=1 :
                            vocalizedText += " "+ custom_suggest[0];
                        else:
                            vocalizedText += " "+ itemD['chosen'];
                            
                        
                suggestList=itemD['suggest'].split(u";");
                self.ResultVocalized.dict.add(itemD['chosen'],suggestList)
        if partialVocalization:
            vocalizedText = araby.reduceTashkeel(vocalizedText);
        return vocalizedText;        

    def singleUpdate(self):
        """
        Slot for singleShot timer timeout
        """
        val = self.singleProgress.value()
        val+=20/val+1
        if val > 90:
            val = 75
        self.singleProgress.setValue(val)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(PyQt5.QtWidgets.QApplication.translate("MainWindow", myAPPLICATION_NAME, None))#))#, ))
##        self.Label.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", ",", None))#, ))
##        self.Label_2.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", ",", None))#, ))
        #self.TSearch.setToolTip(PyQt5.QtWidgets.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'KacstOne\'; font-size:16pt; font-weight:600; font-style:normal;\">\n"
# "<p dir=\'rtl\' style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">1-اكتب الجملة</p>\n"
# "<p dir=\'rtl\' style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">3- اختر الترميز</p>\n"
# "<p dir=\'rtl\' style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">4-اضغط على ترميز</p></body></html>", None))#, ))
##        self.CBLexique.setItemText(0, PyQt5.QtWidgets.QApplication.translate("MainWindow", "دليل الموارد والوسائل العامة", None))#, ))
        self.CBLanguage.setItemText(0, PyQt5.QtWidgets.QApplication.translate("MainWindow", "العربية", None))#))#, ))
        self.CBLanguage.setItemText(1, PyQt5.QtWidgets.QApplication.translate("MainWindow", "فرنسية", None))#))#, ))
        self.CBLanguage.setItemText(2, PyQt5.QtWidgets.QApplication.translate("MainWindow", "إنجليزية", None))#))#, ))
        self.BVocalize.setToolTip(PyQt5.QtWidgets.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'ae_AlMateen\'; font-size:18pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ابحث</p></body></html>", None))#, ))
        self.BVocalize.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "تشكيل", None))#))#, ))
        self.BRemoveTashkeel.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "حذف التشكيل", None))#))#, ))
        self.BRandomText.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "نص عشوائي", None)) #))#, ))

##        self.TabActiveResult.horizontalHeaderItem(0).setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "العربية", None))#, ))
##        self.TabActiveResult.horizontalHeaderItem(1).setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "الفرنسية", None))#, ))
##        self.TabActiveResult.horizontalHeaderItem(2).setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "الإنجليزية", None))#, ))
       
        self.TabVoice.setTabText(self.TabVoice.indexOf(self.TabResultVocalized), PyQt5.QtWidgets.QApplication.translate("MainWindow", "التشكيل", None))#))#, ))
        #self.TabVoice.setTabText(self.TabVoice.indexOf(self.TabHelpVocalized), PyQt5.QtWidgets.QApplication.translate("MainWindow", "الشرح", None))#, ))
        self.menu.setTitle(PyQt5.QtWidgets.QApplication.translate("MainWindow", "ملف", None))#, ))
##        self.menu_6.setTitle(PyQt5.QtWidgets.QApplication.translate("MainWindow", "معاينة قبل الطباعة", None))#, ))
        self.menu_2.setTitle(PyQt5.QtWidgets.QApplication.translate("MainWindow", "عرض", None))#, ))
        self.menu_3.setTitle(PyQt5.QtWidgets.QApplication.translate("MainWindow", "مساعدة", None))#, ))
        self.menu_4.setTitle(PyQt5.QtWidgets.QApplication.translate("MainWindow", "تحرير", None))#, ))
        self.menu_5.setTitle(PyQt5.QtWidgets.QApplication.translate("MainWindow", "أدوات", None))#, ))
        self.menu_insert.setTitle(PyQt5.QtWidgets.QApplication.translate("MainWindow", "إدراج", None))#, ))
        self.menu_tashkeel.setTitle(PyQt5.QtWidgets.QApplication.translate("MainWindow", "تشكيل", None))#, ))
        self.menu_convert.setTitle(PyQt5.QtWidgets.QApplication.translate("MainWindow", "تحويل", None))#, ))       

        self.toolBar.setWindowTitle(PyQt5.QtWidgets.QApplication.translate("MainWindow", "toolBar", None))#, ))
        self.AExport.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "ت&صدير", None))#, ))
        self.AImport.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "فتح", None))#, ))

        self.AExit.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "&خروج", None))#, ))
        self.AFont.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "خط", None))#, ))
        self.AAbout.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "حول البرنامج", None))#, ))
        self.AZoomIn.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "تكبير", None))#, ))
        self.AZoomOut.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow","تصغير" , None))#, ))
        self.AManual.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "دليل الاستعمال", None))#, ))
        self.ACopy.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "نسخ", None))#, ))
        self.AWhoisqutrub.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "عن مشاريعنا", None))#, ))
        self.ASetting.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "تفضيلات", None))#, ))
        self.APrint.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "طباعة...", None))#, ))
##        self.APageSetup.setText(PyQt5.QtWidgets.QApplication.translate("MainWindow", "إعداد الصفحة", None))#, ))






    def show_options(self):
        pass;
##        if self.BMoreOptions.checkState()!=0:
##            self.CBHaraka.show();
##            self.CBHarakaLabel.show();
##            self.BDict.show();
##        else:
##            self.CBHaraka.hide();
##            self.CBHarakaLabel.hide();
##            self.BDict.hide();

    def restore_default_font(self):
        self.font_result=QtGui.QFont(DefaultFont.family(),DefaultFont.pointSize(),DefaultFont.bold());
        fonttext=self.font_result.family()+"[%s]"%str(self.font_result.pointSize())
        self.TSettingFontResult.setText(fonttext)
        self.TSettingFontResult.update()
##        self.centralwidget.update();
    def change_font(self):
        newfont,ok = PyQt5.QtWidgets.QFontDialog.getFont(self.font_result);
        if ok:
            self.font_result=newfont;
            self.ResultVocalized.setFont(self.font_result)
            self.ResultVocalized.update()


    def zoomin(self):
        self.font_result.setPointSize(self.font_result.pointSize()+1);
        self.ResultVocalized.setFont(self.font_result)
        self.ResultVocalized.update();

    def zoomout(self):
        self.font_result.setPointSize(self.font_result.pointSize()-1);
        self.ResultVocalized.setFont(self.font_result)
        self.ResultVocalized.update()

    def set_copy(self):
        self.ResultVocalized.selectAll()
        self.ResultVocalized.copy();

    def page_setup(self):
        pass;
    def print_preview(self):
        pass;
#ToDo 1
    def generate_preview(self,other):
        pass;

    def print_result(self):
        if "HTML" in self.result:
            data=QtCore.QFile("ar/style.css");
            if (data.open(QtCore.QFile.ReadOnly)):
                mySTYLE_SHEET=QtCore.QTextStream(data).readAll();
    ##            text=unicode(text);
            else:
                mySTYLE_SHEET=u"""
body {
    direction: rtl;
    font-family: Traditional Arabic, "Times New Roman";
    font-size: 16pt;
}
"""
            document = PyQt5.QtGui.QTextDocument("")
            document.setDefaultStyleSheet(mySTYLE_SHEET)
            self.result["HTML"]=u"<html dir=rtl><body dir='rtl'>"+self.result["HTML"]+"</body></html>"
            document.setHtml(self.result["HTML"]);
            printer = PyQt5.QtPrintSupport.QPrinter()

            dlg = PyQt5.QtPrintSupport.QPrintDialog(printer, self.centralwidget)
            if dlg.exec_() != QDialog.Accepted:
                return
            self.ResultVocalized.print_(printer)

        else:
            PyQt5.QtWidgets.QMessageBox.warning(self.centralwidget,U"خطأ",
                                u"لا شيء يمكن طبعه.")


    def set_setting(self):
        init_Dialog=QDialog(self.centralwidget)
        Dialog=Ui_Dialog();
        Dialog.setupUi(init_Dialog);
        if init_Dialog.exec_() == QDialog.Accepted:
            self.readSettings();
            self.applySettings();



    def readSettings(self):
        settings = QtCore.QSettings("Arabeyes.org", "Qutrub")
        try:
            #~ family=settings.value("font_base_family", QtCore.QVariant(QString("Traditional Arabic"))).toString()
            family=settings.value("font_base_family", QtCore.QVariant(QString("Traditional Arabic")))#.toString()
        except TypeError:
            family = str(settings.value("font_base_family", "Traditional Arabic"))
        try:
            #~ size,ok=settings.value("font_base_size", QtCore.QVariant(12)).toInt();
            size,ok = int(settings.value("font_base_size", QtCore.QVariant(12)));
        except TypeError:
            size = settings.value("font_base_size", 12)
            size = int(size)
            ok = bool(size)
            
        if not ok:size=12;
        try:
            #~ bold=settings.value("font_base_bold", QtCore.QVariant(True)).toBool()
            bold = bool(settings.value("font_base_bold", QtCore.QVariant(True)))
        except TypeError:
            bold= bool(settings.value("font_base_bold", True))
        self.font_result.setFamily(family)
        self.font_result.setPointSize(size)
        self.font_result.setBold(bold)
        #read of dictsetting options
        try:
            #~ dictsetting,ok = settings.value("DictSetting", QtCore.QVariant(1)).toInt();
            dictsetting,ok = int(settings.value("DictSetting", QtCore.QVariant(1)))
        except TypeError:
            dictsetting = settings.value("DictSetting", 1);
            ok = bool(dictsetting)
        if not ok:dictsetting=1;

        self.BDictOption=dictsetting;
    def applySettings(self):
        self.ResultVocalized.setFont(self.font_result);
        self.ResultVocalized.update();
        self.retranslateUi(self.MainWindow)

    def page_setup(self):
        PyQt5.QtWidgets.QMessageBox.warning(self.centralwidget,U"عذرا",
                                u"غير متوفر حاليا")


    def whoisqutrub(self):
        RightToLeft=1;
        msgBox=PyQt5.QtWidgets.QMessageBox(self.centralwidget);
        msgBox.setWindowTitle(u"عن البرنامج");
        filepath = os.path.join(PWD,"ar/projects.html")
        #~ print(filepath)
        data = QtCore.QFile(filepath);  
        #~ data=QtCore.QFile("ar/projects.html");
        if (data.open(QtCore.QFile.ReadOnly)):
            textstream=QtCore.QTextStream(data);
            textstream.setCodec("UTF-8");
            text=textstream.readAll();
        else:
            text=u"لا يمكن فتح ملف المساعدة"


        msgBox.setText(text);
        msgBox.setLayoutDirection(RightToLeft);
        msgBox.setStandardButtons(PyQt5.QtWidgets.QMessageBox.Ok);
        msgBox.setDefaultButton(PyQt5.QtWidgets.QMessageBox.Ok);
        msgBox.exec_();


    def manual(self):
        filepath = os.path.join(PWD,"ar/help_body.html")
        #~ print(filepath)
        data = QtCore.QFile(filepath);        
        #~ data=QtCore.QFile("ar/help_body.html");
        if (data.open(QtCore.QFile.ReadOnly)):
            textstream=QtCore.QTextStream(data);
            textstream.setCodec("UTF-8");
            text=textstream.readAll();
        else:
            text=u"لا يمكن فتح ملف المساعدة"

        Dialog=QDialog(self.centralwidget)

        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 480)
        Dialog.setWindowTitle(u'دليل الاستعمال')
        gridLayout = QGridLayout(Dialog)
        gridLayout.setObjectName("gridLayout")
        textBrowser = PyQt5.QtWidgets.QTextBrowser(Dialog)
        textBrowser.setObjectName("textBrowser")
        gridLayout.addWidget(textBrowser, 0, 0, 1, 1)
        buttonBox = QDialogButtonBox(Dialog)
        buttonBox.setOrientation(QtCore.Qt.Horizontal)
        buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox.setObjectName("buttonBox")
        gridLayout.addWidget(buttonBox, 1, 0, 1, 1)


        #~ QtCore.QObject.connect(buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        text2=unicode(text)
        textBrowser.setText(text2)
        RightToLeft=1;
        Dialog.setLayoutDirection(RightToLeft);
        Dialog.show();

    def about(self):
        RightToLeft=1;
        msgBox=PyQt5.QtWidgets.QMessageBox(self.centralwidget);
        msgBox.setWindowTitle(u"عن البرنامج");
##          msgBox.setTextFormat(QrCore.QRichText);
        filepath = os.path.join(PWD,"ar/about.html")
        #~ print(filepath)
        data = QtCore.QFile(filepath);
        if (data.open(QtCore.QFile.ReadOnly)):
            textstream=QtCore.QTextStream(data);
            textstream.setCodec("UTF-8");
            text_about=textstream.readAll();
        else:
#            text=u"لا يمكن فتح ملف المساعدة"
            text_about=u"""<h1>فكرة</h1>

"""
        msgBox.setText(text_about);
        msgBox.setLayoutDirection(RightToLeft);
        msgBox.setStandardButtons(PyQt5.QtWidgets.QMessageBox.Ok);
        msgBox.setIconPixmap(QtGui.QPixmap(os.path.join(PWD, "ar/images/logo.png")));
        msgBox.setDefaultButton(PyQt5.QtWidgets.QMessageBox.Ok);
        msgBox.exec_();
    def open_file(self):
        """
        Open file and load it to input Text edit
        """
        display_format='TEXT';
        filename, x = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self.centralwidget,
        PyQt5.QtWidgets.QApplication.translate("MainWindow", "فتح ملف", None),"untitled","Text file (*.txt);;Text Unicode comma separeted format file (*.csv);;HTML file (*.html)");
        if filename:
            #~ filename=unicode(filename)
            tuple=filename.split(".");
            if len(tuple)>=2:
                extention=tuple.pop();
            else:
                extention="html";
                filename+="."+extention
            text=""
            if extention.lower() in ('txt','csv', 'html'):
                display_format=extention.upper();
            #Add text generation
            try:
                file_opened=open(filename,'r', encoding='utf8');
                if file_opened:
                    text=file_opened.read()#.decode('utf8')
                    if display_format=='HTML':
                        self.ResultVocalized.setPlainText(u'');
                        self.ResultVocalized.appendHtml(text);
                    else:
                        self.ResultVocalized.setPlainText(text);
                    file_opened.close();
                else:
                    PyQt5.QtWidgets.QMessageBox.warning(self.centralwidget,PyQt5.QtWidgets.QApplication.translate("MainWindow", "خطأ", None),# ),
                                PyQt5.QtWidgets.QApplication.translate("MainWindow", "لا يمكن فتح الملف %s"%filename, None))
            except:
                PyQt5.QtWidgets.QMessageBox.warning(self.centralwidget,PyQt5.QtWidgets.QApplication.translate("MainWindow", "خطأ", None, ),
                                PyQt5.QtWidgets.QApplication.translate("MainWindow", "لا يمكن فتح الملف %s"%filename, None))

    def save_result(self):
        filename, x = PyQt5.QtWidgets.QFileDialog.getSaveFileName(self.centralwidget,
        u"حفظ ملف","untitled","HTML document (*.html *.htm);;Text file (*.txt);;Text Unicode comma separeted format file (*.csv);;XML file (*.xml)");
        if filename:
            #~ filename=unicode(filename)
            tuple=filename.split(".");
            if len(tuple)>=2:
                extention=tuple.pop();
            else:
                extention="html";
                filename+="."+extention
            text=""
            if extention.lower() in ('html','txt','xml','csv'):
                display_format=extention.upper();
            #Add text generation
                if  extention.upper() not in self.result:
                    PyQt5.QtWidgets.QMessageBox.warning(self.centralwidget,U"خطأ",
                                u"لاشيء يمكن تصديره")
                    return None;
                text+=self.result[extention.upper()];
            else:
                PyQt5.QtWidgets.QMessageBox.warning(self.centralwidget,U"خطأ",
                                u"اسم ملف غير مناسب %s"%filename)
            try:
                file_saved=open(filename,'w+');
                if file_saved:
                    file_saved.write(text)#.encode("utf8"));
                    file_saved.flush();
                    file_saved.close();

                else:
                    PyQt5.QtWidgets.QMessageBox.warning(self.centralwidget,U"خطأ",
                                u"لا يمكن فتح الملف %s"%filename)
            except:
                PyQt5.QtWidgets.QMessageBox.warning(self.centralwidget,U"خطأ",
                                u"لا يمكن حفظ الملف %s"%filename)
    def to_string(self, word):
        """ used to keep legacy between py2 and 3"""
        try: # version 2
            if not word.isEmpty():
                word = unicode(word)
            else:
                word = ""
        except:
            pass
        return word
    def display_result(self,arg=""):

        word = self.ResultVocalized.toPlainText();
        word = self.to_string(word)
        if word:            
            word = word.strip(' ');
            
            reducedTashkeel=(self.BReducedVocalization.checkState()!=0);
            lastMarkTashkeel=(self.BLastMarkVocalization.checkState()!=0);  

            result=self.convert_text(word, reducedTashkeel, lastMarkTashkeel)

            self.result["HTML"] = result;


    def display_resultActions(self,action="DoNothing"):
        text = self.ResultVocalized.toPlainText();
        text = self.to_string(text)
        if text:
            # do actions
            #action=self.CBHaraka.currentText();
            #print action.encode('utf8')
            result=core.adaat.DoAction(unicode(text),action);
            self.ResultVocalized.setPlainText(result)

    def display_resultRemove2(self):

        word = self.ResultVocalized.toPlainText();
        word = self.to_string(word)        
        if word:
            word=unicode(word);
            word = word.strip(' ');
            self.result["HTML"]=araby.strip_tashkeel(word);
            self.display_result_in_tab()
    def display_resultRemove(self):
        
        cursor = self.ResultVocalized.textCursor()
        #~cursor.select(QTextCursor.WordUnderCursor)
        self.ResultVocalized.setTextCursor(cursor)
        # Check if the selected word is misspelled and offer spelling
        if self.ResultVocalized.textCursor().hasSelection():
             
            originaltext = unicode(self.ResultVocalized.textCursor().selectedText())
            #~self.pretxt = originaltext[-1]
            #~self.pretxt = originaltext[0]
            self.correctWord(araby.strip_tashkeel(originaltext))
        else:
            word = self.ResultVocalized.toPlainText();
            word = self.to_string(word)
            if word:
                word=unicode(word);
                word = word.strip(' ');
                self.result["HTML"]=araby.strip_tashkeel(word);
                self.display_result_in_tab()
    def correctWord(self, word):
        '''
        Replaces the selected text with word.
        '''
        cursor = self.ResultVocalized.textCursor()
        cursor.beginEditBlock()
 
        cursor.removeSelectedText()
        #~cursor.insertText(word + self.pretxt)
        cursor.insertText(word)
        cursor.endEditBlock()        


    def display_result_in_tab(self):
        if  "HTML" in self.result:
            #text="<html><body dir='rtl'>"+self.result["HTML"]+"</body></html>"
            text=self.result["HTML"]            
            #print text.encode('utf8');
            self.ResultVocalized.setPlainText(text)


        #display help
            filename="ar/help.html";
##            print filename;
            data=QtCore.QFile(filename);
            if (data.open(QtCore.QFile.ReadOnly)):
                textstream=QtCore.QTextStream(data);
                textstream.setCodec("UTF-8");
                text_help=textstream.readAll();

            else:
    #            text=u"لا يمكن فتح ملف المساعدة"
                text_help=u"""<h1>فكرة</h1>"""
            #self.HelpVocalized.setText(text_help)


            #show result /
            self.TabVoice.show();
            self.MainWindow.showMaximized();
            self.TabVoice.setCurrentIndex(0);
    # enable actions
            self.AExport.setEnabled(True)
            self.AFont.setEnabled(True)
            self.ACopy.setEnabled(True)
            self.APrint.setEnabled(True)
            #self.APrintPreview.setEnabled(True)
            #self.APagesetup.setEnabled(True)
            self.AZoomIn.setEnabled(True)
            self.AZoomOut.setEnabled(True)

            self.centralwidget.update();
        else:
            PyQt5.QtWidgets.QMessageBox.warning(self.centralwidget,U"خطأ",
                            u"لا نتائج  ")
    def progressDialog2(self):
        progressDialog=QDialog(self.centralwidget)
        progressDialog.setObjectName("ProgressDialog")
        progressDialog.setWindowTitle(u'يُشَكِّلُ...')
        gridLayoutPD = QGridLayout(progressDialog)
        gridLayoutPD.setObjectName("gridLayout")
        gridLayoutPD.addWidget(self.singleProgress, 0, 0, 1, 1)
        progressDialog.setLayoutDirection(RightToLeft);
        progressDialog.show();

    def randomText(self):
        data=QtCore.QFile("data/randomtext.txt");
        if (data.open(QtCore.QFile.ReadOnly)):
            textstream=QtCore.QTextStream(data);
            textstream.setCodec("UTF-8");
            text=textstream.readAll();
            textlist=text.split('###');
            
            self.ResultVocalized.setPlainText(random.choice(textlist));
        else:
            text=u"لا يمكن فتح ملف النصوص العشوائية"
            self.ResultVocalized.setPlainText(text);
    def insert(self, text=araby.FATHA):
        #~ print("text", text)
        cursor = self.ResultVocalized.textCursor();
        cursor.insertText(str(text));            

def display_language(lang):
    if lang=="arabic":
        return u"عربي"
    elif lang=="french":
        return u"فرنسي"
    elif lang=="english":
        return u"إنجليزي"
    return lang;

#ToDo
# load lexique information from a file
def load_lexique():
    tab_lexique={
    0:{'name':"Tashkeel2",'title':u"تشكيل تام", }
,
    1:{'name':"ReducedTashkeel",'title':u"تشكيل مُختزَل",  }
,
    2:{'name':"RemoveTashkeel",'title':u"حذف التشكيل",}
    }
    return tab_lexique;


try:
    import app_rc
except:
    from . import app_rc
