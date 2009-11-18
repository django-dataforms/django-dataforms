$(function() {
	// On page load, add the datepicker for all DateFields
	$("input.datepicker").datepicker({
		changeMonth: true,
		changeYear: true,
		showButtonPanel: true
	});
});