import tkinter as tk
from tkinter import messagebox
import datetime

def remind_tasks(tasks):  # tasksを引数として受け取る
    now = datetime.datetime.now()
    today_tasks = [task for task, _ in tasks if datetime.datetime.strptime(task, "%Y-%m-%d").date() == now.date()]
    if today_tasks:
        messagebox.showinfo("リマインダー", "今日のタスク: " + ", ".join(today_tasks))
    else:
        messagebox.showinfo("リマインダー", "今日のタスクはありません。")
