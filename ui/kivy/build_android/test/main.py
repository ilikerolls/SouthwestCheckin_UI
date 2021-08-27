from kivy.app import App
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget


class MainWindow(Widget):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    confirmation_num = ObjectProperty(None)

    def start_btn(self):
        print("First Name:", self.first_name.text, ", Last Name:", self.last_name.text, ", Confirmation #:",
              self.confirmation_num.text)

    def stop_btn(self):
        print('Stopping process')


class SouthwestMobile(App):
    def build(self):
        Config.set('kivy', 'window_icon', '..\img\SouthwestIcon.jpg')
        self.title = 'Southwest Auto Check IN'
        return MainWindow()


if __name__ == "__main__":
    SouthwestMobile().run()
