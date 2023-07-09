import mysql.connector
from logging import ERROR, CRITICAL


class Database():
    """A database"""

    def __init__(self, *, host: str, username: str, password: str, database_name: str, log: classmethod):
        self.host = host
        self.username = username
        self.password = password
        self.database_name = database_name
        self.log = log
        self.database = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database_name
        )
        self.cursor = self.database.cursor()

    def select(self, request: str):
        """Do a select request to database

        Args:
            request (str): The select request to do
        
        Returns:
            list[tuple]: The result of the database
        """
        
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        
        return result

    def insert_or_update(self, request: str):
        """Do a insert or update request to database

        Args:
            request (str): The insert or update request to do
        """
        
        self.cursor.execute(request)
        self.database.commit()
    
    def is_connected(self):
        """Check if the database is connected
        
        Returns:
            bool: If the database is connected
        """
        
        return self.database.is_connected()

    def close(self):
        """Close connexion with database
        """
        
        self.cursor.close()
        self.database.close()
