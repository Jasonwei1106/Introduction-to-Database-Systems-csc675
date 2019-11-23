from flask import Flask

try:
    from .routing import Routing
except ModuleNotFoundError:
    from routing import Routing

app = Flask(__name__)
Routing(app)

if __name__ == "__main__":
    app.run()
