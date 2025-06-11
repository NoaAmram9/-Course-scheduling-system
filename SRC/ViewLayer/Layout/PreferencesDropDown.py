from PyQt5.QtWidgets import QWidget, QToolButton, QMenu, QAction, QActionGroup, QHBoxLayout
from PyQt5.QtCore import Qt
from SRC.ViewLayer.Theme.ModernUIQt5 import ModernUIQt5

class PreferencesDropdown(QWidget):
    
    # Mapping of visible labels to actual internal preference keys
    PREFERENCES_OPTIONS = {
        "None": "None",
        "Active Days": "active_days",
        "Free windows": "free_windows_number",
        "Total free windows": "free_windows_sum",
        "Average Start Time": "average_start_time",
        "Average End Time": "average_end_time",
    }
    
    # Define sorting orders with boolean values
    ORDER_OPTIONS = {
        "Ascending": True,
        "Descending": False
    }
    
    def __init__(self, callback):
        super().__init__()
        self.callback = callback # A function that will be called when a selection changes
        self.current_order = "Ascending"
        self.current_preference = "None"
    
        # Set layout for the whole dropdown component
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Create the dropdown button
        self.button = QToolButton()
        self.button.setText("Display by ▾")
        self.button.setObjectName("dropdownButton")
        self.button.setPopupMode(QToolButton.InstantPopup)  # Opens immediately on click
        
        
        # Create the dropdown menu
        self.menu = QMenu()
        # self.menu.setStyleSheet("QMenu { background-color: white; } QMenu::item:selected { background-color: darkgrey; }")
        self.menu.setAttribute(Qt.WA_StyledBackground, True)
        
        # ------------ Section 1: Preferences --------------
        self.menu.addSection("Preference")
        self.pref_group = QActionGroup(self.menu) # Group of preference actions (radio-style)
        self.pref_group.setExclusive(True) # Only one can be selected at a time
        
        # Create each preference option in the menu
        for label, value in self.PREFERENCES_OPTIONS.items():
            action = QAction(label, self.menu, checkable=True)
            action.setData(value) # Store internal value (not the visible label)
            if value == "None":  # Default selection
                action.setChecked(True)  # Default selection
            self.pref_group.addAction(action)
            self.menu.addAction(action)

        self.menu.addSeparator() # Visual separation between sections

        # --------------- Section 2: Order --------------
        self.menu.addSection("Order")
        self.order_group = QActionGroup(self.menu)
        self.order_group.setExclusive(True)    
        
        # Create each order option in the menu
        for label, value in self.ORDER_OPTIONS.items():
            action = QAction(label, self.menu, checkable=True)
            action.setData(value)
            if label == "Ascending":
                action.setChecked(True)
            self.order_group.addAction(action)
            self.menu.addAction(action)

        # --------------- End of Menu Setup ---------------
        # Connect signal: when any action in either group is triggered, call handler (on_selection_changed)
        self.pref_group.triggered.connect(self.on_selection_changed)
        self.order_group.triggered.connect(self.on_selection_changed)

        # Assign the menu to the button
        self.button.setMenu(self.menu)
        
        # Add button to the layout
        layout.addWidget(self.button)
        self.setLayout(layout)
        # Load and apply external stylesheet
        self.menu.setStyleSheet(ModernUIQt5.get_dropdown_stylesheet())


    def on_selection_changed(self, action):
        """
        Called when either a preference or order option is selected.
        It updates current values and sends them to the external callback.
        """
        # Update current selections
        self.current_order = self.get_checked(self.order_group)
        self.current_preference = self.get_checked(self.pref_group)
        self.callback(self.current_preference, self.current_order)

    def get_checked(self, group):
        """
        Helper method to return the data of the currently checked action in a group.
        """
        for action in group.actions():
            if action.isChecked():
                return action.data()  # Return the stored value (not the label)
        return ""
