from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.textinput import TextInput
from kivy.graphics.texture import Texture
from kivy.effects.scroll import ScrollEffect

from os.path import sep as pathSeparator
from os import getcwd

class CancelableButton (Button):

	def __getActionByEntry(self, key, dictToLook):
		if (key in dictToLook):
			self.__action = dictToLook[key]
			del dictToLook[key]
			return True

		else:
			return False

	def __processAction(self, touch):
		if (self.collide_point(*touch.pos) == True and self.__lastUid != touch.uid and touch.uid == self.__touchUpUid):
			self.__lastUid = touch.uid
			self.__action(self, touch)

		self.__default_on_touch_up(touch)

	def __startButtonSelection(self, touch):
		if (self.collide_point(*touch.pos) == True):
			self.__touchUpUid = touch.uid

		self.__default_on_touch_down(touch)

	def __init__(self, **kwargs):
		assert (not ('on_release' in kwargs and 'on_touch_up' in kwargs))
		
		if (self.__getActionByEntry('on_release', kwargs) == False and self.__getActionByEntry('on_touch_up', kwargs) == False):
			self.__action = None

		super(CancelableButton, self).__init__(**kwargs)
		if (self.__action is not None):
			self.__lastUid = None
			self.__default_on_touch_up = self.on_touch_up
			self.on_touch_up = self.__processAction
			self.__default_on_touch_down = self.on_touch_down
			self.on_touch_down = self.__startButtonSelection


def strToDoubleFloatTuple(s):
	assert(type(s) is str)
	splitted = s.split(',')
	assert(len(splitted) == 2)
	x = float(splitted[0].replace('(', ''))
	y = float(splitted[1].replace(')', ''))
	return (x, y)

def strToDoubleIntTuple(s):
	assert(type(s) is str)
	splitted = s.split(',')
	assert(len(splitted) == 2)
	x = int(splitted[0].replace('(', ''))
	y = int(splitted[1].replace(')', ''))
	return (x, y)

def vector2ToVector3String(v, default = 0):
	return '(' + str(v[0]) + ', ' + str(v[1]) + ', ' + str (default) + ')'

def vector2Multiply(v, x):
	assert(type(v) is tuple or type(v) is list)
	assert(len(v) == 2)
	if (type(v) is tuple):
		return (v[0] * x, v[1] * x)
	else:
		return [v[0] * x, v[1] * x]
	

def copyTexture(sizeToUse, imageToUse):
	newTexture = Texture.create(size = sizeToUse)
	pixels = imageToUse.texture.pixels[:]
	newTexture.blit_buffer(pixels, colorfmt='rgba', bufferfmt='ubyte')
	newTexture.flip_vertical()

	return newTexture

class EmptyScrollEffect(ScrollEffect):
	pass
	
class BaseWarnMethods:

	def open(self):
		self.mainPopUp.open()

	def setTitle(self, value):
		self.mainPopUp.title = value

	def setText(self, value):
		self.mainPopUpText.text = value

	def dismiss(self):
		self.mainPopUp.dismiss()


class Dialog (BaseWarnMethods):

	def __doNothing(self, notUsed = None):
		return None

	def __init__(self, okMethod = None, dialogTitle = '', dialogText = '', dialogOkButtonText = '', dialogCancelButtonText = ''):
		
		self.mainPopUp = Popup(title = dialogTitle, auto_dismiss = False, size_hint = (0.7, 0.5))
		self.mainPopUpText = Label(text = dialogText)
		popUpLayout = BoxLayout(orientation = 'vertical')
		yesNoLayout = BoxLayout(orientation = 'horizontal', size_hint = (1.0, 0.3))
		
		if (okMethod is None):
			self.__okMethod = self.__doNothing
		else:
			self.__okMethod = okMethod
		
		self.__dialogOkButton = CancelableButton(text = dialogOkButtonText, on_release = self.__okMethod)
		popUpLayout.add_widget(self.mainPopUpText)
		yesNoLayout.add_widget(self.__dialogOkButton)
		yesNoLayout.add_widget(CancelableButton(text = dialogCancelButtonText, on_release = self.mainPopUp.dismiss))
		popUpLayout.add_widget(yesNoLayout)
		self.mainPopUp.content = popUpLayout

class AlertPopUp (BaseWarnMethods):
	
	def __init__(self, alertTitle = '', alertText = '', closeButtonText = ''):
		self.mainPopUp = Popup(
			title = alertTitle, 
			auto_dismiss = False,
			size_hint = (0.5, 0.5)
		)
		mainPopUpBox = BoxLayout(orientation = 'vertical')
		self.mainPopUpText = Label(
			text = alertText, size_hint = (1.0, 0.7)
		)
		mainPopUpBox.add_widget(self.mainPopUpText)
		mainPopUpBox.add_widget(CancelableButton(text = closeButtonText, size_hint = (1.0, 0.3), 
			on_release = self.mainPopUp.dismiss))
		self.mainPopUp.content = mainPopUpBox

class FileSelectionPopup:

	def __setFilenameWithoutTheFullPath(self, entry, notUsed = None):
		sepIndex = entry[0].rfind(pathSeparator)
		if (sepIndex != -1):
			self.__chosenFileInput.text = entry[0][sepIndex+1:]
		else:
			self.__chosenFileInput.text = entry[0]

	def __init__(self, title = '', filters = ['*'], cancelButtonText = 'Cancel', size = (1.0, 1.0)):
		self.__contentPopup = Popup(title = title, auto_dismiss = False, size = size)
		self.__chosenFileInput = TextInput (text = '', multiline = False)
		self.__fileChooser = FileChooserIconView(path = getcwd(), filters = filters)
		self.__fileChooser.on_submit = self.__setFilenameWithoutTheFullPath
		self.__cancelButton = CancelableButton(text = cancelButtonText, on_release = self.__contentPopup.dismiss)

	def getFileChooser (self):
		return self.__fileChooser

	def getTextInput (self):
		return self.__chosenFileInput

	def getCancelButton(self):
		return self.__cancelButton

	def setContent(self, value):
		self.__contentPopup.content = value

	def open(self, *args):
		self.__contentPopup.open()

	def dismiss(self, *args):
		self.__contentPopup.dismiss()


class AutoReloadTexture:

	def __reloadTexture(self, textureToReload):
		textureToReload.blit_buffer(self.__pixels, colorfmt='rgba', bufferfmt='ubyte')
		textureToReload.flip_vertical()

	def __init__(self, sizeToUse, imageToUse):
		self.__size = sizeToUse
		self.__texture = Texture.create(size = self.__size)
		self.__pixels = imageToUse.texture.pixels[:]
		self.__texture.blit_buffer(self.__pixels, colorfmt='rgba', bufferfmt='ubyte')
		self.__texture.flip_vertical()
		self.__texture.add_reload_observer(self.__reloadTexture)

	def getTexture(self):
		return self.__texture
		
