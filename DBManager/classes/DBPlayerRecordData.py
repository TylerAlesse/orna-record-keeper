from classes.TableData import TableData

class DBPlayerRecordData(TableData):
    __slots__ = 'Level', 'DateObtained', 'TotalEXP', 'Playtime', 'GlobalRank', 'RegionalRank', \
        'CompetitiveRank', 'MonsterKills', 'BossKills', 'PlayerKills', 'QuestsCompleted', \
        'AreasTaken', 'AreasExplored', 'DungeonsCompleted', 'MonumentsCompleted', \
        'TowersCompleted', 'ColiseumsCompleted', 'ItemsUpgraded', 'FishCaught', \
        'DistanceTravelled', 'Reputation', 'Codex', 'Notes', 'Deleted'

    Level: int
    DateObtained: str
    TotalEXP: int|None
    Playtime: int|None
    GlobalRank: int|None
    RegionalRank: int|None
    CompetitiveRank: int|None
    MonsterKills: int|None
    BossKills: int|None
    PlayerKills: int|None
    QuestsCompleted: int|None
    AreasTaken: int|None
    AreasExplored: int|None
    DungeonsCompleted: int|None
    MonumentsCompleted: int|None
    TowersCompleted: int|None
    ColiseumsCompleted: int|None
    ItemsUpgraded: int|None
    FishCaught: int|None
    DistanceTravelled: int|None
    Reputation: int|None
    Codex: int|None
    Notes: str|None
    Deleted: str|None
    TableName: str = "PlayerRecordData"

    def __init__(self,
                 Level: int, DateObtained: str, TotalEXP: int|None, Playtime: int|None,
                 GlobalRank: int|None, RegionalRank: int|None, CompetitiveRank: int|None,
                 MonsterKills: int|None, BossKills: int|None, PlayerKills: int|None,
                 QuestsCompleted: int|None, AreasTaken: int|None, AreasExplored: int|None,
                 DungeonsCompleted: int|None, MonumentsCompleted: int|None,
                 TowersCompleted: int|None, ColiseumsCompleted: int|None,
                 ItemsUpgraded: int|None, FishCaught: int|None, DistanceTravelled: int|None,
                 Reputation: int|None, Codex: int|None,
                 Notes: str|None, Deleted: str|None) -> None:
        self.Level = Level
        self.DateObtained = DateObtained
        self.TotalEXP = TotalEXP
        self.Playtime = Playtime
        self.GlobalRank = GlobalRank
        self.RegionalRank = RegionalRank
        self.CompetitiveRank = CompetitiveRank
        self.MonsterKills = MonsterKills
        self.BossKills = BossKills
        self.PlayerKills = PlayerKills
        self.QuestsCompleted = QuestsCompleted
        self.AreasTaken = AreasTaken
        self.AreasExplored = AreasExplored
        self.DungeonsCompleted = DungeonsCompleted
        self.MonumentsCompleted = MonumentsCompleted
        self.TowersCompleted = TowersCompleted
        self.ColiseumsCompleted = ColiseumsCompleted
        self.ItemsUpgraded = ItemsUpgraded
        self.FishCaught = FishCaught
        self.DistanceTravelled = DistanceTravelled
        self.Reputation = Reputation
        self.Codex = Codex
        self.Notes = Notes
        self.Deleted = Deleted

    @staticmethod
    def createFromTuple(data: tuple) -> "DBPlayerRecordData":
        slots = DBPlayerRecordData.__slots__
        if not data.__len__() == slots.__len__():
            raise ValueError(f'data was not length {slots.__len__()}')

        for i in range(0, slots.__len__()):
            slotType = DBPlayerRecordData.getAnnotation(slots[i])
            if not isinstance(data[i], slotType):
                raise TypeError(f'data[{i}] was not of type {slotType}')

        return DBPlayerRecordData(
            data[0], data[1], data[2], data[3], data[4], data[5],
            data[6], data[7], data[8], data[9], data[10], data[11],
            data[12], data[13], data[14], data[15], data[16], data[17],
            data[18], data[19], data[20], data[21], data[22], data[23]
        )

    def exportJSON(self) -> str:
        content = f'"Level":{self.Level},'\
                  f'"DateObtained":"{self.DateObtained}",'\
                  f'"TotalEXP":{self.TotalEXP},'\
                  f'"Playtime":{self.Playtime},'\
                  f'"GlobalRank":{self.GlobalRank},'\
                  f'"RegionalRank":{self.RegionalRank},'\
                  f'"CompetitiveRank":{self.CompetitiveRank},'\
                  f'"MonsterKills":{self.MonsterKills},'\
                  f'"BossKills":{self.BossKills},'\
                  f'"PlayerKills":{self.PlayerKills},'\
                  f'"QuestsCompleted":{self.QuestsCompleted},'\
                  f'"AreasTaken":{self.AreasTaken},'\
                  f'"AreasExplored":{self.AreasExplored},'\
                  f'"DungeonsCompleted":{self.DungeonsCompleted},'\
                  f'"MonumentsCompleted":{self.MonumentsCompleted},'\
                  f'"TowersCompleted":{self.TowersCompleted},'\
                  f'"ColiseumsCompleted":{self.ColiseumsCompleted},'\
                  f'"ItemsUpgraded":{self.ItemsUpgraded},'\
                  f'"FishCaught":{self.FishCaught},'\
                  f'"DistanceTravelled":{self.DistanceTravelled},'\
                  f'"Reputation":{self.Reputation},'\
                  f'"Codex":{self.Codex},'\
                  f'"Notes":"{self.Notes}"'
        return f'{{{content}}}'