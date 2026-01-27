import pytest

from classes.DBCodexData import DBCodexData

@pytest.fixture
def mock_DBCodexData() -> DBCodexData:
    return DBCodexData(2, "Monster", 1, "Bandit", None, "Complete", 1, 5)

def test_DBCodexData_init(mock_CodexData: DBCodexData) -> None:
    assert mock_CodexData.ID == 2
    assert mock_CodexData.type == "Monster"
    assert mock_CodexData.name == "Bandit"
    assert mock_CodexData.event == None
    assert mock_CodexData.status == "Complete"
    assert mock_CodexData.manifested == 1
    assert mock_CodexData.kills == 5

def test_DBCodexData_exportJSON(mock_CodexData: DBCodexData) -> None:
    expected = '{ID:2,Type:"Monster",Tier:1,Name:"Bandit",Event:null,Status:"Complete",Manifested:1,Kills:5}'
    actual = mock_CodexData.exportJSON()
    assert actual == expected