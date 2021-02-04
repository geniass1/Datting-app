from django.urls import path
from . import views
urlpatterns = [
    path('', views.main, name='main'),
    path('like/<int:id>/', views.reaction, name='like'),
    path('iter/', views.iter, name='iter'),
    path('user_matched/', views.user_matched, name='user_matched'),
    path('message/<int:id>/', views.messages, name='messages'),
]
