from app.config.database import get_connection


def seed_rbac():
    conn = get_connection()

    try:
        with conn.cursor() as cur:

            # Seed permissions
            permissions = [
                ("task", "create"),
                ("task", "read"),
                ("task", "update"),
                ("task", "delete"),
                ("task", "assign"),
            ]

            for resource, action in permissions:
                cur.execute(
                    """
                    INSERT INTO permissions (resource, action)
                    VALUES (%s, %s)
                    ON CONFLICT (resource, action) DO NOTHING
                    """,
                    (resource, action)
                )

            # Get existing role IDs
            cur.execute(
                """
                SELECT role_id, name
                FROM roles
                WHERE name IN (%s, %s, %s)
                """,
                ("ADMIN", "MEMBER", "MANAGER")
            )

            roles = {
                name: role_id
                for role_id, name in cur.fetchall()
            }

            # Get permission IDs
            cur.execute(
                """
                SELECT permission_id, resource, action
                FROM permissions
                WHERE resource = %s
                """,
                ("task",)
            )

            permission_map = {
                (resource, action): permission_id
                for permission_id, resource, action in cur.fetchall()
            }

            # ADMIN permissions
            admin_permissions = [
                "create",
                "read",
                "update",
                "delete",
                "assign",
            ]

            # MANAGER permissions
            manager_permissions = [
                "create",
                "read",
                "update",
                
            ]

            # MEMBER permissions
            member_permissions = [
                "create",
                "read",
            ]

            # Create role-permission mappings
            role_permissions = {
                "ADMIN": admin_permissions,
                "MANAGER": manager_permissions,
                "MEMBER": member_permissions,
            }

            for role_name, actions in role_permissions.items():

                for action in actions:
                    cur.execute(
                        """
                        INSERT INTO role_permissions (role_id, permission_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        (
                            roles[role_name],
                            permission_map[("task", action)],
                        )
                    )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    seed_rbac()
    print("RBAC seed data inserted successfully.")