from PyQt5 import QtWidgets
from lib.ui.PyQtDesignerGenCode.Ui_main_Form import Ui_MainWindow
from lib.ui.SystemTrayIcon import SystemTrayIcon

__author__ = "Marcis Greenwood"
__email__ = "greenwood.marcis@hotmail.com"
__license__ = "GPL"

class CreateUI(Ui_MainWindow, QtWidgets.QMainWindow, QtWidgets.QApplication):
    """
    Creates the Graphical User Interface. Should be a subclass of your generated PyQt5 class .py file from your .ui
    file using pyuic5 and QtWidgets.QMainWindow 1. Design UI in PyQt5 Designer and save .ui file to
    lib/ui/PyQtDesignerGenCode/ 2. Edit GenUICode.bat to match the name of your .ui file and run it. A GUI .py file
    will be generated 3. Change Ui_main_Form to a different class if you changed the name of the generated pyuic5
    file 4. Edit CreateUICustom class to add
    """

    def __init__(self, icon_file, app):
        """
         Initialize attributes and parents objects
        :param icon_file: path to icon file
        :param app QApplication object
        """
        super().__init__()

        # Instance Variables
        self.icon_file = icon_file
        self.app = app

    def setupUi(self):
        """
        Sets up GUI using settings from PyQt5Designer and creates system tray icon
        """
        # Call generated Code UI setup
        super().setupUi(self)
        tray = SystemTrayIcon(self.icon_file, self)
        tray.show()

    def disable_maximize(self):
        """
        Disable Maximize button & set window to fixed size of current Window Size
        """
        self.setFixedSize(self.width(), self.height())
