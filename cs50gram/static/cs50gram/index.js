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

	view = document.querySelectorAll(".show");
	view.forEach(element => {
		element.addEventListener("click", () => {

			// Gets the post id and the keyword
			post_id = element.getAttribute("data-id");
			keyword = element.getAttribute("data-keyword")

			// Fetch the comments|likes of the post based on the keyword
			fetch(`/post/${keyword}/${post_id}`)
			.then(res => res.json())
			.then(res => {

				// Appoints the number of comments in the Modal title
				document.querySelector("#exampleModalLongTitle").textContent = `${res.response.length} ${keyword}`;

				modal_body = document.querySelector(".modal-body")

				res.response.forEach(single_res => {

					b = document.createElement("b");
					span = document.createElement("span");
					br = document.createElement("br");
					span.classList.add("gray")
					
					if (res.keyword == "comments") {
						b.textContent = single_res.commented_by__username + " ";
						span.textContent = single_res.comment;
					} else if (res.keyword == "likes") {
						b.textContent = single_res.username;
					}

					modal_body.appendChild(b);
					modal_body.appendChild(span);
					modal_body.appendChild(br);

				})
			})
		})
	})

	// Delete a post without requiring reload of the entire page
	delete_btn = document.querySelectorAll(".delete");
	delete_btn.forEach(element => {
		element.addEventListener("click", () => {

			if (confirm("You are about to delete this post.\nThis action cannot be undone.")) {

				// Delete the post
				id = element.getAttribute("data-id");
				post = document.querySelector(`#post-${id}`);

				// Creates a form to be posted to the API
				form = new FormData();
				form.append("id", id);

				fetch("/delete/", {
					method: "POST",
					body: form,
				})
				.then(res => res.json())
				.then(res => {
					if (res.status == 201) {
						// Delete the post
						post.remove();
					}
				})

			} else {
				return false;
			}
			
		})
	})
})