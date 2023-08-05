# coding: utf-8
import tkinter as tk
from tkinter import messagebox
import calendar
import datetime
from reminder import remind_tasks

tasks = []

def add_task():
    task = task_entry.get()
    priority = priority_var.get()
    if task:
        tasks.append((task, priority))
        update_task_list()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("エラー", "タスクを入力してください。")

def update_task_list():
    task_list.delete(0, tk.END)
    for task, priority in tasks:
        task_list.insert(tk.END, f"{task} - 優先度: {priority}")

def complete_task():
    selected_task_index = task_list.curselection()
    if selected_task_index:
        index = selected_task_index[0]
        tasks.pop(index)
        update_task_list()
    else:
        messagebox.showwarning("エラー", "タスクを選択してください。")

def filter_tasks():
    filter_priority = filter_priority_var.get()
    filtered_tasks = [(task, priority) for task, priority in tasks if priority == filter_priority]
    tasks.clear()
    tasks.extend(filtered_tasks)
    update_task_list()

def sort_tasks():
    tasks.sort(key=lambda x: x[1], reverse=True)
    update_task_list()

def save_tasks_to_file():
    with open("tasks.txt", "w") as file:
        for task, priority in tasks:
            file.write(f"{task},{priority}\n")

def load_tasks_from_file():
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                task, priority = line.strip().split(',')
                tasks.append((task, priority))
        update_task_list()
    except FileNotFoundError:
        pass

# タスク管理アプリケーションのGUI作成
root = tk.Tk()
root.title("タスク管理アプリ")
root.geometry("400x450")

# タスクの優先順位選択用のラジオボタン
priority_var = tk.StringVar()
priority_var.set("高")
priority_frame = tk.Frame(root)
tk.Label(priority_frame, text="優先度: ").pack(side=tk.LEFT)
priority_frame.pack()
priority_labels = ["高", "中", "低"]
for priority_label in priority_labels:
    tk.Radiobutton(priority_frame, text=priority_label, variable=priority_var, value=priority_label).pack(side=tk.LEFT)

task_entry = tk.Entry(root,width=50)
task_entry.pack()

add_button = tk.Button(root, text="追加", command=add_task)
add_button.pack()

task_list = tk.Listbox(root,width=50)
task_list.pack()

complete_button = tk.Button(root, text="完了", command=complete_task)
complete_button.pack()

# タスクのフィルタリングとソート
filter_priority_var = tk.StringVar()
filter_priority_var.set("高")
filter_frame = tk.Frame(root)

filter_frame.pack()
tk.Label(filter_frame, text="フィルタリング: ").pack(side=tk.LEFT)
filter_menu = tk.OptionMenu(filter_frame, filter_priority_var, *priority_labels)
filter_menu.pack(side=tk.LEFT)
filter_button = tk.Button(root, text="フィルタリング", command=filter_tasks)
filter_button.pack()
sort_button = tk.Button(root, text="ソート(順序の並び替え)", command=sort_tasks)
sort_button.pack()

# カレンダー表示のためのボタンとウィンドウ
def show_calendar():
    cal_win = tk.Toplevel(root)
    cal_win.title("カレンダー")
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    cal = calendar.month(year, month)
    cal_label = tk.Label(cal_win, text=cal, font=("Arial", 12))
    cal_label.pack()

calendar_button = tk.Button(root, text="カレンダー表示", command=show_calendar)
calendar_button.pack()

# リマインダー機能
remind_button = tk.Button(root, text="今日のタスクを確認", command=lambda: remind_tasks(tasks))  # tasksを渡す
remind_button.pack()

# アプリケーションの起動時に保存されたタスクを読み込む
load_tasks_from_file()

# アプリケーションの終了時にタスクをファイルに保存する
root.protocol("WM_DELETE_WINDOW", save_tasks_to_file)
root.mainloop()
