create_button = document.getElementById('create-btn');
game_id = document.getElementById('game-id');
join_button = document.getElementById('join-btn');
replay_id = document.getElementById('replay-id');
replay_button = document.getElementById('replay-btn');

create_button.addEventListener('click', (e) => {
    e.preventDefault();
    document.location.href = 'http://localhost:8000/game';
});

join_button.addEventListener('click', (e) => {
    e.preventDefault();
    document.location.href = 'http://localhost:8000/game/' + game_id.value;
});

replay_button.addEventListener('click', (e) => {
    e.preventDefault();
    document.location.href = 'http://localhost:8000/replay/' + replay_id.value;
})