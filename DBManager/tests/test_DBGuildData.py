import pytest

from classes.DBGuildData import DBGuildData

@pytest.fixture
def mock_DBGuildData() -> DBGuildData:
    return DBGuildData(81, "Traveler's Guild", 29, 8283)

def test_DBGuildData_init(mock_DBGuildData: DBGuildData) -> None:
    assert mock_DBGuildData.PlayerLevel == 81
    assert mock_DBGuildData.Name == "Traveler's Guild"
    assert mock_DBGuildData.Level == 29
    assert mock_DBGuildData.EXP == 8283
    assert mock_DBGuildData.TableName == "GuildData"

def test_DBGuildData_createFromTuple() -> None:
    input = (83, "Blades of Finesse", 30, 9133)
    actual = DBGuildData.createFromTuple(input)
    assert type(actual) is DBGuildData
    assert actual.PlayerLevel == 83
    assert actual.Name == "Blades of Finesse"
    assert actual.Level == 30
    assert actual.EXP == 9133

def test_DBGuildData_createFromTuple_BadLength() -> None:
    with pytest.raises(ValueError):
        input = (80, "Guild Name")
        DBGuildData.createFromTuple(input)

def test_DBGuildData_createFromTuple_BadType() -> None:
    with pytest.raises(TypeError):
        input = ("Incorrect", "Seer's Guild", 56, 30801)
        DBGuildData.createFromTuple(input)

def test_DBGuildData_exportJSON(mock_DBGuildData: DBGuildData) -> None:
    expected = '{"PlayerLevel":81,"Name":"Traveler\'s Guild","Level":29,"EXP":8283}'
    actual = mock_DBGuildData.exportJSON()
    assert actual == expected