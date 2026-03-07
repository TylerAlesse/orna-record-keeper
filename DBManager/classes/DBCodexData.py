class DBCodexData:
    __slots__ = 'ID', 'type', 'tier', 'name',\
                'event', 'status', 'manifested', 'kills', 'filepath'

    ID: int
    type: str
    tier: int
    name: str
    event: str|None
    status: str
    manifested: int
    kills: int
    filepath: str|None

    def __init__(self, _id: int, _type: str, _tier: int, _name: str,
                 _event: str|None, _status: str, _manifest: int,
                 _kills: int, _filepath: str|None) -> None:
        self.ID: int = _id
        self.type: str = _type
        self.tier: int = _tier
        self.name: str = _name
        self.event: str|None = _event
        self.status: str = _status
        self.manifested: int = _manifest
        self.kills: int = _kills
        self.filepath: str|None = _filepath

    @classmethod
    def getAttributeType(cls, name):
        return cls.__annotations__[name]

    @staticmethod
    def createFromTuple(data: tuple) -> "DBCodexData":
        slots = DBCodexData.__slots__
        if not data.__len__() == slots.__len__():
            raise ValueError('createFromSQLite() failed: ' \
                            f'Parameter "data" was not length {slots.__len__()}')

        for i in range(0, slots.__len__()):
            slotType = DBCodexData.getAttributeType(slots[i])
            if not isinstance(data[i], slotType):
                raise ValueError('createFromSQLite() failed: ' \
                                f'data[{i}] was not of type {slotType}')

        return DBCodexData(data[0], data[1], data[2], data[3],
                data[4], data[5], data[6], data[7], data[8])

    def exportJSON(self) -> str:
        if self.event == None:
            eventName = "null"
        else:
            eventName = f'"{self.event}"'

        content =f'"ID":{self.ID},'\
                 f'"Type":"{self.type}",'\
                 f'"Tier":{self.tier},'\
                 f'"Name":"{self.name}",'\
                 f'"Event":{eventName},'\
                 f'"Status":"{self.status}",'\
                 f'"Manifested":{self.manifested},'\
                 f'"Kills":{self.kills},'\
                 f'"Filepath":"{self.filepath}"'
        
        return f'{{{content}}}'