Usage
=====

Use the following examples below as a base for adding Dataforms to your Django views.

**Remember:** For most arguments on create_form and create_collection, you can pass in
the actual object instead of the slug if that object already exists in your code.  This
way it will save extra database calls.

Basic Form
----------
::
   
   from dataforms.forms import create_form
   
   # ...

   form = create_form(request, form="form-slug", submission="submission-slug")

   if request.method == "POST":
      if form.is_valid():
         form.save()
         return redirect(...) 

   return render(request, "index.html", { 'form' : form })
   
   
Basic Collection
----------------
::

   collection = create_collection(request, collection="collection-slug", submission="submission-slug", section="section-slug")

   if request.method == "POST":
      if collection.is_valid():
         collection.save()
         return redirect(...) 

   return render(request, 'collection.html', { 'forms' : collection })
   
   
Example with objects instead of slugs
-------------------------------------
::

   from dataforms.forms import create_form
   from dataforms.models import Submission

   submission = Submission.objects.get(pk=1)

   form = create_form(request, form="form-slug", submission=submission)


Returning a de-coupled Form class object
----------------------------------------

Sometimes it might be nice just to get back a form object that you can use to
save to somewhere else::

   from dataforms.forms import create_form

   FormClass = create_form(request, form="form-slug", submission="submission-slug", return_class=True)
   form = FormClass(request.POST or None)
   
   if form.is_valid():
      # Process the data in form.cleaned_data
      # ...
      
      
Collection with Table of Contents
---------------------------------
Assuming your view has something similiar to the Basic Collection example above, do something like this in your template::

   {% for section in collection.sections %}
      <li class="{% if section == collection.current_section %}bold{% endif %}">
         <a href="...">{{ section.title }}</a>
      </li>
   {% endfor %}

**Remember:** You also have collection.next_section and collection.previous_section available for you to use.

