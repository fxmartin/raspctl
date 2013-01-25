%rebase base

<br />
<a class="btn" href="/command/edit/new" title="New element"> <i class="icon-plus-sign"></i> New command </a>
<br /> <br /> <br />


<table class="table table-hover">
	<thead>
		<tr>
			<th>Class</th>
			<th>Action</th>
			<th>Command</th>
			<th>Options</th>
		</tr>
	</thead>
	<tbody>

	% for row in rows:
		<tr>
			<td> {{row.class_}} </td>
			<td> {{row.action}} </td>
			<td> {{row.command}} </td>
			<td>
				<a class="btn launch" href="/execute?class={{row.class_}}&action={{row.action}}" title="Launch"><i class="icon-play"></i></a>
				<a class="btn" href="/command/edit/{{row.id}}" title="Edit"><i class="icon-wrench"></i></a>
				<a class="btn remove" href="/command/delete/{{row.id}}" title="Remove"><i class="icon-remove"></i></a>
			</td>
		</tr>
	% end
	</tbody>
</table>

<script type="text/javascript">
	$(document).ready(function(){

		delete_line = function(event) {
			// Because you can click on the <i> element too
			var url = event.target.href || $(event.target).closest('a')[0].href
			$(event.target).parents('tr').remove();
			// AJAX Call to the deletion method
			$.ajax({"url": url});
		}

		$('a.launch').bind('click', function(event){
			event.preventDefault();
			$.get(this.href, {}, function(response) {
				console.log(response);
			})
		})

		$('a.remove').bind('click', function(event) {
			event.preventDefault();
			// If you press CTROL+Delete item, it will be deleted without confirmation
			if (event.ctrlKey) { delete_line(event); return; }
			if (Math.random()*10 >= 5) {
				var yes = "Yes, I want to delete it";
				var no = "No, I don't want to delete it";
			} else {
				var yes = "Hell yes!";
				var no = "Nooop!";
			}
			bootbox.dialog("Do you really want to delete this element?", [
			{
				"label" : no,
				"callback": function() {}
			}, {
				"label" : yes,
				"class" : "btn-danger",
				"callback": function() {
					delete_line(event);
				}
			}]);
		});
	});
</script>
