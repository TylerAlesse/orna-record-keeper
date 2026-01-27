import pytest
from classes.EquipmentData import EquipmentData

from classes.DBItemData import DBItemData
from classes.DBEquipmentCollection import DBEquipmentCollection

@pytest.fixture
def mock_EquipmentData() -> EquipmentData:
    return EquipmentData(504, "Bandit's Axe", 1, "Weapons", "Common",
                         198, "Ornate", False, False, False, "/img/weapons/battle_axe.png")

@pytest.fixture
def mock_CFC() -> EquipmentData:
    item = DBItemData(683, "Carl's Dagger", 1, "Weapons", "Common",
                    False, False, False, 150.0, 1,
                    "/img/weapons/dagger.png", "", False, False)
    equip = DBEquipmentCollection(683, 198, "Ornate", False)
    return EquipmentData.createFromClasses(item, equip)

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

def test_EquipmentData_createFromClasses(mock_CFC: EquipmentData) -> None:
    assert mock_CFC.ID == 683
    assert mock_CFC.Name == "Carl's Dagger"
    assert mock_CFC.Tier == 1
    assert mock_CFC.Type == "Weapons"
    assert mock_CFC.Rarity == "Common"
    assert mock_CFC.QualityPercent == 198
    assert mock_CFC.QualityName == "Ornate"
    assert mock_CFC.IsPerfect == False
    assert mock_CFC.IsEvent == False
    assert mock_CFC.IsRaidDrop == False
    assert mock_CFC.Filepath == "/img/weapons/dagger.png"

def test_EquipmentData_exportJSON(mock_EquipmentData) -> None:
    expected = '{ID:504,Name:"Bandit\'s Axe",Tier:1,Type:"Weapons",Rarity:"Common",'\
                'QualityPercent:198,QualityName:"Ornate",IsPerfect:False,'\
                'IsEvent:False,IsRaidDrop:False,Filepath:"/img/weapons/battle_axe.png"}'

    actual = mock_EquipmentData.exportJSON()
    assert actual == expected