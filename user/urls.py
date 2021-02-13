from django.urls import path
from . import views
from .views import Register, ChangeInfo, Login
urlpatterns = [
    path('rest-reg/', Register.as_view(), name='rest-reg'),
    path('rest-login/', Login.as_view(), name='rest-login'),
    path('rest-change/', ChangeInfo.as_view(), name='rest-change'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('change/', views.change_user_info, name='change'),
]
