%rebase base

<h3 class="text-info">Configuration</h3>
<hr />

<form action="/save_configuration" class="form-horizontal" method="post">
	<h4>Help/Debug Information</h4>
	<div class="control-group">
		<label class="control-label" for="SHOW_DETAILED_INFO">Show detailed information</label>
		<div class="controls">
			<select name="SHOW_DETAILED_INFO">
				<option value="True" {{"selected" if config.SHOW_DETAILED_INFO else ""}}>Enabled</option>
				<option value="False" {{"selected" if not config.SHOW_DETAILED_INFO else ""}}>Disabled</option>
			
			</select>
			<abbr title="Shows/hidde information of how to use the web application">Help</abbr>
		</div>
	</div>

	<div class="control-group">
		<label class="control-label" for="SHOW_DETAILED_INFO">Show TODO's</label>
		<div class="controls">
			<select name="SHOW_TODO">
				<option value="True" {{"selected" if config.SHOW_TODO else ""}}>Enabled</option>
				<option value="False" {{"selected" if not config.SHOW_TODO else ""}}>Disabled</option>
			
			</select>
			<abbr title="Shows/hidde information of the things that are not finished and are tagged as TODO">Help</abbr>
		</div>
	</div>

	<div class="control-group">
		<label class="control-label" for="COMMAND_EXECUTION">Commands execution</label>
		<div class="controls">
			<select name="COMMAND_EXECUTION">
				<option value="True" {{"selected" if config.COMMAND_EXECUTION else ""}}>Enabled</option>
				<option value="False" {{"selected" if not config.COMMAND_EXECUTION else ""}}>Disabled</option>
			
			</select>
			<span class="text-error">Use it with care!</span>
			<abbr title="Enables/Disables the execution of commands from the Web Interface or the HTTP API. Any command can be configured/executed. Be sure that only authorised personal can edit/execute commands.">Help</abbr>
		</div>
	</div>

	<div class="form-actions">
		<button type="submit" class="btn btn-primary">Save changes</button>
	</div>

	<hr />
</form>
