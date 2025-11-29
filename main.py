import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard
from auto_clicker import AutoClicker


class AutoClickerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KinanClicker - Auto Clicker")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        self.auto_clicker = AutoClicker()
        self.listener = None
        self.update_after_id = None
        
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
            text="▶ START (F6)", 
            command=self.on_start_click
        )
        self.start_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.stop_button = ttk.Button(
            button_frame, 
            text="⏹ STOP (F7)", 
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
        info_text = "F6: Start | F7: Stop | Bekerja di background"
        ttk.Label(info_frame, text=info_text, font=("Arial", 8), foreground="gray").pack()

    def setup_hotkeys(self):
        def on_press(key):
            try:
                if key == keyboard.Key.f6:
                    self.on_start_click()
                elif key == keyboard.Key.f7:
                    self.on_stop_click()
            except AttributeError:
                pass
        
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

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
