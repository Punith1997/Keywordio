from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name = "login_view"),
    path('register/', views.register_view, name = "register_view"),
    path('logout/', views.logout_view, name = "logout_view"),
    path('activate/<uidb64>/<token>/', views.activate_view,  name = 'activate'),
    path('forgot_password/', views.forgot_password_view, name = 'forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate_view, name = 'reset_password_validate'),
    path('reset_password/', views.reset_password_view, name = 'reset_password'),
]
