from classes.TableData import TableData

class DBEquipmentCollection(TableData):
    __slots__ = 'ID', 'QualityPercent', 'QualityName', 'IsPerfect'

    ID: int
    QualityPercent: int
    QualityName: str
    IsPerfect: bool
    TableName = "EquipmentCollection"

    def __init__(self, ID: int, QualityPercent: int, QualityName: str, IsPerfect: bool) -> None:
        self.ID: int = ID
        self.QualityPercent: int = QualityPercent
        self.QualityName: str = QualityName
        self.IsPerfect: bool = IsPerfect

    @staticmethod
    def createFromTuple(data: tuple) -> "DBEquipmentCollection":
        slots = DBEquipmentCollection.__slots__
        if not data.__len__() == slots.__len__():
            raise ValueError(f'data was not length {slots.__len__()}')

        for i in range(0, slots.__len__()):
            slotType = DBEquipmentCollection.getAnnotation(slots[i])
            if not isinstance(data[i], slotType):
                raise TypeError(f'data[{i}] was not of type {slotType}')

        return DBEquipmentCollection(data[0], data[1], data[2], data[3])

    def exportJSON(self) -> str:
        content = f'"ID":{self.ID},'\
                  f'"QualityPercent":{self.QualityPercent},'\
                  f'"QualityName":"{self.QualityName}",'\
                  f'"IsPerfect":{self.IsPerfect}'

        return f'{{{content}}}'