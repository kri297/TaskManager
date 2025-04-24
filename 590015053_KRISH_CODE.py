import datetime
import matplotlib.pyplot as plt
import os
import pickle

class TaskManager:
    def __init__(self):
        self.tasks = []

    def print_header(self, title):
        width = 70
        print("\n" + "=" * width)
        print(f"{title.center(width)}")
        print("=" * width)

    def add_task(self, task_name, date_str, time_str):
        if task_name:
            try:
                deadline_str = date_str + " " + time_str
                deadline = datetime.datetime.strptime(deadline_str, "%d-%m-%Y %H:%M")
                now = datetime.datetime.now()
                if deadline < now:
                    print("[ERROR] You have entered an old date and time. Please enter a future date.")
                    return
                self.tasks.append((task_name, deadline, False))
                print(f"[SUCCESS] Task Added: {task_name} | Due: {deadline.strftime('%d-%m-%Y')} | Time: {deadline.strftime('%H:%M')}")
            except ValueError:
                print("[ERROR] Invalid date or time format. Please use DD-MM-YYYY for date and HH:MM for time.")
        else:
            print("[ERROR] Task name cannot be empty")

    def complete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            task_name = self.tasks[task_index][0]
            self.tasks[task_index] = (task_name, self.tasks[task_index][1], True)
            print(f"[SUCCESS] Task completed: {task_name}")
        else:
            print("[ERROR] Invalid task index")

    def view_tasks(self):
        if not self.tasks:
            self.print_header("TASK LIST")
            print("No tasks available.")
            return

        self.print_header("TASK LIST")

        sorted_tasks = sorted(self.tasks, key=lambda x: x[1])
        max_task_len = max([len(task) for task, _, _ in sorted_tasks] + [10]) + 2

        print("+-----+{0}+----------------------+-------------------+".format("-" * (max_task_len)))
        print("| ID  | {0} | Due Date             | Status            |".format("Task".ljust(max_task_len)))
        print("+-----+{0}+----------------------+-------------------+".format("-" * (max_task_len)))

        now = datetime.datetime.now()

        for idx, (task, deadline, completed) in enumerate(sorted_tasks):
            if completed:
                status = "✓ Completed"
            elif deadline < now:
                status = "! Overdue"
            else:
                status = "» Pending"

            print("| {0:<3} | {1} | {2} | {3} |".format(
                idx + 1,
                task.ljust(max_task_len),
                deadline.strftime('%d-%m-%Y %H:%M'),
                status.ljust(17)
            ))

        print("+-----+{0}+----------------------+-------------------+".format("-" * (max_task_len)))

    def daily_summary(self):
        self.print_header("DAILY SUMMARY")
        
        completed_tasks = [task for task, _, completed in self.tasks if completed]
        pending_tasks = [task for task, _, completed in self.tasks if not completed]
        today = datetime.datetime.now()
        overdue_tasks = [task for task, deadline, completed in self.tasks if deadline < today and not completed]

        print("+" + "-" * 68 + "+")
        print("| ✓ Completed Tasks: {0}".format(len(completed_tasks)).ljust(69) + "|")
        if completed_tasks:
            for task in completed_tasks:
                task = task if len(task) <= 60 else task[:57] + "..."
                print("|   {0}".format(task).ljust(69) + "|")
        else:
            print("|   None".ljust(69) + "|")
        print("+" + "-" * 68 + "+")
        
        print("| » Pending Tasks: {0}".format(len(pending_tasks)).ljust(69) + "|")
        if pending_tasks:
            for task in pending_tasks:
                task = task if len(task) <= 60 else task[:57] + "..."
                print("|   {0}".format(task).ljust(69) + "|")
        else:
            print("|   None".ljust(69) + "|")
        print("+" + "-" * 68 + "+")
        
        print("| ! Overdue Tasks: {0}".format(len(overdue_tasks)).ljust(69) + "|")
        if overdue_tasks:
            for task in overdue_tasks:
                task = task if len(task) <= 60 else task[:57] + "..."
                print("|   {0}".format(task).ljust(69) + "|")
        else:
            print("|   None".ljust(69) + "|")
        print("+" + "-" * 68 + "+")

    def productivity_analysis(self):
        completed_count = sum(1 for _, _, completed in self.tasks if completed)
        pending_count = sum(1 for _, _, completed in self.tasks if not completed)
        total_tasks = completed_count + pending_count

        self.print_header("PRODUCTIVITY ANALYSIS")

        if total_tasks == 0:
            print("No tasks to analyze.")
            return

        completion_rate = (completed_count / total_tasks) * 100
        pending_rate = (pending_count / total_tasks) * 100

        print("+" + "-" * 68 + "+")
        print("| Total Tasks: {0}".format(total_tasks).ljust(69) + "|")
        print("| Completed Tasks: {0} ({1:.2f}%)".format(completed_count, completion_rate).ljust(69) + "|")
        print("| Pending Tasks: {0} ({1:.2f}%)".format(pending_count, pending_rate).ljust(69) + "|")
        print("+" + "-" * 68 + "+")

        labels = ['Completed', 'Pending']
        values = [completed_count, pending_count]
        colors = ['#4CAF50', '#FF6347']

        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops={'edgecolor': 'black'})
        ax.set_title(f"Task Completion vs Pending", fontsize=16, fontweight='bold')
        ax.legend(wedges, [f"{label}: {value}" for label, value in zip(labels, values)], title="Task Status", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=12, weight="bold", color='white')
        plt.show()

    def save_tasks(self):
        with open("tasks.pkl", "wb") as f:
            pickle.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists("tasks.pkl"):
            with open("tasks.pkl", "rb") as f:
                self.tasks = pickle.load(f)
            print("[SUCCESS] Old tasks loaded.")
        else:
            print("[INFO] No saved tasks found.")

def prompt_yes_no(question):
    while True:
        response = input(f"{question} (Yes/No): ").strip().lower()
        if response == 'yes':
            return True
        elif response == 'no':
            return False
        else:
            print("[ERROR] Please answer with 'Yes' or 'No'.")

if __name__ == '__main__':
    menu_width = 70
    tool = TaskManager()

    # Load old tasks if available
    if prompt_yes_no("Do you want to load old tasks?"):
        tool.load_tasks()

    while True:
        print("\n+" + "=" * menu_width + "+")
        print("|" + "TASK MANAGER".center(menu_width) + "|")
        print("+" + "=" * menu_width + "+")
        print("|" + "1. Add Task".ljust(menu_width - 1) + "|")
        print("|" + "2. Complete Task".ljust(menu_width - 1) + "|")
        print("|" + "3. View Tasks".ljust(menu_width - 1) + "|")
        print("|" + "4. Daily Summary".ljust(menu_width - 1) + "|")
        print("|" + "5. Productivity Analysis".ljust(menu_width - 1) + "|")
        print("|" + "6. Save and Exit".ljust(menu_width - 1) + "|")
        print("|" + "7. Export Tasks".ljust(menu_width - 1) + "|")
        print("+" + "=" * menu_width + "+")

        choice = input("Enter your choice: ")

        if choice == '1':
            task_name = input("Enter task name: ")
            date_input = input("Enter task date (DD-MM-YYYY): ")
            time_input = input("Enter task time (HH:MM): ")
            tool.add_task(task_name, date_input, time_input)
        elif choice == '2':
            tool.view_tasks()
            try:
                task_index = int(input("Enter task number to mark as completed: ")) - 1
                task_to_complete = sorted(tool.tasks, key=lambda x: x[1])[task_index]
                real_index = tool.tasks.index(task_to_complete)
                tool.complete_task(real_index)
            except (ValueError, IndexError):
                print("[ERROR] Please enter a valid number for the task index.")
        elif choice == '3':
            tool.view_tasks()
        elif choice == '4':
            tool.daily_summary()
        elif choice == '5':
            tool.productivity_analysis()
        elif choice == '6':
            if prompt_yes_no("Do you want to save tasks before exiting?"):
                tool.save_tasks()
            print("Thank you for using the Task Manager. Goodbye!")
            break
        elif choice == '7':
            if prompt_yes_no("Do you want to export your tasks?"):
                with open("tasks_export.txt", "w") as f:
                    for task, deadline, completed in tool.tasks:
                        f.write(f"{task} | Due: {deadline.strftime('%d-%m-%Y %H:%M')} | {'Completed' if completed else 'Pending'}\n")
                print("[SUCCESS] Tasks exported.")
        else:
            print("[ERROR] Invalid choice, please try again.")
