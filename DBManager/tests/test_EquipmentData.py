import pytest
from classes.EquipmentData import EquipmentData

from classes.DBItemData import DBItemData
from classes.DBEquipmentCollection import DBEquipmentCollection

@pytest.fixture
def mock_EquipmentData() -> EquipmentData:
    return EquipmentData(504, "Bandit's Axe", 1, "Weapons", "Common",
                         198, "Ornate", False, False, False, "/img/weapons/battle_axe.png")

def test_EquipmentData_init(mock_EquipmentData: EquipmentData) -> None:
    assert mock_EquipmentData.ID == 504
    assert mock_EquipmentData.Name == "Bandit's Axe"
    assert mock_EquipmentData.Tier == 1
    assert mock_EquipmentData.Type == "Weapons"
    assert mock_EquipmentData.Rarity == "Common"
    assert mock_EquipmentData.QualityPercent == 198
    assert mock_EquipmentData.QualityName == "Ornate"
    assert mock_EquipmentData.IsPerfect == False
    assert mock_EquipmentData.IsEvent == False
    assert mock_EquipmentData.IsRaidDrop == False
    assert mock_EquipmentData.Filepath == "/img/weapons/battle_axe.png"

def test_EquipmentData_createFromClasses() -> None:
    itemData = DBItemData(683, "Carl's Dagger", 1, "Weapons", "Common",
                    False, False, False, 150.0, 1,
                    "/img/weapons/dagger.png", "", False, False, None)
    equipCollection = DBEquipmentCollection(683, 198, "Ornate", False)
    actual = EquipmentData.createFromClasses(itemData, equipCollection)
    
    assert actual.ID == 683
    assert actual.Name == "Carl's Dagger"
    assert actual.Tier == 1
    assert actual.Type == "Weapons"
    assert actual.Rarity == "Common"
    assert actual.QualityPercent == 198
    assert actual.QualityName == "Ornate"
    assert actual.IsPerfect == False
    assert actual.IsEvent == False
    assert actual.IsRaidDrop == False
    assert actual.Filepath == "/img/weapons/dagger.png"

def test_EquipmentData_createFromTuple() -> None:
    input = (683, "Carl's Dagger", 1, "Weapons", "Common",
            198, "Ornate", False, False, False, "/img/weapons/dagger.png")
    actual = EquipmentData.createFromTuple(input)
    assert actual.ID == 683
    assert actual.Name == "Carl's Dagger"
    assert actual.Tier == 1
    assert actual.Type == "Weapons"
    assert actual.Rarity == "Common"
    assert actual.QualityPercent == 198
    assert actual.QualityName == "Ornate"
    assert actual.IsPerfect == False
    assert actual.IsEvent == False
    assert actual.IsRaidDrop == False
    assert actual.Filepath == "/img/weapons/dagger.png"

def test_EquipmentData_createFromTuple_BadType() -> None:
    with pytest.raises(TypeError):
        input = ("Fails", "Carl's Dagger", 1, "Weapons", "Common",
                198, "Ornate", False, False, False, "/img/weapons/dagger.png")
        EquipmentData.createFromTuple(input)

def test_EquipmentData_exportJSON(mock_EquipmentData) -> None:
    expected = '{"ID":504,"Name":"Bandit\'s Axe","Tier":1,"Type":"Weapons","Rarity":"Common",'\
                '"QualityPercent":198,"QualityName":"Ornate","IsPerfect":False,'\
                '"IsEvent":False,"IsRaidDrop":False,"Filepath":"/img/weapons/battle_axe.png"}'

    actual = mock_EquipmentData.exportJSON()
    assert actual == expected