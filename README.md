This project was done to learn the use of rrweb for saving users session replay. 
Users session replay means that it record what user interacted with in your site from start to end store it in a json form.
It also uses websocket to implement live streaming of the sessions. 
For eg. If you want to look at what your user is interacting with you can live stream it.
You can also replay a saved session by choosing the session ID.




How to run?
1) Clone th git repository.
2) Install requirements : pip install fastapi uvicorn websockets
3) Run the server : uvicorn main:app --reload
4) Go to "http://127.0.0.1:8000/viewer" in a new tab.
5) Go to "http://127.0.0.1:8000/test" in another tab.When you close the page it will upload the session to recordings folder which can be viewed later.
6) Now the viewer page shows the ilve replay of whatever the changes occur in test page.
7) Go to "http://127.0.0.1:8000/player" to view all the recorded session. Select a session Id and replay the session
   
