document.addEventListener('DOMContentLoaded', function() {
	
	// Toggle the like button and update the database without reloading
	like = document.querySelectorAll(".liked");
	like.forEach(element => {
		element.addEventListener("click", () => {

			id = element.getAttribute("data-id");
			is_liked = element.getAttribute("data-is_liked");
			icon = document.querySelector(`#post-like-${id}`);
			counter = document.querySelector(`#like-counter-${id}`);

			form = new FormData();
			form.append("id", id);
			form.append("is_liked", is_liked);

			fetch("/like_post/", {
				method: "POST",
				body: form,
			})
			.then((res) => res.json())
			.then((res) => {

				if (res.status == 201) {

					if (res.is_liked === "yes") {
						icon.src = "https://img.icons8.com/ios-filled/32/fa314a/hearts.png";
						element.setAttribute("data-is_liked", "yes");
					} else {
						icon.src = "https://img.icons8.com/windows/32/000000/like--v2.png";
						element.setAttribute("data-is_liked", "no");
					}

					counter.textContent = res.like_count;
				}
			})
		})
	})

	// Add comment without reloading
	comment = document.querySelectorAll(".comment")
	comment.forEach(element => {
		element.addEventListener("click", () => {

			// Gets the comment data
			id = element.getAttribute("data-id");
			comment = document.querySelector(`#post-comment-${id}`);
			counter = document.querySelector(`#comment-counter-${id}`);

			// Checks if the input is not null
			if (comment.value === '') {
				return false;
			}

			// Creates a form to be posted to the API
			form = new FormData();
			form.append("id", id);
			form.append("comment", comment.value);

			fetch("/add_comment/", {
				method: "POST",
				body: form,
			})
			.then((res) => res.json())
			.then((res) => {
				if (res.status == 201) {
					// Update the comment counter
					counter.textContent = res.comment_count;
					
					// Show the new comment
					recent_comment = document.querySelector("#recent_comment");
					b = document.createElement("b");
					span = document.createElement("span");
					span.classList.add("gray")

					b.textContent =  res.commented_by;
					span.textContent = comment.value;

					recent_comment.appendChild(b)
					recent_comment.appendChild(span)

					// Clear the input value
					comment.value = '';
				}
			})
		})
	})

	// Reset Bootstrap modal on close
	$(".modal").on("hidden.bs.modal", function(){
		$(".modal-body").html("");
	});

	view = document.querySelectorAll("#view-comments");
	view.forEach(element => {
		element.addEventListener("click", () => {

			// Gets the post id
			post_id = element.getAttribute("data-id");

			// Fetch the comments of the post
			fetch(`/comments/${post_id}`)
			.then(res => res.json())
			.then(res => {

				// Appoints the number of comments in the Modal title
				document.querySelector("#exampleModalLongTitle").textContent = `${res.comments.length} Comments`;

				res.comments.forEach(comment => {
					
					modal_body = document.querySelector(".modal-body")

					b = document.createElement("b");
					span = document.createElement("span");
					br = document.createElement("br");
					span.classList.add("gray")
					console.log(comment)
					b.textContent = comment.commented_by__username + " ";
					span.textContent = comment.comment;

					modal_body.appendChild(b);
					modal_body.appendChild(span);
					modal_body.appendChild(br);

				})
			})
		})
	})
})