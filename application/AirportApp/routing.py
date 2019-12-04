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
        return render_template('coverpage.html',
                               title='Oakland Airport')

    # Page after entering through index/welcome page
    @app.route('/home')
    def homepage():
        return render_template('home.html', title='Oakland Airport Home Page')

    # Page to display all info on flights
    @app.route('/flight')
    def flights():
        return render_template('flight.html', title='Flights')

    # Page will contain form to add a flight
    @app.route('/addFlight')
    def addFlights():
        return render_template('addFlight.html', title='Add a Flight')

    # Page will delete a specified flight
    # NOTE: This feature will probably be built into flight page and not need its own
    @app.route('/deleteFlight')
    def deleteFlights():
        return render_template('deleteFlight.html', title='Delete a Flight')

    # Page will search for passengers and display them
    @app.route('/passenger')
    def passengers():
        return render_template('passenger.html', title='Welcome Passengers')

    # Page will display all passengers
    # NOTE: This can be built into the passenger search
    @app.route('/infoPassenger')
    def infoPassengers():
        return render_template('infoPassenger.html', title='Passengers Info')

    # Page will delete specified passenger
    @app.route('/deletePassenger')
    def deletePassengers():
        return render_template('deletePassenger.html', title='Delete a Passengers')

    # Page will display all gates
    @app.route('/gate')
    def gate():
        return render_template('gate.html', title='Gate')

    # Page will display all gate?
    # NOTE: Not sure difference between this one and above
    @app.route('/gateInfo')
    def gateInfo():
        return render_template('gateInfo.html', title='Gate Info')

    # Page will update gate info
    # NOTE: This feature will probably be built into gate page and not need its own
    @app.route('/gateUpdate')
    def gateUpdate():
        return render_template('gateUpdate.html', title='Gate Update')

    # Page will update airplane info
    @app.route('/airplane')
    def airplane():
        return render_template('airplane.html', title='Airplanes')

    # Page will update pilot info
    @app.route('/pilot')
    def pilot():
        return render_template('pilot.html', title='Pilots')

    # General FAQ/about page for our project
    @app.route('/support')
    def support():
        return render_template('support.html', title='Support')

    ####################################################################################################################
    #                                                  TESTS                                                           #
    ####################################################################################################################

    @app.route('/example/<string:airport>')
    def test(airport):
        flight1 = db.getFlight('1')
        db.addFlight('2019-11-24 16:38:29', '2019-11-24 22:38:35')
        return render_template('test.html',
                               title='test page',
                               flight=flight1)

    @app.route('/form', methods=["GET", "POST"])
    def form():
        if request.method == "POST":
            name = request.form['name']
            db.addFlight('2019-11-24 16:38:29', '2019-11-24 22:38:35')
            return render_template('home.html')

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

    ####################################################################################################################
    #                                               END TESTS                                                          #
    ####################################################################################################################

    # Define pages for project

    # Page to display flight info
    # Flight, Gate, Airplane, Pilot, BaggageClaim, Passenger Count

    # Page to display gate info

    # Page to search for passengers and display results

    # Form to insert flight

    # Page to delete flights
    # Page to delete passengers

    # Page to update gate gate
    # Page to update gate airplane
    # Page to update gate pilot
