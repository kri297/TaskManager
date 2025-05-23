Task Manager in Python
A terminal-based Task Manager application built with Python that helps you manage your daily to-dos efficiently. 
It supports task scheduling with deadlines, marking tasks as complete, viewing summaries, analyzing productivity, auto-saving/loading data, and exporting your tasks.
🚀 Features
✅ Add Tasks: Add new tasks with specific deadlines.

🕒 Mark as Complete: Easily mark tasks as completed.

📋 View Tasks: See your task list with statuses (Pending, Completed, Overdue).

📅 Daily Summary: Get a categorized view of your tasks (Completed, Pending, Overdue).

📈 Productivity Analysis: Visual pie chart analysis of your task completion rate using matplotlib.

💾 Auto Save/Load: Saves your tasks to a .pkl file and optionally loads them on start.

📤 Export Tasks: Export your task list to a .txt file.

Installation
Clone the repository:

git clone https://github.com/kri297/task-manager-python.git
cd task-manager-python

Install required packages (make sure matplotlib is installed):
pip install matplotlib

Usage
When you run the program, you'll be greeted with a menu of options:


1. Add Task
2. Complete Task
3. View Tasks
4. Daily Summary
5. Productivity Analysis
6. Save and Exit
7. Export Tasks

 Concepts Used
1. datetime for date and time management

2. pickle for saving/loading task data

3. matplotlib for pie chart visualization

4. Object-oriented programming with a TaskManager class

5. Input handling and terminal formatting
