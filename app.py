from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

socketio = SocketIO(app, cors_allowed_origins="*")

app_name = os.getenv("APP_NAME")
env = os.getenv("ENV")

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>""" + str(app_name) + ':' + str(env) + """</title>

<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:Segoe UI,sans-serif;
}

body{
    background:#0f172a;
    height:100vh;
}

#joinScreen{
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
}

.join-card{
    width:400px;
    padding:30px;
    background:#1e293b;
    border-radius:20px;
    box-shadow:0 20px 60px rgba(0,0,0,.4);
}

.join-card h1{
    color:white;
    text-align:center;
    margin-bottom:20px;
}

input{
    width:100%;
    padding:14px;
    margin-top:10px;
    border:none;
    border-radius:12px;
    background:#334155;
    color:white;
}

button{
    width:100%;
    margin-top:15px;
    padding:14px;
    border:none;
    border-radius:12px;
    background:#2563eb;
    color:white;
    cursor:pointer;
}

button:hover{
    background:#1d4ed8;
}

#chatScreen{
    display:none;
    height:100vh;
    flex-direction:column;
}

.header{
    height:70px;
    background:#1e293b;
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:20px;
    font-weight:bold;
}

.messages{
    flex:1;
    overflow-y:auto;
    padding:20px;
}

.msg{
    display:flex;
    margin-bottom:15px;
}

.left{
    justify-content:flex-start;
}

.right{
    justify-content:flex-end;
}

.bubble{
    max-width:70%;
    padding:12px 18px;
    border-radius:18px;
    word-wrap:break-word;
}

.left .bubble{
    background:#334155;
    color:white;
}

.right .bubble{
    background:#2563eb;
    color:white;
}

.name{
    font-size:12px;
    opacity:.7;
    margin-bottom:4px;
}

.input-area{
    display:flex;
    gap:10px;
    padding:15px;
    background:#1e293b;
}

.input-area input{
    margin:0;
}

</style>
</head>

<body>

<div id="joinScreen">

    <div class="join-card">
        <h1>Join v2 Chat Room</h1>

        <input id="username" placeholder="Your Name">
        <input id="room" placeholder="Room Name">

        <button onclick="joinChat()">
            Join
        </button>
    </div>

</div>

<div id="chatScreen">

    <div class="header" id="roomTitle"></div>

    <div class="messages" id="messages"></div>

    <div class="input-area">
        <input id="messageInput"
               placeholder="Type message..."
               onkeypress="enter(event)">
        <button onclick="sendMessage()">Send</button>
    </div>

</div>

<script>

const socket = io();

let username="";
let room="";

function joinChat(){

    username=document.getElementById("username").value.trim();
    room=document.getElementById("room").value.trim();

    if(!username || !room){
        alert("Fill everything");
        return;
    }

    socket.emit("join",{
        username:username,
        room:room
    });

    document.getElementById("joinScreen").style.display="none";

    document.getElementById("chatScreen").style.display="flex";

    document.getElementById("roomTitle").innerText=
        "Room: " + room;
}

function sendMessage(){

    let input=document.getElementById("messageInput");

    let msg=input.value.trim();

    if(!msg) return;

    socket.emit("message",{
        username:username,
        room:room,
        message:msg
    });

    input.value="";
}

function enter(e){
    if(e.key==="Enter"){
        sendMessage();
    }
}

socket.on("message",data=>{

    let box=document.getElementById("messages");

    let side=
        data.username===username
        ? "right"
        : "left";

    box.innerHTML+=`
        <div class="msg ${side}">
            <div class="bubble">
                <div class="name">
                    ${data.username}
                </div>
                ${data.message}
            </div>
        </div>
    `;

    box.scrollTop=box.scrollHeight;
});

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@socketio.on("join")
def handle_join(data):

    room = data["room"]
    username = data["username"]

    join_room(room)

    emit(
        "message",
        {
            "username":"System",
            "message":f"{username} joined the room"
        },
        room=room
    )

@socketio.on("message")
def handle_message(data):

    emit(
        "message",
        {
            "username":data["username"],
            "message":data["message"],
            "time":datetime.now().strftime("%H:%M")
        },
        room=data["room"]
    )

# @app.route("/cpu")
# def cpu():
#     import time
#     total = 0
#     for i in range (5_00_000):
#         total += i
#         time.sleep(1)

#     return str(total)

if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True
    )