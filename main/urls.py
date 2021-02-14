from django.urls import path
from .views import UserMatched, Message, Iter, Reaction


urlpatterns = [
    path('user-matched/', UserMatched.as_view(), name='user-matched'),
    path('message/<int:id>/', Message.as_view(), name='message'),
    path('iter/', Iter.as_view(), name='iter'),
    path('reaction/<int:id>/', Reaction.as_view(), name='reaction'),
]

