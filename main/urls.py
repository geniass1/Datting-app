from django.urls import path
from . import views
from .views import UserMatched, Message, Iter, Reaction
urlpatterns = [
    path('rest-user-matched/', UserMatched.as_view(), name='rest-user-matched'),
    path('rest-message/<int:id>/', Message.as_view(), name='rest-message'),
    path('rest-iter/', Iter.as_view(), name='rest-iter'),
    path('rest-reaction/<int:id>/', Reaction.as_view(), name='rest-reaction'),
    path('', views.main, name='main'),
    path('like/<int:id>/', views.reaction, name='like'),
    path('iter/', views.iter, name='iter'),
    path('user_matched/', views.user_matched, name='user_matched'),
    path('message/<int:id>/', views.messages, name='messages'),
]
