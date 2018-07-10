from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Button, Layout, ButtonHolder, Submit, HTML
from evolv.models import Expense, Contact, StatusUpdate, Note

# global contact fields for the generic views
contact_fields = [
	'contact_type',
	'first_name',
	'last_name',
	'email',
	'phone',
	'created',
	'followup',
	'followup_period',
	'last_contact',
	'email_alerts',
	'notes',
]

status_update_fields = [
	'status',
	'interest_level',
	'update_last_contact_date'
]

expense_fields = [
	'expense_type',
	'date',
	'desc',
	'amount'
]

note_fields = [
	'notes'
]

class EvolvLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(EvolvLoginForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper()

		self.helper.layout = Layout(
			'username',
			'password',
			ButtonHolder(
				Submit('login', 'Login', css_class='btn-primary')
			)
		)
	# end of __init__
# end of LoginForm

class ContactForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		
		self.helper = FormHelper(self)
		self.helper.form_method = "POST"
		
		# adds the button
		self.helper.layout.append(FormActions(Submit('Submit', 'Submit', css_class='btn-primary'), 
									HTML("""<a class="btn btn-warning" href="{% url 'contacts' %}">Cancel</a>""")))
	# end of __init__()
	
	class Meta:
		model = Contact
		fields = contact_fields
	# end of Meta class
# end of ContactForm

class ContactDetailsForm(forms.ModelForm):
	# this is for the status updates
	# form only. The rest of the details
	# are in the template
	def __init__(self, *args, **kwargs):
		super(ContactDetailsForm, self).__init__(*args, **kwargs)
		
		self.helper = FormHelper(self)
		self.helper.form_method = "POST"
		
		# adds the button
		self.helper.layout.append(ButtonHolder(Submit('Submit', 'Submit', css_class='btn-primary')))
	# end of __init__()
	
	class Meta:
		model = StatusUpdate
		fields = status_update_fields
	# end of Meta class
# end of ContactDetailsForm

class StatusUpdateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(StatusUpdateForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_method = "POST"
		self.helper.layout.append(ButtonHolder(Submit('Submit', 'Submit', css_class='btn-primary')))
	# end of __init__
	class Meta:
		model = StatusUpdate
		fields = ['contact', 'date', 'status', 'interest_level', 'update_last_contact_date']
	# end of meta class
# end of StatusUpdateForm

class DeleteForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(DeleteForm, self).__init__(*args, **kwargs)
		
		self.helper = FormHelper(self)
		self.helper.layout = Layout()
		self.helper.layout.append(HTML("""<h4>Are you sure you want to delete {{ object }}?</h4>"""))
		self.helper.layout.append(FormActions(Submit('submit', 'Yes'), 
									HTML("""<a class="btn btn-warning" href={{ next_url }}>Cancel</a>""")))
	# end of __init__()
# end of DeleteForm class

class ExpenseForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ExpenseForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_method = "POST"
		
		self.helper.layout.append(ButtonHolder(Submit('Submit', 'Submit', css_class='btn-primary')))
	# end of __init__()
	class Meta:
		model = Expense
		fields = expense_fields
	# end of Meta class
# end of ExpenseForm class

class NoteForm(forms.ModelForm):
	# this is for the status updates
	# form only. The rest of the details
	# are in the template
	def __init__(self, *args, **kwargs):
		super(NoteForm, self).__init__(*args, **kwargs)
		
		self.helper = FormHelper(self)
		self.helper.form_method = "POST"
		
		# adds the button
		self.helper.layout.append(ButtonHolder(Submit('Submit', 'Submit', css_class='btn-primary')))
	# end of __init__()
	
	class Meta:
		model = Note
		fields = note_fields
	# end of Meta class
# end of ContactDetailsForm
