class DBCodexData:
    def __init__(self, _id: int, _type: str, _tier: int, _name: str,
                 _event: str|None, _status: str, _manifest: int, _kills: int) -> None:
        self.ID = _id
        self.type = _type
        self.tier = _tier
        self.name = _name
        self.event = _event
        self.status = _status
        self.manifested = _manifest
        self.kills = _kills
    
    @staticmethod
    def createFromSQLite(data: tuple) -> "DBCodexData":
        # Need to thoroughly check the tuple's data
        if not data.__len__() == 8:
            raise ValueError(f'createFromSQLite() failed: Parameter "data" was not size (8), was ()')

        tempID = data[0]
        tempType = data[1]
        tempTier = data[2]
        tempName = data[3]
        tempEvent = data[4]
        tempStatus = data[5]
        tempManifested = data[6]
        tempKills = data[7]

        return DBCodexData(tempID, tempType, tempTier, tempName,
                tempEvent, tempStatus, tempManifested, tempKills)

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
                 f'"Kills":{self.kills}'
        
        return f'{{{content}}}'