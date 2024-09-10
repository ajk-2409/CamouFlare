from django.urls import path
from .views import signup_view, login_view, home_view, encode_message, decode_message, logout_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('encode/', encode_message, name='encode_message'),
    path('decode/', decode_message, name='decode_message'),
]
