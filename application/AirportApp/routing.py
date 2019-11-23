from flask import render_template, url_for, redirect

try:
    from .database import Database
except ModuleNotFoundError:
    from database import Database

# This function will be called by init on server start up and establish all routes

def Routing(app):
    # Page routing can pass data into html pages from the database
    # Example: db.getFlight(flightID) will return the flight entry of the given flight id
    db = Database(app)

    # Every web page needs a routing like the one below for home
    # These routes can pass variables into the function below
    @app.route('/')
    def index():
        # Variables and functions can be passed into html files to use
        return render_template('home.html',
                               title='Airport Monitor')

    @app.route('/example')
    def test():
        flight1 = db.getFlight('1')
        return render_template('test.html',
                               title='test page',
                               flight=flight1)

    @app.route('/redirect')
    def redtest():
        """
        Redirect will look for the url of a function
        In this example, 'index' is the name of the function for the home route '/'

        Redirects can also pass variables like render template:
            redirect(url_for('index'), title=redirected)
        These arguments can be used at the redirected page with:
            request.args.get('title')
        """
        return redirect(url_for('index'))