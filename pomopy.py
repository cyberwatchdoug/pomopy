import time
from datetime import datetime
import pymongo
import sys
import csv
import os

def ascii_timer(minutes, task_name):
    """
    A simple timer that prints a countdown in ASCII art style.
    :param minutes: The number of minutes for the countdown.
    :param task_name: The name of the task being timed.
    """
    for i in range(minutes * 60, 0, -1):
        sys.stdout.write(f"\r{task_name} - Time left: {i // 60}:{i % 60:02d}")
        sys.stdout.flush()
        time.sleep(1)
    print("\nTime's up!")

    # Log to NoSQL database
    log_to_csv(minutes, task_name)

def log_to_nosql(minutes, task_name):
    """
    Logs the task and time to a NoSQL database.
    :param minutes: The number of minutes for the countdown.
    :param task_name: The name of the task being timed.
    """
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["task_timer"]
    collection = db["timers"]

    # Create a log entry
    log_entry = {
        "task_name": task_name,
        "duration_minutes": minutes,
        "timestamp": datetime.now()
    }

    # Insert the log entry into the collection
    collection.insert_one(log_entry)
    print(f"Logged: {log_entry}")

def log_to_csv(minutes, task_name):
    """
    Logs the task and time to a CSV file.
    :param minutes: The number of minutes for the countdown.
    :param task_name: The name of the task being timed.
    """
    log_entry = {
        "task_name": task_name,
        "duration_minutes": minutes,
        "timestamp": datetime.now().isoformat()
    }

    # Define the CSV file name
    csv_file = "task_log.csv"

    # Check if the file exists to write the header
    file_exists = os.path.isfile(csv_file)

    # Write the log entry to the CSV file
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=log_entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)

    print(f"Logged to CSV: {log_entry}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pomopy.py <minutes> <task_name>")
        sys.exit(1)

    try:
        minutes = int(sys.argv[1])
        task_name = sys.argv[2]
        ascii_timer(minutes, task_name)
    except ValueError:
        print("Please provide a valid number of minutes.")
        sys.exit(1)