
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
import api_tools
from game_mgr import GameMgr
from tic_tac_toe_player import TicTacToePlayer
from tic_tac_toe_game import Ttt_Game

router = APIRouter()
game_mgr = GameMgr()

tic_tac_toe_link = "/games/tic-tac-toe"
setup_link_one = tic_tac_toe_link + "/setup_one"
setup_link_two = tic_tac_toe_link + "/setup_two"
start_link = tic_tac_toe_link + "/start"
play_link = tic_tac_toe_link + "/play"
replay_link = tic_tac_toe_link + "/replay"
end_link = tic_tac_toe_link + "/end"

def setup_one_content():
    you_button = """<input type="submit" class="blue-button" name="auto" value="You Go First">"""
    computer_button = """<input type="submit" class="blue-button" name="auto" value="Computer Goes First">"""
    button_table = api_tools.make_button_table([you_button, computer_button])
    content = """
        <div class="center"><p><h2>Let's Setup A Tic-Tac-Toe Game</h2></p>
        <br />
        <p><h3>Player One will be X's</h3></p>
        <p><h3>Player Two will be O's</h3></p>
        <br />
        """
    content += api_tools.basic_form_element(start_link, "get")
    content += """
            <label for="name1">Player's Name:</label>
            <input type="text" id="name1" name="name1" minlength="1" required><br><br>
            <input type="hidden" id="name2" name="name2" value="Computer">
            """
    content += button_table
    content += """
        </form></p></div>\n"""
    return content

@router.get(setup_link_one)
def __start_tic_tac_toe():
    return api_tools.create_response_page(setup_one_content())

def setup_two_content():
    content = """
        <div class="center"><p><h2>Let's Setup A Tic-Tac-Toe Game</h2></p>
        <br />
        <p><h3>Player One will be X's and go first</h3></p>
        <p><h3>Player Two will be O's and go second</h3></p>
        <br />
        """
    content += api_tools.basic_form_element(start_link, "get")
    content += """
            <label for="name1">Player One's Name:</label>
            <input type="text" id="name1" name="name1" minlength="1" required><br><br>
            <label for="name2">Player Two's Name:</label>
            <input type="text" id="name2" name="name2" minlength="1" required><br><br><br>
            <input type="hidden" id="auto" name="auto" value="None">
            <div class="center"><input type="submit" class="blue-button" value="Let's Play"></div>
        </form></p></div>\n"""
    return content

@router.get(setup_link_two)
def __start_tic_tac_toe():
    return api_tools.create_response_page(setup_two_content())

def __redirect_to_begin_play_response(game):
    play_url = api_tools.make_url_with_value(play_link, game.game_id())
    play_url = api_tools.make_url_with_value(play_url, Ttt_Game.begin_game_position())
    return RedirectResponse(play_url)

def __create_new_game(players):
    game_id = game_mgr.get_new_game_id()
    move_url = api_tools.make_url_with_value(play_link, game_id)
    game = Ttt_Game(players, game_id, move_url)
    game_mgr.set_game(game, game_id)
    return game

@router.get(start_link)
def __tic_tac_toe_page(name1: str, name2: str, auto: str):
    auto1, auto2 = False, False
    p1_name, p2_name = name1, name2
    if auto.find("Computer") >= 0:
        p1_name = name2
        p2_name = name1
        auto1 = True
    elif auto.find("You") >= 0:
        auto2 = True
    player1 = TicTacToePlayer(p1_name, TicTacToePlayer.x_role, 0, auto1)
    player2 = TicTacToePlayer(p2_name, TicTacToePlayer.o_role, 1, auto2)
    players = [player1, player2]
    game = __create_new_game(players)
    return __redirect_to_begin_play_response(game)

def __game_control_button_content(game_id):
    replay_game_link = api_tools.make_url_with_value(replay_link, game_id)
    replay_button = api_tools.basic_link_element(replay_game_link, "Replay Game", "blue-button")
    end_button_link = api_tools.make_url_with_value(end_link, game_id)
    end_button = api_tools.basic_link_element(end_button_link, "End Game", "blue-button")
    return api_tools.make_button_table([replay_button, end_button])

def __game_content(game):
    player = game.current_player()
    players = game.players()
    move_url = api_tools.make_url_with_value(play_link, game.game_id())
    content = """
        <div class="center">
        <p><h1>Tic-Tac-Toe!<br></h1></p>
        <p><h2>"""
    content += players[0].name() + " is X's and "
    content += players[1].name() + """ is O's</h2></p>
        <p>"""
    content += game.draw_board_html() + """</p>
        <h1>"""
    match game.status():
        case Ttt_Game.GameStatus.WON:
            content += player.name() + " Wins!"
        case Ttt_Game.GameStatus.DRAW:
            content += "Oh No, It's A Draw!"
        case _:
            content += player.name() + "'s Turn"
    content += """</h1></p></div>
        """
    content += __game_control_button_content(game.game_id())
    return content

def __invalid_game_content():
    return """
        <p><h1>Oops, the game you're looking for is not available</h1></p>
        <br><br>
        <p><h2>It may have ended</h2></p>"""

def __invalid_game_response():
    return api_tools.create_response_page(__invalid_game_content())

@router.get(api_tools.make_url_with_value(play_link, "{game_id}/{position}"))
def __tic_tac_toe_play(game_id: int, position: int):
    game = game_mgr.get_game(Ttt_Game.game_name(), game_id)
    if game == None:
        content = __invalid_game_content()
    else:    
        game.make_move(position)
        content = __game_content(game)
    return api_tools.create_response_page(content)

@router.get(api_tools.make_url_with_value(replay_link, "{game_id}"))
def __tic_tac_toe_replay(game_id: int):
    game = game_mgr.get_game(Ttt_Game.game_name(), game_id)
    if game == None: return __invalid_game_response()
    new_game = __create_new_game(game.players())
    game_mgr.del_game(game_id)
    return __redirect_to_begin_play_response(new_game)

@router.get(api_tools.make_url_with_value(end_link, "{game_id}"))
def __tic_tac_toe_end(game_id: int):
    game = game_mgr.get_game(Ttt_Game.game_name(), game_id)
    if game == None:
        game_mgr.del_game(game_id)
    return RedirectResponse(api_tools.home_url())

