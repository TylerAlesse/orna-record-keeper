import pytest

from types import UnionType
from classes.DBPlayerRecordData import DBPlayerRecordData

@pytest.fixture
def mock_DBPlayerRecordData() -> DBPlayerRecordData:
    return DBPlayerRecordData(
        81, "11/19/2025", 3463529, 3481, # Lv, Date, EXP, Playtime
        1310, 67, 1515,                  # Global, Regional, Competitive (Rank)
        512000, 257400, 253700,          # Monster, Boss, Player (Kills)
        13458, 286, 5765, 21934,         # Quests, Taken, Explored, Dungeons
        193, 230, 4190,                  # Monuments, Towers, Coliseums
        20718, 2429, 5506664, 816, 309,  # Items, Fish, Distance, Codex
        "Here be notes", None            # Notes, Deleted
    )

def test_DBPlayerRecordData_init(mock_DBPlayerRecordData: DBPlayerRecordData) -> None:
    assert mock_DBPlayerRecordData.Level == 81
    assert mock_DBPlayerRecordData.DateObtained == "11/19/2025"
    assert mock_DBPlayerRecordData.TotalEXP == 3463529
    assert mock_DBPlayerRecordData.Playtime == 3481
    assert mock_DBPlayerRecordData.GlobalRank == 1310
    assert mock_DBPlayerRecordData.RegionalRank == 67
    assert mock_DBPlayerRecordData.CompetitiveRank == 1515
    assert mock_DBPlayerRecordData.MonsterKills == 512000
    assert mock_DBPlayerRecordData.BossKills == 257400
    assert mock_DBPlayerRecordData.PlayerKills == 253700
    assert mock_DBPlayerRecordData.QuestsCompleted == 13458
    assert mock_DBPlayerRecordData.AreasTaken == 286
    assert mock_DBPlayerRecordData.AreasExplored == 5765
    assert mock_DBPlayerRecordData.DungeonsCompleted == 21934
    assert mock_DBPlayerRecordData.MonumentsCompleted == 193
    assert mock_DBPlayerRecordData.TowersCompleted == 230
    assert mock_DBPlayerRecordData.ColiseumsCompleted == 4190
    assert mock_DBPlayerRecordData.ItemsUpgraded == 20718
    assert mock_DBPlayerRecordData.FishCaught == 2429
    assert mock_DBPlayerRecordData.DistanceTravelled == 5506664
    assert mock_DBPlayerRecordData.Reputation == 816
    assert mock_DBPlayerRecordData.Codex == 309
    assert mock_DBPlayerRecordData.Notes == "Here be notes"
    assert mock_DBPlayerRecordData.Deleted == None
    assert mock_DBPlayerRecordData.TableName == "PlayerRecordData"

def test_DBPlayerRecordData_createFromTuple() -> None:
    input = (
        30, "11/19/2020", 5565, 1021, # Lv, Date, EXP, Playtime
        25000, 12000, 9000,           # Global, Regional, Competitive (Rank)
        51200, 25740, 25370,          # Monster, Boss, Player (Kills)
        158, 26, 57, 21,              # Quests, Taken, Explored, Dungeons
        10, 0, 125,                   # Monuments, Towers, Coliseums
        980, 112, 55064, 816, 109,    # Items, Fish, Distance, Codex
        "Here be notes", None         # Notes, Deleted
    )
    actual = DBPlayerRecordData.createFromTuple(input)
    assert type(actual) is DBPlayerRecordData
    assert actual.Level == 30
    assert actual.DateObtained == "11/19/2020"
    assert actual.TotalEXP == 5565
    assert actual.Playtime == 1021
    assert actual.GlobalRank == 25000
    assert actual.RegionalRank == 12000
    assert actual.CompetitiveRank == 9000
    assert actual.MonsterKills == 51200
    assert actual.BossKills == 25740
    assert actual.PlayerKills == 25370
    assert actual.QuestsCompleted == 158
    assert actual.AreasTaken == 26
    assert actual.AreasExplored == 57
    assert actual.DungeonsCompleted == 21
    assert actual.MonumentsCompleted == 10
    assert actual.TowersCompleted == 0
    assert actual.ColiseumsCompleted == 125
    assert actual.ItemsUpgraded == 980
    assert actual.FishCaught == 112
    assert actual.DistanceTravelled == 55064
    assert actual.Reputation == 816
    assert actual.Codex == 109
    assert actual.Notes == "Here be notes"
    assert actual.Deleted == None

def test_DBPlayerRecordData_createFromTuple_BadLength() -> None:
    with pytest.raises(ValueError):
        input = (30, "11/19/2020", 5565, 1021, None)
        DBPlayerRecordData.createFromTuple(input)

def test_DBPlayerRecordData_createFromTuple_BadType() -> None:
    with pytest.raises(TypeError):
        input = (
            30, "11/19/2020", 5565, 1021, # Lv, Date, EXP, Playtime
            25000, 12000, "9000",         # Global, Regional, Competitive (Rank)
            51200, 25740, 25370,          # Monster, Boss, Player (Kills)
            158, 26, 57, 21,              # Quests, Taken, Explored, Dungeons
            10, 0, 125,                   # Monuments, Towers, Coliseums
            980, 112, 55064, 816, 109,    # Items, Fish, Distance, Codex
            "Here be notes", None         # Notes, Deleted
        )
        DBPlayerRecordData.createFromTuple(input)

def test_DBPlayerRecordData_exportJSON(mock_DBPlayerRecordData: DBPlayerRecordData) -> None:
    expected = '{"Level":81,"DateObtained":"11/19/2025","TotalEXP":3463529,"Playtime":3481,'\
                '"GlobalRank":1310,"RegionalRank":67,"CompetitiveRank":1515,'\
                '"MonsterKills":512000,"BossKills":257400,"PlayerKills":253700,"QuestsCompleted":13458,'\
                '"AreasTaken":286,"AreasExplored":5765,'\
                '"DungeonsCompleted":21934,"MonumentsCompleted":193,"TowersCompleted":230,"ColiseumsCompleted":4190,'\
                '"ItemsUpgraded":20718,"FishCaught":2429,"DistanceTravelled":5506664,'\
                '"Reputation":816,"Codex":309,'\
                '"Notes":"Here be notes"}'
    
    actual = mock_DBPlayerRecordData.exportJSON()
    assert actual == expected