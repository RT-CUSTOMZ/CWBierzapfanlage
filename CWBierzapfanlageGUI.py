#!/usr/bin/pyhton

"""
Sebastian Thiems 2014 

GUI fuer die Automatische-Bierzapfanlage
"""

from PyQt4 import QtGui
from PyQt4 import QtCore
from CWBierzapfanlageConstants import CWConstants

class Button(QtGui.QWidget):
	def __init__(self,parent=None,callback=None,text="New Button",x=0,y=0,w=60,h=30):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		
		QtGui.QWidget.__init__(self, parent)

		self.button = QtGui.QPushButton(text, parent)
		self.button.setGeometry(x, y, w, h)
		
		if text == "Close":
			self.connect(self.button, QtCore.SIGNAL('clicked()'), QtGui.qApp, callback)
		else:
			self.connect(self.button, QtCore.SIGNAL('clicked()'), callback)

class Slider(QtGui.QWidget):
	def __init__(self,parent=None,callback=None,constants=None,section=None,labelText="New Label",x=0,y=0,w=100,h=30):
		self.labelText = labelText
		self.parent = parent
		self.constants = constants
		self.section = section
		QtGui.QWidget.__init__(self, parent)

		self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, parent)
		self.slider.setFocusPolicy(QtCore.Qt.NoFocus)
		self.slider.setGeometry(x,y,w,h)
		self.slider.setMinimum(0)
		self.slider.setMaximum(self.parent.CWConstants.w)
		self.slider.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'), callback)
		#print self.section +" : " + self.labelText
		if(section.size() > 0):
			self.slider.setValue(self.constants.configParser.getint(str(self.section), str(self.labelText)))
		
		Label(parent=parent,title=labelText,x=x,y=(y-30),w=w)

class ComboBox(QtGui.QWidget):
	def __init__(self,parent=None,callback=None,constants=None,x=0,y=0,w=100,h=30):
		self.parent = parent
		self.constants = constants
		QtGui.QWidget.__init__(self, parent)
		self.combo = QtGui.QComboBox(parent)
		self.combo.activated[str].connect(callback)
		self.combo.setGeometry(x,y,w,h)
		self.catchConfigs()
		
	def catchConfigs(self):
		self.combo.clear()
		for section in self.constants.configParser.sections():
			self.combo.addItem(section)

class TextField(QtGui.QWidget):
	def __init__(self, parent=None,x=0,y=0,w=100,h=30):
		self.parent = parent
		QtGui.QWidget.__init__(self, parent)
		self.textField = QtGui.QLineEdit(self.parent)
		self.textField.setGeometry(x,y,w,h)

class Label(QtGui.QWidget):
	def __init__(self,parent=None,title="New Label",x=0,y=0,w=60,h=30):
		self.parent = parent
		QtGui.QWidget.__init__(self, parent)

		self.label = QtGui.QLabel(title,parent)
		self.label.setGeometry(x,y,w,h)

class CWConfigWindow(QtGui.QWidget):
	def __init__(self,constants=CWConstants(),parent=None,w=400,h=600):
		self.CWConstants = constants
		self.w=w
		self.h=h
		QtGui.QWidget.__init__(self, parent)
		self.resize(self.w,self.h)
		self.setWindowTitle('Automatische Bierzapfanlage')
		self.createAndAddGUIElements()
		self.show()

	def createAndAddGUIElements(self):
		#Saved Settings ComboBox
		self.combo = ComboBox(parent=self, callback=self.changeSetting,constants=self.CWConstants, x=10,y=(self.h-580),w=(self.w-150))
		
		#TextField for saving
		self.textField = TextField(parent=self,  x=(self.w/2+60),y=(self.h-580),w=130)
		
		#Close Button
		Button(parent=self,callback=QtCore.SLOT('quit()'), text="Close",x=10,y=(self.h-40))

		#Save Button
		Button(parent=self,callback=self.saveSetting,text="Save",x=(self.w-140),y=(self.h-40))

		#Delete Button
		Button(parent=self,callback=self.deleteSetting,text="Delete",x=(self.w-70),y=(self.h-40))

		#Middle Right Point Slider
		self.middleRightPointSlider = Slider(parent=self, callback=self.CWConstants.changeMiddleRightPointValue,constants=self.CWConstants, section=self.combo.combo.currentText(), labelText=self.CWConstants.middleRightPointString, x=10, y=(self.h-100), w=(self.w-20))

		#Middle Left Point Slider		
		self.middleLeftPointSlider = Slider(parent=self, callback=self.CWConstants.changeMiddleLeftPointValue, constants=self.CWConstants, section=self.combo.combo.currentText(), labelText=self.CWConstants.middleLeftPointString, x=10, y=(self.h-170), w=(self.w-20))

		#Distance Top To Bottom Line Slider
		self.distanceTopToBottomLineSlider = Slider(parent=self, callback=self.CWConstants.changeDistanceTopToBottomLineValue, constants=self.CWConstants, section=self.combo.combo.currentText(), labelText=self.CWConstants.distanceTopToBottomLineString,x=10,y=(self.h-240), w=(self.w-20))

		#Border Glas Distance Div Slider
		self.borderGlasDistanceDivSlider = Slider(parent=self, callback=self.CWConstants.changeBorderGlasDistanceDivValue,  constants=self.CWConstants, section=self.combo.combo.currentText(), labelText=self.CWConstants.borderGlasDistanceDivString, x=10, y=(self.h-310), w=(self.w-20))

		#Border Glas Distance Slider
		self.borderGlasDistanceSlider = Slider(parent=self, callback=self.CWConstants.changeBorderGlasDistanceValue, labelText=self.CWConstants.borderGlasDistanceString, constants=self.CWConstants, section=self.combo.combo.currentText(), x=10, y=(self.h-380), w=(self.w-20))

		#Right Border Ignoer Slider
		self.rightBorderIgnorSlider = Slider(parent=self, callback=self.CWConstants.changeRightBorderIgnorValue, labelText=self.CWConstants.rightBorderIgnorString, constants=self.CWConstants, section=self.combo.combo.currentText(), x=10, y=(self.h-450), w=(self.w-20))

		#Left Border Ignor Slider
		self.leftBorderIgnorSlider = Slider(parent=self, callback=self.CWConstants.changeLeftBorderIgnorValue, labelText=self.CWConstants.leftBorderIgnorString, constants=self.CWConstants, section=self.combo.combo.currentText(), x=10, y=(self.h-520), w=(self.w-20))

	def changeSetting(self):
		if(self.combo.combo.currentText().size() > 0):
			section = str(self.combo.combo.currentText())
			print ("Setting: " + section)
			self.middleRightPointSlider.slider.setValue(int(self.CWConstants.configParser.get(section, str(self.middleRightPointSlider.labelText), True)))
			self.middleLeftPointSlider.slider.setValue(int(self.CWConstants.configParser.get(section, str(self.middleLeftPointSlider.labelText),True)))
			self.distanceTopToBottomLineSlider.slider.setValue(int(self.CWConstants.configParser.get(section, str(self.distanceTopToBottomLineSlider.labelText),True)))
			self.borderGlasDistanceDivSlider.slider.setValue(int(self.CWConstants.configParser.get(section, str(self.borderGlasDistanceDivSlider.labelText),True)))
			self.borderGlasDistanceSlider.slider.setValue(int(self.CWConstants.configParser.get(section, str(self.borderGlasDistanceSlider.labelText),True)))
			self.rightBorderIgnorSlider.slider.setValue(int(self.CWConstants.configParser.get(section, str(self.rightBorderIgnorSlider.labelText),True)))
			self.leftBorderIgnorSlider.slider.setValue(int(self.CWConstants.configParser.get(section, str(self.leftBorderIgnorSlider.labelText),True)))
				
	def deleteSetting(self):
		if(self.combo.combo.currentText().size() > 0):
			self.CWConstants.deleteSection(self.combo.combo.currentText())
			self.combo.catchConfigs()
			self.combo.combo.setCurrentIndex(int(self.combo.combo.count()-1))

	def saveSetting(self):
		if self.textField.textField.text().size() == 0:
			self.CWConstants.updateSection(self.combo.combo.currentText())
		else:
			section = self.textField.textField.text()
			self.CWConstants.saveSetting(section)
			self.combo.catchConfigs()
			self.combo.combo.setCurrentIndex(int(self.combo.combo.count()-1))
			self.changeSetting()

