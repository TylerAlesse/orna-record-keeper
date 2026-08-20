from classes.TableData import TableData
from classes.DBItemData import DBItemData
from classes.DBEquipmentCollection import DBEquipmentCollection

class EquipmentData(TableData):
    __slots__ = 'ID', 'Name', 'Tier', 'Type', 'Rarity', 'QualityPercent', \
        'QualityName', 'IsPerfect', 'IsEvent', 'IsRaidDrop', 'Filepath'
    
    ID: int
    Name: str
    Tier: int
    Type: str
    Rarity: str
    QualityPercent: int
    QualityName: str
    IsPerfect: bool
    IsEvent: bool
    IsRaidDrop: bool
    Filepath: str
    
    def __init__(self,
                 ID: int, Name: str, Tier: int, Type: str, Rarity: str,
                 QualityPercent: int, QualityName: str, IsPerfect: bool,
                 IsEvent: bool, IsRaidDrop: bool, Filepath: str) -> None:
        self.ID = ID
        self.Name = Name
        self.Tier = Tier
        self.Type = Type
        self.Rarity = Rarity
        self.QualityPercent = QualityPercent
        self.QualityName = QualityName
        self.IsPerfect = IsPerfect
        self.IsEvent = IsEvent
        self.IsRaidDrop = IsRaidDrop
        self.Filepath = Filepath

    @staticmethod
    def createFromClasses(itemData: DBItemData, collectionData: DBEquipmentCollection):
        return EquipmentData(
            itemData.ID, itemData.Name, itemData.Tier, itemData.Type, itemData.Rarity,
            collectionData.QualityPercent, collectionData.QualityName, collectionData.IsPerfect,
            itemData.IsEvent, itemData.IsRaidDrop, itemData.Filepath
        )
    
    @staticmethod
    def createFromTuple(data: tuple) -> "EquipmentData":
        slots = EquipmentData.__slots__
        if not data.__len__() == slots.__len__():
            raise ValueError(f'data was not length {slots.__len__()}')

        for i in range(0, slots.__len__()):
            slotType = EquipmentData.getAnnotation(slots[i])
            if not isinstance(data[i], slotType):
                raise TypeError(f'data[{i}] was not of type {slotType}')

        return EquipmentData(
            data[0], data[1], data[2], data[3], data[4], data[5],
            data[6], data[7], data[8], data[9], data[10]
        )

    def exportJSON(self) -> str:
        content = f'"ID":{self.ID},'\
                  f'"Name":"{self.Name}",'\
                  f'"Tier":{self.Tier},'\
                  f'"Type":"{self.Type}",'\
                  f'"Rarity":"{self.Rarity}",'\
                  f'"QualityPercent":{self.QualityPercent},'\
                  f'"QualityName":"{self.QualityName}",'\
                  f'"IsPerfect":{self.IsPerfect},'\
                  f'"IsEvent":{self.IsEvent},'\
                  f'"IsRaidDrop":{self.IsRaidDrop},'\
                  f'"Filepath":"{self.Filepath}"'\
        
        return f'{{{content}}}'