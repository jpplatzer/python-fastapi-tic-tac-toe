# Tic-Tac-Toe Game

Python FastAPI example server-side implementation of a Tic-Tac-Toe game with an auto-play mode.

The main purpose of this project was to get some experience with Python's FastAPI framework for implementing REST APIs.

Some tradeoffs were made for the sake of simplicity and expediency:

* The App is implemented with server-side HTML rendering rather than a client-side web application using something like React.
* It could be implemented more simply using a client-side Javascript implementation, but the purpose was to get some experience with Fastapi.
* Because server-side only HTML rendering is used, the API relies on Get methods rather than on a CRUD interface with Get, Post, Put, and Delete methods.
* Authentication and authorization are not implemented.
* Multi-player functionality is not implemented.

---

Run the "start" script to start the server and application.

To play the game, browse to: http://\<server IP address>:8000/

It's fun for a minute and you won't beat the computer :-)

---

The app runs with Python 3.10 or later and the following Python packages installed:

pip install fastapi

pip install "uvicorn[standard]"

pip install python-multipart

