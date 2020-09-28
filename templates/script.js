function send_command(id_device, command_name) {
    var xhr = new XMLHttpRequest();
    var message = create_notification(command_name);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            message_text = "<h5 class='alert-heading'>" + command_name + "</h5>";
            message.classList.remove("alert-info");
            if (xhr.status === 200) {
                message.classList.add("alert-success");
                message_text += "<strong>Status:</strong> ОК";
                message.innerHTML = message_text;
            } else {
                message.classList.add("alert-danger");
                message_text += "<strong>Status:</strong> Connection ERROR";
                message.innerHTML = message_text;
            }
            setTimeout(function () {
                message.classList.add("message_out");
            }, 3000);
        }
    };
    xhr.open("POST", "/command", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        id: id_device,
        command: command_name
    }));
};

function create_notification(command_name) {
    var notification = document.getElementById("notification");
    const message = document.createElement("div");
    message.className = "alert alert-info animate_background message_in";
    message_text = "<h5 class='alert-heading'>" + command_name + "</h5>";
    message_text += "<strong>Status:</strong> Sending...";
    message.innerHTML = message_text;
    notification.insertBefore(message, notification.firstChild);
    message.addEventListener('animationend', function (event) {
        if (event.animationName == "slideout") {
            message.remove();
        }
    });
    return message;
};