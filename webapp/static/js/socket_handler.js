$(document).ready(function(){

    namespace = '/test';
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

    socket.on('my_response', function(msg) {
        console.log("my_respone");
        $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
    });

    socket.on('push_book', function(msg) {
        for(i=0; i < msg.data.length; i++){
            console.log(msg.data[i].bidPrice);
            $('#log').html(msg.data[i].bidPrice);
        }
    });

    $('form#emit').submit(function(event) {
        socket.emit('my event', {data: $('#emit_data').val()});
        return false;
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
        return false;
    });
});