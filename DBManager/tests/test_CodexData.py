import pytest

from classes.DBCodexData import DBCodexData

@pytest.fixture
def mock_DBCodexData() -> DBCodexData:
    return DBCodexData(2, "Monster", 1, "Bandit", None, "Complete", 1, 5)

def test_DBCodexData_init(mock_DBCodexData: DBCodexData) -> None:
    assert mock_DBCodexData.ID == 2
    assert mock_DBCodexData.type == "Monster"
    assert mock_DBCodexData.name == "Bandit"
    assert mock_DBCodexData.event == None
    assert mock_DBCodexData.status == "Complete"
    assert mock_DBCodexData.manifested == 1
    assert mock_DBCodexData.kills == 5

def test_DBCodexData_exportJSON(mock_DBCodexData: DBCodexData) -> None:
    expected = '{ID:2,Type:"Monster",Tier:1,Name:"Bandit",Event:null,Status:"Complete",Manifested:1,Kills:5}'
    actual = mock_DBCodexData.exportJSON()
    assert actual == expected