import sys
import os
import tempfile
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QScrollArea, QFrame, QMessageBox, QFileDialog,
                             QGridLayout, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette

from reportlab.platypus import SimpleDocTemplate, PageBreak
from reportlab.lib.pagesizes import landscape, A4
from SRC.ViewLayer.Logic.TimeTable import map_courses_to_slots, DAYS, HOURS
from SRC.ViewLayer.Layout.Timetable_qt5 import TimetableGridWidget
from SRC.ViewLayer.Logic.Pdf_Exporter import generate_pdf_from_data
from SRC.ViewLayer.Theme.modern_ui_qt5 import ModernUIQt5
from pathlib import Path
class TimetablesPageQt5(QMainWindow):
    def __init__(self, controller, go_back_callback=None):
        super().__init__()
        self.controller = controller
        self.go_back_callback = go_back_callback
        self.options = controller.get_all_options("Data/courses.txt", "Data/selected_courses.txt")
        self.current_index = 0
        #self.apply_stylesheet()
        self.init_ui()
        self.update_view()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Timetables")
        self.setGeometry(100, 100, 1400, 800)
        
        # Apply similar styling as the main page
        
        self.setStyleSheet(ModernUIQt5.get_timetable_stylesheet())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(20)
        
        # Create navigation bar
        self.create_nav_bar(main_layout)
        
        # Create timetable container
        self.create_timetable_container(main_layout)
    def apply_stylesheet(self):
        # __file__ is the path to this Python file (LandPageView.py)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        qss_path = Path(__file__).resolve().parent.parent / "Theme" / "styles.qss"

        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as file:
                self.setStyleSheet(file.read())
        else:
            print(f"Warning: QSS file not found at {qss_path}")
    def create_nav_bar(self, parent_layout):
        """Create the navigation bar with prev/next buttons and title"""
        nav_frame = QFrame()
        nav_frame.setObjectName("navFrame")
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)
        nav_layout.setContentsMargins(10, 10, 10, 10)
        
        # Back button (to return to course selection)
        self.back_button = QPushButton("← Back to Course Selection")
        self.back_button.setObjectName("backButton")
        self.back_button.setFixedSize(200, 40)
        self.back_button.clicked.connect(self.go_back)
        nav_layout.addWidget(self.back_button)
        
        # Add stretch
        nav_layout.addStretch()
        
        # Previous button
        self.prev_button = QPushButton("◄ Previous")
        self.prev_button.setObjectName("navButton")
        self.prev_button.setFixedSize(100, 40)
        self.prev_button.clicked.connect(self.show_prev)
        nav_layout.addWidget(self.prev_button)
        
        # Title label
        self.title_label = QLabel("")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setMinimumWidth(250)
        nav_layout.addWidget(self.title_label)
        
        # Next button
        self.next_button = QPushButton("Next ►")
        self.next_button.setObjectName("navButton")
        self.next_button.setFixedSize(100, 40)
        self.next_button.clicked.connect(self.show_next)
        nav_layout.addWidget(self.next_button)
        
        # Add stretch
        nav_layout.addStretch()
        
        # Export button
        self.export_button = QPushButton("📄 Export PDF")
        self.export_button.setObjectName("exportButton")
        self.export_button.setFixedSize(120, 40)
        self.export_button.clicked.connect(self.export_pdf_dialog)
        nav_layout.addWidget(self.export_button)
        
        nav_frame.setLayout(nav_layout)
        parent_layout.addWidget(nav_frame)
    
    def create_timetable_container(self, parent_layout):
        """Create a scrollable container for the timetable"""
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setObjectName("scrollArea")
        
        # Create timetable widget
        self.timetable_widget = QWidget()
        self.timetable_widget.setObjectName("timetableWidget")
        self.timetable_layout = QVBoxLayout()
        self.timetable_layout.setContentsMargins(20, 20, 20, 20)
        self.timetable_widget.setLayout(self.timetable_layout)
        
        # Set the widget for scroll area
        self.scroll_area.setWidget(self.timetable_widget)
        parent_layout.addWidget(self.scroll_area)
        
        # No data label (initially hidden)
        self.no_data_label = QLabel("No timetable options available.\nPlease go back and select courses.")
        self.no_data_label.setObjectName("noDataLabel")
        self.no_data_label.setAlignment(Qt.AlignCenter)
        self.no_data_label.hide()
        parent_layout.addWidget(self.no_data_label)
    
    def update_view(self):
        """Update the view to display the current timetable option"""
        if not self.options:
            # Hide timetable components and show no data message
            self.prev_button.hide()
            self.next_button.hide()
            self.title_label.hide()
            self.export_button.hide()
            self.scroll_area.hide()
            self.no_data_label.show()
            return
        
        # Show components and hide no data message
        self.prev_button.show()
        self.next_button.show()
        self.title_label.show()
        self.export_button.show()
        self.scroll_area.show()
        self.no_data_label.hide()
        
        # Update title
        self.title_label.setText(f"Timetable Option {self.current_index + 1} of {len(self.options)}")
        
        # Get current timetable
        current_timetable = self.options[self.current_index]
        
        # Map courses to slots
        slot_map = map_courses_to_slots(current_timetable)
        
        # Clear previous content
        for i in reversed(range(self.timetable_layout.count())):
            child = self.timetable_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Create and add new timetable grid
        timetable_grid = TimetableGridWidget(slot_map)
        self.timetable_layout.addWidget(timetable_grid)
        self.timetable_layout.addStretch()
        
        # Reset scroll position
        self.scroll_area.verticalScrollBar().setValue(0)
        
        # Update button states
        self.update_button_states()
    
    def update_button_states(self):
        """Update the enabled/disabled state of navigation buttons"""
        # Previous button
        if self.current_index > 0:
            self.prev_button.setEnabled(True)
            self.prev_button.setProperty("disabled", False)
        else:
            self.prev_button.setEnabled(False)
            self.prev_button.setProperty("disabled", True)
        
        # Next button
        if self.current_index < len(self.options) - 1:
            self.next_button.setEnabled(True)
            self.next_button.setProperty("disabled", False)
        else:
            self.next_button.setEnabled(False)
            self.next_button.setProperty("disabled", True)
        
        # Force style update
        self.prev_button.style().unpolish(self.prev_button)
        self.prev_button.style().polish(self.prev_button)
        self.next_button.style().unpolish(self.next_button)
        self.next_button.style().polish(self.next_button)
    
    def show_prev(self):
        """Show the previous timetable option"""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_view()
    
    def show_next(self):
        """Show the next timetable option"""
        if self.current_index < len(self.options) - 1:
            self.current_index += 1
            self.update_view()
    
    def go_back(self):
        """Return to the course selection page"""
        if self.go_back_callback:
            self.go_back_callback()
        else:
            self.close()
    
    def export_pdf_dialog(self):
        """Handle PDF export dialog"""
        if not self.options:
            QMessageBox.warning(self, "No Data", "No timetable options to export.")
            return
            
        reply = QMessageBox.question(
            self, 'Export PDF', 
            'Do you want to export all timetable options?\n\n'
            'Yes: Export all options\n'
            'No: Export current option only',
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Cancel:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save PDF', 'timetables.pdf', 'PDF files (*.pdf)'
        )
        
        if not file_path:
            return
        
        try:
            if reply == QMessageBox.Yes:
                # Export all timetable options
                doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
                all_elements = []
                
                for idx, timetable in enumerate(self.options):
                    slot_map = map_courses_to_slots(timetable)
                    title = f"Option {idx + 1}"
                    elements = generate_pdf_from_data(None, slot_map, title, return_elements=True)
                    all_elements.extend(elements)
                    if idx < len(self.options) - 1:  # Don't add page break after last option
                        all_elements.append(PageBreak())
                
                doc.build(all_elements)
                
                QMessageBox.information(
                    self, "Export Complete", 
                    f"Successfully exported {len(self.options)} timetable options to:\n{file_path}"
                )
            else:
                # Export only current timetable
                current_timetable = self.options[self.current_index]
                slot_map = map_courses_to_slots(current_timetable)
                title = f"Option {self.current_index + 1}"
                generate_pdf_from_data(file_path, slot_map, title)
                
                QMessageBox.information(
                    self, "Export Complete", 
                    f"Successfully exported current timetable to:\n{file_path}"
                )
            
            # Open the file when done (cross-platform)
            if sys.platform.startswith('win'):
                os.startfile(file_path)
            elif sys.platform.startswith('darwin'):  # macOS
                os.system(f'open "{file_path}"')
            else:  # Linux
                os.system(f'xdg-open "{file_path}"')
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export PDF:\n{str(e)}")
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.go_back_callback:
            # If we have a callback, use it instead of closing
            self.go_back_callback()
            event.ignore()
        else:
            # Standard close behavior
            reply = QMessageBox.question(
                self, 'Exit', 'Are you sure you want to exit?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if hasattr(self.controller, 'handle_exit'):
                    self.controller.handle_exit()
                event.accept()
            else:
                event.ignore()