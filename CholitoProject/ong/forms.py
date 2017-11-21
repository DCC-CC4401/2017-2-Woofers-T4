from django import forms
from django.contrib.auth.forms import UserCreationForm, User

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.HiddenInput())
    email = forms.EmailField(max_length=200,
                             widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Email"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Nombre"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Contraseña"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Confirma tu contraseña"}))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        if commit:
            user.save()
        return user