# Import standard Python libraries
import sys  # For system-specific parameters and functions, like sys.platform
import os   # For interacting with the operating system, like file paths and starting files
import tempfile # For creating temporary files and directories (though not explicitly used in this snippet, often useful)
from pathlib import Path # For object-oriented filesystem paths, making path manipulation easier and more robust

# Import necessary PyQt5 modules for creating the GUI
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QScrollArea, QFrame, QMessageBox, QFileDialog,
                             QGridLayout, QSizePolicy) # QGridLayout and QSizePolicy were not used directly in the snippet but are common
from PyQt5.QtCore import Qt, QSize # Qt for alignment, policies, etc. QSize for defining sizes.
from PyQt5.QtGui import QFont, QPalette # QFont for text styling, QPalette for widget colors (though styling is mainly via QSS)

# Import modules for PDF generation using reportlab
from reportlab.platypus import SimpleDocTemplate, PageBreak # For creating PDF documents and adding page breaks
from reportlab.lib.pagesizes import landscape, A4 # For defining page size and orientation (A4 landscape)

# Import custom modules from the application's structure
# SRC.ViewLayer.Logic.TimeTable: Contains logic for mapping courses to timetable slots and defines DAYS, HOURS constants
from SRC.ViewLayer.Logic.TimeTable import map_courses_to_slots, DAYS, HOURS
# SRC.ViewLayer.Layout.Timetable_qt5: Contains the TimetableGridWidget class for displaying the timetable
from SRC.ViewLayer.Layout.Timetable_qt5 import TimetableGridWidget # Corrected filename if it was layout_timetable.py previously
# SRC.ViewLayer.Logic.Pdf_Exporter: Contains the function to generate a PDF from timetable data
from SRC.ViewLayer.Logic.Pdf_Exporter import generate_pdf_from_data
# SRC.ViewLayer.Theme.modern_ui_qt5: Contains stylesheet information for a modern UI look
from SRC.ViewLayer.Theme.modern_ui_qt5 import ModernUIQt5


class TimetablesPageQt5(QMainWindow):
    """
    QMainWindow subclass to display generated timetable options.
    It allows users to navigate through different timetable solutions,
    export them to PDF, and go back to the course selection page.
    """
    def __init__(self, controller, go_back_callback=None):
        """
        Constructor for the TimetablesPageQt5.

        Args:
            controller: The application controller instance, used to fetch data
                        and handle application logic.
            go_back_callback (function, optional): A callback function to execute
                                                   when the user wants to return to
                                                   the previous view. Defaults to None.
        """
        super().__init__()  # Call the parent QMainWindow constructor
        self.controller = controller  # Store the controller instance
        self.go_back_callback = go_back_callback  # Store the callback for going back

        # Fetch all possible timetable options using the controller
        # These paths "Data/courses.txt" and "Data/selected_courses.txt" might be parameters to the controller method
        self.options = controller.get_all_options("Data/courses.xlsx", "Data/selected_courses.txt")

        self.current_index = 0  # Index to keep track of the currently displayed timetable option

        # self.apply_stylesheet() # This line is commented out, stylesheet is applied in init_ui
        self.init_ui()      # Initialize the user interface elements
        self.update_view()  # Populate the UI with the first timetable option (if any)

    def init_ui(self):
        """
        Initialize the main user interface components of the window.
        Sets up the window title, geometry, central widget, layout,
        navigation bar, and timetable display area.
        """
        self.setWindowTitle("Timetables")  # Set the window title
        self.setGeometry(100, 100, 1400, 800)  # Set window position (x, y) and size (width, height)

        # Apply the stylesheet for the timetable page from the ModernUIQt5 theme
        self.setStyleSheet(ModernUIQt5.get_timetable_stylesheet())

        # Central widget: A QWidget that will contain all other UI elements
        central_widget = QWidget()
        self.setCentralWidget(central_widget)  # Set this widget as the main content area of the QMainWindow

        # Main layout: A QVBoxLayout to arrange elements vertically
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)  # Set margins around the layout
        main_layout.setSpacing(20)  # Set spacing between widgets within the layout

        # Create and add the navigation bar (contains prev/next, title, export, back buttons)
        self.create_nav_bar(main_layout)

        # Create and add the container for displaying the timetable (a scrollable area)
        self.create_timetable_container(main_layout)

    def apply_stylesheet(self):
        """
        Applies an external QSS (Qt StyleSheet) file to the window.
        Note: This method is currently defined but commented out in __init__.
        It's kept here presumably for potential future use or alternative styling mechanism.
        """
        # __file__ is the path to the current Python script
        # os.path.dirname(os.path.abspath(__file__)) gets the directory of the current script
        # base_dir = os.path.dirname(os.path.abspath(__file__)) # Not used if Path is used

        # Construct the path to the QSS file using pathlib for better cross-platform compatibility
        # It assumes styles.qss is in a "Theme" subfolder, two levels up from the current file's parent directory.
        # This path structure might need adjustment based on the actual project layout.
        qss_path = Path(__file__).resolve().parent.parent / "Theme" / "styles.qss"

        if os.path.exists(qss_path):  # Check if the stylesheet file exists
            with open(qss_path, "r", encoding="utf-8") as file: # Open and read the file
                self.setStyleSheet(file.read()) # Apply the read stylesheet content
        else:
            # Print a warning if the QSS file is not found at the specified path
            print(f"Warning: QSS file not found at {qss_path}")

    def create_nav_bar(self, parent_layout):
        """
        Creates the navigation bar containing controls like 'Back', 'Previous',
        'Next', timetable title, and 'Export PDF'.

        Args:
            parent_layout (QLayout): The layout to which the navigation bar (QFrame) will be added.
        """
        nav_frame = QFrame()  # Create a QFrame to act as a container for the navigation elements
        nav_frame.setObjectName("navFrame")  # Set object name for QSS styling
        nav_layout = QHBoxLayout()  # Use QHBoxLayout to arrange navigation elements horizontally
        nav_layout.setSpacing(10)  # Spacing between elements in the nav bar
        nav_layout.setContentsMargins(10, 10, 10, 10) # Margins around the nav bar content

        # Back button: To return to the course selection screen
        self.back_button = QPushButton("← Back to Course Selection")
        self.back_button.setObjectName("backButton")  # For QSS styling
        self.back_button.setFixedSize(200, 40)      # Set a fixed size for the button
        self.back_button.clicked.connect(self.go_back) # Connect click signal to go_back method
        nav_layout.addWidget(self.back_button)      # Add button to the nav layout

        nav_layout.addStretch()  # Add a stretchable space to push subsequent items to the right/center

        # Previous button: To navigate to the previous timetable option
        self.prev_button = QPushButton("◄ Previous")
        self.prev_button.setObjectName("navButton") # For QSS styling
        self.prev_button.setFixedSize(100, 40)
        self.prev_button.clicked.connect(self.show_prev) # Connect to show_prev method
        nav_layout.addWidget(self.prev_button)

        # Title label: Displays "Timetable Option X of Y"
        self.title_label = QLabel("") # Initially empty, text set in update_view
        self.title_label.setObjectName("titleLabel") # For QSS styling
        self.title_label.setAlignment(Qt.AlignCenter) # Center the text
        self.title_label.setMinimumWidth(250) # Ensure it has enough space
        nav_layout.addWidget(self.title_label)

        # Next button: To navigate to the next timetable option
        self.next_button = QPushButton("Next ►")
        self.next_button.setObjectName("navButton") # For QSS styling
        self.next_button.setFixedSize(100, 40)
        self.next_button.clicked.connect(self.show_next) # Connect to show_next method
        nav_layout.addWidget(self.next_button)

        nav_layout.addStretch() # Add another stretchable space

        # Export button: To export the timetable(s) to a PDF file
        self.export_button = QPushButton("📄 Export PDF")
        self.export_button.setObjectName("exportButton") # For QSS styling
        self.export_button.setFixedSize(120, 40)
        self.export_button.clicked.connect(self.export_pdf_dialog) # Connect to export_pdf_dialog method
        nav_layout.addWidget(self.export_button)

        nav_frame.setLayout(nav_layout)  # Set the QHBoxLayout for the nav_frame
        parent_layout.addWidget(nav_frame) # Add the nav_frame to the main vertical layout

    def create_timetable_container(self, parent_layout):
        """
        Creates a scrollable area where the actual timetable grid will be displayed.
        Also includes a label for "No data" scenarios.

        Args:
            parent_layout (QLayout): The layout to which the scroll area will be added.
        """
        # Scroll Area: To allow scrolling if the timetable is larger than the display area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Allows the widget inside the scroll area to resize
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)   # Show vertical scrollbar only when needed
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded) # Show horizontal scrollbar only when needed
        self.scroll_area.setObjectName("scrollArea") # For QSS styling

        # Timetable widget: This QWidget will hold the actual TimetableGridWidget
        # It's placed inside the scroll_area
        self.timetable_widget = QWidget()
        self.timetable_widget.setObjectName("timetableWidgetContainer") # Distinguish from TimetableGridWidget itself for styling
        self.timetable_layout = QVBoxLayout() # Layout for the content within self.timetable_widget
        self.timetable_layout.setContentsMargins(20, 20, 20, 20) # Margins for the timetable content
        self.timetable_widget.setLayout(self.timetable_layout)

        # Set the timetable_widget as the content of the scroll_area
        self.scroll_area.setWidget(self.timetable_widget)
        parent_layout.addWidget(self.scroll_area) # Add the scroll area to the main layout

        # No data label: Displayed if no timetable options are available
        self.no_data_label = QLabel("No timetable options available.\nPlease go back and select courses.")
        self.no_data_label.setObjectName("noDataLabel") # For QSS styling
        self.no_data_label.setAlignment(Qt.AlignCenter) # Center the text
        self.no_data_label.hide()  # Initially hidden, shown by update_view if needed
        parent_layout.addWidget(self.no_data_label) # Add to the main layout (will be shown/hidden as appropriate)

    def update_view(self):
        """
        Updates the displayed timetable based on self.current_index.
        Clears any existing timetable grid and creates a new one.
        Handles the case where no timetable options are available.
        """
        if not self.options:  # Check if there are any timetable options
            # If no options, hide timetable-related UI elements and show the "no data" label
            self.prev_button.hide()
            self.next_button.hide()
            self.title_label.hide()
            self.export_button.hide()
            self.scroll_area.hide()
            self.no_data_label.show()
            return # Exit the method as there's nothing to display

        # If options exist, ensure timetable UI elements are visible and "no data" label is hidden
        self.prev_button.show()
        self.next_button.show()
        self.title_label.show()
        self.export_button.show()
        self.scroll_area.show()
        self.no_data_label.hide()

        # Update the title label to show current option number and total options
        self.title_label.setText(f"Timetable Option {self.current_index + 1} of {len(self.options)}")

        # Get the course list for the current timetable option
        current_timetable_courses = self.options[self.current_index]

        # Map these courses to the day/hour slots for grid display
        slot_map = map_courses_to_slots(current_timetable_courses)

        # Clear previous timetable content from the timetable_layout
        # Iterate in reverse to safely remove widgets
        for i in reversed(range(self.timetable_layout.count())):
            child_widget_item = self.timetable_layout.itemAt(i)
            if child_widget_item:
                widget = child_widget_item.widget()
                if widget:
                    widget.setParent(None) # Remove widget from layout and mark for deletion
                    widget.deleteLater()   # Ensure proper cleanup
                else: # If it's a spacer item or stretch
                    self.timetable_layout.removeItem(child_widget_item)


        # Create a new TimetableGridWidget with the current slot_map
        timetable_grid = TimetableGridWidget(slot_map)
        self.timetable_layout.addWidget(timetable_grid) # Add the new grid to the layout
        self.timetable_layout.addStretch() # Add a stretch to push the timetable to the top if space allows

        # Reset scroll position to the top for the new timetable view
        self.scroll_area.verticalScrollBar().setValue(0)
        self.scroll_area.horizontalScrollBar().setValue(0) # Also reset horizontal scroll

        # Update the enabled/disabled state of the Previous/Next navigation buttons
        self.update_button_states()

    def update_button_states(self):
        """
        Updates the enabled state of 'Previous' and 'Next' buttons
        based on the current_index and total number of options.
        Also sets a 'disabled' property for QSS styling.
        """
        # Previous button state
        can_go_prev = self.current_index > 0
        self.prev_button.setEnabled(can_go_prev)
        self.prev_button.setProperty("disabled", not can_go_prev) # For QSS: [disabled="true"]

        # Next button state
        can_go_next = self.current_index < len(self.options) - 1
        self.next_button.setEnabled(can_go_next)
        self.next_button.setProperty("disabled", not can_go_next) # For QSS: [disabled="true"]

        # Force style update to reflect the "disabled" property change in QSS
        # This is crucial for stylesheets that use property selectors like QPushButton[disabled="true"]
        self.prev_button.style().unpolish(self.prev_button)
        self.prev_button.style().polish(self.prev_button)
        self.next_button.style().unpolish(self.next_button)
        self.next_button.style().polish(self.next_button)

    def show_prev(self):
        """
        Handles the 'Previous' button click.
        Decrements current_index and updates the view if not at the first option.
        """
        if self.current_index > 0:  # Check if there's a previous option
            self.current_index -= 1   # Decrement index
            self.update_view()        # Refresh the displayed timetable

    def show_next(self):
        """
        Handles the 'Next' button click.
        Increments current_index and updates the view if not at the last option.
        """
        if self.current_index < len(self.options) - 1:  # Check if there's a next option
            self.current_index += 1  # Increment index
            self.update_view()       # Refresh the displayed timetable

    def go_back(self):
        """
        Handles the 'Back to Course Selection' button click.
        If a go_back_callback is provided, it's called. Otherwise, the window closes.
        """
        if self.go_back_callback:  # If a callback function was provided
            self.go_back_callback() # Execute the callback (e.g., to switch views in a larger app)
        else:
            self.close() # If no callback, just close this window

    def export_pdf_dialog(self):
        """
        Handles the 'Export PDF' button click.
        Prompts the user whether to export the current timetable or all options.
        Then, opens a file dialog to choose the save location and generates the PDF.
        """
        if not self.options: # If there are no timetables to export
            QMessageBox.warning(self, "No Data", "No timetable options to export.")
            return

        # Ask the user if they want to export all options or only the current one
        reply = QMessageBox.question(
            self, 'Export PDF',
            'Do you want to export all timetable options?\n\n'
            'Yes: Export all options\n'
            'No: Export current option only',
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, # Buttons: Yes, No, Cancel
            QMessageBox.Cancel # Default button (if user presses Enter, it might select this)
        )

        if reply == QMessageBox.Cancel: # If user cancels the dialog
            return

        # Open a "Save File" dialog to get the desired path and filename from the user
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save PDF', 'timetables.pdf', 'PDF files (*.pdf)' # Dialog title, default filename, file filter
        )

        if not file_path: # If the user cancels the file dialog or enters no path
            return

        try:
            if reply == QMessageBox.Yes: # User chose to export ALL timetable options
                # Create a SimpleDocTemplate for the PDF, using A4 landscape size
                doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
                all_elements = [] # List to hold all reportlab Flowables for the PDF

                # Iterate through all timetable options
                for idx, timetable_courses in enumerate(self.options):
                    slot_map = map_courses_to_slots(timetable_courses) # Map courses to grid slots
                    title = f"Timetable Option {idx + 1}"             # Title for this specific timetable
                    # Generate PDF elements for this timetable
                    # generate_pdf_from_data is expected to return a list of Flowables when return_elements=True
                    elements = generate_pdf_from_data(None, slot_map, title, return_elements=True)
                    all_elements.extend(elements) # Add these elements to the main list

                    # Add a PageBreak after each timetable, except for the last one
                    if idx < len(self.options) - 1:
                        all_elements.append(PageBreak())

                doc.build(all_elements) # Build the PDF document with all collected elements

                QMessageBox.information(
                    self, "Export Complete",
                    f"Successfully exported {len(self.options)} timetable options to:\n{file_path}"
                )
            else: # User chose to export only the CURRENT timetable option (reply == QMessageBox.No)
                current_timetable_courses = self.options[self.current_index] # Get current courses
                slot_map = map_courses_to_slots(current_timetable_courses)  # Map to grid
                title = f"Timetable Option {self.current_index + 1}"         # Title for the PDF
                # Call generate_pdf_from_data to create and save the PDF directly
                generate_pdf_from_data(file_path, slot_map, title)

                QMessageBox.information(
                    self, "Export Complete",
                    f"Successfully exported current timetable to:\n{file_path}"
                )

            # Attempt to open the generated PDF file using the default system application
            if sys.platform.startswith('win'): # For Windows
                os.startfile(file_path)
            elif sys.platform.startswith('darwin'): # For macOS
                os.system(f'open "{file_path}"') # Use 'open' command
            else: # For Linux and other POSIX systems
                os.system(f'xdg-open "{file_path}"') # Use 'xdg-open' command

        except Exception as e: # Catch any errors during PDF generation or file opening
            QMessageBox.critical(self, "Export Error", f"Failed to export PDF:\n{str(e)}")

    def closeEvent(self, event):
        """
        Handles the window close event (e.g., when the user clicks the 'X' button).
        If a go_back_callback is set, it's called, and the close event is ignored.
        Otherwise, it prompts the user for confirmation to exit.

        Args:
            event (QCloseEvent): The close event object.
        """
        if self.go_back_callback:
            # If a go_back_callback exists, it means this window is part of a larger navigation flow.
            # Execute the callback to return to the previous screen.
            self.go_back_callback()
            event.ignore() # Ignore the close event to prevent the window from actually closing.
        else:
            # Standard close behavior: ask for confirmation.
            reply = QMessageBox.question(
                self, 'Exit', 'Are you sure you want to exit?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No # Buttons: Yes, No. Default: No.
            )

            if reply == QMessageBox.Yes: # If user confirms exit
                # Check if the controller has a specific method to handle application exit (e.g., save state)
                if hasattr(self.controller, 'handle_exit') and callable(self.controller.handle_exit):
                    self.controller.handle_exit()
                event.accept() # Accept the close event, allowing the window to close.
            else:
                event.ignore() # Ignore the close event, keeping the window open.