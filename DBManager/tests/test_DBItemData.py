import pytest

from types import UnionType
from classes.DBItemData import DBItemData

@pytest.fixture
def mock_DBItemData() -> DBItemData:
    return DBItemData(
        81, "Antidote", 1, "Other", "Common",
        False, False, False, 12.5, 0,
        "/img/useables/antidote.png", "", False, False, None
    )

def test_DBItemData_init(mock_DBItemData: DBItemData) -> None:
    assert mock_DBItemData.ID == 81
    assert mock_DBItemData.Name == "Antidote"
    assert mock_DBItemData.Tier == 1
    assert mock_DBItemData.Type == "Other"
    assert mock_DBItemData.Rarity == "Common"
    assert mock_DBItemData.IsEvent == False
    assert mock_DBItemData.IsRaidDrop == False
    assert mock_DBItemData.IsBossScaling == False
    assert mock_DBItemData.BSP == 12.5
    assert mock_DBItemData.PSC == 0
    assert mock_DBItemData.Filepath == "/img/useables/antidote.png"
    assert mock_DBItemData.Base64 == ""
    assert mock_DBItemData.Ignored == False
    assert mock_DBItemData.Removed == False
    assert mock_DBItemData.Deleted == None
    assert mock_DBItemData.TableName == "ItemData"

def test_DBItemData_createFromTuple() -> None:
    input = (
        24, "Great Orcish Axe", 5, "Weapon", "Superior",
        False, True, True, 540.0, 2,
        "/img/weapons/great_orcish_axe.png", "NotRealData", False, True, None
    )
    actual = DBItemData.createFromTuple(input)
    assert type(actual) is DBItemData
    assert actual.ID == 24
    assert actual.Name == "Great Orcish Axe"
    assert actual.Tier == 5
    assert actual.Type == "Weapon"
    assert actual.Rarity == "Superior"
    assert actual.IsEvent == False
    assert actual.IsRaidDrop == True
    assert actual.IsBossScaling == True
    assert actual.BSP == 540.0
    assert actual.PSC == 2
    assert actual.Filepath == "/img/weapons/great_orcish_axe.png"
    assert actual.Base64 == "NotRealData"
    assert actual.Ignored == False
    assert actual.Removed == True
    assert actual.Deleted == None

def test_DBItemData_createFromTuple_BadLength() -> None:
    with pytest.raises(ValueError):
        input = (80, "Fake Item Name", 6, "Consumable")
        DBItemData.createFromTuple(input)

def test_DBItemData_createFromTuple_BadType() -> None:
    with pytest.raises(TypeError):
        input = (
            "77", "Great Orcish Axe", 5, "Weapon", "Superior",
            False, True, True, 540.0, 2,
            "/img/weapons/great_orcish_axe.png", "==NotRealData", False, True, None
        )
        DBItemData.createFromTuple(input)

def test_DBItemData_exportJSON(mock_DBItemData: DBItemData) -> None:
    expected = '{"ID":81,"Name":"Antidote","Tier":1,"Type":"Other","Rarity":"Common",'\
                '"IsEvent":False,"IsRaidDrop":False,"IsBossScaling":False,'\
                '"BSP":12.5,"PSC":0,"Filepath":"/img/useables/antidote.png","Base64":"","Ignored":False,"Removed":False}'
    
    actual = mock_DBItemData.exportJSON()
    assert actual == expected