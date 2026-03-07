import pytest
from types import UnionType

from classes.DBCodexData import DBCodexData

@pytest.fixture
def mock_DBCodexData() -> DBCodexData:
    return DBCodexData(2, "Monster", 1, "Bandit", None, "Complete", 1, 5, "bandit.png")

def test_DBCodexData_init(mock_DBCodexData: DBCodexData) -> None:
    assert mock_DBCodexData.ID == 2
    assert mock_DBCodexData.type == "Monster"
    assert mock_DBCodexData.tier == 1
    assert mock_DBCodexData.name == "Bandit"
    assert mock_DBCodexData.event == None
    assert mock_DBCodexData.status == "Complete"
    assert mock_DBCodexData.manifested == 1
    assert mock_DBCodexData.kills == 5
    assert mock_DBCodexData.filepath == "bandit.png"

def test_DBCodexData_getAttributeType(mock_DBCodexData: DBCodexData) -> None:
    assert mock_DBCodexData.getAttributeType("ID") is int
    assert mock_DBCodexData.getAttributeType("type") is str
    assert mock_DBCodexData.getAttributeType("tier") is int
    assert mock_DBCodexData.getAttributeType("name") is str
    assert type(mock_DBCodexData.getAttributeType("event")) is UnionType
    assert mock_DBCodexData.getAttributeType("status") is str
    assert mock_DBCodexData.getAttributeType("manifested") is int
    assert mock_DBCodexData.getAttributeType("kills") is int
    assert type(mock_DBCodexData.getAttributeType("filepath")) is UnionType

def test_DBCodexData_createFromTuple() -> None:
    input = (55, "Boss", 2, "Arachne", "Spider's Nest", "Missing", 0, 10, "spider.png")
    actual = DBCodexData.createFromTuple(input)
    assert type(actual) is DBCodexData
    assert actual.ID == 55
    assert actual.type == "Boss"
    assert actual.tier == 2
    assert actual.name == "Arachne"
    assert actual.event == "Spider's Nest"
    assert actual.status == "Missing"
    assert actual.manifested == 0
    assert actual.kills == 10
    assert actual.filepath == "spider.png"

def test_DBCodexData_createFromTuple_BadLength() -> None:
    with pytest.raises(ValueError):
        queryResult = (33, "Fails")
        DBCodexData.createFromTuple(queryResult)

def test_DBCodexData_createFromTuple_BadType() -> None:
    with pytest.raises(ValueError):
        queryResult = ("Test", 1, 1, "Goblin", None, "Complete", 1, 1, None)
        DBCodexData.createFromTuple(queryResult)

def test_DBCodexData_exportJSON(mock_DBCodexData: DBCodexData) -> None:
    expected = '{"ID":2,"Type":"Monster","Tier":1,"Name":"Bandit","Event":null,"Status":"Complete","Manifested":1,"Kills":5,"Filepath":"bandit.png"}'
    actual = mock_DBCodexData.exportJSON()
    assert actual == expected