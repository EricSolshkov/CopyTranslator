from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import QClipboard
from googletrans import Translator
from concurrent.futures import ThreadPoolExecutor


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
        new_text = text.replace("\n", "")
        self.outputText.setText(new_text)
        self.clipboard.setText(new_text)
        self.infoLabel.setText("Paste to clipboard!")

        def T(text):
            translator = Translator()
            return translator.translate(text, dest='zh-cn').text

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(T, new_text)
            try:
                text = future.result()
            except Exception as e:
                text = str(e)
            self.translatedText.setText(text)


