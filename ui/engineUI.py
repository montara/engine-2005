# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'engineUI.ui'
#
# Created: Mon Jan 16 18:06:56 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


from qt import *


class EngineUI(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("EngineUI")



        self.VelocitySlider = QSlider(self,"VelocitySlider")
        self.VelocitySlider.setGeometry(QRect(10,10,290,20))
        self.VelocitySlider.setMaxValue(20000)
        self.VelocitySlider.setLineStep(1)
        self.VelocitySlider.setPageStep(1000)
        self.VelocitySlider.setOrientation(QSlider.Horizontal)
        self.VelocitySlider.setTickmarks(QSlider.Above)
        self.VelocitySlider.setTickInterval(1000)

        self.VelocityLabel = QLabel(self,"VelocityLabel")
        self.VelocityLabel.setGeometry(QRect(120,30,71,20))

        self.TorqueSlider = QSlider(self,"TorqueSlider")
        self.TorqueSlider.setGeometry(QRect(10,60,290,20))
        self.TorqueSlider.setMaxValue(20000)
        self.TorqueSlider.setPageStep(100)
        self.TorqueSlider.setOrientation(QSlider.Horizontal)
        self.TorqueSlider.setTickmarks(QSlider.Above)
        self.TorqueSlider.setTickInterval(1000)

        self.TorqueLabel = QLabel(self,"TorqueLabel")
        self.TorqueLabel.setGeometry(QRect(120,80,72,20))

        self.RPMDial = QDial(self,"RPMDial")
        self.RPMDial.setGeometry(QRect(80,110,140,140))
        self.RPMDial.setNotchesVisible(1)
        self.RPMDial.setMinValue(0)
        self.RPMDial.setMaxValue(8000)
        self.RPMDial.setLineStep(200)
        self.RPMDial.setPageStep(500)

        self.RPMLabel = QLabel(self,"RPMLabel")
        self.RPMLabel.setGeometry(QRect(130,250,34,20))
        self.RPMLabel.setAlignment(QLabel.AlignVCenter)

        self.languageChange()

        self.resize(QSize(317,276).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Engine Parameters"))
        self.VelocityLabel.setText(self.__tr("Velocity"))
        self.TorqueLabel.setText(self.__tr("Torque"))
        self.RPMLabel.setText(self.__tr("RPM"))


    def __tr(self,s,c = None):
        return qApp.translate("EngineUI",s,c)
