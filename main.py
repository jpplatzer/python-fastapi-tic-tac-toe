from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import api_tools
from tic_tac_toe_endpoint import setup_link_two as ttt_setup_link_two, \
    setup_link_one as ttt_setup_link_one, router as ttt_router

app = FastAPI()
app.include_router(ttt_router)

app.mount(api_tools.static_path(), \
    StaticFiles(directory=api_tools.static_dir()), name="static")

def homepage_content():
    ttt_one_button = api_tools.basic_link_element(ttt_setup_link_one, \
        "Tic-Tac-Toe<br>Single Player", "game-select-button")
    ttt_two_button = api_tools.basic_link_element(ttt_setup_link_two, \
        "Tic-Tac-Toe<br>Two Player", "game-select-button")
    content = """
        <div class="center"><p><h2>Would you like to play a game?</h2></p>
        <br />
        <p>"""
    content += api_tools.make_button_table([ttt_one_button, ttt_two_button])
    content += """</p>
        <br />
        <p><h2>Nope, just want to stare at the screen</h2></p></div>\n"""
    return content

@app.get(api_tools.home_url())
def home_page():
    return api_tools.create_response_page(homepage_content())

