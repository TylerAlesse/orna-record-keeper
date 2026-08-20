import pytest
from app import create_app
from classes.DBItemData import DBItemData
import os

#**                  **#
#*      Fixtures      *#
#**                  **#

# Sets current working directory to test file location
@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname)

@pytest.fixture
def app():
    test_config = {
        'TESTING': True,
        'DATABASE_URI': 'data/app_test.db',
        'DATABASE_AUTOCOMMIT': True
    }

    app = create_app(test_config)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

#! Don't have a way to test requestArgumentInputChecker()
#! with the current implementation.
#? Consider changing it such that it can?

# def test_app_requestArgumentInputChecker_valid(client) -> None:
#     pytest.skip()

# def test_app_requestArgumentInputChecker_invalid_requiredAndNotGiven(client) -> None:
#     pytest.skip()

# def test_app_requestArgumentInputChecker_invalid_cannotCast(client) -> None:
#     pytest.skip()

def test_app_response_NotFound(client) -> None:
    getResponse = client.get(path="/api/does_not_exist", query_string={})
    assert getResponse.status_code == 404

#**                  **#
#*     Codex Data     *#
#**                  **#

# Get Codex Data

def test_app_getCodexData(client) -> None:
    response = client.get(path="/api/codexData")
    assert response.status_code == 200
    assert len(response.json) > 0

def test_app_getCodexData_GivenID(client) -> None:
    requestData = {"ID": 1}
    getResponse = client.get(path="/api/codexData", query_string=requestData)
    getExpected = {
        "ID": 1,
        "Type": "Monster",
        "Tier": 1,
        "Name": "Bandit",
        "Event": None,
        "Status": "Complete",
        "Manifested": 1,
        "Kills": 5,
        "Filepath": "/img/monsters/bandit.png",
    }

    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == getExpected

def test_app_getCodexData_IDNotFound(client) -> None:
    requestData = {"ID": 9999}
    getResponse = client.get(path="/api/codexData", query_string=requestData)
    getExpected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Primary Key: ID"
    }
    
    assert getResponse.status_code == 404
    assert getResponse.json == getExpected

def test_app_getCodexData_BadID(client) -> None:
    requestData = {"ID": "Fails"}
    getResponse = client.get(path="/api/codexData", query_string=requestData)
    getExpected = {
        "error": "Bad request",
        "reason": "Argument 'ID' was of incorrect type. Expected: Number"
    }
    
    assert getResponse.status_code == 400
    assert getResponse.json == getExpected

# Update Codex Data

def test_app_updateCodexData(client) -> None:
    requestData = {
        "ID": 2,
        "Type": "Boss",
        "Tier": 4,
        "Name": "Spooky Ghost",
        "Event": "The Hallowed",
        "Status": "Seen",
        "Manifested": 0,
        "Kills": 2,
        "Filepath": "/img/bosses/ghost.png"
    }
    putResponse = client.put(path="/api/codexData", query_string=requestData)
    assert putResponse.status_code == 200

    #^ Confirm PUT updated correctly
    getResponse = client.get(path="/api/codexData", query_string={"ID": 2})
    getExpected = {
        "ID": 2,
        "Type": "Boss",
        "Tier": 4,
        "Name": "Spooky Ghost",
        "Event": "The Hallowed",
        "Status": "Seen",
        "Manifested": 0,
        "Kills": 2,
        "Filepath": "/img/bosses/ghost.png",
    }

    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == getExpected

def test_app_updateCodexData_NotEnoughAttributes(client) -> None:
    requestData = {"ID": 4}
    putResponse = client.put(path="/api/codexData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "No values to be updated were provided",
        "arguments": [ #! Would need to be updated as the DB is updated
            {"Name": "Type", "Type": "Text"},
            {"Name": "Tier", "Type": "Number"},
            {"Name": "Name", "Type": "Text"},
            {"Name": "Event", "Type": "Text"},
            {"Name": "Status", "Type": "Text"},
            {"Name": "Manifested", "Type": "Number"},
            {"Name": "Kills", "Type": "Number"},
            {"Name": "Filepath", "Type": "Text"},
        ]
    }
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateCodexData_NoIDProvided(client) -> None:
    requestData = {"Name": "Goblin"}
    putResponse = client.put(path="/api/codexData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'ID' was not given."
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateCodexData_IDNotFound(client) -> None:
    requestData = {"ID": 9999, "Name": "Goblin Warrior"}
    putResponse = client.put(path="/api/codexData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Primary Key: ID"
    }
    
    assert putResponse.status_code == 404
    assert putResponse.json == putExpected

    #^ Confirm PUT failed to update the non-existent entry
    getResponse = client.get(path="/api/codexData", query_string=requestData)
    getExpected = {
            "error": "Bad request",
            "reason": "Could not find entry with given Primary Key: ID"
        }

    assert getResponse.status_code == 404
    assert getResponse.json == getExpected

def test_app_updateCodexData_BadID(client) -> None:
    requestData = {"ID": "Fails", "Name": "Goblin Mage"}
    putResponse = client.put(path="/api/codexData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Argument 'ID' was of incorrect type. Expected: Number"
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateCodexData_BadArguments(client) -> None:
    requestData = {"ID": 4, "Name": 12}
    putResponse = client.put(path="/api/codexData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Argument 'Name' was of incorrect type. Expected: Text"
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

    #^ Confirm PUT failed to update
    getResponse = client.get(path="/api/codexData", query_string=requestData)
    getExpected = {
        "ID": 4,
        "Type": "Boss",
        "Tier": 8,
        "Name": "Fafnir",
        "Event": None,
        "Status": "Seen",
        "Manifested": -1,
        "Kills": 0,
        "Filepath": "/img/bosses/fafnir.png",
    }

    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == getExpected

# Insert Codex Data

def test_app_insertCodexData_WithoutID(client) -> None:
    requestData = {
        "Type": "Monster",
        "Tier": 3,
        "Name": "Great Mimic",
        "Event": None,
        "Status": "Completed",
        "Manifested": 0,
        "Kills": 2,
        "Filepath": "/img/monsters/great_mimic.png",
    }

    postResponse = client.post(path="/api/codexData", query_string=requestData)

    assert postResponse.status_code == 201

    #^ Confirm POST worked correctly
    getResponse = client.get(path="/api/codexData", query_string={"ID": 5})
    getExpected = {
        "ID": 5,
        "Type": "Monster",
        "Tier": 3,
        "Name": "Great Mimic",
        "Event": None,
        "Status": "Completed",
        "Manifested": 0,
        "Kills": 2,
        "Filepath": "/img/monsters/great_mimic.png",
    }

    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == getExpected

def test_app_insertCodexData_GivenID(client) -> None:
    requestData = {
        "ID": 10,
        "Type": "Boss",
        "Tier": 4,
        "Name": "Undead Golem",
        "Event": None,
        "Status": "Seen",
        "Manifested": 1,
        "Kills": 12,
        "Filepath": "/img/bosses/undead_golem.png",
    }

    postResponse = client.post(path="/api/codexData", query_string=requestData)
    assert postResponse.status_code == 201

    #^ Confirm POST worked correctly
    getResponse = client.get(path="/api/codexData", query_string={"ID": 10})

    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == requestData

def test_app_insertCodexData_IDConflict(client) -> None:
    requestData = {
        "ID": 1,
        "Type": "Monster",
        "Tier": 8,
        "Name": "Kobold",
        "Event": None,
        "Status": "Missing",
        "Manifested": -1,
        "Kills": 0,
        "Filepath": "/img/monsters/kobold.png",
    }

    postResponse = client.post(path="/api/codexData", query_string=requestData)
    postExpected = {
        "error": "Conflict",
        "reason": "ID already in use."
    }
    assert postResponse.status_code == 409
    assert postResponse.json == postExpected

def test_app_insertCodexData_RequiredAttributeNotGiven(client) -> None:
    # Getting the count of entries prior to a failed insert
    getResponse = client.get(path="/api/codexData")
    assert getResponse.status_code == 200
    prevEntryCount = len(getResponse.json)

    # POST Request
    requestData = {
        # "Type": "Boss", #! Intended Missing
        "Tier": 10,
        "Name": "Test",
        "Event": None,
        "Status": "Completed",
        "Manifested": -1,
        "Kills": 0,
        "Filepath": "",
    }
    
    postResponse = client.post(path="/api/codexData", query_string=requestData)
    postExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'Type' was not given."
    }
    
    assert postResponse.status_code == 400
    assert postResponse.json == postExpected

    #^ Confirm POST failed
    checkResponse = client.get(path="/api/codexData")
    assert checkResponse.status_code == 200
    assert len(checkResponse.json) == prevEntryCount

def test_app_insertCodexData_BadArguments(client) -> None:
    # Getting the count of entries prior to a failed insert
    getResponse = client.get(path="/api/codexData")
    assert getResponse.status_code == 200
    prevEntryCount = len(getResponse.json)

    # POST Request
    requestData = {
        "Type": "Boss",
        "Tier": "Fails", # Supposed to be Integer
        "Name": "Test",
        "Event": None,
        "Status": "Completed",
        "Manifested": -1,
        "Kills": 0,
        "Filepath": "",
    }

    postResponse = client.post(path="/api/codexData", query_string=requestData)
    postExpected = {
        "error": "Bad request",
        "reason": "Argument 'Tier' was of incorrect type. Expected: Number"
    }
    
    assert postResponse.status_code == 400
    assert postResponse.json == postExpected

    #^ Confirm POST failed
    checkResponse = client.get(path="/api/codexData")
    assert checkResponse.status_code == 200
    assert len(checkResponse.json) == prevEntryCount

# Delete Codex Data

def test_app_deleteCodexData(client) -> None:
    requestData = {"ID": 3}
    deleteResponse = client.delete(path="/api/codexData", query_string=requestData)
    assert deleteResponse.status_code == 200

    #^ Confirm DELETE via GET
    getResponse = client.get(path="/api/codexData", query_string=requestData)
    getExpected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Primary Key: ID"
    }
    
    assert getResponse.status_code == 404
    assert getResponse.json == getExpected

def test_app_deleteCodexData_NonexistentID(client) -> None:
    requestData = {"ID": 9999}
    deleteResponse = client.delete(path="/api/codexData", query_string=requestData)
    
    assert deleteResponse.status_code == 200

def test_app_deleteCodexData_NoIDGiven(client) -> None:
    requestData = {}
    deleteResponse = client.delete(path="/api/codexData", query_string=requestData)
    deleteExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'ID' was not given."
    }
    
    assert deleteResponse.status_code == 400
    assert deleteResponse.json == deleteExpected

def test_app_deleteCodexData_BadID(client) -> None:
    requestData = {"ID": "Fails"}
    deleteResponse = client.delete(path="/api/codexData", query_string=requestData)
    deleteExpected = {
        "error": "Bad request",
        "reason": "Argument 'ID' was of incorrect type. Expected: Number"
    }
    
    assert deleteResponse.status_code == 400
    assert deleteResponse.json == deleteExpected

#**                    **#
#* Equipment Collection *#
#**                    **#

# Get Equipment Collection

def test_app_getEquipmentCollection(client) -> None:
    getResponse = client.get(path="/api/equipmentCollection")
    assert getResponse.status_code == 200
    assert len(getResponse.json) > 0

def test_app_getEquipmentCollection_GivenID(client) -> None:
    requestData = {"ID": 1}
    getResponse = client.get(path="/api/equipmentCollection", query_string=requestData)
    getExpected = {
        "ID": 1,
        "QualityPercent": 180,
        "QualityName": "Ornate",
        "IsPerfect": None
    }
    
    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == getExpected

def test_app_getEquipmentCollection_BadID(client) -> None:
    requestData = {"ID": "Fails"}
    getResponse = client.get(path="/api/equipmentCollection", query_string=requestData)
    getExpected = {
        "error": "Bad request",
        "reason": "Argument 'ID' was of incorrect type. Expected: Number"
    }
    
    assert getResponse.status_code == 400
    assert getResponse.json == getExpected

def test_app_getEquipmentCollection_IDNotFound(client) -> None:
    requestData = {"ID": 9999}
    getResponse = client.get(path="/api/equipmentCollection", query_string=requestData)
    getExpected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Primary Key: ID"
    }
    
    assert getResponse.status_code == 404
    assert getResponse.json == getExpected

# Update Equipment Collection

def test_app_updateEquipmentCollection(client) -> None:
    requestData = {
        "ID": "2",
        "QualityPercent": 160,
        "QualityName": "Legendary",
        "IsPerfect": None
    }
    
    putResponse = client.put(path="/api/equipmentCollection", query_string=requestData)
    assert putResponse.status_code == 200

    #^ Confirm PUT via GET
    getResponse = client.get(path="/api/equipmentCollection", query_string={"ID": 2})
    expected = {
        "ID": 2,
        "Type": "Boss",
        "Tier": 4,
        "Name": "Spooky Ghost",
        "Event": "The Hallowed",
        "Status": "Missing",
        "Manifested": -1,
        "Kills": 0,
        "Filepath": "/img/bosses/spectre.png",
    }

    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == expected

def test_app_updateEquipmentCollection_NotEnoughAttributes(client) -> None:
    requestData = {"ID": 3}
    putResponse = client.put(path="/api/equipmentCollection", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "No values to be updated were provided",
        "arguments": [ #! Would need to be updated as the DB is updated
            {"Name": "QualityPercent", "Type": "Number"},
            {"Name": "QualityName", "Type": "Text"},
            {"Name": "IsPerfect", "Type": "Boolean"},
        ]
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

    #^ Confirmation PUT failed correctly
    getResponse = client.get(path="/api/equipmentCollection", query_string=requestData)
    getExpected = {
        "ID": 3,
        "QualityPercent": 99,
        "QualityName": "Poor",
        "IsPerfect": None
    }
    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == getExpected

def test_app_updateEquipmentCollection_NoIDProvided(client) -> None:
    # Getting the count of entries prior to a failed insert
    firstResponse = client.get(path="/api/equipmentCollection")
    assert firstResponse.status_code == 200
    prevEntryCount = len(firstResponse.json)

    # Failing PUT request
    putRequestData = {"QualityPercent": 115, "QualityName": "Superior"}
    putResponse = client.put(path="/api/equipmentCollection", query_string=putRequestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'ID' was not given."
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

    #^ Confirmation PUT failed correctly
    checkResponse = client.get(path="/api/equipmentCollection")
    assert checkResponse.status_code == 200
    assert len(checkResponse) == prevEntryCount

def test_app_updateEquipmentCollection_IDNotFound(client) -> None:
    requestData = {
        "ID": 9999,
        "QualityPercent": 200,
        "QualityName": "Ornate",
        "IsPerfect": 1
    }
    putResponse = client.put(path="/api/equipmentCollection", query_string=requestData)
    expected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Primary Key: ID"
    }
    
    assert putResponse.status_code == 404
    assert putResponse.json == expected

    #^ Confirm PUT failed to update the non-existent entry
    getResponse = client.get(path="/api/equipmentCollection", query_string={"ID": 9999})

    assert getResponse.status_code == 404
    assert getResponse.json == expected

def test_app_updateEquipmentCollection_BadID(client) -> None:
    requestData = {"ID": "Fails"}
    putResponse = client.put(path="/api/equipmentCollection", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Argument 'ID' was of incorrect type. Expected: Number"
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateEquipmentCollection_BadArguments(client) -> None:
    requestData = {"ID": 6, "QualityPercent": "Fails", "QualityName": "Famed"}
    putResponse = client.put(path="/api/equipmentCollection", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Argument 'QualityPercent' was of incorrect type. Expected: Number"
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

    #^ Confirm PUT failed to update
    getResponse = client.get(path="/api/equipmentCollection", query_string=requestData)
    getExpected = {
        "ID": 6,
        "QualityPercent": 112,
        "QualityName": "Superior",
        "IsPerfect": None
    }

    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == getExpected

# Insert Equipment Collection

def test_app_insertEquipmentCollection(client) -> None:
    requestData = {"ID": 5, "QualityPercent": 100, "QualityName": "Standard"}
    postResponse = client.post(path="/api/equipmentCollection", query_string=requestData)
    
    assert postResponse.status_code == 201
    assert postResponse.json == None

    #^ Confirm POST worked correctly
    getResponse = client.get(path="/api/equipmentCollection", query_string={"ID": 5})
    expected = {
        "ID": 5,
        "QualityPercent": 100,
        "QualityName": "Standard",
        "IsPerfect": None
    }

    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == expected

def test_app_insertEquipmentCollection_IDConflict(client) -> None:
    requestData = {"ID": 1, "QualityPercent": 100, "QualityName": "Standard"}
    postResponse = client.post(path="/api/equipmentCollection", query_string=requestData)
    postExpected = {
        "error": "Conflict",
        "reason": "ID already in use."
    }

    assert postResponse.status_code == 409
    assert postResponse.json == postExpected

def test_app_insertEquipmentCollection_RequiredAttributeNotGiven(client) -> None:
    requestData = {
        # Missing Item ID
        "QualityPercent": 100,
        "QualityName": "Standard",
        "IsPerfect": None
    }
    
    postResponse = client.post(path="/api/equipmentCollection", query_string=requestData)
    postExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'ID' was not given."
    }
    
    assert postResponse.status_code == 400
    assert postResponse.json == postExpected

def test_app_insertEquipmentCollection_BadArguments(client) -> None:
    requestData = {
        "ID": 6,
        "QualityPercent": "Fails"
    }
    
    postResponse = client.post(path="/api/equipmentCollection", query_string=requestData)
    postExpected = {
        "error": "Bad request",
        "reason": "Argument 'QualityPercent' was of incorrect type. Expected: Number"
    }
    
    assert postResponse.status_code == 400
    assert postResponse.json == postExpected

# Delete Equipment Collection

def test_app_deleteEquipmentCollection(client) -> None:
    requestData = {"ID": 4}
    deleteResponse = client.delete(path="/api/equipmentCollection", query_string=requestData)
    
    assert deleteResponse.status_code == 200

    #^ Confirm DELETE removed the ID
    getResponse = client.get(path="/api/equipmentCollection", query_string=requestData)
    getExpected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Primary Key: ID"
    }
    
    assert getResponse.status_code == 404
    assert getResponse.json == getExpected

def test_app_deleteEquipmentCollection_NonexistentID(client) -> None:
    requestData = {"ID": 9999}
    deleteResponse = client.delete(path="/api/equipmentCollection", query_string=requestData)
    
    assert deleteResponse.status_code == 200

def test_app_deleteEquipmentCollection_NoIDGiven(client) -> None:
    requestData = {}
    deleteResponse = client.delete(path="/api/equipmentCollection", query_string=requestData)
    deleteExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'ID' was not given."
    }
    
    assert deleteResponse.status_code == 400
    assert deleteResponse.json == deleteExpected

def test_app_deleteEquipmentCollection_BadID(client) -> None:
    requestData = {"ID": "Fails"}
    deleteResponse = client.delete(path="/api/equipmentCollection", query_string=requestData)
    deleteExpected = {
        "error": "Bad request",
        "reason": "Argument 'ID' was of incorrect type. Expected: Number"
    }
    
    assert deleteResponse.status_code == 400
    assert deleteResponse.json == deleteExpected

#**                  **#
#*     Guild Data     *#
#**                  **#

# Get Guild Data

def test_app_getGuildData(client) -> None:
    getResponse = client.get(path="/api/guildData")
    assert getResponse.status_code == 200
    assert len(getResponse.json) > 0

def test_app_getGuildData_GivenKey(client) -> None:
    requestData = {"PlayerLevel": 83, "Name": "Traveler's Guild"}
    getResponse = client.get(path="/api/guildData", query_string=requestData)
    getExpected = {
        "PlayerLevel": 83,
        "Name": "Traveler's Guild",
        "Level": 32,
        "EXP": 10526
    }
    
    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == getExpected

def test_app_getGuildData_KeyNotFound(client) -> None:
    requestData = {"PlayerLevel": 80, "Name": "Not A Guild"}
    response = client.get(path="/api/guildData", query_string=requestData)
    expected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Composite Key: Player Level, Name"
    }
    
    assert response.status_code == 404
    assert response.json == expected

def test_app_getGuildData_BadKey_PlayerLevel(client) -> None:
    requestData = {"PlayerLevel": "Fails", "Name": "Not A Guild"}
    getResponse = client.get(path="/api/guildData", query_string=requestData)
    getExpected = {
        "error": "Bad request",
        "reason": "Argument 'PlayerLevel' was of incorrect type. Expected: Number"
    }
    
    assert getResponse.status_code == 400
    assert getResponse.json == getExpected

def test_app_getGuildData_BadKey_Name(client) -> None:
    requestData = {"PlayerLevel": 55, "Name": 12}
    getResponse = client.get(path="/api/guildData", query_string=requestData)
    getExpected = {
        "error": "Bad request",
        "reason": "Argument 'Name' was of incorrect type. Expected: Text"
    }
    
    assert getResponse.status_code == 400
    assert getResponse.json == getExpected

# Update Guild Data

def test_app_updateGuildData(client) -> None:
    putRequestData = {
        "PlayerLevel": 83,
        "Name": "Conqueror's Guild",
        "EXP": 6064, # Originally: 6034
    }
    putResponse = client.put(path="/api/guildData", query_string=putRequestData)
    assert putResponse.status_code == 200
    
    getRequestData = {
        "PlayerLevel": 83,
        "Name": "Conqueror's Guild"
    }
    getResponse = client.get(path="/api/guildData", query_string=getRequestData)
    
    getExpected = {
        "PlayerLevel": 83,
        "Name": "Conqueror's Guild",
        "Level": 25,
        "EXP": 6064
    }
    
    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == getExpected

def test_app_updateGuildData_NotEnoughAttributes(client) -> None:
    requestData = {
        "PlayerLevel": 83,
        "Name": "Conqueror's Guild"
    }
    putResponse = client.put(path="/api/guildData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "No values to be updated were provided",
        "arguments": [ #! Would need to be updated as the DB is updated
            {"Name": "Level", "Type": "Number"},
            {"Name": "EXP", "Type": "Number"},
        ]
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateGuildData_KeyNotProvided_PlayerLevel(client) -> None:
    requestData = {
        # "PlayerLevel": 83,
        "Name": "Conqueror's Guild"
    }
    putResponse = client.put(path="/api/guildData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'PlayerLevel' was not given."
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateGuildData_KeyNotProvided_Name(client) -> None:
    requestData = {
        "PlayerLevel": 83,
        # "Name": "Conqueror's Guild"
    }
    putResponse = client.put(path="/api/guildData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'Name' was not given."
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateGuildData_CompositeKeyNotFound(client) -> None:
    requestData = {"PlayerLevel": 80, "Name": "Not A Guild"}
    putResponse = client.put(path="/api/guildData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Composite Key: Player Level, Name"
    }
    
    assert putResponse.status_code == 404
    assert putResponse.json == putExpected

def test_app_updateGuildData_BadID_PlayerLevel(client) -> None:
    requestData = {"PlayerLevel": "Fails", "Name": "Traveler's Guild"}
    putResponse = client.put(path="/api/guildData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Argument 'PlayerLevel' was of incorrect type. Expected: Number"
    }
    
    assert putResponse.status_code == 404
    assert putResponse.json == putExpected

def test_app_updateGuildData_BadID_Name(client) -> None:
    requestData = {"PlayerLevel": 80, "Name": 22}
    putResponse = client.put(path="/api/guildData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Argument 'Name' was of incorrect type. Expected: Text"
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateGuildData_BadArguments_Level(client) -> None:
    requestData = {
        "PlayerLevel": 83,
        "Name": "Traveler's Guild",
        "Level": "Fails",
        "EXP": 5555
    }
    putResponse = client.put(path="/api/guildData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Argument 'Level' was of incorrect type. Expected: Number"
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateGuildData_BadArguments_EXP(client) -> None:
    requestData = {
        "PlayerLevel": 83,
        "Name": "Traveler's Guild",
        "Level": 5,
        "EXP": "Fails"
    }
    putResponse = client.put(path="/api/guildData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Argument 'EXP' was of incorrect type. Expected: Number"
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

# Insert Guild Data

def test_app_insertGuildData(client) -> None:
    requestData = {
        "PlayerLevel": 84,
        "Name": "Monumental Guild",
        "Level": 90,
        "EXP": 80800
    }
    postResponse = client.post(path="/api/guildData", query_string=requestData)
    
    assert postResponse.status_code == 201

    #^ Confirm POST worked correctly
    compKey = {"PlayerLevel": 84, "Name": "Monumental Guild"}
    getResponse = client.get(path="/api/guildData", query_string=compKey)
    
    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == requestData

def test_app_insertGuildData_CompositeKeyConflict(client) -> None:
    requestData = {
        "PlayerLevel": 84,
        "Name": "Monumental Guild",
        "Level": 90,
        "EXP": 80800
    }
    postResponse = client.post(path="/api/guildData", query_string=requestData)
    postExpected = {
        "error": "Conflict",
        "reason": "Composite Key already in use."
    }
    assert postResponse.status_code == 409
    assert postResponse.json == postExpected

def test_app_insertGuildData_BadArguments_Level(client) -> None:
    requestData = {
        "PlayerLevel": 90,
        "Name": "Traveler's Guild",
        "Level": "Fails",
        "EXP": 7777
    }
    postResponse = client.post(path="/api/guildData", query_string=requestData)
    postExpected = {
        "error": "Bad request",
        "reason": "Argument 'Level' was of incorrect type. Expected: Number"
    }
    
    assert postResponse.status_code == 400
    assert postResponse.json == postExpected

def test_app_insertGuildData_BadArguments_EXP(client) -> None:
    requestData = {
        "PlayerLevel": 90,
        "Name": "Traveler's Guild",
        "Level": 5,
        "EXP": "Fails"
    }
    postResponse = client.post(path="/api/guildData", query_string=requestData)
    postExpected = {
        "error": "Bad request",
        "reason": "Argument 'EXP' was of incorrect type. Expected: Number"
    }
    
    assert postResponse.status_code == 400
    assert postResponse.json == postExpected

# Delete Guild Data

def test_app_deleteGuildData(client) -> None:
    requestData = {"PlayerLevel": 99, "Name": "Seer's Guild"}
    deleteResponse = client.delete(path="/api/guildData", query_string=requestData)
    assert deleteResponse.status_code == 200

    #^ Confirm DELETE worked
    getResponse = client.get(path="/api/guildData", query_string=requestData)
    expected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Primary Key: ID"
    }
    
    assert getResponse.status_code == 404
    assert getResponse.json == expected

def test_app_deleteGuildData_NonexistentKey(client) -> None:
    requestData = {"PlayerLevel": 0, "Name": ""}
    deleteResponse = client.delete(path="/api/guildData", query_string=requestData)
    assert deleteResponse.status_code == 200

def test_app_deleteGuildData_IncompleteKey_PlayerLevel(client) -> None:
    requestData = {"Name": "Seer's Guild"}
    deleteResponse = client.delete(path="/api/guildData", query_string=requestData)
    deleteExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'PlayerLevel' was not given."
    }
    
    assert deleteResponse.status_code == 400
    assert deleteResponse.json == deleteExpected

def test_app_deleteGuildData_IncompleteKey_Name(client) -> None:
    requestData = {"PlayerLevel": 99}
    deleteResponse = client.delete(path="/api/guildData", query_string=requestData)
    deleteExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'Name' was not given."
    }
    
    assert deleteResponse.status_code == 400
    assert deleteResponse.json == deleteExpected

def test_app_deleteGuildData_BadKey_PlayerLevel(client) -> None:
    requestData = {"PlayerLevel": "Fails", "Name": "Seer's Guild"}
    deleteResponse = client.delete(path="/api/guildData", query_string=requestData)
    deleteExpected = {
        "error": "Bad request",
        "reason": "Argument 'PlayerLevel' was of incorrect type. Expected: Number"
    }
    
    assert deleteResponse.status_code == 400
    assert deleteResponse.json == deleteExpected

def test_app_deleteGuildData_BadKey_Name(client) -> None:
    requestData = {"PlayerLevel": 99, "Name": 12}
    deleteResponse = client.delete(path="/api/guildData", query_string=requestData)
    deleteExpected = {
        "error": "Bad request",
        "reason": "Argument 'Name' was of incorrect type. Expected: Text"
    }
    
    assert deleteResponse.status_code == 400
    assert deleteResponse.json == deleteExpected

#**                   **#
#*   Item Collection   *#
#**                   **#

# Get Item Collection

def test_app_getItemCollection(client) -> None:
    getResponse = client.get(path="/api/itemCollection")
    assert getResponse.status_code == 200
    assert len(getResponse.json) > 0

def test_app_getItemCollection_GivenID(client) -> None:
    requestData = {"ID": 1}
    getResponse = client.get(path="/api/itemCollection", query_string=requestData)
    getExpected = {
        "ID": 1,
        "Quantity": 5000
    }

    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json == getExpected

def test_app_getItemCollection_IDNotFound(client) -> None:
    requestData = {"ID": 9999}
    getResponse = client.get(path="/api/itemCollection", query_string=requestData)
    getExpected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Primary Key: ID"
    }

    assert getResponse.status_code == 404
    assert getResponse.json == getExpected

def test_app_getItemCollection_BadID(client) -> None:
    requestData = {"ID": "Fails"}
    getResponse = client.get(path="/api/itemCollection", query_string=requestData)
    getExpected = {
        "error": "Bad request",
        "reason": "Argument 'ID' was of incorrect type. Expected: Number"
    }

    assert getResponse.status_code == 400
    assert getResponse.json == getExpected

# Update Item Collection

def test_app_updateItemCollection(client) -> None:
    requestData = {"ID": 2, "Quantity": 2}
    putResponse = client.put(path="/api/itemCollection", query_string=requestData)
    assert putResponse.status_code == 200
    
    getResponse = client.get(path="/api/itemCollection", query_string={"ID": 2})
    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json == requestData

def test_app_updateItemCollection_NotEnoughAttributes(client) -> None:
    requestData = {"ID": 3}
    putResponse = client.put(path="/api/itemCollection", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "No values to be updated were provided",
        "arguments": [ #! Would need to be updated as the DB is updated
            {"Name": "ID", "Type": "Number"},
            {"Name": "Quantity", "Type": "Number"},
        ]
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateItemCollection_NoIDProvided(client) -> None:
    requestData = {"Quantity": 9999}
    putResponse = client.put(path="/api/itemCollection", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'ID' was not given."
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateItemCollection_IDNotFound(client) -> None:
    requestData = {"ID": 9999, "Quantity": 0}
    putResponse = client.put(path="/api/itemCollection", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Primary Key: ID"
    }
    
    assert putResponse.status_code == 404
    assert putResponse.json == putExpected

def test_app_updateItemCollection_BadID(client) -> None:
    requestData = {"ID": "Fails", "Quantity": 0}
    putResponse = client.put(path="/api/itemCollection", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Argument 'ID' was of incorrect type. Expected: Number"
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateItemCollection_BadArguments(client) -> None:
    requestData = {"ID": 3, "Quantity": "Fails"}
    putResponse = client.put(path="/api/itemCollection", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Argument 'Quantity' was of incorrect type. Expected: Number"
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

# Insert Item Collection

def test_app_insertItemCollection(client) -> None:
    requestData = {"ID": 5, "Quantity": 623}
    postResponse = client.post(path="/api/itemCollection", query_string=requestData)
    assert postResponse.status_code == 200

    #^ Confirm POST worked correctly
    getResponse = client.get(path="/api/itemCollection", query_string={"ID": 5})
    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json == requestData

def test_app_insertItemCollection_IDConflict(client) -> None:
    requestData = {"ID": 5, "Quantity": 25000}
    postResponse = client.post(path="/api/itemCollection", query_string=requestData)

    postExpected = {
        "error": "Conflict",
        "reason": "ID already in use."
    }
    assert postResponse.status_code == 409
    assert postResponse.json == postExpected

def test_app_insertItemCollection_RequireAttributeNotGiven(client) -> None:
    requestData = {"ID": 6}
    postResponse = client.post(path="/api/itemCollection", query_string=requestData)
    postExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'Quantity' was not given."
    }
    
    assert postResponse.status_code == 400
    assert postResponse.json == postExpected

def test_app_insertItemCollection_BadArguments(client) -> None:
    firstResponse = client.post(path="/api/itemCollection", query_string={
        "ID": "Fails",
        "Quantity": 12
    })

    firstExpected = {
        "error": "Bad request",
        "reason": "Argument 'ID' was of incorrect type. Expected: Number"
    }
    
    assert firstResponse.status_code == 400
    assert firstResponse.json == firstExpected

    secondResponse = client.post(path="/api/itemCollection", query_string={
        "ID": 12,
        "Quantity": "Fails"
    })
    
    secondExpected = {
        "error": "Bad request",
        "reason": "Argument 'Quantity' was of incorrect type. Expected: Number"
    }

    assert secondResponse.status_code == 400
    assert secondResponse.json == secondExpected

# Delete Item Collection

def test_app_deleteItemCollection(client) -> None:
    requestData = {"ID": 4}
    deleteResponse = client.delete(path="/api/itemCollection", query_string=requestData)
    assert deleteResponse.status_code == 200

    #^ Confirm DELETE worked
    getResponse = client.get(path="/api/itemCollection", query_string=requestData)
    expected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Primary Key: ID"
    }
    
    assert getResponse.status_code == 404
    assert getResponse.json == expected

def test_app_deleteItemCollection_NonexistentID(client) -> None:
    requestData = {"ID": 9999}
    deleteResponse = client.delete(path="/api/itemCollection", query_string=requestData)
    assert deleteResponse.status_code == 200

def test_app_deleteItemCollection_NoIDGiven(client) -> None:
    requestData = {}
    deleteResponse = client.delete(path="/api/itemCollection", query_string=requestData)
    deleteExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'ID' was not given."
    }
    
    assert deleteResponse.status_code == 400
    assert deleteResponse.json == deleteExpected

def test_app_deleteItemCollection_BadID(client) -> None:
    requestData = {"ID": "Fails"}
    deleteResponse = client.delete(path="/api/itemCollection", query_string=requestData)
    deleteExpected = {
        "error": "Bad request",
        "reason": "Argument 'ID' was of incorrect type. Expected: Number"
    }
    
    assert deleteResponse.status_code == 400
    assert deleteResponse.json == deleteExpected

#**                  **#
#*     Item Data      *#
#**                  **#

# Get Item Data

def test_app_getItemData(client) -> None:
    getResponse = client.get(path="/api/itemData")
    assert getResponse.status_code == 200
    assert len(getResponse.json) > 0

def test_app_getItemData_GivenID(client) -> None:
    requestData = {"ID": 1}
    getResponse = client.get(path="/api/itemData", query_string=requestData)
    getExpected = {
        "ID": 1,
        "Name": "Small Health Potion",
        "Tier": 1,
        "Type": "Curatives",
        "Rarity": "Common",
        "IsEvent": 0,
        "IsRaidDrop": 0,
        "IsBossScaling": 0,
        "BSP": 12.5,
        "PSC": 0,
        "Filepath": "/img/useables/potion.png",
        "Base64": None,
        "Ignored": False,
        "Removed": False,
        "Deleted": None
    }

    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json == getExpected

def test_app_getItemData_IDNotFound(client) -> None:
    requestData = {"ID": 9999}
    getResponse = client.get(path="/api/itemData", query_string=requestData)
    getExpected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Primary Key: ID"
    }

    assert getResponse.status_code == 404
    assert getResponse.json == getExpected

def test_app_getItemData_BadID(client) -> None:
    requestData = {"ID": "Fails"}
    getResponse = client.get(path="/api/itemData", query_string=requestData)
    getExpected = {
        "error": "Bad request",
        "reason": "Argument 'ID' was of incorrect type. Expected: Number"
    }

    assert getResponse.status_code == 400
    assert getResponse.json == getExpected

# Update Item Data

def test_app_updateItemData(client) -> None:
    requestData = {
        "ID": 2,                    #* Previous Values *#
        "Name": "Aglovale",         # "Fine Whetstone"		0	0	0		0	
        "Tier": 10,                 # 2
        "Type": "Weapons",          # "Items"
        "Rarity": "Legendary",      # "Superior"
        "IsEvent": 1,               # 0
        "IsRaidDrop": 1,            # 0
        "IsBossScaling": 1,         # 0
        "BSP": 2306500.00,          # 1250.0
        "PSC": 4,                   # 0
        "Filepath": "/img/weapons/aglovale.png", # "/img/useables/whetstone.png"
        
        #? While I probably should test that these values can be written to...
        # "Base64": None,             # None
        # "Ignored": False,           # False
        # "Removed": False,           # False
        # "Deleted": None             # None
    }
    putResponse = client.put(path="/api/itemData", query_string=requestData)
    assert putResponse.status_code == 200

    getResponse = client.get(path="/api/itemData", query_string={"ID": 2})
    getExpected = {
        "ID": 2,
        "Name": "Aglovale",
        "Tier": 10,
        "Type": "Weapons",
        "Rarity": "Legendary",
        "IsEvent": 1,
        "IsRaidDrop": 1,
        "IsBossScaling": 1,
        "BSP": 2306500.00,
        "PSC": 4,
        "Filepath": "/img/weapons/aglovale.png",
        "Base64": None,
        "Ignored": False,
        "Removed": False,
        "Deleted": None
    }
    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json == getExpected

def test_app_updateItemData_NotEnoughAttributes(client) -> None:
    requestData = {"ID": 3}
    putResponse = client.put(path="/api/itemData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "No values to be updated were provided",
        "arguments": [ #! Would need to be updated as the DB is updated
            {"Name": "ID",            "Type": "Number"},
            {"Name": "Quantity",      "Type": "Number"},
            {"Name": "ID",            "Type": "Number"},
            {"Name": "Name",          "Type": "Text"},
            {"Name": "Tier",          "Type": "Number"},
            {"Name": "Type",          "Type": "Text"},
            {"Name": "Rarity",        "Type": "Text"},
            {"Name": "IsEvent",       "Type": "Boolean"},
            {"Name": "IsRaidDrop",    "Type": "Boolean"},
            {"Name": "IsBossScaling", "Type": "Boolean"},
            {"Name": "BSP",           "Type": "Number"},
            {"Name": "PSC",           "Type": "Number"},
            {"Name": "Filepath",      "Type": "Text"},
            {"Name": "Base64",        "Type": "Text"},
            {"Name": "Ignored",       "Type": "Boolean"},
            {"Name": "Removed",       "Type": "Boolean"},
        ]
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateItemData_NoIDProvided(client) -> None:
    requestData = {"Name": "Dagger"}
    putResponse = client.put(path="/api/itemData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'ID' was not given."
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateItemData_IDNotFound(client) -> None:
    requestData = {"ID": 9999, "Name": "Dagger"}
    putResponse = client.put(path="/api/itemData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Primary Key: ID"
    }

    assert putResponse.status_code == 404
    assert putResponse.json == putExpected

def test_app_updateItemData_BadID(client) -> None:
    requestData = {"ID": "Fails", "Name": "Dagger"}
    putResponse = client.put(path="/api/itemData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Argument 'ID' was of incorrect type. Expected: Number"
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

def test_app_updateItemData_BadArguments(client) -> None:
    requestData = {"ID": 3, "Name": "Dagger", "Tier": "Fails"}
    putResponse = client.put(path="/api/itemData", query_string=requestData)
    putExpected = {
        "error": "Bad request",
        "reason": "Argument 'Tier' was of incorrect type. Expected: Number"
    }
    
    assert putResponse.status_code == 400
    assert putResponse.json == putExpected

    #^ Confirm PUT failed to update the entry
    getResponse = client.get(path="/api/itemData", query_string={"ID": 3})
    getExpected = {
        "ID": 3,
        "Name": "Hardened Steel",
        "Tier": 3,
        "Type": "Materials",
        "Rarity": "Famed",
        "IsEvent": 0,
        "IsRaidDrop": 0,
        "IsBossScaling": 0,
        "BSP": 250.0,
        "PSC": 0,
        "Filepath": "/img/materials/steel.png",
        "Base64": None,
        "Ignored": False,
        "Removed": False,
        "Deleted": None
    }
    
    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == getExpected

# Insert Item Data

def test_app_insertItemData_WithID(client) -> None:
    requestData = {
        "ID": 8,
        "Name": "Aldon's Hat",
        "Tier": 2,
        "Type": "Head",
        "Rarity": "Common",
        "IsEvent": 0,
        "IsRaidDrop": 0,
        "IsBossScaling": 0,
        "BSP": 637.50,
        "PSC": 3,
        "Filepath": "/img/armor/leather_hat.png",
        "Base64": None,
        "Ignored": False,
        "Removed": False,
        "Deleted": None
    }
    postResponse = client.post(path="/api/itemData", query_string=requestData)
    assert postResponse.status_code == 200

    #^ Confirm POST worked correctly
    getResponse = client.get(path="/api/itemData", query_string={"ID": 8})
    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == requestData

def test_app_insertItemData_WithoutID(client) -> None:
    requestData = {
        "Name": "Ambrosia",
        "Tier": 7,
        "Type": "Items",
        "Rarity": "Superior",
        "IsEvent": 0,
        "IsRaidDrop": 0,
        "IsBossScaling": 0,
        "BSP": 10000.0,
        "PSC": 0,
        "Filepath": "/img/useables/ambrosia.png",
    }
    postResponse = client.post(path="/api/itemData", query_string=requestData)
    assert postResponse.status_code == 200

    #^ Confirm POST worked correctly
    getResponse = client.get(path="/api/itemData", query_string={"ID": 9})
    expected = {
        "ID": 9,
        "Name": "Ambrosia",
        "Tier": 7,
        "Type": "Items",
        "Rarity": "Superior",
        "IsEvent": 0,
        "IsRaidDrop": 0,
        "IsBossScaling": 0,
        "BSP": 10000.0,
        "PSC": 0,
        "Filepath": "/img/useables/ambrosia.png",
        "Base64": None,
        "Ignored": False,
        "Removed": False,
        "Deleted": None
    }

    assert getResponse.status_code == 200
    assert len(getResponse.json) == 1
    assert getResponse.json[0] == expected

def test_app_insertItemData_IDConflict(client) -> None:
    requestData = {
        "ID": 1,
        "Name": "FooBar",
        "Tier": 1,
        "Type": "Items",
        "Rarity": "Common",
        "IsEvent": 0,
        "IsRaidDrop": 0,
        "IsBossScaling": 0,
        "BSP": 12.5,
        "PSC": 0,
        "Filepath": "does_not_exist.png",
    }
    postResponse = client.post(path="/api/itemData", query_string=requestData)
    postExpected = {
        "error": "Conflict",
        "reason": "ID already in use."
    }
    assert postResponse.status_code == 409
    assert postResponse.json == postExpected

def test_app_insertItemData_RequireAttributeNotGiven(client) -> None:
    requestData = {
        "ID": 1,
        # Missing Item Name
        "Tier": 1,
        "Type": "Items",
        "Rarity": "Common",
        "IsEvent": 0,
        "IsRaidDrop": 0,
        "IsBossScaling": 0,
        "BSP": 12.5,
        "PSC": 0,
        "Filepath": "does_not_exist.png",
    }
    postResponse = client.post(path="/api/itemData", query_string=requestData)
    postExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'Name' was not given."
    }
    
    assert postResponse.status_code == 400
    assert postResponse.json == postExpected

def test_app_insertItemData_BadArguments(client) -> None:
    requestData = {
        "ID": 1,
        "Name": "Dagger",
        "Tier": "Fails",
        "Type": "Items",
        "Rarity": "Common",
        "IsEvent": 0,
        "IsRaidDrop": 0,
        "IsBossScaling": 0,
        "BSP": 12.5,
        "PSC": 0,
        "Filepath": "does_not_exist.png",
    }
    postResponse = client.post(path="/api/itemData", query_string=requestData)
    postExpected = {
        "error": "Bad request",
        "reason": "Argument 'Tier' was of incorrect type. Expected: Number"
    }
    
    assert postResponse.status_code == 400
    assert postResponse.json == postExpected

# Delete Item Data

def test_app_deleteItemData(client) -> None:
    requestData = {"ID": 6}
    deleteResponse = client.delete(path="/api/itemData", query_string=requestData)

    assert deleteResponse.status_code == 200

    #^ Confirm DELETE via GET
    getResponse = client.get(path="/api/itemData", query_string=requestData)
    getExpected = {
        "error": "Bad request",
        "reason": "Could not find entry with given Primary Key: ID"
    }
    
    assert getResponse.status_code == 404
    assert getResponse.json == getExpected

def test_app_deleteItemData_NonexistentID(client) -> None:
    requestData = {"ID": 9999}
    deleteResponse = client.delete(path="/api/itemData", query_string=requestData)

    assert deleteResponse.status_code == 200

def test_app_deleteItemData_NoIDGiven(client) -> None:
    requestData = {"ID": 9999}
    deleteResponse = client.delete(path="/api/itemData", query_string=requestData)
    deleteExpected = {
        "error": "Bad request",
        "reason": "Required attribute 'ID' was not given."
    }
    
    assert deleteResponse.status_code == 400
    assert deleteResponse.json == deleteExpected

def test_app_deleteItemData_BadID(client) -> None:
    requestData = {"ID": "Fails"}
    deleteResponse = client.delete(path="/api/itemData", query_string=requestData)
    deleteExpected = {
        "error": "Bad request",
        "reason": "Argument 'ID' was of incorrect type. Expected: Number"
    }
    
    assert deleteResponse.status_code == 400
    assert deleteResponse.json == deleteExpected