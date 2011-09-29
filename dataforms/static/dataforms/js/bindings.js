var binding_results = {};

function setBindings() {
	// Create the binding event handlers
	var binding_selectors = $("input[type='hidden'][name*='js_dataform_bindings']");
	var bindings = [];

	// Parse the bindings from the hidden field into a javascript array
	$.each(binding_selectors, function(index, binding){
		var binding = jQuery.parseJSON($(this).val());
		if (binding) {
			bindings.push(binding);
		}
		
		// Remove values from all hidden fields
		$.unique($(this).parents('form')).submit(function() {
			$(".dataform-field:hidden").val('').removeAttr('checked');			
		});
		
	});

	$.each(bindings, function(i1, bindingArray){

		$.each(bindingArray, function(i2, binding){
			
			var selector = smartGetSelector(binding.selector);
			
			if (selector.data('bindings')) {
				selector.data('bindings').push(binding);
			}
			else {
				selector.data('bindings', [binding]);
			}
			
			// Set the event handlers			
			if (selector.is('select')) {
				selector.change(doBindings);
			}
			else if (selector.is('input:text, textarea')) {
				selector.keyup(doBindings);
			}
			else {
				selector.click(doBindings);
			}

			selector.bind('init', function(event){
				doBindings(event, true);
			});

			// Manually trigger bindings for page start
			selector.trigger('init');
		});
	});
}


function smartGetSelector(name, choiceValue) {
    var bindingElement;
    
    if (choiceValue) {
	    var value = choiceValue;
    } 

	if (value) {
		// Get a Field Choice Element
		bindingElement = $("[name='"+name+"'][value='"+value+"']");
		// If length is 0, then it is assumed that
		// the Field Choice is an select option
		if (bindingElement.length == 0) {
			bindingElement = $("[name='"+name+"'] option[value='"+value+"']");
		}
	} else {
		// Get a Field Element 
		bindingElement = $("[name='"+name+"']");
	}
	
	return bindingElement;
}


function doBindings(event, noAnimation) {
	// Assign the binding
	var selector = $(event.currentTarget);
	var bindings = selector.data('bindings');
	
	$.each(bindings, function(index, binding){
		var isTrue = hasTruth(selector, binding);	
	
		if (noAnimation) {
			var speed = 0;
		}
		else {
			var speed = 100;
		}
	
		// Do show/hide action
		if (binding.action == 'show-hide') {
	
				
			// If true
			if (isTrue) {
				
				if (binding.true_field) {
					// Loop through the true fields to show
					$.each(binding.true_field, function(index, selector){
						$("label[for*='id_"+selector+"']").closest(".dataform-field,tr,ul,p,li").show(speed);
					});
				}
				
				if (binding.true_choice) {
					// Loop though the true field choices to show
					$.each(binding.true_choice, function(index, selector){
	
						var bindingElement = smartGetSelector(selector[0], selector[1]);
						
						$("label[for*='id_"+selector[0]+"_0']").first().show(speed);
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
			// If false
			else {
				
				if (binding.false_field) {
					// Loop through the false fields to hide
					$.each(binding.false_field, function(index, selector){
						$("label[for*='id_"+selector+"']").closest(".dataform-field,tr,ul,p,li").hide(speed);
					});
				}
	
				// Loop though the false field choices to hide
				if (binding.false_choice) {
					$.each(binding.false_choice, function(index, selector){
						
						var bindingElement = smartGetSelector(selector[0], selector[1]);
						
						// Hide if the value matches the fieldchoice
						if (bindingElement.is("option")) {
							bindingElement.attr('disabled', 'disabled');
						}
						else {
							bindingElement.closest('li').hide('fast', function(){
								if (bindingElement.closest(".dataform-field,tr,ul,p").find('input:visible').length == 0) {
									$("label[for*='id_"+selector[0]+"']").first().hide();
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
	
	});

}


function hasTruth(selector, binding) {
	var bindingValue;
	var selectorValue = [];
	//var binding = selector.data('bindings');
	var bindingOperator = binding.operator;
	var result = false;
	
	
	// Find out the operator and the value
	if (binding.field_choice) {
		bindingValue = binding.field_choice__choice__value;
		bindingSelector = smartGetSelector(binding.selector, bindingValue);
	}
	else {
		bindingValue = binding.value;
		bindingSelector = smartGetSelector(binding.selector);
	}
	
	// First evaluate for checked
	if (bindingOperator == 'checked') {
		// Checked should only work for radios, checkboxes, or selects
		if (bindingSelector.is(":radio,:checkbox,select,option")) {
			
			// If we have a select and something is selected the selected value is not null
			// We know that its a field and it should return true.
			if (bindingSelector.is("select") && bindingSelector.val()) {
				result = true;
			}
			// If Option, then we know its a field choice from a select
			else if (bindingSelector.is("option")) {
			
				// Re-assign to the parent select
				bindingSelector = bindingSelector.parent();
				
				// Check if the select has a value
				if (bindingSelector.val()){
					
					// This logic covers single select and multi-selct boxes
					// We put all answers into an array
					if ($.isArray(bindingSelector.val())){
						selectorValue = bindingSelector.val();
					}
					else {
						selectorValue.push(bindingSelector.val())
					}
					
					// If something values match
					if ($.inArray(bindingValue, selectorValue) != -1) {
						result = true;
					}
				}
			}
			
			// Otherwise we have radios or checkboxes so we just
			// need to see if they are checked.
			else if (bindingSelector.is(":checked")) {
				result = true;
			}
		}
		
		// true if has a value
		else if (bindingSelector.val()){
			result = true;
		}
	}
	// Now evaluate based on other contidions
	// Check to see if there is a value
	else if (bindingSelector.val()) {
		
		// If this is a multi-select, put its values into the selectorValue array.
		if (bindingSelector.is("select[multiple='multiple']")) {
			selectorValue = bindingSelector.val();
		}
		// If this is one or more checkboxes, push the value(s) into the selectorValue array.
		else if (bindingSelector.is(":checkbox,:radio")) {
			$.each(bindingSelector.filter(":checked"), function(index, value){
				selectorValue.push($(value).val());
			});
		}
		// Otherwise everything ise is just a single value, put that into the array.
		else {
			selectorValue.push(bindingSelector.val());
		}
		
		// equal match
		if (bindingOperator == 'equal'  && $.inArray(bindingValue, selectorValue) != -1) {
			result = true;
		}
		// not equal match
		if (bindingOperator == 'not-equal'  && $.inArray(bindingValue, selectorValue) == -1) {
			result = true;
		}
		// contains match
		if (bindingOperator == 'contain') {
			$.each(selectorValue, function(index, value){
				if (value.indexOf(bindingValue) != -1) {
					result = true;
				}
			});
		}
		// does not contains match
		if (bindingOperator == 'not-contain') {
			$.each(selectorValue, function(index, value){
				if (value.indexOf(bindingValue) == -1) {
					result = true;
				}
			});
		}
	}
	
	binding_results[binding.id] = result
	
	// Loop through additional rules to see if they are false
	// If they are, we override the result until they are true.
	// This allows us to use compound bindings.
	if (binding.additional_rules) {
		$.each(binding.additional_rules, function(index, value){
			if (!binding_results[value] || binding_results[value] == false) {
				result = false;
			}
		});
	}
	return result;
}


$(function() {
	setBindings();
});
