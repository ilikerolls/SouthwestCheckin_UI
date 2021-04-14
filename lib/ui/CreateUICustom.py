from PyQt5.QtWidgets import QMessageBox

from lib.ui.CreateUI import CreateUI
from configparser import ConfigParser
import os
import sys
import checkin

__author__ = "Marcis Greenwood"
__email__ = "greenwood.marcis@hotmail.com"
__license__ = "GPL"

class CreateUICustom(CreateUI):
    """
    Edit this class to link Custom actions to your widgets(buttons, etc....)
    """

    def __init__(self, icon_file, app):
        super().__init__(icon_file, app)
        self.config = Config(self)
        self.running = False

    def setupUi(self):
        """
        Set up buttons and actions in GUI
        """
        super().setupUi()

        # load previously used settings
        self.config.load_config_file_to_gui()

        # disable the maximize option
        self.disable_maximize()
        # Link up the save button to save configuration
        self.pushButton_exit.clicked.connect(self.exit_button)

        # Start button
        self.pushButton_start_stop.clicked.connect(self.start_stop_button)

    def start_stop_button(self):
        """
        Start button pushed. Activates imdb searcher
        """
        if self.running is False:
            self.config.get_cur_app_config()

            try:
                checkin.auto_checkin(self.config.get('MAIN', 'ConfirmationNum'), self.config.get('MAIN', 'FirstName'), self.config.get('MAIN', 'LastName'), False, cli=False)
            except Exception as e:
                msg_box = QMessageBox()
                msg_box.setWindowTitle('Error')
                msg_box.setText(str(e))
                msg_box.setIcon(QMessageBox.Critical)
                msg_box.exec_()
                return

            self.setWindowTitle('SouthWest Auto Checkin - Running')
            self.pushButton_start_stop.setText('Stop')
            self.running = True
        else:
            self.setWindowTitle('SouthWest Auto Checkin - Stopped')
            self.pushButton_start_stop.setText('Start')
            self.running = False

    def exit_button(self):
        """
        Save GUI data and exit application when Exit button pushed
        """
        self.config.save_cur_app_config()
        self.quit()


class Config(ConfigParser):
    """
    Configuration class for saving and loading settings
    """

    def __init__(self, pyqt_form, config_file='config.ini'):
        """
        Set instance variables
        :param pyqt_form: Should be CreateUI class or the class of a form
        :param config_file: Configuration filename default '/lib/ui/config.ini'
        """
        super().__init__()
        self.pyqt_form = pyqt_form

        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.config_file_name = os.path.join(base_path, config_file)

    def get_cur_app_config(self):
        """
        Gets all the settings from the GUI and puts them in ConfigParser()
        """
        self['MAIN'] = {
            'FirstName': self.pyqt_form.lineEdit_first_name.text(),
            'LastName': self.pyqt_form.lineEdit_last_name.text(),
            'ConfirmationNum': self.pyqt_form.lineEdit_confirmation.text(),
        }

    def save_cur_app_config(self):
        """
        Save settings in GUI to the config file
        """
        self.get_cur_app_config()
        with open(self.config_file_name, 'w') as configfile:
            self.write(configfile)

    def load_config_file_to_gui(self):
        """
        Loads configuration file and updates settings GUI app settings based on previous configuration file
        """
        if os.path.isfile(self.config_file_name):
            self.read_file(open(self.config_file_name))

            # set First Name text box
            self.pyqt_form.lineEdit_first_name.setText(self.get('MAIN', 'FirstName'))
            # set Last Name text box
            self.pyqt_form.lineEdit_last_name.setText(self.get('MAIN', 'LastName'))
            # Set confirmation #
            self.pyqt_form.lineEdit_confirmation.setText(self.get('MAIN', 'ConfirmationNum'))
