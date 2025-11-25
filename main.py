
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

DATA_FILE = "tasks.json"


class TaskRepository:
    """Simple JSON-based storage for tasks."""

    def __init__(self, path: str = DATA_FILE):
        self.path = path
        self.tasks = []
        self._load()

    def _load(self):
        if not os.path.exists(self.path):
            self.tasks = []
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Basic validation
                if isinstance(data, list):
                    self.tasks = data
                else:
                    self.tasks = []
        except (json.JSONDecodeError, OSError):
            self.tasks = []

    def _save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except OSError as e:
            messagebox.showerror("Save error", f"Could not save tasks:\n{e}")

    def _next_id(self) -> int:
        if not self.tasks:
            return 1
        return max(t.get("id", 0) for t in self.tasks) + 1

    def add_task(self, title: str):
        new_task = {
            "id": self._next_id(),
            "title": title,
            "completed": False,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        self.tasks.append(new_task)
        self._save()
        return new_task

    def toggle_task(self, task_id: int):
        for t in self.tasks:
            if t.get("id") == task_id:
                t["completed"] = not t.get("completed", False)
                break
        self._save()

    def delete_task(self, task_id: int):
        self.tasks = [t for t in self.tasks if t.get("id") != task_id]
        self._save()

    def get_tasks(self, status_filter: str = "all"):
        """Return tasks filtered by status: all, pending, completed."""
        if status_filter == "pending":
            return [t for t in self.tasks if not t.get("completed", False)]
        if status_filter == "completed":
            return [t for t in self.tasks if t.get("completed", False)]
        return list(self.tasks)


class TaskApp(tk.Tk):
    """Task manager application with basic filters and JSON persistence."""

    def __init__(self):
        super().__init__()

        self.title("Task Manager")
        self.geometry("650x500")
        self.minsize(650, 500)

        self.repo = TaskRepository()
        self.filter_state = tk.StringVar(value="all")

        self._build_ui()
        self._refresh_table()

    # ----------------------------------------------------------
    # -----------------------UI building -----------------------
    # ----------------------------------------------------------

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill="both", expand=True)

        # Top: add task
        add_frame = ttk.LabelFrame(main, text="Add task")
        add_frame.pack(fill="x")

        self.new_task_var = tk.StringVar()
        self.new_task_entry = ttk.Entry(add_frame, textvariable=self.new_task_var)
        self.new_task_entry.pack(side="left", fill="x", expand=True, padx=(5, 5), pady=5)
        self.new_task_entry.bind("<Return>", lambda e: self.add_task())

        add_btn = ttk.Button(add_frame, text="Add", command=self.add_task)
        add_btn.pack(side="left", padx=(0, 5), pady=5)

        # Filters
        filter_frame = ttk.LabelFrame(main, text="Filters")
        filter_frame.pack(fill="x", pady=(10, 0))

        ttk.Radiobutton(
            filter_frame,
            text="All",
            variable=self.filter_state,
            value="all",
            command=self._refresh_table,
        ).pack(side="left", padx=5, pady=5)

        ttk.Radiobutton(
            filter_frame,
            text="Pending",
            variable=self.filter_state,
            value="pending",
            command=self._refresh_table,
        ).pack(side="left", padx=5, pady=5)

        ttk.Radiobutton(
            filter_frame,
            text="Completed",
            variable=self.filter_state,
            value="completed",
            command=self._refresh_table,
        ).pack(side="left", padx=5, pady=5)

        # Table
        table_frame = ttk.Frame(main)
        table_frame.pack(fill="both", expand=True, pady=(10, 0))

        columns = ("id", "title", "status", "created_at")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10,
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Task")
        self.tree.heading("status", text="Status")
        self.tree.heading("created_at", text="Created")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("title", width=280, anchor="w")
        self.tree.column("status", width=90, anchor="center")
        self.tree.column("created_at", width=140, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Row style for completed tasks
        self.tree.tag_configure("completed", foreground="#888")

        # Bottom buttons and summary
        bottom = ttk.Frame(main)
        bottom.pack(fill="x", pady=(10, 0))

        # Use classic tk.Button so they render correctly on all Windows themes
        toggle_btn = tk.Button(
            bottom,
            text="Complete / Undo",
            command=self.toggle_selected,
            font=("Segoe UI", 10),
            width=16,
            height=2
        )
        toggle_btn.pack(side="left", padx=(0, 10), pady=5)

        delete_btn = tk.Button(
            bottom,
            text="Delete",
            command=self.delete_selected,
            font=("Segoe UI", 10),
            width=10,
            height=2
        )
        delete_btn.pack(side="left", pady=5)

        self.summary_label = ttk.Label(bottom, text="0 tasks | 0 completed")
        self.summary_label.pack(side="right", pady=5)

    # ---------------------------------------------------
    # --------------------- Actions ---------------------
    # ---------------------------------------------------

    def add_task(self):
        title = self.new_task_var.get().strip()
        if not title:
            messagebox.showinfo("Empty task", "Please enter a task title.")
            return

        self.repo.add_task(title)
        self.new_task_var.set("")
        self._refresh_table()

    def _get_selected_task_id(self):
        selection = self.tree.selection()
        if not selection:
            return None
        item_id = selection[0]
        values = self.tree.item(item_id, "values")
        try:
            return int(values[0])
        except (ValueError, IndexError):
            return None

    def toggle_selected(self):
        task_id = self._get_selected_task_id()
        if task_id is None:
            messagebox.showinfo("No selection", "Please select a task first.")
            return
        self.repo.toggle_task(task_id)
        self._refresh_table()

    def delete_selected(self):
        task_id = self._get_selected_task_id()
        if task_id is None:
            messagebox.showinfo("No selection", "Please select a task to delete.")
            return

        if not messagebox.askyesno("Confirm deletion", "Delete selected task?"):
            return

        self.repo.delete_task(task_id)
        self._refresh_table()

    def _refresh_table(self):
        # Clear current rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        tasks = self.repo.get_tasks(self.filter_state.get())

        total = len(self.repo.tasks)
        completed = sum(1 for t in self.repo.tasks if t.get("completed", False))
        self.summary_label.config(text=f"{total} tasks | {completed} completed")

        for t in tasks:
            status = "Done" if t.get("completed", False) else "Pending"
            created = t.get("created_at", "")[:19]
            tag = "completed" if t.get("completed", False) else ""
            self.tree.insert(
                "",
                "end",
                values=(t.get("id"), t.get("title"), status, created),
                tags=(tag,),
            )


if __name__ == "__main__":
    app = TaskApp()
    app.mainloop()
