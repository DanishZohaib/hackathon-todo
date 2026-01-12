from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.task import Task, TaskCreate, TaskUpdate
from ..database.connection import get_db


class TaskService:
    @staticmethod
    def create_task(db: Session, task_create: TaskCreate, user_id: str) -> Task:
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            due_date=task_create.due_date,
            priority=task_create.priority,
            user_id=user_id
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_task_by_id(db: Session, task_id: str, user_id: str) -> Optional[Task]:
        return db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_id)
        ).first()

    @staticmethod
    def get_tasks_by_user(
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        status_filter: Optional[str] = None
    ) -> List[Task]:
        query = db.query(Task).filter(Task.user_id == user_id)

        if status_filter:
            if status_filter == "completed":
                query = query.filter(Task.is_completed == True)
            elif status_filter == "pending":
                query = query.filter(Task.is_completed == False)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_task(db: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
        db_task = db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_id)
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
        db_task = db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_id)
        ).first()
        if not db_task:
            return False

        db.delete(db_task)
        db.commit()
        return True

    @staticmethod
    def toggle_task_completion(db: Session, task_id: str, user_id: str, is_completed: bool) -> Optional[Task]:
        db_task = db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_id)
        ).first()
        if not db_task:
            return None

        db_task.is_completed = is_completed
        db.commit()
        db.refresh(db_task)
        return db_task