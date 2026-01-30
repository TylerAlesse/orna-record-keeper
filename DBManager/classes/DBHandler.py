import os
import sqlite3

class DBHandler:
    # Constructor
    def __init__(self, filepath: str, autocommit: bool = True) -> None:
        self.__filepath = filepath
        self.__connection = None
        self.__autocommit = autocommit
        self.__pending = False

    def getFilepath(self) -> str:
        return self.__filepath
    
    def getAutocommit(self) -> bool:
        return self.__autocommit
    
    def setAutocommit(self, val: bool) -> None:
        self.__autocommit = val

    def createConnetion(self) -> None:
        if not os.path.exists(self.__filepath):
            raise FileNotFoundError(f'Could not find: "{self.__filepath}"')
        
        if not self.isConnected():
            self.__connection = sqlite3.connect(
                database=self.__filepath, autocommit=self.__autocommit)

    def closeConnection(self) -> None:
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def isConnected(self) -> bool:
        return (self.__connection is not None)

    def commit(self):
        if self.__connection is None:
            raise AttributeError(f'Class attribute \'DBHandler.__connection\' has not been initialized.')
        
        if self.__pending:
            self.__connection.commit()
    
    def rollback(self):
        if self.__connection is None:
            raise AttributeError(f'Class attribute \'DBHandler.__connection\' has not been initialized.')
        
        if self.__pending:
            self.__connection.rollback()

    def request(self, query, parameters=[]) -> list:
        result = list()
        dbCursor = None
        
        try:
            if self.__connection is None:
                raise AttributeError(f'Class attribute \'DBHandler.__connection\' has not been initialized.')

            dbCursor = self.__connection.cursor()
            result = dbCursor.execute(query, parameters).fetchall()
            
            if self.__autocommit == False:
                self.__pending = True

            return result
        except Exception as err:
            raise err
        finally:
            if(isinstance(dbCursor, sqlite3.Cursor)):
                dbCursor.close()
