# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created: Fri Oct 02 19:27:28 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
    
    
RightToLeft=1;
DefaultFont = QtGui.QFont()
DefaultFont.setFamily("Traditional Arabic")
DefaultFont.setPointSize(16)
DefaultFont.setBold(True)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.font_result=QtGui.QFont(DefaultFont.family(),DefaultFont.pointSize(),DefaultFont.bold());

        self.Dialog=Dialog;

        Dialog.setObjectName("Dialog")
        Dialog.resize(337, 202)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.SettingFontResultLabel = QtWidgets.QLabel(Dialog)
        self.SettingFontResultLabel.setObjectName("SettingFontResultLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.SettingFontResultLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TSettingFontResult = QtWidgets.QLineEdit(Dialog)
        self.TSettingFontResult.setObjectName("TSettingFontResult")
        self.horizontalLayout.addWidget(self.TSettingFontResult)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.BModifyFontResult = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BModifyFontResult.sizePolicy().hasHeightForWidth())
        self.BModifyFontResult.setSizePolicy(sizePolicy)
        self.BModifyFontResult.setObjectName("BModifyFontResult")
        self.horizontalLayout_2.addWidget(self.BModifyFontResult)
        self.BFontResultDefault = QtWidgets.QPushButton(Dialog)
        self.BFontResultDefault.setObjectName("BFontResultDefault")
        self.horizontalLayout_2.addWidget(self.BFontResultDefault)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.CBLanguageLabel = QtWidgets.QLabel(Dialog)
        self.CBLanguageLabel.setObjectName("CBLanguageLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.CBLanguageLabel)
        self.CBLanguage = QtWidgets.QComboBox(Dialog)
        self.CBLanguage.setEnabled(False)
        self.CBLanguage.setObjectName("CBLanguage")
        self.CBLanguage.addItem(str())
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.CBLanguage)
##        self.BDictSetting = QtGui.QCheckBox(Dialog)
##        self.BDictSetting.setChecked(True)
##        self.BDictSetting.setObjectName("BDictSetting")
##        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.BDictSetting)
##        self.BHarakatColor = QtGui.QCheckBox(Dialog)
##        self.BHarakatColor.setEnabled(False)
##        self.BHarakatColor.setChecked(False)
##        self.BHarakatColor.setObjectName("BHarakatColor")
##        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.BHarakatColor)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        #~ QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        #~ QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.Dialog.reject)
        #~ QtCore.QObject.connect(self.BModifyFontResult, QtCore.SIGNAL("clicked()"),self.change_font)
        #~ QtCore.QObject.connect(self.BFontResultDefault, QtCore.SIGNAL("clicked()"),self.restore_default_font)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.Dialog.reject)
        self.BModifyFontResult.clicked.connect(self.change_font)
        self.BFontResultDefault.clicked.connect(self.restore_default_font)

##        QtCore.QObject.connect(self.BDictSetting, QtCore.SIGNAL("stateChanged(int)"), self.setDictSetting)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
# execution
        fonttext=self.font_result.family()+"[%s]"%str(self.font_result.pointSize())
        self.TSettingFontResult.setText(fonttext)
        Dialog.setLayoutDirection(RightToLeft);
# readSetting
        self.readSettings();
        self.set_font_box();

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "تفضيلات", None, ))
        self.SettingFontResultLabel.setText(QtWidgets.QApplication.translate("Dialog", "خط عرض النتائج", None, ))
        self.BModifyFontResult.setText(QtWidgets.QApplication.translate("Dialog", "تعديل", None, ))
        self.BFontResultDefault.setText(QtWidgets.QApplication.translate("Dialog", "استعادة الخط الافتراضي", None, ))
        self.CBLanguageLabel.setText(QtWidgets.QApplication.translate("Dialog", "لغة التطبيق", None, ))
        self.CBLanguage.setItemText(0, QtWidgets.QApplication.translate("Dialog", "العربية", None, ))
##        self.BDictSetting.setText(QtGui.QApplication.translate("Dialog", "البحث دائما في معجم الأفعال الثلاثية", None, QtGui.QApplication.UnicodeUTF8))
##        self.BHarakatColor.setText(QtGui.QApplication.translate("Dialog", "إظهار علامات التشكيل بلون مختلف", None, QtGui.QApplication.UnicodeUTF8))


    def change_font(self):
        newfont,ok = QtWidgets.QFontDialog.getFont(self.font_result);
        if ok:
            self.font_result=newfont;
            self.set_font_box();

    def readSettings(self):
        settings = QtCore.QSettings("Arabeyes.org", "Qutrub")
        try:
            family=settings.value("font_base_family", QtCore.QVariant(str("Traditional Arabic")))
            size,ok=settings.value("font_base_size", QtCore.QVariant(12));
            size = int(size)
            bold=settings.value("font_base_bold", QtCore.QVariant(True))
            bold = bool(bold)
            dictsetting = settings.value("DictSetting", QtCore.QVariant(1))
            dictsetting = int(dictsetting)
        except TypeError:
            family=settings.value("font_base_family", "Traditional Arabic")
            size=settings.value("font_base_size", "12")
            size= int(size)
            ok = bool(size)
            bold=settings.value("font_base_bold", True)
            bold = bool(bold)
            dictsetting =settings.value("DictSetting", "1")
            dictsetting = int(dictsetting)
        if not ok:size=12;
        self.font_result.setFamily(family)
        self.font_result.setPointSize(size)
        self.font_result.setBold(bold)
        #read of dictsetting options
        
        if not ok:dictsetting=1;

##        self.BDictSetting.setCheckState(dictsetting);

    def writeSettings(self):
        settings = QtCore.QSettings("Arabeyes.org", "Qutrub")
        try:
            settings.setValue("font_base_family", QtCore.QVariant(self.font_result.family()))
            settings.setValue("font_base_size", QtCore.QVariant(self.font_result.pointSize()))
            settings.setValue("font_base_bold", QtCore.QVariant(self.font_result.bold()))
        except:
            settings.setValue("font_base_family", self.font_result.family())
            settings.setValue("font_base_size", self.font_result.pointSize())
            settings.setValue("font_base_bold", self.font_result.bold())
        #write of dictsetting options
##        settings.setValue("DictSetting", QtCore.QVariant(self.BDictSetting.checkState()));


    def restore_default_font(self):
        self.font_result=QtGui.QFont(DefaultFont.family(),DefaultFont.pointSize(),DefaultFont.bold());
        self.set_font_box();

    def set_font_box(self):
        fonttext=self.font_result.family()+"[%s]"%str(self.font_result.pointSize())
        self.TSettingFontResult.setText(fonttext)

##    def setDictSetting(self):
##        self.DictSetting=(self.BDictSetting.checkState()!=0)

    def accept(self):
        self.writeSettings();
        self.Dialog.accept();

