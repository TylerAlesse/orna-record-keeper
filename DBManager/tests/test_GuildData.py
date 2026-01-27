import pytest

from classes.DBGuildData import DBGuildData

@pytest.fixture
def mock_DBGuildData() -> DBGuildData:
    return DBGuildData(81, "Traveler's Guild", 29, 8283)

def test_CodexData_init(mock_DBGuildData: DBGuildData) -> None:
    assert mock_DBGuildData.PlayerLevel == 81
    assert mock_DBGuildData.Name == "Traveler's Guild"
    assert mock_DBGuildData.Level == 29
    assert mock_DBGuildData.EXP == 8283

def test_CodexData_exportJSON(mock_DBGuildData: DBGuildData) -> None:
    expected = '{PlayerLevel:81,Name:"Traveler\'s Guild",Level:29,EXP:8283}'
    actual = mock_DBGuildData.exportJSON()
    assert actual == expected