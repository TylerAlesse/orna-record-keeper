class DBItemData:
    __slots__ = 'ID', 'Name', 'Tier', 'Type', 'Rarity', 'IsEvent', 'IsRaidDrop', \
                'IsBossScaling', 'BSP', 'PSC', 'Filepath', 'Base64', 'Ignored', 'Removed', 
    
    ID: int
    Name: str
    Tier: int
    Type: str
    Rarity: str
    IsEvent: bool
    IsRaidDrop: bool
    IsBossScaling: bool
    BSP: float
    PSC: int
    Filepath: str
    Base64: str
    Ignored: bool
    Removed: bool

    def __init__(self,
                 ID: int, Name: str, Tier: int, Type: str, Rarity: str,
                 IsEvent: bool, IsRaidDrop: bool, IsBossScaling: bool,
                 BSP: float, PSC: int, Filepath: str, Base64: str, Ignored: bool, Removed: bool) -> None:
        self.ID = ID
        self.Name = Name
        self.Tier = Tier
        self.Type = Type
        self.Rarity = Rarity
        self.IsEvent = IsEvent
        self.IsRaidDrop = IsRaidDrop
        self.IsBossScaling = IsBossScaling
        self.BSP = BSP
        self.PSC = PSC
        self.Filepath = Filepath
        self.Base64 = Base64
        self.Ignored = Ignored
        self.Removed = Removed
    
    @classmethod
    def getAnnotation(cls, name):
        return cls.__annotations__[name]

    @staticmethod
    def createFromTuple(data: tuple) -> "DBItemData":
        slots = DBItemData.__slots__
        if not data.__len__() == slots.__len__():
            raise ValueError(f'data was not length {slots.__len__()}')

        for i in range(0, slots.__len__()):
            slotType = DBItemData.getAnnotation(slots[i])
            if not isinstance(data[i], slotType):
                raise ValueError(f'data[{i}] was not of type {slotType}')

        return DBItemData(
            data[0], data[1], data[2], data[3], data[4],
            data[5], data[6], data[7], data[8], data[9],
            data[10], data[11], data[12], data[13]
        )

    def exportJSON(self) -> str:
        content = f'"ID":{self.ID},'\
                  f'"Name":"{self.Name}",'\
                  f'"Tier":{self.Tier},'\
                  f'"Type":"{self.Type}",'\
                  f'"Rarity":"{self.Rarity}",'\
                  f'"IsEvent":{self.IsEvent},'\
                  f'"IsRaidDrop":{self.IsRaidDrop},'\
                  f'"IsBossScaling":{self.IsBossScaling},'\
                  f'"BSP":{self.BSP},'\
                  f'"PSC":{self.PSC},'\
                  f'"Filepath":"{self.Filepath}",'\
                  f'"Base64":"{self.Base64}",'\
                  f'"Ignored":{self.Ignored},'\
                  f'"Removed":{self.Removed}'
        
        return f'{{{content}}}'