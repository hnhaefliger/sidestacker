const game = JSON.parse(document.getElementById('game').textContent);

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


function nextMove(game, color) {
    if (game.length > 0) {
        addToken(game.substring(0, 2), color);

        if (color === 'white') {
            color = 'black';
        } else {
            color = 'white';
        }

        window.setTimeout(function () {
            nextMove(game.substring(2), color)
        }, 1000);
    }
}

if (game !== 'invalid') {
    nextMove(game, 'white');

} else {
    showMessage('Invalid game id.')

    message_button.addEventListener('click', (e) => {
        e.preventDefault();
        document.location.href = 'http://localhost:8000/';
    })
}
