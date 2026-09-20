from app.repositories.task_repository import TaskRepository

class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def list_tasks(self, user_id):
        return self.repository.get_all(user_id)

    def create_task(self, title, user_id):
        return self.repository.create(title, user_id)

    def update_task(self, task_id, title, completed):
        return self.repository.update(task_id, title, completed)

    def delete_task(self, task_id):
        return self.repository.delete(task_id)

    def assign_task(self, task_id, user_id):
        return self.repository.assign(task_id, user_id)