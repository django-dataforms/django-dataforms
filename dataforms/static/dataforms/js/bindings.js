var binding_results = {};

function setBindings() {
	// Create the binding event handlers
	var binding_selectors = $("input[type='hidden'][name*='js_dataform_bindings']");
	var bindings = [];

	// Parse the bindings from the hidden field into a javascript array
	$.each(binding_selectors, function(index, binding){
		bindings.push(jQuery.parseJSON($(this).val()));
	});

	$.each(bindings, function(i1, bindingArray){
		
		$.each(bindingArray, function(i2, binding){
			
			if (binding.field_choice) {
				var selector = smartGetSelector(binding.selector, true, true);
			}
			else {
				var selector = smartGetSelector(binding.selector);
			}
			
			//console.log(selector);
			//console.log(binding.selector);
			
			selector.data('binding', binding);
			selector.bind('init', function(event){
				doBinding(event, true);
			});
			
			// Set the event handlers			
			if (selector.is('select')) {
				selector.change(doBinding);
			}
			else if (selector.is('input:text, textarea')) {
				selector.keyup(doBinding);
			}
			else {
				selector.click(doBinding);
			}
			
			// Manually trigger bindings for page start
			selector.trigger('init');
		});
	});
}


function smartGetSelector(selector, isChoiceField, isRootElement) {
    var bindingElement;
    
    var name = selector.split('___')[0];
    if (isChoiceField) {
	    var value = selector.split('___')[1];
    } 

	if (value) {
		// We're on a list (parent with choice)
		bindingElement = $(":input[name='"+name+"'][value='"+value+"'], select[name='"+name+"'] option[value='"+value+"']");
		
		// FIXME: Hackish way to include selects, should write this better.
		if (isRootElement && bindingElement.is("option")) {
			bindingElement = bindingElement.parent();
		}
	} else {
		// We're on a string (direct parent)
		bindingElement = $(":input[name='"+name+"']");
		
		// TODO: Do we need this??
		if (!bindingElement.length) {
			// If we didn't find an element #id_ directly, look for a label with for=id_name
			bindingElement = $("label[for*='id_"+name+"']");
		}
	}
	return bindingElement;
}


function smartGetElement(selector) {
	return selector.split('___')[0];
}

function smartGetElementValue(selector) {
	return selector.split('___')[1];
}


function doBinding(event, noAnimation) {
	// Assign the binding
	var binding = $(event.currentTarget).data('binding');
	var isTrue = hasTruth($(event.currentTarget));
	var bindingElement = smartGetSelector(binding.selector);
	
	if (noAnimation) {
		var speed = 0;
	}
	else {
		var speed = 100;
	}

	if (binding.value) {
		var bindingValue = binding.value;
	}
	else {
		var bindingValue = smartGetElementValue(binding.selector);
	}

	// Do show/hide action
	if (binding.action == 'show-hide') {
		// If this is an object (array), then we know we have a fieldchoice
		
		// If the value  matches, then we are true!
		if (isTrue) {
			
			if (binding.true_field) {
				// Loop through the true fields to show
				$.each(binding.true_field, function(index, selector){
					$("label[for*='id_"+selector+"']").closest(".dataform-field,tr,ul,p").show(speed);
				});
			}
			
			if (binding.true_choice) {
				// Loop though the true field choices to show
				$.each(binding.true_choice, function(index, selector){

					var bindingElement = smartGetSelector(selector, true);
					var element = smartGetElement(selector);
					var value = smartGetElementValue(selector);
					
					// console.log(element);
					// console.log(value);
					
					$("label[for*='id_"+element+"_0']").first().show(speed);
					// Show if the value matches the fieldchoice
					if (bindingElement.is("option")) {
						bindingElement.removeAttr('disabled');
					}
					else {
						bindingElement.closest('li').show(speed)
					}
				});
			}
			
		}
		// If The value does not match then we are false!
		else {
			
			if (binding.false_field) {
				// Loop through the false fields to hide
				$.each(binding.false_field, function(index, selector){
					$("label[for*='id_"+selector+"']").filter(":first").closest(".dataform-field,tr,ul,p").hide(speed);
				});
			}

			// Loop though the false field choices to hide
			if (binding.false_choice) {
				$.each(binding.false_choice, function(index, selector){
					
					var bindingElement = smartGetSelector(selector, true);
					var element = smartGetElement(selector);
					var value = smartGetElementValue(selector);
					
					//console.log(binding.false_choice);
					//console.log(bindingElement);
					//console.log(selector);
					//console.log(element);
					//console.log(value);
					
					
					// Hide if the value matches the fieldchoice
					if (bindingElement.is("option")) {
						bindingElement.attr('disabled', 'disabled');
					}
					else {
						bindingElement.closest('li').hide('fast', function(){
							if (bindingElement.closest(".dataform-field,tr,ul,p").find('input:visible').length == 0) {
								$("label[for*='id_"+element+"']").first().hide();
							}
						});
					}
				});
			}
		}
			
		
	}
	// Do custom function, not implemented yet...
	else {
		// TODO: Need to code this.		
	}

}


function hasTruth(selector) {
	var bindingOperator;
	var bindingValue;
	var binding = selector.data('binding');
	var bindingElement = smartGetSelector(binding.selector);
	var result = false;
	
	// Find out the operator and the value
	if (binding.field_choice) {
		bindingOperator = 'checked';
		bindingValue = smartGetElementValue(binding.selector);
	}
	else {
		bindingOperator = binding.operator;
		bindingValue = binding.value;
	}
	
	// The default is to return true because this is coming from a
	// click or change handler, meaning we know something was checked
	if (bindingOperator == 'checked') {
		// If there is a value then we need to check to see if the values
		// match and if not then return false
		if (selector.is("input")) {
			if (selector.is(":checked")) {
				result = true;
			}
		}
		else {
			if (bindingValue == selector.val()) {
				result = true;
			}
		}
	}
	// All other operators require that there is a value, so if there is not
	// then return false below
	else {
		// If there is a value then we need to check to see if the values
		
		// equal match
		if (bindingOperator == 'equal'  && selector.val() == bindingValue) {
			result = true;
		}
		// not equal match
		if (bindingOperator == 'not-equal'  && selector.val() != bindingValue) {
			result = true;
		}
		// contains match
		if (bindingOperator == 'contain'  && selector.val().indexOf(bindingValue) != -1) {
			result = true;
		}
		// does not contains match
		if (bindingOperator == 'not-contain'  && selector.val().indexOf(bindingValue) == -1) {
			result = true;
		}
		
	}
	
	binding_results[binding.id] = result
	
	// Loop through additional rules to see if they are false
	// If they are, we override the result until they are true.
	// This allows us to use compound bindings.
	if (binding.additional_rules) {
		$.each(binding.additional_rules, function(index, value){
			if (binding_results[value] == false) {
				result = false;
			}
		});
	}

	return result;
}

$(function() {
	setBindings();
});
