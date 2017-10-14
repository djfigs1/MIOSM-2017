var prevPhotos = -1;

function loadUser() {
    var photoURL = "/photo/";
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var json = JSON.parse(this.responseText);
            var id = window.location.href.split("/")[window.location.href.split("/").length -1]
            var table = document.getElementById("photoTable");
            var photos = Object.keys(json.users[id].photos);


            // Only update the table if there are new photos.
            if (prevPhotos == 0) {
                prevPhotos = photos.length;
            }else{
                if (photos.length > prevPhotos || prevPhotos == -1) {
                    // Clear table
                    table.innerHTML = "";

                    // Setup title row
                    row = table.insertRow(0);
                    row.insertCell(-1).innerHTML = "<b>Image</b>";
                    row.insertCell(-1).innerHTML = "<b>Caption</b>";
                    row.insertCell(-1).innerHTML = "<b>Time</b>";
                    row.insertCell(-1).innerHTML = "<b>Extension</b>";
                    row.insertCell(-1).innerHTML = "<b>Approved?</b>";

                    for (x=0;x<photos.length;x++) {
                        var photoId = photos[x];
                        var d = new Date(json.users[id].photos[photoId].time);
                        var approved = json.users[id].photos[photoId].approved
                        row = table.insertRow(-1);
                        row.insertCell(-1).innerHTML = '<img src="' + photoURL + photoId + '"></img>'
                        row.insertCell(-1).innerHTML = json.users[id].photos[photoId].caption
                        row.insertCell(-1).innerHTML = d.toLocaleDateString() + " " + d.toLocaleTimeString()
                        row.insertCell(-1).innerHTML = json.users[id].photos[photoId].extension
                        if (approved == 0) {
                            row.insertCell(-1).innerHTML = "<button class='approve' onClick='approvePhoto(this, 1)' data-photoId='" + photoId + "'>Approve (1 Point)</button><button class='approve' onClick='approvePhoto(this, 2)' data-photoId='" + photoId + "'>Approve (2 Points)</button><button class='approve' onClick='approvePhoto(this, 3)' data-photoId='" + photoId + "'>Approve (3 Points)</button> <button class='deny' onClick='denyPhoto(this)' data-photoid='" + photoId + "'>Deny</button>"
                        } else {
                            if (approved == 1) {
                                row.insertCell(-1).innerHTML = "Approved"
                            } else {
                                row.insertCell(-1).innerHTML = "Denied"
                            }
                        }

                    }

                    prevPhotos = photos.length;
                }
            }
        }
    }
    xhttp.open("GET", "/json", true);
    xhttp.send();
}

function approvePhoto(button, points) {
    ga('send', 'event', 'Uploads', 'approve');
    var photo = button.dataset.photoid;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            givePoint(points)
        }
    }
    xhttp.open("GET", "/rate/" + photo + "/1", true)
    xhttp.send()
}

function denyPhoto(button) {
    ga('send', 'event', 'Uploads', 'deny');
    var photo = button.dataset.photoid;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            location.reload()
        }
    }
    xhttp.open("GET", "/rate/" + photo + "/2", true)
    xhttp.send()
}

function givePoint(points) {
    var xhttp = new XMLHttpRequest();
    var user = window.location.href.split("/")[window.location.href.split("/").length -1]
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            location.reload()
        }
    }

    xhttp.open("GET", "/points/" + user + "/" + points, true)
    xhttp.send()
}

function takePoint(points) {
    var xhttp = new XMLHttpRequest();
    var user = window.location.href.split("/")[window.location.href.split("/").length -1]
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            location.reload()
        }
    }
    xhttp.open("GET", "/points/" + user + "/" + -points, true)
    xhttp.send()
}
loadUser();
setInterval(function(){loadUser()}, 5000);