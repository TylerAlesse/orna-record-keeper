import pytest

from classes.DBItemData import DBItemData

@pytest.fixture
def mock_DBItemData() -> DBItemData:
    return DBItemData(
        81, "Antidote", 1, "Other", "Common",
        False, False, False, 12.5, 0,
        "/img/useables/antidote.png", "", False, False
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

def test_DBItemData_exportJSON(mock_DBItemData: DBItemData) -> None:
    expected = '{"ID":81,"Name":"Antidote","Tier":1,"Type":"Other","Rarity":"Common",'\
                '"IsEvent":False,"IsRaidDrop":False,"IsBossScaling":False,'\
                '"BSP":12.5,"PSC":0,"Filepath":"/img/useables/antidote.png","Base64":"","Ignored":False,"Removed":False}'
    
    actual = mock_DBItemData.exportJSON()
    assert actual == expected