import pytest
from unittest import mock
import os
import shutil
from SRC.Models.ValidationError import ValidationError 
from SRC.ViewLayer.LandPage import LandPage
import tkinter as tk
import tkinterdnd2 as TkinterDnD

# Mock drag-and-drop globally for all tests where it is not needed
@pytest.fixture(autouse=True)
def mock_drag_and_drop():
    with mock.patch("tkinterdnd2.Tk.drop_target_register", return_value=None):
        yield

@pytest.fixture
def landpage(tmp_path):
    with mock.patch("customtkinter.CTkFrame.drop_target_register", create=True):
        try:
            root = TkinterDnD.Tk()
        except tk.TclError:
            root = tk.Tk()

        controller = mock.Mock()
        page = LandPage(root, controller)
        return page


# --- 1. Upload a valid .txt file via dialog ---
def test_upload_via_dialog_txt_file(tmp_path, landpage):
    file_path = tmp_path / "courses.txt"
    file_path.write_text("course_id, name")

    with mock.patch("tkinter.filedialog.askopenfilename", return_value=str(file_path)), \
         mock.patch("shutil.copy") as mock_copy:
        landpage.upload_file()
        mock_copy.assert_called_once()
        assert landpage.file_uploaded is True
        assert "Uploaded:" in landpage.file_label.cget("text")


# --- 2. Upload a valid .txt file via drag-and-drop ---
def test_upload_via_drag_and_drop_valid_txt(tmp_path, landpage):
    file_path = tmp_path / "courses.txt"
    file_path.write_text("course_id,name")

    event = mock.Mock()
    event.data = f"{{{file_path}}}"  # simulate drag-and-drop path with braces

    with mock.patch("shutil.copy") as mock_copy:
        landpage.handle_drop(event)
        mock_copy.assert_called_once()
        assert landpage.file_uploaded is True
        assert "Uploaded:" in landpage.file_label.cget("text")


# --- 3. Reject invalid file type via drag-and-drop ---
def test_reject_invalid_file_type(landpage):
    event = mock.Mock()
    event.data = "{bad_file.pdf}"

    with mock.patch("tkinter.messagebox.showerror") as mock_error:
        landpage.handle_drop(event)
        mock_error.assert_called_once_with("Invalid file", "Only .txt files are allowed.")
        assert landpage.file_uploaded is False


# --- 4. Show file name in label after upload ---
def test_file_label_updates_correctly(tmp_path, landpage):
    file_path = tmp_path / "courses.txt"
    file_path.write_text("test data")

    with mock.patch("tkinter.filedialog.askopenfilename", return_value=str(file_path)), \
         mock.patch("shutil.copy"):
        landpage.upload_file()
        assert landpage.file_label.cget("text") == f"Uploaded: {file_path.name}"


# --- 5. SEND button shows warning if no file uploaded ---
def test_send_action_blocks_without_file(landpage):
    landpage.file_uploaded = False

    with mock.patch("tkinter.messagebox.showwarning") as mock_warn:
        landpage.send_action()
        mock_warn.assert_called_once_with("Missing File", "Please upload a .txt file before proceeding.")


# --- 6. SEND button proceeds only if file uploaded ---
def test_send_action_launches_main_page_if_uploaded(landpage):
    landpage.file_uploaded = True
    landpage.root = mock.Mock()

    # Simulate successful processing (not all are ValidationErrors)
    landpage.controller = mock.Mock()
    landpage.controller.process_repository_file.return_value = ["OK"]

    with mock.patch("SRC.ViewLayer.LandPage.MainPage") as MockMainPage:
        instance = MockMainPage.return_value
        landpage.send_action()
        landpage.root.withdraw.assert_called_once()
        instance.run.assert_called_once()

# --- 7. Data directory is created if missing ---
def test_upload_creates_data_directory(tmp_path, landpage):
    file_path = tmp_path / "courses.txt"
    file_path.write_text("abc")

    with mock.patch("tkinter.filedialog.askopenfilename", return_value=str(file_path)), \
         mock.patch("shutil.copy"), \
         mock.patch("os.makedirs") as mock_makedirs:

        landpage.upload_file()

        # Capture the actual path used
        called_path, kwargs = mock_makedirs.call_args

        # It should end with 'Data'
        assert called_path[0].endswith("Data")
        assert kwargs == {"exist_ok": True}


# --- 8. No crash if file dialog is canceled ---
def test_upload_file_dialog_cancel_does_nothing(landpage):
    with mock.patch("tkinter.filedialog.askopenfilename", return_value=""):
        landpage.upload_file()
        assert landpage.file_uploaded is False


# --- 9. Normalize drag path with spaces or braces ---
def test_handle_drop_path_with_spaces(tmp_path, landpage):
    file_path = tmp_path / "my courses file.txt"
    file_path.write_text("data")
    event = mock.Mock()
    event.data = f"{{{file_path}}}"  # simulate drop with curly braces

    with mock.patch("shutil.copy"):
        landpage.handle_drop(event)
        assert landpage.file_uploaded is True

# --- 10. Check if welcome header is present ---
def test_welcome_header_present(landpage):
    header_text = landpage.root.winfo_children()[0].cget("text")
    assert "WELCOME TO SCHEDUAL SYSTEM CREATOR" in header_text


# --- 11. Check if upload label text is correct ---
def test_upload_label_text(landpage):
    assert "drag a .txt file" in landpage.drop_label.cget("text").lower()


# --- 12. Check if file format hint is shown ---
def test_file_format_hint_shown(landpage):
    assert ".txt" in landpage.drop_label.cget("text")