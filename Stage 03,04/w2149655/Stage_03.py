import json
import os

# List of dictionaries for tasks
tasks = []

# Functions for CRUD operations

def add_task():
    months_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    task_upload = []

    while True:
        name = input("Enter your task name: ")
        if name:
            task_upload.insert(0, name)
            break
        else:
            print("Please enter a proper task name")

    while True:
        description = input("Enter the task description:").strip()
        if description:
            task_upload.insert(1, description)
            break
        else:
            print("Please enter a proper task description")

    while True:
        priority = input("Enter the priority of the task (high,medium,low): ").strip().lower()
        if priority in ["high", "medium", "low"]:
            task_upload.insert(2, priority)
            break
        else:
            print("Please enter a valid priority level (high,medium,low)")

    while True:
        due_date = input("Enter the task due date in the following format (yyyy-mm-dd): ").strip()
        if len(due_date) == 10 and due_date[4] == '-' and due_date[7] == '-' and due_date.replace('-', '').isdigit():
            try:
                year, month, day = map(int, due_date.split("-"))
                if 1 <= month <= 12 and 1 <= day <= months_list[month - 1]:
                    task_upload.insert(3, due_date)
                    break
                else:
                    print("Invalid day or month. Please enter a proper task due date.")
            except ValueError:
                print("Invalid input. Please enter a proper task due date.")
        else:
            print("Invalid format. Please enter the date in yyyy-mm-dd format with hyphens (-).")

    tasks.append(task_upload)
    save_tasks()
    print("Task added successfully!")

def view_tasks():
    if not tasks:
        print("No tasks available.")
        return
    print("\nTask List:")
    for index, task in enumerate(tasks, start=1):
        print(f"{index}. Name: {task[0]}, Description: {task[1]}, Priority: {task[2]}, Due Date: {task[3]}")

def update_task():
    view_tasks()
    if not tasks:
        return
    try:
        task_number = int(input("Enter the task number to update:")) - 1
        if 0 <= task_number < len(tasks):
            tasks[task_number][0] = input("Enter new task name: ").strip() or tasks[task_number][0]
            tasks[task_number][1] = input("Enter new description: ").strip() or tasks[task_number][1]
            tasks[task_number][2] = input("Enter new priority (high/medium/low): ").strip().lower() or tasks[task_number][2]
            save_tasks()
            print("Task updated successfully!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def delete_task():
    view_tasks()
    if not tasks:
        return
    try:
        task_number = int(input("Enter the task number to delete:")) - 1
        if 0 <= task_number < len(tasks):
            del tasks[task_number]
            save_tasks()
            print("Task deleted successfully!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# JSON file handling functions
def load_tasks_from_json():
    global tasks
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            tasks = json.load(file)

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

if __name__ == "__main__":
    load_tasks_from_json()
# Main function calls to test CRUD
# CRUD functions to work with dictionaries and JSON

    print("Welcome to Task Manager.")
    while True:
        print("""
Options:
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Exit
""")

        try:
            user_input = int(input("Please enter a number for doing any task [1/2/3/4/5]: "))
            if user_input in [1, 2, 3, 4, 5]:
                if user_input == 1:
                    add_task()
                elif user_input == 2:
                    view_tasks()
                elif user_input == 3:
                    update_task()
                elif user_input == 4:
                    delete_task()
                elif user_input == 5:
                    print("Thank you for using the system")
                    break
            else:
                print("Invalid input. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")




