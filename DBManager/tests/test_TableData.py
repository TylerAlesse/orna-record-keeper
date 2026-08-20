import pytest
from types import UnionType
from classes.TableData import TableData

# Sets current working directory to test file location
@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname)

# Test Classes to facilitate testing

class MissingAttributesTest(TableData):
    __slots__ = []
    TableName: str = 'MissingAttributesTest'

class TestSubClass(TableData):
    __slots__ = 'Foo', 'Bar', 'FooBar'
    Foo: int
    Bar: bool
    FooBar: str|None
    TableName: str = "TestSubClass"

    #& Subclasses Test Independently
    @staticmethod
    def createFromTuple(data: tuple):
        return

    #& Subclasses Test Independently
    def exportJSON(self) -> str:
        return ""

# getAnnotation

def test_TableData_getAnnotation() -> None:
    assert TestSubClass.getAnnotation("Foo") is int
    assert TestSubClass.getAnnotation("Bar") is bool
    assert type(TestSubClass.getAnnotation("FooBar")) is UnionType

# createArgumentsList

def test_TableData_createArgumentsList_EmptyIgnored() -> None:
    actual = TestSubClass.createArgumentsList()
    expected = [
        {
            "name": "Foo",
            "type": int,
            "val": None,
            "insertReq": True
        },
        {
            "name": "Bar",
            "type": bool,
            "val": None,
            "insertReq": True
        },
        {
            "name": "FooBar",
            "type": str,
            "val": None,
            "insertReq": False
        },
    ]
    assert actual == expected

def test_TableData_createArgumentsList_HasIgnored() -> None:
    ignore = ["Bar"]
    actual = TestSubClass.createArgumentsList(ignore)
    expected = [
        {
            "name": "Foo",
            "type": int,
            "val": None,
            "insertReq": True
        },
        {
            "name": "FooBar",
            "type": str,
            "val": None,
            "insertReq": False
        },
    ]
    assert actual == expected

def test_TableData_createArgumentsList_NoAttributes() -> None:
    actual = MissingAttributesTest.createArgumentsList()
    expected = []
    assert actual == expected

def test_TableData_createArgumentsList_Fails_NoTableName() -> None:
    with pytest.raises(AttributeError):
        TableData.createArgumentsList()

# createSelectQuery

def test_TableData_createSelectQuery_EmptyIgnore_EmptyCondition() -> None:
    query, params = TestSubClass.createSelectQuery()
    expectedQuery = "SELECT Foo,Bar,FooBar FROM TestSubClass"
    expectedParams = []
    assert query == expectedQuery
    assert params == expectedParams

def test_TableData_createSelectQuery_HasIgnore_EmptyCondition() -> None:
    query, params = TestSubClass.createSelectQuery(ignored=["Bar"])
    expectedQuery = "SELECT Foo,FooBar FROM TestSubClass"
    expectedParams = []
    assert query == expectedQuery
    assert params == expectedParams

def test_TableData_createSelectQuery_EmptyIgnore_HasConditions() -> None:
    query, params = TestSubClass.createSelectQuery(conditions={"Foo": 1})
    expectedQuery = "SELECT Foo,Bar,FooBar FROM TestSubClass WHERE Foo = ?"
    expectedParams = [1]
    assert query == expectedQuery
    assert params == expectedParams

def test_TableData_createSelectQUery_HasIgnore_HasConditions() -> None:
    query, params = TestSubClass.createSelectQuery(["FooBar"], {"Foo": 1})
    expectedQuery = "SELECT Foo,Bar FROM TestSubClass WHERE Foo = ?"
    expectedParams = [1]
    assert query == expectedQuery
    assert params == expectedParams

def test_TableData_createSelectQuery_Fails_MissingTableName() -> None:
    with pytest.raises(AttributeError):
        TableData.createSelectQuery()

def test_TableData_createSelectQuery_Fails_MissingAttributes() -> None:
    with pytest.raises(AttributeError):
        MissingAttributesTest.createSelectQuery()

def test_TableData_createSelectQuery_Fails_ZeroValidColumns() -> None:
    with pytest.raises(RuntimeError):
        TestSubClass.createSelectQuery(["Foo", "Bar", "FooBar"])

# createUpdateQuery

def test_TableData_createUpdateQuery_HasConditions() -> None:
    pytest.skip()

def test_TableData_createUpdateQuery_EmptyConditions() -> None:
    pytest.skip()

def test_TableData_createUpdateQuery_Fails_NoArguments() -> None:
    pytest.skip()

def test_TableData_createUpdateQuery_Fails_MissingTableName() -> None:
    pytest.skip()

def test_TableData_createUpdateQuery_Fails_MissingAttributes() -> None:
    pytest.skip()

# createInsertQuery

def test_TableData_createInsertQuery() -> None:
    pytest.skip()

def test_TableData_createInsertQuery_MissingRequiredArguments() -> None:
    pytest.skip()

def test_TableData_createInsertQuery_NoArgumentsGiven() -> None:
    pytest.skip()

def test_TableData_createInsertQuery_Fails_MissingTableName() -> None:
    pytest.skip()

def test_TableData_createInsertQuery_Fails_MissingAttributes() -> None:
    pytest.skip()

# createDeleteQuery

def test_TableData_createDeleteQuery_HasConditions() -> None:
    pytest.skip()

def test_TableData_createDeleteQuery_MissingConditions() -> None:
    pytest.skip()

def test_TableData_createDeleteQuery_Fails_MissingTableName() -> None:
    pytest.skip()

def test_TableData_createDeleteQuery_Fails_MissingAttributes() -> None:
    pytest.skip()