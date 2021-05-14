document.addEventListener('DOMContentLoaded', function() {

	// Toggle the follow/unfollow and update the database without reloading
	if (follow = document.querySelector(".follow")) {

		follow = document.querySelector(".follow");

		follow.onclick = function() {

			user = follow.getAttribute("data-id"); // User to be followed
			follower_counter = document.querySelector("#follower-counter");
			keyword = document.querySelector("#keyword");

			form = new FormData()
			form.append("user", user)
			form.append("keyword", keyword.innerText)

			fetch("/follow/", {
				method: "POST",
				body: form,
			})
			.then(res => res.json())
			.then(res => {

				follower_counter.textContent = res.followers;
				keyword.innerText = res.keyword;
			})
		}
	}

	// Show followers and followings in a modal
	btn = document.querySelectorAll(".followings");

	btn.forEach(element => {
		element.addEventListener("click", () => {

			user = element.getAttribute("data-id");
			keyword = element.getAttribute("data-keyword");

			fetch(`/user/${user}/${keyword}`)
			.then(res => res.json())
			.then(res => {

				modal_body = document.querySelector(".modal-body");

				document.querySelector(".modal-title").textContent = `${res.response_count} ${keyword}`;

				res.response.forEach(res => {

					b = document.createElement("b");
					br = document.createElement("br");

					b.textContent = res.username;

					modal_body.appendChild(b);
					modal_body.appendChild(br);
				})
				
			})

		})
	})
	
})