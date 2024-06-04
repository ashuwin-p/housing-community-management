# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~

"""
DISCLAIMER:
    This module represents a collaborative effort undertaken by a group of students.
    The latest update occurred on December 26, 2023. This code is tailored to fulfill specific functionalities within its designated scope.
    Users are encouraged to review, comprehend, and customize the code to fit their unique project requirements. 
    We strongly advise performing comprehensive testing and validation to ensure compliance with project specifications before deploying it in a live environment.
    Kindly use this code responsibly, adhering to applicable guidelines and best practices. 
    Remember, this project is a part of academic coursework and should be approached in that context.
"""

# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~


# Import Section

# $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $

from flask import Flask, render_template, url_for, request, redirect

from occupant import (
    PaymentStrategy,
    OneBHKPayment,
    TwoBHKPayment,
    ThreeBHKPayment,
    PaymentState,
    PaidState,
    UnpaidState,
    Observer,
    PaymentObserver,
    PaymentDB,
    OCCUPANT_DB,
    OCCUPANT,
)

from client import CLIENT_DB, Client

from housingcommunity import (
    HousingCommunity,
    HC_ERROR,
    Flat,
    State,
    UnoccupiedState,
    OccupiedState,
)

from validation import (
    ValidationException,
    ClientValidationException,
    OccupantValidationException,
    Validation,
    Validations,
)

from ps import (
    PaymentStrategy,
    OneBHKPayment,
    TwoBHKPayment,
    ThreeBHKPayment,
)

from admin import Admin

# $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $ - $

app = Flask(__name__)


class User:
    _current = None


@app.route("/")
def home():
    return render_template("home.html")


# { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ }


@app.route("/al.html")
def admin():
    return render_template("al.html")


@app.route("/admin/login", methods=["POST"])
def admin_login():
    user_id = request.form["userId"]
    password = request.form["password"]

    if Admin.validate_credential(user_id, password):
        # Redirect to admin.html upon successful login
        return redirect(url_for("admin_panel"))
    else:
        # Show invalid credentials alert using JavaScript alert
        return """
        <script>
            alert("Invalid credentials");
            window.location.href = '/al.html';
        </script>
        """


@app.route("/admin/panel")
def admin_panel():
    return render_template("admin_panel.html")


@app.route("/unoccu.html")
def unoccu():
    hc = HousingCommunity.GET_HC()
    unoccupied_flats = hc.get_unoccupied_flats_info()
    return render_template("unoccu.html", unoccupied_flats=unoccupied_flats)


@app.route("/occu.html")
def occu():
    hc = HousingCommunity.GET_HC()
    unoccupied_flats = hc.list_occupied_flats()
    return render_template("occu.html", unoccupied_flats=unoccupied_flats)


@app.route("/add_block.html", methods=["GET", "POST"])
def add_block():
    hc = HousingCommunity.GET_HC()
    if request.method == "GET":
        return render_template("/add_block.html")
    elif request.method == "POST":
        block = request.form["block"]
        if block.isalpha():
            hc.add_block(block)
            return redirect(url_for("add_block"))
        else:
            return "Please enter alphabets only for the block name."


@app.route("/add_flat.html", methods=["GET", "POST"])
def add_flat():
    hc = HousingCommunity.GET_HC()

    if request.method == "GET":
        blocks = hc.list_blocks()
        return render_template("/add_flat.html", blocks=blocks)

    elif request.method == "POST":
        block_no = request.form["block"]
        flat_no = request.form["flat_no"]
        bhk = int(request.form["bhk"])

        try:
            new_flat = Flat(block_no, flat_no, bhk)
            hc.add_flat(new_flat)
            return redirect(url_for("add_flat"))
        except HC_ERROR as e:
            return f"Error: {str(e)}"


@app.route("/payments")
def display_payments():
    payment_rows = PaymentDB.get_payments()
    return render_template("payments.html", payment_rows=payment_rows)


# { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ }


@app.route("/or.html")
def Occupant_Registration():
    hc = HousingCommunity.GET_HC()
    unoccupied_flats = hc.get_unoccupied_flats_info()
    return render_template("or.html", unoccupied_flats=unoccupied_flats)


def choose_payment_stategy(flat):
    if flat._bhk == 1:
        return OneBHKPayment()
    elif flat._bhk == 2:
        return TwoBHKPayment()
    elif flat._bhk == 3:
        return ThreeBHKPayment()
    else:
        return None


@app.route("/Osubmit", methods=["POST"])
def submit_occupant_registration():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        aadhar = request.form.get("aadhar")
        email = request.form.get("email")
        password = request.form.get("password")
        selected_flat = request.form.get("unoccupied_flats")
        flat_details = selected_flat.split("-")
        block_no = flat_details[0]
        flat_no = flat_details[1]
        hc = HousingCommunity.GET_HC()
        flat = hc.get_flat_by_details(block_no, flat_no)
        payment_strategy = choose_payment_stategy(flat)
        occupant = OCCUPANT(
            name, phone, aadhar, email, password, block_no, flat_no, payment_strategy
        )
        flat.occupy(occupant)
        return "Occupant registered successfully!"
    return "Error submitting form. Please try again."


@app.route("/ol.html", methods=["GET", "POST"])
def Occupant_Login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if OCCUPANT_DB.validate_credential(email, password):
            User._current = OCCUPANT_DB.get_occupant(email)
            return redirect(url_for("occupant_page"))
        else:
            return render_template(
                "ol.html", error="Invalid credentials. Please try again."
            )
    return render_template("ol.html")


@app.route("/occupant")
def occupant_page():
    return render_template("occupant_panel.html")


@app.route("/occupant_payment", methods=["GET"])
def occupant_payment():
    if User._current:
        occupant = User._current
        amount_to_pay = occupant.get_amount()
        return render_template("occu_pay.html", amount_to_pay=amount_to_pay)
    else:
        return redirect(url_for("Occupant_Login"))


@app.route("/make_payment", methods=["POST"])
def make_payment():
    if User._current:
        occupant = User._current
        payment_status = occupant.pay_bill()
        if payment_status:
            amount_to_pay = occupant.get_amount()
            return render_template("occu_pay.html", amount_to_pay=amount_to_pay)
        else:
            return "Payment failed. Please try again."
    else:
        return redirect(url_for("Occupant_Login"))


@app.route("/payment_history")
def payment_history():
    current_occupant_email = User._current._email_id
    payment_history = PaymentDB.get_payment_history(current_occupant_email)

    return render_template("payment_history.html", payment_history=payment_history)


# { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ }


@app.route("/cr.html")
def Client_Registration():
    return render_template("cr.html")


@app.route("/Csubmit", methods=["POST"])
def Csubmit():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]

        new_occupant = Client(name, phone, email, password)

        return render_template("cl.html")


@app.route("/cl.html", methods=["GET", "POST"])
def Client_Login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if CLIENT_DB.validate_credential(email, password):
            User._current = CLIENT_DB.get_client(email)
            return redirect(url_for("client_page"))
        else:
            return render_template(
                "cl.html", error="Invalid credentials. Please try again."
            )
    return render_template("cl.html")


@app.route("/client")
def client_page():
    client_name = User._current._name
    hc = HousingCommunity.GET_HC()
    unoccupied_flats = hc.get_unoccupied_flats_info()
    return render_template(
        "client.html", client_name=client_name, unoccupied_flats=unoccupied_flats
    )


# { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ } { ~ }

if __name__ == "__main__":
    app.run()
