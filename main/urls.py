from django.urls import path
from . import views
urlpatterns = [
    path('', views.main, name='main'),
    path('like/<int:id>/', views.like, name='like'),
]
