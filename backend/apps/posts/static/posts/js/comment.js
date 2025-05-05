
document.getElementById('btn-submit-comment').addEventListener('click', async () => {

    const commentContent = document.getElementById('text-comment').value
    if (!commentContent.trim()) {
        alert("Comment content cannot be empty!");
        return;
    }

    const script = document.getElementById('comment-script');
    const data = script.dataset;

    const response = await fetch(data.url, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": window.csrfToken
        },
        body: JSON.stringify({
            post_id: data.post_id,
            content: commentContent
        })
    });

    if (response.redirected) {
        const redirectUrl = response.url;
        if (redirectUrl.includes('/login/')) {
            alert("You need to be logged in to comment. Redirecting to login...");
            window.location.href = redirectUrl;
            return;
        }
    }

    const contentType = response.headers.get("Content-Type");

    if (!response.ok) {
        const errorText = await response.text();
        console.error("Error response: ", errorText);
        alert("An error occurred: " + errorText);
        return;
    }

    if (!contentType || !contentType.includes("application/json")) {
        console.error("Expected JSON, but received: ", response);
        alert("Unexpected response format. Please try again.");
        return;
    }

    const result = await response.json();

    if (result.success) {
        const newComment = `
                    <div class="flex mb-6">
                      <img class="w-14 h-14 rounded-full mr-4" src="${result.avatar}" alt="Avatar of User"/>
                      <div class="flex-1">
                        <p class="text-green-600 font-normal">${result.username}</p>
                        <p class="text-gray-600 text-sm mb-2">Posted on ${result.created_at}</p>
                        <p class="text-gray-800">${result.content}</p>
                      </div>
                    </div>
                    `;

        document.getElementById('comments').insertAdjacentHTML('afterbegin', newComment)

        document.getElementById('text-comment').value = ""
    } else {
        console.error("Error: ", result.error);
    }


})

