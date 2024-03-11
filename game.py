
class Game:
    def __init__(self, name, players, game_id) -> None:
        self.__name = name
        self.__players = players
        self.__game_id = game_id

    def name(self):
        return self.__name
    
    def players(self):
        return self.__players

    def game_id(self):
        return self.__game_id
    
    def set_game_id(self, game_id):
        self.__game_id = game_id
    