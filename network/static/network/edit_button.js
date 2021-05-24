document.addEventListener('DOMContentLoaded', function() {

    // edit buttons

    edit_button = document.querySelectorAll(".edit-button").forEach(button => {

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

            post_id = button.dataset.post;

            console.log("Found post of: ");
            console.log(post_id);
        
            fetch('edit_button', {
                method: 'POST',
                credentials: 'same-origin',
                headers:{
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest', 
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'post_id': post_id,
                }),
            })
            .then(response => response.json())
            .then(data => {

                console.log("Fetch request complete.");
                console.log(`Returned ${data.content_to_edit}`);

                // prepare the content to be edited
                const text_box = document.createElement('textarea');
                text_box.innerHTML = data.content_to_edit;
                text_box.autofocus = true;
                text_box.id = `text_box${post_id}`;
                text_box.type = "text";
                text_box.classList.add("form-control");
                text_box.classList.add("w-20");
                text_box.classList.add("p-3");
                text_box.style.display = "block";
                text_box.style.whiteSpace = "pre-wrap"; 
                text_box.style.height = "120px";

                // append this after `time${post_id}`
                const time = document.querySelector(`#time${post_id}`);
                time.insertAdjacentElement('afterend', text_box);
                
                // also hide `content${post_id}`
                document.querySelector(`#content${post_id}`).style.display = "none";

                // show and hide buttons
                document.querySelector(`#save${post_id}`).classList.remove("d-none");
                document.querySelector(`#cancel${post_id}`).classList.remove("d-none");
                document.querySelector(`#delete${post_id}`).classList.remove("d-none");
                document.querySelector(`#edit${post_id}`).classList.add("d-none");
            })
        })
    })

    // cancel buttons
    
    cancel_button = document.querySelectorAll(".cancel-button").forEach(button => {

        button.addEventListener('click', event => {

            post_id = button.dataset.post;
            
            // Remove the text box
            document.querySelector(`#text_box${post_id}`).remove();
            document.querySelector(`#content${post_id}`).style.display = "block";

            // show and hide buttons
            document.querySelector(`#save${post_id}`).classList.add("d-none");
            document.querySelector(`#cancel${post_id}`).classList.add("d-none");
            document.querySelector(`#delete${post_id}`).classList.add("d-none");
            document.querySelector(`#edit${post_id}`).classList.remove("d-none");
            
        })
    })

    // delete buttons

    delete_button = document.querySelectorAll(".delete-button").forEach(button => {

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

            post_id = button.dataset.post;

            console.log("Found post of: ");
            console.log(post_id);
        
            fetch('delete_button', {
                method: 'POST',
                credentials: 'same-origin',
                headers:{
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest', 
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'post_id': post_id,
                }),
            })
            .then(response => response.json())
            .then(data => {

                // delete the html element for the container of the post
                document.querySelector(`#container${post_id}`).remove();
            })
        })
    })

    // save buttons
    
    save_button = document.querySelectorAll(".save-button").forEach(button => {

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

            post_id = button.dataset.post;
            updated_content = document.querySelector(`#text_box${post_id}`).value;

            console.log("Found content to post as: ")
            console.log(updated_content)
            console.log("Found post of: ");
            console.log(post_id);
        
            fetch('save_button', {
                method: 'POST',
                credentials: 'same-origin',
                headers:{
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest', 
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'post_id': post_id,
                    'updated_content': updated_content,
                }),
            })
            .then(response => response.json())
            .then(data => {

                // Remove the text box
                document.querySelector(`#text_box${post_id}`).remove();
                document.querySelector(`#content${post_id}`).innerHTML = updated_content;
                document.querySelector(`#content${post_id}`).style.display = "block";

                // show and hide buttons
                document.querySelector(`#save${post_id}`).classList.add("d-none");
                document.querySelector(`#cancel${post_id}`).classList.add("d-none");
                document.querySelector(`#delete${post_id}`).classList.add("d-none");
                document.querySelector(`#edit${post_id}`).classList.remove("d-none");

            })
        })
    })
});