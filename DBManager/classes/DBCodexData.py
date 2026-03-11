class DBCodexData:
    __slots__ = 'ID', 'Type', 'Tier', 'Name',\
                'Event', 'Status', 'Manifested', 'Kills', 'Filepath'

    ID: int
    Type: str
    Tier: int
    Name: str
    Event: str|None
    Status: str
    Manifested: int
    Kills: int
    Filepath: str|None

    def __init__(self, _id: int, _type: str, _tier: int, _name: str,
                 _event: str|None, _status: str, _manifest: int,
                 _kills: int, _filepath: str|None) -> None:
        self.ID: int = _id
        self.Type: str = _type
        self.Tier: int = _tier
        self.Name: str = _name
        self.Event: str|None = _event
        self.Status: str = _status
        self.Manifested: int = _manifest
        self.Kills: int = _kills
        self.Filepath: str|None = _filepath

    @classmethod
    def getAnnotation(cls, name):
        return cls.__annotations__[name]

    @staticmethod
    def createFromTuple(data: tuple) -> "DBCodexData":
        slots = DBCodexData.__slots__
        if not data.__len__() == slots.__len__():
            raise ValueError(f'data was not length {slots.__len__()}')

        for i in range(0, slots.__len__()):
            slotType = DBCodexData.getAnnotation(slots[i])
            if not isinstance(data[i], slotType):
                raise ValueError(f'data[{i}] was not of type {slotType}')

        return DBCodexData(
            data[0], data[1], data[2], data[3],
            data[4], data[5], data[6], data[7], data[8]
        )

    def exportJSON(self) -> str:
        if self.Event == None:
            eventName = "null"
        else:
            eventName = f'"{self.Event}"'

        content =f'"ID":{self.ID},'\
                 f'"Type":"{self.Type}",'\
                 f'"Tier":{self.Tier},'\
                 f'"Name":"{self.Name}",'\
                 f'"Event":{eventName},'\
                 f'"Status":"{self.Status}",'\
                 f'"Manifested":{self.Manifested},'\
                 f'"Kills":{self.Kills},'\
                 f'"Filepath":"{self.Filepath}"'
        
        return f'{{{content}}}'