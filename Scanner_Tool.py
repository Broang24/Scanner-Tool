#!/usr/bin/env python3
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import subprocess
import notify2
import time


# Enter your directory that you want to be watched and scanned when new files or folders enter it.
directory_to_scan = ""
# Define log file directory and name.
log_file = ""
notify2.init("Clamav Scan")


# Event handler
class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            with open(log_file, "a") as file:
                file.write(f"{event.src_path.replace(f"{directory_to_scan}", ".")}/ directory is being scanned...\n")
            result = subprocess.run(["clamscan", "-r", event.src_path], capture_output=True, text=True)
        else:
            with open(log_file, "a") as file:
                file.write(f"{event.src_path.replace(f"{directory_to_scan}", ".")} is being scanned...\n")
            result = subprocess.run(["clamscan", event.src_path], capture_output=True, text=True)

        with open(log_file, "a") as file:
            file.write(f"{result.stdout}")
            file.write(f"{result.stderr}\n")

        if "Infected files: 0" not in result.stdout:
            with open(log_file, "a") as file:
                file.write("Infected File Found!!!")
                file.write("\n"*3)
            notification = notify2.Notification("Virus Was Found!!!", f"A virus was found in the {directory_to_scan} directory!", "dialog-warning")
            notification.set_urgency(notify2.URGENCY_CRITICAL)
            notification.show()
        else:
            with open(log_file, "a") as file:
                file.write("No infected files found.")
                file.write("\n"*3)


# Observer being created, setup and started.
event_handler = EventHandler()
observer = Observer()

observer.schedule(event_handler, directory_to_scan)


with open(log_file, "w") as file:
    file.write("Scanner Starting...")
    file.write("\n"*2)
observer.start()


# An infinite loop so the program runs forever
while True:
    time.sleep(5)
