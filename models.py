from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import json

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Volunteers(db.Model):
    __tablename__ = "volunteers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    profile = db.relationship(
        "Profile",
        back_populates="volunteer",
        uselist=False,
        cascade="all, delete-orphan",
    )

    tasks = db.relationship(
        "Tasks",
        secondary="task_assignments",
        back_populates="volunteers",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profile": self.profile.to_dict() if self.profile else None,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    # Convert to json.dumps() format
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    def __repr__(self) -> str:
        return f"<Volunteer {self.name}, email: {self.email}>"


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey("volunteers.id"), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)

    volunteer = db.relationship("Volunteers", back_populates="profile", uselist=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "volunteer_id": self.volunteer_id,
            "bio": self.bio,
            "phone": self.phone,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    def __repr__(self) -> str:
        return f"<Profile of Volunteer ID {self.volunteer_id}, bio: {self.bio}, phone: {self.phone}>"


class Projects(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    def __repr__(self) -> str:
        return f"<Project {self.name}, description: {self.description}>"


class Tasks(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    description = db.Column(db.Text, nullable=True)

    project = db.relationship("Projects", backref=db.backref("tasks", lazy=True))

    volunteers = db.relationship(
        "Volunteers",
        secondary="task_assignments",
        back_populates="tasks",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "project_id": self.project_id,
            "description": self.description,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    def __repr__(self) -> str:
        return f"<Task {self.title}, project ID: {self.project_id}, description: {self.description}>"


task_assignments = db.Table(
    "task_assignments",
    db.Column(
        "volunteer_id", db.Integer, db.ForeignKey("volunteers.id"), primary_key=True
    ),
    db.Column("task_id", db.Integer, db.ForeignKey("tasks.id"), primary_key=True),
)
