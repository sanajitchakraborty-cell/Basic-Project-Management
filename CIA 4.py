import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt


# ===============================
# 🧱 Class: ProjectTask
# ===============================
class ProjectTask:
    def _init_(self, task_id, name, estimated_hours):
        self.task_id = task_id
        self.name = name
        self.estimated_hours = estimated_hours
        self.spent_hours = 0
        self.status = "Not Started"

    def update_hours(self, hours):
        """Update hours spent and change task status accordingly."""
        self.spent_hours += hours
        if self.spent_hours == 0:
            self.status = "Not Started"
        elif self.spent_hours < self.estimated_hours:
            self.status = "In Progress"
        else:
            self.status = "Completed"


# ===============================
# 🧱 Class: ProjectManager
# ===============================
class ProjectManager:
    def _init_(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def find_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def task_report(self):
        """Return a list of all tasks with details."""
        report = []
        for task in self.tasks:
            report.append({
                "Task ID": task.task_id,
                "Name": task.name,
                "Estimated Hours": task.estimated_hours,
                "Spent Hours": task.spent_hours,
                "Status": task.status
            })
        return report

    def project_completion_rate(self):
        """Calculate percentage of tasks completed."""
        if not self.tasks:
            return 0
        completed = sum(1 for t in self.tasks if t.status == "Completed")
        return (completed / len(self.tasks)) * 100


# ===============================
# 🎨 GUI Section
# ===============================
pm = ProjectManager()

root = tk.Tk()
root.title("🌸 Project Task Management System 🌸")
root.geometry("600x600")
root.configure(bg="#f9f2ff")


# ===============================
# 🧾 Helper Functions
# ===============================
def add_task():
    """Add a new task to the project manager."""
    try:
        task_id = entry_id.get().strip()
        name = entry_name.get().strip()
        hours = float(entry_hours.get().strip())

        if not task_id or not name:
            messagebox.showerror("Error", "Please fill all fields!")
            return

        if pm.find_task(task_id):
            messagebox.showerror("Error", "Task ID already exists!")
            return

        task = ProjectTask(task_id, name, hours)
        pm.add_task(task)
        messagebox.showinfo("✅ Success", f"Task '{name}' added successfully!")

        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_hours.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric hours!")


def update_task():
    """Update the task progress by adding hours."""
    try:
        task_id = entry_update_id.get().strip()
        hours = float(entry_update_hours.get().strip())

        task = pm.find_task(task_id)
        if not task:
            messagebox.showerror("Error", "Task not found!")
            return

        task.update_hours(hours)
        messagebox.showinfo("✅ Updated", f"Task '{task.name}' updated successfully!")

        entry_update_id.delete(0, tk.END)
        entry_update_hours.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric hours!")


def show_report():
    """Display all tasks with completion summary."""
    report = pm.task_report()
    if not report:
        messagebox.showinfo("📋 Report", "No tasks available yet.")
        return

    report_text = "📊 Project Task Report:\n\n"
    for t in report:
        report_text += (f"🔹 Task ID: {t['Task ID']}\n"
                        f"   Name: {t['Name']}\n"
                        f"   Estimated Hours: {t['Estimated Hours']}\n"
                        f"   Spent Hours: {t['Spent Hours']}\n"
                        f"   Status: {t['Status']}\n\n")

    completion = pm.project_completion_rate()
    report_text += f"🎯 Project Completion Rate: {completion:.1f}%"

    messagebox.showinfo("📊 Project Report", report_text)
    show_charts()  # show graphs when report is viewed


def show_charts():
    """Display bar and pie charts using matplotlib."""
    report = pm.task_report()
    if not report:
        return

    task_names = [t['Name'] for t in report]
    spent = [t['Spent Hours'] for t in report]
    estimated = [t['Estimated Hours'] for t in report]
    statuses = [t['Status'] for t in report]

    # Bar Chart - Hours Spent vs Estimated
    plt.figure(figsize=(8, 4))
    x = range(len(task_names))
    plt.bar(x, estimated, color='#90caf9', label='Estimated Hours', width=0.4)
    plt.bar([i + 0.4 for i in x], spent, color='#ef9a9a', label='Spent Hours', width=0.4)
    plt.xticks([i + 0.2 for i in x], task_names, rotation=20)
    plt.xlabel("Tasks")
    plt.ylabel("Hours")
    plt.title("📊 Task Hours Comparison")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Pie Chart - Status Distribution
    status_labels = ["Not Started", "In Progress", "Completed"]
    status_counts = [statuses.count(s) for s in status_labels]
    colors = ['#ffcc80', '#81d4fa', '#a5d6a7']

    plt.figure(figsize=(5, 5))
    plt.pie(status_counts, labels=status_labels, colors=colors,
            autopct='%1.1f%%', startangle=140, shadow=True)
    plt.title("🎯 Task Status Distribution")
    plt.show()


# ===============================
# 🧱 GUI Layout
# ===============================

# Header
tk.Label(root, text="🌸 Project Task Management System 🌸",
         font=("Verdana", 16, "bold"), fg="white", bg="#8e24aa", pady=10).pack(fill="x")

# Frame for Adding Tasks
frame_add = tk.LabelFrame(root, text="➕ Add Task", bg="#f9f2ff", fg="#6a1b9a", font=("Arial", 12, "bold"))
frame_add.pack(padx=20, pady=15, fill="x")

tk.Label(frame_add, text="Task ID:", bg="#f9f2ff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_id = tk.Entry(frame_add, width=25)
entry_id.grid(row=0, column=1, pady=5)

tk.Label(frame_add, text="Task Name:", bg="#f9f2ff").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_name = tk.Entry(frame_add, width=25)
entry_name.grid(row=1, column=1, pady=5)

tk.Label(frame_add, text="Estimated Hours:", bg="#f9f2ff").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_hours = tk.Entry(frame_add, width=25)
entry_hours.grid(row=2, column=1, pady=5)

tk.Button(frame_add, text="Add Task", bg="#8e24aa", fg="white", width=15, command=add_task).grid(row=3, columnspan=2, pady=10)

# Frame for Updating Tasks
frame_update = tk.LabelFrame(root, text="🛠 Update Task", bg="#f9f2ff", fg="#6a1b9a", font=("Arial", 12, "bold"))
frame_update.pack(padx=20, pady=15, fill="x")

tk.Label(frame_update, text="Task ID:", bg="#f9f2ff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_update_id = tk.Entry(frame_update, width=25)
entry_update_id.grid(row=0, column=1, pady=5)

tk.Label(frame_update, text="Add Hours:", bg="#f9f2ff").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_update_hours = tk.Entry(frame_update, width=25)
entry_update_hours.grid(row=1, column=1, pady=5)

tk.Button(frame_update, text="Update Task", bg="#6a1b9a", fg="white", width=15, command=update_task).grid(row=2, columnspan=2, pady=10)

# Frame for Report
frame_report = tk.LabelFrame(root, text="📋 Reports", bg="#f9f2ff", fg="#6a1b9a", font=("Arial", 12, "bold"))
frame_report.pack(padx=20, pady=15, fill="x")

tk.Button(frame_report, text="Show Report & Charts", bg="#43a047", fg="white", width=20, command=show_report).pack(pady=10)

# Exit Button
tk.Button(root, text="Exit", bg="#d32f2f", fg="white", font=("Arial", 11, "bold"),
          width=20, command=root.destroy).pack(pady=15)

# ===============================
# 🚀 Launch GUI
# ===============================
root.mainloop()
