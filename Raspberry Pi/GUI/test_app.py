import kivy
from kivy.app import App
#from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.properties import ObjectProperty
from kivy.clock import Clock
#Clock.max_iteration = 20
from kivy.lang import Builder
from kivy.properties import *
import time

Builder.load_file('test_app.kv')
kivy.require("1.11.1")
Window.clearcolor = (.827, .827, .827, 1)

class DefaultLabel(Label):
    pass

class Time(DefaultLabel):
    def update(self, *args):
        self.text = time.strftime('%H:%M:%S')

class TimeInfo(DefaultLabel):
    now_time = Time()
    now_time.text = time.strftime('%H:%M:%S')
    Clock.schedule_interval(now_time.update,1)

class DateInfo(DefaultLabel):
    now_date = Time()
    now_date.text = time.strftime('%d %B %Y')
    Clock.schedule_interval(now_date.update,1)

class DateTime(BoxLayout):
    pass
class StatusBar(BoxLayout):
    pass

class Taskbar(BoxLayout):
    def btn_home(self):
        screen_manager.transition = SlideTransition()
        screen_manager.transition.direction = 'right'
        screen_manager.current = 'home'
    def btn_ac(self):
        screen_manager.transition = NoTransition()
        screen_manager.current = 'ac'
    def btn_email(self):
        screen_manager.transition = NoTransition()
        screen_manager.current = 'email'
    def btn_settings(self):
        screen_manager.transition = NoTransition()
        screen_manager.current = 'setting'
    def btn_log(self):
        screen_manager.transition = NoTransition()
        screen_manager.current = 'log'
    def btn_report(self):
        screen_manager.transition = NoTransition()
        screen_manager.current = 'report'

class LoginPage(Screen):
    def check_login(self):
        user_text = self.ids.username.text
        password_text = self.ids.password.text
        if user_text == "abc" and password_text == "123":
            screen_manager.transition = SlideTransition(direction='left')
            screen_manager.current = "home" 
            
        else:
            info = self.ids.info
            info.text = '[color=#FF0000]Username and password not found[/color]'


class Home(Screen):
    pass

class ACControl(Screen):
    pass

class Email(Screen):
    pass

class Setting(Screen):
    pass

class Report(Screen):
    pass

class Log(Screen):
    pass

screen_manager = ScreenManager()
screens = [LoginPage(name="login"),Home(name="home"),Report(name="report"),ACControl(name="ac"),Email(name="email"),Setting(name="setting"),Log(name="log")]
for screen in screens:
    screen_manager.add_widget(screen)
screen_manager.current = "login"

class ServerApp(App):
    def build(self):
        return screen_manager

if __name__ == "__main__":
    my_app = ServerApp()
    my_app.run()