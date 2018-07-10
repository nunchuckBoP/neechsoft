# evolv models file
# -------------------------------------------------
from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
today = timezone.now
default_followup = timezone.now() + timezone.timedelta(days=7)  

class ContactType(models.Model):

	# description of the contact type
	desc = models.CharField(max_length=50, default='Non Team Member')
	
	def __str__(self):
		return self.desc
	# end of __str__
# end of ContactType

class Contact(models.Model):
	
	# the user that created the contact
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	contact_type = models.ForeignKey(ContactType, on_delete=models.CASCADE, null=False)
	first_name = models.CharField(max_length=50, blank=False, null=False)
	last_name = models.CharField(max_length=50, blank=True, null=True, default='')
	email = models.EmailField(blank=True, null=True)
	phone = models.CharField(blank=True, null=True, max_length=50)
	created = models.DateField('Creation Date', default=today)
	followup = models.DateField('Follow up Date', default=default_followup)
	last_contact = models.DateField('Last Contact Date', default=today)
	followup_period = models.PositiveSmallIntegerField(default=7, blank=True, null=False)
	notes = models.CharField(max_length=140, null=True, blank=True)
	email_alerts = models.BooleanField(default=True)

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)
	# end of __str__()

	def getStatusUpdates(self):
		return StatusUpdate.objects.filter(contact=self.id)
	# end of getStatusUpdates

# end of Contact

class StatusUpdate(models.Model):
	date = models.DateTimeField(default=today)
	status = models.CharField(max_length=140, null=True)
	interest_level = models.IntegerField(default=1)
	contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)
	update_last_contact_date = models.BooleanField(default=False)

	def __str__(self):
		return "date: %s, status: %s" % (self.date, self.status)
	# end of __str__()

# end of StatusUpdate()

class ExpenseType(models.Model):
	desc = models.CharField(max_length=50, default='')
	def __str__(self):
		return self.desc
	# end of __str__()
# end of expenseType

class Expense(models.Model):
	
	# the user that created the expense
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	
	expense_type = models.ForeignKey(ExpenseType, null=True, on_delete=models.SET_NULL)
	date = models.DateField('Date', default=today)
	desc = models.CharField(max_length=140, null=True)
	amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
	
	def __str__(self):
		return "type: %s, date: %s, description: %s, amount: %s" % (self.expense_type.desc, self.date, self.desc, self.amount)
	# end of __str__()
# end of Expense

class Note(models.Model):

	# the user that created the notes
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	
	timestamp = models.DateTimeField('Timestamp', default=today)
	notes = models.CharField(max_length=1000, null=True)
	
	def __str__(self):
		return "timestamp: %s, notes: %s" % (self.timestamp, self.notes)
	# end of __str__
# end of Notes
