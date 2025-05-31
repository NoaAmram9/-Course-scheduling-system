from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent
import os
from pathlib import Path
class LandPageView(QWidget):
    file_uploaded = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Schedule System Creator")
        self.setFixedSize(800, 800)
        self.setAcceptDrops(True)
        self.uploaded_path = None

        self.apply_stylesheet()
        self.setup_ui()

    def apply_stylesheet(self):
        # __file__ is the path to this Python file (LandPageView.py)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        qss_path = Path(__file__).resolve().parent.parent / "Theme" / "styles.qss"

        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as file:
                self.setStyleSheet(file.read())
        else:
            print(f"Warning: QSS file not found at {qss_path}")

    def setup_ui(self):
        layout = QVBoxLayout()

        # === HEADER ===
        header = QLabel("WELCOME TO SCHEDUAL SYSTEM CREATOR")
        header.setObjectName("HeaderLabel")

        # === DROP AREA ===
        self.drop_frame = QFrame()
        self.drop_frame.setObjectName("DropFrame")
        self.drop_frame.setFixedSize(400, 200)
        drop_layout = QVBoxLayout(self.drop_frame)

        self.drop_label = QLabel("You can drag a .txt or .xlsx file here\nor upload a file.")
        self.drop_label.setObjectName("DropLabel")
        drop_layout.addWidget(self.drop_label)

        # === UPLOAD BUTTON ===
        self.upload_button = QPushButton("UPLOAD")
        self.upload_button.setObjectName("UploadButton")
        drop_layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)

        # === FILE NAME LABEL ===
        self.file_label = QLabel("")
        self.file_label.setObjectName("FileLabel")

        # === SEND BUTTON ===
        self.send_button = QPushButton("SEND.")
        self.send_button.setObjectName("SendButton")
        send_layout = QHBoxLayout()
        send_layout.addStretch()
        send_layout.addWidget(self.send_button)

        # === FOOTER ===
        footer = QLabel("All rights reserved to the SchedSquad team.")
        footer.setObjectName("FooterLabel")

        layout.addWidget(header)
        layout.addStretch()
        layout.addWidget(self.drop_frame, alignment=Qt.AlignCenter)
        layout.addWidget(self.file_label)
        layout.addStretch()
        layout.addLayout(send_layout)
        layout.addWidget(footer)

        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().endswith((".txt", ".xlsx")):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.endswith((".txt", ".xlsx")):
                self.uploaded_path = path
                self.file_label.setText(f"Uploaded: {os.path.basename(path)}")
                self.file_uploaded.emit(path)
