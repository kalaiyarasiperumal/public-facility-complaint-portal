from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Upload folder
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Complaint data
complaints = [
    {
        "id": 1,
        "name": "Ravi Kumar",
        "facility": "Water Supply",
        "location": "Ward 5",
        "description": "Water supply problem",
        "photo": "",
        "status": "Pending"
    },
    {
        "id": 2,
        "name": "Priya S",
        "facility": "Street Light",
        "location": "Ward 2",
        "description": "Street light not working",
        "photo": "",
        "status": "Resolved"
    },
    {
        "id": 3,
        "name": "Arun M",
        "facility": "Road Damage",
        "location": "Ward 8",
        "description": "Road is damaged",
        "photo": "",
        "status": "In Progress"
    }
]


# Home page
@app.route("/")
def home():
    return render_template("index.html")
    @app.route("/facility")
def facility():
    return render_template("facility.html")

# Admin dashboard
@app.route("/admin")
def admin():

    filter_status = request.args.get("filter", "All")
    search = request.args.get("search", "").lower()

    filtered_complaints = complaints

    if filter_status != "All":
        filtered_complaints = [
            complaint
            for complaint in complaints
            if complaint["status"] == filter_status
        ]

    if search:
        filtered_complaints = [
            complaint
            for complaint in filtered_complaints
            if search in complaint["name"].lower()
            or search in complaint["location"].lower()
            or search in complaint["facility"].lower()
        ]

    return render_template(
        "admin.html",
        complaints=filtered_complaints,
        all_complaints=complaints,
        filter_status=filter_status,
        search=search
    )


# Add complaint
@app.route("/add_complaint", methods=["POST"])
def add_complaint():

    name = request.form.get("name")
    facility = request.form.get("facility")
    location = request.form.get("location")
    description = request.form.get("description")

    photo = request.files.get("photo")

    photo_filename = ""

    if photo and photo.filename != "":
        photo_filename = photo.filename

        photo_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            photo_filename
        )

        photo.save(photo_path)

    new_id = max(
        [complaint["id"] for complaint in complaints],
        default=0
    ) + 1

    new_complaint = {
        "id": new_id,
        "name": name,
        "facility": facility,
        "location": location,
        "description": description,
        "photo": photo_filename,
        "status": "Pending"
    }

    complaints.append(new_complaint)

    return redirect(url_for("admin"))


# Update complaint status
@app.route("/update_status/<int:id>", methods=["POST"])
def update_status(id):

    new_status = request.form.get("status")

    for complaint in complaints:
        if complaint["id"] == id:
            complaint["status"] = new_status
            break

    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
