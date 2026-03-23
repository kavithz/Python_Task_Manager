import json
import tkinter as tk
from tkinter import ttk

# Define the Task class to represent each task
class Task:
    def __init__(self, name, description, priority, due_date):
        self.name = name
        self.description = description
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date
        }

# Define the TaskManager class to handle task operations
class TaskManager:
    def __init__(self, json_file='tasks.json'):
        self.tasks = []
        self.json_file = json_file
        self.load_tasks_from_json()

    def load_tasks_from_json(self):
        try:
            with open(self.json_file, 'r') as file:
                data = json.load(file)
                self.tasks = []

                for item in data:
                    if isinstance(item, list):  # Stage 03 list format
                        task = Task(item[0], item[1], item[2], item[3])
                    elif isinstance(item, dict):  # Proper dictionary format
                        task = Task(item.get("name", ""), item.get("description", ""), item.get("priority", ""), item.get("due_date", ""))
                    self.tasks.append(task)

        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def get_filtered_tasks(self, name_filter=None, priority_filter=None, due_date_filter=None):
        filtered = self.tasks
        if name_filter:
            filtered = [t for t in filtered if name_filter.lower() in t.name.lower()]
        if priority_filter:
            filtered = [t for t in filtered if priority_filter.lower() == t.priority.lower()]
        if due_date_filter:
            filtered = [t for t in filtered if due_date_filter == t.due_date]
        return filtered

    def sort_tasks(self, sort_key='name'):
        if sort_key in ['name', 'priority', 'due_date']:
            self.tasks.sort(key=lambda t: getattr(t, sort_key))

# Define the TaskManagerGUI class to create the Tkinter interface
class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Task Manager")
        self.task_manager = TaskManager()
        self.setup_gui()
        self.populate_tree(self.task_manager.tasks)

    def setup_gui(self):
        # Filter section
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Priority:").grid(row=0, column=2)
        self.priority_combo = ttk.Combobox(self.root, values=["", "high", "medium", "low"])
        self.priority_combo.grid(row=0, column=3)

        tk.Label(self.root, text="Due Date (YYYY-MM-DD):").grid(row=0, column=4)
        self.due_date_entry = tk.Entry(self.root)
        self.due_date_entry.grid(row=0, column=5)

        filter_button = tk.Button(self.root, text="Filter", command=self.apply_filter)
        filter_button.grid(row=0, column=6, padx=5)

        # Sort section
        tk.Label(self.root, text="Sort By:").grid(row=1, column=0, padx=5, pady=5)
        self.sort_combo = ttk.Combobox(self.root, values=["name", "priority", "due_date"])
        self.sort_combo.grid(row=1, column=1)

        sort_button = tk.Button(self.root, text="Sort", command=self.apply_sort)
        sort_button.grid(row=1, column=2, padx=5)

        # Treeview table
        columns = ("name", "description", "priority", "due_date")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.capitalize(), command=lambda c=col: self.sort_tasks(c))
            self.tree.column(col, width=150)

        self.tree.grid(row=2, column=0, columnspan=7, padx=10, pady=10)

    def populate_tree(self, task_list):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for task in task_list:
            self.tree.insert("", tk.END, values=(task.name, task.description, task.priority, task.due_date))

    def apply_filter(self):
        name_filter = self.name_entry.get()
        priority_filter = self.priority_combo.get()
        due_date_filter = self.due_date_entry.get()

        filtered_tasks = self.task_manager.get_filtered_tasks(
            name_filter=name_filter,
            priority_filter=priority_filter,
            due_date_filter=due_date_filter
        )
        self.populate_tree(filtered_tasks)

    def apply_sort(self):
        sort_key = self.sort_combo.get()
        if sort_key:
            self.task_manager.sort_tasks(sort_key)
            self.populate_tree(self.task_manager.tasks)

    def sort_tasks(self, sort_key):
        self.task_manager.sort_tasks(sort_key)
        self.populate_tree(self.task_manager.tasks)

# Main program execution
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()

