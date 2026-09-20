from app.config.database import get_connection
from app.models.task import Task
class TaskRepository:

    def get_all(self, user_id: int) -> list[Task]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT task_id, title, completed, user_id
                    FROM tasks
                    WHERE user_id = %s
                    ORDER BY task_id DESC
                    """,
                    (user_id,)
                )

                rows = cur.fetchall()

        return [
            Task(row[0], row[1], row[2], row[3])
            for row in rows
        ]

    def create(self, title: str, user_id: int) -> Task:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO tasks (title, completed, user_id)
                    VALUES (%s, %s, %s)
                    RETURNING task_id, title, completed, user_id
                    """,
                    (title, False, user_id)
                )

                row = cur.fetchone()
                conn.commit()

        return Task(row[0], row[1], row[2], row[3])

    def update(
        self,
        task_id: int,
        title: str,
        completed: bool
    ) -> Task | None:

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE tasks
                    SET title = %s, completed = %s
                    WHERE task_id = %s
                    RETURNING task_id, title, completed, user_id
                    """,
                    (title, completed, task_id)
                )

                row = cur.fetchone()

                if row is None:
                    conn.rollback()
                    return None

                conn.commit()

        return Task(row[0], row[1], row[2], row[3])

    def delete(self, task_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM tasks
                    WHERE task_id = %s
                    """,
                    (task_id,)
                )

                deleted = cur.rowcount
                conn.commit()

        return deleted > 0

    def assign(self, task_id: int, user_id: int) -> Task | None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE tasks
                    SET user_id = %s
                    WHERE task_id = %s
                    RETURNING task_id, title, completed, user_id
                    """,
                    (user_id, task_id)
                )

                row = cur.fetchone()

                if row is None:
                    conn.rollback()
                    return None

                conn.commit()

        return Task(row[0], row[1], row[2], row[3])