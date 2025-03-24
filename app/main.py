import os
import sys
import logging


from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication,
)

from app.src.mainwindow import MainWindow

from app.src.logger import logger, ColoredFormatter, ColoredLogger

def main():
    
    # Set up the logger
    logger.setLevel(getattr(logging, "info".upper()))
    if not logger.hasHandlers():
        # This block ensures that the logger has a handler after class change
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = ColoredFormatter(ColoredLogger.FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Enable scaling for high dpi screens
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_EnableHighDpiScaling, True
    )  # enable highdpi scaling
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_UseHighDpiPixmaps, True
    )  # use highdpi icons
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    
    # create the application
    app = QApplication(sys.argv)
    window = MainWindow(
        app=app,
        config=None,
    )
    window.show()
    window.showMaximized()
    window.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


