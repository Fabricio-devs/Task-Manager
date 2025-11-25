
# 📝 Task Manager (Python + Tkinter)

A simple and efficient **Task Manager desktop application** built with Python using Tkinter.  
Tasks are stored locally in a clean JSON file, and the app provides filters, actions, and a clear UI.

This project is ideal for a beginner–intermediate portfolio and demonstrates GUI programming, state management, and persistent storage.

---

## 🚀 Features

- Add new tasks
- Mark tasks as completed or pending (toggle)
- Delete tasks
- Filters:
  - **All**
  - **Pending**
  - **Completed**
- Clean task table using `ttk.Treeview`
- Automatic local storage in `tasks.json`
- Buttons and UI compatible with all Windows themes

---

## 🛠 Requirements

- Python 3.x  
- No external libraries required  
- Uses only:
  - `tkinter`
  - `json`
  - `datetime`
  - `os`

---

## ▶️ How to Run

1. Place the file `todo_app.py` in any folder you like.
2. In a terminal inside that folder:

```bash
python todo_app.py
```

3. The app will auto-create the file:

```
tasks.json
```

where tasks are stored.

---

## 📁 Project Structure

```
TaskManager/
│── todo_app.py
│── README.md
└── tasks.json   (created automatically)
```

---

## 🧠 How It Works

### Storage
Tasks are saved in JSON format, each containing:

- ID  
- Title  
- Completion status  
- Creation timestamp  

### Filters
The task list can be filtered by:

- **All**  
- **Pending**  
- **Completed**  

### UI
- Uses `tkinter` + `ttk`
- Classic `tk.Button` ensures proper display on Windows scaling
- Smooth task listing with `ttk.Treeview`

---

## 👨‍💻 Author

Created by **Fabricio Cardozo**  
Developed as part of a professional Python portfolio.

---

## 📝 License

MIT License — free to use, modify, and learn from.
