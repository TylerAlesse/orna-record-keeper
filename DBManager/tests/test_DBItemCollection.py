import pytest

from classes.DBItemCollection import DBItemCollection

@pytest.fixture
def mock_DBItemCollection() -> DBItemCollection:
    return DBItemCollection(10, 100)

def test_DBItemCollection_init(mock_DBItemCollection: DBItemCollection) -> None:
    assert mock_DBItemCollection.ID == 10
    assert mock_DBItemCollection.Quantity == 100
    assert mock_DBItemCollection.TableName == "ItemCollection"

def test_DBItemCollection_createFromTuple() -> None:
    input = (74, 4327)
    actual = DBItemCollection.createFromTuple(input)
    assert type(actual) is DBItemCollection
    assert actual.ID == 74
    assert actual.Quantity == 4327

def test_DBItemCollection_createFromTuple_BadLength() -> None:
    with pytest.raises(ValueError):
        input = (80, 100, 12)
        DBItemCollection.createFromTuple(input)

def test_DBItemCollection_createFromTuple_BadType() -> None:
    with pytest.raises(TypeError):
        input = (56, "22")
        DBItemCollection.createFromTuple(input)

def test_DBItemCollection_exportJSON(mock_DBItemCollection: DBItemCollection) -> None:
    expected = '{"ID":10,"Quantity":100}'
    actual = mock_DBItemCollection.exportJSON()
    assert actual == expected