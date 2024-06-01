import logging

import tkinter as tk
import ui

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(message)s", filename="WRSA.log", level=logging.INFO
    )
    logger.info("Starting Wireless Reachability Simulator Application")
    root = tk.Tk()
    app = ui.WirelessReachabilitySimApp(root)
    root.mainloop()
    logger.info("Wireless Reachability Simulator Application Closed")