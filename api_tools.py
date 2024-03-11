from fastapi.responses import HTMLResponse, RedirectResponse

__home_url = "/"
__static_path = "/static"
__static_dir = "static"
__stylesheet_path = __static_path + "/tic-tac-toe.css"

__page_head = """<!DOCTYPE html>\n<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Play Games</title>
    """ + """<link rel="stylesheet" href=\"""" + __stylesheet_path + """">
</head>
"""
__page_start_body = """
<body>
<table class="center">
<tr><td>
"""
__page_end_body = """
</td></tr>
</table>
</body>\n</html>\n"""

def home_url():
    return __home_url

def static_path():
    return __static_path

def static_dir():
    return __static_dir

def create_response_page(content):
    page_content = __page_head + __page_start_body + content + __page_end_body
    return HTMLResponse(content=page_content, status_code=200)

def basic_link_element(link, text, link_class=None):
    elem = "<a href=\"" + link + "\""
    elem += ">" if link_class == None else " class=\"" + link_class + "\">"
    elem += text + "</a>"
    return elem

def basic_form_element(action_link, method="post"):
    return "<form action=\"" + action_link + "\" method=\"" + method + "\">"

def make_url_with_value(base_link, value):
    return base_link + "/" + str(value)

def make_button_table(buttons):
    content = """<table class="center"><tr><div class="center">"""
    for button in buttons:
        content += "<td>" + button + "</td>"
    content += """</div></tr></table>"""
    return content
