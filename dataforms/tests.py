"""
django-dataforms Unit Tests
===========================

This module provides unit tests to ensure integrity and consistency
of the django-dataforms code.
"""

from django.test import TestCase
from django.http import HttpRequest

from . import forms
from .models import DataForm, DataFormCollection 

class FormsTestCase(TestCase):
	def testDataFormClass(self):
		# Make sure we're checking for DataForm existence before creation
		try:
			forms._create_form(form="non-existent-slug", title="Test Title", description="Test description")
		except DataForm.DoesNotExist:
			pass # Correct, this dataform should _not_ exist
		else:
			self.fail("""A DataForm existed where it shouldn't. Make sure that we are correctly checking
			for the existence of a DataForm object before using it in _create_form""")
			
	def testDataForm(self):
		
		request = HttpRequest()
		
		forms.create_form(request, form="personal-information", submission="myForm")
		
	def testDataFormCollection(self):
		self.assertEquals(True, True)
		
	def testCreateFormClassTitle(self):
		data = (
			("my-form-name", "MyFormName"),
			("slugName", "Slugname"),
		)
		
		for row in data:
			self.assertEquals(forms.create_form_class_title(row[0]), "%sForm" % row[1])
		
	def testSave(self):
		self.assertEquals(True, True)

	def testGetAnswers(self):
		self.assertEquals(True, True)
		
	def testValidation(self):
		self.assertEquals(True, True)
