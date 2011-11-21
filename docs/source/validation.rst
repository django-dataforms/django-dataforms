Dataforms Form Validation
=========================

Validation on Dataforms is very similiar to how you would do validation on a regular
Django form.  The are only 2 things that you needs to remember:

	*	Make sure you declare a *staticmethod* decorator on all classes that are to be 
		used for validation on Dataforms
		
	*	| The name of you validation class has to match the slug of the dataform
		| for which you intend to validate.
		|
		| This is accomplished by *create_form_class_title* method in dataforms.forms.
		| For example: a slug of 'my-bio' will translate to 'MyBioForm'
		
Below is an example of how this could work::

	from django import forms

	class BaseValidationForm(object):
		@staticmethod
		def clean(self):
			raise forms.ValidationError('clean base error')

	# The name of your form slug should be 'personal-information'	
	class PersonalInformationForm(BaseValidationForm):
		@staticmethod
		def clean(self):
			raise forms.ValidationError('clean error')
		
		@staticmethod
		def clean_textbox(self):
			raise forms.ValidationError('clean field error')
		