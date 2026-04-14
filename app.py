from flask import Flask, render_template, request, redirect,session 
from database import conn, cursor
from datetime import date, timedelta
today = date.today()
soon_date = today + timedelta(days=30)


import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.secret_key = "pharma_optima_secret_2026"

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        query = "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)"
        values = (name,email,password)

        cursor.execute(query, values)
        conn.commit()

        return "User Registered Successfully"

    return render_template("signup.html")


@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    query = "SELECT * FROM users WHERE email=%s AND password=%s"
    values = (email,password)

    cursor.execute(query, values)
    user = cursor.fetchone()

    if user:
        session["user"] = user[1]
        return redirect("/dashboard")
    else:
        return "Invalid Credentials"
    


@app.route("/view_medicines", methods=["GET", "POST"])
def view_medicines():

    if request.method == "POST":
        search = request.form["search"]

        query = """
        SELECT * FROM medicines
        WHERE drug_name LIKE %s OR drug_id LIKE %s
        """

        cursor.execute(query, ('%' + search + '%', '%' + search + '%'))
        data = cursor.fetchall()

    else:
        cursor.execute("SELECT * FROM medicines")
        data = cursor.fetchall()

    return render_template("view_medicines.html", medicines=data)

@app.route("/add_medicine", methods=["GET", "POST"])
def add_medicine():

    if request.method == "POST":
        drug_id = request.form["drug_id"]
        drug_name = request.form["drug_name"]
        therapeutic_area = request.form["therapeutic_area"]
        molecule_type = request.form["molecule_type"]
        launch_year = request.form["launch_year"]
        region = request.form["region"]
        month_year = request.form["month_year"]
        units_sold = request.form["units_sold"]
        drug_price = request.form["drug_price"]

        query = """
        INSERT INTO medicines
        (drug_id, drug_name, therapeutic_area, molecule_type, launch_year, region, month_year, units_sold, drug_price)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            drug_id, drug_name, therapeutic_area, molecule_type,
            launch_year, region, month_year, units_sold, drug_price
        )

        cursor.execute(query, values)
        conn.commit()

        return redirect("/view_medicines")

    return render_template("add_medicine.html")
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/dashboard")
def dashboard():

    cursor.execute("SELECT COUNT(*) FROM medicines WHERE expiry_date < CURDATE()")
    expired = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*) FROM medicines 
    WHERE expiry_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
    """)
    soon = cursor.fetchone()[0]
    return render_template(
        "dashboard.html",
        expired=expired,
        soon=soon,
        today=today,
        soon_date=soon_date
    )

@app.route("/expiry_date")
def expired_medicines():

    cursor.execute("""
        SELECT * FROM medicines
    """)
    data = cursor.fetchall()
    

    return render_template("expiry_date.html", medicines=data)

@app.route("/delete/<id>")
def delete(id):

    query = "DELETE FROM medicines WHERE drug_id=%s"
    cursor.execute(query, (id,))
    conn.commit()

    return redirect("/view_medicines")


if __name__ == "__main__":
    app.run(debug=True)