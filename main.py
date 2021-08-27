from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

screen_helper = """
ScreenManager:
    MainScreen:
        name: 'main'
        
<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [0,dp(50),dp(20),0]
        
        GridLayout:
            cols: 2
            Label:
                text: "First Name: "
                size_hint_y: None
                height: dp(25)
            TextInput:
                id: first_name
                multiline: False
                size_hint_y: None
                height: dp(25)
                
        GridLayout:
            cols: 2
            Label:
                text: "Last Name: "
                halign: 'center'
                size_hint_y: None
                height: dp(25)
            TextInput:
                id: last_name
                multiline: False
                size_hint_y: None
                height: dp(25)

        GridLayout:
            cols: 2
            Label:
                text: "Confirmation #: "
                halign: 'center'
                size_hint_y: None
                height: dp(25)
            TextInput:
                id: confirmation_num
                multiline: False
                size_hint_y: None
                height: dp(25)

        GridLayout:
            cols: 2
            spacing: 0.08*root.width
            padding: [dp(20),0,0,0]
            Button:
                id: start_button
                text: "Start"
                size_hint_y: None
                height: dp(25)
            Button:
                id: stop_button
                text: "Stop"
                size_hint_y: None
                height: dp(25)
"""

class MainScreen(Screen):
    pass

class SouthwestMobileApp(App):
    def build(self):
        self.title = 'Southwest Auto Check IN'

        # Not available in regular kivy?
        #self.theme_cls.theme_style = "Dark"
        screen = Builder.load_string(screen_helper)
        return screen


if __name__ == "__main__":
    # Create the screen manager
    sm = ScreenManager()
    sm.add_widget(MainScreen(name='main'))
    SouthwestMobileApp().run()
