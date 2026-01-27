class DBEquipmentCollection:
    def __init__(self, ID: int, QualityPercent: int, QualityName: str, IsPerfect: bool) -> None:
        self.ID = ID
        self.QualityPercent = QualityPercent
        self.QualityName = QualityName
        self.IsPerfect = IsPerfect

    def exportJSON(self) -> str:
        content = f'ID:{self.ID},'\
                  f'QualityPercent:{self.QualityPercent},'\
                  f'QualityName:"{self.QualityName}",'\
                  f'IsPerfect:{self.IsPerfect}'
                  
        return f'{{{content}}}'