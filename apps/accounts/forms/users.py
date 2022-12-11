from django import forms
from django.contrib.messages.views import messages
from django.contrib.auth import get_user_model, authenticate, login

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div, Fieldset, HTML, Field, MultiField

from apps.accounts.signals import user_logged_in

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=32, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        data = self.cleaned_data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            msg = messages.error(self.request, "Invalid credentials.")
            raise forms.ValidationError(msg)
        login(self.request, user)
        user_logged_in.send(user.__class__, instance=user, request=self.request)
        return data

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-12 col-12 mb-1'),
                css_class='form-row'
            ),
            Row(
                Column('password', css_class='col-md-12 col-12 mb-1'),
                css_class='row',
                style='margin-top: 5px'
            ),
            Div(Submit('submit', 'Login', css_class='button button-primary button-outline'), style='margin-top: 5px', css_class="text-left btn-block")
        )


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=32, label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
        )
        labels = {
            'first_name': 'First Name*',
            'last_name': 'Last Name*',
            'username': 'username*',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password Don't match!")
        return password2

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-12 col-12 mb-1'),
                css_class='form-row'
            ),
            Row(
                Column('last_name', css_class='col-md-12 col-12 mb-1'),
                css_class='row'
            ),
            Row(
                Column('username', css_class='col-md-12 col-12 mb-1'),
                css_class='row'
            ),
            Row(
                Column('password1', css_class='col-md-12 col-12 mb-1'),
                css_class='row'
            ),
            Row(
                Column('password2', css_class='col-md-12 col-12 mb-1'),
                css_class='row'
            ),
            Div(Submit('submit', 'Registration', css_class='button button-primary button-outline'), style='margin-top: 5px', css_class="text-left btn-block")
        )
