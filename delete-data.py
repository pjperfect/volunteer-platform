# Deletes all data from the database tables. Use with caution!
from app import app
from models import db, Volunteers, Profile, Projects, Tasks, task_assignments

with app.app_context():
    # Clear all data
    db.session.execute(task_assignments.delete())
    db.session.query(Tasks).delete()
    db.session.query(Profile).delete()
    db.session.query(Volunteers).delete()
    db.session.query(Projects).delete()
    db.session.commit()