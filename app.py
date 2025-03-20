import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)

from app_info import __app_name__





def main():
    
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


