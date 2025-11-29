import threading
from pynput.mouse import Button, Controller
import time


class AutoClicker:
    def __init__(self):
        self.running = False
        self.paused = False
        self.click_thread = None
        self.interval_ms = 100
        self.click_type = "left"
        self.mouse_controller = Controller()

    def set_interval(self, interval_ms):
        try:
            self.interval_ms = int(interval_ms)
            if self.interval_ms <= 0:
                raise ValueError("Interval harus lebih dari 0")
            return True, f"Interval set ke {self.interval_ms} ms"
        except ValueError:
            return False, "Interval harus berupa angka positif"

    def set_click_type(self, click_type):
        if click_type in ["left", "right"]:
            self.click_type = click_type
            return True
        return False

    def start(self):
        if self.running:
            return False, "Auto clicker sudah berjalan"
        
        self.running = True
        self.click_thread = threading.Thread(target=self._click_loop, daemon=True)
        self.click_thread.start()
        return True, "Auto clicker dimulai"

    def stop(self):
        if not self.running:
            return False, "Auto clicker tidak berjalan"
        
        self.running = False
        if self.click_thread:
            self.click_thread.join(timeout=1)
        return True, "Auto clicker dihentikan"

    def is_running(self):
        return self.running

    def _click_loop(self):
        interval_seconds = self.interval_ms / 1000.0
        
        while self.running:
            try:
                if self.click_type == "left":
                    self.mouse_controller.click(Button.left, 1)
                elif self.click_type == "right":
                    self.mouse_controller.click(Button.right, 1)
                
                time.sleep(interval_seconds)
            except Exception as e:
                print(f"Error saat klik: {e}")
                break
        
        self.running = False
