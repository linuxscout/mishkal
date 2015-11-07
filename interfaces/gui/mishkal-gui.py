#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
PWD = os.path.join(os.path.dirname(sys.argv[0]))
sys.path.append(os.path.join(PWD, '../../support/'))
#sys.path.append(os.path.join(PWD, '../../mishkal/lib/'))
sys.path.append(os.path.join(PWD, '../../mishkal'))
sys.path.append(os.path.join(PWD, '../../'))
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
