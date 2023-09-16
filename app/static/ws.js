var wsProtocol = 'ws://';
if (window.location.protocol === 'https:') {
    wsProtocol = 'wss://';
}
let socket = null;

function connectWebSocket() {
    socket = new WebSocket(wsProtocol + location.host + location.pathname + 'ws');

    // Connection opened
    socket.addEventListener('open', (event) => {
        document.getElementById('connectionStatus').textContent = "Connected";
        document.getElementById('connectionStatus').style.color = "green";
    });

    // Listen for messages
    socket.addEventListener('message', ev => {
        var users = JSON.parse(ev.data);
        if (users.length > 0){
            var listUsers = users.map((user) => {
                return `
                <div class="row align-items-center mb-1">
                    <div class="col-auto pr-0">
                        <img width="30" height="30" src=${document.getElementsByName('pic')[0].content}/>
                    </div>
                    <div class="col pl-3">
                        <h3 class="mb-0">${user}</h3>
                    </div>
                </div>
                `;
            });
            document.getElementById('list').innerHTML = listUsers.join("");
        } else {
            document.getElementById('list').innerHTML = "";
        }
    });

    // Connection closed
    socket.addEventListener('close', (event) => {
        document.getElementById('connectionStatus').textContent = "Disconnected";
        document.getElementById('connectionStatus').style.color = "red";

        // Attempt to reconnect after a delay (e.g., 3 seconds)
        setTimeout(connectWebSocket, 3000);
    });

    // Connection error
    socket.addEventListener('error', (event) => {
        document.getElementById('connectionStatus').textContent = "Error";
        document.getElementById('connectionStatus').style.color = "red";
    });
}

// Start the initial connection
connectWebSocket();
