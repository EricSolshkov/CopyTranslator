import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from CTMainWindow import CTMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序对象
    main_window = CTMainWindow(app)  # 创建主窗口
    main_window.resize(800, 600)  # 设置窗口大小
    main_window.show()  # 显示窗口
    sys.exit(app.exec_())