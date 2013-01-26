%rebase base

<h3 class="text-info"> Webcam </h3>
<hr />

<a id="take_picture" class="btn btn-primary offset3 span4" href="/take_picture">Take new picture</a>
<br /> <br />

<img id="picture" class="offset1" src="/static/img/webcam_last.jpg" width="640px" height="480px" onerror="imgError(this);" />

<br />

<hr />

<script type="text/javascript">

$(document).ready(function() {
	function imgError(image) {
	    image.onerror = "";
	    image.src = "/static/img/no_image.gif";
	    return true;
	}

	$('#take_picture').bind('click', function(event){
		event.preventDefault();
		// Launch the HTTP Request with ajax
		$.get(this.href, {}, function(response) {})
		setTimeout(function (){}, 3500); // Just wait 3.5 seconds
		d = new Date();
		// Reload the image without reloading the page (and avoiding cache problems)
		$("#picture").attr("src", "/static/img/webcam_last.jpg?" + d.getTime());
	});
});

</script>

