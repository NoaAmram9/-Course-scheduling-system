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
from SRC.ViewLayer.Logic.TimetablesSorter import TimetablesSorter
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5
from SRC.ViewLayer.View.TimeTableWorker import TimetableWorker
from SRC.ViewLayer.Layout.TimetablesUIComponents import TimetableUIComponents
from SRC.ViewLayer.Logic.Pdf_Exporter_System import ScreenshotPDFExporter

class TimetablesPageQt5(QMainWindow):
    """
    Main Timetables Page UI class for sequentially displaying timetable options.
    """

    # Signal for when a new timetable is ready to be shown
    new_timetable_ready = pyqtSignal()
    
    def __init__(self, controller, go_back_callback, filePath):
        super().__init__()
        self.controller = controller
        self.go_back_callback = go_back_callback
        self._is_exiting_from_back = False  # Handle back navigation
        self.filePath = filePath
        
        # Timetable data and display management
        self.all_options = []  # All generated timetables
        self.current_index = 0  # Current timetable index being shown
        self.loading_complete = False  # Flag to indicate loading completion
        self.total_expected = 0  # Total number of expected timetables
        self.timetables_sorter = TimetablesSorter()  # Timetable sorting utility
        self.sorted_timetables = []  # Sorted timetable cache
        self.display_sorted = False  # Display sorted flag
        
        # Background worker for loading timetables
        self.worker = None
        self.is_loading = False
        
        # Auto-display settings (e.g. slideshow)
        self.auto_display_enabled = False
        self.display_timer = QTimer()
        self.display_timer.timeout.connect(self.auto_next_timetable)
        self.display_interval = 3000  # 3 seconds per timetable
        
        # Current batch management
        self.current_batch = []
        self.batch_index = 0
        
        self.init_screenshot_exporter()  # Initialize PDF screenshot exporter
        self.init_ui()  # Initialize user interface
        self.start_background_loading()  # Start loading timetables in background

    def init_ui(self):
        """Initialize the main UI layout and components"""
        self.setWindowTitle("Timetables - Sequential Display")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet(ModernUIQt5.get_timetable_stylesheet())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(20)

        # Add enhanced navigation and progress bar controls
        TimetableUIComponents.create_enhanced_nav_bar(main_layout, self) 
        TimetableUIComponents.create_enhanced_loading_indicator(main_layout, self)
        
        # Add timetable scrollable container
        self.create_timetable_container(main_layout)

        # Add status bar at bottom
        TimetableUIComponents.create_status_bar(main_layout, self)
        self.setStyleSheet(ModernUIQt5.get_timetable_stylesheet())

    def create_timetable_container(self, parent_layout):
        """Create the scrollable area to display timetable widgets"""
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

        # Label to show when no timetables are loaded yet
        self.no_data_label = QLabel("Waiting for timetables to load...")
        self.no_data_label.setObjectName("noDataLabel")
        self.no_data_label.setAlignment(Qt.AlignCenter)
        parent_layout.addWidget(self.no_data_label)
        self.setStyleSheet(ModernUIQt5.get_timetable_stylesheet())
        
    def init_screenshot_exporter(self):
        """Initialize the PDF screenshot export system"""
        try:
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
        """Export all displayed timetables as PDF screenshots"""
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
            self.screenshot_exporter.export_pdf_screenshots()
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Export Error", 
                f"Failed to export PDF screenshots:\n{str(e)}"
            )

    ########################
    # Worker thread control
    ########################

    def start_background_loading(self):
        """Start the worker thread to generate timetables in the background"""
        if self.worker is not None:
            self.stop_background_loading()
        
        try:
            self.worker = TimetableWorker(
                self.controller,
                self.filePath,  # Main data file
                "Data/selected_courses.txt",
                batch_size=50  # Load in batches of 50
            )
            
            # Connect signals from the worker to this UI
            self.worker.new_options_available.connect(self.on_new_batch_loaded)
            self.worker.loading_progress.connect(self.on_loading_progress)
            self.worker.loading_finished.connect(self.on_loading_finished)
            self.worker.error_occurred.connect(self.on_loading_error)
            
            self.worker.start()
            self.is_loading = True
            self.pause_button.setText("⏸ Pause Loading")
            self.status_label.setText("Loading timetables...")
            
            # Mark time for loading rate calculation
            import time
            self.loading_start_time = time.time()
            
        except Exception as e:
            self.on_loading_error(f"Failed to start loading: {str(e)}")
    
    def stop_background_loading(self):
        """Stop the background worker if it is running"""
        if self.worker is not None:
            self.worker.stop()
            self.worker.wait(3000)  # Allow 3 seconds to finish
            if self.worker.isRunning():
                self.worker.terminate()
                self.worker.wait(1000)
            self.worker = None
        self.is_loading = False
        self.status_label.setText("Loading stopped")
    
    def toggle_loading(self):
        """Pause or resume the background timetable generation"""
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
        """Handle a new batch of generated timetables from the worker"""
        if not new_batch:
            return
        
        self.all_options.extend(new_batch)

        # If first batch, display the first timetable
        if len(self.all_options) == len(new_batch):
            self.current_index = 0
            self.update_view()
        
        self.update_title()
        self.update_button_states()
        self.status_label.setText(f"Loaded {len(self.all_options)} timetables")

        # If auto-display is enabled, start the display timer
        if self.auto_display_enabled and not self.display_timer.isActive():
            self.display_timer.start(self.display_interval)
            
    def on_loading_progress(self, current, total):
        """Update progress bar and rate of timetable generation"""
        if total > 0:
            self.total_expected = total
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)
            self.progress_bar.setVisible(True)
            self.progress_label.setText(f"{current} of {total} options loaded")
        else:
            self.progress_bar.setVisible(False)
            self.progress_label.setText(f"{current} options loaded")
            
        # Calculate and display loading rate (options per second)
        if hasattr(self, 'loading_start_time'):
            import time
            elapsed = time.time() - self.loading_start_time
            if elapsed > 0.001:
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
            # Show message when no timetables were loaded
            self.no_data_label.setText("No timetable options found.\nPlease go back and select different courses.")
            self.no_data_label.show()
            self.status_label.setText("No timetables found")
        else:
            self.status_label.setText(f"Loading complete - {len(self.all_options)} timetables loaded")
            
            # If auto display was enabled but hasn't started yet, start it now
            if self.auto_display_enabled and not self.display_timer.isActive():
                self.display_timer.start(self.display_interval)
                
    def on_loading_error(self, error_message):
        """Handle loading errors with a popup message"""
        QMessageBox.critical(self, "Loading Error", f"Error loading timetables:\n{error_message}")
        self.loading_frame.hide()
        self.status_label.setText("Loading failed")


    def stop_auto_display(self):
        """Stop automatic timetable display"""
        self.auto_display_enabled = False
        self.auto_display_button.setText("▶ Start Auto Display")
        self.display_timer.stop()
        self.status_label.setText("Auto display stopped")

        # Re-enable manual navigation controls
        self.update_button_states()

    def auto_next_timetable(self):
        """Automatically move to next timetable in sequence"""
        if not self.all_options:
            self.stop_auto_display()
            return
        
        # Cycle to the next timetable; loop to the start if at the end
        self.current_index = (self.current_index + 1) % len(self.all_options)
        self.update_view()
        
        self.status_label.setText(f"Auto display: {self.current_index + 1} of {len(self.all_options)}")


    def jump_to_first(self):
        """Jump to the first timetable in the list"""
        if self.all_options:
            self.current_index = 0
            self.update_view()

    def jump_to_index(self, index):
        """
        Jump to a specific timetable index.
        Handles both sorted and unsorted modes.
        :param index: 1-based index of the timetable
        """
        if 0 < index <= len(self.all_options):
            if self.display_sorted and index > len(self.sorted_timetables):
                self.refresh_timetables()  # Reload if index exceeds sorted list
            self.current_index = index - 1  # Convert to 0-based index
            self.update_view()
        else:
            QMessageBox.warning(self, "Invalid Index", f"   Index {index} is out of range.   ")

    def jump_to_last(self):
        """Jump to the last available timetable"""
        if self.all_options:
            self.jump_to_index(len(self.all_options))  # Use unified index logic

    def update_view(self):
        """Update and render the currently selected timetable"""
        if not self.all_options:
            self.scroll_area.hide()
            self.no_data_label.show()
            return

        self.scroll_area.show()
        self.no_data_label.hide()

        self.update_title()
        self.update_metrics()

        # Get the relevant timetable (sorted or original)
        if self.display_sorted:
            current_timetable_courses = self.sorted_timetables[self.current_index]
        else:
            current_timetable_courses = self.all_options[self.current_index]

        # Convert course data to slot-based map
        slot_map = map_courses_to_slots(current_timetable_courses)

        # Clear previous timetable widgets
        for i in reversed(range(self.timetable_layout.count())):
            child_widget_item = self.timetable_layout.itemAt(i)
            if child_widget_item:
                widget = child_widget_item.widget()
                if widget:
                    widget.setParent(None)
                    widget.deleteLater()
                else:
                    self.timetable_layout.removeItem(child_widget_item)

        # Create and show new timetable grid
        timetable_grid = TimetableGridWidget(slot_map)
        self.timetable_layout.addWidget(timetable_grid)
        self.timetable_layout.addStretch()

        # Reset scrollbars to top/left
        self.scroll_area.verticalScrollBar().setValue(0)
        self.scroll_area.horizontalScrollBar().setValue(0)

        self.update_button_states()

    def update_title(self):
        """Update the timetable title label based on the current index and state"""
        if len(self.all_options) == 0:
            self.title_label.setText("No timetable options available")
        elif self.loading_complete:
            self.title_label.setText(f"Timetable Option {self.current_index + 1} of {len(self.all_options)}")
        else:
            remaining_text = f"+ (Loading...)" if self.is_loading else ""
            self.title_label.setText(f"Timetable Option {self.current_index + 1} of {len(self.all_options)}{remaining_text}")

    def update_metrics(self):
        """Update the metrics display for the current timetable"""
        if self.display_sorted:
            metrics = self.sorted_timetables[self.current_index].metrics
        else:
            metrics = self.all_options[self.current_index].metrics

        self.metrics_label.setText(
            f"active days: {metrics.active_days}, free windows: {metrics.free_windows_number}, "
            f"total free windows: {metrics.free_windows_sum}, "
            f"average start time: {metrics.average_start_time}, average end time: {metrics.average_end_time}"
        )

    def update_button_states(self):
        """Enable/disable navigation buttons based on current state"""
        if self.auto_display_enabled:
            # Disable manual controls during auto display
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return

        can_go_prev = self.current_index > 0
        can_go_next = self.current_index < len(self.all_options) - 1
        has_options = len(self.all_options) > 0

        self.prev_button.setEnabled(can_go_prev)
        self.prev_button.setProperty("disabled", not can_go_prev)

        self.next_button.setEnabled(can_go_next)
        self.next_button.setProperty("disabled", not can_go_next)

        self.jump_first_button.setEnabled(has_options and self.current_index > 0)
        self.jump_last_button.setEnabled(has_options and self.current_index < len(self.all_options) - 1)

        # Refresh button styles to reflect state change
        for button in [self.prev_button, self.next_button, self.jump_first_button, self.jump_last_button]:
            button.style().unpolish(button)
            button.style().polish(button)

    def show_prev(self):
        """Show the previous timetable"""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_view()

    def show_next(self):
        """Show the next timetable"""
        self.jump_to_index(self.current_index + 2)  # Index is 1-based in jump_to_index

    def go_back(self):
        """Handle back button logic; stop auto display and go to previous screen"""
        self.stop_background_loading()
        if self.go_back_callback:
            self.go_back_callback()

    def handle_back(self):
        """Trigger back logic and initiate window close"""
        self._is_exiting_from_back = True
        self.close()  # Will trigger closeEvent

    def closeEvent(self, event):
        """Custom close event handler for X or Back button distinction"""
        if getattr(self, "_is_exiting_from_back", False):
            if self.go_back_callback:
                self.go_back_callback()
            event.accept()
            return

        # Pause the worker, but do not stop it yet
        if self.worker is not None and self.worker.isRunning():
            self.worker.pause()
        
        # self.stop_background_loading()

        # if self.worker is not None and self.worker.isRunning():
        #     self.worker.stop()
        #     if not self.worker.wait(2000):
        #         print("Worker did not stop gracefully, attempting to terminate.")
        #         self.worker.terminate()
        #         self.worker.wait(500)

        reply = QMessageBox.question(
            self, 
            'Exit', 'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No, 
            defaultButton=QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            self.stop_background_loading()
            if hasattr(self.controller, 'handle_exit') and callable(self.controller.handle_exit):
                self.controller.handle_exit()
            event.accept()
        else:
            if self.worker is not None:
                self.worker.resume()
            event.ignore()

    def apply_display_sort(self, key, ascending):
        """Apply sorting to the display based on a metric (key)"""
        if key == "None":
            self.display_sorted = False
        else:
            self.sorted_timetables = self.timetables_sorter.sort_timetables_by_key(self.all_options, key, ascending)
            self.display_sorted = True
        self.update_view()

    def on_index_entered(self, index):
        """Handle user entering an index to jump to a specific timetable"""
        if index == "":
            return
        try:
            int_index = int(index)
            self.jump_to_index(int_index)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", f"   '{index}' is not a valid index.   ")

    def refresh_timetables(self):
        """Re-apply sorting and refresh the display if sorting is active"""
        if not self.display_sorted:
            return

        self.start_refresh_animation()
        key, ascending = self.timetables_sorter.get_current_sort_key(self.sorted_timetables)
        self.apply_display_sort(key, ascending)
        QTimer.singleShot(1000, self.stop_refresh_animation)

    def start_refresh_animation(self):
        """Start icon refresh animation while sorting timetables"""
        self.refresh_animation_index = 0
        self.refresh_animation_timer = QTimer()
        self.refresh_animation_timer.timeout.connect(self.update_refresh_icon)
        self.refresh_animation_timer.start(100)

    def update_refresh_icon(self):
        """Cycle refresh icon frame (animated loading)"""
        icon = self.refresh_icons[self.refresh_animation_index]
        self.refresh_label.setPixmap(icon.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.refresh_animation_index = (self.refresh_animation_index + 1) % len(self.refresh_icons)

    def stop_refresh_animation(self):
        """Stop the refresh animation and reset icon"""
        if hasattr(self, "refresh_animation_timer"):
            self.refresh_animation_timer.stop()
            del self.refresh_animation_timer
        self.refresh_label.setPixmap(self.default_refresh_icon.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
