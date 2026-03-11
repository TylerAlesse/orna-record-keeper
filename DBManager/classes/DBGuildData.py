class DBGuildData:
    __slots__ = 'PlayerLevel', 'Name', 'Level', 'EXP'

    PlayerLevel: int
    Name: str
    Level: int
    EXP: int

    def __init__(self, PlayerLevel: int, Name: str, Level: int, EXP: int) -> None:
        self.PlayerLevel = PlayerLevel
        self.Name = Name
        self.Level = Level
        self.EXP = EXP

    @classmethod
    def getAnnotation(cls, name):
        return cls.__annotations__[name]

    @staticmethod
    def createFromTuple(data: tuple) -> "DBGuildData":
        slots = DBGuildData.__slots__
        if not data.__len__() == slots.__len__():
            raise ValueError(f'data was not length {slots.__len__()}')

        for i in range(0, slots.__len__()):
            slotType = DBGuildData.getAnnotation(slots[i])
            if not isinstance(data[i], slotType):
                raise ValueError(f'data[{i}] was not of type {slotType}')

        return DBGuildData(data[0], data[1], data[2], data[3])
    
    def exportJSON(self) -> str:
        content = f'"PlayerLevel":{self.PlayerLevel},'\
                  f'"Name":"{self.Name}",'\
                  f'"Level":{self.Level},'\
                  f'"EXP":{self.EXP}'

        return f'{{{content}}}'