.. django-dataforms - Dynamically database driven Django forms master file, created by
   sphinx-quickstart on Thu Apr 14 11:03:55 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Getting Started
===============

Introduction
------------

**django-dataforms** is a Django application that that allows Django forms to be
dynamically data-driven.  Django form logic is abstracted to the database layer.
This allows for quick updates to forms and gives the user access to modify forms
through the Django admin interface.


Requirements
------------

1.	Django 1.3

	**django-dataforms** has only been tested with 1.3.  It might work with previous
	versions, but has not been tested as such.

	
2.	JQuery

	**django-dataforms** uses JQuery for parts of the admin interface.  JQuery-UI
	is also used for date picker fields.
	
	

Installation
------------

To get this application up and running, please follow the steps below:

1.	Create a Django production environment using the setup of your choice.
	Refer to: http://docs.djangoproject.com/en/dev/intro/install/

2.	Create a new Django Project::

		$ django-admin.py startproject <projectname>

3.	Install django-bft to either your PYTHON_PATH or in a folder inside your project:

	*	Install from pip::
	
		$ pip install django-dataforms
		
	*	`Download`__ and install from source::		

		$ python setup.py install
		
	*	Install source to local directory::
	
		$ python setup.py build
		$ cp build/lib/bft /<PROJECT_ROOT>/
		
4.	Add the following to your **settings.py** file:

	*	Add 'dataforms', 'staticfiles' and 'admin' to INSTALLED_APPS::
	
			INSTALLED_APPS = (
				...
				'django.contrib.admin',
				'django.contrib.staticfiles',
				'dataforms',
			)
			
	*	Make sure your static file finders are configured::
	
			STATICFILES_FINDERS = (
			    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
			)
			
	*	To maintain data integrity, you'll need to add the transaction middleware 
		to your `settings.py`. This will put all queries from each request into 
		a single transaction—so if something goes wrong, all DB changes 
		from the entire request will not be committed.::
		
			MIDDLEWARE_CLASSES = (
				# ...
				'django.middleware.transaction.TransactionMiddleware',	
			)
			
5.	Modify **app_settings.py** as needed.  See :doc:`settings` for specifics.

		
6.	Don't forget to collect your static files and sync your database::

		$ python manage.py syncdb
		$ python manage.py collectstatic

	
__ https://github.com/django-dataforms/dango-dataforms/downloads


.. toctree::
   :maxdepth: 2
   :hidden:
   
   usage
   concepts
   settings
   validation
   forms
   diagram
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`