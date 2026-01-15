from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder="Template")
FILE = "donors.txt"

# Home page
@app.route("/")
def index():
    total_donors = 0
    blood_types = {}
    try:
        with open(FILE, "r") as f:
            for line in f:
                total_donors += 1
                blood = line.strip().split(",")[1]
                blood_types[blood] = blood_types.get(blood, 0) + 1
    except FileNotFoundError:
        total_donors = 0
        blood_types = {}

    return render_template("index.html", total=total_donors, blood_types=blood_types)

# Add donor page
@app.route("/add")
def add_donor():
    return render_template("add_donor.html")

# Save donor
@app.route("/save", methods=["POST"])
def save():
    name = request.form["name"].strip()
    blood = request.form["blood"].strip().upper()
    age = request.form["age"].strip()
    phone = request.form["phone"].strip()

    valid_blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

    if not name:
        return "Name is required"
    if blood not in valid_blood_types:
        return "Invalid Blood Type"
    try:
        age = int(age)
        if age < 18:
            return "Donor must be 18+"
    except ValueError:
        return "Age must be a number"

    with open(FILE, "a") as f:
        f.write(f"{name},{blood},{age},{phone}\n")

    return redirect("/donors")

# Donors list page
@app.route("/donors")
def donors():
    data = []
    try:
        with open(FILE, "r") as f:
            for line in f:
                data.append(line.strip().split(","))
    except FileNotFoundError:
        data = []

    return render_template("donors.html", donors=data)

if __name__ == "__main__":
    app.run(debug=True)

