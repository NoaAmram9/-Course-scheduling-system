# SRC/ViewLayer/Layout/TimetablesUIComponents.py

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar
from PyQt5.QtCore import Qt

class TimetableUIComponents:

    @staticmethod
    def create_enhanced_loading_indicator(parent, instance):
        """Enhanced loading progress indicator"""
        loading_frame = QFrame()
        loading_layout = QVBoxLayout()

        top_row = QHBoxLayout()
        instance.loading_label = QLabel("Loading timetables...")
        instance.progress_label = QLabel("0 options loaded")
        instance.pause_button = QPushButton("⏸ Pause Loading")
        instance.pause_button.clicked.connect(instance.toggle_loading)
        instance.stop_button = QPushButton("⏹ Stop Loading")
        instance.stop_button.clicked.connect(instance.stop_background_loading)

        top_row.addWidget(instance.loading_label)
        top_row.addStretch()
        top_row.addWidget(instance.progress_label)
        top_row.addWidget(instance.pause_button)
        top_row.addWidget(instance.stop_button)

        instance.progress_bar = QProgressBar()
        instance.progress_bar.setVisible(False)

        loading_layout.addLayout(top_row)
        loading_layout.addWidget(instance.progress_bar)

        loading_frame.setLayout(loading_layout)
        instance.loading_frame = loading_frame
        parent.addWidget(loading_frame)

    @staticmethod
    def create_enhanced_nav_bar(parent_layout, instance):
        nav_frame = QFrame()
        nav_frame.setObjectName("navFrame")
        nav_layout = QVBoxLayout()
        nav_layout.setSpacing(10)
        nav_layout.setContentsMargins(10, 10, 10, 10)

        # Top row - main navigation
        top_nav = QHBoxLayout()

        # Back button
        instance.back_button = QPushButton("← Back to Course Selection")
        instance.back_button.setObjectName("backButton")
        instance.back_button.setFixedSize(200, 40)
        instance.back_button.clicked.connect(instance.handle_back)
        top_nav.addWidget(instance.back_button)

        top_nav.addStretch()

        # Manual navigation buttons
        instance.prev_button = QPushButton("◄ Previous")
        instance.prev_button.setObjectName("navButton")
        instance.prev_button.setFixedSize(100, 40)
        instance.prev_button.clicked.connect(instance.show_prev)
        top_nav.addWidget(instance.prev_button)

        # Title label
        instance.title_label = QLabel("Loading...")
        instance.title_label.setObjectName("titleLabel")
        instance.title_label.setAlignment(Qt.AlignCenter)
        instance.title_label.setMinimumWidth(300)
        top_nav.addWidget(instance.title_label)

        # Next button
        instance.next_button = QPushButton("Next ►")
        instance.next_button.setObjectName("navButton")
        instance.next_button.setFixedSize(100, 40)
        instance.next_button.clicked.connect(instance.show_next)
        top_nav.addWidget(instance.next_button)

        top_nav.addStretch()

        # Export button
        instance.export_button = QPushButton("📄 Export PDF")
        instance.export_button.setObjectName("exportButton")
        instance.export_button.setFixedSize(120, 40)
        instance.export_button.clicked.connect(instance.export_pdf_dialog)
        top_nav.addWidget(instance.export_button)

        # Bottom row - auto-display controls
        auto_nav = QHBoxLayout()
        auto_nav.addStretch()

        jump_label = QLabel("Jump to:")
        jump_label.setObjectName("jumpLabel")
        auto_nav.addWidget(jump_label)

        instance.jump_first_button = QPushButton("⏮ First")
        instance.jump_first_button.setObjectName("jumpButton")
        instance.jump_first_button.setFixedSize(70, 30)
        instance.jump_first_button.clicked.connect(instance.jump_to_first)
        auto_nav.addWidget(instance.jump_first_button)

        instance.jump_last_button = QPushButton("⏭ Last")
        instance.jump_last_button.setObjectName("jumpButton")
        instance.jump_last_button.setFixedSize(70, 30)
        instance.jump_last_button.clicked.connect(instance.jump_to_last)
        auto_nav.addWidget(instance.jump_last_button)

        nav_layout.addLayout(top_nav)
        nav_layout.addLayout(auto_nav)
        nav_frame.setLayout(nav_layout)
        parent_layout.addWidget(nav_frame)
    @staticmethod
    def create_status_bar(parent_layout, instance):
        """Create status bar with additional information"""
        status_frame = QFrame()
        status_frame.setObjectName("statusFrame")
        status_layout = QHBoxLayout()

        instance.status_label = QLabel("Ready")
        instance.status_label.setObjectName("statusLabel")
        status_layout.addWidget(instance.status_label)

        status_layout.addStretch()

        instance.loading_rate_label = QLabel("")
        instance.loading_rate_label.setObjectName("loadingRateLabel")
        status_layout.addWidget(instance.loading_rate_label)

        status_frame.setLayout(status_layout)
        parent_layout.addWidget(status_frame)

