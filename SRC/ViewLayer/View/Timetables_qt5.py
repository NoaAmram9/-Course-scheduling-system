# Import standard Python libraries
import sys  
import os   
import tempfile 
from pathlib import Path 

# Import necessary PyQt5 modules for creating the GUI
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QScrollArea, QFrame, QMessageBox, QFileDialog,
                             QGridLayout, QSizePolicy, QProgressBar)
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPalette

# Import modules for PDF generation using reportlab
from reportlab.platypus import SimpleDocTemplate, PageBreak
from reportlab.lib.pagesizes import landscape, A4

# Import custom modules from the application's structure
from SRC.ViewLayer.Logic.TimeTable import map_courses_to_slots, DAYS, HOURS
from SRC.ViewLayer.Layout.Timetable_qt5 import TimetableGridWidget
from SRC.ViewLayer.Logic.Pdf_Exporter import generate_pdf_from_data
from SRC.ViewLayer.Theme.modern_ui_qt5 import ModernUIQt5
from SRC.ViewLayer.View.TimeTableWorker import TimetableWorker


class TimetablesPageQt5(QMainWindow):
    """
    Enhanced TimetablesPageQt5 with sequential display of timetables
    """
    
    # Custom signals
    new_timetable_ready = pyqtSignal()
    
    def __init__(self, controller, go_back_callback=None):
        super().__init__()
        self.controller = controller
        self.go_back_callback = go_back_callback
        
        # Timetable data management
        self.all_options = []  # All loaded timetables
        self.current_index = 0
        self.loading_complete = False
        self.total_expected = 0  # Total number of timetables expected
        
        # Worker thread for background loading
        self.worker = None
        self.is_loading = False
        
        # Auto-display settings
        self.auto_display_enabled = False
        self.display_timer = QTimer()
        self.display_timer.timeout.connect(self.auto_next_timetable)
        self.display_interval = 3000  # 3 seconds between timetables
        
        # Batch loading management
        self.current_batch = []
        self.batch_index = 0
        
        self.init_ui()
        self.start_background_loading()
    
    def init_ui(self):
        """Initialize UI with enhanced controls"""
        self.setWindowTitle("Timetables - Sequential Display")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet(ModernUIQt5.get_timetable_stylesheet())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(20)

        # Create loading indicator with progress
        self.create_enhanced_loading_indicator(main_layout)
        
        # Create navigation bar with auto-display controls
        self.create_enhanced_nav_bar(main_layout)
        
        # Create timetable container
        self.create_timetable_container(main_layout)
        
        # Create status bar
        self.create_status_bar(main_layout)
    
    def create_enhanced_loading_indicator(self, parent_layout):
        """Create enhanced loading progress indicator"""
        self.loading_frame = QFrame()
        self.loading_frame.setObjectName("loadingFrame")
        loading_layout = QVBoxLayout()
        
        # Top row - status and controls
        top_row = QHBoxLayout()
        
        self.loading_label = QLabel("Loading timetables...")
        self.loading_label.setObjectName("loadingLabel")
        
        self.progress_label = QLabel("0 options loaded")
        self.progress_label.setObjectName("progressLabel")
        
        # Loading control buttons
        self.pause_button = QPushButton("⏸ Pause Loading")
        self.pause_button.setObjectName("controlButton")
        self.pause_button.setFixedSize(120, 40)
        self.pause_button.clicked.connect(self.toggle_loading)
        
        self.stop_button = QPushButton("⏹ Stop Loading")
        self.stop_button.setObjectName("controlButton")
        self.stop_button.setFixedSize(120, 40)
        self.stop_button.clicked.connect(self.stop_background_loading)
        
        top_row.addWidget(self.loading_label)
        top_row.addStretch()
        top_row.addWidget(self.progress_label)
        top_row.addWidget(self.pause_button)
        top_row.addWidget(self.stop_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setVisible(False)  # Hidden until we know total count
        
        loading_layout.addLayout(top_row)
        loading_layout.addWidget(self.progress_bar)
        
        self.loading_frame.setLayout(loading_layout)
        parent_layout.addWidget(self.loading_frame)

    def create_enhanced_nav_bar(self, parent_layout):
        """Create enhanced navigation bar with auto-display controls"""
        nav_frame = QFrame()
        nav_frame.setObjectName("navFrame")
        nav_layout = QVBoxLayout()
        nav_layout.setSpacing(10)
        nav_layout.setContentsMargins(10, 10, 10, 10)

        # Top row - main navigation
        top_nav = QHBoxLayout()
        
        # Back button
        self.back_button = QPushButton("← Back to Course Selection")
        self.back_button.setObjectName("backButton")
        self.back_button.setFixedSize(200, 40)
        self.back_button.clicked.connect(self.go_back)
        top_nav.addWidget(self.back_button)

        top_nav.addStretch()

        # Manual navigation buttons
        self.prev_button = QPushButton("◄ Previous") 
        self.prev_button.setObjectName("navButton")
        self.prev_button.setFixedSize(100, 40)
        self.prev_button.clicked.connect(self.show_prev)
        top_nav.addWidget(self.prev_button)

        # Title label
        self.title_label = QLabel("Loading...")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setMinimumWidth(300)
        top_nav.addWidget(self.title_label)

        # Next button
        self.next_button = QPushButton("Next ►")
        self.next_button.setObjectName("navButton")
        self.next_button.setFixedSize(100, 40)
        self.next_button.clicked.connect(self.show_next)
        top_nav.addWidget(self.next_button)

        top_nav.addStretch()

        # Export button
        self.export_button = QPushButton("📄 Export PDF")
        self.export_button.setObjectName("exportButton")
        self.export_button.setFixedSize(120, 40)
        self.export_button.clicked.connect(self.export_pdf_dialog)
        top_nav.addWidget(self.export_button)

        # Bottom row - auto-display controls
        auto_nav = QHBoxLayout()
        
        # Auto display toggle
        self.auto_display_button = QPushButton("▶ Start Auto Display")
        self.auto_display_button.setObjectName("autoButton")
        self.auto_display_button.setFixedSize(150, 35)
        self.auto_display_button.clicked.connect(self.toggle_auto_display)
        auto_nav.addWidget(self.auto_display_button)
        
        # Speed controls
        speed_label = QLabel("Speed:")
        speed_label.setObjectName("speedLabel")
        auto_nav.addWidget(speed_label)
        
        self.speed_slow_button = QPushButton("Slow (5s)")
        self.speed_slow_button.setObjectName("speedButton")
        self.speed_slow_button.setFixedSize(80, 30)
        self.speed_slow_button.clicked.connect(lambda: self.set_display_speed(5000))
        auto_nav.addWidget(self.speed_slow_button)
        
        self.speed_normal_button = QPushButton("Normal (3s)")
        self.speed_normal_button.setObjectName("speedButton")
        self.speed_normal_button.setFixedSize(90, 30)
        self.speed_normal_button.clicked.connect(lambda: self.set_display_speed(3000))
        auto_nav.addWidget(self.speed_normal_button)
        
        self.speed_fast_button = QPushButton("Fast (1s)")
        self.speed_fast_button.setObjectName("speedButton")
        self.speed_fast_button.setFixedSize(80, 30)
        self.speed_fast_button.clicked.connect(lambda: self.set_display_speed(1000))
        auto_nav.addWidget(self.speed_fast_button)
        
        auto_nav.addStretch()
        
        # Jump to controls
        jump_label = QLabel("Jump to:")
        jump_label.setObjectName("jumpLabel")
        auto_nav.addWidget(jump_label)
        
        self.jump_first_button = QPushButton("⏮ First")
        self.jump_first_button.setObjectName("jumpButton")
        self.jump_first_button.setFixedSize(70, 30)
        self.jump_first_button.clicked.connect(self.jump_to_first)
        auto_nav.addWidget(self.jump_first_button)
        
        self.jump_last_button = QPushButton("⏭ Last")
        self.jump_last_button.setObjectName("jumpButton")
        self.jump_last_button.setFixedSize(70, 30)
        self.jump_last_button.clicked.connect(self.jump_to_last)
        auto_nav.addWidget(self.jump_last_button)

        nav_layout.addLayout(top_nav)
        nav_layout.addLayout(auto_nav)
        nav_frame.setLayout(nav_layout)
        parent_layout.addWidget(nav_frame)

    def create_timetable_container(self, parent_layout):
        """Create scrollable timetable container"""
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setObjectName("scrollArea")

        self.timetable_widget = QWidget()
        self.timetable_widget.setObjectName("timetableWidgetContainer")
        self.timetable_layout = QVBoxLayout()
        self.timetable_layout.setContentsMargins(20, 20, 20, 20)
        self.timetable_widget.setLayout(self.timetable_layout)

        self.scroll_area.setWidget(self.timetable_widget)
        parent_layout.addWidget(self.scroll_area)

        # No data label
        self.no_data_label = QLabel("Waiting for timetables to load...")
        self.no_data_label.setObjectName("noDataLabel")
        self.no_data_label.setAlignment(Qt.AlignCenter)
        parent_layout.addWidget(self.no_data_label)
    
    def create_status_bar(self, parent_layout):
        """Create status bar with additional information"""
        status_frame = QFrame()
        status_frame.setObjectName("statusFrame")
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        self.loading_rate_label = QLabel("")
        self.loading_rate_label.setObjectName("loadingRateLabel")
        status_layout.addWidget(self.loading_rate_label)
        
        status_frame.setLayout(status_layout)
        parent_layout.addWidget(status_frame)
    
    def start_background_loading(self):
        """Start the background worker thread"""
        if self.worker is not None:
            self.stop_background_loading()
        
        try:
            self.worker = TimetableWorker(
                self.controller,
                "Data/courses.xlsx", 
                "Data/selected_courses.txt",
                batch_size=50  # Process in batches of 50
            )
            
            # Connect worker signals
            self.worker.new_options_available.connect(self.on_new_batch_loaded)
            self.worker.loading_progress.connect(self.on_loading_progress)
            self.worker.loading_finished.connect(self.on_loading_finished)
            self.worker.error_occurred.connect(self.on_loading_error)
            
            self.worker.start()
            self.is_loading = True
            self.pause_button.setText("⏸ Pause Loading")
            self.status_label.setText("Loading timetables...")
            
            # Initialize loading start time
            import time
            self.loading_start_time = time.time()
            
        except Exception as e:
            self.on_loading_error(f"Failed to start loading: {str(e)}")
    
    def stop_background_loading(self):
        """Stop the background worker thread"""
        if self.worker is not None:
            self.worker.stop()
            self.worker.wait(3000)  # Wait up to 3 seconds
            if self.worker.isRunning():
                self.worker.terminate()
                self.worker.wait(1000)
            self.worker = None
        self.is_loading = False
        self.status_label.setText("Loading stopped")
    
    def toggle_loading(self):
        """Toggle pause/resume of background loading"""
        if self.worker is None:
            return
            
        if self.worker._paused:
            self.worker.resume()
            self.pause_button.setText("⏸ Pause Loading")
            self.status_label.setText("Loading resumed...")
        else:
            self.worker.pause()
            self.pause_button.setText("▶ Resume Loading")
            self.status_label.setText("Loading paused")
    
    def on_new_batch_loaded(self, new_batch):
        """Handle new batch of timetable options loaded by worker"""
        if not new_batch:  # אם הבאצ' ריק, אל תעשה כלום
            return
            
        self.all_options.extend(new_batch)
        
        # If this is the first batch, show the first timetable
        if len(self.all_options) == len(new_batch):
            self.current_index = 0
            self.update_view()
        
        self.update_title()
        self.update_button_states()
        self.status_label.setText(f"Loaded {len(self.all_options)} timetables")
        
        # אם נמצאים במצב auto display ועדיין לא התחלנו, התחל עכשיו
        if self.auto_display_enabled and not self.display_timer.isActive():
            self.display_timer.start(self.display_interval)
            
    def on_loading_progress(self, current, total):
        """Handle loading progress updates"""
        if total > 0:
            self.total_expected = total
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)
            self.progress_bar.setVisible(True)
            self.progress_label.setText(f"{current} of {total} options loaded")
        else:
            # אם אין total ידוע, הסתר את ה-progress bar והראה רק מספר
            self.progress_bar.setVisible(False)
            self.progress_label.setText(f"{current} options loaded")
            
        # Calculate loading rate
        if hasattr(self, 'loading_start_time'):
            import time
            elapsed = time.time() - self.loading_start_time
            if elapsed > 0:
                rate = current / elapsed
                self.loading_rate_label.setText(f"Rate: {rate:.1f} options/sec")
        else:
            import time
            self.loading_start_time = time.time()
    
    def on_loading_finished(self):
        """Handle completion of background loading"""
        self.loading_complete = True
        self.loading_frame.hide()
        self.is_loading = False
        
        if not self.all_options:
            self.no_data_label.setText("No timetable options found.\nPlease go back and select different courses.")
            self.no_data_label.show()
            self.status_label.setText("No timetables found")
        else:
            self.status_label.setText(f"Loading complete - {len(self.all_options)} timetables loaded")
            
            # אם auto display הופעל אבל עדיין לא רץ, התחל עכשיו
            if self.auto_display_enabled and not self.display_timer.isActive():
                self.display_timer.start(self.display_interval)
                
    def on_loading_error(self, error_message):
        """Handle loading errors"""
        QMessageBox.critical(self, "Loading Error", f"Error loading timetables:\n{error_message}")
        self.loading_frame.hide()
        self.status_label.setText("Loading failed")
    
    # Auto-display functionality
    def toggle_auto_display(self):
        """Toggle automatic sequential display of timetables"""
        if not self.all_options and not self.is_loading:
            QMessageBox.information(self, "No Timetables", "No timetables available for auto display.")
            return
        
        if not self.all_options and self.is_loading:
            QMessageBox.information(self, "Loading", "Waiting for timetables to load. Auto display will start automatically.")
            return
        
        if self.auto_display_enabled:
            self.stop_auto_display()
        else:
            self.start_auto_display()
    
    def start_auto_display(self):
        """Start automatic sequential display"""
        self.auto_display_enabled = True
        self.auto_display_button.setText("⏸ Stop Auto Display")
        self.display_timer.start(self.display_interval)
        self.status_label.setText("Auto display started")
        
        # Disable manual navigation during auto display
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)
    
    def stop_auto_display(self):
        """Stop automatic sequential display"""
        self.auto_display_enabled = False
        self.auto_display_button.setText("▶ Start Auto Display")
        self.display_timer.stop()
        self.status_label.setText("Auto display stopped")
        
        # Re-enable manual navigation
        self.update_button_states()
    
    def auto_next_timetable(self):
        """Automatically advance to next timetable"""
        if not self.all_options:
            self.stop_auto_display()
            return
        
        # Move to next timetable, wrap around to beginning if at end
        self.current_index = (self.current_index + 1) % len(self.all_options)
        self.update_view()
        
        # Update status
        self.status_label.setText(f"Auto display: {self.current_index + 1} of {len(self.all_options)}")
    
    def set_display_speed(self, interval_ms):
        """Set the interval for auto display"""
        self.display_interval = interval_ms
        if self.auto_display_enabled:
            self.display_timer.stop()
            self.display_timer.start(self.display_interval)
        
        # Update button styles to show active speed
        for btn in [self.speed_slow_button, self.speed_normal_button, self.speed_fast_button]:
            btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
        # Mark active button
        if interval_ms == 5000:
            self.speed_slow_button.setProperty("active", True)
        elif interval_ms == 3000:
            self.speed_normal_button.setProperty("active", True)
        elif interval_ms == 1000:
            self.speed_fast_button.setProperty("active", True)
    
    def jump_to_first(self):
        """Jump to first timetable"""
        if self.all_options:
            self.current_index = 0
            self.update_view()
    
    def jump_to_last(self):
        """Jump to last loaded timetable"""
        if self.all_options:
            self.current_index = len(self.all_options) - 1
            self.update_view()
    
    def update_view(self):
        """Update the displayed timetable"""
        if not self.all_options:
            self.scroll_area.hide()
            self.no_data_label.show()
            return

        self.scroll_area.show()
        self.no_data_label.hide()
        
        self.update_title()
        
        # Get current timetable
        current_timetable_courses = self.all_options[self.current_index]
        slot_map = map_courses_to_slots(current_timetable_courses)
        
        # Clear previous content
        for i in reversed(range(self.timetable_layout.count())):
            child_widget_item = self.timetable_layout.itemAt(i)
            if child_widget_item:
                widget = child_widget_item.widget()
                if widget:
                    widget.setParent(None)
                    widget.deleteLater()
                else:
                    self.timetable_layout.removeItem(child_widget_item)
        
        # Create new timetable grid
        timetable_grid = TimetableGridWidget(slot_map)
        self.timetable_layout.addWidget(timetable_grid)
        self.timetable_layout.addStretch()
        
        # Reset scroll position
        self.scroll_area.verticalScrollBar().setValue(0)
        self.scroll_area.horizontalScrollBar().setValue(0)
        
        self.update_button_states()
    
    def update_title(self):
        """Update the title label"""
        if self.loading_complete:
            self.title_label.setText(f"Timetable Option {self.current_index + 1} of {len(self.all_options)}")
        else:
            remaining_text = f"+ (Loading...)" if self.is_loading else ""
            self.title_label.setText(f"Timetable Option {self.current_index + 1} of {len(self.all_options)}{remaining_text}")
    
    def update_button_states(self):
        """Update navigation button states"""
        if self.auto_display_enabled:
            # During auto display, disable manual navigation
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return
        
        # Previous button
        can_go_prev = self.current_index > 0
        self.prev_button.setEnabled(can_go_prev)
        self.prev_button.setProperty("disabled", not can_go_prev)
        
        # Next button
        can_go_next = self.current_index < len(self.all_options) - 1
        self.next_button.setEnabled(can_go_next)
        self.next_button.setProperty("disabled", not can_go_next)
        
        # Jump buttons
        has_options = len(self.all_options) > 0
        self.jump_first_button.setEnabled(has_options and self.current_index > 0)
        self.jump_last_button.setEnabled(has_options and self.current_index < len(self.all_options) - 1)
        
        # Force style update
        for button in [self.prev_button, self.next_button, self.jump_first_button, self.jump_last_button]:
            button.style().unpolish(button)
            button.style().polish(button)
    
    def show_prev(self):
        """Show previous timetable"""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_view()
    
    def show_next(self):
        """Show next timetable"""
        if self.current_index < len(self.all_options) - 1:
            self.current_index += 1
            self.update_view()
    
    def go_back(self):
        """Handle back button - stop auto display first"""
        self.stop_auto_display()
        if self.go_back_callback:
            self.go_back_callback()
        else:
            self.close()
    
    def export_pdf_dialog(self):
        """Handle PDF export with all current options"""
        if not self.all_options:
            QMessageBox.warning(self, "No Data", "No timetable options to export.")
            return

        # Ask the user if they want to export all options or only the current one
        reply = QMessageBox.question(
            self, 'Export PDF',
            f'Do you want to export all {len(self.all_options)} loaded timetable options?\n\n'
            'Yes: Export all loaded options\n'
            'No: Export current option only',
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Cancel:
            return

        # Open file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save PDF', 'timetables.pdf', 'PDF files (*.pdf)'
        )

        if not file_path:
            return

        try:
            if reply == QMessageBox.Yes:
                # Export all loaded options
                doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
                all_elements = []

                for idx, timetable_courses in enumerate(self.all_options):
                    slot_map = map_courses_to_slots(timetable_courses)
                    title = f"Timetable Option {idx + 1}"
                    elements = generate_pdf_from_data(None, slot_map, title, return_elements=True)
                    all_elements.extend(elements)

                    if idx < len(self.all_options) - 1:
                        all_elements.append(PageBreak())

                doc.build(all_elements)

                QMessageBox.information(
                    self, "Export Complete",
                    f"Successfully exported {len(self.all_options)} timetable options to:\n{file_path}"
                )
            else:
                # Export current option only
                current_timetable_courses = self.all_options[self.current_index]
                slot_map = map_courses_to_slots(current_timetable_courses)
                title = f"Timetable Option {self.current_index + 1}"
                generate_pdf_from_data(file_path, slot_map, title)

                QMessageBox.information(
                    self, "Export Complete",
                    f"Successfully exported current timetable to:\n{file_path}"
                )

            # Open the generated PDF
            if sys.platform.startswith('win'):
                os.startfile(file_path)
            elif sys.platform.startswith('darwin'):
                os.system(f'open "{file_path}"')
            else:
                os.system(f'xdg-open "{file_path}"')

        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export PDF:\n{str(e)}")

               
                
    def closeEvent(self, event):
        """Handle window close event - stop all background processes"""
        self.stop_auto_display()
        self.stop_background_loading()

        # המתן שה-worker יסתיים לפני סגירה
        if self.worker is not None:
            if self.worker.isRunning(): # בדוק אם ה-worker עדיין רץ
                self.worker.stop()      # בקש ממנו לעצור
                if not self.worker.wait(2000): # המתן עד 2 שניות
                    # אם הוא לא סיים תוך 2 שניות, נסה לסיים בכוח
                    print("Worker did not stop gracefully, attempting to terminate.")
                    self.worker.terminate()
                    self.worker.wait(500) # המתנה קצרה לאחר terminate

        # הצג תמיד שאלת אישור כאשר לוחצים על "X"
        reply = QMessageBox.question(
                self, 'Exit', 'Are you sure you want to exit?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

        if reply == QMessageBox.Yes:
                if hasattr(self.controller, 'handle_exit') and callable(self.controller.handle_exit):
                    self.controller.handle_exit()
                event.accept()
        else:
                self.start_background_loading()  # Restart loading if user cancels
                event.ignore()
                
