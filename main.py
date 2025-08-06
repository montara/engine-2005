#!/usr/bin/env python
from qt import *
from engineUI import EngineUI

class UI(EngineUI):
	def __init__(self, parent=None, name=None, fl=0):
		EngineUI.__init__(self,parent,name,fl)

if __name__ == "__main__":
	import sys
	a = QApplication(sys.argv)
	QObject.connect(a,SIGNAL("lastWindowClosed()"), a, SLOT("quit()"))
	w = UI()
	a.setMainWidget(w)
	w.show()
	a.exec_loop()

	print "we got here!"