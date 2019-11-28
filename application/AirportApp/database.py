from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base



class Database:

    def __init__(self, app):
        """
        This Class will take the project app as a parameter and connect it to the given database.
        The tunneling code is for testing it in local machines, the server itself does not need to tunnel.
        """
        mysql_user = "root"
        mysql_pass = "team7"
        db_port = 3306
        db_name = "mydb"

        ################################################################################################################
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TUNNELING INFORMATION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        #                   This is needed only for local testing. Remove before merging into master                   #
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        from sshtunnel import SSHTunnelForwarder

        remote_user = "ubuntu"
        remote_key = "./server/675team7.pem"
        remote_host = "ec2-18-223-133-52.us-east-2.compute.amazonaws.com"
        remote_port = 22
        localhost = "127.0.0.1"

        server = SSHTunnelForwarder(
            ssh_address_or_host=(remote_host, remote_port),
            ssh_username=remote_user,
            ssh_pkey=remote_key,
            remote_bind_address=(localhost, db_port),
        )

        server.start()
        db_port = server.local_bind_port
        ################################################################################################################

        app.config['SQLALCHEMY_DATABASE_URI'] = r"mysql://%s:%s@127.0.0.1:%s/%s" % (mysql_user,
                                                                                    mysql_pass,
                                                                                    db_port,
                                                                                    db_name)

        # DB will be used for querying and inserting
        self.DB = SQLAlchemy(app)
        # Base will be used to access tables
        self.Base = automap_base()
        self.Base.prepare(self.DB.engine, reflect=True, schema=db_name)

    def getTable(self, table):
        """
        Function will take table name as string parameter and return the database table

        Following tables are available (case sensitive):
            Airplane
            Airport
            BaggageClaim
            Company
            Employee
            Employment
            Flight
            Gate
            hires
            Luggage
            Passenger
            Pilot
            Ticket

        For attribute name/info, please refer to sql code in the milestone 2 folder
        """
        return self.DB.Table(table, self.DB.MetaData(), autoload=True, autoload_with=self.DB.engine)

    def getFlight(self, flightID):
        """
        Example database query.
        1. Get the table
        2. Query the table via database
        3. Add restrictions

        'idFlight' is the name of the id attribute in the 'Flight' table
        End query with all() to get all entries or first() to get first match.
        """
        Flight = self.getTable('Flight')
        return self.DB.session.query(Flight).filter_by(idFlight=flightID).first()

    """
    Insert functions for Tables:
        Airplane
        Airport
        BaggageClaim
        Company
        Flight
        Gate
        Passenger
        Pilot
    """

    def addAirport(self, name, location):
        Airport = self.getTable('Airport')
        newAirport = Airport.insert().values(name=name,
                                             location=location)
        self.DB.session.execute(newAirport)
        self.DB.session.commit()

    def addFlight(self, departure, arrival):
        Flight = self.getTable('Flight')
        newflight = Flight.insert().values(departure=departure,
                                           arrival=arrival)
        self.DB.session.execute(newflight)
        self.DB.session.commit()

    def addCompany(self, name):
        Company = self.getTable('Company')
        newCompany = Company.insert().values(name=name)
        self.DB.session.execute(newCompany)
        self.DB.session.commit()

    def addAirplane(self, name, idCompany, idFlight):
        Airplane = self.getTable('Airplane')
        newAirplane = Airplane.insert().values(name=name,
                                               idCompany=idCompany,
                                               idFlight=idFlight)
        self.DB.session.execute(newAirplane)
        self.DB.session.commit()

    def addGate(self, name, idAirplane, idAirport):
        Gate = self.getTable('Gate')
        newGate = Gate.insert().values(name=name,
                                               idAirplane=idAirplane,
                                               idAirport=idAirport)
        self.DB.session.execute(newGate)
        self.DB.session.commit()

    def addPilot(self, name, idFlight):
        Pilot = self.getTable('Pilot')
        newPilot = Pilot.insert().values(name=name,
                                               idFlight=idFlight)
        self.DB.session.execute(newPilot)
        self.DB.session.commit()

    def addBaggageClaim(self, name, idAirport):
        BaggageClaim = self.getTable('BaggageClaim')
        newBaggageClaim = BaggageClaim.insert().values(name=name,
                                               idAirport=idAirport)
        self.DB.session.execute(newBaggageClaim)
        self.DB.session.commit()

    def addPassenger(self, name, idFlight):
        Passenger = self.getTable('Passenger')
        newPassenger = Passenger.insert().values(name=name,
                                               idFlight=idFlight)
        self.DB.session.execute(newPassenger)
        self.DB.session.commit()


    # Define classes here to access database

    # FLIGHT TABLE
    # Flight, Airplane, Gate, Pilot, BaggageClaim, Passenger Count

    def getInfo(self, airportID):
        # grab needed tables
        Flight = self.getTable('Flight')
        Airplane = self.getTable('Airplane')
        Gate = self.getTable('Gate')
        Pilot = self.getTable('Pilot')
        BaggageClaim = self.getTable('BaggageClaim')
        Passenger = self.getTable('Passenger')
        list = []

        allFlights = [row[0] for row in self.DB.session.query(Flight.columns.idFlight).distinct()]
        for id in allFlights:

            # grab necessary variables
            retAirplane = self.DB.select([Airplane.columns.name]).where(Airplane.columns.idFlight == id)
            retPilot = self.DB.select([Pilot.columns.name]).where(Pilot.columns.idFlight == id)
            retBag = self.DB.select([BaggageClaim.columns.name]).where(BaggageClaim.columns.idAirport == airportID)
            passCount = self.DB.session.query(Passenger).filter(Passenger.columns.idFlight == id).count()

            # execute sql code
            _A = self.DB.session.execute(retAirplane)
            A = [row[0] for row in _A]
            _P = self.DB.session.execute(retPilot)
            P = [row[0] for row in _P]
            _B = self.DB.session.execute(retBag)
            B = [row[0] for row in _B]

            # grab airplane ID for gate
            airplaneIDSQL = self.DB.select([Airplane.columns.idAirplane]).where(Airplane.columns.idFlight == id)
            airplaneID = self.DB.session.execute(airplaneIDSQL)
            retGate = self.DB.select([Gate.columns.name]).where(Gate.columns.idAirplane == airplaneID and Gate.columns.idAirport == airportID)
            _G = self.DB.session.execute(retGate)
            G = [row[0] for row in _G]

            list.append((id, A, G, P, B, passCount))
        return list

    # GATE TABLE
    # Gates

    # SEARCH PASSENGER
    # Passenger

    # INSERT FLIGHT

    # DELETE FLIGHT
    # DELETE PASSENGER

    # UPDATE GATE
    # UPDATE AIRPLANE
    # UPDATE PILOT
