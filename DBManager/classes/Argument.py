class Argument:
    ArgName: str
    ArgType: type
    InsertReq: bool

    def __init__(self, _name: str, _type: type, _value, _insertReq: bool) -> None:
        self.ArgName = _name
        self.ArgType = _type
        self.ArgValue = _value
        self.InsertReq = _insertReq