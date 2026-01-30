import shutil
import pytest
import sqlite3
from classes.DBHandler import DBHandler

def copy(src_path, dst_path):
    shutil.copyfile(src_path, dst_path)

@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname)

@pytest.fixture
def mock_DBHandler() -> DBHandler:
    return DBHandler("none")

@pytest.fixture
def mock_DBHandler_badFilepath() -> DBHandler:
    return DBHandler("does_not_exist.db")

# Initialization
def test_DBHandler_init(mock_DBHandler) -> None:
    assert isinstance(mock_DBHandler, DBHandler)

# getFilepath
def test_DBHandler_getFilepath(mock_DBHandler) -> None:
    assert mock_DBHandler.getFilepath() == "none"

# getAutocommit
def test_DBHandler_getAutocommit(mock_DBHandler) -> None:
    assert mock_DBHandler.getAutocommit() == True

# setAutocommit
def test_DBHandler_setAutocommit(mock_DBHandler) -> None:
    mock_DBHandler.setAutocommit(False)

# isConnected
def test_DBHandler_isConnected_False(mock_DBHandler) -> None:
    assert mock_DBHandler.isConnected() == False

def test_DBHandler_isConnected_True(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db")
    tempDB.createConnetion() # Relies on createConnection to be True
    assert tempDB.isConnected() == True
    tempDB.closeConnection()

# createConnection
def test_DBHandler_createConnection_validFilepath(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db")
    tempDB.createConnetion()

def test_DBHandler_createConnection_invalidFilepath(mock_DBHandler_badFilepath: DBHandler) -> None:
    with pytest.raises(FileNotFoundError):
        mock_DBHandler_badFilepath.createConnetion()

def test_DBHandler_createConnection_preexistingConnection(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db")
    tempDB.createConnetion()
    tempDB.createConnetion() # second call should do nothing

# closeConnection
def test_DBHandler_closeConnection_success(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db")
    tempDB.createConnetion()
    tempDB.closeConnection()
    assert tempDB.isConnected() == False

def test_DBHandler_closeConnection_noConnection(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db")
    assert tempDB.isConnected() == False

# request
def test_DBHandler_request_noConnection(mock_DBHandler) -> None:
    with pytest.raises(AttributeError):
        mock_DBHandler.request("")

def test_DBHandler_request_validRequest_select(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db")
    tempDB.createConnetion()
    
    expected = [
        (1, "Foo"),
        (2, "Bar"),
        (3, "FooBar")
    ]

    actual = tempDB.request("SELECT ID, Value FROM test_table ORDER BY ID ASC")
    assert expected == actual

def test_DBHandler_request_validRequest_create(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db")
    tempDB.createConnetion()

    tempDB.request('CREATE TABLE "new_table" ("ID" INTEGER)')
    
    expected = list()
    actual = tempDB.request("SELECT * FROM new_table") # Shouldn't error
    assert expected == actual

def test_DBHandler_request_validRequest_insert(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db")
    tempDB.createConnetion()

    tempDB.request('INSERT INTO test_table VALUES (4, "Baz")')
    
    expected = [
        (1, "Foo"),
        (2, "Bar"),
        (3, "FooBar"),
        (4, "Baz")
    ]
    actual = tempDB.request("SELECT ID, Value FROM test_table ORDER BY ID ASC")
    assert expected == actual

def test_DBHandler_request_validRequest_delete(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db")
    tempDB.createConnetion()
    tempDB.request("DELETE FROM test_table WHERE ID = 1")

    expected = [
        (2, "Bar"),
        (3, "FooBar")
    ]
    actual = tempDB.request("SELECT ID, Value FROM test_table ORDER BY ID ASC")
    assert expected == actual

def test_DBHandler_request_invalidRequest(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db")
    tempDB.createConnetion()
    with pytest.raises(sqlite3.OperationalError):
        tempDB.request("WHERE SELECT FROM")

# commit
def test_DBHandler_commit(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db", False)
    tempDB.createConnetion()
    tempDB.request("DELETE FROM test_table WHERE ID = 1")
    tempDB.commit()
    tempDB.closeConnection()

    newConn = DBHandler(tmp_path / "test.db", False)
    newConn.createConnetion()

    expected = [
        (2, "Bar"),
        (3, "FooBar")
    ]
    actual = newConn.request("SELECT ID, Value FROM test_table ORDER BY ID ASC")
    assert expected == actual

def test_DBHandler_commit_noConnection(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db", False)
    with pytest.raises(AttributeError):
        tempDB.commit()

# rollback
def test_DBHandler_rollback(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db", False)
    tempDB.createConnetion()
    tempDB.request("DELETE FROM test_table WHERE ID = 1")
    tempDB.rollback()

    expected = [
        (1, "Foo"),
        (2, "Bar"),
        (3, "FooBar")
    ]
    actual = tempDB.request("SELECT ID, Value FROM test_table ORDER BY ID ASC")
    assert expected == actual

def test_DBHandler_rollback_noConnection(tmp_path) -> None:
    copy("./data/test.db", tmp_path / "test.db")
    tempDB = DBHandler(tmp_path / "test.db", False)
    with pytest.raises(AttributeError):
        tempDB.rollback()