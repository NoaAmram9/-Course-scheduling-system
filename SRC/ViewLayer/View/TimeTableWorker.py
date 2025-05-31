from PyQt5.QtCore import QThread, pyqtSignal
import time

class TimetableWorker(QThread):
    """
    Worker thread for loading timetables in the background
    """
    new_options_available = pyqtSignal(list)  # Emits batch of new timetables
    loading_progress = pyqtSignal(int, int)   # current, total (total=-1 if unknown)
    loading_finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self, controller, file_path1, file_path2, batch_size=50):
        super().__init__()
        self.controller = controller
        self.file_path1 = file_path1
        self.file_path2 = file_path2
        self.batch_size = batch_size
        self._stop_requested = False
        self._paused = False
        self.loaded_count = 0
        
    def run(self):
        """Main worker thread execution"""
        try:
            # Get the batch generator from controller
            batch_generator = self.controller.get_all_options(
                self.file_path1, 
                self.file_path2, 
                batch_size=self.batch_size
            )
            
            batch_count = 0
            for batch in batch_generator:
                # Check if stop was requested
                if self._stop_requested:
                    break
                
                # Handle pause
                while self._paused and not self._stop_requested:
                    self.msleep(100)  # Sleep for 100ms while paused
                
                if self._stop_requested:
                    break
                
                # Process the batch
                if batch:  # Make sure batch is not empty
                    self.loaded_count += len(batch)
                    batch_count += 1
                    
                    # Emit the new batch
                    self.new_options_available.emit(batch)
                    
                    # Emit progress (we don't know total, so use -1)
                    self.loading_progress.emit(self.loaded_count, -1)
                    
                    # Small delay to prevent UI freezing
                    self.msleep(10)
                
            # Emit completion signal
            if not self._stop_requested:
                self.loading_finished.emit()
                
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def stop(self):
        """Request the worker to stop"""
        self._stop_requested = True
    
    def pause(self):
        """Pause the worker"""
        self._paused = True
    
    def resume(self):
        """Resume the worker"""
        self._paused = False