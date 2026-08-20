from classes.TableData import TableData

class DBItemCollection(TableData):
    __slots__ = 'ID', 'Quantity'

    ID: int
    Quantity: int
    TableName: str = "ItemCollection"

    def __init__(self, ID: int, Quantity: int) -> None:
        self.ID = ID
        self.Quantity = Quantity

    @staticmethod
    def createFromTuple(data: tuple) -> "DBItemCollection":
        slots = DBItemCollection.__slots__
        if not data.__len__() == slots.__len__():
            raise ValueError(f'data was not length {slots.__len__()}')

        for i in range(0, slots.__len__()):
            slotType = DBItemCollection.getAnnotation(slots[i])
            if not isinstance(data[i], slotType):
                raise TypeError(f'data[{i}] was not of type {slotType}')

        return DBItemCollection(data[0], data[1])
    
    def exportJSON(self) -> str:
        content = f'"ID":{self.ID},'\
                  f'"Quantity":{self.Quantity}'
        return f'{{{content}}}'