from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.config import Config

from checkin import CheckIN
import time


class MainWindow(Widget):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    confirmation_num = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        self.task_running = False

    def start_btn(self):
        print("First Name:", self.first_name.text, ", Last Name:", self.last_name.text, ", Confirmation #:",
              self.confirmation_num.text)


        #check_in = CheckIN(self.config.get('MAIN', 'ConfirmationNum'), self.config.get('MAIN', 'FirstName'),
        #                   self.config.get('MAIN', 'LastName'), False, cli=False)
        check_in = CheckIN(self.confirmation_num.text, self.first_name.text, self.last_name.text, verbose=False, cli=False)
        check_in.auto_checkin()
        while check_in.boarding_msg is None:
            time.sleep(10)

            if not self.task_running:
                check_in.kill_thread()
                while len(check_in.threads) > 0:
                    time.sleep(1)
                return
        print('Finished Start button....')

    def stop_btn(self):
        print('Stopping process')


class SouthwestMobile(App):
    def build(self):
        Config.set('kivy', 'window_icon', '..\img\SouthwestIcon.jpg')
        self.title = 'Southwest Auto Check IN'
        return MainWindow()


if __name__ == "__main__":
    SouthwestMobile().run()
