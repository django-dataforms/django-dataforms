$(document).ready(function() {
	
	$("#add-fields-nav li a").click(function(){
		$.ajax({
			url: 'field/' + $(this).attr('id').split('-')[1],
			success: function(response) {
				$("#form-layout-fields").append(response);
				

	
			}
		})
		
		return false;
	});
	
	$("#form-layout-fields").sortable();
	
	$("#form-layout-fields li").live('click', function(){
		$("#form-layout-fields li").removeClass('form-selected');
		$(this).addClass('form-selected');
	});
	
	$("#builder-nav a").click(function(){
		$("#builder-panel div.panel").hide();
		
		var divID = $(this).attr('rel');
		$("#"+divID).show();
		console.log(divID);
		return false;
	});
});