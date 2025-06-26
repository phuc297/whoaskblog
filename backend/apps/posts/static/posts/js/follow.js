data = document.currentScript.dataset;

document.querySelectorAll("#btn-follow").forEach(e => e.addEventListener("click", () => {

    var xhr = new XMLHttpRequest();

    xhr.open("POST", data.url, true);

    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.setRequestHeader("X-CSRFToken", window.csrfToken);

    xhr.onreadystatechange = function () {

        if (xhr.readyState === 4 && xhr.status === 200) {

            document.querySelectorAll("#btn-follow").forEach(e => e.classList.toggle("hidden"));

            document.querySelectorAll("#btn-unfollow").forEach(e => e.classList.toggle("hidden"));

        }

    };

    xhr.send(JSON.stringify({

        "user_profile_id": data.user,

        "profile_id": data.profile

    }));
}))

document.querySelectorAll("#btn-unfollow").forEach(e => e.addEventListener("click", () => {

    var xhr = new XMLHttpRequest();

    xhr.open("POST", data.url, true);

    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.setRequestHeader("X-CSRFToken", window.csrfToken);

    xhr.onreadystatechange = function () {

        if (xhr.readyState === 4 && xhr.status === 200) {

            document.querySelectorAll("#btn-follow").forEach(e => e.classList.toggle("hidden"));

            document.querySelectorAll("#btn-unfollow").forEach(e => e.classList.toggle("hidden"));

        }

    };

    xhr.send(JSON.stringify({

        "user_profile_id": data.user,

        "profile_id": data.profile

    }));

}))
