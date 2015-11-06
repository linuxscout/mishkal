#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('mishkal/');
sys.path.append('mishkal/lib/');
from gui.appgui import *
#from adawaty import *

import sys

app = QtGui.QApplication(sys.argv)

widget = QtGui.QMainWindow()
##widget.resize(250, 150)
widget.layoutDirection='RightToLeft';
widget.setWindowTitle('simple')
widget.show()

w=Ui_MainWindow();
w.setupUi(widget);
##w.show();
sys.exit(app.exec_())
