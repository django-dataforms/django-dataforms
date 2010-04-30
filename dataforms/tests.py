"""
django-dataforms Unit Tests
===========================

This module provides unit tests to ensure integrity and consistency
of the django-dataforms code.

These tests are expected to be run from the `example` directory
and are DEPENDENT on the example fixture.

Usage::

	# From django-dataforms/example/
	./manage.py test dataforms
	
"""

from . import forms
from .models import DataForm, Submission, AnswerText
from .test_helpers import RequestFactory, CustomTestCase
from django import template
rf = RequestFactory()

# You can see sample POST data by dumping request.POST before is_valid is called in the view.
# Make sure, if you are changing testing fields, that you update the main initial_data.json fixture.
TEST_FORM_POST_DATA = {
	u'personal-information__profession': [u'programmer'],
	u'personal-information__has-flag': [u'no'],
	u'personal-information__languages': [u'python', u'other'],
	u'personal-information__other-languages': [u'mips\u25c6'],
	#u'personal-information__single-binding-note': [u''], 		# Won't exist in POST
	#u'personal-information__compound-binding-note': [u''],		# Won't exist in POST
	#u'personal-information__other-field-types-note': [u''],	# Won't exist in POST
	u'personal-information__favorite-language': [u'python'],
	u'personal-information__import-antigravity': [u'1'],		# Single checkbox checked = u'1'. Unchecked will not exist.
	u'personal-information__also-heard-of': [u'not-a-chance'],
	u'personal-information__birthday': [u'2011-10-09'],
	u'personal-information__email': [u'test@example.com'],
	u'personal-information__password': [u'n3wPassw0rd!\xbf'],
	#u'personal-information__profile-photo': [u''],				# NotImplemented
	u'personal-information__select-multiple': [u'pick-me-too'],
	u'personal-information__biography' : [u'Not much to say\u2600'],
}

TEST_FORM_POST_DATA2 = {
	u'personal-information__profession': [u'conquistador'],
	u'personal-information__has-flag': [u'yes'],
	#u'personal-information__languages': [u'python', u'other'], # Won't exist in POST if both unchecked
	u'personal-information__other-languages': [u'\u25c6lisp'],
	#u'personal-information__single-binding-note': [u''], 		# Won't exist in POST
	#u'personal-information__compound-binding-note': [u''],		# Won't exist in POST
	#u'personal-information__other-field-types-note': [u''],	# Won't exist in POST
	u'personal-information__favorite-language': [u'python'],
	#u'personal-information__import-antigravity': [u'1'],		# Single checkbox checked = u'1'. Unchecked will not exist.
	u'personal-information__also-heard-of': [u'import-this'],
	u'personal-information__birthday': [u'2012-10-09'],
	u'personal-information__email': [u'test2@example.com'],
	u'personal-information__password': [u'\xbfn3w2Passw0rd!'],
	#u'personal-information__profile-photo': [u''],				# NotImplemented
	u'personal-information__select-multiple': [u'im-all-alone'],
	u'personal-information__biography' : [u'\u2600All about me'],
}

TEST_COLLECTION_POST_DATA = {
	u'form-field-dupes__profession': ['conquistador'],
	u'form-field-dupes__has-flag': [u'yes'],
	u'personal-information__select-multiple': [u'no-choose-me', u'im-all-alone'],
}
TEST_COLLECTION_POST_DATA.update(TEST_FORM_POST_DATA)

class FormsTestCase(CustomTestCase):
	fixtures = ['../dataforms/tests.json']
	
	def testDataFormClass(self):
		# Make sure we're checking for DataForm existence before creation
		self.assertRaises(
			DataForm.DoesNotExist,
			forms._create_form,
			form="non-existent-slug",
			title="Test Title",
			description="Test description"
		)
			
	def testCreateUnboundDataForm(self):
		request = rf.get('/')
		form = forms.create_form(request, form="personal-information", submission="myForm")
		
	def testCreateBountDataForm(self):
		request = rf.post('/form/', TEST_FORM_POST_DATA)
		form = forms.create_form(request, form="personal-information", submission="myForm")
		
	def testSaveDataForm(self):
		request = rf.post('/form/', TEST_FORM_POST_DATA)
		form = forms.create_form(request, form="personal-information", submission="myForm")
		
		# Make sure there's no submission object yet
		self.assertRaises(AttributeError, getattr, form, 'submission')
		
		# Validate the form to populate cleaned_data for the save function
		form.is_valid()
		if form.errors:
			self.fail(form.errors)
		
		# Try saving the form
		form.save()
		
		# Verify the data was input correctly
		self.assertValidSave(data=TEST_FORM_POST_DATA, submission="myForm")
		
		# Test creation of another bound form tied to a existing Submission
		request = rf.get('/')
		form = forms.create_form(request, form="personal-information", submission="myForm")
		
		# Make sure template rendering doesn't throw errors
		x = template.Template("{% for field in form %}{{ field }}{% endfor %}")
		c = template.Context({"form":form})
		x.render(c)
		
		# Ensure Unicode encoding is being returned from models correctly
		answer_texts = AnswerText.objects.all()
		
		for answer_text in answer_texts:
			try:
				answer_text.__unicode__()
			except UnicodeEncodeError:
				self.fail("UnicodeEncodeError: 'ascii' codec can't encode character... Make sure you are using unicode() in every model's __unicode__() function, NOT str()")
		
		# Test re-submission of form with different data to make sure that edits work.
		# Tests for regression of data integrity bug where a checked checkbox
		# could never be un-checked because it would not exist in the form POST.
		request = rf.post('/form/', TEST_FORM_POST_DATA2)
		form = forms.create_form(request, form="personal-information", submission="myForm")
		
		# Validate the form to populate cleaned_data for the save function
		form.is_valid()
		if form.errors:
			self.fail(form.errors)
		
		# Try saving the form
		form.save()
		
		# Verify the data was input correctly
		self.assertValidSave(data=TEST_FORM_POST_DATA2, submission="myForm")
		
	def testCreateUnboundCollection(self):
		request = rf.get('/')
		form = forms.create_form(request, form="personal-information", submission="myForm")
		
	def testCreateBoundCollection(self):
		request = rf.post('/collection/', TEST_COLLECTION_POST_DATA)
		collection = forms.create_collection(request, collection="test-collection", submission="myCollection")
		
	def testSaveCollection(self):
		request = rf.post('/collection/', TEST_COLLECTION_POST_DATA)
		collection = forms.create_collection(request, collection="test-collection", submission="myCollection")
		
		# Validate the form to populate cleaned_data for the save function
		self.assertTrue(collection.is_valid())
		
		# Try saving the form
		collection.save()
		
		# Verify the data was input correctly
		self.assertValidSave(data=TEST_COLLECTION_POST_DATA, submission="myCollection")
		
		# Test creation of another bound collection tied to a existing Submission
		request = rf.get('/')
		collection = forms.create_collection(request, collection="test-collection", submission="myCollection")
		
	def testCreateFormClassTitle(self):
		# Create some test name cases
		data = (
			("my-form-name", "MyFormName"),
			("slugName", "Slugname"),
		)
		
		# Test each name set
		for row in data:
			self.assertEquals(forms.create_form_class_title(row[0]), "%sForm" % row[1])
			
	def testCollectionSlicing(self):
		# FIXME: these tests are incomplete
		
		request = rf.get('/')
		collection = forms.create_collection(request, collection="test-collection", submission="myCollection")
		
		# Should have a collection with length of 2
		self.assertEqual(2, len(collection))

		# Check __getitem__ returns just a DataForm
		self.assertEqual('PersonalInformationForm', str(collection[0].__class__.__name__))
		
		collection = collection[0:1]
		self.assertEqual(1, len(collection))
		
	def testGetAnswers(self):
		# Test getting answers the submission from the tests fixture using a string arg
		answers = forms.get_answers(submission="testSubmission")
		
		# Just make sure it's not empty.
		# FIXME: actually compare data against `tests` fixture
		# FIXME: should verify that answers come back WITHOUT form name prepended
		# (ie. default argument to get_answers of for_form=False) 
		self.assertTrue(answers)
		
		# Test the submission from the tests fixture using a Submission object arg
		submission = Submission.objects.get(slug="testSubmission")
		answers = forms.get_answers(submission=submission, for_form=True)
		
		# Just make sure it's not empty (could do more I guess)
		# FIXME: should verify that answers come back WITH form name prepended
		# (ie. argument to get_answers of for_form=True) 
		self.assertTrue(answers)
		
	def testGetSingleFieldAnswers(self):
		submission = Submission.objects.get(slug="testSubmission")
	
		# Test get_answers when given a single field string
		lang_answer = forms.get_answers(submission, field="other-languages")
		bio_answer = forms.get_answers(submission, field="biography")
	
		self.assertEqual(len(lang_answer), 1, "Too many answers returned! Got: %s, should have: 1." % len(lang_answer))
		self.assertEqual(lang_answer['other-languages'], u'\u2600')

		self.assertEqual(len(bio_answer), 1, "Too many answers returned! Got: %s, should have: 1." % len(bio_answer))
		self.assertEqual(bio_answer['biography'], u'Blah blah blah\u2600')		

	def testGetMultipleFieldAnswers(self):
		submission = Submission.objects.get(slug="testSubmission")
		
		# Test get_answers when given multiple field slugs
		answers = forms.get_answers(submission=submission, for_form=False, field=["other-languages","biography"])

		self.assertEqual(answers['other-languages'], u'\u2600')
		self.assertEqual(answers['biography'], u'Blah blah blah\u2600')
		
	def testValidation(self):
		self.assertEquals(True, True)
