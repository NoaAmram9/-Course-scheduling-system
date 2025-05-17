import pytest
from unittest import mock
import os
import shutil
from SRC.Models.ValidationError import ValidationError 
from SRC.ViewLayer.LandPage import LandPage
import tkinter as tk
import tkinterdnd2 as TkinterDnD

# Mock drag-and-drop registration globally to prevent errors in tests without real DnD
@pytest.fixture(autouse=True)
def mock_drag_and_drop():
    with mock.patch("tkinterdnd2.Tk.drop_target_register", return_value=None):
        yield

@pytest.fixture
def landpage(tmp_path):
    # Patch to avoid real drag-drop widget setup and create LandPage instance
    with mock.patch("customtkinter.CTkFrame.drop_target_register", create=True):
        try:
            root = TkinterDnD.Tk()
        except tk.TclError:
            root = tk.Tk()

        controller = mock.Mock()
        page = LandPage(root, controller)
        return page

def test_upload_via_dialog_txt_file(tmp_path, landpage):
    """Test uploading a valid .txt file via file dialog."""
    file_path = tmp_path / "courses.txt"
    file_path.write_text("course_id, name")

    with mock.patch("tkinter.filedialog.askopenfilename", return_value=str(file_path)), \
         mock.patch("shutil.copy") as mock_copy:
        landpage.upload_file()
        mock_copy.assert_called_once()
        assert landpage.file_uploaded is True
        assert "Uploaded:" in landpage.file_label.cget("text")

def test_upload_via_drag_and_drop_valid_txt(tmp_path, landpage):
    """Test drag-and-drop upload of a valid .txt file."""
    file_path = tmp_path / "courses.txt"
    file_path.write_text("course_id,name")

    event = mock.Mock()
    event.data = f"{{{file_path}}}"

    with mock.patch("shutil.copy") as mock_copy:
        landpage.handle_drop(event)
        mock_copy.assert_called_once()
        assert landpage.file_uploaded is True
        assert "Uploaded:" in landpage.file_label.cget("text")

def test_reject_invalid_file_type(landpage):
    """Test that uploading an invalid file type shows an error and rejects it."""
    event = mock.Mock()
    event.data = "{bad_file.pdf}"

    with mock.patch("tkinter.messagebox.showerror") as mock_error:
        landpage.handle_drop(event)
        mock_error.assert_called_once_with("Invalid file", "Only .txt files are allowed.")
        assert landpage.file_uploaded is False

def test_file_label_updates_correctly(tmp_path, landpage):
    """Test the file label updates with the uploaded file's name."""
    file_path = tmp_path / "courses.txt"
    file_path.write_text("test data")

    with mock.patch("tkinter.filedialog.askopenfilename", return_value=str(file_path)), \
         mock.patch("shutil.copy"):
        landpage.upload_file()
        assert landpage.file_label.cget("text") == f"Uploaded: {file_path.name}"

def test_send_action_blocks_without_file(landpage):
    """Test that proceeding without uploading a file shows a warning."""
    landpage.file_uploaded = False

    with mock.patch("tkinter.messagebox.showwarning") as mock_warn:
        landpage.send_action()
        mock_warn.assert_called_once_with("Missing File", "Please upload a .txt file before proceeding.")

def test_send_action_launches_main_page_if_uploaded(landpage):
    """Test that send_action opens MainPage if a file is uploaded and processed."""
    landpage.file_uploaded = True
    landpage.root = mock.Mock()
    landpage.controller = mock.Mock()
    landpage.controller.process_repository_file.return_value = ["OK"]

    with mock.patch("SRC.ViewLayer.LandPage.MainPage") as MockMainPage:
        instance = MockMainPage.return_value
        landpage.send_action()
        landpage.root.withdraw.assert_called_once()
        instance.run.assert_called_once()

def test_upload_creates_data_directory(tmp_path, landpage):
    """Test that uploading creates the 'Data' directory if not present."""
    file_path = tmp_path / "courses.txt"
    file_path.write_text("abc")

    with mock.patch("tkinter.filedialog.askopenfilename", return_value=str(file_path)), \
         mock.patch("shutil.copy"), \
         mock.patch("os.makedirs") as mock_makedirs:

        landpage.upload_file()
        called_path, kwargs = mock_makedirs.call_args
        assert called_path[0].endswith("Data")
        assert kwargs == {"exist_ok": True}

def test_upload_file_dialog_cancel_does_nothing(landpage):
    """Test that cancelling the file dialog does not upload any file."""
    with mock.patch("tkinter.filedialog.askopenfilename", return_value=""):
        landpage.upload_file()
        assert landpage.file_uploaded is False

def test_handle_drop_path_with_spaces(tmp_path, landpage):
    """Test drag-and-drop handling of file paths containing spaces."""
    file_path = tmp_path / "my courses file.txt"
    file_path.write_text("data")
    event = mock.Mock()
    event.data = f"{{{file_path}}}"

    with mock.patch("shutil.copy"):
        landpage.handle_drop(event)
        assert landpage.file_uploaded is True

def test_welcome_header_present(landpage):
    """Test that the welcome header label is present on the LandPage."""
    header_text = landpage.root.winfo_children()[0].cget("text")
    assert "WELCOME TO SCHEDUAL SYSTEM CREATOR" in header_text

def test_upload_label_text(landpage):
    """Test that the drop label instructs the user to drag a .txt file."""
    assert "drag a .txt file" in landpage.drop_label.cget("text").lower()

def test_file_format_hint_shown(landpage):
    """Test that the label mentions the required .txt file format."""
    assert ".txt" in landpage.drop_label.cget("text")
