%rebase base

% import config



<p> <i>Commands</i> section is used when you want to define some commands that will be executed on the Raspberry Pi. The commands can be executed either from the web interface or using a HTTP API. </p>

% if config.SHOW_DETAILED_INFO:

	<p class="text-error"> Be very careful when using this tool because ANY command can be executed, even "rm -rf /". The UID (User ID) of the one who is running the web application will be used. It is strongly recommended to NOT use root user for obvious reasons. Take care.  </p>

	<p>Let's explain each item:</p>
	<ul>
		<li>Class: Used for defining a generic name. Same as Category. Just for being able to group all the commands by the same subject or type.</li>
		<li>Action: Just a descriptive name of the action this command will perform. Only letters, numbers and the '_' character can be used (because it must be URL friendly in order to be used in the HTTP API)</li>
		<li>Command: The command itself. This command will be executed in the shell. The command can receive parameters too (not true, is in my TODO list)</li>
	</ul>

	<p> The URL API is very easy to use. You just have to do a request to: </p>

	<p> http://your-rasperry-ip<b>/execute?class=CLASS&amp;action=ACTION&amp;param1=FOO</b> </p>

	<p> Where CLASS and ACTION are required fields and will be used for searching the command, if any match is found, the command will be executed passing the given parameters </p>


% end
% if config.SHOW_TODO:
	<p> <b class="text-error">TODO</b>: Support a way of enabling/disabling the commands section thru a configuration file or something like that. </p>
% end


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
