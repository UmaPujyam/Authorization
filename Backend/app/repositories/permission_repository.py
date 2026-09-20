from app.config.database import get_connection


class PermissionRepository:

    def has_permission(self,user_id: int,resource: str,action: str) -> bool:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM user_roles ur
                JOIN role_permissions rp
                    ON rp.role_id = ur.role_id
                JOIN permissions p
                    ON p.permission_id = rp.permission_id
                WHERE ur.user_id = %s
                  AND p.resource = %s
                  AND p.action = %s
            )
            """,
            (user_id, resource, action)
        )

        result = cur.fetchone()[0]

        cur.close()
        conn.close()

        return result