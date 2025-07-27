import requests
import time
import random
import threading
import importlib.util
import subprocess
import sys
from tkinter import Tk, Label, Frame, Text, Scrollbar, LEFT, RIGHT, BOTH, Y, END
from typing import List

COLORS = [
    "red", "green", "blue", "purple", "orange", "cyan",
    "magenta", "gold", "deep sky blue", "lime green",
    "crimson", "dark orange", "orchid", "turquoise", "salmon"
]

def check_dependencies(dependencies: List[str]) -> None:
    missing = [dep for dep in dependencies if not importlib.util.find_spec(dep)]
    if missing:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])

def get_wikipedia_topics(limit: int = 10) -> List[str]:
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnlimit={limit}&rnnamespace=0"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [item["title"] for item in data["query"]["random"]]
    except requests.RequestException as e:
        return [f"Error: {e}"]

def update_content(topic_box: Text, log_box: Text) -> None:
    topics = get_wikipedia_topics()
    timestamp = time.strftime("%H:%M:%S")
    log_text = f"[{timestamp}] Request sent — Received {len(topics)} topics\n"
    log_box.insert(END, log_text)
    log_box.see(END)

    for topic in topics:
        color = random.choice(COLORS)
        topic_box.insert(END, f"{topic}\n", color)
        topic_box.tag_config(color, foreground=color)
    topic_box.see(END)

def refresh_loop(topic_box: Text, log_box: Text) -> None:
    def loop():
        while True:
            update_content(topic_box, log_box)
            time.sleep(3)
    threading.Thread(target=loop, daemon=True).start()

def create_gui():
    root = Tk()
    root.title("Wikipedia Random Topics")
    root.geometry("800x700")
    root.configure(bg="black")

    # Left panel (topics)
    left_frame = Frame(root, width=400, bg="black")
    left_frame.pack(side=LEFT, fill=BOTH, expand=True)

    branding = Label(left_frame, text="Sponsored by Wikipedia", font=("Helvetica", 14, "bold"),
                     fg="white", bg="black", anchor="w", justify=LEFT)
    branding.pack(pady=(10, 0), anchor="w")

    topic_container = Frame(left_frame, bg="black")
    topic_container.pack(fill=BOTH, expand=True, padx=10, pady=5)

    topic_box = Text(topic_container, bg="black", fg="white", font=("Helvetica", 11), wrap="word")
    topic_box.pack(side=LEFT, fill=BOTH, expand=True)

    topic_scroll = Scrollbar(topic_container, command=topic_box.yview)
    topic_scroll.pack(side=RIGHT, fill=Y)
    topic_box.config(yscrollcommand=topic_scroll.set)

    # Right panel (logs)
    right_frame = Frame(root, width=400, bg="black")
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    log_title = Label(right_frame, text="API Logs", font=("Helvetica", 12, "bold"), fg="white", bg="black")
    log_title.pack(pady=(10, 0), anchor="w")

    log_container = Frame(right_frame, bg="black")
    log_container.pack(fill=BOTH, expand=True, padx=10, pady=5)

    log_box = Text(log_container, bg="black", fg="lime", font=("Courier", 10), wrap="none", height=10)
    log_box.pack(side=LEFT, fill=BOTH, expand=True)

    log_scroll = Scrollbar(log_container, command=log_box.yview)
    log_scroll.pack(side=RIGHT, fill=Y)
    log_box.config(yscrollcommand=log_scroll.set)

    refresh_loop(topic_box, log_box)
    root.mainloop()

if __name__ == "__main__":
    check_dependencies(["requests"])
    create_gui()
