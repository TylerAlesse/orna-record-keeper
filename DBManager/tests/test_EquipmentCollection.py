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

def test_DBEquipmentCollection_exportJSON(mock_Collection: DBEquipmentCollection) -> None:
    expected = '{ID:504,QualityPercent:198,QualityName:"Ornate",IsPerfect:False}'
    actual = mock_Collection.exportJSON()
    assert actual == expected