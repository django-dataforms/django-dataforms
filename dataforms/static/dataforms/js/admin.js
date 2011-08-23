$(document).ready(function() {
	
	// Helper Function for Sort
	var fixHelper = function(e, ui) {
	    ui.children().each(function() {
	        $(this).width($(this).width());
	    });
	    return ui;
	};
	
	// Sort for Mapping list Views
	if (((location.search.indexOf("__id__exact") != -1) ||
		(location.search.indexOf("__title=") != -1)) &&
		(location.search.indexOf("ot=") == -1) && 
		(location.search.indexOf("o=") == -1)) {
		
		$('#result_list').sortable({
			items: '.row1, .row2',
			handle: 'td',
			helper: fixHelper,
			update: function(event, ui) {
				var items_moved = $(ui.item).parent().children();
				
				$(items_moved).each(function(index, ele){
					$(this).find('input[class="vIntegerField"]').val(index);
				});
			}
		});
		
		
		$('#result_list td').css({'cursor':'move'});
	}
	
	// Sort for Tabular Inlines
	$('div.inline-group table tbody').sortable({
		items: '.row1, .row2',
		handle: 'td',
		helper: fixHelper,
		update: function(event, ui) {
			var items_moved = $(ui.item).parent().children();
			
			$(items_moved).each(function(index, ele){
				$(this).find('input[class="vIntegerField"]').val(index);
			});
		}
	});
		
	$('div.inline-group table tbody tr').css({'cursor':'move'});
	
	
	// Binding Function Helpers
	$("#binding_form #id_data_form").change(function(){
		$.getJSON('ajax/dataformfield/?values=field__slug,field__id&order=field__slug&data_form__id='+$(this).val(), function(data) {
			if(data) {
				var items = ['<option value="">---------</option>'];
				$.each(data, function(key, val) {
					items.push('<option value="' + val.field__id + '">' + val.field__slug + '</option>');
				});
				
				var selected = $("#binding_form #id_field").val();
				$("#binding_form #id_field").html(items.join(''));
				$("#binding_form #id_field").val(selected);
			}
		});
	}).trigger('change');

	$("#binding_form #id_field").change(function(){
		$.getJSON('ajax/fieldchoice/?values=field__slug,choice__value,id&order=choice__value&field__id='+$(this).val(), function(data) {
			if(data) {
				var items = ['<option value="">---------</option>'];
				$.each(data, function(key, val) {
					items.push('<option value="' + val.id + '">' + val.choice__value + ' (' + val.field__slug + ')</option>');
				});
				
				var selected = $("#binding_form #id_field_choice").val();
				$("#binding_form #id_field_choice").html(items.join(''));
				$("#binding_form #id_field_choice").val(selected);
			}
		});
	}).trigger('change');

	$("#binding_form #id_field_choice").change(function(){
		if ($(this).val()) {
			$("#binding_form #id_operator").val('checked');
			$("#binding_form #id_operator option:not(:selected)").attr('disabled', 'disabled');
		}
		else {
			$("#binding_form #id_operator").val('');
			$("#binding_form #id_operator option").removeAttr('disabled');
		}
	});
});


