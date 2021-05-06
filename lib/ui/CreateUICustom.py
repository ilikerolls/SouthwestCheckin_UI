from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

from lib.ui.CreateUI import CreateUI
from configparser import ConfigParser
import os
import sys
import time
from checkin import CheckIN

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
        self.worker_thread = {}

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
            self.worker_thread['auto_check_in'] = WorkerThread('auto_check_in', self.config)
            self.worker_thread['auto_check_in'].sig_auto_check_in_finished.connect(self.auto_check_in_finished)
            self.worker_thread['auto_check_in'].start()

            self.setWindowTitle('SouthWest Auto Checkin - Running')
            self.pushButton_start_stop.setText('Stop')
            self.running = True
        else:
            if self.worker_thread['auto_check_in'].isRunning():
                self.worker_thread['auto_check_in'].terminate()

            self.setWindowTitle('SouthWest Auto Checkin - Stopped')
            self.pushButton_start_stop.setText('Start')
            self.running = False

    def auto_check_in_finished(self, msg, error):
        """
        Runs after auto_check_in is finished and sets process as no longer running

        :param error: boolean. False if we failed to check in
        :param msg: String containing your boarding seat
        """

        self.show()
        msg_box = QMessageBox()
        msg_box.setText(msg)

        if not error:
            self.setWindowTitle('SouthWest Auto Checkin - Checked in successfully!')
            msg_box.setWindowTitle('Successfully Checked in!')
            msg_box.setIcon(QMessageBox.Information)
        else:
            self.setWindowTitle('SouthWest Auto Checkin - Stopped')
            msg_box.setWindowTitle('Error')
            msg_box.setText(msg)
            msg_box.setIcon(QMessageBox.Critical)

        msg_box.exec_()

        self.pushButton_start_stop.setText('Start')
        self.running = False

    def exit_button(self):
        """
        Save GUI data and exit application when Exit button pushed
        """
        self.config.save_cur_app_config()
        self.quit()


class WorkerThread(QThread):
    """ Worker Thread for GUI """

    sig_auto_check_in_finished = pyqtSignal(str, bool)

    def __init__(self, task, config=None):
        super(WorkerThread, self).__init__(parent=None)
        self.config = config
        self.task_name = task
        self.task_running = False

    def run(self):
        self.task_running = True
        task_result = getattr(self, self.task_name)()
        self.task_running = False
        return task_result

    def auto_check_in(self):
        """ Automatically Check into Southwest Airlines and display boarding seat when done. To be loaded in seperate
        thread not to freeze the GUI. Then emits message back to method connected to sig_auto_check_in_finished """

        error = False
        try:
            check_in = CheckIN(self.config.get('MAIN', 'ConfirmationNum'), self.config.get('MAIN', 'FirstName'),
                               self.config.get('MAIN', 'LastName'), False, cli=False)
            check_in.auto_checkin()
            while check_in.boarding_msg is None:
                time.sleep(10)

                if not self.task_running:
                    check_in.kill_thread()
                    while len(check_in.threads) > 0:
                        time.sleep(1)
                    return

        except Exception as e:
            error = True
            check_in.boarding_msg = str(e)

        self.sig_auto_check_in_finished.emit(check_in.boarding_msg, error)

    def terminate(self) -> None:
        """
        Terminates a long running thread like hitting the stop button
        """
        self.task_running = False

        if self.task_name not in ['auto_check_in']:
            super().terminate()



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
