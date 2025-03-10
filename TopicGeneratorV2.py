import requests
import time
import random
import subprocess
import sys

# ANSI escape codes for colored text
COLORS = [
    "\033[31m",  # Red
    "\033[32m",  # Green
    "\033[33m",  # Yellow
    "\033[34m",  # Blue
    "\033[35m",  # Magenta
    "\033[36m",  # Cyan
    "\033[91m",  # Bright Red
    "\033[92m",  # Bright Green
    "\033[93m",  # Bright Yellow
    "\033[94m",  # Bright Blue
    "\033[95m",  # Bright Magenta
    "\033[96m",  # Bright Cyan
    "\033[38;5;208m",  # Orange
    "\033[38;5;226m",  # Bright Yellow 2
    "\033[38;5;118m",  # Lime Green
    "\033[38;5;21m",  # Teal
    "\033[38;5;164m",  # Violet
    "\033[38;5;196m",  # Pink
    "\033[38;5;46m",  # Olive Green
    "\033[38;5;51m",  # Sky Blue
    "\033[38;5;202m",  # Gold
    "\033[38;5;93m",  # Brown
    "\033[38;5;160m",  # Purple
    "\033[38;5;82m",  # Sea Green
    "\033[38;5;178m",  # Light Purple
    "\033[38;5;214m",  # Light Orange
    "\033[38;5;155m",  # Light Pink
    "\033[38;5;112m",  # Gray/Silver
    "\033[38;5;230m",  # Light Yellow
    "\033[38;5;120m",  # Light Green 2
    "\033[38;5;50m",  # Light Blue 2
    "\033[38;5;207m",  # Light Red
    "\033[38;5;170m",  # Turquoise
    "\033[38;5;135m",  # Coral
    "\033[38;5;184m",  # Lavender
    "\033[38;5;130m",  # Khaki
    "\033[38;5;172m",  # Beige
    "\033[38;5;220m",  # Light Brown
    "\033[38;5;100m",  # Dark Green
    "\033[38;5;25m",  # Dark Blue
    "\033[38;5;88m",  # Dark Red
    "\033[38;5;58m",  # Dark Magenta
    "\033[38;5;59m",  # Dark Cyan
    "\033[38;5;94m",  # Dark Yellow/Gold
    "\033[38;5;107m",  # Dark Orange/Brown
    "\033[38;5;163m",  # Dark Purple/Violet
    "\033[38;5;203m",  # Dark Pink/Magenta
    "\033[38;5;52m",  # Dark Teal/Cyan
]
RESET = "\033[0m"  # Reset to default color

def check_dependencies(dependencies):
    """Checks and installs dependencies."""
    missing_dependencies = []
    for dependency in dependencies:
        try:
            __import__(dependency)
        except ImportError:
            missing_dependencies.append(dependency)

    if missing_dependencies:
        print(f"Missing dependencies: {', '.join(missing_dependencies)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_dependencies])
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            input("Press Enter to exit...")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred during dependency installation: {e}")
            input("Press Enter to exit...")
            sys.exit(1)
    else:
        print("All dependencies are installed.")

def get_wikipedia_topics(limit=20):
    """Retrieves a list of random Wikipedia topics using the API."""
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnlimit={limit}&rnnamespace=0"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        topics = [page['title'] for page in data['query']['random']]
        return topics
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Wikipedia topics: {e}")
        return []

def print_topics_with_colors(topics):
    """Prints topics with random colors."""
    for topic in topics:
        color = random.choice(COLORS)
        print(f"{color}{topic}{RESET}")

def main():
    dependencies = ["requests"]
    check_dependencies(dependencies)

    try:
        while True:
            topics = get_wikipedia_topics()
            if topics:
                print_topics_with_colors(topics)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
