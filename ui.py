import tkinter as tk
from tkinter import filedialog, messagebox

from configuration import Configuration
from simentry import run_through_configuration


class WirelessReachabilitySimApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wireless Reachability Simulator!")
        self.root.geometry("350x150")

        self.config_name = tk.StringVar()
        self.config_name.set("No config file loaded")

        # Load Config Button
        self.load_button = tk.Button(
            root, text="Load Config File", command=self.load_config
        )
        self.load_button.pack(pady=17)

        # Label to display current config name
        self.config_label = tk.Label(root, textvariable=self.config_name)
        self.config_label.pack(pady=5)

        # Run Simulation Button
        self.run_button = tk.Button(
            root, text="Run Simulation", command=self.run_simulation, state=tk.DISABLED
        )
        self.run_button.pack(pady=5)

        # Spacer
        # self.spacer = tk.Label(root, text="------------------------")
        # self.spacer.pack(pady=5)

        # # Text space (read-only and not wide)
        # self.text_space = tk.Text(root, height=10, width=40, state=tk.DISABLED)
        # self.text_space.pack(pady=5)

        self.config = Configuration()

    def load_config(self):
        config_file_path = filedialog.askopenfilename(
            initialdir=".",
            title="Select Config File",
            filetypes=[("CSV Files", "*.csv")],
        )
        if config_file_path:
            self.config_name.set(config_file_path.split("/")[-1])
            try:
                self.config.load(config_file_path)
                self.run_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading config file: {e}")
        else:
            self.config_name.set("No config file loaded")

    def run_simulation(self):
        config_file = self.config_name.get()
        if config_file == "No config file loaded":
            messagebox.showwarning(
                "Warning", "Please load a config file before running the simulation."
            )
        else:
            # messagebox.showinfo("Info", f"Running simulation with config file: {config_file}")
            run_through_configuration(self.config)
