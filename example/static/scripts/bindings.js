function doBindings(parent, child, effectTime) {
	var boundArea = child.parent()
	effectTime = typeof(effectTime) != 'undefined' ? effectTime : 500;
	
	// This fixes subelements like multiple checkboxes
	if (boundArea.attr("tagName").toLowerCase() == "label") {
		switch (boundArea.parent().attr("tagName").toLowerCase()){
			case "li":
				boundArea = boundArea.parent().parent()
				boundArea = boundArea.add(boundArea.prev())
				break;
		}
	}
	
	// We can't just do slideToggle because this slide is going to be called
	// once for every subelement bound to the parent, where slideDown and
	// slideUp mask this behavior because they can be called multiple times
	if (parent.attr("checked")) {
		boundArea.slideDown(effectTime);
	} else {
		boundArea.slideUp(effectTime);
	}
}

$(function() {
	
	// Create the binding event handlers
	relatedFields = $("input[rel], select[rel]");
	relatedFields.each(function() {
		var child = $(this);
		var parent = $("#" + child.attr("rel"));
		
		parent.change(function() {
			doBindings(parent, child);
		});
		
		// Hide/show all bound fields default state
		doBindings(parent, child, 0);
	});
	
});