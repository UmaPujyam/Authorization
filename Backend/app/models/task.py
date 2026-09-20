class Task:

    def __init__(
        self,
        task_id: int,
        title: str,
        completed: bool,
        user_id: int
    ):
        self.task_id = task_id
        self.title = title
        self.completed = completed
        self.user_id = user_id