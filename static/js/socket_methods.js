const socket = io.connect('http://' + document.domain + ':' + location.port);

function showLoginPage() {
    return socket.emit('login');
}