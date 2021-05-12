document.addEventListener('DOMContentLoaded', function() {

	// Show image preview before submitting
	document.getElementById("id_image").onchange = function () {
		var src = URL.createObjectURL(this.files[0]);
		document.getElementById("image-preview").src = src;
	}
})