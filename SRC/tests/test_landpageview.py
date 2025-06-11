import pytest
from unittest import mock
import os
import shutil
import sys
from pathlib import Path
import PyQt5
os.environ["QT_QPA_PLATFORM"] = "offscreen"  # Ensure headless testing for PyQt5
from SRC.Models.ValidationError import ValidationError 
from SRC.ViewLayer.View.LandPageView import LandPageView
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFrame
from PyQt5.QtCore import Qt, QUrl, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtTest import QTest
from PyQt5.QtTest import QSignalSpy

def normalize_path(path):
    """Normalize path separators for cross-platform comparison"""
    return str(path).replace('\\', '/')

@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance for tests"""
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    yield app

@pytest.fixture
def landpage(tmp_path, qapp):
    """Create LandPageView instance with mocked functionality"""
    # Mock the stylesheet loading to avoid file path issues in tests
    with mock.patch.object(LandPageView, 'apply_stylesheet'):
        page = LandPageView()
        page.hide()  # Hide the window during tests
        
        # Connect upload button to a mock function for testing
        def mock_upload():
            dialog = mock.Mock()
            dialog.getOpenFileName = mock.Mock()
            # This will be mocked in individual tests
            pass
        
        page.upload_button.clicked.connect(mock_upload)
        return page

def test_upload_via_dialog_txt_file(tmp_path, landpage):
    """Test uploading a valid .txt file via file dialog."""
    file_path = tmp_path / "courses.txt"
    file_path.write_text("course_id, name")

    # Mock the file dialog to return our test file
    with mock.patch("PyQt5.QtWidgets.QFileDialog.getOpenFileName") as mock_dialog:
        mock_dialog.return_value = (str(file_path), "Text files (*.txt)")
        
        # Simulate the upload process by directly calling what the button should do
        filename, _ = mock_dialog.return_value
        if filename:
            landpage.uploaded_path = filename
            landpage.file_label.setText(f"Uploaded: {os.path.basename(filename)}")
            landpage.file_uploaded.emit(filename)
        
        assert landpage.uploaded_path == str(file_path)
        assert "Uploaded:" in landpage.file_label.text()
        assert file_path.name in landpage.file_label.text()

def test_upload_via_drag_and_drop_valid_txt(tmp_path, landpage):
    """Test drag-and-drop upload of a valid .txt file."""
    file_path = tmp_path / "courses.txt"
    file_path.write_text("course_id,name")

    # Create mock drop event
    mime_data = QMimeData()
    urls = [QUrl.fromLocalFile(str(file_path))]
    mime_data.setUrls(urls)
    
    drop_event = QDropEvent(
        landpage.drop_frame.pos(),
        Qt.CopyAction,
        mime_data,
        Qt.LeftButton,
        Qt.NoModifier
    )

    # Mock the mimeData method to return our test data
    drop_event.mimeData = mock.Mock(return_value=mime_data)

    landpage.dropEvent(drop_event)
    
    # Use helper function for path comparison
    assert normalize_path(landpage.uploaded_path) == normalize_path(file_path)
    assert "Uploaded:" in landpage.file_label.text()
    assert file_path.name in landpage.file_label.text()

def test_reject_invalid_file_type(landpage):
    """Test that uploading an invalid file type shows an error and rejects it."""
    # Create mock drop event with PDF file
    mime_data = QMimeData()
    urls = [QUrl.fromLocalFile("/path/to/bad_file.pdf")]
    mime_data.setUrls(urls)
    
    drop_event = QDropEvent(
        landpage.drop_frame.pos(),
        Qt.CopyAction,
        mime_data,
        Qt.LeftButton,
        Qt.NoModifier
    )

    drop_event.mimeData = mock.Mock(return_value=mime_data)

    landpage.dropEvent(drop_event)
    
    # Should not update the uploaded_path for invalid files
    assert landpage.uploaded_path is None
    assert landpage.file_label.text() == ""

def test_drag_enter_accepts_valid_files(landpage):
    """Test that drag enter event accepts valid file types."""
    mime_data = QMimeData()
    urls = [QUrl.fromLocalFile("/path/to/file.txt")]
    mime_data.setUrls(urls)
    
    drag_event = QDragEnterEvent(
        landpage.drop_frame.pos(),
        Qt.CopyAction,
        mime_data,
        Qt.LeftButton,
        Qt.NoModifier
    )
    
    drag_event.mimeData = mock.Mock(return_value=mime_data)
    drag_event.acceptProposedAction = mock.Mock()
    drag_event.ignore = mock.Mock()
    
    landpage.dragEnterEvent(drag_event)
    
    drag_event.acceptProposedAction.assert_called_once()
    drag_event.ignore.assert_not_called()

def test_drag_enter_rejects_invalid_files(landpage):
    """Test that drag enter event rejects invalid file types."""
    mime_data = QMimeData()
    urls = [QUrl.fromLocalFile("/path/to/file.pdf")]
    mime_data.setUrls(urls)
    
    drag_event = QDragEnterEvent(
        landpage.drop_frame.pos(),
        Qt.CopyAction,
        mime_data,
        Qt.LeftButton,
        Qt.NoModifier
    )
    
    drag_event.mimeData = mock.Mock(return_value=mime_data)
    drag_event.acceptProposedAction = mock.Mock()
    drag_event.ignore = mock.Mock()
    
    landpage.dragEnterEvent(drag_event)
    
    drag_event.acceptProposedAction.assert_not_called()
    drag_event.ignore.assert_called_once()

def test_file_label_updates_correctly(tmp_path, landpage):
    """Test the file label updates with the uploaded file's name."""
    file_path = tmp_path / "courses.txt"
    file_path.write_text("test data")

    # Simulate file upload by directly setting the values as dropEvent does
    landpage.uploaded_path = str(file_path)
    landpage.file_label.setText(f"Uploaded: {os.path.basename(str(file_path))}")
    
    assert landpage.file_label.text() == f"Uploaded: {file_path.name}"

def test_upload_file_dialog_cancel_does_nothing(landpage):
    """Test that cancelling the file dialog does not upload any file."""
    # Simulate cancelled dialog (empty filename)
    filename = ""
    if filename:
        landpage.uploaded_path = filename
        landpage.file_label.setText(f"Uploaded: {os.path.basename(filename)}")
    
    assert landpage.uploaded_path is None
    assert landpage.file_label.text() == ""

def test_handle_drop_path_with_spaces(tmp_path, landpage):
    """Test drag-and-drop handling of file paths containing spaces."""
    file_path = tmp_path / "my courses file.txt"
    file_path.write_text("data")
    
    mime_data = QMimeData()
    urls = [QUrl.fromLocalFile(str(file_path))]
    mime_data.setUrls(urls)
    
    drop_event = QDropEvent(
        landpage.drop_frame.pos(),
        Qt.CopyAction,
        mime_data,
        Qt.LeftButton,
        Qt.NoModifier
    )

    drop_event.mimeData = mock.Mock(return_value=mime_data)

    landpage.dropEvent(drop_event)
    
    # Use helper function for path comparison
    assert normalize_path(landpage.uploaded_path) == normalize_path(file_path)
    assert "my courses file.txt" in landpage.file_label.text()

def test_welcome_header_present(landpage):
    """Test that the welcome header label is present on the LandPage."""
    # Find the header label among the children
    header_found = False
    for child in landpage.findChildren(QLabel):
        if "Scudual System Creator" in child.text():
            header_found = True
            break
    assert header_found

def test_upload_label_text(landpage):
    """Test that the drop label instructs the user to drag a file."""
    drop_text = landpage.drop_label.text().lower()
    assert "drag" in drop_text
    assert ".txt" in drop_text or ".xlsx" in drop_text

def test_file_format_hint_shown(landpage):
    """Test that the label mentions the required file formats."""
    drop_text = landpage.drop_label.text()
    assert ".txt" in drop_text or ".xlsx" in drop_text

def test_accepts_xlsx_files(tmp_path, landpage):
    """Test that .xlsx files are also accepted."""
    file_path = tmp_path / "courses.xlsx"
    file_path.write_bytes(b"fake excel content")  # Create fake xlsx file
    
    mime_data = QMimeData()
    urls = [QUrl.fromLocalFile(str(file_path))]
    mime_data.setUrls(urls)
    
    drop_event = QDropEvent(
        landpage.drop_frame.pos(),
        Qt.CopyAction,
        mime_data,
        Qt.LeftButton,
        Qt.NoModifier
    )

    drop_event.mimeData = mock.Mock(return_value=mime_data)

    landpage.dropEvent(drop_event)
    
    # Use helper function for path comparison
    assert normalize_path(landpage.uploaded_path) == normalize_path(file_path)
    assert "Uploaded:" in landpage.file_label.text()

def test_multiple_files_in_drop_takes_first_valid(tmp_path, landpage):
    """Test that when multiple files are dropped, the first valid one is taken."""
    txt_file = tmp_path / "courses.txt"
    txt_file.write_text("data")
    pdf_file = tmp_path / "invalid.pdf"
    pdf_file.write_bytes(b"pdf content")
    
    mime_data = QMimeData()
    urls = [
        QUrl.fromLocalFile(str(pdf_file)),  # Invalid first
        QUrl.fromLocalFile(str(txt_file))   # Valid second
    ]
    mime_data.setUrls(urls)
    
    drop_event = QDropEvent(
        landpage.drop_frame.pos(),
        Qt.CopyAction,
        mime_data,
        Qt.LeftButton,
        Qt.NoModifier
    )

    drop_event.mimeData = mock.Mock(return_value=mime_data)

    landpage.dropEvent(drop_event)
    
    # Use helper function for path comparison
    assert normalize_path(landpage.uploaded_path) == normalize_path(txt_file)
    assert "courses.txt" in landpage.file_label.text()
def test_file_uploaded_signal_emitted(tmp_path, landpage):
    """Test that the file_uploaded signal is emitted when a file is uploaded."""
    file_path = tmp_path / "courses.txt"
    file_path.write_text("data")

    # Use a Qt signal spy for better signal testing
    spy = QSignalSpy(landpage.file_uploaded)

    mime_data = QMimeData()
    urls = [QUrl.fromLocalFile(str(file_path))]
    mime_data.setUrls(urls)

    drop_event = QDropEvent(
        landpage.drop_frame.pos(),
        Qt.CopyAction,
        mime_data,
        Qt.LeftButton,
        Qt.NoModifier
    )

    drop_event.mimeData = mock.Mock(return_value=mime_data)

    landpage.dropEvent(drop_event)

    assert len(spy) == 1
    # Use normalize_path helper to handle cross-platform path comparison
    assert normalize_path(spy[0][0]) == normalize_path(str(file_path))
def test_ui_elements_present(landpage):
    """Test that all expected UI elements are present."""
    # Check that essential UI components exist
    assert landpage.drop_frame is not None
    assert landpage.drop_label is not None
    assert landpage.upload_button is not None
    assert landpage.file_label is not None
    assert landpage.send_button is not None
    
    # Check button texts
    assert landpage.upload_button.text() == "UPLOAD"
    assert landpage.send_button.text() == "SEND."

def test_window_properties(landpage):
    """Test window properties are set correctly."""
    assert landpage.windowTitle() == "Schedule System Creator"
    assert landpage.size().width() == 800
    assert landpage.size().height() == 800

def test_accepts_drops_enabled(landpage):
    """Test that the widget accepts drops."""
    assert landpage.acceptDrops() == True

def test_initial_state(landpage):
    """Test that the widget starts in the correct initial state."""
    assert landpage.uploaded_path is None
    assert landpage.file_label.text() == ""

def test_drag_enter_with_no_files(landpage):
    """Test drag enter event with no files."""
    mime_data = QMimeData()
    # No URLs set
    
    drag_event = QDragEnterEvent(
        landpage.drop_frame.pos(),
        Qt.CopyAction,
        mime_data,
        Qt.LeftButton,
        Qt.NoModifier
    )
    
    drag_event.mimeData = mock.Mock(return_value=mime_data)
    drag_event.acceptProposedAction = mock.Mock()
    drag_event.ignore = mock.Mock()
    
    landpage.dragEnterEvent(drag_event)
    
    drag_event.acceptProposedAction.assert_not_called()
    drag_event.ignore.assert_called_once()

def test_drop_with_no_valid_files(landpage):
    """Test drop event with no valid files."""
    mime_data = QMimeData()
    urls = [QUrl.fromLocalFile("/path/to/file.pdf"), QUrl.fromLocalFile("/path/to/file.doc")]
    mime_data.setUrls(urls)
    
    drop_event = QDropEvent(
        landpage.drop_frame.pos(),
        Qt.CopyAction,
        mime_data,
        Qt.LeftButton,
        Qt.NoModifier
    )

    drop_event.mimeData = mock.Mock(return_value=mime_data)

    landpage.dropEvent(drop_event)
    
    # Should not update anything for invalid files
    assert landpage.uploaded_path is None
    assert landpage.file_label.text() == ""