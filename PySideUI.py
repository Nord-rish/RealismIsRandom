from pymel.core import *
from maya import OpenMayaUI as apiUI

try:
	from PySide2 import QtCore
	from PySide2 import QtWidgets
	from shiboken2 import wrapInstance
	import pyside2uic as pyside2uic
except:
	from PySide import QtCore
	from PySide import QtGui as QtWidgets
	from shiboken import wrapInstance
	import pysideuic as pyside2uic

from cStringIO import StringIO
import xml.etree.ElementTree as xml

def loadUiType(uiFile):
	"""
	Pyside lacks the "loadUiType" command, so we have to convert the ui file to py code in-memory first
	and then execute it in a special frame to retrieve the form_class.
	The contents of this method were not written by me and as it is used in this exact form by
	many python scripts, therefore I am unable to name the original author.
	"""
	parsed = xml.parse(uiFile)
	widget_class = parsed.find('widget').get('class')
	form_class = parsed.find('class').text

	with open(uiFile, 'r') as f:
		o = StringIO()
		frame = {}

		pyside2uic.compileUi(f, o, indent=0)
		pyc = compile(o.getvalue(), '<string>', 'exec')
		exec pyc in frame

		#Fetch the base_class and form class based on their type in the xml from designer
		form_class = frame['Ui_%s'%form_class]
		base_class = eval('QtWidgets.%s'%widget_class)
	return form_class, base_class

def getMayaWindow():
	"""
	Get the main Maya window as a QtWidgets.QMainWindow instance
	@return: QtWidgets.QMainWindow instance of the top level Maya windows
	"""
	ptr = apiUI.MQtUtil.mainWindow()
	if ptr is not None:
		return wrapInstance(long(ptr),QtWidgets.QWidget)

def newUI(uiFile):
	pyUIForm, pyUIBase = loadUiType(uiFile)
	class PyUI(pyUIForm, pyUIBase):
		"""docstring for PyUI"""
		def __init__(self, parent = getMayaWindow()):
			super(PyUI, self).__init__(parent)
			self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
			self.setupUi(self)

	return PyUI()
