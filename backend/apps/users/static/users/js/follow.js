
const data = document.currentScript.dataset;

document.getElementById("btn-follow").addEventListener("click", () => {
    var xhr = new XMLHttpRequest();
    
    xhr.open("POST", data.url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", data.token);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById("btn-follow").classList.toggle("hidden");
            document.getElementById("btn-unfollow").classList.toggle("hidden")
        }
    };

    xhr.send(JSON.stringify({
        "profile_id": data.profile
    }));
})

document.getElementById("btn-unfollow").addEventListener("click", () => {
    var xhr = new XMLHttpRequest();

    xhr.open("POST", data.url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", data.token);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById("btn-unfollow").classList.toggle("hidden");
            document.getElementById("btn-follow").classList.toggle("hidden")
        }
    };

    xhr.send(JSON.stringify({
        "profile_id": data.profile
    }));
})


