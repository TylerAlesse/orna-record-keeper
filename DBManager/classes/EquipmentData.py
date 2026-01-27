from classes.DBItemData import DBItemData
from classes.DBEquipmentCollection import DBEquipmentCollection

class EquipmentData:
    @staticmethod
    def createFromClasses(itemData: DBItemData, collectionData: DBEquipmentCollection):
        return EquipmentData(
            itemData.ID, itemData.Name, itemData.Tier, itemData.Type, itemData.Rarity,
            collectionData.QualityPercent, collectionData.QualityName, collectionData.IsPerfect,
            itemData.IsEvent, itemData.IsRaidDrop, itemData.Filepath
        )

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

    def exportJSON(self) -> str:
        content = f'ID:{self.ID},'\
                  f'Name:"{self.Name}",'\
                  f'Tier:{self.Tier},'\
                  f'Type:"{self.Type}",'\
                  f'Rarity:"{self.Rarity}",'\
                  f'QualityPercent:{self.QualityPercent},'\
                  f'QualityName:"{self.QualityName}",'\
                  f'IsPerfect:{self.IsPerfect},'\
                  f'IsEvent:{self.IsEvent},'\
                  f'IsRaidDrop:{self.IsRaidDrop},'\
                  f'Filepath:"{self.Filepath}"'\
        
        return f'{{{content}}}'