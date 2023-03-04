import sys
import threading
import subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QCompleter


class PingWidget(QWidget):
    def __init__(self):
        super().__init__()

        # GUI elements
        self.ip_label = QLabel('IP/Domain:')
        self.ip_edit = QLineEdit()
        self.ping_label = QLabel('Ping Results:')
        self.ping_output = QLabel()
        self.start_button = QPushButton('Start')
        self.stop_button = QPushButton('Stop')
        self.stop_button.setEnabled(False)
        self.packet_label = QLabel('Sent Packets:')
        self.packet_count = QLabel('0')

        # IP field
        self.completer_model = QStandardItemModel()
        self.completer = QCompleter(self.completer_model, self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ip_edit.setCompleter(self.completer)

        # GUI layout
        layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        form_layout.addWidget(self.ip_label)
        form_layout.addWidget(self.ip_edit)
        form_layout.addWidget(self.packet_label)
        form_layout.addWidget(self.packet_count)
        layout.addLayout(form_layout)
        layout.addWidget(self.ping_label)
        layout.addWidget(self.ping_output)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_ping)
        self.stop_button.clicked.connect(self.stop_ping)

        self.ping_process = None
        self.packet_sent = 0

        # stylesheet
        self.setStyleSheet("""
            PingWidget {
                background-color: #f5f5f5;
                border-radius: 5px;
                border: 1px solid #e0e0e0;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QLineEdit {
                border: 1px solid #e0e0e0;
                padding: 5px;
            }
            QListView {
                background-color: white;
                border: 1px solid #e0e0e0;
                padding: 5px;
                font-size: 14px;
            }
            QListView::item {
                padding: 2px;
            }
        """)

    def start_ping(self):
        ip = self.ip_edit.text()
        self.ping_process = subprocess.Popen(
            ['ping', '-t', ip], stdout=subprocess.PIPE)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        threading.Thread(target=self.update_ping_output).start()

    def stop_ping(self):
        self.ping_process.kill()
        self.ping_process = None
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.ping_output.setText("")
        
    def update_ping_output(self):
        while self.ping_process is not None:
            try:
                ping_output = self.ping_process.stdout.readline().decode('utf-8')
                if ping_output:
                    self.ping_output.setText(ping_output)
                    self.packet_sent += 1
                    self.packet_count.setText(str(self.packet_sent))
            except:
                print("x")
                pass

    def update_completer(self, ip_list):
        self.completer_model.clear()
        for ip in ip_list:  
            self.completer_model.appendRow(QStandardItem(ip))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.start_ping()
        elif event.key() == Qt.Key_Escape:
            self.stop_ping()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create ping widget & center it
        self.ping_widget = PingWidget()
        self.setCentralWidget(self.ping_widget)

        # Window properties
        self.setWindowTitle('IP & Domain Pinger')
        self.setFixedSize(500, 300)

        # colors
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#f5f5f5'))
        palette.setColor(QPalette.WindowText, QColor('#333333'))
        palette.setColor(QPalette.Base, QColor('#ffffff'))
        palette.setColor(QPalette.AlternateBase, QColor('#f5f5f5'))
        palette.setColor(QPalette.ToolTipBase, QColor('#333333'))
        palette.setColor(QPalette.ToolTipText, QColor('#ffffff'))
        palette.setColor(QPalette.Text, QColor('#333333'))
        palette.setColor(QPalette.Button, QColor('#007bff'))
        palette.setColor(QPalette.ButtonText, QColor('#ffffff'))
        palette.setColor(QPalette.BrightText, QColor('#ffffff'))
        palette.setColor(QPalette.Highlight, QColor('#007bff'))
        palette.setColor(QPalette.HighlightedText, QColor('#ffffff'))
        self.setPalette(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

