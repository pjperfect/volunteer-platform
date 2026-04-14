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

    # Seed volunteers
    v1 = Volunteers(name="Alice Johnson", email="alice@example.com")
    v2 = Volunteers(name="Bob Smith", email="bob@example.com")
    v3 = Volunteers(name="Carol White", email="carol@example.com")
    v4 = Volunteers(name="David Brown", email="david@example.com")
    v5 = Volunteers(name="Eva Green", email="eva@example.com")
    v6 = Volunteers(name="Frank Black", email="frank@example.com")
    v7 = Volunteers(name="Grace Lee", email="grace@example.com")
    v8 = Volunteers(name="Henry Adams", email="henry@example.com")
    v9 = Volunteers(name="Irene Clark", email="irene@example.com")
    v10 = Volunteers(name="James Wilson", email="james@example.com")
    db.session.add_all([v1, v2, v3, v4, v5, v6, v7, v8, v9, v10])
    db.session.commit()

    # Seed profiles
    p1 = Profile(volunteer_id=v1.id, bio="Loves community work", phone="0711000001")
    p2 = Profile(volunteer_id=v2.id, bio="Experienced in logistics", phone="0711000002")
    p3 = Profile(volunteer_id=v3.id, bio="Background in healthcare", phone="0711000003")
    p4 = Profile(volunteer_id=v4.id, bio="Skilled in carpentry", phone="0711000004")
    p5 = Profile(volunteer_id=v5.id, bio="Fluent in sign language", phone="0711000005")
    p6 = Profile(volunteer_id=v6.id, bio="Experienced driver", phone="0711000006")
    p7 = Profile(volunteer_id=v7.id, bio="Social media coordinator", phone="0711000007")
    p8 = Profile(
        volunteer_id=v8.id, bio="Former military, disciplined", phone="0711000008"
    )
    p9 = Profile(volunteer_id=v9.id, bio="Teacher and trainer", phone="0711000009")
    p10 = Profile(volunteer_id=v10.id, bio="IT and tech support", phone="0711000010")
    db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
    db.session.commit()

    # Seed projects
    proj1 = Projects(name="Clean Up Drive", description="City-wide cleanup initiative")
    proj2 = Projects(name="Food Bank", description="Weekly food distribution")
    proj3 = Projects(name="Youth Mentorship", description="Mentoring at-risk youth")
    proj4 = Projects(name="Medical Outreach", description="Free clinics in rural areas")
    db.session.add_all([proj1, proj2, proj3, proj4])
    db.session.commit()

    # Seed tasks
    t1 = Tasks(
        title="Collect Supplies",
        project_id=proj1.id,
        description="Gather cleaning materials",
    )
    t2 = Tasks(
        title="Assign Zones", project_id=proj1.id, description="Divide cleanup areas"
    )
    t3 = Tasks(
        title="Sort Donations", project_id=proj2.id, description="Categorize food items"
    )
    t4 = Tasks(
        title="Deliver Packages",
        project_id=proj2.id,
        description="Transport food to families",
    )
    t5 = Tasks(
        title="Run Workshops",
        project_id=proj3.id,
        description="Lead youth skills sessions",
    )
    t6 = Tasks(
        title="Coordinate Mentors",
        project_id=proj3.id,
        description="Match mentors with mentees",
    )
    t7 = Tasks(
        title="Set Up Clinic",
        project_id=proj4.id,
        description="Prepare medical equipment",
    )
    t8 = Tasks(
        title="Patient Registration",
        project_id=proj4.id,
        description="Register incoming patients",
    )
    db.session.add_all([t1, t2, t3, t4, t5, t6, t7, t8])
    db.session.commit()

    # Seed task assignments
    v1.tasks.extend([t1, t2])
    v2.tasks.extend([t2, t3])
    v3.tasks.extend([t3, t7])
    v4.tasks.extend([t1, t4])
    v5.tasks.extend([t5, t6])
    v6.tasks.extend([t4, t8])
    v7.tasks.extend([t6, t5])
    v8.tasks.extend([t7, t8])
    v9.tasks.extend([t5, t3])
    v10.tasks.extend([t2, t6])
    db.session.commit()
    # We use the extend() method and not append() because tasks is a list-like relationship, and we want to add multiple tasks to each volunteer. The extend() method allows us to add multiple items to the list at once, while append() would only allow us to add one item at a time. By using extend(), we can efficiently assign multiple tasks to each volunteer in a single operation.

    print(
        "Seeded 10 volunteers, 10 profiles, 4 projects, 8 tasks, and task assignments."
    )
