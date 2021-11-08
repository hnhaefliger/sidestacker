const game_id = JSON.parse(document.getElementById('game-id').textContent);

console.log(game_id);

const ws = window.location.protocol == "https:" ? "wss://" : "ws://"
const socket = new WebSocket(ws + window.location.host + '/' + game_id + '/');

Array.from(document.getElementsByClassName('placer')).forEach((element) => {
    element.addEventListener('click', (e) => {
        var id = element.id.split('-')[1];
        var side = document.getElementById('side-' + id)

        if (id[0] == '0') {
            side.innerHTML += '<div class="token token-white"></div>';
        } else {
            side.innerHTML = '<div class="token token-white"></div>' + side.innerHTML;
        }

        socket.send(id);
    })
})

socket.onmessage = function(message) {
    console.log(message);
    var type = message.data.split('|')[0];
    var content = message.data.split('|')[1];

    if (type == 'move') {
        /* draw the move */
    };
};

socket.onerror = function(message) {
    console.log(message);
}

socket.ondisconnect = function(message) {
    console.log('disconnected');
}