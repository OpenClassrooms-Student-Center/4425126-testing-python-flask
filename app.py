"""
Starting point of flask application
All routes are defined here
"""
from flask import Flask, render_template, request, session, url_for, redirect
from utilities import init_db
from utilities.user import user
from utilities.calculation import calculation


def create_app(config):
    app = Flask(__name__)
    app.config.from_object("config")
    app.config["TESTING"] = config.get("TESTING")
    init_db()

    @app.route("/", methods=["GET", "POST"])
    def index():
        """This route will calculate the conversions but needs user to login"""
        if "user_id" not in session:
            return redirect(url_for("login"))
        if request.method == "GET":
            return render_template("calculation.html", user_id=session.get("user_id"))
        # taking input
        inp = request.form.get("input")
        base = request.form.get("base")
        # validating input
        if inp in [None, ""] or base is None:
            return (
                render_template(
                    "calculation.html",
                    error="Please enter valid input",
                    user_id=session.get("user_id"),
                ),
                400,
            )
        # conversion
        try:
            dec_val = int(inp, int(base))
            bin_val = bin(dec_val).replace("0b", "")
            hex_val = hex(dec_val).replace("0x", "").upper()
            # store in database
            out = calculation.add_calculation(session.get("user_id"), inp, base)
            if out is None:
                return render_template(
                    "calculation.html",
                    error="Could not add in history",
                    user_id=session.get("user_id"),
                )
            return render_template(
                "calculation.html",
                hex=hex_val,
                dec=dec_val,
                bin=bin_val,
                base=base,
                input=inp,
                user_id=session.get("user_id"),
            )
        except:
            return (
                render_template(
                    "calculation.html",
                    error="Please enter valid input",
                    user_id=session.get("user_id"),
                ),
                400,
            )

    @app.route("/dashboard")
    def dashboard():
        """Dashboard route, need to login"""
        if "user_id" not in session:
            return redirect(url_for("index"))

        # loading history
        history = calculation.get_user_history(session.get("user_id"))
        if history is None:
            return render_template(
                "error.html",
                error="Something went wrong, while loading history",
                title="Error",
                user_id=session.get("user_id"),
            )
        output = []
        # generate required output
        for h in history:
            dec_val = int(h[0], h[1])
            hex_val = hex(dec_val).replace("0x", "").upper()
            bin_val = bin(dec_val).replace("0b", "")
            output.append(
                {
                    "input": h[0],
                    "base": h[1],
                    "hex": hex_val,
                    "dec": dec_val,
                    "bin": bin_val,
                }
            )
        return render_template(
            "dashboard.html",
            user_id=session.get("user_id"),
            user_name=session.get("user_name"),
            history=output,
        )

    @app.route("/login", methods=["GET", "POST"])
    def login():
        """Route used for login purpose"""
        if "user_id" in session:
            return redirect(url_for("index"))

        if request.method == "GET":
            return render_template("login.html")

        # getting input
        email = request.form.get("email")
        password = request.form.get("password")
        # validate input
        if email is None or password is None:
            return render_template("login.html", error="Please fill all fields"), 400
        user_data = user.login(email, password)
        if user_data is None:
            return render_template("login.html", error="Invalid email or password"), 403
        # saving session
        session["user_id"] = user_data[0]
        session["user_name"] = user_data[1]
        return redirect(url_for("index"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        """Register user"""
        if "user_id" in session:
            return redirect(url_for("index"))

        if request.method == "GET":
            return render_template("register.html")
        # loading input from form
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        print(name)
        # validating input
        if name is None or password is None or email is None:
            return render_template("register.html", error="Please fill all fields"), 400

        # check for email already exists
        if user.is_email_exists(email) is not None:
            return render_template("register.html", error="Email already exists"), 403

        user_data = user.register(name, email, password)
        if user_data is None:
            return render_template("register.html", error="Could not add user"), 403

        session["user_id"] = user_data[0]
        session["user_name"] = user_data[1]
        return redirect(url_for("index"))

    @app.route("/logout")
    def logout():
        """Clearing the session to make user logout"""
        calculation.clear()
        session.clear()
        return redirect(url_for("index"))

    return app


app = create_app({"TESTING": False})

if __name__ == "__main__":
    app.run()
