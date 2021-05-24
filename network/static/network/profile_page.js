document.addEventListener('DOMContentLoaded', function() {

    follow_button = document.querySelector("#follow_button")

    follow_button.addEventListener('click', function() {

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        const csrftoken = getCookie('csrftoken');

        follow_status = follow_button.innerHTML
        followed_user_id = follow_button.dataset.followingUser
        following_user_id = follow_button.dataset.followedUser
        following_count = parseInt(document.querySelector('#follower_count').innerHTML)
    
        fetch('follow_button', {
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', 
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'follow_status': follow_status,
                'followed_user_id': followed_user_id, 
                'following_user_id': following_user_id
            }),
        })
        .then(response => response.json())
        .then(data => {
            follow_button.innerHTML = data.follow_status;
            if (follow_status == "follow") {
                document.querySelector('#follower_count').innerHTML = (following_count + 1)
            } else {
                document.querySelector('#follower_count').innerHTML = (following_count - 1)
            }
        })
    })


});