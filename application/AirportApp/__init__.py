from flask import Flask, render_template

try:
    from .database import Database
except ModuleNotFoundError:
    from database import Database

app = Flask(__name__)
db = Database(app)


# Every web page needs a routing like the one below for home
# These routes can pass variables into the function below
@app.route('/')
def homepage():
    return render_template('home.html')


if __name__ == "__main__":
    app.run()
