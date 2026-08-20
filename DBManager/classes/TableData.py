from abc import ABCMeta, abstractmethod
from types import UnionType
from classes.Argument import Argument

class TableData(metaclass=ABCMeta):
    __slots__ = []
    TableName: str

    @classmethod
    def getAnnotation(cls, name):
        return cls.__annotations__[name]

    @classmethod
    def createArgumentsList(cls, ignored: list[str] = []) -> list[Argument]:
        argList: list[Argument] = []

        if cls.TableName is None:
            raise AttributeError("TableName is not set.")

        if cls.__slots__ is None:
            return []

        for name in cls.__slots__:
            if ignored.__contains__(name): continue
            
            attrType = cls.getAnnotation(name)

            if type(attrType) is UnionType:
                neededType = attrType.__args__[0]
                isRequired = False
            else:
                neededType = attrType
                isRequired = True

            argList.append(Argument(name, neededType, None, isRequired))
            
        return argList

    @classmethod
    def createSelectQuery(cls, ignored: list[str] = [], conditions: dict = {}):
        # Quick Pre-Checks
        if cls.TableName == "":
            raise AttributeError("TableName not set")

        if len(cls.__slots__) == 0:
            raise AttributeError("Class has no attributes")

        columnNames = cls.__slots__

        selectColumns = ""
        whereColumns = ""
        whereParameters = []

        for name in columnNames:
            if ignored.__contains__(name):
                continue

            selectColumns += f"{name},"
            cond = conditions.get(name, None)
            if cond:
                whereColumns += f"{name} = ?,"
                whereParameters.append(cond)
        
        if selectColumns == "":
            raise RuntimeError("selectColumns cannot be empty.")
        selectColumns = selectColumns[:-1] # Remove trailing comma
        query = f"SELECT {selectColumns} FROM {cls.TableName}"
        
        if len(whereParameters) > 0:
            whereColumns = whereColumns[:-1] # Remove trailing comma
            query += f" WHERE {whereColumns}"
        
        return query, whereParameters

    @classmethod
    def createUpdateQuery(cls, args: list[Argument], conditions: dict = {}):
        columns = ""
        parameters = []
        for arg in args:
            if arg["val"] is not None:
                columns += f'"{arg["name"]}" = ?,'
                parameters.append(arg["val"])
        
        # Must have at least one valid new value to update
        if len(parameters) == 0:
            raise AttributeError("No valid arguments provided")
        
        columns = columns[:-1]  # remove the last comma
        
        #TODO# Allow for composite key tables to be updated
        query = ""

        # parameters.append(ID)   # add the ID to the parameters
        # query = f"UPDATE {tableName} SET {columns} WHERE ID = ?"
        
        return query, parameters

    @classmethod
    def createInsertQuery(cls, args: list[Argument]):
        columns = ""
        placeholders = ""
        parameters = []
        for arg in args:
            if arg["val"] is None:
                if arg["insertReq"]:
                    raise AttributeError(
                        f'"{arg["name"]}" is required for {cls.TableName}.')
            else:
                columns += f'"{arg["name"]}",'
                placeholders += "?,"
                parameters.append(arg["val"])

        columns = columns[:-1]            # remove the last comma
        placeholders = placeholders[:-1]  # remove the last comma
        query = f"INSERT INTO {cls.TableName} ({columns}) VALUES ({placeholders})"
        return query, parameters

    @classmethod
    def createDeleteQuery(cls):
        raise NotImplementedError("TODO")

    @staticmethod
    @abstractmethod
    def createFromTuple(data: tuple):
        raise NotImplementedError("Implemention required by subclass")

    @abstractmethod
    def exportJSON(self) -> str:
        raise NotImplementedError("Implemention required by subclass")