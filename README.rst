**django-dataforms** is a wrapper for the Django forms API that lets you dynamically define forms in a database, rather than hard-coding form definitions. This can be especially helpful for projects that have many forms and/or forms which constantly change, and you don't want to be constantly updating models and schemas. No model creation required.

See the `Wiki`__ for more information.

===============
Go from this...
===============

::

	# forms.py 
	from django import forms

	class ContactForm(forms.Form):
	    subject = forms.CharField(max_length=100)
	    message = forms.CharField()
	    sender = forms.EmailField()
	    cc_myself = forms.BooleanField(required=False)

	# view.py
	def contact(request):
	    if request.method == 'POST':
	        form = ContactForm(request.POST)
	        # ...
	    else:
	        form = ContactForm()

	    return render_to_response('contact.html', {'form': form,})

========
To this!
========

::

	# Now your form is stored in the database and you can
	# change it without changing a model and DB schema!
	create_form(request=request, form="contact-form" submission="mySubmission")

__ https://github.com/django-dataforms/dango-dataforms/wiki/Instant-Example