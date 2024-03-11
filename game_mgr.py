from datetime import datetime, timedelta

class GameMgr:
    __game_key = "game"
    __last_time_key = "last_time"

    @staticmethod
    def __make_games_value(game):
        return {
            GameMgr.__game_key: game,
            GameMgr.__last_time_key: datetime.now()
        }

    # Make this a singleton class
    def __new__(cls):
        if not hasattr(cls, '__instance'):
            cls.__instance = super(GameMgr, cls).__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.__games = {}

    def get_new_game_id(self):
        id = max(iter(self.__games)) + 1 if len(self.__games) > 0 else 1
        return id

    def set_game(self, game, game_id):
        self.__games[game_id] = self.__make_games_value(game)
        return game
    
    def get_game(self, name, game_id):
        game_value = self.__games.get(game_id)
        if game_value == None or game_value[self.__game_key].name() != name:
            return None
        game_value[GameMgr.__last_time_key] = datetime.now()
        return game_value[GameMgr.__game_key]

    def del_game(self, game_id):
        self.__games[game_id] = None

