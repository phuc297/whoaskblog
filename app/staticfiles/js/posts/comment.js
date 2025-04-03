$(document).ready(function () {
  const scriptTag = document.getElementById("comment-script");
  const data = scriptTag.dataset;
  $('#btn-submit-comment').on("click", function () {
    const txtComment = $('#comment-content').val();
    if (!txtComment.trim()) {
      alert("Comment content cannot be empty!");
      return;
    }
    $.ajax({
      type: 'GET',
      url: data.url,
      data: {
        csrfmiddlewaretoken: data.token,
        post_id: data.post_id,
        user_id: data.user_id,
        comment_content: txtComment,
      },
      success: function (data) {
        const newComment = `
                    <div class="flex mb-6">
                      <img class="w-14 h-14 rounded-full mr-4" src="${data.avatar}" alt="Avatar of User"/>
                      <div class="flex-1">
                        <p class="text-green-600 font-normal">${data.username}</p>
                        <p class="text-gray-600 text-sm mb-2">Posted on ${data.created_at}</p>
                        <p class="text-gray-800">${data.content}</p>
                      </div>
                    </div>
                    `;
        $('#comments-section').prepend(newComment);
        $('#comment-content').val('');

      },
      error: function (xhr, status, error) {
        console.error("Error posting comment:", error);
        alert("Failed to post comment. Please try again.");
      }
    });
  });
});