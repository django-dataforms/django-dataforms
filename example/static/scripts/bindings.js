function setBindings() {
	// Create the binding event handlers
	var many_bindings_js = $("input[type='hidden'][name*='js_dataform_bindings']");
	var bindings_js = '';
	var bindings;
	var bindingParent;
	
	for (var j=0; j < many_bindings_js.length; j++) {
		bindings_js = many_bindings_js[j].value;
		
		if (!bindings_js)
			continue;
		
		bindings = JSON.parse(bindings_js);
		
		for (var k=0; k < bindings.length; k++) {
			var parents = bindings[k]['parents'];
			for (var i=0; i < parents.length; i++) {
				for (var j=0; j < parents[i].length; j++) {
					bindingParent = smartGetElement(parents[i][j]);
					
					// Replace the original string with the actual DOM element 
					if (typeof parents[i][j] == "object") {
						parents[i][j][0] = bindingParent;
					} else {
						parents[i][j] = bindingParent;
					}
					
					bindingParent.data("parents", bindings[k]['parents']);
					bindingParent.data("children", bindings[k]['children']);
					
					// Set event handler
					bindingParent.change(doBinding);
				}
			}
			var children = bindings[k]['children'];
			for (var i=0; i < children.length; i++) {
				child = smartGetElement(children[i]);
				children[i] = child.closest(".form-row");
				$(children[i]).hide();
			}
		}
	}
}

function smartGetElement(name) {
	if (typeof name == "object") {
		// We're on a list (parent with choice)
		bindingParent = $("input[name='"+name[0]+"'], select[name='"+name[0]+"']");
	} else {
		// We're on a string (direct parent)
		bindingParent = $("#id_"+name);
		if (!bindingParent.length) {
			// If we didn't find an element #id_ directly, look for a label with for=id_name
			bindingParent = $("label[for*='id_"+name+"']");
		}
	}
	
	return bindingParent;
}

function doBinding() {
	var parents = $(this).data('parents');
	var children = $(this).data('children');
	
	if (hasAllTruth(parents)){
		// show
		for (var i=0; i<children.length; i++){
			$(children[i]).slideDown();
		}
	} else {
		// hide
		for (var i=0; i<children.length; i++){
			$(children[i]).slideUp();
		}
	}
}

function hasSingleTruth(element) {
	var choice = null;
	if (element.length > 1) {
		// We're on a list (parent with choice)
		choice = element[1];
		element = element[0];
	}
	
	var tagName = element.attr("type");
	
	if (
	(tagName == "checkbox" && element.attr("checked"))
	|| (tagName == "select-multiple" && element.val() == choice)
	|| (tagName == "radio" && element.filter(":checked").val() == choice)) {
		// FIXME add && choice in element.val()
		return true;
	} else {
		return false;
	}
}

function hasAllTruth(listOfParents) {
	for(var i=0; i < listOfParents.length; i++) {
		var parentSet = listOfParents[i];
		
		// Assume we have all truth
		var tempTruth = true;
		
		for(var x=0; x < parentSet.length; x++){
			var parent = parentSet[x];
			
			// Make sure I always had truth before
			tempTruth = hasSingleTruth(parent) && tempTruth;
		}
		
		if(tempTruth)
			return true;
	}
	return false;
}

$(function() {
	setBindings();
});
