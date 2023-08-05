class MultiplePrices:
    def __init__(self, 
                 UNIX_TIMESTAMP: int, 
                 SYMBOL: str, 
                 CARRY: float = None, 
                 CARRY_CONTRACT: int = None,
                 PRICE: float = None, 
                 PRICE_CONTRACT: int = None, 
                 FORWARD: float = None, 
                 FORWARD_CONTRACT: int = None):
        
        self.UNIX_TIMESTAMP = UNIX_TIMESTAMP
        self.SYMBOL = SYMBOL
        self.CARRY = CARRY
        self.CARRY_CONTRACT = CARRY_CONTRACT
        self.PRICE = PRICE
        self.PRICE_CONTRACT = PRICE_CONTRACT
        self.FORWARD = FORWARD
        self.FORWARD_CONTRACT = FORWARD_CONTRACT
