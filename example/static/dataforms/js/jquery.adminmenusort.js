/* menu-sort.js */

jQuery(function($) {
	$('div.inline-group').sortable({
		/*containment: 'parent',
		zindex: 10, */
		items: 'div.inline-related',
		handle: 'h3',
		update: function() {
			reOrder();
		}
	});
	$('div.inline-related h3').css({'cursor':'move'});
	
	if ($('div.inline-related').find('ul.errorlist').length == 0) {
		//$('div.inline-related').find('input[id$=order]').parent('div').hide();
	}
});

jQuery(function($) {
	$("div.inline-related input:checkbox[id$=DELETE]").change(function() {
		if ($(this).attr('checked')) {
			$(this).parents('div.inline-related').children('fieldset.module').addClass('collapsed');
		} else {
			$(this).parents('div.inline-related').children('fieldset.module').removeClass('collapsed');
		}
	});
});

jQuery(function($) {
	
	$('form')[0].reset();
	
	//create the 'add another link
	var add_ul = $('<ul class="tools"><li></li></ul>');
	var add_href = $('<a></a>').addClass("add").text('Add Another').attr('href','#');
	
	//attach the 'add another' link to the inline
	$(add_ul).children("li").append(add_href);
	$("div.inline-group").append(add_ul);
	
	$('fieldset.module select').click(function(){
		reOrder();
	});
	
	$('div.inline-group a.add').click(function(){
		var inline_group = $(this).parents('div.inline-group');
		var last_related = $(inline_group).children('div.inline-related:last');
		var related_num = $(last_related).children('input:last').val();
		var copy = $(last_related).clone(true);
		
		var remove_span = $('<span></span>').addClass("delete");
		var remove_href = $('<a></a>').text('Remove').attr('href','#');
		$(remove_span).append(remove_href);
		
		
		//clear all selects and inputs
		$(copy).find('input').val('');
		$(copy).find('select').val('');
		$(copy).find('input:last').val(related_num);
		$(copy).find('input[id$=order]').parent('div').show();
		
		//find the h3 and delete everything then add the b and modified span tag
		var h3_b = $(copy).find('h3 b');
		$(copy).find('h3').empty().append(h3_b).append(remove_span);
		
		//add the ele to the page
		$(last_related).after(copy);
		
		$(copy).find('span.delete a').click(function(){
			$(this).parents('div.inline-related').find('fieldset').html('');
			$(this).parents('div.inline-related').removeClass('inline-related last-related').addClass('inline-disabled').hide();
			reOrder();
			return false;
		});
		
		//re-order the order fields
		reOrder();
		
		//increment TOTAL_FORMS for the current group
		changeFormValues(inline_group);
		
		return false;
	});
	
});

function changeFormValues(inline_group) {
	//total number of forms
	var total_forms_val = $(inline_group).find("input[id*='TOTAL_FORMS']").val();
	var num_str = '-'+(total_forms_val)+'-';
	total_forms_val++;
	
	$(inline_group).find("input[id*='TOTAL_FORMS']").val(total_forms_val);
	
	$(inline_group).children('div.last-related').find("[id*='_set-'],[for*='_set-']").each(function(){
		
		if($(this).attr('id')) {
			$(this).attr('id', $(this).attr('id').replace(/-(\d+)-/, num_str));
		}

		if($(this).attr('for')){
			$(this).attr('for', $(this).attr('for').replace(/-(\d+)-/, num_str));
		}

		if($(this).attr('name')){
			$(this).attr('name', $(this).attr('name').replace(/-(\d+)-/, num_str));
		}
	});
}

function reOrder() {
	$('div.inline-group').each(function(){
		var count = 1
		$(this).find('div.inline-related').each(function() {
			$(this).removeClass('last-related');
			if ($(this).find('select').val()) {
				$(this).find('input[id$=order]').val(count);
				count++;
			}
			else {
				$(this).find('input[id$=order]').val('');
			}
		});
		$(this).children('div.inline-related:last').addClass('last-related');
	});
}
