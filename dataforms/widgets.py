from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
#from datetime import date

class NoteWidget(forms.Widget):
	def render(self, name, value, attrs=None):
		return ""
	
class FileWidget(forms.FileInput):
	"""
	A FileField Widget that shows its current value if it has one.
	"""
	def __init__(self, attrs={}):
		super(FileWidget, self).__init__(attrs)

	def render(self, name, value, attrs=None):
		output = []
		output.append(super(FileWidget, self).render(name, value, attrs))
		if value:
			# FIXME:  Possible figure out a way to dynamically pass widget arguments to create the proper file path.
			#if hasattr(value, "name"):
			#	value = "/".join([date.today().strftime(settings.UPLOAD_PATH), value.name])
			
			output.append('<div class="cfile">%s <a target="_blank" href="%s">%s</a></div>' % \
				('Currently:', '/'.join([settings.MEDIA_URL, value]), value))
		return mark_safe(u''.join(output))
	
class AjaxSingleFileWidget(forms.TextInput):
	"""
	A file upload widget which handles a single file and uploads it
	by 
	"""

	def __init__(self, attrs={}):
		super(AjaxSingleFileWidget, self).__init__(attrs)

	def render(self, name, value, attrs=None):
		output = []
		
		files = ''
		if value:
			files = '<li><a href="%s">%s</a></li>' % ('/'.join([settings.MEDIA_URL, value]), value.split("/")[-1])
			
		vals = {
			'name' : name,
			'files' : files
		}
		
		output.append("""
			<div id="button_%(name)s" class="uploadFile">Upload</div>
			<ul class="files">
				%(files)s
			</ul>
			<input id="id_%(name)s" type="hidden" name="%(name)s" value="" />
			
			<script type="text/javascript">
				$(function() {
					var button = $('#button_%(name)s');
					var interval;
					
					var upload_url = '/upload/';
					if (typeof(get_upload_url) != "undefined") {
						upload_url = get_upload_url();
					}
					
					new AjaxUpload(button, {
						action: upload_url,
						name: button.attr("id"),
						onSubmit: function(file, ext){
							button.text('Uploading');
													
							// Disable upload button to allow uploading only 1 file at time
							this.disable();
							
							// Uploading. -> Uploading.. -> Uploading...
							interval = window.setInterval(function(){
								var text = button.text();
								if (text.length < 13){
									button.text(text + '.');					
								} else {
									button.text('Uploading');				
								}
							}, 200);
						},
						onComplete: function(file, response){
							button.text('Upload');
							
							window.clearInterval(interval);
							
							// Enable upload button
							this.enable();
							
							var link = response.split("/");
							link = '<a href="'+response+'">'+link[link.length-1]+'</a>';
							
							// add file to the list
							button.next(".files").html($('<li></li>').html(link));
							
							// Add the path to the hidden variable input in order to save
							button.next(".files").next("input").val(response);
						}
					});
				});
			</script>
		
		""" % vals)
		
		return mark_safe(u''.join(output))