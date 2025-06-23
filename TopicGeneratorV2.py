import requests
import time
import random
import subprocess
import sys
import importlib.util
from typing import List

# ANSI escape codes for colored text
COLORS = [
    "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m",
    "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m",
    "\033[38;5;208m", "\033[38;5;226m", "\033[38;5;118m", "\033[38;5;21m",
    "\033[38;5;164m", "\033[38;5;196m", "\033[38;5;46m", "\033[38;5;51m",
    "\033[38;5;202m", "\033[38;5;93m", "\033[38;5;160m", "\033[38;5;82m",
    "\033[38;5;178m", "\033[38;5;214m", "\033[38;5;155m", "\033[38;5;112m",
    "\033[38;5;230m", "\033[38;5;120m", "\033[38;5;50m", "\033[38;5;207m",
    "\033[38;5;170m", "\033[38;5;135m", "\033[38;5;184m", "\033[38;5;130m",
    "\033[38;5;172m", "\033[38;5;220m", "\033[38;5;100m", "\033[38;5;25m",
    "\033[38;5;88m", "\033[38;5;58m", "\033[38;5;59m", "\033[38;5;94m",
    "\033[38;5;107m", "\033[38;5;163m", "\033[38;5;203m", "\033[38;5;52m"
]
RESET = "\033[0m"

def check_dependencies(dependencies: List[str]) -> None:
    """Check and install missing Python dependencies."""
    missing = [
        dep for dep in dependencies
        if not importlib.util.find_spec(dep)
    ]

    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Installation failed: {e}")
            sys.exit(1)
    else:
        print("All dependencies are installed.")

def get_wikipedia_topics(limit: int = 20) -> List[str]:
    """Fetch a list of random Wikipedia topics."""
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnlimit={limit}&rnnamespace=0"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [page['title'] for page in data['query']['random']]
    except requests.RequestException as e:
        print(f"Error fetching topics: {e}")
        return []

def print_topics_with_colors(topics: List[str]) -> None:
    """Print topics with colorful flair."""
    for topic in topics:
        color = random.choice(COLORS)
        print(f"{color}{topic}{RESET}")

def main():
    check_dependencies(["requests"])
    try:
        while True:
            topics = get_wikipedia_topics()
            if topics:
                print_topics_with_colors(topics)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
