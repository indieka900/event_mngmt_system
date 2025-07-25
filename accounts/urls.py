from django.urls import path
from accounts.views import (
    UserSignUpView, UserLoginView, UserProfileView
)

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]