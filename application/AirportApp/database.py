from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base


class Database:

    def __init__(self, app):
        """
        This Class will take the project app as a parameter and connect it to the given database.
        The tunneling code is for testing it in local machines, the server itself does not need to tunnel.
        """
        self.mysql_user = "root"
        self.mysql_pass = "team7"
        self.db_port = 3306
        self.db_name = "mydb"

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
            remote_bind_address=(localhost, self.db_port),
        )

        server.start()
        self.db_port = server.local_bind_port
        ################################################################################################################

        app.config['SQLALCHEMY_DATABASE_URI'] = r"mysql://%s:%s@127.0.0.1:%s/%s" % (self.mysql_user,
                                                                                    self.mysql_pass,
                                                                                    self.db_port,
                                                                                    self.db_name)

        # DB will be used for querying and inserting
        self.DB = SQLAlchemy(app)
        # Base will be used to access tables
        self.Base = automap_base()
        self.Base.prepare(self.DB.engine, reflect=True)

    def getTable(self, table):
        """
        Function will take table name as string parameter and return the database table
        """
        return getattr(self.Base.classes, table)

    # Define classes here to access database
