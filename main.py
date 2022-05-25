from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("learn.html")

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route('/practice')
def practice():
    return render_template("practice.html")

@app.route("/about")
def about():
    return render_template("about.html")
    
if __name__ == "__main__":
    app.run(debug=True)