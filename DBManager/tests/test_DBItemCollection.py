import pytest

from classes.DBItemCollection import DBItemCollection

@pytest.fixture
def mock_DBItemCollection() -> DBItemCollection:
    return DBItemCollection(10, 100)

def test_DBItemCollection_init(mock_DBItemCollection: DBItemCollection) -> None:
    assert mock_DBItemCollection.ID == 10
    assert mock_DBItemCollection.Quantity == 100

def test_DBItemCollection_exportJSON(mock_DBItemCollection: DBItemCollection) -> None:
    expected = '{"ID":10,"Quantity":100}'
    actual = mock_DBItemCollection.exportJSON()
    assert actual == expected