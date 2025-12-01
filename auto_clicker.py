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
        self.mode = "toggle"  # "toggle" or "hold"
        self.hold_active = False

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

    def set_mode(self, mode):
        if mode in ["toggle", "hold"]:
            self.mode = mode
            return True
        return False

    def get_mode(self):
        return self.mode

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

    def force_stop(self):
        """Force stop the auto clicker even if thread is stuck"""
        self.running = False
        return True, "Auto clicker dipaksa berhenti"

    def is_running(self):
        return self.running

    def start_hold(self):
        """Start hold mode clicking"""
        if self.mode != "hold":
            return False, "Mode bukan hold"
        
        if self.hold_active:
            return False, "Hold mode sudah aktif"
        
        self.hold_active = True
        self.running = True
        self.click_thread = threading.Thread(target=self._hold_click_loop, daemon=True)
        self.click_thread.start()
        return True, "Hold mode dimulai"

    def stop_hold(self):
        """Stop hold mode clicking"""
        if self.mode != "hold":
            return False, "Mode bukan hold"
        
        if not self.hold_active:
            return False, "Hold mode tidak aktif"
        
        self.hold_active = False
        self.running = False
        if self.click_thread:
            self.click_thread.join(timeout=1)
        return True, "Hold mode dihentikan"

    def is_hold_active(self):
        return self.hold_active and self.mode == "hold"

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

    def _hold_click_loop(self):
        """Click loop for hold mode"""
        interval_seconds = self.interval_ms / 1000.0
        
        while self.hold_active and self.running:
            try:
                if self.click_type == "left":
                    self.mouse_controller.click(Button.left, 1)
                elif self.click_type == "right":
                    self.mouse_controller.click(Button.right, 1)
                
                time.sleep(interval_seconds)
            except Exception as e:
                print(f"Error saat klik hold: {e}")
                break
        
        self.hold_active = False
        self.running = False
