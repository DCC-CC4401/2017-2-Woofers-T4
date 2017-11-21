from django.shortcuts import render, redirect

from django.views import View

from ong.forms import SignUpForm
from ong.models import ONG, ONGUser

class SignUpView(View):
	user_form = SignUpForm(initial={'username': 'dummy'}, prefix='user')
	context = {'user_form': user_form}
	template_name = 'form.html'

	def get(self, request, **kwargs):
		return render(request, self.template_name, self.context)

	# def post(self, request, **kwargs):
 #        user_form = SignUpForm(request.POST, prefix='user')
 #        if user_form.is_valid():
 #            user_ = user_form.save()
 #            user_.refresh_from_db()
 #            natural_user = NaturalUser.objects.create(
 #                user=user_, avatar=avatar_form.cleaned_data.get('avatar'))
 #            username = user_form.cleaned_data.get('email')
 #            raw_password = user_form.cleaned_data.get('password1')
 #            user = authenticate(username=username, password=raw_password)
 #            login(request, user)
 #            return redirect('/')
 #        messages.error(request,
 #                       "Ha ocurrido un error en el registro. Debes ingresar todos los campos para registrarse")
 #        return render(request, self.template_name, context=self.context)


