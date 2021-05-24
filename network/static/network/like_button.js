document.addEventListener('DOMContentLoaded', function() {

    like_button = document.querySelectorAll(".like-button").forEach(button => {

        button.addEventListener('click', event => {

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

            like_status = button.innerHTML
            post_id = button.id
            like_count = parseInt(document.querySelector(`#count${post_id}`).innerHTML)
        
            fetch('like_button', {
                method: 'POST',
                credentials: 'same-origin',
                headers:{
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest', 
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'like_status': like_status,
                    'post_id': post_id 
                }),
            })
            .then(response => response.json())
            .then(data => {
                button.innerHTML = data.like_status;
                if (like_status == "like") {
                    document.querySelector(`#count${post_id}`).innerHTML = (like_count + 1)
                } else {
                    document.querySelector(`#count${post_id}`).innerHTML = (like_count - 1)
                }
            })
        })
    })
});