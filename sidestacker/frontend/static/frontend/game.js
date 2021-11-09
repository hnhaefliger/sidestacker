const game_id = JSON.parse(document.getElementById('game-id').textContent);

const ws = window.location.protocol == "https:" ? "wss://" : "ws://"
const socket = new WebSocket(ws + window.location.host + '/' + game_id + '/');

const message_box = document.getElementById('message');
const message_text = document.getElementById('message-text');
const message_button = document.getElementById('message-button');


function hideMessage() {
    message_box.classList.remove('shown');
    message_box.classList.add('hidden');
}


message_button.addEventListener('click', (e) => {
    e.preventDefault();
    hideMessage();
})


function showMessage(message, button=false) {
    message_text.innerHTML = message;

    if (button) {
        message_button.classList.remove('hidden');
    } else {
        message_button.classList.add('hidden');
    }

    message_box.classList.remove('hidden');
    message_box.classList.add('shown');
}


function addToken(id, color) {
    var side = document.getElementById('side-' + id)

    if (id[1] == '0') {
        side.innerHTML += `<div class="token token-${color}"></div>`;
    } else {
        side.innerHTML = `<div class="token token-${color}"></div>` + side.innerHTML;
    }
}


Array.from(document.getElementsByClassName('placer')).forEach((element) => {
    element.addEventListener('click', (e) => {
        var id = element.id.split('-')[1];

        socket.send(id);
    })
})


socket.onmessage = function(message) {
    var type = message.data.split('|')[0];
    var content = message.data.split('|')[1];

    if (type == 'move') {
        addToken(content.slice(0, 2), content.slice(2, content.length));

    } else {
        if (type == 'wait') {
            showMessage(`Waiting for a second player to join the game. Your game id is ${content}`, false);

        } else {
            if (type == 'start') {
                hideMessage();

            } else {
                if (type == 'win') {
                    socket.close();

                    showMessage(`${content} won the game!`, true);

                    message_button.addEventListener('click', (e) => {
                        e.preventDefault();
                        document.location.href = 'http://localhost:8000/';
                    })
                } else {
                    if (type == 'end') {
                        socket.close();

                        document.location.href = 'http://localhost:8000/';
                    }
                }
            }
        }
    }
};


socket.onerror = function(error) {
    console.log(error);
}


socket.ondisconnect = function(message) {
    document.location.href = 'http://localhost:8000/';
}