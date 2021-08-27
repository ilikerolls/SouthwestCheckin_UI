from PyQt5 import QtGui, QtWidgets

__author__ = "Marcis Greenwood"
__email__ = "greenwood.marcis@hotmail.com"
__license__ = "GPL"


class RightClickMenuIndicator(QtWidgets.QMenu):
    """
    Right Click Menu Class for tray icon
    """

    def __init__(self, parent):
        """
        Initialize params, create and add actions to Right click Tray menu
        :param parent: parent object of the window usually CreateUI
        """
        self.parent = parent
        QtWidgets.QMenu.__init__(self, "File", parent)

        show_hide_action = QtWidgets.QAction("Show/Hide", parent)
        show_hide_action.triggered.connect(self.show_hide_action)
        self.addAction(show_hide_action)

        quit_action = QtWidgets.QAction("Quit", parent)
        quit_action.triggered.connect(parent.quit)
        self.addAction(quit_action)

    def show_hide_action(self):
        """
        Show or Hide Action. Shows Window if it is hidden. Hides it if it isn't hidden
        """
        if self.parent.isVisible():
            self.parent.hide()
        else:
            self.parent.show()


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    Add a system tray icon and menu
    """

    def __init__(self, icon_file, parent):
        """
        Initialize attributes and create system tray with a right click menu
        :param icon_file: icon file path name
        :param parent: parent object of the window usually CreateUI
        """
        self.icon_file = icon_file
        self.parent = parent
        # Init QSystemTrayIcon
        QtWidgets.QSystemTrayIcon.__init__(self, self.parent)
        self.setIcon(QtGui.QIcon(self.icon_file))

        self.right_menu = RightClickMenuIndicator(self.parent)
        self.setContextMenu(self.right_menu)
        self.activated.connect(self.onTrayIconActivated)

        QtWidgets.QSystemTrayIcon.show(self)

        self.setToolTip('SouthWest Auto Check IN App')

    def onTrayIconActivated(self, reason):
        """
        Show window on double Click
        :param reason: the reason the Tray icon was activated ex: QtWidgets.QSystemTrayIcon.DoubleClick
        """
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick and not self.parent.isVisible():
            self.parent.show()

