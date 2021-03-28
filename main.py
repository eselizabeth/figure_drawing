from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.lang import Builder
from kivy import Config
from kivy.clock import Clock
from plyer import filechooser
from datetime import datetime, timedelta
import os
import random




class CustomPopup(Popup):
	pass

class FirstWindow(Screen):

	def on_enter(self):
		App.get_running_app().fileList = []
		App.get_running_app().path = ''
		self.ids.folderName.text = ''
		self.ids.slider1.value = 0
		self.ids.slider2.value = 0
		self.ids.current.text = datetime.now().strftime("%H:%M")
		self.ids.finish.text = datetime.now().strftime("%H:%M")
		self.ids.letsdraw.disabled = True

	def selectFolder(self):
		App.get_running_app().path = filechooser.choose_dir(title="Select a folder")
		if App.get_running_app().path:
			App.get_running_app().path = App.get_running_app().path[0]
			folderName = App.get_running_app().path.split('\\')[-1]
			App.get_running_app().fileList = [file for file in os.listdir(App.get_running_app().path) if file.endswith(('.png', '.jpg', '.bmp', '.gif'))]
			self.ids.folderName.text = f"{folderName}, {len(App.get_running_app().fileList)} images exist"
			random.shuffle(App.get_running_app().fileList)

	def update(self):
		minutes = int(self.ids.slider1.value * self.ids.slider2.value / 60)
		currentTime = datetime.now().strftime("%H:%M")
		finishTime = (datetime.now() + timedelta(minutes = minutes)).strftime("%H:%M")
		self.ids.current.text = currentTime
		self.ids.finish.text = finishTime
		App.get_running_app().timerPerDrawing = int(self.ids.slider1.value)
		App.get_running_app().numberOfDrawings = int(self.ids.slider2.value)
		if len(App.get_running_app().fileList) >= 1 and App.get_running_app().timerPerDrawing > 0 and App.get_running_app().numberOfDrawings > 0:
				self.ids.letsdraw.disabled = False
				
class SecondWindow(Screen):

	def on_enter(self):
		self.ids.img.source = f'{App.get_running_app().path}\\{App.get_running_app().fileList[0]}'
		self.clock = Clock.schedule_interval(self.updateLabel, 1)
		if App.get_running_app().timerPerDrawing > 99:
			self.ids.timer.size = (70, 70)
		self.ids.timer.text = str(App.get_running_app().timerPerDrawing)

	def updateLabel(self, *args):
		self.ids.timer.text = str(int(self.ids.timer.text) - 1)
		if int(self.ids.timer.text) == -1:
			self.nextImage()

	def change(self, direction):
		App.get_running_app().counter += direction
		if(App.get_running_app().counter == len(App.get_running_app().fileList) - 1 or len(App.get_running_app().fileList) == 1):
			App.get_running_app().counter = 0
		self.ids.timer.text = str(App.get_running_app().timerPerDrawing)
		self.ids.img.source = f'{App.get_running_app().path}\\{App.get_running_app().fileList[App.get_running_app().counter]}'
		App.get_running_app().numberOfDrawings -= 1
		if(App.get_running_app().numberOfDrawings == 0):
			self.clock.cancel()
			popup = CustomPopup()
			popup.open()	

	def manageTime(self):
		if(self.ids.stop.text) == "||":
			self.ids.stop.text = "|>"
			self.clock.cancel()
		elif(self.ids.stop.text) == "|>":
			self.ids.stop.text = "||"
			self.clock = Clock.schedule_interval(self.updateLabel, 1)	




class MainApp(App):

	counter = 0
	def build(self):
		Window.minimum_width, Window.minimum_height = (650, 600)
		self.title = "FigureDrawing"
		self.icon = ''
		sManager = ScreenManager(transition=FadeTransition())
		fWindow = FirstWindow()
		sWindow = SecondWindow()
		sManager.add_widget(fWindow)
		sManager.add_widget(sWindow)
		return sManager

if __name__ == '__main__':
	application = MainApp()
	application.run()
