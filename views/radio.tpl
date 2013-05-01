%rebase base


<p><a id ="add_new_radio"href="#new_radio"> <i class="icon-plus"></i> Add new radio </a> </p>

% if successfully_saved:
	<div class="alert alert-success">The radios as been saved!</div>
% end

<br /> <br />

<table class="hide">
<tr id="tmpl" class="hide">
	<td>
		<input type="text" name="name_UUIDNAME" value="" class="name" />
	</td>
	<td>
		<input type="text" name="stream_UUIDSTREAM" value="" class="stream" />
	</td>
	<td>
		<a class="btn launch" href="#" title="Start" id="foo">
			<i class="icon-play"></i>
		</a>
	</td>
	<td>
		<a class="btn launch" href="/radio/stop" title="Stop">
			<i class="icon-stop"></i>
		</a>
	</td>
</tr>
</table>

<form action="/radio/save" method="post">
	<table class="table">
		<tr>
			<th>Radio name</th>
			<th>Stream</th>
			<th>Play</th>
			<th>Stop</th>
		</tr>
		<tbody id="radios">
			% for i, (name, stream) in enumerate(radios, 0):
			<tr>
				<td>
					<input type="text" name="name_{{i}}" value="{{name}}" class="name" />
				</td>
				<td>
					<input type="text" name="stream_{{i}}" value="{{stream}}" class="stream" />
				</td>
				<td>
					<a class="btn launch" href="/radio/play?stream=" title="Start">
						<i class="icon-play"></i>
					</a>
				</td>
				<td>
					<a class="btn launch" href="/radio/stop?stream=" title="Stop">
						<i class="icon-stop"></i>
					</a>
				</td>
			</tr>
			% end

		</tbody>
	</table>

	<div class="form-actions">
		<button type="submit" class="btn btn-primary">Save changes</button>
	</div>

</form>

<script type="text/javascript">
	add_events = function() {
		$('#radios a').on('click', null, undefined, function(ev) {
			event.preventDefault();
			// I fucking love this ugly hacks =D
			var stream = $(ev.currentTarget).parents('tr').find('.stream')[0].value;
			var href = ev.currentTarget.href;
			$.get(href + stream, function() {});
		});
	};
	add_events();

	remove_events = function() {
		$('#radios a').off('click');
	};

	$('#add_new_radio').click(function(ev) {
		var random = Math.floor(Math.random() * Math.pow(10, 13));
		event.preventDefault();
		var tr = document.createElement('tr');
		var tmpl = $('#tmpl').html();
		tmpl = tmpl.replace('UUIDNAME', random);
		tmpl = tmpl.replace('UUIDSTREAM', random);
		$(tr).html(tmpl).appendTo($('#radios'));
		remove_events();
		add_events();
	});
</script>
