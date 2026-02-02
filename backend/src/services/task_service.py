from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import Session
from sqlalchemy import and_
import uuid
from ..models.task import Task, TaskCreate, TaskUpdate
from ..database.connection import get_session


class TaskService:
    @staticmethod
    def create_task(db: Session, task_create: TaskCreate, user_id: str) -> Task:
        # Convert string user_id to UUID for proper comparison
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )

        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            due_date=task_create.due_date,
            priority=task_create.priority,
            user_id=user_uuid
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_task_by_id(db: Session, task_id: str, user_id: str) -> Optional[Task]:
        # Convert string user_id to UUID for proper comparison
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )

        return db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_uuid)
        ).first()

    @staticmethod
    def get_tasks_by_user(
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        status_filter: Optional[str] = None,
        sort_by: str = "created"
    ) -> List[Task]:
        # Convert string user_id to UUID for proper comparison
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )

        query = db.query(Task).filter(Task.user_id == user_uuid)

        # Apply status filter if provided
        if status_filter:
            if status_filter == "completed":
                query = query.filter(Task.is_completed == True)
            elif status_filter == "pending":
                query = query.filter(Task.is_completed == False)

        # Apply sorting
        if sort_by == "due_date":
            query = query.order_by(Task.due_date.asc().nullslast())
        elif sort_by == "priority":
            # Sort by priority: high, medium, low
            from sqlalchemy import case
            priority_case = case(
                (Task.priority == 'high', 1),
                (Task.priority == 'medium', 2),
                (Task.priority == 'low', 3),
                else_=4
            )
            query = query.order_by(priority_case)
        else:  # Default is "created" which sorts by creation date (id)
            query = query.order_by(Task.id.desc())

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_task(db: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
        # Convert string user_id to UUID for proper comparison
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )

        db_task = db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_uuid)
        ).first()
        if not db_task:
            return None

        # Update fields if they are provided
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: str, user_id: str) -> bool:
        # Convert string user_id to UUID for proper comparison
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )

        db_task = db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_uuid)
        ).first()
        if not db_task:
            return False

        db.delete(db_task)
        db.commit()
        return True

    @staticmethod
    def toggle_task_completion(db: Session, task_id: str, user_id: str, is_completed: bool) -> Optional[Task]:
        # Convert string user_id to UUID for proper comparison
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )

        db_task = db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_uuid)
        ).first()
        if not db_task:
            return None

        db_task.is_completed = is_completed
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def delete_completed_tasks(db: Session, user_id: str) -> int:
        # Convert string user_id to UUID for proper comparison
        try:
            user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )

        # Count tasks that will be deleted
        completed_tasks = db.query(Task).filter(
            and_(Task.user_id == user_uuid, Task.is_completed == True)
        ).all()

        # Delete completed tasks
        deleted_count = db.query(Task).filter(
            and_(Task.user_id == user_uuid, Task.is_completed == True)
        ).delete(synchronize_session=False)

        db.commit()
        return deleted_count