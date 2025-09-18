#!/usr/bin/env python3
"""
To-Do List App (Console Based) - Corrected version

Improvements / fixes applied:
- Avoids printing emoji characters (some consoles can raise UnicodeEncodeError).
- Uses explicit UTF-8 when reading/writing the tasks file.
- Handles KeyboardInterrupt / EOFError gracefully.
- Validates input and prevents adding empty tasks.
- Uses Path for file path so tasks.txt is created next to this script.
"""

from pathlib import Path
import sys

TASK_FILE = Path(__file__).parent / "tasks.txt"

def load_tasks():
    try:
        with TASK_FILE.open("r", encoding="utf-8") as f:
            return [line.rstrip("\n") for line in f.readlines()]
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    # Write all tasks with a trailing newline, ensure UTF-8 encoding
    with TASK_FILE.open("w", encoding="utf-8") as f:
        for task in tasks:
            f.write(f"{task}\n")

def show_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.")
    else:
        print("\nYour Tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

def prompt(prompt_text):
    # Wrapper to handle EOFError/KeyboardInterrupt during input
    try:
        return input(prompt_text)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting...")
        sys.exit(0)

def main():
    tasks = load_tasks()

    while True:
        print("\nTo-Do List Menu")
        print("1) Add Task")
        print("2) View Tasks")
        print("3) Remove Task")
        print("4) Exit")

        choice = prompt("Choose an option (1-4): ").strip()

        if choice == "1":
            task = prompt("Enter task: ").strip()
            if not task:
                print("Cannot add an empty task.")
                continue
            tasks.append(task)
            save_tasks(tasks)
            print("Task added.")

        elif choice == "2":
            show_tasks(tasks)

        elif choice == "3":
            show_tasks(tasks)
            if tasks:
                num_str = prompt("Enter task number to remove: ").strip()
                try:
                    num = int(num_str)
                    if 1 <= num <= len(tasks):
                        removed = tasks.pop(num - 1)
                        save_tasks(tasks)
                        print(f"Removed: {removed}")
                    else:
                        print("Invalid task number.")
                except ValueError:
                    print("Please enter a valid integer.")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
