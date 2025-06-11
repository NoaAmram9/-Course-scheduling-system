# Import standard Python libraries
import sys  
import os   
import tempfile 
from pathlib import Path 

from threading import Timer
import threading

# Import necessary PyQt5 modules for creating the GUI
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QScrollArea, QFrame, QMessageBox, QFileDialog,QApplication,
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
from SRC.ViewLayer.Logic.TimetablesSorter import TimetablesSorter
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5
from SRC.ViewLayer.View.TimeTableWorker import TimetableWorker
from SRC.ViewLayer.Layout.TimetablesUIComponents import TimetableUIComponents
from SRC.ViewLayer.Logic.Pdf_Exporter_System import ScreenshotPDFExporter

class TimetablesPageQt5(QMainWindow):
    """
    Enhanced TimetablesPageQt5 with sequential display of timetables
    """
    
    # Custom signals
    new_timetable_ready = pyqtSignal()
    
    def __init__(self, controller, go_back_callback, filePath):
        super().__init__()
        self.controller = controller
        self.go_back_callback = go_back_callback
        self._is_exiting_from_back = False #התמודדות עם כפתור חזרה אחורה
        self.filePath = filePath
        
        # # Thread-safe timetable management
        # self.display_manager = TimetablesDisplayManager()
        # self.display_manager.set_ui_update_callback(self._on_sorted_data_updated)
        
        # # Legacy support - keep references for existing code
        # self.all_options = []
        # self.current_index = 0
        # self.loading_complete = False
        # self.total_expected = 0
       
        # Timetable data management
        self.all_options = []  # All loaded timetables
        self.current_index = 0
        self.loading_complete = False
        self.total_expected = 0  # Total number of timetables expected
        self.timetables_sorter = TimetablesSorter()  # Instance of the sorter for managing timetable sorting
        self.sorted_timetables = []  # Cache for sorted timetables
        self.display_sorted = False  # Flag to indicate if sorted timetables should be displayed
        
        # Worker thread for background loading
        self.worker = None
        self.is_loading = False
        
        # Auto-display settings
        self.auto_display_enabled = False
        self.display_timer = QTimer()
        self.display_timer.timeout.connect(self.auto_next_timetable)
        self.display_interval = 3000  # 3 seconds between timetables
        
        # # UI update throttling to prevent excessive refreshes
        # self._ui_update_timer = Timer(0.2, self._delayed_ui_update)
        # self._ui_update_pending = False
        # self._ui_update_lock = threading.Lock()
        
        # Batch loading management
        self.current_batch = []
        self.batch_index = 0
       # אתחול מערכת ייצוא Screenshots
        self.init_screenshot_exporter()
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

        
        # nav_bars = TimetableUIComponents()
        
        # # Create loading indicator with progress
        # nav_bars.create_enhanced_nav_bar(main_layout, self)
        
        # nav_bars.indexEntered.connect(self.jump_to_index)
        
        
        # Create loading indicator with progress
        TimetableUIComponents.create_enhanced_nav_bar(main_layout, self) 
        # Create navigation bar with auto-display controls
        TimetableUIComponents.create_enhanced_loading_indicator(main_layout, self)
        
        # Create timetable container
        self.create_timetable_container(main_layout)
    
        
        # Create status bar
        TimetableUIComponents.create_status_bar(main_layout, self)
        self.setStyleSheet(ModernUIQt5.get_timetable_stylesheet())

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
        self.setStyleSheet(ModernUIQt5.get_timetable_stylesheet())
        
    def init_screenshot_exporter(self):
        """אתחול מערכת ייצוא PDF עם Screenshots"""
        try:
            # ייבוא המחלקה
            from SRC.ViewLayer.Logic.Pdf_Exporter_System import ScreenshotPDFExporter
            self.screenshot_exporter = ScreenshotPDFExporter(self)
            print("Screenshot exporter initialized successfully")
        except ImportError as e:
            print(f"Failed to import ScreenshotPDFExporter: {e}")
            self.screenshot_exporter = None
        except Exception as e:
            print(f"Failed to initialize screenshot exporter: {e}")
            self.screenshot_exporter = None

    def export_pdf_screenshots(self):
        """ייצוא PDF עם Screenshots - הפונקציה שהכפתור קורא אליה"""
        if self.screenshot_exporter is None:
            QMessageBox.critical(
                self, 
                "Export Error", 
                "Screenshot exporter is not available.\nPlease check if all required modules are installed."
            )
            return
        
        if not self.all_options:
            QMessageBox.warning(
                self, 
                "No Data", 
                "No timetables available for export.\nPlease wait for timetables to load."
            )
            return
        
        try:
            # קריאה לפונקציית הייצוא
            self.screenshot_exporter.export_pdf_screenshots()
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Export Error", 
                f"Failed to export PDF screenshots:\n{str(e)}"
            )

    
    ############קריאה ל-Worker - מה שמציג את המערכות############
    def start_background_loading(self):
        """Start the background worker thread"""
        if self.worker is not None:
            self.stop_background_loading()
        
        try:
            self.worker = TimetableWorker(
                self.controller,
                self.filePath,  # Pass the Data object to the worker
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
        if not new_batch:  # If no new options, do nothing
            return
        
        self.all_options.extend(new_batch)
        # self.timetables_sorter.add_timetables(new_batch)  # Add new timetables to sorter
        # If this is the first batch, show the first timetable
        if len(self.all_options) == len(new_batch):
            self.current_index = 0
            self.update_view()
        
        self.update_title()
        self.update_button_states()
        self.status_label.setText(f"Loaded {len(self.all_options)} timetables")
        

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
            # If total is unknown, just show current count
            self.progress_bar.setVisible(False)
            self.progress_label.setText(f"{current} options loaded")
            
        # Calculate loading rate
        if hasattr(self, 'loading_start_time'):
            import time
            elapsed = time.time() - self.loading_start_time
            if elapsed > 0.001:  # Avoid division by zero
                rate = current / elapsed
                self.loading_rate_label.setText(f"Rate: {rate:.1f} options/sec")
            else:
                self.loading_rate_label.setText("Rate: calculating...")
        else:
            import time
            self.loading_start_time = time.time()
    
    def on_loading_finished(self):
        """Handle completion of background loading"""
        self.loading_complete = True
        self.loading_frame.hide()
        self.is_loading = False
       
        self.update_title()
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
    

    #####למחוק
    def stop_auto_display(self):
        """Stop automatic sequential display"""
        self.auto_display_enabled = False
        self.auto_display_button.setText("▶ Start Auto Display")
        self.display_timer.stop()
        self.status_label.setText("Auto display stopped")
        
        # Re-enable manual navigation
        self.update_button_states()
    ######למחוק
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
    
 
    
    def jump_to_first(self):
        """Jump to first timetable"""
        if self.all_options:
            self.current_index = 0
            self.update_view()
    
    def jump_to_index(self, index):
        """
        Jump to specific timetable index.
        Handle both sorted and unsorted timetables. 
        param index: 1-based index of the timetable to jump to.
        """
        if 0 < index <= len(self.all_options):
            if self.display_sorted and index > len(self.sorted_timetables):
                self.refresh_timetables()  # Refresh if index is out of bounds for sorted list
            self.current_index = index - 1  # Convert to zero-based index
            self.update_view()
        else:
            QMessageBox.warning(self, "Invalid Index", f"   Index {index} is out of range.   ")
    
    def jump_to_last(self):
        """Jump to last loaded timetable"""
        if self.all_options:
            # self.current_index = len(self.all_options) - 1
            # self.update_view()
            self.jump_to_index(len(self.all_options))  # Use the jump_to_index method with the last index
    
    def update_view(self):
        """Update the displayed timetable"""
        if not self.all_options:
            self.scroll_area.hide()
            self.no_data_label.show()
            return

        self.scroll_area.show()
        self.no_data_label.hide()
        
        self.update_title()
        # self.update_metrics()
        
        # Get current timetable
        if self.display_sorted:
            # If sorted display is enabled, use the sorted list
            current_timetable_courses = self.sorted_timetables[self.current_index]
        else:
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
        if len(self.all_options) == 0:
            self.title_label.setText("No timetable options available")
        elif self.loading_complete:
            self.title_label.setText(f"Timetable Option {self.current_index + 1} of {len(self.all_options)}")
        else:
            remaining_text = f"+ (Loading...)" if self.is_loading else ""
            self.title_label.setText(f"Timetable Option {self.current_index + 1} of {len(self.all_options)}{remaining_text}")
    
    # def update_metrics(self):
    #     if self.display_sorted :
    #         metrics = self.sorted_timetables[self.current_index].metrics
    #     else: 
    #         metrics = self.all_options[self.current_index].metrics
    #     self.metrics_label.setText(f"metrics:  active days: {metrics.active_days}, free windows: {metrics.free_windows_number}," + 
    #                                    f" total free windows: {metrics.free_windows_sum}, " +
    #                                    f" average start time: {metrics.average_start_time}, average end time: {metrics.average_end_time}")
    #     PREFERENCES_OPTIONS = {
    #             "None": "None",
    #             "Active Days": "active_days",
    #             "Free windows": "free_windows_number",
    #             "Total free windows": "free_windows_sum",
    #             "Average Start Time": "average_start_time",
    #             "Average End Time": "average_end_time",
    #         }     
        
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
        # if self.display_sorted:
        #     if self.current_index >= len(self.sorted_timetables) - 1:
        #         self.refresh_timetables()
        #     if self.current_index < len(self.sorted_timetables) - 1:
        #         self.current_index += 1
        #         self.update_view()
        
        # elif self.current_index < len(self.all_options) - 1:
        #     self.current_index += 1
        #     self.update_view()
        
        # Use the jump_to_index method to handle bounds checking + sorting if needed
        self.jump_to_index(self.current_index + 2)  
    
    def go_back(self):
        """Handle back button - stop auto display first"""
    
        self.stop_background_loading()  # עצור טעינה אם יש
        if self.go_back_callback:
            self.go_back_callback()

    def handle_back(self):
        self._is_exiting_from_back = True
        self.close()  # זה יפעיל את closeEvent

    def closeEvent(self, event):
        """Handle window close event - distinguish between Back and X buttons"""

        # אם חזרנו דרך כפתור BACK
        if getattr(self, "_is_exiting_from_back", False):
            if self.go_back_callback:
                self.go_back_callback()
            event.accept()
            return  # לא לבצע שום דבר נוסף

        # אחרת - סוגרים דרך X או סגירה רגילה

        # עצור תהליכי רקע
        self.stop_background_loading()

        # המתן שה-worker יסתיים לפני סגירה
        if self.worker is not None:
            if self.worker.isRunning():
                self.worker.stop()
                if not self.worker.wait(2000):
                    print("Worker did not stop gracefully, attempting to terminate.")
                    self.worker.terminate()
                    self.worker.wait(500)

        # הצג תיבת אישור
        reply = QMessageBox.question(
            self, 'Exit', 'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if hasattr(self.controller, 'handle_exit') and callable(self.controller.handle_exit):
                self.controller.handle_exit()
            event.accept()
        else:
           # self.start_background_loading()
            event.ignore()
    
    def apply_display_sort(self, key, ascending):
        if key == "None":
            self.display_sorted = False
        else:
        # print(f"Applying display sort on timetables by {key} in {'ascending' if ascending else 'descending'} order.")
            self.sorted_timetables = self.timetables_sorter.sort_timetables_by_key(self.all_options, key, ascending)
            self.display_sorted = True
        # sort_timetables(self.all_options, key, ascending)
        self.update_view()

    def on_index_entered(self, index):
        """Emit index entered signal"""
        if index == "":
            return
        try:
            int_index = int(index)
            self.jump_to_index(int_index)

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", f"   '{index}' is not a valid index.   ")

    def refresh_timetables(self) :
        if not self.display_sorted:
            return
        
        self.start_refresh_animation()

        """Refresh the displayed timetables after sorting: re-sort by the current key"""
        key, ascending = self.timetables_sorter.get_current_sort_key(self.sorted_timetables)
        self.apply_display_sort(key, ascending)
        
        # Stop animation after short delay
        QTimer.singleShot(1000, self.stop_refresh_animation)
    
    def start_refresh_animation(self):
        self.refresh_animation_index = 0
        self.refresh_animation_timer = QTimer()
        self.refresh_animation_timer.timeout.connect(self.update_refresh_icon)
        self.refresh_animation_timer.start(100)  # Update every 100 ms

    def update_refresh_icon(self):
        icon = self.refresh_icons[self.refresh_animation_index]
        self.refresh_label.setPixmap(icon.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.refresh_animation_index = (self.refresh_animation_index + 1) % len(self.refresh_icons)

    def stop_refresh_animation(self):
        if hasattr(self, "refresh_animation_timer"):
            self.refresh_animation_timer.stop()
            del self.refresh_animation_timer
        self.refresh_label.setPixmap(self.default_refresh_icon.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        