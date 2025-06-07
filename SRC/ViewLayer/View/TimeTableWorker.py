from PyQt5.QtCore import QThread, pyqtSignal
import time

class TimetableWorker(QThread):
    """
    This class runs in the background and loads timetable options without freezing the app.
    It works in a separate thread, so the GUI stays responsive.
    """

    # These are "signals" that the thread can send to the main program (the GUI)
    new_options_available = pyqtSignal(list)  # Sends a list of new timetables
    loading_progress = pyqtSignal(int, int)   # Tells how many have loaded so far (current, total)
    loading_finished = pyqtSignal()           # Says "we're done loading!"
    error_occurred = pyqtSignal(str)          # Sends an error message if something goes wrong

    def __init__(self, controller, file_path1, file_path2, batch_size=50):
        super().__init__()
        self.controller = controller          # The logic/controller part of your app
        self.file_path1 = file_path1          # Path to the first input file
        self.file_path2 = file_path2          # Path to the second input file
        self.batch_size = batch_size          # How many results to send at a time
        self._stop_requested = False          # If True, the thread should stop
        self._paused = False                  # If True, the thread should pause
        self.loaded_count = 0                 # How many timetables were loaded so far
        print(f"TimetableWorker initialized with files: {file_path1}, {file_path2} and batch size: {batch_size}")
    def run(self):
        """This is what runs when you start the thread."""
        try:
            # Get a generator that gives us batches of timetables
            batch_generator = self.controller.get_all_options(
                self.file_path1, 
                self.file_path2, 
                batch_size=self.batch_size
            )

            batch_count = 0
            for batch in batch_generator:
                # Stop the thread if requested
                if self._stop_requested:
                    break

                # Wait here if paused
                while self._paused and not self._stop_requested:
                    self.msleep(100)  # Wait 100ms before checking again

                if self._stop_requested:
                    break

                if batch:  # If the batch is not empty
                    self.loaded_count += len(batch)
                    batch_count += 1

                    # Let the GUI know we got new data
                    self.new_options_available.emit(batch)

                    # Let the GUI know how much we've done
                    self.loading_progress.emit(self.loaded_count, -1)  # -1 means we don't know total

                    # Small sleep so the GUI doesn’t freeze
                    self.msleep(10)

            # If we finished normally (no stop requested), tell the GUI we’re done
            if not self._stop_requested:
                self.loading_finished.emit()

        except Exception as e:
            # If an error happened, let the GUI know
            self.error_occurred.emit(str(e))

    def stop(self):
        """Call this if you want to stop the thread."""
        self._stop_requested = True

    def pause(self):
        """Call this to pause the thread."""
        self._paused = True

    def resume(self):
        """Call this to continue after pause."""
        self._paused = False
