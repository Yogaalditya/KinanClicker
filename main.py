import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard, mouse
import threading
from auto_clicker import AutoClicker


class AutoClickerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KinanClicker - Auto Clicker")
        self.root.geometry("400x380")
        self.root.resizable(False, False)

        self.auto_clicker = AutoClicker()
        self.listener = None
        self.mouse_listener = None
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
            command=self.open_mode_selection
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
            if isinstance(key, mouse.Button):
                return str(key).replace("Button.", "").upper()
            return str(key).replace("Key.", "").upper()
        except:
            return str(key).upper()

    def setup_hotkeys(self):
        if self.listener:
            try:
                self.listener.stop()
            except:
                pass
        if self.mouse_listener:
            try:
                self.mouse_listener.stop()
            except:
                pass

        def handle_input_press(key):
            try:
                if self.auto_clicker.get_mode() == "toggle":
                    if key == self.hotkey_start:
                        self.root.after_idle(self.on_start_click)
                    elif key == self.hotkey_stop:
                        self.root.after_idle(self.on_stop_click)
                elif self.auto_clicker.get_mode() == "hold":
                    if key == self.hotkey_start:
                        self.root.after_idle(self.on_hold_start)
            except AttributeError:
                pass
            except Exception as e:
                print(f"Input error: {e}")

        def handle_input_release(key):
            try:
                if self.auto_clicker.get_mode() == "hold":
                    if key == self.hotkey_start:
                        self.root.after_idle(self.on_hold_stop)
            except AttributeError:
                pass
            except Exception as e:
                print(f"Input release error: {e}")

        def on_press(key):
            handle_input_press(key)

        def on_release(key):
            handle_input_release(key)

        def on_click(x, y, button, pressed):
            if pressed:
                handle_input_press(button)
            else:
                handle_input_release(button)

        try:
            self.listener = keyboard.Listener(
                on_press=on_press, 
                on_release=on_release,
                suppress=False
            )
            self.listener.start()
            
            self.mouse_listener = mouse.Listener(
                on_click=on_click
            )
            self.mouse_listener.start()
            
            # Start hotkey monitoring thread
            self.start_hotkey_monitor()
        except Exception as e:
            print(f"Failed to start hotkey listener: {e}")
            self.show_fallback_message()

    def open_mode_selection(self):
        """Open mode selection dialog before hotkey settings"""
        mode_window = tk.Toplevel(self.root)
        mode_window.title("Pilih Mode Auto Clicker")
        mode_window.geometry("350x200")
        mode_window.resizable(False, False)
        mode_window.grab_set()

        main_frame = ttk.Frame(mode_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Pilih Mode Auto Clicker", font=("Arial", 12, "bold")).pack(pady=10)

        # Toggle mode button
        toggle_frame = ttk.Frame(main_frame)
        toggle_frame.pack(fill=tk.X, pady=5)
        ttk.Button(
            toggle_frame,
            text="🔄 TOGGLE MODE",
            command=lambda: self.select_mode("toggle", mode_window),
            width=25
        ).pack(fill=tk.X)
        ttk.Label(toggle_frame, text="Tekan sekali untuk start, tekan lagi untuk stop", font=("Arial", 8), foreground="gray").pack(pady=2)

        # Hold mode button
        hold_frame = ttk.Frame(main_frame)
        hold_frame.pack(fill=tk.X, pady=5)
        ttk.Button(
            hold_frame,
            text="⏰ HOLD MODE",
            command=lambda: self.select_mode("hold", mode_window),
            width=25
        ).pack(fill=tk.X)
        ttk.Label(hold_frame, text="Aktif selama tombol ditekan/hold", font=("Arial", 8), foreground="gray").pack(pady=2)

        # Cancel button
        ttk.Button(main_frame, text="Batal", command=mode_window.destroy).pack(pady=10)

    def select_mode(self, mode, mode_window):
        """Select mode and open hotkey settings"""
        self.auto_clicker.set_mode(mode)
        mode_window.destroy()
        self.open_hotkey_settings()

    def open_hotkey_settings(self):
        settings_window = tk.Toplevel(self.root)
        current_mode = self.auto_clicker.get_mode()
        mode_text = "Toggle" if current_mode == "toggle" else "Hold"
        settings_window.title(f"Hotkey Settings - {mode_text} Mode")
        settings_window.geometry("350x300")
        settings_window.resizable(False, False)
        settings_window.grab_set()

        main_frame = ttk.Frame(settings_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text=f"Atur Hotkey - {mode_text} Mode", font=("Arial", 12, "bold")).pack(pady=10)

        if current_mode == "toggle":
            # Toggle mode - show both start and stop hotkeys
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
        else:
            # Hold mode - only show hold key
            hold_frame = ttk.Frame(main_frame)
            hold_frame.pack(fill=tk.X, pady=10)
            ttk.Label(hold_frame, text="Hotkey Hold:", width=15).pack(side=tk.LEFT)
            self.start_key_label = ttk.Label(
                hold_frame,
                text=self.get_key_name(self.hotkey_start),
                font=("Arial", 10, "bold"),
                foreground="blue",
                width=15
            )
            self.start_key_label.pack(side=tk.LEFT, padx=5)
            ttk.Button(hold_frame, text="Ganti", command=lambda: self.capture_hotkey("start", self.start_key_label)).pack(side=tk.LEFT, padx=5)

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
        
        # Define listeners first so we can refer to them in handle_capture
        # We use a mutable container for listeners to access them inside closure if needed, 
        # but since we define them before starting, we can just use local variables if we are careful.
        # However, handle_capture is called by listeners, so we need to be careful about scope.
        # Using a class or simple object to hold listeners might be safer, or just rely on closure.
        
        listeners = {'keyboard': None, 'mouse': None}

        def handle_capture(key):
            try:
                captured_key[0] = key
                status_label.config(text=f"Tombol: {self.get_key_name(key)}", foreground="green")
                
                # Stop listeners
                if listeners['keyboard']: listeners['keyboard'].stop()
                if listeners['mouse']: listeners['mouse'].stop()
                
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

        def on_press(key):
            handle_capture(key)
            return False

        def on_click(x, y, button, pressed):
            if pressed:
                handle_capture(button)
                return False

        listeners['keyboard'] = keyboard.Listener(on_press=on_press)
        listeners['keyboard'].start()
        
        listeners['mouse'] = mouse.Listener(on_click=on_click)
        listeners['mouse'].start()

        def on_window_close():
            try:
                if listeners['keyboard']: listeners['keyboard'].stop()
                if listeners['mouse']: listeners['mouse'].stop()
            except:
                pass
            capture_window.destroy()

        capture_window.protocol("WM_DELETE_WINDOW", on_window_close)

    def start_hotkey_monitor(self):
        """Monitor hotkey listener and restart if it fails"""
        def monitor_loop():
            import time
            while hasattr(self, 'root') and self.root.winfo_exists():
                try:
                    if (self.listener and not self.listener.running) or \
                       (self.mouse_listener and not self.mouse_listener.running):
                        print("Hotkey listener died, restarting...")
                        self.setup_hotkeys()
                        break
                    time.sleep(2)
                except Exception as e:
                    print(f"Monitor error: {e}")
                    break
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()

    def show_fallback_message(self):
        """Show message when hotkeys fail"""
        messagebox.showwarning(
            "Hotkey Warning", 
            "Hotkey mungkin tidak berfungsi dengan beberapa aplikasi/game.\n"
            "Gunakan tombol START/STOP di interface jika hotkey tidak responsif."
        )

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

    def on_hold_start(self):
        """Handle hold mode start"""
        if self.auto_clicker.get_mode() != "hold":
            return
        
        interval_text = self.interval_input.get()
        success, message = self.auto_clicker.set_interval(interval_text)
        if not success:
            messagebox.showerror("Error", message)
            return

        success, message = self.auto_clicker.start_hold()
        if success:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.interval_input.config(state=tk.DISABLED)

    def on_hold_stop(self):
        """Handle hold mode stop"""
        if self.auto_clicker.get_mode() != "hold":
            return
        
        success, message = self.auto_clicker.stop_hold()
        if success:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.interval_input.config(state=tk.NORMAL)

    def on_click_type_change(self, event=None):
        click_type = self.click_type_var.get()
        self.auto_clicker.set_click_type(click_type)

    def update_status(self):
        if self.auto_clicker.get_mode() == "hold":
            if self.auto_clicker.is_hold_active():
                self.status_label.config(text="🟢 HOLD ACTIVE", foreground="green")
            else:
                self.status_label.config(text="🔴 HOLD READY", foreground="orange")
        else:
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
