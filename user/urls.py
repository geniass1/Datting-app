from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('change/', views.change_user_info, name='change'),
]
