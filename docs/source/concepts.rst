Concepts and Definitions
========================

Below are some important concepts that are helpfull to understand when working
with Dataforms.


Collection
----------

A Dataform collection is a group of Dataform Forms.  A collection can separate out
forms into sections and by doing this, you can render a table of contents.

See the *create_collection* and *BaseCollection* objects in :doc:`forms` for more information. 


Bindings
--------

Bindings are a way of showing and/or hiding certain fields based on the actions
of others fields.  Say you hide certain fields in your form until a uses clicks
on a specific checkbox and then show them.

Bindings can show or hide fields based on the follow conditions:

	*	A Field that is checked or has a value
	*	A Field value that is equal to a specific value
	*	A Field value that is not equal to specific value
	*	A Field value that contains a specific value
	*	A Field value that does not contains a specific value
	
Bindings can be added through the Django admin.


Mappings
--------

You will notice in the Django admin there are three mapping models. (Choice Mappings, Collection Mappings, and Field Mappings)
These are the bridge table relations that connect Choices to Fields, Forms to Collections, and Fields to Forms.

In the future, a re-work of the admin interface is planned to be more intuitive but for now this admin areas
serve as the way to connect the pieces of your forms togethor.

	