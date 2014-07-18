from singleton import Singleton

@Singleton
class CollisionToSceneCommunication:

	def __init__(self, selectionMethod, allObjectsMethod):
		self.__getSelectionMethod = selectionMethod
		self.__getAllObjectsMethod = allObjectsMethod

	def getSelectedObjects(self):
		return self.__getSelectionMethod()

	def getAllObjects(self):
		return self.__getAllObjectsMethod() 

@Singleton
class CollisionToMainLayoutCommunication:

	def __init__(self, giveBackKeyboardMethod):
		self.__giveBackKeyboardMethod = giveBackKeyboardMethod

	def giveBackKeyboard(self):
		self.__giveBackKeyboardMethod()