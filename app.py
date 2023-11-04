from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        #data = dict(request.form)

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        available_date = request.form["date"]
        occupation = request.form["occupation"]
        print(first_name, last_name, email, available_date, occupation)

        #print(data)

    return render_template("index.html")

app.run(debug=True, port=5001)
