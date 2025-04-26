

document.querySelectorAll(".btn-follow").forEach(button => {
    button.addEventListener("click", () => {
        handleFollow(button);
    });
});

document.querySelectorAll(".btn-unfollow").forEach(button => {
    button.addEventListener("click", () => {
        handleUnfollow(button);
    });
});

function handleFollow(button) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", button.dataset.url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", window.csrfToken);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            button.classList.add("hidden");
            button.previousElementSibling.classList.remove("hidden")
        }
        else {
            console.log("Error:", "Error when follow profile");
        }
    };
    xhr.send(JSON.stringify({
        "user_profile_id": button.dataset.user,
        "profile_id": button.dataset.profile
    }));
}

function handleUnfollow(button) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", button.dataset.url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", window.csrfToken);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            button.classList.add("hidden");
            button.nextElementSibling.classList.remove("hidden")
        }
        else {
            console.log("Error:", "Error when unfollow profile");
        }
    };
    xhr.send(JSON.stringify({
        "user_profile_id": button.dataset.user,
        "profile_id": button.dataset.profile
    }));
}