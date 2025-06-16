from storage import load_tasks, save_tasks

class TaskManager:
    def __init__(self):
        self.tasks = []

    def load(self):
        self.tasks = load_tasks()

    def add_task(self, task_name):
        self.tasks.append({'name': task_name, 'completed': False})
        save_tasks(self.tasks)

    def delete_task(self, task_name):
        self.tasks = [task for task in self.tasks if task['name'] != task_name]
        save_tasks(self.tasks)

    def toggle_task(self, task_name):
        for task in self.tasks:
            if task['name'] == task_name:
                task['completed'] = not task['completed']
        save_tasks(self.tasks)
