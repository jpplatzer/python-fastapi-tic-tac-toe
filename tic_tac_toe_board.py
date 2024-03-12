from enum import Enum
import functools
import random
import api_tools
from tic_tac_toe_player import TicTacToePlayer

class Tic_Tac_Toe_Board:
    MoveStatus = Enum('MoveStatus', ['VALID', 'INVALID', 'WON', 'DRAW'])
    empty_square = " "
    x_square = TicTacToePlayer.x_role
    o_square = TicTacToePlayer.o_role

    __num_squares = 9

    __square_number_to_cell_class_map = {
        0: "board-lr-cell",
        1: "board-lr-cell",
        2: "board-l-cell",
        3: "board-lr-cell",
        4: "board-lr-cell",
        5: "board-l-cell",
        6: "board-r-cell",
        7: "board-r-cell",
        8: "board-no-cell"
    }

    def __init__(self, game_id, move_link) -> None:
        self.__game_id = game_id
        self.__move_link = move_link
        self.__board = [self.empty_square for i in range(self.__num_squares)]
        self.__highlight = [False for i in range(self.__num_squares)]

    def num_squares():
        return Tic_Tac_Toe_Board.__num_squares

    def find_line(self, find_fcn):
        # Find horizontal lines
        step = 1
        for i in range(0, 9, 3):
            if find_fcn(self.__board, i, step):
                return (i, step)
        # Find vertical lines
        step = 3
        for i in range(3):
            if find_fcn(self.__board, i, step):
                return (i, step)
        # Find the / line
        if find_fcn(self.__board, 2, 2):
            return (2, 2)
        # Find the \ line
        if find_fcn(self.__board, 0, 4):
            return (0, 4)
        return None

    def is_line(board, start, step):
        start_value = board[start]
        return start_value != Tic_Tac_Toe_Board.empty_square and \
            start_value == board[start + step] and \
            start_value == board[start + (step * 2)]
    
    def draw_html(self, active):
        content = """<table class="center">
            """
        for i in range(self.__num_squares):
            square_value = self.__board[i]
            content += "<tr>" if i % 3 == 0 else ""
            content += self.__draw_square(i,  active)
            if i % 3 == 2:
                content += """</tr>
            """
        content += """
        </table>
        """
        return content

    def __draw_square(self, idx, active):
        value = self.__board[idx]
        cell_class = self.__square_number_to_cell_class_map[idx]
        span_class = "hilite-board-text" if self.__highlight[idx] else "board-text"
        if value == self.empty_square:
            cell_text = self.__empty_cell_content(idx, active)
        else:
            cell_text = "X" if value == self.x_square else "O"
        cell_content = "<td class=\"" + cell_class + "\">"
        cell_content += "<span class=\"" + span_class + "\">"
        cell_content += cell_text + "</span></td>"
        return cell_content
    
    def __empty_cell_content(self, idx, active):
        if active:
            link = api_tools.make_url_with_value(self.__move_link, idx)
            href = " href=\"" + link + "\""
        else:
            href = ""
        return "<a class=\"clear-link\"" + href + ">_</a>"

    def __set_highlight(self, start, step):
        for i in range(start, start + (step * 3), step):
            self.__highlight[i] = True

    def make_move(self, position, square_value) -> MoveStatus:
        status: Tic_Tac_Toe_Board.MoveStatus = self.MoveStatus.VALID
        if position not in range(self.__num_squares) or self.__board[position] != self.empty_square:
            return self.MoveStatus.INVALID
        self.__board[position] = square_value
        line_parms = self.find_line(Tic_Tac_Toe_Board.is_line)
        if line_parms != None:
            status = self.MoveStatus.WON
            self.__set_highlight(line_parms[0], line_parms[1])
        elif all(square != Tic_Tac_Toe_Board.empty_square \
            for square in self.__board):
            status = self.MoveStatus.DRAW
        return status

    __corners = [0, 2, 6, 8]

    def auto_move_position(self, square_value) -> int | None:
        position = None
        empties = [i for i in range(self.__num_squares)\
            if self.__board[i] == Tic_Tac_Toe_Board.empty_square]
        num_moves = self.__num_squares - len(empties)
        if num_moves == self.__num_squares: return None
        if num_moves == 0: return random.randint(0, self.__num_squares - 1)
        if self.__board[4] == Tic_Tac_Toe_Board.empty_square: return 4 
        position = self.get_best_next_auto_position(empties, square_value)
        return position
    
    def get_best_next_auto_position(self, empties, square_value) -> int:
        opponents_value = Tic_Tac_Toe_Board.x_square \
            if square_value == Tic_Tac_Toe_Board.o_square else \
                Tic_Tac_Toe_Board.o_square
        # try to win
        position = self.find_best_empty_with_2_1_match(square_value,\
            Tic_Tac_Toe_Board.empty_square)
        if position != None: return position
        # avoid defeat
        position = self.find_best_empty_with_2_1_match(opponents_value,\
            Tic_Tac_Toe_Board.empty_square)
        if position != None: return position
        # pick more favorable position if there is one
        position = self.find_best_empty_with_2_1_match( \
            Tic_Tac_Toe_Board.empty_square, square_value)
        if position != None: return position
        # prefer an empty corner
        pick_list = [i for i in empties if i in Tic_Tac_Toe_Board.__corners]
        if len(pick_list) == 0:
            # any other empty will do
            pick_list = empties
        position = random.choice(pick_list)
        return position
    
    def find_best_empty_with_2_1_match(self, value1, value2) -> int:
        position = None
        
        def matches(board, start, step):
            count1 = sum(1 for i in range(start, start + (step * 3), step) \
                if board[i] == value1)
            count2 = sum(1 for i in range(start, start + (step * 3), step) \
                if board[i] == value2)
            return count1 == 2 and count2 == 1
        
        line_params = self.find_line(matches)
        if line_params:
            start = line_params[0]
            step = line_params[1]
            for i in range(start, start + (step * 3), step):
                if self.__board[i] == Tic_Tac_Toe_Board.empty_square:
                    position = i
                    if i in self.__corners: break # again prefer corners
        return position
