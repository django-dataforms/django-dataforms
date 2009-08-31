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
		
		//var bindings = JSON.parse(bindings_js);
		var bindings = [
		                // Single checkbox
		                {
		                	"parents" : [["personal-information__checkbox"]],
		                	"children" : ["personal-information__dropdown"]
		                },
		                // Single dropdown with choice of "Yes"
		                {
		                	"parents" : [[["personal-information__dropdown", "yes"]]],
		                	"children" : ["personal-information__date"]
		                },
		                // Dropdown with choice of "Yes" OR Checkbox checked
		                {
		                	"parents" : [[["personal-information__dropdown", "yes"]], ["personal-information__checkbox"]],
		                	"children" : ["personal-information__checkbox"]
		                }
		                ];
		                
		
		// Ready, go.
		
		
	}
}

$(function() {
	setBindings();
});
