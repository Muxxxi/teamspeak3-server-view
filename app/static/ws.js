var wsProtocol = 'ws://';
if (window.location.protocol === 'https:') {
    wsProtocol = 'wss://';
}
const socket = new WebSocket(wsProtocol + location.host + location.pathname + 'ws');
socket.addEventListener('message', ev => {
  var users = JSON.parse(ev.data)
  if (users.length > 0){
    var listUsers = users.map((user) => {
      return `
        <div class="row align-items-center mb-1">
          <div class="col-sm-auto pr-0">
            <img width="30" height="30" src=${document.getElementsByName('pic')[0].content}/>
          </div>
          <div class="col-sm pl-3">
            <h2 class="mb-0" >${user}</h2>
          </div>
        </div>
        `
    });
    document.getElementById('list').innerHTML = listUsers.join("");
  } else {
    document.getElementById('list').innerHTML = "";
  }
});
