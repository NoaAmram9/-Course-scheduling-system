# SRC/ViewLayer/Layout/TimetablesUIComponents.py

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar, QLineEdit, QStackedLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import QSize
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5
from SRC.ViewLayer.Layout.PreferencesDropDown import PreferencesDropdown
import os

class TimetableUIComponents:
    # # Signal: emits index (str) when user presses Enter
    # indexEntered = pyqtSignal(str)

    # def __init__(self):
    #     super().__init__()

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

        # Export + Jump Buttons Group (all in the same row)
        export_jump_group = QHBoxLayout()

        # Export button
        instance.export_button = QPushButton("📄 Export PDF")
        instance.export_button.setObjectName("exportButton")
        instance.export_button.setFixedSize(120, 40)
        instance.export_button.clicked.connect(instance.export_pdf_dialog)
        export_jump_group.addWidget(instance.export_button)
        
        # Preferences row - second line
        preferences_jump_row = QHBoxLayout()
        
        # Preferences Dropdown
        instance.preferences_dropdown = PreferencesDropdown(instance.apply_display_sort)
        preferences_jump_row.addWidget(instance.preferences_dropdown)
        
        preferences_jump_row.addStretch()
        
        # # metrics label
        # instance.metrics_label = QLabel("metrics")
        # instance.metrics_label.setObjectName("metrics")
        # instance.metrics_label.setAlignment(Qt.AlignCenter)
        # instance.metrics_label.setMinimumWidth(300)
        # preferences_jump_row.addWidget(instance.metrics_label)
        
        # preferences_jump_row.addStretch()

        metrics_grid = QHBoxLayout()
        # Metrics Grid - for displaying metrics
        instance.metrics_grid = QFrame()
        instance.metrics_grid.setObjectName("metricsGrid")
        instance.metrics_grid.setLayout(metrics_grid)
        instance.metrics_grid.setFixedHeight(40)
        instance.metrics_grid.setContentsMargins(0, 0, 0, 0)
        
        preferences_jump_row.addWidget(instance.metrics_grid)
        
        # metrics label
        instance.metrics_label = QLabel("metrics")
        instance.metrics_label.setObjectName("metrics")
        instance.metrics_label.setAlignment(Qt.AlignCenter)
        instance.metrics_label.setMinimumWidth(300)
        metrics_grid.addWidget(instance.metrics_label)
        
        preferences_jump_row.addStretch()
        
        # # Add a refresh button
        # instance.refresh_button = QPushButton("🔄 Refresh")
        # instance.refresh_button.setObjectName("refreshButton")
        # instance.refresh_button.setFixedSize(120, 40)
        # instance.refresh_button.clicked.connect(instance.refresh_timetables)
        # preferences_jump_row.addWidget(instance.refresh_button)
        # preferences_jump_row.addStretch()
        
        # instance.refresh_button = QPushButton()
        # instance.refresh_button.setObjectName("refreshButton")
        # instance.refresh_label = QLabel("🔄 Refresh")
        # instance.refresh_label.setText("🔄 Refresh")
        # instance.refresh_movie = QMovie("../../../Data/refresh_icon.gif")
        # instance.refresh_label.setMovie(instance.refresh_movie)
        # instance.refresh_button.setFixedSize(120, 40)
        # # instance.refresh_button.setLayout(QVBoxLayout())
        # # instance.refresh_button.layout().addWidget(instance.refresh_label)
        
        # preferences_jump_row.addWidget(instance.refresh_button)
        # preferences_jump_row.addStretch()
        
        # # --- Refresh Button with GIF ---
        
        # # Create a layout inside the button
        # refresh_button_layout = QVBoxLayout()
        # refresh_button_layout.setContentsMargins(0, 0, 0, 0)
        # refresh_button_layout.setAlignment(Qt.AlignCenter)

        # # Create a QLabel with the animated gif
        # instance.refresh_label = QLabel()
        # instance.refresh_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Align to the right and center vertically
        # instance.refresh_label.setLayout(refresh_button_layout)  # Set the layout for the label
        
        # # Load the GIF safely using relative path
        # current_dir = os.path.dirname(__file__)
        # gif_path = os.path.normpath(os.path.join(current_dir, "../../../Data/refresh_right.gif"))
        # print(f"[DEBUG] Loading GIF from: {gif_path}")  # Debugging line to check path
        # instance.refresh_movie = QMovie(gif_path)
        # instance.refresh_movie.setScaledSize(QSize(20, 20))
        # instance.refresh_label.setMovie(instance.refresh_movie)
        # instance.refresh_movie.start()  # Hide the movie animation
        # # instance.refresh_label.setText("🔄 Refresh")  

        # # instance.refresh_movie.setLayout(refresh_button_layout)  # Set the layout for the label


        # # Create the button and set layout
        # instance.refresh_button = QPushButton()
        # instance.refresh_button.setObjectName("refreshButton")
        # instance.refresh_button.setFixedSize(120, 40)
        # instance.refresh_button.setLayout(refresh_button_layout)
        # refresh_button_layout.addWidget(instance.refresh_label)

        # # Connect the button to the refresh function
        # instance.refresh_button.clicked.connect(instance.refresh_timetables)
        
        # # # Add to layout
        # preferences_jump_row.addWidget(instance.refresh_button)
        # preferences_jump_row.addStretch()

        # Create the refresh button with icons
        current_dir = os.path.dirname(__file__)
        instance.refresh_icons = [
            QPixmap(os.path.normpath(os.path.join(current_dir, "../../../Data/refresh_down.gif"))),
            QPixmap(os.path.normpath(os.path.join(current_dir, "../../../Data/refresh_left.gif"))),
            QPixmap(os.path.normpath(os.path.join(current_dir, "../../../Data/refresh_up.gif"))),
            QPixmap(os.path.normpath(os.path.join(current_dir, "../../../Data/refresh_right.gif"))),
        ]

        # ברירת מחדל: האייקון הימני
        instance.default_refresh_icon = instance.refresh_icons[-1]  # refresh_right

        # לייבל בתוך הכפתור
        instance.refresh_label = QLabel()
        instance.refresh_label.setPixmap(instance.default_refresh_icon.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        instance.refresh_label.setAlignment(Qt.AlignCenter)

        # הכפתור עצמו
        instance.refresh_button = QPushButton()
        instance.refresh_button.setObjectName("refreshButton")
        instance.refresh_button.setFixedSize(40, 40)

        # עיצוב הכפתור
        refresh_button_layout = QVBoxLayout()
        refresh_button_layout.setContentsMargins(0, 0, 0, 0)
        refresh_button_layout.setAlignment(Qt.AlignCenter)
        refresh_button_layout.addWidget(instance.refresh_label)
        instance.refresh_button.setLayout(refresh_button_layout)

        # התחברות לפונקציית ריענון
        instance.refresh_button.clicked.connect(instance.refresh_timetables)

        preferences_jump_row.addWidget(instance.refresh_button)

        
        
        # # --- Refresh Button with Text+GIF switching ---

        # # Create the button
        # instance.refresh_button = QPushButton()
        # instance.refresh_button.setObjectName("refreshButton")
        # instance.refresh_button.setFixedSize(120, 40)

        # # Create two QLabel widgets: one for text and one for GIF
        # instance.refresh_text_label = QLabel("🔄 Refresh")
        # instance.refresh_text_label.setAlignment(Qt.AlignCenter)

        # instance.refresh_gif_label = QLabel()
        # instance.refresh_gif_label.setAlignment(Qt.AlignCenter)

        # # Load the movie (GIF)
        # current_dir = os.path.dirname(__file__)
        # gif_path = os.path.normpath(os.path.join(current_dir, "../../../Data/refresh_icon.gif"))
        # instance.refresh_movie = QMovie(gif_path)
        # instance.refresh_movie.setScaledSize(QSize(20, 20))  # Adjust size as needed
        
        # instance.refresh_movie.setCacheMode(QMovie.CacheAll)
        # instance.refresh_movie.setSpeed(100)  # 100% מהירות
        # instance.refresh_movie.setScaledSize(QSize(20, 20))
        
        # instance.refresh_gif_label.setMovie(instance.refresh_movie)


        # # Create a stacked layout to switch between text and gif
        # refresh_button_layout = QStackedLayout()
        # refresh_button_layout.setContentsMargins(0, 0, 0, 0)
        # refresh_button_layout.addWidget(instance.refresh_text_label)  # index 0
        # refresh_button_layout.addWidget(instance.refresh_gif_label)   # index 1

        # # Set the layout to the button
        # instance.refresh_button.setLayout(refresh_button_layout)
        # instance.refresh_button_layout = refresh_button_layout  # Save reference for switching

        # # Connect to refresh function
        # instance.refresh_button.clicked.connect(instance.refresh_timetables)

        # # Add to layout
        # preferences_jump_row.addWidget(instance.refresh_button)
        # preferences_jump_row.addStretch()


        #     # צור את הכפתור וה־QMovie
        # instance.refresh_button = QPushButton()
        # instance.refresh_button.setFixedSize(120, 40)
        # instance.refresh_button.setObjectName("refreshButton")

        # # צור QLabel שישמש כתמונה של הכפתור
        # instance.refresh_label = QLabel()
        
        # # Load the GIF safely using relative path
        # current_dir = os.path.dirname(__file__)
        # gif_path = os.path.normpath(os.path.join(current_dir, "../../../Data/refresh_icon.gif"))
        # print(f"[DEBUG] Loading GIF from: {gif_path}")  # Debugging line to check path
        # instance.refresh_movie = QMovie(gif_path)
        
        # # instance.refresh_movie = QMovie("נתיב_מדויק/refresh_icon.gif")
        # instance.refresh_movie.setScaledSize(QSize(24, 24))  # אפשר לשנות ל־40,40 אם את רוצה את כל הכפתור כתמונה
        # instance.refresh_label.setMovie(instance.refresh_movie)

        # # יצירת טקסט לצד ה־GIF
        # instance.refresh_text = QLabel("Refresh")

        # # סדר את הכל בלייאאוט פנימי
        # refresh_layout = QHBoxLayout()
        # refresh_layout.setContentsMargins(0, 0, 0, 0)
        # refresh_layout.addWidget(instance.refresh_label)
        # refresh_layout.addWidget(instance.refresh_text)

        # # שים את הלייאאוט בכפתור
        # instance.refresh_button.setLayout(refresh_layout)       
        
        # # # Add to layout
        # preferences_jump_row.addWidget(instance.refresh_button)
        # # preferences_jump_row.addStretch()

        
        # Jump Label
        jump_label = QLabel("Jump to:")
        jump_label.setObjectName("jumpLabel")
        jump_label.setFixedHeight(40)
        preferences_jump_row.addWidget(jump_label)

        # Jump First
        instance.jump_first_button = QPushButton("First")
        instance.jump_first_button.setObjectName("jumpButton")
        instance.jump_first_button.setFixedSize(70, 30)
        instance.jump_first_button.clicked.connect(instance.jump_to_first)
        preferences_jump_row.addWidget(instance.jump_first_button)

        # Jump to Index (QLineEdit)
        instance.jump_index_input = QLineEdit()
        instance.jump_index_input.setObjectName("jumpInput")
        instance.jump_index_input.setPlaceholderText("Index")
        instance.jump_index_input.setAlignment(Qt.AlignCenter)
        instance.jump_index_input.setFixedSize(60, 35)
        preferences_jump_row.addWidget(instance.jump_index_input)
        
        # Connect Enter key press in input to emit signal
        instance.jump_index_input.returnPressed.connect(
            lambda: instance.on_index_entered(instance.jump_index_input.text())
        )

        # Jump Last
        instance.jump_last_button = QPushButton("Last")
        instance.jump_last_button.setObjectName("jumpButton")
        instance.jump_last_button.setFixedSize(70, 30)
        instance.jump_last_button.clicked.connect(instance.jump_to_last)
        preferences_jump_row.addWidget(instance.jump_last_button)
        
        top_nav.addLayout(export_jump_group)

        # Final assembly
        nav_layout.addLayout(top_nav)
        nav_frame.setLayout(nav_layout)
        nav_layout.addLayout(preferences_jump_row)
        parent_layout.addWidget(nav_frame)
        
  
    @staticmethod
    def create_status_bar(parent_layout, instance):
        """Create status bar with additional information"""
        status_frame = QFrame()
        status_frame.setObjectName("statusFrame")
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(10, 5, 10, 5)
        status_layout.setSpacing(10)

        # Left label
        instance.status_label = QLabel("Ready")
        instance.status_label.setObjectName("statusLabel")
        status_layout.addWidget(instance.status_label)

        status_layout.addStretch()

        # Logo in the center
        logo_label = QLabel()
        logo_label.setObjectName("logoLabel")
        logo_pixmap = QPixmap("Data/logo.png")  
        logo_pixmap = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(logo_label)

        status_layout.addStretch()

        # Right loading rate
        instance.loading_rate_label = QLabel("")
        instance.loading_rate_label.setObjectName("loadingRateLabel")
        status_layout.addWidget(instance.loading_rate_label)

        status_frame.setLayout(status_layout)
        parent_layout.addWidget(status_frame)

    def emit_index_entered(self):
        value = self.jump_index_input.text()
        self.indexEntered.emit(value)