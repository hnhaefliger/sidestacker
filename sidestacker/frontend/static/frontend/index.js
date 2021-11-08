create_button = document.getElementById('create-btn');
game_id = document.getElementById('game-id');
join_button = document.getElementById('join-btn');

create_button.addEventListener('click', (e) => {
    document.location.href = 'http://localhost:8000/game';
});

join_button.addEventListener('click', (e) => {
    document.location.href = 'http://localhost:8000/game/' + game_id.value;
});