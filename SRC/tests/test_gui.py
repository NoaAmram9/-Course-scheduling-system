import unittest
from unittest.mock import patch
import os
from SRC.ViewLayer.gui import GUI

@patch('tkinter.messagebox.showinfo')
@patch('tkinter.filedialog.askopenfilename')
@patch('shutil.copy')
def test_load_file(mock_copy, mock_filedialog, mock_showinfo):
    mock_filedialog.return_value = 'fake_path.txt'
    mock_copy.return_value = None

    gui = GUI(None)
    gui.load_file()

    expected_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'courses.txt')
    )

    actual_dst = os.path.normpath(mock_copy.call_args[0][1])
    assert mock_copy.call_args[0][0] == 'fake_path.txt'
    assert actual_dst == expected_path

    msgbox_args = mock_showinfo.call_args[0]
    actual_message_path = os.path.normpath(msgbox_args[1].split('\n')[-1])

    assert msgbox_args[0] == "Success"
    assert actual_message_path == expected_path