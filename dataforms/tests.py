"""
django-dataforms Unit Tests
===========================

This module provides unit tests to ensure integrity and consistency
of the django-dataforms code.

These tests are expected to be run from the `example` directory
and are dependent on the example fixture. 

Usage::

	# From django-dataforms/example/
	./manage.py test dataforms
	
"""

from django.utils import simplejson as json

from . import forms
from .models import DataForm, Collection, Submission
from .test_helpers import RequestFactory, CustomTestCase
rf = RequestFactory()

TEST_FORM_POST_DATA = {
	u'personal-information__textbox': [u'asdf'],
	u'personal-information__checkboxes-multiple': [u'python', u'java'],
	u'personal-information__password': [u'new password!'],
	u'personal-information__languages': [u'java', u'cpp'],
	u'personal-information__p-np': [u'no'],
	u'personal-information__email': [u'email@new-example.com'],
	u'personal-information__dropdown': [u'no'],
	u'personal-information__title': [u'new title'],
	u'personal-information__date': [u'2012-09-11'],
}

TEST_COLLECTION_POST_DATA = {
	u'form-field-dupes__title': [u'This is an example second title'],
	u'form-field-dupes__checkboxes-multiple': [u'java', u'cpp'], 
	u'form-field-dupes__languages': [u'python', u'java'],
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
		self.assertEqual(form.is_valid(), True)
		
		# Try saving the form
		form.save()
		
		# Verify the data was input correctly
		self.assertValidSave(data=TEST_FORM_POST_DATA, submission="myForm")
		
		# Test creation of another bound form tied to a existing Submission
		request = rf.get('/')
		form = forms.create_form(request, form="personal-information", submission="myForm")
		
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
		self.assertEqual(collection.is_valid(), True)
		
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
		
	def testGetAnswers(self):
		# Test getting answers the submission from the tests fixture using a string arg
		answers = forms.get_answers(submission="testSubmission")
		
		# Just make sure it's not empty (could do more I guess)
		self.assertTrue(answers)
		
		# Test the submission from the tests fixture using a Submission object arg
		submission = Submission.objects.get(slug="testSubmission")
		answers = forms.get_answers(submission=submission)
		
		# Just make sure it's not empty (could do more I guess)
		self.assertTrue(answers)
		
	def testValidation(self):
		self.assertEquals(True, True)
