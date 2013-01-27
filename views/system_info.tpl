<div class="span4">
	<h3 class="text-info"> Basic </h3>
	<dl class="dl-horizontal">
		<dt>User</dt>
		<dd>{{info['USER']}}</dd>
		<dt>Hostname</dt>
		<dd>{{info['HOSTNAME']}}</dd>
		<dt>IP address</dt>
		<dd>{{info['IP_ADDRESS']}}</dd>
		<dt>Uptime</dt>
		<dd>{{info['UPTIME']}}</dd>
	</dl>

	<hr />

	<h3 class="text-info"> Processor </h3>
	<dl>
		<dt>CPU Name</dt>
		<dd>{{info['PROCESSOR_NAME']}}</dd>
		<dt>Bogomits</dt>
		<dd>{{info['PROCESSOR_BOGOMITS']}}</dd>
		<dt>Current speed (Hz)</dt>
		<dd>{{info['PROCESSOR_CURRENT_SPEED']}}</dd>
		<dt>Overcloked speed (MHz)</dt>
		<dd>{{info['PROCESSOR_OVERLOCK']}}</dd>
		<dt>Load Average</dt>
		<dd>{{info['LOAD_AVG']}}</dd>
	</dl>
</div>

<div class="span5">
	<h3 class="text-info">Memory usage</h3>
	% used = int(float(info['USED_MEMORY']) / float(info['MEMORY_TOTAL']) * 100)
	% free = int(float(info['FREE_MEMORY']) / float(info['MEMORY_TOTAL']) * 100)
	% color = "success" if used < 70 else "warning" if used < 85 else "danger"
	<div class="progress progress-{{color}}">
		<div class="bar" style="width: {{used}}%;"></div>
	</div>
	<dl class="dl-horizontal">
		<dt>Total memory</dt>
		<dd>{{info['MEMORY_TOTAL']}} K</dd>
		<dt>Used</dt>
		<dd>{{info['USED_MEMORY']}} K <b>({{used}}%)</b></dd>
		<dt>Free</dt>
		<dd>{{info['FREE_MEMORY']}} K ({{free}}%)</dd>
	</dl>

	<hr />


	<h3 class="text-info">Disk usage</h3>
	% clean = lambda str: float(filter(lambda x: x.isdigit(), str))
	% used = int(clean(info['DISK_USED']) / clean(info['DISK_TOTAL']) * 100)
	% free = int(clean(info['DISK_FREE']) / clean(info['DISK_TOTAL']) * 100)
	% color = "success" if used < 70 else "warning" if used < 85 else "danger"
	<div class="progress progress-{{color}}">
		<div class="bar" style="width: {{used}}%;"></div>
	</div>
	<dl class="dl-horizontal">
		<dt>Total HDD space</dt>
		<dd>{{info['DISK_TOTAL']}}</dd>
		<dt>Used</dt>
		<dd>{{info['DISK_USED']}} <b>({{used}}%)</b></dd>
		<dt>Free</dt>
		<dd>{{info['DISK_FREE']}} ({{free}}%)</dd>
	</dl>

</div>
