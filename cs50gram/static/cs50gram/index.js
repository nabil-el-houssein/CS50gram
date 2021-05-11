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
})