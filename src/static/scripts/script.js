const form = document.getElementById('nerForm');
const input = document.getElementById('nerInput');

form.addEventListener('submit', handleInput);

function handleInput(e) {
    e.preventDefault();

    sentence = input.value.replace(/\s/g, "%20");

    document.location.href = `/query/${sentence}`;
}