// Function to create a new post element with delete and update buttons
function createPostElement(post) {
    const postDiv = document.createElement('div');
    postDiv.className = 'post';
    postDiv.innerHTML = `<h2>${post.title}</h2>
                        <p>${post.content}</p>
                        <p><strong>Author:</strong> ${post.author}</p>
                        <p><strong>Date:</strong> ${post.date}</p>
                        <div class="button-container">
                            <button class="delete-button" onclick="deletePost(${post.id})">Delete</button>
                        </div>`;
    return postDiv;
}


// Function to redirect to update page
function redirectToUpdatePage(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    fetch(baseUrl + '/update/' + postId, {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to redirect');
        }
        return response.json();
    })
    .then(data => {
    window.location.href = "http://127.0.0.1:5001/update.html"
    })
    .catch(error => console.error('Error:', error));
}


// Function to load posts and render them on the page
function loadPosts() {
    var baseUrl = document.getElementById('api-base-url').value;

    fetch(baseUrl + '/posts')
        .then(response => response.json())
        .then(data => {
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            data.forEach(post => {
                const postDiv = createPostElement(post);
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Function to add a new post
function addPost() {
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;
    var postAuthor = document.getElementById('post-author').value;
    var postDate = document.getElementById('post-date').value;

    var newPost = {
        title: postTitle,
        content: postContent,
        author: postAuthor,
        date: postDate
    };

    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPost)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to add post');
        }
        return response.json();
    })
    .then(post => {
        console.log('Post added:', post);
        loadPosts();
        document.getElementById('post-title').value = '';
        document.getElementById('post-content').value = '';
        document.getElementById('post-author').value = '';
        document.getElementById('post-date').value = '';
        showSuccessMessage('Post added successfully!');
    })
    .catch(error => console.error('Error:', error));
}

// Function to show a success message
function showSuccessMessage(message) {
    var successMessage = document.createElement('div');
    successMessage.textContent = message;
    successMessage.className = 'success-message';

    var container = document.querySelector('.container');
    var postContainer = document.getElementById('post-container');
    container.insertBefore(successMessage, postContainer);

    setTimeout(function() {
        successMessage.remove();
    }, 3000);
}

// Function to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete post');
        }
        return response.json();
    })
    .then(data => {
        console.log('Post deleted:', data);
        loadPosts();
    })
    .catch(error => console.error('Error:', error));
}

// Call the loadPosts function when the window is fully loaded
window.onload = function() {
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
};
