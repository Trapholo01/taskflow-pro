from app import db
from datetime import datetime

class Project(db.Model):
    """A project groups related tasks together."""
    __tablename__ = "projects"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship — access project.tasks to get all tasks
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "description": self.description,
            "task_count":  len(self.tasks),
            "created_at":  self.created_at.isoformat(),
        }


class Task(db.Model):
    """An individual task that belongs to a project."""
    __tablename__ = "tasks"

    id          = db.Column(db.Integer, primary_key=True)
    project_id  = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority    = db.Column(db.Enum("low","medium","high","critical", name="priority_enum"), default="medium")
    status      = db.Column(db.Enum("todo","in_progress","done","blocked", name="status_enum"), default="todo")
    due_date    = db.Column(db.Date)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id":          self.id,
            "project_id":  self.project_id,
            "title":       self.title,
            "description": self.description,
            "priority":    self.priority,
            "status":      self.status,
            "due_date":    self.due_date.isoformat() if self.due_date else None,
            "created_at":  self.created_at.isoformat(),
        }
