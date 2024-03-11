from player import Player

class TicTacToePlayer(Player):
    x_role = "X"
    o_role = "O"

    def __init__(self, name, role, order, is_auto=False) -> None:
        super().__init__(name)
        self.__role = role
        self.__order = order
        self.__is_auto = is_auto
    
    def role(self):
        return self.__role
    
    def order(self):
        return self.__order

    def is_auto(self):
        return self.__is_auto
