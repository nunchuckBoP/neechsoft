from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import RedirectView
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from evolv.models import ContactType, Contact, StatusUpdate, ExpenseType, Expense, Note
from evolv.forms import EvolvLoginForm, ExpenseForm, ContactForm, DeleteForm, ContactDetailsForm, NoteForm
from evolv.forms import StatusUpdateForm
from braces import views
import datetime
import decimal

# global contact fields for the generic views
contact_fields = [
	'contact_type',
	'first_name',
	'last_name',
	'email',
	'phone',
	'followup',
	'followup_period',
	'last_contact',
	'email_alerts',
	'notes',
]

# global login url for the protexted views
login_url = reverse_lazy('evolvLogin')

class EvolvLoginView(FormView, views.AnonymousRequiredMixin, views.FormValidMessageMixin):
	form_class = EvolvLoginForm
	success_url = reverse_lazy('evolvHome')
	template_name = 'accounts/login.html'
	form_valid_message = 'Hurray! You are logged in!'

	def form_valid(self, form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)

		if user is not None:
			login(self.request, user)
			return super(EvolvLoginView, self).form_valid(form)
		else:
			return self.form_invalid(form)
		# end if
	# end of form_valid
# end of LoginView()

class EvolvLogOutView(RedirectView, views.LoginRequiredMixin, views.MessageMixin):
	
	url = reverse_lazy('evolvHome')

	def get(self, request, *args, **kwargs):
		logout(request)
		self.messages.success("You have been logged out of the system. Come back soon.")
		return super(EvolvLogOutView, self).get(request, *args, **kwargs)
	# end of get
# end LogOutView

class EvolvHomePageView(TemplateView):
	template_name = 'evolv.html'
# end of HomePageView

class ContactListView(LoginRequiredMixin, ListView):
	login_url = login_url
	template_name = 'contact_list.html'
	model = Contact
	order_by = 'last_contact'

	class Meta:
		global contact_type
		global contacts
		def __init__(self, contact_type, contacts):
			self.contact_type = contact_type
			self.contacts = contacts
		# end of __init__
	# end of Meta class
	
	def get_context_data(self, **kwargs):
		context = super(ContactListView, self).get_context_data(**kwargs)

		# gets the contacts for the user
		user_contacts = Contact.objects.filter(user=self.request.user)		
		
		# gets all of the contact types
		contact_types = ContactType.objects.all()
		
		_data_objects = []
		for t in contact_types:
			c = user_contacts.order_by(self.order_by).filter(contact_type=t)
			_data_objects.append(self.Meta(t, c))
		# end for
		context['data_objects'] = _data_objects
		return context
	# end of get_context_data
# end of ContactListView

class ContactDetailsView(View, LoginRequiredMixin, views.MessageMixin):
	login_url = login_url
	template_name = 'contact_details.html'
	#fields = contact_fields
	
	def get(self, request, pk, *args, **kwargs):
	
		if request.user.is_authenticated:
			# get the contact
			contact = get_object_or_404(Contact, pk=pk)
		
			# get the status updates for the contact
			status_updates = StatusUpdate.objects.order_by('date').filter(contact=contact)
		
			# form the context object
			context = {'contact': contact, 'status_updates': status_updates, 'form': ContactDetailsForm()}
		
			return render(request, self.template_name, context)
		else:
			return HttpResponseRedirect(login_url)
		# end if
	# end of get
	
	def post(self, request, pk, *args, **kwargs):
		# get the contact object
		contact = get_object_or_404(Contact, pk=pk)
		
		# get the form object
		form_class = ContactDetailsForm
		form = form_class(request.POST)
		
		if form.is_valid():
			# clean the data, and add the ones not in the form
			date = datetime.datetime.now()
			status = form.cleaned_data['status']
			interest_level = form.cleaned_data['interest_level']
			update_last_contact = form.cleaned_data['update_last_contact_date']
			
			s = StatusUpdate(contact=contact, date=date, status=status, interest_level=interest_level,
							update_last_contact_date=update_last_contact)
			s.save()
			
			if(update_last_contact == True):
				# update the contact data
				contact.last_contact = datetime.datetime.now()
				
				# update the followup date based on followup interval
				contact.followup = contact.last_contact + datetime.timedelta(days=contact.followup_period)
				
				# save the contact
				contact.save()
				
			# end if
			self.messages.success("saved update.")
			return HttpResponseRedirect('/evolv/contact/details/%s' % contact.id)
		else:
			self.messages.error("something went wrong.")
			
			# get the contact
			contact = get_object_or_404(Contact, pk=pk)
		
			# get the status updates for the contact
			status_updates = StatusUpdate.objects.order_by('date').filter(contact=contact)
		
			# form the context object
			context = {'contact': contact, 'status_updates': status_updates, 'form': ContactDetailsForm()}
		
			return render(request, self.template_name, context)
		# end if
	# end of post
	
# end of ContactDetailView

# base contact edit view. This is used for create view
# and edit view (DRY)
class ContactCreateView(CreateView, LoginRequiredMixin, views.MessageMixin):
	login_url = login_url
	model = Contact
	template_name = 'contact_form.html'
	initial = {'key': 'value'}
	success_url = reverse_lazy('contacts')
	form_class = ContactForm
	
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return super(ContactCreateView, self).get(request, *args, **kwargs)
		else:
			return HttpResponseRedirect(login_url)
		# end of if
	# end of get
	
	def form_valid(self, form):
		if self.request.user.is_authenticated:
			contact = form.save(commit=False)
			contact.user = self.request.user
			self.messages.success("successfully created contact %s" % contact)
			contact.save()
			return HttpResponseRedirect(self.success_url)
		else:
			return HttpResponseRedirect(self.login_url)
		# end if
	# end of form_valid()
	
# end of ContactEditView

class ContactUpdateView(UpdateView, LoginRequiredMixin, views.MessageMixin):
	login_url = login_url
	model = Contact
	template_name = 'contact_form.html'
	initial = {'key': 'value'}
	success_url = reverse_lazy('contacts')
	form_class = ContactForm
	
	def form_valid(self, form):
		contact = form.save(commit=False)
		self.messages.success("successfully updated contact %s" % contact)
		
		return super(ContactUpdateView, self).form_valid(form)
	# end of form_valid
# end of ContactUpdateView

class ContactDeleteView(View, LoginRequiredMixin, views.MessageMixin):
	template_name = 'delete_confirm.html'
	login_url = login_url
	redirect_url = reverse_lazy('contacts')
	next_url = redirect_url
	def get(self, request, pk, *args, **kwargs):
		
		try:
			self.next_url = request.GET['next']
		except Exception as ex:
			self.next_url = self.redirect_url
		# end of try
		
		# get the contact
		contact = get_object_or_404(Contact, pk=pk)
		
		# form the context object
		context = {'object': contact, 'form': DeleteForm(), "next_url": self.next_url}
		
		return render(request, self.template_name, context)
	# end of get
	def post(self, request, pk, *args, **kwargs):
		# get the contact object
		contact = get_object_or_404(Contact, pk=pk)
		
		# get the form object
		form_class = DeleteForm
		form = form_class(request.POST)
		
		if form.is_valid():
			# delete the contact
			contact.delete()
			self.messages.success("Contact deleted successfully.")
			return HttpResponseRedirect(self.next_url)
		else:
			self.messages.error("Something went wrong.")
			return HttpResponseRedirect(self.next_url)
	# end of post
# end of ContactDeleteView

class StatusUpdateDeleteView(View, LoginRequiredMixin, views.MessageMixin):
	template_name = 'delete_confirm.html'
	login_url = login_url
	redirect_url = reverse_lazy('contacts')
	next_url = redirect_url
	def get(self, request, pk, *args, **kwargs):
		try:
			self.next_url = request.GET['next']
		except Exception as ex:
			self.next_url = self.redirect_url
		# end try
		
		status_update = get_object_or_404(StatusUpdate, pk=pk)
		context = {'object': status_update, 'form': DeleteForm(), 'next_url': self.next_url}
		return render(request, self.template_name, context)
	# end of get
	def post(self, request, pk, *args, **kwargs):
		try:
			self.next_url = request.GET['next']
		except Exception as ex:
			self.next_url = self.redirect_url
		# end of try
		
		status_update = get_object_or_404(StatusUpdate, pk=pk)
		form_class = DeleteForm
		form = form_class(request.POST)
		if form.is_valid():
			status_update.delete()
			self.messages.success("Status update deleted successfully.")
			return HttpResponseRedirect(self.next_url)
		else:
			self.messages.error("Something went wrong.")
			return HttpResponseRedirect(self.next_url)
		# end if
	# end of post
# end of StatusUpdateDeleteView

class StatusUpdateUpdateView(UpdateView, LoginRequiredMixin, views.MessageMixin):
	login_url = login_url
	model = StatusUpdate
	template_name = 'status_update_form.html'
	initial = {'key': 'value'}
	success_url = reverse_lazy('contacts')
	form_class = StatusUpdateForm
	
	def form_valid(self, form):
		status_update = form.save(commit=False)
		
		# should redirect to the same contact page
		self.success_url = '/evolv/contact/details/%s' % status_update.contact.id
		self.messages.success("successfully updated status update.")
		
		return super(StatusUpdateUpdateView, self).form_valid(form)
	# end of form_valid
# end of StatusUpdateUpdateView

class ExpenseListView(View, LoginRequiredMixin, views.MessageMixin):
	
	template_name = 'expense_list.html'
	login_url = login_url
	
	class ExpenseDataObject:
		global expense_type
		global expenses
		global total
		def __init__(self, expense_type, expenses, total):
			self.expense_type = expense_type
			self.expenses = expenses
			self.total = total
		# end of __init__
	# end of ExpenseDataObject class
	
	def get_context_data(self, request, year=None, *args, **kwargs):
		next_year = -1
		prev_year = -1
		if year is not None:
			try:
				year_int = int(year)
				next_year = year_int + 1
				prev_year = year_int - 1
			except Exception as ex:
				self.messages.error("ERROR: %s" % ex)
		# end if
		
		# get the expenses
		expense_types = ExpenseType.objects.all()
		user_expenses = Expense.objects.filter(user=request.user)
		data_objects = []
		total = decimal.Decimal(0.0)
		for t in expense_types:
			if year is not None:
				_expenses = user_expenses.order_by('date').filter(expense_type=t).filter(date__year=year)
			else:
				_expenses = user_expenses.order_by('date').filter(expense_type=t)
			# end if
			
			for e in _expenses:
				total = total + e.amount
			# end of totalling up the expenses
			data_objects.append(self.ExpenseDataObject(t, _expenses, total))
		# end for
		
		# context (data we are passing onto the view)
		if year is not None:
			context = {"data_objects": data_objects, 'form': ExpenseForm(), 'year_view':True, 'year': year, 'next_year': next_year, 'prev_year': prev_year}
		else:
			context = {"data_objects": data_objects, 'form': ExpenseForm(), 'year_view':False}
		
		return render(request, self.template_name, context)
	
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return self.get_context_data(request, *args, **kwargs)
		else:
			# redirect to the login page
			return HttpResponseRedirect(login_url)
		# end if
		
	def post(self, request, *args, **kwargs):
	
		# get the form object
		form_class = ExpenseForm
		form = form_class(request.POST)
		
		if form.is_valid():
			user = request.user
			expense_type = form.cleaned_data['expense_type']
			date = form.cleaned_data['date']
			desc = form.cleaned_data['desc']
			amount = form.cleaned_data['amount']
			
			e = Expense(user=user, expense_type=expense_type, date=date, desc=desc, amount=amount)
			e.save()
			
			self.messages.success("successfully saved expense.")
			
			return HttpResponseRedirect(request.get_full_path())
		else:
			# redo the get
			self.messages.error("something went wrong.")
			return self.get_context_data(self, request, *args, **kwargs)
		# end if
	# end of post
# end of ExpenseListView

class ExpenseListViewYear(ExpenseListView, LoginRequiredMixin, views.MessageMixin):
	login_url = login_url
	def get(self, request, year, *args, **kwargs):
		if request.user.is_authenticated:
			return self.get_context_data(request, year, *args, **kwargs)
		else:
			return HttpResponseRedirect(login_url)
		# end if
	# end of get
# end of ExpenseListViewYear

class ExpenseUpdateView(UpdateView, LoginRequiredMixin, views.MessageMixin):
	login_url = login_url
	model = Expense
	template_name = 'expense_form.html'
	initial = {'key': 'value'}
	success_url = reverse_lazy('expenses')
	form_class = ExpenseForm
	
	def form_valid(self, form):
		expense = form.save(commit=False)
		self.messages.success("successfully updated expense.")
		
		return super(ExpenseUpdateView, self).form_valid(form)
	# end of form_valid
# end of expenseupdateview

class ExpenseDeleteView(View, LoginRequiredMixin, views.MessageMixin):
	template_name = 'delete_confirm.html'
	login_url = login_url
	redirect_url = reverse_lazy('expenses')
	global next_url
	
	def get(self, request, pk, *args, **kwargs):
		
		try:
			self.next_url = request.GET['next']
		except Exception as ex:
			self.next_url = self.redirect_url
		# end of try
		
		# get the expense
		expense = get_object_or_404(Expense, pk=pk)
		
		# form the context object
		context = {'object': expense, 'form': DeleteForm(), 'next_url': self.next_url}
		
		return render(request, self.template_name, context)
	# end of get
	def post(self, request, pk, *args, **kwargs):
		
		try:
			self.next_url = request.GET['next']
		except Exception as ex:
			self.next_url = self.redirect_url
		# end of try
		
		# get the contact object
		expense = get_object_or_404(Expense, pk=pk)
		
		# get the form object
		form_class = DeleteForm
		form = form_class(request.POST)
				
		if form.is_valid():
			# delete the contact
			expense.delete()
			redirect_url = '/evolv/expense'
			self.messages.success("Expense deleted successfully.")
			return HttpResponseRedirect(self.next_url)
		else:
			self.messages.error("Something went wrong.")
			return HttpResponseRedirect(self.next_url)
		# end if
	# end of post
# end of ExpenseDeleteView

class NoteListView(View, LoginRequiredMixin, views.MessageMixin):
	template_name = 'note_list.html'
	login_url = login_url
	
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			
			note_objects = Note.objects.order_by('timestamp').filter(user=request.user)
			form = NoteForm()
			
			context = {'note_objects': note_objects, 'form': form}
			
			return render(request, self.template_name, context)
			
		else:
			return HttpResponseRedirect(login_url)
		# end if
	# end of get
	def post(self, request, *args, **kwargs):
	
		form_class = NoteForm
		form = form_class(request.POST)
		
		if form.is_valid():
			user = self.request.user
			notes = form.cleaned_data['notes']
			note = Note(user=user, notes=notes)
			
			note.save()
			self.messages.success("note saved.")
			return HttpResponseRedirect(reverse_lazy('notes'))
		else:
			self.messages.error("something went wrong.")
			return HttpResponseRedirect(reverse_lazy('notes'))
		# end of if
	# end of post
# end of NoteListView
