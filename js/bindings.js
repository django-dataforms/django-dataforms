function setBinding(parent, child, choice, effectTime) {
	parent.change(function() {
		doBinding(parent, child, choice, effectTime);
	});
}

function doBinding(parent, child, choice, effectTime){
	var boundArea = child.parent()
	var effectTime = typeof(effectTime) != 'undefined' ? effectTime : 500;
	var choice = typeof(choice) != 'undefined' ? choice : -1;
	
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
	if (parent.attr("checked") || parent.val() == choice) {
		boundArea.slideDown(effectTime);
	} else {
		boundArea.slideUp(effectTime);
	}
}

$(function() {
	
	// Create the binding event handlers
	bindings = JSON.parse($("input[type='hidden'][name*='js_dataform_bindings']").val());
	
	for (var i = 0; i < bindings.length; i++) {
		var parent = $("#id_" + bindings[i][0]);
		var choiceVal = undefined;
		
		if (bindings[i].length == 2) {
			// Simple binding (like a single checkbox).
			// (parent, child)
			
			var child = $("#id_" + bindings[i][1]);
			setBinding(parent, child);
			
		} else if (bindings[i].length == 3) {
			// Choice binding (like a dropdown)
			// (parent, choice value, child)
			
			var child = $("#id_" + bindings[i][2]);
			var choiceVal = bindings[i][1];
			
			var parent = $("#id_" + bindings[i][0]);
			if (!parent.length){
				parent = $("input[name='"+ bindings[i][0]+"'][value='"+choiceVal+"']");
			}
			
			if (parent.length) {
				var elementName = parent[0].tagName.toLowerCase();
				
				if (elementName == "select") {
					// Select element
					setBinding(parent, child, choiceVal);
				} else if (elementName == "input" && parent[0].type == "radio") {
					// Radio buttons
					setBinding(parent, child);
				} else {
					if (console && console.log){
						console.log(parent);
						console.log(child);
					}
					alert("Choice bindings for " + elementName + " elements has not been implemented.")
				}
			} else {
				if (console && console.log){
					console.log("Couldn't find parent " + "#id_" + bindings[i][0])
				}
			}
		}
		
		// Hide/show all bound fields default state
		doBinding(parent, child, choiceVal, 0);
	}
	
});