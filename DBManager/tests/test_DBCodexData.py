import pytest

from types import UnionType
from classes.DBCodexData import DBCodexData

@pytest.fixture
def mock_DBCodexData() -> DBCodexData:
    return DBCodexData(2, "Monster", 1, "Bandit", None, "Complete", 1, 5, "bandit.png")

def test_DBCodexData_init(mock_DBCodexData: DBCodexData) -> None:
    assert mock_DBCodexData.ID == 2
    assert mock_DBCodexData.Type == "Monster"
    assert mock_DBCodexData.Tier == 1
    assert mock_DBCodexData.Name == "Bandit"
    assert mock_DBCodexData.Event == None
    assert mock_DBCodexData.Status == "Complete"
    assert mock_DBCodexData.Manifested == 1
    assert mock_DBCodexData.Kills == 5
    assert mock_DBCodexData.Filepath == "bandit.png"

def test_DBCodexData_getAttributeType() -> None:
    assert DBCodexData.getAnnotation("ID") is int
    assert DBCodexData.getAnnotation("Type") is str
    assert DBCodexData.getAnnotation("Tier") is int
    assert DBCodexData.getAnnotation("Name") is str
    assert type(DBCodexData.getAnnotation("Event")) is UnionType
    assert DBCodexData.getAnnotation("Status") is str
    assert DBCodexData.getAnnotation("Manifested") is int
    assert DBCodexData.getAnnotation("Kills") is int
    assert type(DBCodexData.getAnnotation("Filepath")) is UnionType

def test_DBCodexData_createFromTuple() -> None:
    input = (55, "Boss", 2, "Arachne", "Spider's Nest", "Missing", 0, 10, "spider.png")
    actual = DBCodexData.createFromTuple(input)
    assert type(actual) is DBCodexData
    assert actual.ID == 55
    assert actual.Type == "Boss"
    assert actual.Tier == 2
    assert actual.Name == "Arachne"
    assert actual.Event == "Spider's Nest"
    assert actual.Status == "Missing"
    assert actual.Manifested == 0
    assert actual.Kills == 10
    assert actual.Filepath == "spider.png"

def test_DBCodexData_createFromTuple_BadLength() -> None:
    with pytest.raises(ValueError):
        input = (33, "Fails")
        DBCodexData.createFromTuple(input)

def test_DBCodexData_createFromTuple_BadType() -> None:
    with pytest.raises(ValueError):
        input = ("Test", 1, 1, "Goblin", None, "Complete", 1, 1, None)
        DBCodexData.createFromTuple(input)

def test_DBCodexData_exportJSON(mock_DBCodexData: DBCodexData) -> None:
    expected = '{"ID":2,"Type":"Monster","Tier":1,"Name":"Bandit","Event":null,"Status":"Complete","Manifested":1,"Kills":5,"Filepath":"bandit.png"}'
    actual = mock_DBCodexData.exportJSON()
    assert actual == expected