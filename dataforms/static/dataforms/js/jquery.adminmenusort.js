$(document).ready(function() {
	
	if (((location.search.indexOf("__id__exact") != -1) ||
		(location.search.indexOf("__title=") != -1)) &&
		(location.search.indexOf("ot=") == -1) && 
		(location.search.indexOf("o=") == -1)) {
		
		var fixHelper = function(e, ui) {
		    ui.children().each(function() {
		        $(this).width($(this).width());
		    });
		    return ui;
		};
		
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
});


