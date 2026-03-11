import pytest

from classes.DBEquipmentCollection import DBEquipmentCollection

@pytest.fixture
def mock_Collection() -> DBEquipmentCollection:
    return DBEquipmentCollection(504, 198, "Ornate", False)

def test_DBEquipmentCollection_init(mock_Collection: DBEquipmentCollection) -> None:
    assert mock_Collection.ID == 504
    assert mock_Collection.QualityPercent == 198
    assert mock_Collection.QualityName == "Ornate"
    assert mock_Collection.IsPerfect == False

def test_DBEquipmentCollection_getAttributeType() -> None:
    assert DBEquipmentCollection.getAnnotation("ID") is int
    assert DBEquipmentCollection.getAnnotation("QualityPercent") is int
    assert DBEquipmentCollection.getAnnotation("QualityName") is str
    assert DBEquipmentCollection.getAnnotation("IsPerfect") is bool

def test_DBEquipmentCollection_createFromTuple() -> None:
    input = (30, 113, "Superior", False)
    actual = DBEquipmentCollection.createFromTuple(input)
    assert type(actual) is DBEquipmentCollection
    assert actual.ID == 30
    assert actual.QualityPercent == 113
    assert actual.QualityName == "Superior"
    assert actual.IsPerfect == False

def test_DBEquipmentCollection_createFromTuple_BadLength() -> None:
    with pytest.raises(ValueError):
        input = (20, 100)
        DBEquipmentCollection.createFromTuple(input)

def test_DBEquipmentCollection_createFromTuple_BadType() -> None:
    with pytest.raises(ValueError):
        input = ("Incorrect", 100, "Standard", False)
        DBEquipmentCollection.createFromTuple(input)

def test_DBEquipmentCollection_exportJSON(mock_Collection: DBEquipmentCollection) -> None:
    expected = '{"ID":504,"QualityPercent":198,"QualityName":"Ornate","IsPerfect":False}'
    actual = mock_Collection.exportJSON()
    assert actual == expected