import re

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QApplication
from googletrans import Translator
from PyQt5.QtCore import QRunnable, QThreadPool


class WorkerSignals(QObject):
    # 这些信号只能写在继承自QObject的类型里。注意不能写在__init__里。
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(object)
    callback = pyqtSignal(object)


class TranslationWorker(QRunnable):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        translator = Translator()
        try:
            result = translator.translate(self.text, dest='zh-cn').text
        except Exception as e:
            self.signals.error.emit("An error occurred: " + str(e))  # 发送错误信息
        else:
            self.signals.result.emit(result)  # 发送结果
        finally:
            self.signals.finished.emit()


class RLBMainWindow(QMainWindow):
    def __init__(self, parent: QApplication):
        super().__init__()

        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.app = parent
        self.clipboard = QApplication.clipboard()
        self.setCentralWidget(QWidget())
        self.sourceText = QTextEdit()
        self.sourceText.setAcceptRichText(False)
        self.outputText = QTextEdit()
        self.translatedText = QTextEdit()
        self.infoLabel = QLabel()
        mainLayout = QHBoxLayout()

        mainLayout.addWidget(self.sourceText)
        mainLayout.addLayout(QVBoxLayout())
        mainLayout.itemAt(1).layout().addWidget(self.outputText)
        mainLayout.itemAt(1).layout().addWidget(self.infoLabel)
        mainLayout.addWidget(self.translatedText)
        self.centralWidget().setLayout(mainLayout)

        self.sourceText.textChanged.connect(self.update)

    def update(self):
        text: str = self.sourceText.toPlainText()
        text = re.sub(r"(?<=[a-zA-Z0-9])\n(?=[a-zA-Z0-9])", " ", text)
        new_text = text.replace("\n", "")
        self.outputText.setText(new_text)
        self.clipboard.setText(new_text)
        self.infoLabel.setText("Paste to clipboard!")
        if self.translatedText.toPlainText() == '':
            self.translatedText.setText("Translating...")

        worker = TranslationWorker(new_text)
        worker.signals.result.connect(self.OnTranslationComplete)
        worker.signals.error.connect(self.OnTranslationComplete)
        QThreadPool.globalInstance().start(worker)

    def OnTranslationComplete(self, text):
        self.translatedText.setText(text)
