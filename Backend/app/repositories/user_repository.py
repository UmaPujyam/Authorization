from app.config.database import get_connection
from app.models.user import User
class UserRepository:

    def get_by_id(self, user_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT user_id, name, email, password_hash
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)
        )

        row = cur.fetchone()

        cur.close()
        conn.close()

        return User(*row) if row else None

    def get_by_email(self, email):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT user_id, name, email, password_hash
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        row = cur.fetchone()

        cur.close()
        conn.close()

        return User(*row) if row else None

    def get_role_ids(self, user_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT role_id
            FROM user_roles
            WHERE user_id = %s
            ORDER BY role_id
            """,
            (user_id,)
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [row[0] for row in rows]

    def create(self, name, email, password_hash):
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                """
                INSERT INTO users (name, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING user_id, name, email, password_hash
                """,
                (name, email, password_hash)
            )

            row = cur.fetchone()
            user_id = row[0]

            cur.execute(
                """
                SELECT role_id
                FROM roles
                WHERE role_name = %s
                """,
                ("MEMBER",)
            )

            role_row = cur.fetchone()

            if not role_row:
                raise ValueError("MEMBER role not found")

            role_id = role_row[0]

            cur.execute(
                """
                INSERT INTO user_roles (user_id, role_id)
                VALUES (%s, %s)
                """,
                (user_id, role_id)
            )

            conn.commit()

            return User(*row)

        except Exception:
            conn.rollback()
            raise

        finally:
            cur.close()
            conn.close()