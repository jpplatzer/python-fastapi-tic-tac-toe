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
 
    def __init__(self, players, game_id, move_link) -> None:
        super().__init__(Ttt_Game.__game_name, players, game_id)
        self.__status = self.GameStatus.ACTIVE
        self.__players_turn = 0
        self.__board = Board(game_id, move_link)

    def status(self) -> GameStatus:
        return self.__status
    
    def current_player(self) -> TicTacToePlayer:
        return self.players()[self.__players_turn]
    
    def draw_board_html(self) -> str:
        active = self.__status == self.GameStatus.ACTIVE
        return self.__board.draw_html(active)

    def make_move(self, position) -> Board.MoveStatus:
        if self.__status != self.GameStatus.ACTIVE:
            return Board.MoveStatus.INVALID
        player = self.current_player()
        move_status = self.__board.make_move(position, player.role())
        self.__status = self.__move_status_to_game_status_map[move_status]
        if move_status == Board.MoveStatus.VALID:
            self.__players_turn = self.next_turn()
        return move_status
    
    def next_turn(self):
        return (self.__players_turn + 1) % 2
    
    def make_auto_move(self, player) -> Board.MoveStatus:
        position = self.__board.auto_move_position(player.role())
        return self.make_move(position)
