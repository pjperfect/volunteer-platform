from flask import Flask, request, jsonify
from models import db, Volunteers as Volunteer, Profile
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Volunteer Platform API"})


# /Volunteers CRUD


@app.route("/volunteers", methods=["POST"])
def create_volunteer():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"message": "Name and email are required"}), 400

    try:
        new_volunteer = Volunteer(name=data["name"], email=data["email"])
        db.session.add(new_volunteer)
        db.session.commit()
        return jsonify(new_volunteer.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route("/volunteers", methods=["GET"])
def get_volunteers():
    volunteers = Volunteer.query.all()
    return jsonify([volunteer.to_dict() for volunteer in volunteers]), 200


@app.route("/volunteers/<int:volunteer_id>", methods=["GET"])
def get_volunteer(volunteer_id):
    volunteer = db.get_or_404(Volunteer, volunteer_id)
    return jsonify(volunteer.to_dict()), 200


@app.route("/volunteers/<int:volunteer_id>", methods=["PATCH"])
def update_volunteer(volunteer_id):
    volunteer = db.get_or_404(Volunteer, volunteer_id)
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    try:
        if "name" in data:
            volunteer.name = data["name"]
        if "email" in data:
            volunteer.email = data["email"]

        db.session.commit()
        return jsonify(volunteer.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route("/volunteers/<int:volunteer_id>", methods=["DELETE"])
def delete_volunteer(volunteer_id):
    volunteer = db.get_or_404(Volunteer, volunteer_id)

    try:
        db.session.delete(volunteer)
        db.session.commit()
        return "", 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# /Profiles CRUD


@app.route("/profiles", methods=["POST"])
def create_profile():
    data = request.get_json()
    volunteer_id = data.get("volunteer_id")

    if not volunteer_id:
        return jsonify({"message": "Volunteer ID is required"}), 400

    volunteer = db.session.get(Volunteer, volunteer_id)
    if not volunteer:
        return jsonify({"message": "Volunteer not found"}), 404

    if volunteer.profile:
        return jsonify({"message": "Volunteer already has a profile"}), 409

    try:
        new_profile = Profile(
            bio=data.get("bio"), phone=data.get("phone"), volunteer=volunteer
        )
        db.session.add(new_profile)
        db.session.commit()
        return jsonify(new_profile.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route("/profiles", methods=["GET"])
def get_profiles():
    profiles = Profile.query.all()
    return jsonify([profile.to_dict() for profile in profiles]), 200


@app.route("/profiles/<int:profile_id>", methods=["GET"])
def get_profile(profile_id):
    profile = db.get_or_404(Profile, profile_id)
    return jsonify(profile.to_dict()), 200


@app.route("/profiles/<int:profile_id>", methods=["PATCH"])
def update_profile(profile_id):
    profile = db.get_or_404(Profile, profile_id)
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    try:
        if "bio" in data:
            profile.bio = data["bio"]
        if "phone" in data:
            profile.phone = data["phone"]

        db.session.commit()
        return jsonify(profile.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route("/profiles/<int:profile_id>", methods=["DELETE"])
def delete_profile(profile_id):
    profile = db.get_or_404(Profile, profile_id)

    try:
        db.session.delete(profile)
        db.session.commit()
        return "", 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
