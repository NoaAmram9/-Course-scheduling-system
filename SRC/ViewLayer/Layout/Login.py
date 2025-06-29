from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QLabel, QLineEdit, QPushButton, QFrame, 
                            QSpacerItem, QSizePolicy, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap


class LoginLayout:
    """Layout manager for login screen"""
    
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the login UI layout"""
        # Main layout
        main_layout = QVBoxLayout(self.parent)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Center container
        center_frame = QFrame()
        center_frame.setObjectName("centerFrame")
        center_layout = QHBoxLayout(center_frame)
        center_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add spacers for centering
        center_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Login card
        login_card = QFrame()
        login_card.setObjectName("loginCard")
        login_card.setFixedSize(400, 500)
        
        # Login card layout
        card_layout = QVBoxLayout(login_card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)
        
        # Header
        self.setup_header(card_layout)
        
        # Form
        self.setup_form(card_layout)
        
        # Buttons
        self.setup_buttons(card_layout)
        
        # Footer
        self.setup_footer(card_layout)
        
        center_layout.addWidget(login_card)
        center_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Add vertical spacers
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(center_frame)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    def setup_header(self, layout):
        """Setup header section"""
        # Title
        title_label = QLabel("Welcome Back")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Please sign in to your account")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
        # Spacer
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
    
    def setup_form(self, layout):
        """Setup form section"""
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        
        # Username field
        username_label = QLabel("Username:")
        username_label.setObjectName("fieldLabel")
        self.parent.username_input = QLineEdit()
        self.parent.username_input.setObjectName("inputField")
        self.parent.username_input.setPlaceholderText("Enter your username")
        form_layout.addRow(username_label, self.parent.username_input)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setObjectName("fieldLabel")
        self.parent.password_input = QLineEdit()
        self.parent.password_input.setObjectName("inputField")
        self.parent.password_input.setPlaceholderText("Enter your password")
        self.parent.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(password_label, self.parent.password_input)
        
        layout.addLayout(form_layout)
        
        # Remember me checkbox
        remember_layout = QHBoxLayout()
        self.parent.remember_checkbox = QCheckBox("Remember me")
        self.parent.remember_checkbox.setObjectName("checkBox")
        remember_layout.addWidget(self.parent.remember_checkbox)
        remember_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        layout.addLayout(remember_layout)
    
    def setup_buttons(self, layout):
        """Setup buttons section"""
        # Login button
        self.parent.login_button = QPushButton("Sign In")
        self.parent.login_button.setObjectName("primaryButton")
        layout.addWidget(self.parent.login_button)
        
        # Spacer
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
    
    def setup_footer(self, layout):
        """Setup footer section"""
        # Register link
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignCenter)
        
        dont_have_label = QLabel("Don't have an account?")
        dont_have_label.setObjectName("footerLabel")
        
        self.parent.register_link = QPushButton("Sign Up")
        self.parent.register_link.setObjectName("linkButton")
        
        footer_layout.addWidget(dont_have_label)
        footer_layout.addWidget(self.parent.register_link)
        
        layout.addLayout(footer_layout)
        
        # Add stretch to push everything up
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))