from django.shortcuts import redirect, reverse
from django.views.generic import FormView, CreateView, TemplateView
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth import logout

from apps.accounts.models import User
from apps.accounts.forms import UserLoginForm, UserRegistrationForm


class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class NextUrlMixin(object):
    default_next = '/'

    def get_next_url(self):
        next_ = self.request.GET.get('next')
        next_post = self.request.POST.get('next')
        redirect_path = next_ or next_post or None
        if url_has_allowed_host_and_scheme(redirect_path, self.request.get_host()):
            return redirect_path
        return self.default_next


class UserLoginView(TemplateView):
    # template_name = 'base_front.html'
    template_name = 'accounts/accounts.html'

# class UserLoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
#     form_class = UserLoginForm
#     template_name = 'accounts/login.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         response = super().dispatch(request, *args, **kwargs)
#         if request.user.is_authenticated:
#             return redirect("home:home")
#         return response
#
#     def form_valid(self, form):
#         next_path = self.get_next_url()
#         return redirect(next_path)
#
#     def get_context_data(self, **kwargs):
#         context = super(UserLoginView, self).get_context_data(**kwargs)
#         context['title'] = 'Login'
#         return context
#
#     def get_success_url(self):
#         return reverse('home:home')


class UserRegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/registration.html'
    success_message = 'Registration successful :)'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.user.is_authenticated:
            redirect("home:home")
        return response

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data(**kwargs)
        context['title'] = 'Registration'
        return context

    def get_success_url(self):
        return reverse('accounts:login')


def get_logout(request):
    logout(request)
    return redirect('accounts:login')
