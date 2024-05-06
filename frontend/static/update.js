function loadPost(postId) {
  var baseUrl = document.getElementById("api-base-url-update").value;

  fetch(baseUrl + "/update/" + postId)
    .then((response) => response.json())
    .then((data) => {
      title = data.title;
      date = data.date;
      content = data.content;
      author = data.author;

      console.log(date);

      document.getElementById("update-title").value = title;
      document.getElementById("update-date").value = date;
      document.getElementById("update-content").value = content;
      document.getElementById("update-author").value = author;
    })
    .catch((error) => console.error("Error:", error));
}

function updatePost() {
  var baseUrl = document.getElementById("api-base-url-update").value;
  var title = document.getElementById("update-title").value;
  var postDate = document.getElementById("update-date").value;
  var content = document.getElementById("update-content").value;
  var author = document.getElementById("update-author").value;

  //Get post Id from the URL
  postId = window.location.pathname.split("/")[2];

  var updatedPost = {
    title: title,
    content: content,
    author: author,
    date: postDate,
  };

  fetch(baseUrl + "/posts/" + postId, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updatedPost),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to add post");
      }
      return response.json();
    })
    .then((post) => {
      console.log("Post updated:", post);
      // redirection
      window.location.href = "/";
    })
    .catch((error) => console.error("Error:", error));
}

window.onload = function () {
  post_id = window.location.pathname.split("/")[2];

  //get the post information
  loadPost(post_id);
};
