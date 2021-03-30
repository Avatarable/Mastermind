from kivy.config import Config
Config.set('graphics', 'resizable', '0')

import random
import os, json
from win32api import GetSystemMetrics

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window


class LoginPage(Screen):
    def on_enter(self, *args):
        if os.path.isfile('prev_details.json'):
            with open('prev_details.json') as json_file:
                try:
                    data = json.load(json_file)
                    data_normal = data['normal']
                    data_super = data['super']

                    best_name_normal = list(data_normal.keys())[0]
                    best_score_normal = list(data_normal.values())[0]

                    best_name_super = list(data_super.keys())[0]
                    best_score_super = list(data_super.values())[0]

                    scores = {'normal': {best_name_normal:best_score_normal}, 'super':{best_name_super:best_score_super}}
                    # print(scores)
                except:
                    scores = {}

class SignupPage(BoxLayout):
    def login(self):
        nickname = self.ids.nickname.text
        if len(nickname.strip())>0:
            NormalScreen.user = nickname
            login_app.root.current = "GameScreen"
        else:
            warning('Invalid Login', 'Required field cannot be blank')

class SuperSignupPage(BoxLayout):
    def login(self):
        nickname = self.ids.nickname.text
        if len(nickname.strip())>0:
            SuperScreen.user = nickname
            login_app.root.current = "SuperGameScreen"
        else:
            warning('Invalid Login', 'Required field cannot be blank')



class Content(BoxLayout):
    pass
class NewDialog(MDDialog):
    pass

class DrawerList(ThemableBehavior, MDList):
    pass

class ProposedColors(GridLayout):
    pass

class SuperProposedColors(GridLayout):
    pass

class RoundedButton(Button):
    pass


class NormalScreen(Screen):
    dialog = None
    global available_colors
    global selected_colors_list
    user = ""
    best_name = ""
    best_score = ""
    selected_colors_list = []
    available_colors = [(0.0, 0.0, 1.0, 1.0), (1.0, 0.0, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (1.0, 0.4, 0.8, 1.0), (0.9, 0.9, 0.9, 1.0)]

    def defaults(self):
        self.tries = 0
        self.selected_colors_list = [(0.0, 0.0, 1.0, 1.0), (1.0, 0.0, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0)]
        if os.path.isfile('prev_details.json'):
            with open('prev_details.json') as json_file:
                try:
                    data = json.load(json_file)
                    data = data['normal']
                    self.best_name = list(data.keys())[0]
                    self.best_score = list(data.values())[0]
                except:
                    self.best_name = ""
                    self.best_score = ""
        self.ids.list_toolbar.title = f"Player:  {self.user}               Best Score: {self.best_score}({self.best_name})"

        self.game_colors = random.sample(available_colors, 4)             # Colors to guess
        # print(self.game_colors)



    def on_enter(self, *args):
        self.defaults()

    def add_color(self, btn, text):
        switcher = {
            'Blue':(0.0, 0.0, 1.0, 1.0), 'Red': (1.0, 0.0, 0.0, 1.0),
            'Yellow':(1.0, 1.0, 0.0, 1.0), 'Green':(0.0, 1.0, 0.0, 1.0),
            'Pink':(1.0, 0.4, 0.8, 1.0), 'Grey':(0.9, 0.9, 0.9, 1.0)
        }
        color = switcher.get(text)

        self.selected_colors_list[btn] = color


    def add_item(self):
        self.row = ProposedColors()
        self.ids.list_content.add_widget(
            self.row
        )
        self.row.ids['color1'].background_color = self.selected_colors_list[0]
        self.row.ids['color2'].background_color = self.selected_colors_list[1]
        self.row.ids['color3'].background_color = self.selected_colors_list[2]
        self.row.ids['color4'].background_color = self.selected_colors_list[3]

        self.output = [(0.6, 0.6, 0.6, 1.0),(0.6, 0.6, 0.6, 1.0),(0.6, 0.6, 0.6, 1.0),(0.6, 0.6, 0.6, 1.0)]

        n = 0
        right_pos = 0
        checked = []

        for color in self.selected_colors_list:
            if checked.count(color) == 0:
                t = self.game_colors.count(color)
                n += t
                checked.append(color)
        for i in range(len(self.game_colors)):
            if self.selected_colors_list[i] == self.game_colors[i]:
                right_pos += 1
        for j in range(n):
            self.output[j] = (1.0, 1.0, 1.0, 1.0)
        for k in range(right_pos):
            self.output[k] = (0.0, 0.0, 0.0, 1.0)

        checker = ProposedColors()
        self.ids.check_list.add_widget(
            checker
        )
        checker.ids['color1'].background_color = self.output[0]
        checker.ids['color1'].size = (20,20)
        checker.ids['color2'].background_color = self.output[1]
        checker.ids['color2'].size = (20,20)
        checker.ids['color3'].background_color = self.output[2]
        checker.ids['color3'].size = (20,20)
        checker.ids['color4'].background_color = self.output[3]
        checker.ids['color4'].size = (20,20)

        self.tries += 1

        if self.selected_colors_list == self.game_colors:
            if self.best_score == "":
                self.best_score = 10
            if self.tries < int(self.best_score):
                self.best_score = self.tries
                self.best_name = self.user
                self.save_score()
            self.show_alert_dialog('                    You won! Congratulations!!\n                    Play again??')

        if self.tries == 10:
            self.show_alert_dialog('                     Game Over!!    Play again??')


    def play_again(self, e):
        self.ids.list_content.clear_widgets()
        self.ids.check_list.clear_widgets()
        self.defaults()
        self.dialog.dismiss()
        self.dialog = None

    def save_score(self):
        data = {self.user: self.best_score}
        scores['normal'] = data
        if os.path.isfile('prev_details.json'):
            with open('prev_details.json', 'w') as file:
                json.dump(scores, file)
                # file.write(self.user+"|"+str(self.best_score))


    def logout(self, e):
        login_app.root.current = "Login"
        if self.dialog != None:
            self.dialog.dismiss()
            self.dialog = None
        self.ids.list_content.clear_widgets()
        self.ids.check_list.clear_widgets()

    def show_alert_dialog(self, txt):
        if not self.dialog:
            self.dialog = MDDialog(
                title="",
                text=txt,
                buttons=[
                    MDFlatButton(
                        text="NO", text_color=login_app.theme_cls.primary_color, on_release=self.logout
                    ),
                    MDFlatButton(
                        text="OK", text_color=login_app.theme_cls.primary_color, on_release=self.play_again
                    ),
                ],
            )
            self.dialog.set_normal_height()
            self.dialog.open()


class SuperScreen(Screen):
    dialog = None
    global super_available_colors
    global super_selected_colors_list
    user = ""
    best_name = ""
    best_score = ""
    super_selected_colors_list = []
    super_available_colors = [(0.0, 0.0, 1.0, 1.0), (1.0, 0.0, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0),
                        (1.0, 0.4, 0.8, 1.0), (0.9, 0.9, 0.9, 1.0),(0.6, 0.0, 0.9, 1.0), (0.8, 0.6, 0.6, 1.0)]

    def defaults(self):
        self.tries = 0
        self.super_selected_colors_list = [(0.0, 0.0, 1.0, 1.0), (1.0, 0.0, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (0.9, 0.9, 0.9, 1.0)]
        if os.path.isfile('prev_details.json'):
            with open('prev_details.json') as json_file:
                try:
                    data = json.load(json_file)
                    data = data['super']
                    self.best_name = list(data.keys())[0]
                    self.best_score = list(data.values())[0]
                except:
                    self.best_name = ""
                    self.best_score = ""

        self.ids.list_toolbar.title = f"Player:  {self.user}               Best Score: {self.best_score}({self.best_name})"

        self.game_colors = random.sample(super_available_colors, 5)             # Colors to guess
        # print(self.game_colors)



    def on_enter(self, *args):
        self.defaults()

    def add_color(self, btn, text):
        switcher = {
            'Blue':(0.0, 0.0, 1.0, 1.0), 'Red': (1.0, 0.0, 0.0, 1.0),
            'Yellow':(1.0, 1.0, 0.0, 1.0), 'Green':(0.0, 1.0, 0.0, 1.0),
            'Pink':(1.0, 0.4, 0.8, 1.0), 'Grey':(0.9, 0.9, 0.9, 1.0),
            'Purple':(0.6, 0.0, 0.9, 1.0), 'Brown':(0.8, 0.6, 0.6, 1.0)
        }
        color = switcher.get(text)

        self.super_selected_colors_list[btn] = color


    def add_item(self):
        self.row = SuperProposedColors()
        self.ids.list_content.add_widget(
            self.row
        )
        self.row.ids['color1'].background_color = self.super_selected_colors_list[0]
        self.row.ids['color2'].background_color = self.super_selected_colors_list[1]
        self.row.ids['color3'].background_color = self.super_selected_colors_list[2]
        self.row.ids['color4'].background_color = self.super_selected_colors_list[3]
        self.row.ids['color5'].background_color = self.super_selected_colors_list[4]

        self.output = [(0.6, 0.6, 0.6, 1.0),(0.6, 0.6, 0.6, 1.0),(0.6, 0.6, 0.6, 1.0),(0.6, 0.6, 0.6, 1.0),(0.6, 0.6, 0.6, 1.0)]

        n = 0
        right_pos = 0
        checked = []

        for color in self.super_selected_colors_list:
            if checked.count(color) == 0:
                t = self.game_colors.count(color)
                n += t
                checked.append(color)
        for i in range(len(self.game_colors)):
            if self.super_selected_colors_list[i] == self.game_colors[i]:
                right_pos += 1
        for j in range(n):
            self.output[j] = (1.0, 1.0, 1.0, 1.0)
        for k in range(right_pos):
            self.output[k] = (0.0, 0.0, 0.0, 1.0)

        checker = SuperProposedColors()
        self.ids.check_list.add_widget(
            checker
        )
        checker.ids['color1'].background_color = self.output[0]
        checker.ids['color1'].size = (20,20)
        checker.ids['color2'].background_color = self.output[1]
        checker.ids['color2'].size = (20,20)
        checker.ids['color3'].background_color = self.output[2]
        checker.ids['color3'].size = (20,20)
        checker.ids['color4'].background_color = self.output[3]
        checker.ids['color4'].size = (20,20)
        checker.ids['color5'].background_color = self.output[4]
        checker.ids['color5'].size = (20,20)

        self.tries += 1

        if self.super_selected_colors_list == self.game_colors:
            if self.best_score == "":
                self.best_score = 12
            if self.tries < int(self.best_score):
                self.best_score = 10 - self.tries
                self.best_name = self.user
                self.save_score()
            self.show_alert_dialog('                    You won! Congratulations!!\n                    Play again??')

        if self.tries == 12:
            self.show_alert_dialog('                     Game Over!!    Play again??')


    def play_again(self, e):
        self.ids.list_content.clear_widgets()
        self.ids.check_list.clear_widgets()
        self.defaults()
        self.dialog.dismiss()
        self.dialog = None

    def save_score(self):
        data = {self.user: self.best_score}
        scores['super'] = data
        if os.path.isfile('prev_details.json'):
            with open('prev_details.json', 'w') as file:
                json.dump(scores, file)
                # file.write(self.user+"|"+str(self.best_score))


    def logout(self, e):
        login_app.root.current = "Login"
        if self.dialog != None:
            self.dialog.dismiss()
            self.dialog = None
        self.ids.list_content.clear_widgets()
        self.ids.check_list.clear_widgets()

    def show_alert_dialog(self, txt):
        if not self.dialog:
            self.dialog = MDDialog(
                title="",
                text=txt,
                buttons=[
                    MDFlatButton(
                        text="NO", text_color=login_app.theme_cls.primary_color, on_release=self.logout
                    ),
                    MDFlatButton(
                        text="OK", text_color=login_app.theme_cls.primary_color, on_release=self.play_again
                    ),
                ],
            )
            self.dialog.set_normal_height()
            self.dialog.open()



class WindowManager(ScreenManager):
    pass


def warning(title, msg):
    pop = Popup(title=title, content=MDLabel(text=msg, halign='center', theme_text_color="Custom",
                                             text_color=(1, 1, 1, 1)),
                size_hint=(None, None), size=(300, 200))
    pop.open()



class MainApp(MDApp):
    dialog = None
    confirm = False
    the_class = None
    Window.size = (500, 800)
    Window.maximum_width, Window.maximum_height = Window.size


    initial_center = None
    def build(self):
        Window.left = (GetSystemMetrics(0) - Window.size[0])/2
        Window.top = (GetSystemMetrics(1) - Window.size[1])/2
        # return Builder.load_file("main.kv")
        self.theme_cls.primary_palette = 'Brown'
        self.theme_cls.accent_palette = 'Blue'
        self.theme_cls.theme_style = 'Dark'


if os.path.isfile('prev_details.json'):
    with open('prev_details.json') as json_file:
        try:
            data = json.load(json_file)
            data_normal = data['normal']
            data_super = data['super']

            best_name_normal = list(data_normal.keys())[0]
            best_score_normal = list(data_normal.values())[0]

            best_name_super = list(data_super.keys())[0]
            best_score_super = list(data_super.values())[0]

            scores = {'normal': {best_name_normal:best_score_normal}, 'super':{best_name_super:best_score_super}}
        except:
            scores = {'normal': "", 'super': ""}


if __name__ == '__main__':
    login_app = MainApp()
    login_app.run()
