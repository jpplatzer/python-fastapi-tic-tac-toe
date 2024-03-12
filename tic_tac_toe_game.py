# This is where the Tic Tac Toe does its thing

from enum import Enum
from game import Game
from tic_tac_toe_player import TicTacToePlayer
from tic_tac_toe_board import Tic_Tac_Toe_Board as Board

class Ttt_Game(Game):
    GameStatus = Enum('GameStatus', ['ACTIVE', 'WON', 'DRAW'])
    __game_name = "tic_tac_toe"

    def game_name():
        return Ttt_Game.__game_name

    __move_status_to_game_status_map = {
        Board.MoveStatus.VALID: GameStatus.ACTIVE,
        Board.MoveStatus.INVALID: GameStatus.ACTIVE,
        Board.MoveStatus.WON: GameStatus.WON,
        Board.MoveStatus.DRAW: GameStatus.DRAW,
    }
 
    def __init__(self, players, game_id, play_link) -> None:
        super().__init__(Ttt_Game.__game_name, players, game_id)
        self.__status = self.GameStatus.ACTIVE
        self.__players_turn = 0
        self.__board = Board(game_id, play_link)

    def status(self) -> GameStatus:
        return self.__status
    
    def current_player(self) -> TicTacToePlayer:
        return self.players()[self.__players_turn]
    
    def draw_board_html(self) -> str:
        active = self.__status == self.GameStatus.ACTIVE
        return self.__board.draw_html(active)

    def begin_game_position():
        return Board.num_squares()
    
    def make_move(self, position) -> Board.MoveStatus:
        if self.current_player().is_auto():
            move_status = self.__perform_auto_move()
        else:
            move_status = self.__perform_move(position)
            if move_status == Board.MoveStatus.VALID and \
                self.current_player().is_auto():
                move_status = self.__perform_auto_move()
        return move_status

    def __perform_move(self, position):
        if self.__status != self.GameStatus.ACTIVE:
            return Board.MoveStatus.INVALID
        move_status = self.__board.make_move(position, self.current_player().role())
        self.__status = self.__move_status_to_game_status_map[move_status]
        if move_status == Board.MoveStatus.VALID:
            self.__players_turn = Ttt_Game.next_turn(self.__players_turn)
        return move_status

    def __perform_auto_move(self):
        position = self.__board.auto_move_position(self.current_player().role())
        return self.__perform_move(position)

    def next_turn(current_turn):
        return (current_turn + 1) % 2

