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
