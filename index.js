document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "192.168.0.103";   // the IP address of your Raspberry PI
var trigger = "triggerOff";

function client(){
    
    const net = require('net');
    var input = document.getElementById("message").value;

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
    });
    
    // get the data from the server
    client.on('data', (data) => {
        document.getElementById("message").innerHTML = data;
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
        trigger="triggerOff"
    });


}

function setTrigger(){
    console.log(trigger)
    if (trigger=="triggerOff") {
        trigger="triggerOn";
        send_data(trigger);
    }
    else {
        trigger="triggerOff";
        send_data(trigger);
        document.getElementById("Obstacle").innerHTML = "Detection Off";
        document.getElementById("Obstacle").style.color = "grey";
    }
    console.log(trigger)
}



// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        send_data("87");
        
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        send_data("83");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        send_data("65");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        send_data("68");
    }
    else if (e.keyCode == '32') {
        send_data("32")
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}

function send_data(e) {
    const net = require('net');
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${e}\r\n`);
    })
    client.on('data', (data) => {
        values=data.toString().split('|');
        console.log(values);
        document.getElementById("action").innerHTML = values[0];
        document.getElementById("power").innerHTML = values[2];
        document.getElementById("temperature").innerHTML = values[3];
        var Obstacle=values[1];
        if (Obstacle=="No Obstacle"&&trigger=="triggerOn"){
            document.getElementById("Obstacle").innerHTML = values[1];
            document.getElementById("Obstacle").style.color = "green";
        }
        else if (Obstacle=="Obstacle"&&trigger=="triggerOn"){
            document.getElementById("Obstacle").innerHTML = values[1];
            document.getElementById("Obstacle").style.color = "red";
        }
        else 
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}

function speed_up(){
    send_data("Up")
}

function slow_down(){
    send_data("Down")
}


// update data for every 50ms
function update_data(){
        // get image from python server
        client();
}
