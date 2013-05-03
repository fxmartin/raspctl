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

$('#volume a').click(function() { 
	event.preventDefault();
	$.get(event.currentTarget.href, function(){});
});
