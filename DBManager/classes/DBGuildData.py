class DBGuildData:
    def __init__(self, PlayerLevel: int, Name: str, Level: int, EXP: int) -> None:
        self.PlayerLevel = PlayerLevel
        self.Name = Name
        self.Level = Level
        self.EXP = EXP
    
    def exportJSON(self) -> str:
        content = f'PlayerLevel:{self.PlayerLevel},'\
                  f'Name:"{self.Name}",'\
                  f'Level:{self.Level},'\
                  f'EXP:{self.EXP}'

        return f'{{{content}}}'