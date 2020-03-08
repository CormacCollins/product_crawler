import kivy
import os
import sys
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.base import runTouchApp
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.lang import Builder
kivy.require("1.11.0")



class SampFloatLayout(FloatLayout):

  
  def spinner_clicked(self, value):
    print("Spinner Value " + value)

presentation = Builder.load_file("Nut.kv") #telling the app which .kv file to use

class NutritionApp(App):

  def build(self):
    Window.clearcolor = (1,1,1,1)
    return SampFloatLayout()

nutrionApp = NutritionApp()
nutrionApp.run()