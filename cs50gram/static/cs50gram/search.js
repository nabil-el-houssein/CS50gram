document.addEventListener('DOMContentLoaded', function() {

	// Hide the search results box when clicked outside the box
	document.addEventListener('click', function(e) {
		var search_results = document.querySelector("#search-results");

		if (!search_results.contains(e.target)) {
			search_results.style.display = "none";
		}

	})


	document.querySelector("#search").addEventListener('input', function() {

		var search_results = document.querySelector("#search-results");

		search_results.textContent = '';

		if (this.value === '') {
			search_results.style.display = "none";
		}
		
		fetch(`/search/${this.value.trim()}`)
		.then(res => res.json())
		.then(res => {
			
			search_results.style.display = "block";

			if (res.error) {
				search_results.innerText = res.error;
			} else if (res.response) {

				res.response.forEach(single_res => {

					div = document.createElement("div");
					a = document.createElement("a");
					b = document.createElement("b");
					p = document.createElement("p")
					br = document.createElement("br");

					b.textContent = single_res.username;
					p.textContent = `${single_res.first_name} ${single_res.last_name}`;

					div.appendChild(b);
					div.appendChild(p);

					a.classList.add("single-res");

					a.appendChild(div);

					// Add link to each response
					a.href = `/profile/${single_res.username}`;

					search_results.appendChild(a);
				})
			}

		})
	})
})