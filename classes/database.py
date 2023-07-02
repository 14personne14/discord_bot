import mysql.connector


class Database():
    """A database"""

    def __init__(self, *, host: str, username: str, password: str, database_name: str):
        self.host = host
        self.username = username
        self.password = password
        print(password)
        self.database_name = database_name
        self.database = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database_name
        )
        self.cursor = self.database.cursor()

    def request(self, request: str):
        """Do a request to database

        Args:
            request (str): The request to do
        """
        
        self.cursor.execute(request)
        self.database.commit()

    def close(self):
        """Close connexion with database
        """
        
        self.cursor.close()
        self.database.close()
