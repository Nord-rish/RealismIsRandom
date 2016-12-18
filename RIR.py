from pymel.core import *
from maya import cmds
from maya import OpenMayaUI as apiUI
import maya.api.OpenMaya as api

try:
	from PySide2 import QtCore
	from PySide2 import QtWidgets
except:
	from PySide import QtCore
	from PySide import QtGui as QtWidgets

from sys import argv
from functools import partial
import random
import PySideUI
import math
import xml.etree.ElementTree as ET

def startRIR(*args):
	scriptRoot = internalVar(usd = True)
	RIRInstance = RIR_MUI(scriptRoot + 'RealismIsRandom/RIR_UI.ui')

def closeRIR(RIRInstance):
	del(RIRInstance)
	del(PySideUI)
	api.MGlobal.displayInfo('RealismIsRandom closed.')


#===============================================================================
#=================== RIR Settings ==============================================
#===============================================================================
class RIR_Settings:
	def __init__(self, RIRMUI):
		self.RIRMUI = RIRMUI
		self.ApplyTo = self.getApplyTo(1)
		self.RndSeedAndScale = self.getRndSeedAndScale(1)
		self.LocationSettings = self.getLocationSettings(1)
		self.RotationSettings = self.getRotationSettings(1)
		self.ScaleSettings = self.getScaleSettings(1)

	def getApplyTo(self, mode = 0):
		"""Mode 0 = from Var;
		Mode 1 = from UI;
		returns dictionary: {X: bool, Y: bool, Z: bool}"""

		if (mode == 0):
			ApplyTo = self.ApplyTo
		elif (mode == 1):
			ApplyTo = { 'X': self.RIRMUI.PyUI.CB_ApplyToX.isChecked(),
						'Y': self.RIRMUI.PyUI.CB_ApplyToY.isChecked(),
						'Z': self.RIRMUI.PyUI.CB_ApplyToZ.isChecked() }

		return ApplyTo

	def setApplyTo(self, ApplyToX, ApplyToY, ApplyToZ, mode = 0):
		"""Mode 0 = set Var;
		Mode 1 = set UI;
		Mode 2 = set Var and UI"""
		if (mode == 0):
			self.ApplyTo = {'X': ApplyToX,
							'Y': ApplyToY,
							'Z': ApplyToZ}
		elif (mode == 1):
			self.RIRMUI.PyUI.CB_ApplyToX.setChecked(ApplyToX)
			self.RIRMUI.PyUI.CB_ApplyToY.setChecked(ApplyToY)
			self.RIRMUI.PyUI.CB_ApplyToZ.setChecked(ApplyToZ)
		elif (mode == 2):
			self.ApplyTo = {'X': ApplyToX,
							'Y': ApplyToY,
							'Z': ApplyToZ}

			self.RIRMUI.PyUI.CB_ApplyToX.setChecked(ApplyToX)
			self.RIRMUI.PyUI.CB_ApplyToY.setChecked(ApplyToY)
			self.RIRMUI.PyUI.CB_ApplyToZ.setChecked(ApplyToZ)


	def getRndSeedAndScale(self, mode = 0):
		"""Mode 0 = from Var;
		Mode 1 = from UI;"""
		if (mode == 0):
			RndSeedAndScale = self.RndSeedAndScale
		elif (mode == 1):
			RndSeedAndScale = { 'RndSeed': self.RIRMUI.PyUI.SB_RandomSeed.value() ,
								'RndScale': self.RIRMUI.PyUI.SB_dRandomScale.value() }
		return RndSeedAndScale

	def setRndSeedAndScale(self, RndSeed, RndScale, mode = 0):
		"""Mode 0 = set Var;
		Mode 1 = set UI;
		Mode 2 = set Var and UI"""
		if (mode == 0):
			self.RndSeedAndScale = {'RndSeed': RndSeed,
									'RndScale': RndScale}
		elif (mode == 1):
			self.RIRMUI.PyUI.SB_RandomSeed.setValue(RndSeed)
			self.RIRMUI.PyUI.SB_dRandomScale.setValue(RndScale)
		elif (mode == 2):
			self.RndSeedAndScale = {'RndSeed': RndSeed,
									'RndScale': RndScale}
			self.RIRMUI.PyUI.SB_RandomSeed.setValue(RndSeed)
			self.RIRMUI.PyUI.SB_dRandomScale.setValue(RndScale)


	def getLocationSettings(self, mode = 0):
		"""Mode 0 = from Var;
		Mode 1 = from UI;"""
		if (mode == 0):
			LocationSettings = self.LocationSettings
		elif (mode == 1):
			LocationSettings = {'Enabled': self.RIRMUI.PyUI.GB_Location.isChecked(),
								'Clamp': self.RIRMUI.PyUI.CB_LocationClamp.isChecked(),
								'RndMin': self.RIRMUI.PyUI.SB_dLocationMin.value(),
								'RndMax': self.RIRMUI.PyUI.SB_dLocationMax.value() }

		return LocationSettings

	def setLocationSettings(self, Enabled, Clamp, RndMin, RndMax, mode = 0):
		"""Mode 0 = set Var;
		Mode 1 = set UI;
		Mode 2 = set Var and UI"""
		if (mode == 0):
			self.LocationSettings = {'Enabled': Enabled,
									 'Clamp': Clamp,
									 'RndMin': RndMin,
									 'RndMax': RndMax }
		elif (mode == 1):
			self.RIRMUI.PyUI.GB_Location.setChecked(Enabled)
			self.RIRMUI.PyUI.CB_LocationClamp.setChecked(Clamp)
			self.RIRMUI.PyUI.SB_dLocationMin.setValue(RndMin)
			self.RIRMUI.PyUI.SB_dLocationMax.setValue(RndMax)
		elif (mode == 2):
			self.LocationSettings = {'Enabled': Enabled,
									 'Clamp': Clamp,
									 'RndMin': RndMin,
									 'RndMax': RndMax }
			self.RIRMUI.PyUI.GB_Location.setChecked(Enabled)
			self.RIRMUI.PyUI.CB_LocationClamp.setChecked(Clamp)
			self.RIRMUI.PyUI.SB_dLocationMin.setValue(RndMin)
			self.RIRMUI.PyUI.SB_dLocationMax.setValue(RndMax)


	def getRotationSettings(self, mode = 0):
		"""Mode 0 = from Var;
		Mode 1 = from UI;"""
		if (mode == 0):
			RotationSettings = self.RotationSettings
		elif (mode == 1):
			RotationSettings = {'Enabled': self.RIRMUI.PyUI.GB_Rotation.isChecked(),
								'Clamp': self.RIRMUI.PyUI.CB_RotationClamp.isChecked(),
								'RndMin': self.RIRMUI.PyUI.SB_dRotationMin.value(),
								'RndMax': self.RIRMUI.PyUI.SB_dRotationMax.value() }
		return RotationSettings

	def setRotationSettings(self, Enabled, Clamp, RndMin, RndMax, mode = 0):
		"""Mode 0 = set Var;
		Mode 1 = set UI;
		Mode 2 = set Var and UI"""
		if (mode == 0):
			self.RotationSettings = {'Enabled': Enabled,
									 'Clamp': Clamp,
									 'RndMin': RndMin,
									 'RndMax': RndMax }
		elif (mode == 1):
			self.RIRMUI.PyUI.GB_Rotation.setChecked(Enabled)
			self.RIRMUI.PyUI.CB_RotationClamp.setChecked(Clamp)
			self.RIRMUI.PyUI.SB_dRotationMin.setValue(RndMin)
			self.RIRMUI.PyUI.SB_dRotationMax.setValue(RndMax)
		elif (mode == 2):
			self.RotationSettings = {'Enabled': Enabled,
									 'Clamp': Clamp,
									 'RndMin': RndMin,
									 'RndMax': RndMax }
			self.RIRMUI.PyUI.GB_Rotation.setChecked(Enabled)
			self.RIRMUI.PyUI.CB_RotationClamp.setChecked(Clamp)
			self.RIRMUI.PyUI.SB_dRotationMin.setValue(RndMin)
			self.RIRMUI.PyUI.SB_dRotationMax.setValue(RndMax)


	def getScaleSettings(self, mode = 0):
		"""Mode 0 = from Var;
		Mode 1 = from UI;"""
		if (mode == 0):
			ScaleSettings = self.ScaleSettings
		elif (mode == 1):
			ScaleSettings = {'Enabled': self.RIRMUI.PyUI.GB_Scale.isChecked(),
							 'Clamp': self.RIRMUI.PyUI.CB_ScaleClamp.isChecked(),
							 'RndMin': self.RIRMUI.PyUI.SB_dScaleMin.value(),
							 'RndMax': self.RIRMUI.PyUI.SB_dScaleMax.value() }
		return ScaleSettings

	def setScaleSettings(self, Enabled, Clamp, RndMin, RndMax, mode = 0):
		"""Mode 0 = set Var;
		Mode 1 = set UI;
		Mode 2 = set Var and UI"""
		if (mode == 0):
			self.ScaleSettings = {'Enabled': Enabled,
								  'Clamp': Clamp,
								  'RndMin': RndMin,
								  'RndMax': RndMax }
		elif (mode == 1):
			self.RIRMUI.PyUI.GB_Scale.setChecked(Enabled)
			self.RIRMUI.PyUI.CB_ScaleClamp.setChecked(Clamp)
			self.RIRMUI.PyUI.SB_dScaleMin.setValue(RndMin)
			self.RIRMUI.PyUI.SB_dScaleMax.setValue(RndMax)
		elif (mode == 2):
			self.ScaleSettings = {'Enabled': Enabled,
								  'Clamp': Clamp,
								  'RndMin': RndMin,
								  'RndMax': RndMax }
			self.RIRMUI.PyUI.GB_Scale.setChecked(Enabled)
			self.RIRMUI.PyUI.CB_ScaleClamp.setChecked(Clamp)
			self.RIRMUI.PyUI.SB_dScaleMin.setValue(RndMin)
			self.RIRMUI.PyUI.SB_dScaleMax.setValue(RndMax)


#===============================================================================
#=================== Core Functions ============================================
#===============================================================================
class RIR_Core():
	"""docstring for RIR_Core."""
	def __init__(self, RIRMUI):
		self.RIRMUI = RIRMUI
		self.callbacks = self.addCallbacks()
		self.randomSeed = self.newRandomSeed()
		self.presetFile = internalVar(usd = True) + 'RealismIsRandom/RIR_Presets.xml'
		self.selObjects = [] #array of MFnDagPath
		self.oldTransforms = []
		self.currentTransforms = []
		self.undoStack = []

	def newRandomSeed(self):
		randomSeed = random.randint(0, 99999)
		self.randomSeed = randomSeed
		return randomSeed

	def addCallbacks(self):
		callbacks = []

		callbacks.append(api.MEventMessage.addEventCallback("SelectionChanged", self.selectionChanged))
		self.selectionChanged()

		return callbacks

	def removeCallbacks(self, *args, **kwargs):
		for callback in self.callbacks:
			if(callback):
				api.MMessage.removeCallback(callback)


	def loadPresets(self, location):
		tree = ET.parse(location)
		root = tree.getroot()

		for preset in root:
			ps = self.settingsFromPreset(preset)
			self.addPresetToUI(preset.find('name').text, ps)

	def savePreset(self, location, name, RIRsettings):
		tree = ET.parse(location)
		root = tree.getroot()

		presetExists = False

		for preset in root:
			if (preset.find('name').text == name):
				presetExists = True
				preset = self.updatePresetElement(preset, RIRsettings)
				break

		if (presetExists == False):
			newPreset = ET.XML(ET.tostring(preset, method="xml"))
			newPreset.find('name').text = name
			newPreset = self.updatePresetElement(newPreset, RIRsettings)
			root.append(newPreset)

			self.addPresetToUI(name, RIRsettings)

		tree.write(location)

	def updatePresetElement(self, preset, RIRsettings):
		applyTo = preset.find('applyTo')
		applyTo.find('x').text = str(RIRsettings.ApplyTo['X'])
		applyTo.find('y').text = str(RIRsettings.ApplyTo['Y'])
		applyTo.find('z').text = str(RIRsettings.ApplyTo['Z'])

		preset.find('rndSeed').text = str(RIRsettings.RndSeedAndScale['RndSeed'])
		preset.find('rndScale').text = str(RIRsettings.RndSeedAndScale['RndScale'])

		locationSettings = preset.find('locationSettings')
		locationSettings.find('Enabled').text = str(RIRsettings.LocationSettings['Enabled'])
		locationSettings.find('Clamp').text = str(RIRsettings.LocationSettings['Clamp'])
		locationSettings.find('RndMin').text = str(RIRsettings.LocationSettings['RndMin'])
		locationSettings.find('RndMax').text = str(RIRsettings.LocationSettings['RndMax'])

		rotationSettings = preset.find('rotationSettings')
		rotationSettings.find('Enabled').text = str(RIRsettings.RotationSettings['Enabled'])
		rotationSettings.find('Clamp').text = str(RIRsettings.RotationSettings['Clamp'])
		rotationSettings.find('RndMin').text = str(RIRsettings.RotationSettings['RndMin'])
		rotationSettings.find('RndMax').text = str(RIRsettings.RotationSettings['RndMax'])

		scaleSettings = preset.find('scaleSettings')
		scaleSettings.find('Enabled').text = str(RIRsettings.ScaleSettings['Enabled'])
		scaleSettings.find('Clamp').text = str(RIRsettings.ScaleSettings['Clamp'])
		scaleSettings.find('RndMin').text = str(RIRsettings.ScaleSettings['RndMin'])
		scaleSettings.find('RndMax').text = str(RIRsettings.ScaleSettings['RndMax'])

		return preset

	def settingsFromPreset(self, preset):
		settings = RIR_Settings(self.RIRMUI)

		applyTo = preset.find('applyTo')
		settings.ApplyTo['X'] = self.stringToBool(applyTo.find('x').text)
		settings.ApplyTo['Y'] = self.stringToBool(applyTo.find('y').text)
		settings.ApplyTo['Z'] = self.stringToBool(applyTo.find('z').text)

		settings.RndSeedAndScale['RndSeed'] = int(preset.find('rndSeed').text)
		settings.RndSeedAndScale['RndScale'] = float(preset.find('rndScale').text)

		locationSettings = preset.find('locationSettings')
		settings.LocationSettings['Enabled'] = self.stringToBool(locationSettings.find('Enabled').text)
		settings.LocationSettings['Clamp'] = self.stringToBool(locationSettings.find('Clamp').text)
		settings.LocationSettings['RndMin'] = float(locationSettings.find('RndMin').text)
		settings.LocationSettings['RndMax'] = float(locationSettings.find('RndMax').text)

		rotationSettings = preset.find('rotationSettings')
		settings.RotationSettings['Enabled'] = self.stringToBool(rotationSettings.find('Enabled').text)
		settings.RotationSettings['Clamp'] = self.stringToBool(rotationSettings.find('Clamp').text)
		settings.RotationSettings['RndMin'] = float(rotationSettings.find('RndMin').text)
		settings.RotationSettings['RndMax'] = float(rotationSettings.find('RndMax').text)

		scaleSettings = preset.find('scaleSettings')
		settings.ScaleSettings['Enabled'] = self.stringToBool(scaleSettings.find('Enabled').text)
		settings.ScaleSettings['Clamp'] = self.stringToBool(scaleSettings.find('Clamp').text)
		settings.ScaleSettings['RndMin'] = float(scaleSettings.find('RndMin').text)
		settings.ScaleSettings['RndMax'] = float(scaleSettings.find('RndMax').text)

		return settings

	def addPresetToUI(self, name, settings):
		rm = self.RIRMUI
		if((name in rm.presets) == False):
			presetAction = rm.loadPresetMenu.menu().addAction(name, partial(rm.on_MB_Presets_Load_triggered, name))
			rm.presets[name] = {'QAction': presetAction, 'Settings': settings}
			api.MGlobal.displayInfo('RealismIsRandom presets loaded successfully.')
		else:
			api.MGlobal.displayWarning('RealismIsRandom has duplicate presets!')

	def removePresetFromUI(self, name):
		rm = self.RIRMUI
		presetAction = rm.loadPresetMenu.menu().removeAction(rm.presets[name]['QAction'])


	def selectionChanged(self, *args, **kwargs):
		currentSelection = api.MGlobal.getActiveSelectionList()
		selectionIterator = api.MItSelectionList(currentSelection)

		#filter meshes? or apply to everything without exception?
		selectionIterator.setFilter(api.MFn.kMesh) #comment out to use the script for every kind of object
		selectionIterator.reset()
		#emtpy array
		self.selObjects = []
		self.oldTransforms = []
		self.undoStack = []

		while (selectionIterator.isDone() == False):
			#objDagPath of type MDagPath
			objDagPath = selectionIterator.getComponent()[0]
			self.selObjects.append(objDagPath)

			currentObj = api.MFnDagNode(objDagPath)
			currentParent = currentObj.parent(0) #returns MObject
			currentTransform = api.MFnTransform(currentParent)
			oT = api.MTransformationMatrix(currentTransform.transformation())
			self.oldTransforms.append(oT)

			selectionIterator.next()

		self.undoStack.append(self.oldTransforms)

	def updateTransforms(self, objectPaths):
		"""objectPaths has to be list of MFnDagPath"""
		#remove all non-objects from objects
		#read current transforms and save them temporarily
		#apply new transforms
		#worldspace = 4#

		for i in range(0, len(objectPaths)):
			currentObj = api.MFnDagNode(objectPaths[i])
			currentParent = currentObj.parent(0) #returns MObject
			currentTransform = api.MFnTransform(currentParent)

			currentTransform.setTransformation(self.calcRndTransformation(currentTransform.transformation() ,self.RIRMUI.currentSettings, i))


	def calcRndTransformation(self, transformation, settings, seedoffset):
		newRndTransform = api.MTransformationMatrix()
		rnd = random.Random()
		seed = settings.getRndSeedAndScale()['RndSeed'] + (seedoffset * 13)
		rndScale = settings.getRndSeedAndScale()['RndScale']
		applyTo = settings.getApplyTo()
		rnd.seed(seed)

		#=== calc and set translation ===
		transSettings = settings.getLocationSettings()
		transEnabled = transSettings['Enabled']
		transClamp = transSettings['Clamp']
		transMin = transSettings['RndMin']
		transMax = transSettings['RndMax']

		if(transEnabled and transMax != transMin):
			if(transClamp):
				if(rnd.uniform(0, 100) >= 50):
					rndTransX = transMax * rndScale
				else:
					rndTransX = transMin * rndScale
				rnd.seed(seed + 11)
				if(rnd.uniform(0, 100) >= 50):
					rndTransY = transMax * rndScale
				else:
					rndTransY = transMin * rndScale
				rnd.seed(seed + 12)
				if(rnd.uniform(0, 100) >= 50):
					rndTransZ = transMax * rndScale
				else:
					rndTransZ = transMin * rndScale
			else:
				rndTransX = rnd.uniform(transMin, transMax) * rndScale
				rnd.seed(seed + 11)
				rndTransY = rnd.uniform(transMin, transMax) * rndScale
				rnd.seed(seed + 12)
				rndTransZ = rnd.uniform(transMin, transMax) * rndScale

			rndTranslation = api.MVector([rndTransX, rndTransY, rndTransZ])

		else:
			rndTranslation = api.MVector([0,0,0])

		if not(applyTo['X']):
			rndTranslation.x = 0
		if not(applyTo['Y']):
			rndTranslation.y = 0
		if not(applyTo['Z']):
			rndTranslation.z = 0

		transformation.translateBy(rndTranslation, 1)

		#=== calc and set rotation ===
		rotSettings = settings.getRotationSettings()
		rotEnabled = rotSettings['Enabled']
		rotClamp = rotSettings['Clamp']
		rotMin = rotSettings['RndMin']
		rotMax = rotSettings['RndMax']

		if(rotEnabled and rotMin != rotMax):
			if(rotClamp):
				if(rnd.uniform(0, 100) >= 50):
					rndRotX = rotMax * rndScale
				else:
					rndRotX = rotMin * rndScale
				rnd.seed(seed + 13)
				if(rnd.uniform(0, 100) >= 50):
					rndRotY = rotMax * rndScale
				else:
					rndRotY = rotMin * rndScale
				rnd.seed(seed + 14)
				if(rnd.uniform(0, 100) >= 50):
					rndRotZ = rotMax * rndScale
				else:
					rndRotZ = rotMin * rndScale
			else:
				rndRotX = rnd.uniform(rotMin, rotMax) * rndScale
				rnd.seed(seed + 13)
				rndRotY = rnd.uniform(rotMin, rotMax) * rndScale
				rnd.seed(seed + 14)
				rndRotZ = rnd.uniform(rotMin, rotMax) * rndScale

			rndRotation = api.MEulerRotation(self.degToRad([rndRotX, rndRotY, rndRotZ]))

		else:
			rndRotation = api.MEulerRotation([0,0,0])

		if not(applyTo['X']):
			rndRotation.x = 0
		if not(applyTo['Y']):
			rndRotation.y = 0
		if not(applyTo['Z']):
			rndRotation.z = 0

		transformation.rotateBy(rndRotation, 1)

		#=== calc and set scale ===
		scaleSettings = settings.getScaleSettings()
		scaleEnabled = scaleSettings['Enabled']
		scaleClamp = scaleSettings['Clamp']
		scaleMin = scaleSettings['RndMin']
		scaleMax = scaleSettings['RndMax']

		if(scaleEnabled and scaleMin != scaleMax):
			if(scaleClamp):
				if(rnd.uniform(0, 100) >= 50):
					rndScaleX = scaleMax * rndScale
				else:
					rndScaleX = scaleMin * rndScale
				rnd.seed(seed + 15)
				if(rnd.uniform(0, 100) >= 50):
					rndScaleY = scaleMax * rndScale
				else:
					rndScaleY = scaleMin * rndScale
				rnd.seed(seed + 16)
				if(rnd.uniform(0, 100) >= 50):
					rndScaleZ = scaleMax * rndScale
				else:
					rndScaleZ = scaleMin * rndScale
			else:
				rndScaleX = rnd.uniform(scaleMin, scaleMax) * rndScale
				rnd.seed(seed + 15)
				rndScaleY = rnd.uniform(scaleMin, scaleMax) * rndScale
				rnd.seed(seed + 16)
				rndScaleZ = rnd.uniform(scaleMin, scaleMax) * rndScale

			currScale = transformation.scale(1)
			rndScale = [rndScaleX + currScale[0], rndScaleY + currScale[1], rndScaleZ + currScale[2]]

		else:
			rndScale = [1.0,1.0,1.0]

		if not(applyTo['X']):
			rndScale[0] = 1.0
		if not(applyTo['Y']):
			rndScale[1] = 1.0
		if not(applyTo['Z']):
			rndScale[2] = 1.0


		transformation.scaleBy(rndScale, 1)
		return transformation


	def applyTransforms(self, settings):
		#apply transforms and discard old ones
		#clear selection
		self.oldTransforms = []

		objectPaths = self.selObjects
		for i in range(0, len(objectPaths)):
			currentObj = api.MFnDagNode(objectPaths[i])
			currentParent = currentObj.parent(0) #returns MObject
			currentTransform = api.MFnTransform(currentParent)
			oT = api.MTransformationMatrix(currentTransform.transformation())
			self.oldTransforms.append(oT)

			currentTransform.setTransformation(self.calcRndTransformation(currentTransform.transformation() ,settings, i))

		self.undoStack.append(self.oldTransforms)

	def resetTransforms(self):
		#apply old transforms and clear selection
		if(len(self.undoStack) > 0):
			objectPaths = self.selObjects
			for i in range(0, len(objectPaths)):
				currentObj = api.MFnDagNode(objectPaths[i])
				currentParent = currentObj.parent(0) #returns MObject
				currentTransform = api.MFnTransform(currentParent)

				currentTransform.setTransformation(self.undoStack[len(self.undoStack) - 1][i])

			del self.undoStack[len(self.undoStack) - 1]


	def radToDeg(self, floats):
		if(type(floats) != float):
			degFloats = []
			for i in range(0, len(floats)):
				degFloats.append((180/math.pi) * floats[i])
			return degFloats
		else:
			return (180/math.pi) * floats

	def degToRad(self, floats):
		if(type(floats) != float):
			degFloats = []
			for i in range(0, len(floats)):
				degFloats.append(floats[i] / (180/math.pi))
			return degFloats
		else:
			return floats[i] / (180/math.pi)

	def stringToBool(self, string):
		if(string == 'True'):
			return True
		else:
			return False

#===============================================================================
#=================== UI Functions ==============================================
#===============================================================================
class RIR_MUI:
	"""docstring for RIR_MUI."""
	def __init__(self, UIFile):
		self.UIFile = UIFile
		self.PyUI = self.createUI(UIFile)
		self.showUI()
		self.RIRCore = RIR_Core(self)

		self.presetsMenu = None
		self.resetToDefaultMenu = None
		self.loadPresetMenu = None
		self.savePresetMenu = None
		self.deletePresetMenu = None
		self.getMenuActions()

		self.defaultSettings = RIR_Settings(self)
		self.currentSettings = RIR_Settings(self)
		self.presets = {}
		self.RIRCore.loadPresets(self.RIRCore.presetFile)

	def createUI(self, UIFile):
		PyUI = PySideUI.newUI(UIFile)
		return PyUI

	def showUI(self):
		self.bindUIFunctions()
		self.PyUI.show()

	def getMenuActions(self):
		menuBar = self.PyUI.menubar.actions()
		presetsMenu = menuBar[0].menu()
		self.presetsMenu = presetsMenu
		self.resetToDefaultMenu = presetsMenu.actions()[0]
		self.loadPresetMenu = presetsMenu.actions()[1]
		self.loadPresetMenu.setMenu(QtWidgets.QMenu())
		self.loadPresetMenu.menu().setTearOffEnabled(True)
		self.savePresetMenu = presetsMenu.actions()[2]
		self.deletePresetMenu = presetsMenu.actions()[3]

		self.savePresetMenu.triggered.connect(self.on_MB_Presets_Save_triggered)
		self.deletePresetMenu.triggered.connect(self.on_MB_Presets_Delete_triggered)
		self.resetToDefaultMenu.triggered.connect(self.on_MB_Presets_Reset_triggered)

	def updateSettingsValues(self, getmode = 1, setmode = 0):
		cs = self.currentSettings

		at = cs.getApplyTo(getmode)
		cs.setApplyTo(at['X'], at['Y'], at['Z'], setmode)
		rsas = cs.getRndSeedAndScale(getmode)
		cs.setRndSeedAndScale(rsas['RndSeed'], rsas['RndScale'], setmode)
		ls = cs.getLocationSettings(getmode)
		cs.setLocationSettings(ls['Enabled'], ls['Clamp'], ls['RndMin'], ls['RndMax'], setmode)
		rs = cs.getRotationSettings(getmode)
		cs.setRotationSettings(rs['Enabled'], rs['Clamp'], rs['RndMin'], rs['RndMax'], setmode)
		ss = cs.getScaleSettings(getmode)
		cs.setScaleSettings(ss['Enabled'], ss['Clamp'], ss['RndMin'], ss['RndMax'], setmode)

	def setUIValues(self, settings, getmode = 0, setmode = 1):
		cs = self.currentSettings

		at = settings.ApplyTo
		cs.setApplyTo(at['X'], at['Y'], at['Z'], setmode)
		rsas = settings.RndSeedAndScale
		cs.setRndSeedAndScale(rsas['RndSeed'], rsas['RndScale'], setmode)
		ls = settings.LocationSettings
		cs.setLocationSettings(ls['Enabled'], ls['Clamp'], ls['RndMin'], ls['RndMax'], setmode)
		rs = settings.RotationSettings
		cs.setRotationSettings(rs['Enabled'], rs['Clamp'], rs['RndMin'], rs['RndMax'], setmode)
		ss = settings.ScaleSettings
		cs.setScaleSettings(ss['Enabled'], ss['Clamp'], ss['RndMin'], ss['RndMax'], setmode)


	def presetNamePrompt(self):
		result = cmds.promptDialog(
						title = 'Preset Name',
						message = 'Enter Name:',
						button = ['OK', 'Cancel'],
						defaultButton = 'OK',
						cancelButton = 'Cancel',
						dismissString = 'Cancel')
		name = None
		if result == 'OK':
			name = cmds.promptDialog(query = True, text = True)

		return name

	#=== Menu Bar Actions ===
	def on_MB_Presets_Save_triggered(self):
		presetName = self.presetNamePrompt()
		presetFile = self.RIRCore.presetFile

		if not (presetName == None):
			self.RIRCore.savePreset(presetFile, presetName, RIR_Settings(self))

	def on_MB_Presets_Load_triggered(self, name):
		self.setUIValues(self.presets[name]['Settings'], 0, 2)

	def on_MB_Presets_Delete_triggered(self):
		presetName = self.presetNamePrompt()
		self.RIRCore.removePresetFromUI(presetName)

	def on_MB_Presets_Reset_triggered(self):
		self.setUIValues(self.defaultSettings, 0, 2)

	#=== ApplyToAxis Checkboxes ===
	def on_CB_ApplyToX_toggled(self, checked): #bool
		self.updateSettingsValues()

	def on_CB_ApplyToY_toggled(self, checked): #bool
		self.updateSettingsValues()

	def on_CB_ApplyToZ_toggled(self, checked): #bool
		self.updateSettingsValues()

	#=== Random Seed and Scale ===
	def on_SB_RandomSeed_valueChanged(self, value): #int
		cs = self.currentSettings
		cs.setRndSeedAndScale(value, cs.getRndSeedAndScale(1)['RndScale'])

	def on_B_RandomSeed_clicked(self):
		newRndSeed = self.RIRCore.newRandomSeed()
		cs = self.currentSettings
		cs.setRndSeedAndScale(newRndSeed, cs.getRndSeedAndScale(1)['RndScale'], 2)

	def on_SB_dRandomScale_valueChanged(self, value): #double
		cs = self.currentSettings
		cs.setRndSeedAndScale(cs.getRndSeedAndScale(1)['RndSeed'], value)

	#=== Location ===
	def on_GB_Location_toggled(self, checked): #bool
		self.updateSettingsValues()

	def on_CB_LocationClamp_toggled(self, checked): #bool
		self.updateSettingsValues()

	def on_SB_dLocationMin_valueChanged(self, value): #double
		cs = self.currentSettings
		mode = 0
		if (value > cs.LocationSettings['RndMax']):
			value = cs.LocationSettings['RndMin']
			mode = 2
		cs.setLocationSettings(cs.LocationSettings['Enabled'],
								cs.LocationSettings['Clamp'],
								value,
								cs.LocationSettings['RndMax'],
								mode )

	def on_SB_dLocationMax_valueChanged(self, value): #double
		cs = self.currentSettings
		mode = 0
		if (value < cs.LocationSettings['RndMin']):
			value = cs.LocationSettings['RndMax']
			mode = 2
		cs.setLocationSettings(cs.LocationSettings['Enabled'],
								cs.LocationSettings['Clamp'],
								cs.LocationSettings['RndMin'],
								value,
								mode )

	#=== Rotation ===
	def on_GB_Rotation_toggled(self, checked): #bool
		self.updateSettingsValues()

	def on_CB_RotationClamp_toggled(self, checked): #bool
		self.updateSettingsValues()

	def on_SB_dRotationMin_valueChanged(self, value): #double
		cs = self.currentSettings
		cs = self.currentSettings
		mode = 0
		if (value > cs.RotationSettings['RndMax']):
			value = cs.RotationSettings['RndMin']
			mode = 2
		cs.setRotationSettings(cs.RotationSettings['Enabled'],
								cs.RotationSettings['Clamp'],
								value,
								cs.RotationSettings['RndMax'],
								mode )

	def on_SB_dRotationMax_valueChanged(self, value): #double
		cs = self.currentSettings
		mode = 0
		if (value < cs.RotationSettings['RndMin']):
			value = cs.RotationSettings['RndMax']
			mode = 2
		cs.setRotationSettings(cs.RotationSettings['Enabled'],
								cs.RotationSettings['Clamp'],
								cs.RotationSettings['RndMin'],
								value,
								mode )

	#=== Scale ===
	def on_GB_Scale_toggled(self, checked): #bool
		self.updateSettingsValues()

	def on_CB_ScaleClamp_toggled(self, checked): #bool
		self.updateSettingsValues()

	def on_SB_dScaleMin_valueChanged(self, value): #double
		cs = self.currentSettings
		cs = self.currentSettings
		mode = 0
		if (value > cs.ScaleSettings['RndMax']):
			value = cs.ScaleSettings['RndMin']
			mode = 2
		cs.setScaleSettings(cs.ScaleSettings['Enabled'],
								cs.ScaleSettings['Clamp'],
								value,
								cs.ScaleSettings['RndMax'],
								mode)

	def on_SB_dScaleMax_valueChanged(self, value): #double
		cs = self.currentSettings
		mode = 0
		if (value < cs.ScaleSettings['RndMin']):
			value = cs.ScaleSettings['RndMax']
			mode = 2
		cs.setScaleSettings(cs.ScaleSettings['Enabled'],
								cs.ScaleSettings['Clamp'],
								cs.ScaleSettings['RndMin'],
								value,
								mode )

	#=== Apply and Reset Transform ===
	def on_B_Reset_clicked(self):
		self.RIRCore.resetTransforms()

	def on_B_Apply_clicked(self):
		modifiers = QtWidgets.QApplication.keyboardModifiers()
		if(modifiers == QtCore.Qt.AltModifier):
			print("ALT")
			self.on_B_Reset_clicked()
			self.on_B_RandomSeed_clicked()
			self.RIRCore.applyTransforms(self.currentSettings)
		else:
			self.RIRCore.applyTransforms(self.currentSettings)


	#=== Bind events to corresponding functions ===
	def bindUIFunctions(self):
		self.PyUI.CB_ApplyToX.toggled.connect(self.on_CB_ApplyToX_toggled)
		self.PyUI.CB_ApplyToY.toggled.connect(self.on_CB_ApplyToY_toggled)
		self.PyUI.CB_ApplyToZ.toggled.connect(self.on_CB_ApplyToZ_toggled)

		self.PyUI.SB_RandomSeed.valueChanged.connect(self.on_SB_RandomSeed_valueChanged)
		self.PyUI.B_RandomSeed.clicked.connect(self.on_B_RandomSeed_clicked)
		self.PyUI.SB_dRandomScale.valueChanged.connect(self.on_SB_dRandomScale_valueChanged)

		self.PyUI.GB_Location.toggled.connect(self.on_GB_Location_toggled)
		self.PyUI.CB_LocationClamp.toggled.connect(self.on_CB_LocationClamp_toggled)
		self.PyUI.SB_dLocationMin.valueChanged.connect(self.on_SB_dLocationMin_valueChanged)
		self.PyUI.SB_dLocationMax.valueChanged.connect(self.on_SB_dLocationMax_valueChanged)

		self.PyUI.GB_Rotation.toggled.connect(self.on_GB_Rotation_toggled)
		self.PyUI.CB_RotationClamp.toggled.connect(self.on_CB_RotationClamp_toggled)
		self.PyUI.SB_dRotationMin.valueChanged.connect(self.on_SB_dRotationMin_valueChanged)
		self.PyUI.SB_dRotationMax.valueChanged.connect(self.on_SB_dRotationMax_valueChanged)

		self.PyUI.GB_Scale.toggled.connect(self.on_GB_Scale_toggled)
		self.PyUI.CB_ScaleClamp.toggled.connect(self.on_CB_ScaleClamp_toggled)
		self.PyUI.SB_dScaleMin.valueChanged.connect(self.on_SB_dScaleMin_valueChanged)
		self.PyUI.SB_dScaleMax.valueChanged.connect(self.on_SB_dScaleMax_valueChanged)

		self.PyUI.B_Reset.clicked.connect(self.on_B_Reset_clicked)
		self.PyUI.B_Apply.clicked.connect(self.on_B_Apply_clicked)

		#happens to be the only way to do this properly? (don't like it really)
		#don't do this at home kids: monkeypatching
		self.PyUI.closeEvent = self.onMainWindowClose

	def onMainWindowClose(self, event):
		"""reimplementing the closeEvent to unbind all evencallbacks"""
		result = cmds.confirmDialog(
						title = 'Closing RIR!',
						message = 'Changes made with RealismIsRandom will not be undoable!',
						button = ['OK', 'Cancel'],
						defaultButton = 'OK',
						cancelButton = 'Cancel',
						dismissString = 'Cancel')
		if result == 'Cancel':
			event.ignore() #ignores the close of the window

			self.RIRCore.removeCallbacks()
			closeRIR(self)
