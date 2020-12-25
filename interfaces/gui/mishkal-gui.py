#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import PyQt5.QtGui
import PyQt5.QtWidgets
PWD = os.path.join(os.path.dirname(sys.argv[0]))
sys.path.append(os.path.join(PWD, '../../support/'))
sys.path.append(os.path.join(PWD, '../../mishkal'))
sys.path.append(os.path.join(PWD, '../../'))

from gui.appgui import *
app = PyQt5.QtWidgets.QApplication(sys.argv)

widget =  PyQt5.QtWidgets.QMainWindow()
##widget.resize(250, 150)
widget.layoutDirection='RightToLeft';
widget.setWindowTitle('simple')
widget.show()

w= Ui_MainWindow();
w.setupUi(widget);
##w.show();
sys.exit(app.exec_())
