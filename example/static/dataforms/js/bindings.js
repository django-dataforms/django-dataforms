function setBindings() {
	// Create the binding event handlers
	var many_bindings_js = $("input[type='hidden'][name*='js_dataform_bindings']");
	var bindings_js = '';
	var bindings;
	var bindingParent;
	var parents;
	var children;
	
	for (var B=0; B < many_bindings_js.length; B++) {
		bindings_js = many_bindings_js[B].value;
		
		if (!bindings_js)
			continue;
		
		bindings = JSON.parse(bindings_js);
		
		for (var k=0; k < bindings.length; k++) {
			
			// Parents
			parents = bindings[k]['parents'];
			for (var i=0; i < parents.length; i++) {
				for (var j=0; j < parents[i].length; j++) {
					bindingParent = smartGetElement(parents[i][j]);
					
					// Replace the original string with the actual DOM element 
					if (typeof parents[i][j] == "object") {
						parents[i][j][0] = bindingParent;
					} else {
						parents[i][j] = bindingParent;
					}
					
					// Create the set of bindings on this element
					// FIXME: If the exact same binding has already been set before,
					// it will be set again here. Potential performance hit if
					// setBindings() is called too many times. 
					// 
					if (!bindingParent.data("bindings")) {
						bindingParent.data("bindings", []);
					}
                    
                    // Set each group of compound or single bindings (elements which
					// are AND'd together). Each group will be OR'd together to evaluate truth.					
					bindingParent.data("bindings").push(bindings[k]);

					// Set event handler
					bindingParent.change(doBinding).click(doBinding);
					if (bindingParent.attr("type") == 'text') {
						bindingParent.keyup(doBinding);
					}
				}
			}
			
			// Children
			children = bindings[k]['children'];
			for (var i=0; i < children.length; i++) {
				var child = smartGetElement(children[i]);
				children[i] = child.closest(".form-row");
				
				// Evaluate initial parent states and hide children if needed
				if (!hasAllTruth(parents)) {
					$(children[i]).hide();
				}
			}
		}
	}
}

function smartGetElement(name) {
    var bindingElement;
    
	if (typeof name == "object") {
		// We're on a list (parent with choice)
		bindingElement = $("input[name='"+name[0]+"'], select[name='"+name[0]+"'], textarea[name='"+name[0]+"']");
	} else {
		// We're on a string (direct parent)
		bindingElement = $("#id_"+name);
		if (!bindingElement.length) {
			// If we didn't find an element #id_ directly, look for a label with for=id_name
			bindingElement = $("label[for*='id_"+name+"']");
		}
	}
	return bindingElement;
}

function doBinding() {
	var parents;
	var children;
	var bindings = $(this).data("bindings");
	
	for (var b=0; b < bindings.length; b++) {
		parents = bindings[b]['parents'];
		children = bindings[b]['children'];
		
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
}

function contains(haystack, needle) {
	for (i in haystack)
		if (haystack[i] == needle)
			return true;
	return false;
}

function hasSingleTruth(element) {
	var choice = null;
	if (element.length > 1) {
		// We're on a list (parent with choice)
		choice = element[1];
		element = element[0];
	}
	
	var tagName = element.attr("type");
	var value = element.val();
	
	if (
	(tagName == "checkbox" && (element.length == 1 && element.attr("checked") || element.filter("input[value='"+choice+"']").attr("checked")))
	|| (tagName == "select-one" && value == choice)
	|| (tagName == "select-multiple" && value && contains(value, choice))
	|| (tagName == "text" && value != '')
	|| (tagName == "radio" && element.filter(":checked").val() == choice)) {
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
