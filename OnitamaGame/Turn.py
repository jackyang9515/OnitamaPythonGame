class Turn:
    """
    A class that represents the turns a player can have given a specific style

    Attributes:

    row_o: original row number
    col_o: original column number
    row_d: row number after turn has been made
    col_d: column number after turn has been made
    style_name: the given style's name
    player: the player's id
    """
    row_o: int
    col_o: int
    row_d: int
    col_d: int
    style_name: str
    player: str

    def __init__(self, row_o: int, col_o: int, row_d: int, col_d: int,
                 style_name: str, player: str) -> None:
        """
        Initializes the class Turn
        """
        self.row_o = row_o
        self.col_o = col_o
        self.row_d = row_d
        self.col_d = col_d
        self.style_name = style_name
        self.player = player
