from singleton import Singleton

from os.path import join
from os import listdir, getcwd

from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from editorobjects import BaseObject
from objectdescriptor import ObjectDescriptor
from editorutils import EmptyScrollEffect
from communicationobjects import SceneToObjectsMenu
from splittedimagemap import SplittedImageImporter

class ObjectMenuItem:

	def __handle(self, image, touch):
		if (touch.is_mouse_scrolling == False and self.getDisplayImage().collide_point(*touch.pos) == True and
				touch.is_double_tap == True):
			if (ObjectDescriptor.Instance().getCurrentObject() == self.getBaseObject()):
				SceneToObjectsMenu.Instance().draw(self.getBaseObject())
			else:
				ObjectDescriptor.Instance().setObject(self.getBaseObject())

	def __init__(self, baseObject, size):
		self.__baseObject = baseObject
		self.__displayImage = Image(texture = baseObject.getBaseImage().texture, size = size, size_hint = (None, None),
			on_touch_down = self.__handle)

	def getBaseObject(self):
		return self.__baseObject

	def getDisplayImage(self):
		return self.__displayImage

@Singleton
class ObjectsMenu:

	def __loadPng(self, item, pngsToIgnoreList):
		fullPath = join(getcwd(), 'tiles', item)
		if (fullPath in pngsToIgnoreList):
			return

		img = Image(source = fullPath)
		obj = BaseObject(img, self.__baseObjectId)
		self.__menuObjectsList.append(ObjectMenuItem(obj, (64, 64)))
		self.__numberOfItems += 1
		self.__baseObjectId += 1

	def __loadOpf(self, item, pngsToIgnoreList):
		resourceInfo = SplittedImageImporter.load(join(getcwd(), 'tiles',item))
		mainImage = Image (source = resourceInfo.getPath())
		for selection in resourceInfo.getSelectionList():
			x = selection.getX()
			y = selection.getY()
			width = selection.getSizeX()
			height = selection.getSizeY()
			newTexture = mainImage.texture.get_region(x, y, width, height)
			image = Image(texture = newTexture, size = (width, height), size_hint = (None, None))
			obj = BaseObject(image, self.__baseObjectId, resourceInfo.getPath(), (x, y))
			self.__menuObjectsList.append(ObjectMenuItem(obj, (64, 64)))
			self.__numberOfItems += 1
			self.__baseObjectId += 1

		pngsToIgnoreList.append(obj.getPath())

	def __loadItems(self):
		l = listdir(join(getcwd(), 'tiles'))
		self.__menuObjectsList = []
		self.__numberOfItems = 0
		self.__baseObjectId = 0
		pngsToIgnoreList = []
		for item in l:
			if (item[-4:] == '.opf'):
				self.__loadOpf(item, pngsToIgnoreList)
				

		for item in l:
			if (item[-4:] == '.png' and item not in pngsToIgnoreList):
				self.__loadPng(item, pngsToIgnoreList)

		if (self.__objectListLayout is None):
			self.__objectListLayout = GridLayout(cols=1, rows = self.__numberOfItems, size_hint = (None, None),
				spacing = (0, 3))
		else:
			self.__objectListLayout.rows = self.__numberOfItems

		for menuObject in self.__menuObjectsList:
			img = menuObject.getDisplayImage()
			self.__objectListLayout.add_widget(img)

		self.__objectListLayout.size[1] = (self.__numberOfItems * 67)

	def __init__(self):
		self.__objectListLayout = None

		self.__loadItems()

		self.__scrollView = ScrollView(size_hint = (1.0, 1.0), do_scroll = (0, 1), effect_cls = EmptyScrollEffect)
		self.__scrollView.add_widget(self.__objectListLayout)
		self.__scrollView.do_scroll_x = False

	def reloadResource(self, resourceInfo):
		pass

	def getLayout(self):
		return self.__scrollView

	def resetAllWidgets(self):
		for menuObject in self.__menuObjectsList:
			self.__layout.remove_widget(menuObject.getDisplayImage())
			menuObject = None

		self.__loadItems()

