function setBinding(parent, child, choice, effectTime) {
	parent.change(function() {
		doBinding(parent, child, choice, effectTime);
	});
}

function doBinding(parent, child, choice, effectTime){
	var boundArea = child.parent()
	var effectTime = typeof(effectTime) != 'undefined' ? effectTime : 500;
	var choice = typeof(choice) != 'undefined' ? choice : -1;
	
	if (!boundArea.length && window.console && window.console.log && window.console.error) {
		console.error("Couldn't do binding because boundArea was empty.")
		console.log("Parent:")
		console.log(parent)
		console.log("Child:")
		console.log(child)
		return;
	} else if (!boundArea.length) {
		return;
	}
	
	// This fixes subelements like multiple checkboxes
	if (boundArea.attr("tagName").toLowerCase() == "label") {
		switch (boundArea.parent().attr("tagName").toLowerCase()){
		case "li":
			boundArea = boundArea.parent().parent().parent()
			break;
		}
	}
	
	// We can't just do slideToggle because this slide is going to be called
	// once for every subelement bound to the parent, where slideDown and
	// slideUp mask this behavior because they can be called multiple times
	if (parent.attr("checked")
		|| (parent.parent().find("input:checked").length && parent.val() == choice)
		|| (parent.parent().find("select").length && parent.val() == choice)) {
		boundArea.slideDown(effectTime);
		boundArea.show();
	} else {
		boundArea.slideUp(effectTime);
		boundArea.hide();
	}
}

function setBindings() {
	// Create the binding event handlers
	var many_bindings_js = $("input[type='hidden'][name*='js_dataform_bindings']");
	var bindings_js = '';
	
	for (var j=0; j < many_bindings_js.length; j++) {
		bindings_js = many_bindings_js[j].value;
		
		if (!bindings_js)
			continue;
		
		var bindings = JSON.parse(bindings_js);
		
		for (var i = 0; i < bindings.length; i++) {
			var parent = $("#id_" + bindings[i][0]);
			var choiceVal = undefined;
			var success = true;
			
			if (bindings[i].length == 2) {
				// Simple binding (like a single checkbox).
				// (parent, child)
				
				var child = $("#id_" + bindings[i][1]);
				if (!child.length){
					child = $("input[name='"+ bindings[i][1]+"']").slice(0,1);
				}
				
				setBinding(parent, child);
				
			} else if (bindings[i].length == 3) {
				// Choice binding (like a dropdown)
				// (parent, choice value, child)
				
				var choiceVal = bindings[i][1];
				var child = $("#id_" + bindings[i][2]);
				if (!child.length){
					child = $("input[name='"+ bindings[i][2]+"']").slice(0,1);
				}
				
				var parent = $("#id_" + bindings[i][0]);
				if (!parent.length){
					parent = $("input[name='"+ bindings[i][0]+"'][value='"+choiceVal+"']");
				}
				
				if (parent.length) {
					var elementName = parent[0].tagName.toLowerCase();
					
					if (elementName == "select") {
						// Select element
						if (window.console && window.console.log){
							console.log("Adding select binding for " + "#id_" + bindings[i][0] + " --> " + "#id_" + bindings[i][2])
						}
						setBinding(parent, child, choiceVal);
					} else if (elementName == "input" && parent[0].type == "radio") {
						// Radio buttons
						if (window.console && window.console.log){
							console.log("Adding radio binding for " + "#id_" + bindings[i][0] + " --> " + "#id_" + bindings[i][2])
						}
						setBinding(parent, child, choiceVal);
					} else {
						if (window.console && window.console.log){
							console.log(parent);
							console.log(child);
						}
						success = false;
						if (window.console && window.console.error){
							console.error("Choice bindings for " + elementName + " elements has not been implemented.")
						}
					}
				} else {
					success = false;
					if (window.console && window.console.error){
						console.error("Couldn't find parent " + "#id_" + bindings[i][0])
					}
				}
			}
			
			// Hide/show all bound fields default state
			if (success) {
				doBinding(parent, child, choiceVal, 0);
			}
		}
	}
}

$(function() {
	setBindings();
});
