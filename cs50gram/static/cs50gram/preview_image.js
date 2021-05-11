document.addEventListener('DOMContentLoaded', function() {

	// Show image preview before submitting
	document.getElementById("id_image").onchange = function () {

		var reader = new FileReader();

		reader.onload = function (e) {
			// get loaded data and render thumbnail.
			document.getElementById("image-preview").src = e.target.result;
		};

		// read the image file as a data URL.
		reader.readAsDataURL(this.files[0]);
	}
})