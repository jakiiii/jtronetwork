from django.urls import path
from apps.accounts.views import (
    UserLoginView,
    UserRegistrationView,
    get_logout
)

app_name = 'accounts'


urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('logout/', get_logout, name='logout'),
]
