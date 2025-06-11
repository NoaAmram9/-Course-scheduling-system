# screenshot_pdf_exporter.py - ייצוא PDF באמצעות screenshots

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QCheckBox, QSpinBox, QGroupBox, QRadioButton,
                             QButtonGroup, QMessageBox, QLineEdit, QComboBox, 
                             QProgressBar, QApplication)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QPainter
from reportlab.platypus import SimpleDocTemplate, PageBreak, Image as RLImage, Spacer
from reportlab.lib.pagesizes import landscape, A4, letter
from reportlab.lib.units import inch
import os
import sys
import tempfile
from datetime import datetime
from PIL import Image
import io

class ScreenshotPDFExportDialog(QDialog):
    """דיאלוג לבחירת אפשרויות ייצוא PDF מ-screenshots"""
    
    def __init__(self, total_timetables, current_index, parent=None):
        super().__init__(parent)
        self.total_timetables = total_timetables
        self.current_index = current_index
        self.export_options = {}
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("PDF Export - Screenshot Mode")
        self.setModal(True)
        self.resize(400, 450)
        
        layout = QVBoxLayout()
        
        # כותרת
        title = QLabel("Screenshot PDF Export")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        info = QLabel("This will capture screenshots of the displayed timetables")
        info.setStyleSheet("color: gray; font-style: italic;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        # בחירת מערכות
        self.create_timetable_selection_group(layout)
        
        # אפשרויות screenshot
        self.create_screenshot_options_group(layout)
        
        # שם קובץ
        self.create_filename_group(layout)
        
        # כפתורי פעולה
        self.create_action_buttons(layout)
        
        self.setLayout(layout)
        
    def create_timetable_selection_group(self, parent_layout):
        """יצירת קבוצת בחירת מערכות"""
        group = QGroupBox("Select Timetables to Export")
        layout = QVBoxLayout()
        
        self.export_group = QButtonGroup()
        
        self.current_only = QRadioButton(f"Current timetable only (#{self.current_index + 1})")
        self.current_only.setChecked(True)
        self.export_group.addButton(self.current_only, 0)
        layout.addWidget(self.current_only)
        
        self.all_timetables = QRadioButton(f"All loaded timetables ({self.total_timetables} total)")
        self.export_group.addButton(self.all_timetables, 1)
        layout.addWidget(self.all_timetables)
        
        # טווח מותאם אישית
        range_layout = QHBoxLayout()
        self.custom_range = QRadioButton("Custom range:")
        self.export_group.addButton(self.custom_range, 2)
        range_layout.addWidget(self.custom_range)
        
        range_layout.addWidget(QLabel("From:"))
        self.start_spin = QSpinBox()
        self.start_spin.setMinimum(1)
        self.start_spin.setMaximum(self.total_timetables)
        self.start_spin.setValue(1)
        range_layout.addWidget(self.start_spin)
        
        range_layout.addWidget(QLabel("To:"))
        self.end_spin = QSpinBox()
        self.end_spin.setMinimum(1)
        self.end_spin.setMaximum(self.total_timetables)
        self.end_spin.setValue(min(5, self.total_timetables))
        range_layout.addWidget(self.end_spin)
        
        layout.addLayout(range_layout)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
        
    def create_screenshot_options_group(self, parent_layout):
        """יצירת אפשרויות screenshot"""
        group = QGroupBox("Screenshot Options")
        layout = QVBoxLayout()
        
        # איכות תמונה
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Image Quality:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["High (Recommended)", "Medium", "Low"])
        quality_layout.addWidget(self.quality_combo)
        layout.addLayout(quality_layout)
        
        # גודל עמוד
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Page Size:"))
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["A4", "Letter"])
        size_layout.addWidget(self.page_size_combo)
        layout.addLayout(size_layout)
        
        # השהיה בין screenshots
        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel("Delay between captures (ms):"))
        self.delay_spin = QSpinBox()
        self.delay_spin.setMinimum(100)
        self.delay_spin.setMaximum(2000)
        self.delay_spin.setValue(500)
        delay_layout.addWidget(self.delay_spin)
        layout.addLayout(delay_layout)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
        
    def create_filename_group(self, parent_layout):
        """יצירת קבוצת שם קובץ"""
        group = QGroupBox("Output File")
        layout = QVBoxLayout()
        
        filename_layout = QHBoxLayout()
        filename_layout.addWidget(QLabel("Filename:"))
        self.filename_edit = QLineEdit()
        self.filename_edit.setText(f"timetables_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        filename_layout.addWidget(self.filename_edit)
        layout.addLayout(filename_layout)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
        
    def create_action_buttons(self, parent_layout):
        """יצירת כפתורי פעולה"""
        button_layout = QHBoxLayout()
        
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.export_button = QPushButton("Start Screenshot Export")
        self.export_button.clicked.connect(self.accept_export)
        self.export_button.setDefault(True)
        button_layout.addWidget(self.export_button)
        
        parent_layout.addLayout(button_layout)
        
    def get_export_options(self):
        """קבלת אפשרויות הייצוא שנבחרו"""
        selection_id = self.export_group.checkedId()
        
        if selection_id == 0:  # Current only
            timetable_indices = [self.current_index]
        elif selection_id == 1:  # All
            timetable_indices = list(range(self.total_timetables))
        else:  # Custom range
            start = self.start_spin.value() - 1
            end = self.end_spin.value()
            timetable_indices = list(range(start, end))
            
        return {
            'timetable_indices': timetable_indices,
            'quality': self.quality_combo.currentText(),
            'page_size': self.page_size_combo.currentText(),
            'delay': self.delay_spin.value(),
            'filename': self.filename_edit.text()
        }
        
    def accept_export(self):
        """אישור ייצוא"""
        self.export_options = self.get_export_options()
        
        if not self.export_options['filename']:
            QMessageBox.warning(self, "Invalid Input", "Please enter a filename.")
            return
            
        if not self.export_options['filename'].endswith('.pdf'):
            self.export_options['filename'] += '.pdf'
            
        if len(self.export_options['timetable_indices']) == 0:
            QMessageBox.warning(self, "Invalid Range", "Please select a valid range.")
            return
            
        self.accept()


class ScreenshotPDFExporter:
    """מחלקה לייצוא PDF באמצעות screenshots"""
    
    def __init__(self, parent_window):
        self.parent = parent_window
        self.screenshots = []
        self.current_screenshot_index = 0
        self.export_options = {}
        self.temp_files = []  # לניקוי קבצים זמניים
        
    def export_pdf_screenshots(self):
        """התחלת תהליך ייצוא screenshots"""
        if not hasattr(self.parent, 'all_options') or not self.parent.all_options:
            QMessageBox.warning(self.parent, "No Data", "No timetable options to export.")
            return
            
        # פתיחת דיאלוג
        dialog = ScreenshotPDFExportDialog(
            len(self.parent.all_options), 
            self.parent.current_index, 
            self.parent
        )
        
        if dialog.exec_() != QDialog.Accepted:
            return
            
        self.export_options = dialog.export_options
        
        # התחלת תהליך הצילום
        self.start_screenshot_process()
        
    def start_screenshot_process(self):
        """התחלת תהליך צילום המסכים"""
        self.screenshots = []
        self.current_screenshot_index = 0
        timetable_indices = self.export_options['timetable_indices']
        
        # יצירת progress dialog
        self.progress_dialog = QMessageBox(self.parent)
        self.progress_dialog.setWindowTitle("Capturing Screenshots")
        self.progress_dialog.setText("Preparing to capture screenshots...")
        self.progress_dialog.setStandardButtons(QMessageBox.Cancel)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        
        # הוספת progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(len(timetable_indices))
        self.progress_dialog.layout().addWidget(self.progress_bar, 1, 0, 1, 2)
        
        # חיבור כפתור ביטול
        self.progress_dialog.buttonClicked.connect(self.cancel_export)
        
        self.progress_dialog.show()
        
        # התחלת הצילום עם delay
        self.timer = QTimer()
        self.timer.timeout.connect(self.capture_next_screenshot)
        self.timer.start(self.export_options['delay'])
        
    def capture_next_screenshot(self):
        """צילום המסך הבא"""
        timetable_indices = self.export_options['timetable_indices']
        
        if self.current_screenshot_index >= len(timetable_indices):
            # סיימנו עם כל הצילומים
            self.timer.stop()
            self.progress_dialog.close()
            self.create_pdf_from_screenshots()
            return
        
        try:
            # עבור למערכת הנוכחית
            target_index = timetable_indices[self.current_screenshot_index]
            self.parent.current_index = target_index
            self.parent.update_view()  # עדכון התצוגה
            
            # עדכון progress
            self.progress_bar.setValue(self.current_screenshot_index)
            self.progress_dialog.setText(f"Capturing screenshot {self.current_screenshot_index + 1} of {len(timetable_indices)}")
            
            QApplication.processEvents()  # עדכון UI
            
            # צילום המסך של אזור מערכת השעות
            screenshot = self.capture_timetable_widget()
            if screenshot:
                self.screenshots.append(screenshot)
            
            self.current_screenshot_index += 1
            
        except Exception as e:
            self.timer.stop()
            self.progress_dialog.close()
            QMessageBox.critical(self.parent, "Screenshot Error", f"Failed to capture screenshot: {str(e)}")
            
    def capture_timetable_widget(self):
        """צילום המסך של widget מערכת השעות"""
        try:
            # מציאת widget מערכת השעות (תתאים לשם ה-widget שלך)
            timetable_widget = None
            
            # חיפוש אוטומטי של widget מערכת השעות
            if hasattr(self.parent, 'timetable_widget'):
                timetable_widget = self.parent.timetable_widget
            elif hasattr(self.parent, 'centralWidget'):
                # חיפוש בכל ה-children
                for child in self.parent.centralWidget().findChildren(object):
                    if 'timetable' in child.objectName().lower() or 'table' in child.objectName().lower():
                        timetable_widget = child
                        break
            
            if not timetable_widget:
                # כברירת מחדל - צילום כל החלון
                timetable_widget = self.parent
            
            # יצירת QPixmap מהWidget
            pixmap = timetable_widget.grab()
            
            # המרה לPIL Image לעיבוד נוסף
            qimage = pixmap.toImage()
            buffer = qimage.bits().asstring(qimage.byteCount())
            img = Image.frombytes("RGBA", (qimage.width(), qimage.height()), buffer, "raw", "RGBA")
            
            # המרה ל-RGB (להסרת שקיפות)
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            
            return img
            
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None
            
    def create_pdf_from_screenshots(self):
        """יצירת PDF מהscreenshots"""
        try:
            file_path = self.export_options['filename']
            page_size = A4 if self.export_options['page_size'] == 'A4' else letter
            
            doc = SimpleDocTemplate(file_path, pagesize=page_size)
            elements = []
            
            for i, img in enumerate(self.screenshots):
                # שמירה זמנית של התמונה
                temp_img_path = tempfile.mktemp(suffix='.png')
                self.temp_files.append(temp_img_path)
                
                # קביעת איכות לפי בחירת המשתמש
                quality_map = {"High (Recommended)": 95, "Medium": 75, "Low": 50}
                quality = quality_map.get(self.export_options['quality'], 95)
                
                img.save(temp_img_path, 'PNG', quality=quality)
                
                # הוספה ל-PDF
                # חישוב גודל מתאים לעמוד
                img_width, img_height = img.size
                page_width, page_height = page_size
                
                # שמירה על יחס גובה-רוחב
                scale = min((page_width - 72) / img_width, (page_height - 72) / img_height)  # 72 = 1 inch margins
                
                new_width = img_width * scale
                new_height = img_height * scale
                
                rl_img = RLImage(temp_img_path, width=new_width, height=new_height)
                elements.append(rl_img)
                
                # הוספת מעבר עמוד אם לא התמונה האחרונה
                if i < len(self.screenshots) - 1:
                    elements.append(PageBreak())
            
            # בניית ה-PDF
            doc.build(elements)
            
            # ניקוי קבצים זמניים
            self.cleanup_temp_files()
            
            # הצגת הודעת הצלחה
            QMessageBox.information(
                self.parent, "Export Complete",
                f"Successfully exported PDF with {len(self.screenshots)} screenshots to:\n{file_path}"
            )
            
            # פתיחת הקובץ
            self.open_pdf_file(file_path)
            
        except Exception as e:
            self.cleanup_temp_files()
            QMessageBox.critical(self.parent, "Export Failed", f"Failed to create PDF: {str(e)}")
            
    def cleanup_temp_files(self):
        """ניקוי קבצים זמניים"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        self.temp_files.clear()
        
    def cancel_export(self):
        """ביטול תהליך הייצוא"""
        if hasattr(self, 'timer'):
            self.timer.stop()
        self.cleanup_temp_files()
        
    def open_pdf_file(self, file_path):
        """פתיחת קובץ PDF"""
        try:
            if sys.platform.startswith('win'):
                os.startfile(file_path)
            elif sys.platform.startswith('darwin'):
                os.system(f'open "{file_path}"')
            else:
                os.system(f'xdg-open "{file_path}"')
        except Exception as e:
            QMessageBox.warning(
                self.parent, "Cannot Open PDF", 
                f"PDF exported successfully but couldn't open it automatically:\n{str(e)}"
            )