class DBItemData:
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
        self.Base64 = ""
        self.Ignored = Ignored
        self.Removed = Removed
    
    def exportJSON(self) -> str:
        content = f'ID:{self.ID},'\
                  f'Name:"{self.Name}",'\
                  f'Tier:{self.Tier},'\
                  f'Type:"{self.Type}",'\
                  f'Rarity:"{self.Rarity}",'\
                  f'IsEvent:{self.IsEvent},'\
                  f'IsRaidDrop:{self.IsRaidDrop},'\
                  f'IsBossScaling:{self.IsBossScaling},'\
                  f'BSP:{self.BSP},'\
                  f'PSC:{self.PSC},'\
                  f'Filepath:"{self.Filepath}",'\
                  f'Base64:"{self.Base64}",'\
                  f'Ignored:{self.Ignored},'\
                  f'Removed:{self.Removed}'
        
        return f'{{{content}}}'