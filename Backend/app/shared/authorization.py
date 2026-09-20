from fastapi import Depends, HTTPException, status

from app.shared.dependencies import get_current_user
from app.repositories.permission_repository import PermissionRepository
from app.schemas.auth import CurrentUser


permission_repository = PermissionRepository()


def require_permission(resource: str, action: str):

    def permission_checker(
        current_user: CurrentUser = Depends(get_current_user),
    ) -> CurrentUser:

        has_permission = permission_repository.has_permission(
            current_user.user_id,
            resource,
            action
        )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        return current_user

    return permission_checker