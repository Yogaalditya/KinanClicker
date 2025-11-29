import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard
from auto_clicker import AutoClicker


class AutoClickerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KinanClicker - Auto Clicker")
        self.root.geometry("400x380")
        self.root.resizable(False, False)

        self.auto_clicker = AutoClicker()
        self.listener = None
        self.update_after_id = None
        self.hotkey_start = keyboard.Key.f6
        self.hotkey_stop = keyboard.Key.f7

        self.setup_ui()
        self.setup_hotkeys()
        self.update_status()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="⚙️ AUTO CLICKER SETTINGS", font=("Arial", 12, "bold")).pack(pady=10)

        interval_frame = ttk.Frame(main_frame)
        interval_frame.pack(fill=tk.X, pady=10)
        ttk.Label(interval_frame, text="Interval (ms):", width=15).pack(side=tk.LEFT)
        self.interval_input = ttk.Entry(interval_frame, width=15)
        self.interval_input.insert(0, "100")
        self.interval_input.pack(side=tk.LEFT, padx=5)

        click_type_frame = ttk.Frame(main_frame)
        click_type_frame.pack(fill=tk.X, pady=10)
        ttk.Label(click_type_frame, text="Jenis Klik:", width=15).pack(side=tk.LEFT)
        self.click_type_var = tk.StringVar(value="left")
        click_dropdown = ttk.Combobox(
            click_type_frame,
            textvariable=self.click_type_var,
            values=["left", "right"],
            state="readonly",
            width=12
        )
        click_dropdown.pack(side=tk.LEFT, padx=5)
        click_dropdown.bind("<<ComboboxSelected>>", self.on_click_type_change)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)

        self.start_button = ttk.Button(
            button_frame,
            text="▶ START",
            command=self.on_start_click
        )
        self.start_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.stop_button = ttk.Button(
            button_frame,
            text="⏹ STOP",
            command=self.on_stop_click,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=20)
        ttk.Label(status_frame, text="Status:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.status_label = ttk.Label(
            status_frame,
            text="🔴 STOPPED",
            font=("Arial", 10, "bold"),
            foreground="red"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=10)
        self.info_text = ttk.Label(info_frame, font=("Arial", 8), foreground="gray")
        self.info_text.pack()
        self.update_info_text()

        hotkey_button_frame = ttk.Frame(main_frame)
        hotkey_button_frame.pack(fill=tk.X, pady=5)
        self.hotkey_settings_button = ttk.Button(
            hotkey_button_frame,
            text="🔧 HOTKEY SETTINGS",
            command=self.open_hotkey_settings
        )
        self.hotkey_settings_button.pack(fill=tk.X)

    def update_info_text(self):
        start_key = self.get_key_name(self.hotkey_start)
        stop_key = self.get_key_name(self.hotkey_stop)
        info_text = f"{start_key}: Start | {stop_key}: Stop | Bekerja di background"
        self.info_text.config(text=info_text)

    def get_key_name(self, key):
        try:
            if hasattr(key, 'name'):
                return key.name.upper()
            return str(key).replace("Key.", "").upper()
        except:
            return str(key).upper()

    def setup_hotkeys(self):
        if self.listener:
            try:
                self.listener.stop()
            except:
                pass

        def on_press(key):
            try:
                if key == self.hotkey_start:
                    self.on_start_click()
                elif key == self.hotkey_stop:
                    self.on_stop_click()
            except AttributeError:
                pass

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def open_hotkey_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Hotkey Settings")
        settings_window.geometry("350x250")
        settings_window.resizable(False, False)
        settings_window.grab_set()

        main_frame = ttk.Frame(settings_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Atur Hotkey", font=("Arial", 12, "bold")).pack(pady=10)

        start_frame = ttk.Frame(main_frame)
        start_frame.pack(fill=tk.X, pady=10)
        ttk.Label(start_frame, text="Hotkey Start:", width=15).pack(side=tk.LEFT)
        self.start_key_label = ttk.Label(
            start_frame,
            text=self.get_key_name(self.hotkey_start),
            font=("Arial", 10, "bold"),
            foreground="blue",
            width=15
        )
        self.start_key_label.pack(side=tk.LEFT, padx=5)
        ttk.Button(start_frame, text="Ganti", command=lambda: self.capture_hotkey("start", self.start_key_label)).pack(side=tk.LEFT, padx=5)

        stop_frame = ttk.Frame(main_frame)
        stop_frame.pack(fill=tk.X, pady=10)
        ttk.Label(stop_frame, text="Hotkey Stop:", width=15).pack(side=tk.LEFT)
        self.stop_key_label = ttk.Label(
            stop_frame,
            text=self.get_key_name(self.hotkey_stop),
            font=("Arial", 10, "bold"),
            foreground="blue",
            width=15
        )
        self.stop_key_label.pack(side=tk.LEFT, padx=5)
        ttk.Button(stop_frame, text="Ganti", command=lambda: self.capture_hotkey("stop", self.stop_key_label)).pack(side=tk.LEFT, padx=5)

        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=15)
        ttk.Label(info_frame, text="Klik tombol 'Ganti' lalu tekan tombol yang diinginkan", font=("Arial", 9), foreground="gray", wraplength=300, justify=tk.LEFT).pack()

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Tutup", command=settings_window.destroy).pack(fill=tk.X)

    def capture_hotkey(self, hotkey_type, label_widget):
        capture_window = tk.Toplevel(self.root)
        capture_window.title("Capture Hotkey")
        capture_window.geometry("300x150")
        capture_window.resizable(False, False)
        capture_window.grab_set()

        main_frame = ttk.Frame(capture_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Tekan tombol yang diinginkan...", font=("Arial", 11, "bold")).pack(pady=20)

        status_label = ttk.Label(main_frame, text="Menunggu input...", font=("Arial", 10), foreground="orange")
        status_label.pack(pady=10)

        captured_key = [None]

        def on_press(key):
            try:
                captured_key[0] = key
                status_label.config(text=f"Tombol: {self.get_key_name(key)}", foreground="green")
                self.root.after(500, lambda: capture_window.destroy())

                if hotkey_type == "start":
                    self.hotkey_start = key
                    label_widget.config(text=self.get_key_name(key))
                else:
                    self.hotkey_stop = key
                    label_widget.config(text=self.get_key_name(key))

                self.setup_hotkeys()
                self.update_info_text()

                return False
            except Exception as e:
                status_label.config(text=f"Error: {str(e)}", foreground="red")

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        def on_window_close():
            try:
                listener.stop()
            except:
                pass
            capture_window.destroy()

        capture_window.protocol("WM_DELETE_WINDOW", on_window_close)

    def on_start_click(self):
        interval_text = self.interval_input.get()

        success, message = self.auto_clicker.set_interval(interval_text)
        if not success:
            messagebox.showerror("Error", message)
            return

        success, message = self.auto_clicker.start()
        if success:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.interval_input.config(state=tk.DISABLED)
            self.update_status()
        else:
            messagebox.showwarning("Warning", message)

    def on_stop_click(self):
        success, message = self.auto_clicker.stop()
        if success:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.interval_input.config(state=tk.NORMAL)
            self.update_status()
        else:
            messagebox.showwarning("Warning", message)

    def on_click_type_change(self, event=None):
        click_type = self.click_type_var.get()
        self.auto_clicker.set_click_type(click_type)

    def update_status(self):
        if self.auto_clicker.is_running():
            self.status_label.config(text="🟢 RUNNING", foreground="green")
        else:
            self.status_label.config(text="🔴 STOPPED", foreground="red")

        self.update_after_id = self.root.after(500, self.update_status)

    def on_closing(self):
        if self.update_after_id:
            self.root.after_cancel(self.update_after_id)

        try:
            if self.listener:
                self.listener.stop()
        except:
            pass

        if self.auto_clicker.is_running():
            self.auto_clicker.stop()

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
