from fastapi import APIRouter, Depends, HTTPException

from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.schemas.auth import CurrentUser
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.shared.authorization import require_permission


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


def get_task_service():
    return TaskService(TaskRepository())


def to_response(task):
    return TaskResponse(
        task_id=task.task_id,
        title=task.title,
        completed=task.completed
    )


# GET /tasks → task:read
@router.get("", response_model=list[TaskResponse])
def get_tasks(
    current_user: CurrentUser = Depends(
        require_permission("task", "read")
    )
):
    service = get_task_service()

    tasks = service.list_tasks(current_user.user_id)

    return [to_response(task) for task in tasks]


# POST /tasks → task:create
@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    current_user: CurrentUser = Depends(
        require_permission("task", "create")
    )
):
    service = get_task_service()

    created = service.create_task(
        task.title,
        current_user.user_id
    )

    return to_response(created)


# PUT /tasks/{task_id} → task:update
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user: CurrentUser = Depends(
        require_permission("task", "update")
    )
):
    service = get_task_service()

    updated = service.update_task(
        task_id,
        task.title,
        task.completed
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return to_response(updated)


# DELETE /tasks/{task_id} → task:delete
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: CurrentUser = Depends(
        require_permission("task", "delete")
    )
):
    service = get_task_service()

    deleted = service.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task deleted successfully"
    }


# POST /tasks/{task_id}/assign → task:assign
@router.post("/{task_id}/assign", response_model=TaskResponse)
def assign_task(
    task_id: int,
    user_id: int,
    current_user: CurrentUser = Depends(
        require_permission("task", "assign")
    )
):
    service = get_task_service()

    assigned = service.assign_task(
        task_id,
        user_id
    )

    if assigned is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return to_response(assigned)