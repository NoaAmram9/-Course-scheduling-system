from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QLabel, QLineEdit, QPushButton, QFrame, 
                            QSpacerItem, QSizePolicy, QCheckBox, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class RegisterLayout:
    """Layout manager for register screen"""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.setObjectName("RegisterPage")
        self.parent.setStyleSheet("QWidget#RegisterWidget { background: white; }")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the register UI layout"""
        main_layout = QVBoxLayout(self.parent)
        main_layout.setContentsMargins(60, 40, 60, 40)
       
        main_layout.setSpacing(0)
        
        scroll_area = QScrollArea(self.parent)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setObjectName("scrollArea")
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        register_card = QFrame()
        register_card.setObjectName("registerCard")
        register_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        card_layout = QVBoxLayout(register_card)
        card_layout.setContentsMargins(20, 20, 20, 20) 
        card_layout.setSpacing(20)
        
        self.setup_header(card_layout)
        self.setup_form(card_layout)
        self.setup_terms(card_layout)
        self.setup_buttons(card_layout)
        self.setup_footer(card_layout)
        
        scroll_area.setWidget(register_card)
        
        main_layout.addWidget(scroll_area)


    def setup_header(self, layout):
        """Setup header section"""
        # Title
        title_label = QLabel("Create Account")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Join us today - it's free!")
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
        
        # First Name field
        first_name_label = QLabel("First Name:")
        first_name_label.setObjectName("fieldLabel")
        self.parent.first_name_input = QLineEdit()
        self.parent.first_name_input.setObjectName("inputField")
        self.parent.first_name_input.setPlaceholderText("Enter your first name")
        form_layout.addRow(first_name_label, self.parent.first_name_input)
        
        # Last Name field
        last_name_label = QLabel("Last Name:")
        last_name_label.setObjectName("fieldLabel")
        self.parent.last_name_input = QLineEdit()
        self.parent.last_name_input.setObjectName("inputField")
        self.parent.last_name_input.setPlaceholderText("Enter your last name")
        form_layout.addRow(last_name_label, self.parent.last_name_input)
        
        # Username field
        username_label = QLabel("Username:")
        username_label.setObjectName("fieldLabel")
        self.parent.username_input = QLineEdit()
        self.parent.username_input.setObjectName("inputField")
        self.parent.username_input.setPlaceholderText("Choose a unique username")
        form_layout.addRow(username_label, self.parent.username_input)
        
        # Email field
        email_label = QLabel("Email Address:")
        email_label.setObjectName("fieldLabel")
        self.parent.email_input = QLineEdit()
        self.parent.email_input.setObjectName("inputField")
        self.parent.email_input.setPlaceholderText("Enter your email address")
        form_layout.addRow(email_label, self.parent.email_input)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setObjectName("fieldLabel")
        self.parent.password_input = QLineEdit()
        self.parent.password_input.setObjectName("inputField")
        self.parent.password_input.setPlaceholderText("Create a strong password")
        self.parent.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(password_label, self.parent.password_input)
        
        # Confirm Password field
        confirm_password_label = QLabel("Confirm Password:")
        confirm_password_label.setObjectName("fieldLabel")
        self.parent.confirm_password_input = QLineEdit()
        self.parent.confirm_password_input.setObjectName("inputField")
        self.parent.confirm_password_input.setPlaceholderText("Confirm your password")
        self.parent.confirm_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(confirm_password_label, self.parent.confirm_password_input)
        
        layout.addLayout(form_layout)
        
        # Password strength indicator
        self.parent.password_strength_label = QLabel("")
        self.parent.password_strength_label.setObjectName("passwordStrengthLabel")
        layout.addWidget(self.parent.password_strength_label)
    
    def setup_terms(self, layout):
        """Setup terms and conditions section"""
        terms_layout = QHBoxLayout()
        self.parent.terms_checkbox = QCheckBox()
        self.parent.terms_checkbox.setObjectName("checkBox")
        
        terms_text = QLabel("I agree to the Terms of Service and Privacy Policy")
        terms_text.setObjectName("termsLabel")
        terms_text.setWordWrap(True)
        
        terms_layout.addWidget(self.parent.terms_checkbox)
        terms_layout.addWidget(terms_text)
        terms_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        layout.addLayout(terms_layout)
    
    def setup_buttons(self, layout):
        """Setup buttons section"""
        # Register button
        self.parent.register_button = QPushButton("Create Account")
        self.parent.register_button.setObjectName("primaryButton")
        layout.addWidget(self.parent.register_button)
        
        # Spacer
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
    
    def setup_footer(self, layout):
        """Setup footer section"""
        # Login link
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignCenter)
        
        already_have_label = QLabel("Already have an account?")
        already_have_label.setObjectName("footerLabel")
        
        self.parent.login_link = QPushButton("Sign In")
        self.parent.login_link.setObjectName("linkButton")
        
        footer_layout.addWidget(already_have_label)
        footer_layout.addWidget(self.parent.login_link)
        
        layout.addLayout(footer_layout)
        
        # Add stretch to push everything up
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))