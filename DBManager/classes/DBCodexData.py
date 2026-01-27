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
    
    def exportJSON(self) -> str:
        if self.event == None:
            eventName = "null"
        else:
            eventName = f'"{self.event}"'

        content =f'ID:{self.ID},'\
                 f'Type:"{self.type}",'\
                 f'Tier:{self.tier},'\
                 f'Name:"{self.name}",'\
                 f'Event:{eventName},'\
                 f'Status:"{self.status}",'\
                 f'Manifested:{self.manifested},'\
                 f'Kills:{self.kills}'
        
        return f'{{{content}}}'