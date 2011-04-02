#summary Getting started with dynamic Django dataforms.

= Instant Example =

To see django-dataforms in action, download the source, then go into the `example` folder and run `./manage.py runserver`. Now visit your server and you'll see the dynamically created form. You can also see the data needed to create this form in the administration interface.

This is a single dynamic form which will create Answers in the database when you submit the form.

= Creating your own custom database-driven forms =

== Add the transaction middleware ==

To maintain data integrity, you'll need to add the transaction middleware to your `settings.py`. This will put all queries from each request into a single transaction—so if something goes wrong, all DB changes from the entire request will not be committed.

{{{
MIDDLEWARE_CLASSES = (
	# ...
	'django.middleware.transaction.TransactionMiddleware',	
)
}}}

== Import static files ==

Copy `example/static/scripts/jquery.adminmenusort.js` and `example/static/scripts/bindings.js` to a subdirectory of your MEDIA_URL named `scripts`. So, for example, if your MEDIA_URL was `/static`, then you should copy the file to the folder that serves `/static/scripts/jquery.adminmenusort.js`

== Create your form definition ==

Now, create the definition of your form using the Django admin, creating a dataform and associating the correct fields and choices to fields. 

WRITEME

== Bindings ==

Django-dataforms has built-in support for field bindings (If the user checks "yes" on a field, show another field or fields.) The bindings just need to be defined in the admin when creating your form definition.

WRITEME

== Use the form on a page ==

In a view, you simply have to call `create_form` and pass the submission string

{{{
from dataforms.forms import create_form

def view_function(request):
	form = create_form(request=request, form='personal-information', submission="myForm")
	
	if request.method == "POST":
		if form.is_valid():
			form.save()
}}}

Let's look at the arguments to `create_form`:
 * `request` is the standard view request object, used so that `create_form` can know when the user has submitted POST data so we can repopulate the form and perform validation.
 * `form` is the slug of a DataForm object
 * `submission` is a create-on-use submission name. Meaning, it does not need to exist the first time that `create_form` is called. Once the user submits the form, a Submission object will be created in the background, and this name will be the slug of the Submission object. This is the reference name for how `create_form` is able to repopulate a form from a specific previous submission. A submission slug can be anything you want, which allows you to have multiple submissions from one form definition (because each submission slug is unique).

If `form.save()` is called on a bound form object (a form that is already tied to a Submission), the submitted data will be overwritten in the database allowing for easy editing of previously submitted form data.
