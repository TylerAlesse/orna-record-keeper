class DBItemCollection:
    def __init__(self, ID: int, Quantity: int) -> None:
        self.ID = ID
        self.Quantity = Quantity
    
    def exportJSON(self) -> str:
        content = f'"ID":{self.ID},'\
                  f'"Quantity":{self.Quantity}'
        return f'{{{content}}}'