import logging

import tkinter as tk
from tkinter import filedialog, messagebox

from configuration import Configuration
from simentry import run_through_configuration

logger = logging.getLogger(__name__)

class WirelessReachabilitySimApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wireless Reachability Simulator!")
        # self.root.geometry("350x150")
        self.root.minsize(400, 480)

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
        self.spacer = tk.Label(
            root, text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
        )
        self.spacer.pack(pady=5)

        # Listbox (list view)
        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=5)

        # Labels and Spinbox for 'from' and 'to'
        self.from_label = tk.Label(root, text="From:")
        self.from_label.pack(pady=5)
        self.from_spinbox = tk.Spinbox(root, from_=1, to=5, width=5, state=tk.DISABLED)
        self.from_spinbox.pack(pady=5)

        self.to_label = tk.Label(root, text="To:")
        self.to_label.pack(pady=5)
        strvar = tk.StringVar()
        strvar.set("2")
        self.to_spinbox = tk.Spinbox(
            root, from_=1, to=5, width=5, textvariable=strvar, state=tk.DISABLED
        )
        self.to_spinbox.pack(pady=5)

        logger.info("UI Inflated")

        self.config = Configuration()

    def add_spinboxes(self, from_, to_):
        logger.info("Spinboxes added with ranges: %d to %d", from_, to_)
        self.from_spinbox.config(from_=from_, to=to_)
        self.to_spinbox.config(from_=from_, to=to_)
        self.from_spinbox.config(state=tk.NORMAL)
        self.to_spinbox.config(state=tk.NORMAL)

    def populate_listbox(self, items):
        logging.info("Populating Listbox with items: %s", items)
        self.add_spinboxes(1, len(items))
        for i, item in enumerate(items):
            self.listbox.insert(tk.END, f"{i+1}. {item}")

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
                logging.info("Config file loaded: %s", config_file_path)
                # Populate Listbox with example items
                self.populate_listbox(self.config.equipment)
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
            logging.warn("Simulation run attempted with no config file loaded")
        else:
            # messagebox.showinfo("Info", f"Running simulation with config file: {config_file}")
            from_, to_ = (
                int(self.from_spinbox.get()) - 1,
                int(self.to_spinbox.get()) - 1,
            )
            run_through_configuration(self.config, from_, to_)
