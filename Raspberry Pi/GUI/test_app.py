import kivy
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
Clock.max_iteration = 20
from kivy.lang import Builder
from kivy.properties import *
import time

Builder.load_file('test_app.kv')
kivy.require("1.11.1")
Window.clearcolor = (.06, .45, .45, 1)


class Time(Label):
    def update(self, *args):
        self.text = time.strftime('%H:%M:%S')

class DateTime(BoxLayout):
    now_time = Time()
    now_date = Time()
    now_time.text = time.strftime('%H %M %S')
    now_date.text = time.strftime('%d %B %Y')
    #Clock.schedule_interval(now_time.update,1)

class LoginPage(Screen):
    def check_login(self):
        user_text = self.ids.username.text
        password_text = self.ids.password.text
        if user_text == "abc" and password_text == "123":
            self.manager.current = "status" 
        else:
            info = self.ids.info
            info.text = '[color=#FF0000]Username and password not found[/color]'
        
class Status(Screen):
    pass

class ACControl(Screen):
    pass

class Email(Screen):
    pass

class Settings(Screen):
    pass

class ServerApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginPage(name="login"))
        screen_manager.add_widget(Status(name="status"))
        screen_manager.add_widget(ACControl(name="ac"))
        screen_manager.add_widget(Email(name="email"))
        screen_manager.add_widget(Settings(name="settings"))
        return screen_manager

if __name__ == "__main__":
    my_app = ServerApp()
    my_app.run()