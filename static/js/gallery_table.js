function loadTable() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var json = JSON.parse(this.responseText);
            var table = document.getElementById("usertable");
            // Clear table
            table.innerHTML = "";

            // Setup title row
            row = table.insertRow(0);
            row.insertCell(-1).innerHTML = "<b>Name</b>";
            row.insertCell(-1).innerHTML = "<b>Cookie UUID</b>";
            row.insertCell(-1).innerHTML = "<b>Last Upload Time</b>";
            row.insertCell(-1).innerHTML = "<b>Points</b>";
            row.insertCell(-1).innerHTML = "<b>Photos</b>";

            // Add rows
            for (x=0;x<Object.keys(json.users).length;x++) {
                user = Object.keys(json.users)[x];
                var d = new Date(json.users[user].lastUploadTime);
                row = table.insertRow(-1);
                var nameString = "";
                for (y=0;y<json.users[user].names.length;y++) {
                    if (nameString != "") {
                        nameString += ", ";
                    }
                    nameString += json.users[user].names[y];
                }
                row.insertCell(-1).innerHTML = nameString;
                row.insertCell(-1).innerHTML = user;
                row.insertCell(-1).innerHTML = d.toLocaleDateString() + " " + d.toLocaleTimeString()
                row.insertCell(-1).innerHTML = json.users[user].points;
                row.insertCell(-1).innerHTML = '<a href="/user/' + user + '">' + Object.keys(json.users[user].photos).length + '</a>'
                /*
                var node = document.createElement("a");
                node.href = '/user/' + user + '/view'
                node.innerHTML = Object.keys(json.users[user].photos).length;
                row.insertCell(-1).append(node);
                */
            }
        }
    }
    xhttp.open("GET", "/json", true);
    xhttp.send();
}
loadTable();
setInterval(function(){loadTable()}, 5000);