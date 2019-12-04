from flask import render_template, url_for, redirect, request

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


    @app.route('/example/<string:airport>')
    def test(airport):
        flight1 = db.getFlight('1')
        db.addFlight('2019-11-24 16:38:29', '2019-11-24 22:38:35')
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

    # Define pages for project

    # Page to display flight info
    @app.route('/flight')
    def flight():
        Flightcolumns = db.getInfo('1')
        return render_template('flight.html',
                               title='Airport Monitor',
                               columns=Flightcolumns
                               )

    # Form to insert flight
    @app.route('/form',methods=["POST","GET"])
    def form():
        if request.method == "POST":
            gate = request.form['Gate']
            airplane = request.form['Airplane']
            pilot = request.form['Pilot']
            passenger = request.form['Passenger']
            ## Add the Flight based on the info here
            ## Have to input in the database
            return redirect(url_for('flight'))
        else: return render_template('addflight.html')

# Flight, Gate, Airplane, Pilot, BaggageClaim, Passenger Count

    # Page to display gate info
    @app.route('/gateinfo',methods=["GET"])
    def gate():
        #get all gates info
        # Three Columns gate Airplane last one(If airplane is null then return empty)
        gate = db.getGate('1')
        print(gate)
        return render_template('gate.html',
                               columns=gate)

    # Page to search for passengers and display results
    # Page to delete flights
    # Page to delete passengers

    # Page to update gate gate
    # Page to update gate airplane
    # Page to update gate pilot

