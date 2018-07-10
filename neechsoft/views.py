from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from neechsoft.forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from braces import views

class HomePageView(generic.TemplateView):
	template_name = 'home.html'
# end of HomePageView

class SignUpView(generic.CreateView, views.AnonymousRequiredMixin, views.FormValidMessageMixin):
	form_class = RegistrationForm
	model = User
	success_url = reverse_lazy('login')
	template_name = 'accounts/signup.html'
	form_valid_message = 'Hurray! You are signed right up! Now go-ahead and log in...I know you can do it.'
# end of signupview

class LoginView(generic.FormView, views.AnonymousRequiredMixin, views.FormValidMessageMixin):
	form_class = LoginForm
	success_url = reverse_lazy('home')
	template_name = 'accounts/login.html'
	form_valid_message = 'Hurray! You are logged in!'

	def form_valid(self, form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)

		if user is not None:
			login(self.request, user)
			return super(LoginView, self).form_valid(form)
		else:
			return self.form_invalid(form)
		# end if
	# end of form_valid
# end of LoginView()

class LogOutView(generic.RedirectView, views.LoginRequiredMixin, views.MessageMixin):
	
	url = reverse_lazy('home')

	def get(self, request, *args, **kwargs):
		logout(request)
		self.messages.success("You have been logged out of the system. Come back soon.")
		return super(LogOutView, self).get(request, *args, **kwargs)
	# end of get
# end LogOutView
